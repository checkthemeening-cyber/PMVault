#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日経ニュース収集・サマリスキル（改善版）
5つのカテゴリから毎日のニュースを収集し、Markdownファイルとして記録する。
Cookie ベース認証で有料記事の本文取得に対応。

実行方法:
  python nikkei-news.py [morning|evening|monthly|yearly]

実行例:
  python nikkei-news.py morning     # 朝の収集（デフォルト）
  python nikkei-news.py evening     # 夕方の収集
  python nikkei-news.py monthly     # 月次サマリ作成
  python nikkei-news.py yearly      # 年次サマリ作成
"""

import sys
import os
from datetime import datetime, timedelta, timezone
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import time
import urllib.request
import urllib.parse
from http.cookiejar import Cookie, CookieJar
from html.parser import HTMLParser

# ニュース監視カテゴリ設定
CATEGORIES = {
    "資源エネルギー": "https://www.nikkei.com/business/energy/",
    "建設・不動産": "https://www.nikkei.com/business/realestate/",
    "物流・運輸": "https://www.nikkei.com/business/logistics/",
    "商社・卸売り": "https://www.nikkei.com/business/wholesale/",
    "自動車": "https://www.nikkei.com/business/vehicles-machinery/",
}

BASE_DIR = Path(__file__).parent.parent.parent / "nikkei-news"
COOKIE_FILE = Path(__file__).parent / "nikkei-cookies.txt"


class HTMLArticleParser(HTMLParser):
    """HTML から記事本文を抽出するパーサー（新しい日経新聞の構造に対応）"""

    def __init__(self):
        super().__init__()
        self.in_title = False
        self.in_subtitle = False
        self.in_body = False
        self.title = ""
        self.subtitle = ""
        self.body_parts = []
        self.current_text = ""
        self.is_member_only = False  # 会員限定記事フラグ
        self.title_found = False
        self.subtitle_found = False
        self.body_found = False

    def _class_matches(self, class_attr: str, patterns: List[str]) -> bool:
        """クラス属性が複数のパターンのいずれかにマッチするか確認"""
        if not class_attr:
            return False

        class_list = class_attr.split()
        for pattern in patterns:
            # 完全一致
            if pattern in class_list:
                return True
            # プレフィックスマッチ（例: body_* で始まるクラス）
            if pattern.endswith('*'):
                prefix = pattern[:-1]
                for cls in class_list:
                    if cls.startswith(prefix):
                        return True
        return False

    def handle_starttag(self, tag, attrs):
        """タグの開始を処理"""
        attrs_dict = dict(attrs)

        # 会員限定記事を検出
        if tag == "k-lock-banner":
            self.is_member_only = True

        # 記事タイトル（複数のセレクタをカスケード）
        if tag == "h1" and not self.title_found:
            class_attr = attrs_dict.get("class", "")
            # 新規セレクタ: title_t3guga0（通常記事）、/prime/ 記事、旧セレクタ
            if self._class_matches(class_attr, ["title_t3guga0", "index-module*", "cmn-article-title"]):
                self.in_title = True
                self.title_found = True
            # フォールバック: 最初の h1 タグ（他の形式の記事）
            elif not self.title_found and not class_attr:
                self.in_title = True
                self.title_found = True

        # サブタイトル（リード文）（複数のセレクタをカスケード）
        if tag == "p" and not self.subtitle_found:
            class_attr = attrs_dict.get("class", "")
            # 新規セレクタ: descriptionTitle_d1r1zct3、旧セレクタ: cmn-article-subtitle
            if self._class_matches(class_attr, ["descriptionTitle_d1r1zct3", "cmn-article-subtitle"]):
                self.in_subtitle = True
                self.subtitle_found = True

        # 記事本文（複数のセレクタをカスケード）
        # 通常記事: body_* / article-body
        # /prime/ 記事: paragraph-node-module* / article-section-module*
        if tag == "div" and not self.body_found:
            class_attr = attrs_dict.get("class", "")
            if self._class_matches(class_attr, ["body_*", "article-body", "paragraph-node-module*", "article-section-module*"]):
                self.in_body = True
                self.body_found = True

        # /prime/ パスの article タグも本文として処理
        if tag == "article" and not self.body_found:
            class_attr = attrs_dict.get("class", "")
            if self._class_matches(class_attr, ["article-section-module*"]):
                self.in_body = True
                self.body_found = True

    def handle_endtag(self, tag):
        """タグの終了を処理"""
        if tag == "h1" and self.in_title:
            self.in_title = False

        if tag == "p" and self.in_subtitle:
            if self.current_text.strip():
                self.subtitle = self.current_text.strip()
            self.current_text = ""
            self.in_subtitle = False

        if tag == "div" and self.in_body:
            self.in_body = False

    def handle_data(self, data):
        """テキストデータを処理"""
        text = data.strip()
        if text:
            if self.in_title:
                self.title += text
            elif self.in_subtitle:
                self.current_text += text + " "
            elif self.in_body:
                self.body_parts.append(text)


class CookieManager:
    """Netscape Cookie ファイル形式の Cookie を管理"""

    @staticmethod
    def load_cookies(cookie_file: Path) -> Dict[str, str]:
        """Netscape HTTP Cookie File 形式から Cookie を読み込む"""
        cookies = {}

        if not cookie_file.exists():
            print(f"警告: Cookie ファイルが見つかりません: {cookie_file}")
            return cookies

        try:
            with open(cookie_file, 'r', encoding='utf-8') as f:
                for line in f:
                    # コメント行とヘッダーをスキップ
                    if line.startswith('#') or not line.strip():
                        continue

                    # フィールド分割：domain, flag, path, secure, expiration, name, value
                    parts = line.strip().split('\t')
                    if len(parts) >= 7:
                        name = parts[5]
                        value = parts[6]
                        cookies[name] = value

            print(f"Cookie を読み込みました: {len(cookies)} 個")
            return cookies

        except Exception as e:
            print(f"エラー: Cookie ファイルの読み込みに失敗: {e}")
            return cookies

    @staticmethod
    def build_cookie_header(cookies: Dict[str, str]) -> str:
        """Cookie 辞書から HTTP Cookie ヘッダー値を生成"""
        if not cookies:
            return ""
        return "; ".join([f"{k}={v}" for k, v in cookies.items()])


class WebFetcher:
    """Cookie 認証付きの Web フェッチ"""

    DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

    def __init__(self, cookies: Optional[Dict[str, str]] = None):
        """初期化"""
        self.cookies = cookies or {}

    def fetch(self, url: str, timeout: int = 10) -> Optional[str]:
        """URL を取得して HTML を返す"""
        try:
            req = urllib.request.Request(url)

            # User-Agent を設定
            req.add_header('User-Agent', self.DEFAULT_USER_AGENT)

            # Cookie を設定
            if self.cookies:
                cookie_header = CookieManager.build_cookie_header(self.cookies)
                req.add_header('Cookie', cookie_header)

            # リダイレクト対応
            with urllib.request.urlopen(req, timeout=timeout) as response:
                html = response.read().decode('utf-8', errors='ignore')
                return html

        except urllib.error.HTTPError as e:
            print(f"HTTP エラー {e.code}: {url}")
            return None
        except Exception as e:
            print(f"フェッチエラー: {url} - {e}")
            return None


def extract_article_body(html: str) -> Dict[str, str]:
    """HTML から記事本文を抽出（会員限定記事対応）"""
    try:
        parser = HTMLArticleParser()
        parser.feed(html)

        body_text = "\n".join(parser.body_parts).strip()

        # 会員限定記事の場合、本文の先頭に注記を追加
        if parser.is_member_only and not body_text:
            body_text = "【会員限定記事】本文は有料記事のため取得できません。タイトルとリード文のみ表示しています。"
        elif parser.is_member_only:
            body_text = "【会員限定記事】\n\n" + body_text

        return {
            "title": parser.title.strip(),
            "subtitle": parser.subtitle.strip(),
            "body": body_text,
            "is_member_only": parser.is_member_only
        }
    except Exception as e:
        print(f"HTML パースエラー: {e}")
        return {"title": "", "subtitle": "", "body": "", "is_member_only": False}


class NikkeiNewsCollector:
    """日経ニュース収集・サマリクラス"""

    def __init__(self):
        """初期化"""
        self.base_dir = BASE_DIR
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.jst = self._get_jst_time()

        # Cookie を読み込む
        self.cookies = CookieManager.load_cookies(COOKIE_FILE)
        self.fetcher = WebFetcher(self.cookies)

    @staticmethod
    def _get_jst_time() -> datetime:
        """現在時刻をJSTで取得"""
        # UTC タイムゾーン対応版
        now_utc = datetime.now(timezone.utc)
        jst_offset = timedelta(hours=9)
        return now_utc + jst_offset

    def _format_datetime_jst(self) -> str:
        """現在時刻をJST形式でフォーマット"""
        return self.jst.strftime("%Y年%m月%d日 %H:%M")

    def _get_date_dir(self, date: datetime) -> Path:
        """日付ディレクトリパスを取得"""
        return self.base_dir / "daily" / f"{date.year:04d}" / f"{date.month:02d}" / f"{date.day:02d}"

    def _fetch_news_real(self, category_name: str, category_url: str) -> List[Dict]:
        """
        実際のニュースを取得する（Cookie 認証対応）
        """
        articles = []

        # カテゴリページを取得
        html = self.fetcher.fetch(category_url)
        if not html:
            print(f"  警告: {category_name} のページ取得に失敗しました")
            return articles

        # 記事リンクを抽出（正規表現）
        # 注: URL は https://www.nikkei.com/{path}/article/XXX の形式
        # /prime/, /business/ などの中間パスを含む可能性がある
        article_urls = re.findall(
            r'href="(https://www\.nikkei\.com/[^"]*?/article/[^"]+)"',
            html
        )

        print(f"  検出された記事数: {len(article_urls)}")

        # 各記事の詳細を取得
        for article_url in article_urls[:10]:  # 最新10件のみ処理
            time.sleep(0.5)  # サーバーへの負荷軽減
            article_html = self.fetcher.fetch(article_url)

            if article_html:
                article_data = extract_article_body(article_html)

                # 公開日時を抽出
                date_match = re.search(
                    r'(\d{4}年\d{1,2}月\d{1,2}日)\s+(\d{1,2}):(\d{2})',
                    article_html
                )

                if date_match:
                    date_str = date_match.group(1)
                    hour = date_match.group(2).zfill(2)
                    minute = date_match.group(3)
                else:
                    date_str = self.jst.strftime("%Y年%m月%d日")
                    hour = f"{self.jst.hour:02d}"
                    minute = f"{self.jst.minute:02d}"

                # 有料記事かどうかを判定（parser のフラグと HTML テキストから併合判定）
                is_member_only = article_data.get("is_member_only", False)
                is_paid = is_member_only or "有料記事" in article_html or "プレミアム" in article_html

                article_info = {
                    "title": article_data.get("title", ""),
                    "date": date_str,
                    "time": f"{hour}:{minute}",
                    "url": article_url,
                    "summary": article_data.get("subtitle", ""),
                    "body": article_data.get("body", ""),
                    "is_paid": is_paid
                }

                if article_info["title"]:  # タイトルが取得できた場合のみ追加
                    articles.append(article_info)

        return articles

    def _mock_fetch_news(self, category_name: str, url: str) -> List[Dict]:
        """
        テスト用のモックデータ
        """
        # テスト用のモックデータを返す
        today_str = self.jst.strftime("%Y年%m月%d日")

        mock_articles = {
            "資源エネルギー": [
                {
                    "title": "太陽光発電の新規案件、上期で過去最高 脱炭素投資加速",
                    "date": today_str,
                    "time": f"{self.jst.hour:02d}:{self.jst.minute:02d}",
                    "url": "https://www.nikkei.com/article/example-001/",
                    "summary": "再生可能エネルギーの導入加速により、太陽光発電の新規案件が上期で過去最高を記録。",
                    "body": "太陽光発電事業の新規案件が上期で過去最高に達した。国内大手企業を含む複数の事業者が大規模プロジェクトへの投資を発表している。\n\n脱炭素化目標の達成に向けた企業投資が一段と勢いを増しており、産業全体での供給能力拡大が進んでいる。\n\nこの動向は長期的な成長トレンドの一部であり、関連産業への好影響が期待される。",
                    "is_paid": False
                },
                {
                    "title": "原油高騰、ガソリン価格に波及 夏場の値上げ圧力強まる",
                    "date": today_str,
                    "time": f"{self.jst.hour-1:02d}:{30:02d}",
                    "url": "https://www.nikkei.com/article/example-002/",
                    "summary": "中東情勢の不透明性が継続し、原油相場は高止まり。",
                    "body": "中東情勢の不透明性を受け、原油相場は1バレル当たり80ドル台での高止まりが続いている。これに伴い、ガソリン価格への波及が不可避な状況となっている。\n\n主要石油企業は7月中旬での価格改定を予定しており、ガソリンスタンドでの値上げが相次ぐ見通しだ。消費者負担の増加が懸念される。",
                    "is_paid": True
                }
            ],
            "建設・不動産": [
                {
                    "title": "オフィス空き家率、地方で上昇加速 テレワーク普及で需要減",
                    "date": today_str,
                    "time": f"{self.jst.hour:02d}:{self.jst.minute-5:02d}",
                    "url": "https://www.nikkei.com/article/example-003/",
                    "summary": "テレワークの定着に伴い、地方のオフィス空き家率が加速度的に上昇。",
                    "body": "テレワークの定着に伴い、地方都市のオフィス空き家率が加速度的に上昇している。大阪や福岡などの主要都市でも空室率が6ポイント以上上昇。\n\nこれまでのオフィス空間は賃貸住宅や商業施設への用途転換が進んでおり、都市再開発の在り方が大きく変わろうとしている。",
                    "is_paid": False
                }
            ],
            "物流・運輸": [
                {
                    "title": "トラック運転手不足、物流企業が賃上げで確保急ぐ",
                    "date": today_str,
                    "time": f"{self.jst.hour-2:02d}:{15:02d}",
                    "url": "https://www.nikkei.com/article/example-004/",
                    "summary": "労働力不足が深刻化する物流業界。主要企業が積極的な賃上げで人材確保に奔走。",
                    "body": "物流業界の人手不足が深刻化している。ヤマト運輸やKG ロジスティクスなど主要企業が、賃上げや待遇改善で人材確保に奔走している。\n\n業界全体での人員不足は配送遅延のリスク要因となっており、各社は自動化投資と人材確保を並行して推進している。",
                    "is_paid": False
                }
            ],
            "商社・卸売り": [
                {
                    "title": "大手商社、脱炭素事業に今年2兆円超投資 成長事業軸に",
                    "date": today_str,
                    "time": f"{self.jst.hour-3:02d}:{45:02d}",
                    "url": "https://www.nikkei.com/article/example-005/",
                    "summary": "脱炭素化への対応が商社の経営戦略の中核へ。新規事業投資が急増。",
                    "body": "大手総合商社5社が2026年度に脱炭素関連事業へ2兆円超の投資を計画。従来の商取引から再生可能エネルギーや環境関連事業へのシフトが加速している。\n\n利益構造の転換が急速に進み、次世代の成長エンジンとしての位置づけが確定しつつある。",
                    "is_paid": False
                }
            ],
            "自動車": [
                {
                    "title": "EV電池工場、国内新設相次ぐ 北米販売強化に対応",
                    "date": today_str,
                    "time": f"{self.jst.hour-4:02d}:{30:02d}",
                    "url": "https://www.nikkei.com/article/example-006/",
                    "summary": "EV普及に伴い、国内の電池工場新設計画が相次いで発表。",
                    "body": "EV普及加速に対応し、国内での電池工場新設計画が相次いで発表されている。トヨタ・パナソニック、ホンダなど主力メーカーが北米市場強化に向けた投資を加速。\n\n国内製造業の競争力維持が急務となる中、政府の補助金制度の活用も進んでいる。",
                    "is_paid": False
                },
                {
                    "title": "自動運転技術、走行距離と精度で新段階へ 5年内実用化目指す",
                    "date": today_str,
                    "time": f"{self.jst.hour-5:02d}:{20:02d}",
                    "url": "https://www.nikkei.com/article/example-007/",
                    "summary": "自動運転技術の開発競争が激化。複数の企業が5年内の実用化を標榜。",
                    "body": "自動運転技術開発競争が激化している。テスラ、Waymo、中国の自動運転ベンチャーなどが技術実証を加速し、2030年前後の本格実用化を目指している。\n\n走行距離の延伸と認識精度の向上が次のマイルストーンであり、大手自動車メーカーも開発投資を倍増させている。",
                    "is_paid": True
                }
            ]
        }

        # 該当カテゴリのモックデータを返す
        return mock_articles.get(category_name, [])

    def _create_article_entry(self, article: Dict, index: int = 1) -> str:
        """記事エントリを作成（本文付き）"""
        entry = f"### {index}. {article['title']}\n\n"
        entry += f"**公開日時**: {article['date']} {article['time']}\n"
        entry += f"**URL**: {article['url']}\n\n"

        if article['is_paid']:
            entry += f"**【有料記事】**\n\n"

        # リード文
        if article.get('summary'):
            entry += f"> {article['summary']}\n\n"

        # 本文
        body = article.get('body', '')
        if body:
            # 本文を段落で分割
            paragraphs = [p.strip() for p in body.split('\n') if p.strip()]
            entry += "\n\n".join(paragraphs) + "\n"
        else:
            entry += "> 本文の取得に失敗しました\n"

        return entry

    def collect_morning(self):
        """morning モード: 当日記事を収集（本文付き）"""
        print(f"[morning] {self._format_datetime_jst()} の収集を開始します")

        date_dir = self._get_date_dir(self.jst)
        date_dir.mkdir(parents=True, exist_ok=True)

        for category_name, category_url in CATEGORIES.items():
            print(f"  → {category_name} を収集中...")

            # ニュースを取得（Cookie がある場合はリアル、ない場合はモック）
            if self.cookies:
                articles = self._fetch_news_real(category_name, category_url)
            else:
                articles = self._mock_fetch_news(category_name, category_url)

            # ファイルを作成
            file_path = date_dir / f"{category_name}.md"

            content = f"# {category_name} ニュースサマリ\n\n"
            content += f"**収集日時**: {self._format_datetime_jst()} (JST)\n"
            content += f"**ソース**: {category_url}\n"
            content += f"**収集記事数**: {len(articles)}件（当日分）\n"
            content += f"**認証**: {'Cookie 認証有効' if self.cookies else 'Cookie なし（モック表示）'}\n\n"
            content += "---\n\n"

            if articles:
                # 本日のまとめを作成
                content += "## 本日のまとめ\n\n"
                summary_text = self._generate_summary(category_name, articles)
                content += f"{summary_text}\n\n"
                content += "---\n\n"

                # 記事一覧を本文付きで作成
                content += "## 記事一覧（本文付き）\n\n"
                for i, article in enumerate(articles, 1):
                    content += self._create_article_entry(article, i)
                    content += "\n---\n\n"
            else:
                content += "## 本日のまとめ\n\n"
                content += "本日の新着記事はありません\n\n"

            # ファイルに保存
            file_path.write_text(content, encoding='utf-8')
            print(f"    保存完了: {file_path}")

        print(f"[morning] 収集完了")

    def collect_evening(self):
        """evening モード: 新着記事のみを追記（本文付き）"""
        print(f"[evening] {self._format_datetime_jst()} の更新を開始します")

        date_dir = self._get_date_dir(self.jst)

        for category_name, category_url in CATEGORIES.items():
            file_path = date_dir / f"{category_name}.md"

            if not file_path.exists():
                print(f"  → {category_name} の朝のファイルが見つかりません（morning モードを先に実行してください）")
                continue

            print(f"  → {category_name} の新着を確認中...")

            # 朝のファイルから既収集URLを抽出
            content = file_path.read_text(encoding='utf-8')
            existing_urls = set(re.findall(r'\*\*URL\*\*: (https?://[^\s]+)', content))

            # 新規記事を取得（Cookie がある場合はリアル、ない場合はモック）
            if self.cookies:
                articles = self._fetch_news_real(category_name, category_url)
            else:
                articles = self._mock_fetch_news(category_name, category_url)

            new_articles = [a for a in articles if a['url'] not in existing_urls]

            if new_articles:
                # 既存ファイルに追記
                update_text = f"\n\n---\n\n## 夕刊更新（{self._format_datetime_jst()} 追記）\n\n"
                start_idx = len(existing_urls) + 1
                for i, article in enumerate(new_articles, start=start_idx):
                    update_text += self._create_article_entry(article, i)
                    update_text += "\n---\n\n"

                file_path.write_text(content + update_text, encoding='utf-8')
                print(f"    {len(new_articles)}件の新着を追記: {file_path}")
            else:
                # 新着がない場合は追記メッセージのみ
                update_text = f"\n\n---\n\n## 夕刊更新（{self._format_datetime_jst()} 追記）\n\n本時点での新着記事はありませんでした。\n"
                file_path.write_text(content + update_text, encoding='utf-8')
                print(f"    新着記事なし: {file_path}")

        print(f"[evening] 更新完了")

    def collect_monthly(self):
        """monthly モード: 月次サマリを作成"""
        # 前月を対象とする
        target_date = self.jst.replace(day=1) - timedelta(days=1)

        print(f"[monthly] {target_date.year}年{target_date.month}月 の月次サマリを作成します")

        daily_dir = self.base_dir / "daily" / f"{target_date.year:04d}" / f"{target_date.month:02d}"

        if not daily_dir.exists():
            print(f"  対象月のファイルが見つかりません")
            return

        # 月次ディレクトリを作成
        monthly_dir = self.base_dir / "monthly" / f"{target_date.year:04d}"
        monthly_dir.mkdir(parents=True, exist_ok=True)

        # 日次ファイルを集約
        monthly_summary = self._create_monthly_summary(target_date, daily_dir)

        # 保存
        file_path = monthly_dir / f"{target_date.month:02d}_summary.md"
        file_path.write_text(monthly_summary, encoding='utf-8')
        print(f"  保存完了: {file_path}")

    def collect_yearly(self):
        """yearly モード: 年次サマリを作成"""
        # 前年を対象とする
        target_year = self.jst.year - 1

        print(f"[yearly] {target_year}年 の年次サマリを作成します")

        monthly_dir = self.base_dir / "monthly" / f"{target_year:04d}"

        if not monthly_dir.exists():
            print(f"  対象年の月次ファイルが見つかりません")
            return

        # 年次ディレクトリを作成
        yearly_dir = self.base_dir / "yearly"
        yearly_dir.mkdir(parents=True, exist_ok=True)

        # 月次ファイルを集約
        yearly_summary = self._create_yearly_summary(target_year, monthly_dir)

        # 保存
        file_path = yearly_dir / f"{target_year}_summary.md"
        file_path.write_text(yearly_summary, encoding='utf-8')
        print(f"  保存完了: {file_path}")

    def _generate_summary(self, category_name: str, articles: List[Dict]) -> str:
        """記事からサマリを生成（モック実装）"""
        if not articles:
            return "本日の新着記事はありません"

        # シンプルなサマリテンプレート
        summaries = {
            "資源エネルギー": "エネルギー市場では供給面での課題と価格動向が引き続き注目されている。脱炭素化への取り組みと国際的なエネルギー情勢のバランスが、今後の業界動向を左右する重要な要素となっている。",
            "建設・不動産": "不動産市場ではテレワーク普及に伴う用途転換と、都市開発の再構想が進行中。供給過剰地域と需要地域の二極化が進展している。",
            "物流・運輸": "物流業界は人材不足と運送コスト上昇という二重の課題に直面。効率化投資と待遇改善が急務となっており、業界全体の構造改革が加速している。",
            "商社・卸売り": "商社セクターでは脱炭素化と新興市場への事業展開が経営戦略の中核へシフト。従来の商取引モデルから機能転換を迫られている。",
            "自動車": "自動車業界ではEV化と自動運転技術開発が経営資源の集約先。競争の激化に伴い、産業再編の可能性も高まっている。"
        }

        return summaries.get(category_name, "本日のニュース動向をご確認ください")

    def _create_monthly_summary(self, target_date: datetime, daily_dir: Path) -> str:
        """月次サマリを作成"""
        summary = f"# {target_date.year}年{target_date.month:02d}月 ニュース月次サマリ\n\n"
        summary += f"**対象期間**: {target_date.year}年{target_date.month}月1日〜{target_date.month}月末日\n"
        summary += f"**作成日時**: {self._format_datetime_jst()}\n\n"
        summary += "---\n\n"

        summary += "## 月間まとめ（全カテゴリ横断）\n\n"
        summary += "本月の重要なニュース動向と業界横断的なトレンドを記載します。\n\n"
        summary += "---\n\n"

        for category_name in CATEGORIES.keys():
            summary += f"## {category_name}\n\n"
            summary += f"### 月間まとめ\n\n"
            summary += f"{category_name}分野の月間動向をまとめます。\n\n"
            summary += "### 月間主要ニュース Top5\n\n"
            summary += "1. （記事タイトル1）\n"
            summary += "2. （記事タイトル2）\n"
            summary += "3. （記事タイトル3）\n"
            summary += "4. （記事タイトル4）\n"
            summary += "5. （記事タイトル5）\n\n"
            summary += "---\n\n"

        return summary

    def _create_yearly_summary(self, target_year: int, monthly_dir: Path) -> str:
        """年次サマリを作成"""
        summary = f"# {target_year}年 ニュース年次サマリ\n\n"
        summary += f"**対象期間**: {target_year}年1月〜12月\n"
        summary += f"**作成日時**: {self._format_datetime_jst()}\n\n"
        summary += "---\n\n"

        summary += "## 年間まとめ（全カテゴリ横断）\n\n"
        summary += f"{target_year}年を通じた重要なニュース動向と業界横断的なトレンドを記載します。\n\n"
        summary += "### 来年への示唆\n\n"
        summary += "- 各カテゴリの展望を箇条書きで記述\n\n"
        summary += "---\n\n"

        for category_name in CATEGORIES.keys():
            summary += f"## {category_name}\n\n"
            summary += "### 年間まとめ\n\n"
            summary += f"{category_name}分野の年間動向をまとめます。\n\n"
            summary += "### 年間重大ニュース Top10\n\n"
            for i in range(1, 11):
                summary += f"{i}. （重大ニュース{i}）\n"
            summary += "\n---\n\n"

        return summary


def main():
    """メイン処理"""
    mode = sys.argv[1] if len(sys.argv) > 1 else "morning"

    if mode not in ["morning", "evening", "monthly", "yearly"]:
        print(f"エラー: 不正なモード '{mode}'")
        print("使用方法: python nikkei-news.py [morning|evening|monthly|yearly]")
        sys.exit(1)

    collector = NikkeiNewsCollector()

    if mode == "morning":
        collector.collect_morning()
    elif mode == "evening":
        collector.collect_evening()
    elif mode == "monthly":
        collector.collect_monthly()
    elif mode == "yearly":
        collector.collect_yearly()

    print()
    print(f"[OK] {mode} モードの処理が完了しました")


if __name__ == "__main__":
    main()
