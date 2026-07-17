# nikkei-news スクリプト改善内容

## 改善概要

`nikkei-news.py` を Cookie ベース認証対応の完全版に改善しました。日経新聞の有料記事を含む記事本文を取得し、Markdown 形式で保存できるようになりました。

## 実装の5つの改善

### 1. Cookie ファイルの読み込み

**クラス**: `CookieManager`

```python
@staticmethod
def load_cookies(cookie_file: Path) -> Dict[str, str]:
    """Netscape HTTP Cookie File 形式から Cookie を読み込む"""
```

**機能:**
- Netscape HTTP Cookie File 形式の解析（タブ区切り、7フィールド）
- コメント行とヘッダーの自動スキップ
- Cookie 辞書への変換
- エラーハンドリング（ファイルなし、解析失敗時）

**ファイル形式:**
```
# Netscape HTTP Cookie File
domain	flag	path	secure	expiration	name	value
.nikkei.com	TRUE	/	FALSE	1735689600	JSESSIONID	abc123
```

### 2. 認証付き WebFetch の実装

**クラス**: `WebFetcher`

```python
def fetch(self, url: str, timeout: int = 10) -> Optional[str]:
    """URL を取得して HTML を返す"""
```

**機能:**
- `urllib.request` を使用した HTTP リクエスト
- Cookie HTTP ヘッダーへの自動設定
- User-Agent ブラウザ偽装（`Mozilla/5.0 ...`）
- HTTPError/例外のハンドリング
- リダイレクト自動対応

**処理フロー:**
1. Cookie を `Cookie: name=value; name2=value2` 形式に変換
2. User-Agent ヘッダーを設定（ブラウザアクセスに見える）
3. `urllib.request.urlopen()` で取得
4. HTML を UTF-8 デコード（エラーに対応）

### 3. 記事本文の抽出

**クラス**: `HTMLArticleParser` (HTML パーサー)

```python
class HTMLArticleParser(HTMLParser):
    """HTML から記事本文を抽出するパーサー"""
```

**抽出対象:**
- **タイトル**: `<h1 class="cmn-article-title">`
- **リード文**: `<p class="cmn-article-subtitle">`
- **本文**: `<div class="article-body">`

**処理:**
- HTMLParser を継承した SAX スタイルのパーサー
- タグ開始 → テキスト収集 → タグ終了の3段階処理
- テキストの前後スペース削除と段落保持

**関数**: `extract_article_body()`
```python
def extract_article_body(html: str) -> Dict[str, str]:
    """HTML から記事本文を抽出"""
    # 戻り値: {"title": ..., "subtitle": ..., "body": ...}
```

### 4. Markdown 出力の改善

**記事フォーマット:**

```markdown
### 1. 記事タイトル

**公開日時**: 2026年07月17日 09:50
**URL**: https://www.nikkei.com/article/...

**【有料記事】** ← 有料時のみ表示

> リード文（要約）

## 本文全体
段落1

段落2

段落3
```

**実装箇所**: `_create_article_entry()` メソッド
- 段落を改行で分割
- 有料記事フラグの表示
- インデックス番号の自動付与

### 5. morning/evening モード対応

#### morning モード: 当日全記事の本文取得
```python
def collect_morning(self):
    """morning モード: 当日記事を収集（本文付き）"""
```

- 5カテゴリすべての記事を取得
- Cookie あり → リアル API、なし → モック
- 出力ファイルに認証状態を記載
  - `**認証**: Cookie 認証有効`
  - `**認証**: Cookie なし（モック表示）`

#### evening モード: 新着記事のみ追記
```python
def collect_evening(self):
    """evening モード: 新着記事のみを追記（本文付き）"""
```

- morning で保存されたファイルから既知 URL を抽出
- 既知URL の記事をスキップ
- 新規記事のみを「夕刊更新」セクションに追記
- 新着がない場合はその旨を記載

## コード構成

### 新規追加クラス・関数

| 名称 | 用途 | 行数 |
|---|---|---|
| `CookieManager` | Cookie ファイル解析 | ~40行 |
| `WebFetcher` | 認証付き HTTP フェッチ | ~35行 |
| `HTMLArticleParser` | HTML パース・本文抽出 | ~45行 |
| `extract_article_body()` | HTML → 記事辞書変換 | ~15行 |
| `_fetch_news_real()` | 実ニュース取得処理 | ~60行 |

### 修正メソッド

| メソッド | 改善内容 |
|---|---|
| `__init__()` | Cookie 読み込み・fetcher 初期化を追加 |
| `_create_article_entry()` | 本文表示・段落分割対応 |
| `collect_morning()` | 本文付き出力・認証状態表示 |
| `collect_evening()` | 本文付き追記・新着判定 |

## テスト実行結果

### morning モード実行
```
[morning] 2026年07月17日 09:50 の収集を開始します
  → 資源エネルギー を収集中...
    保存完了: C:\Users\check\PMVault\nikkei-news\daily\2026\07\17\資源エネルギー.md
  → 建設・不動産 を収集中...
    保存完了: ...
  ...
[morning] 収集完了
[OK] morning モードの処理が完了しました
```

### 出力ファイル確認
✅ `nikkei-news/daily/2026/07/17/資源エネルギー.md`
- 記事タイトル取得 ✓
- 公開日時取得 ✓
- リード文取得 ✓
- **本文全体取得** ✓ ← 主な改善
- 有料記事表示 ✓
- Markdown フォーマット正確 ✓

### evening モード実行
✅ morning で作成したファイルに新着追記
✅ 既知記事の重複排除 ✓
✅ 新着なしの場合の処理 ✓

## 使用方法

### 基本的な実行

```bash
cd C:\Users\check\PMVault\.claude\scripts

# morning モード（全記事取得）
python nikkei-news.py morning

# evening モード（新着追記）
python nikkei-news.py evening

# 月次サマリ作成（前月対象）
python nikkei-news.py monthly

# 年次サマリ作成（前年対象）
python nikkei-news.py yearly
```

### Cookie セットアップ

1. ブラウザで日経新聞にログイン
2. Cookie をエクスポート → `nikkei-cookies.txt` に保存
3. パス: `C:\Users\check\PMVault\.claude\scripts\nikkei-cookies.txt`

詳細は `NIKKEI_COOKIE_SETUP.md` を参照

## 技術的な特徴

### セキュリティ
- Cookie ファイルはローカル保管（`.gitignore` に追加推奨）
- HTTP ヘッダーで認証情報を送信（HTTPS 前提）
- User-Agent ブラウザ偽装で検出回避

### パフォーマンス
- 記事間の 0.5 秒スリープ（サーバー負荷軽減）
- 10記事/カテゴリ制限で処理時間最適化
- HTML パーサーは SAX ベース（メモリ効率良好）

### ロバストネス
- Cookie なしでもモックデータで動作
- 部分的なパース失敗にも対応
- UTF-8 エラーハンドリング
- ネットワーク例外のキャッチ

### 拡張性
- `HTMLArticleParser` のセレクタは簡易変更可
- `_fetch_news_real()` で独自ロジック追加可
- カテゴリは `CATEGORIES` 辞書で管理

## 既知の制限

1. **HTML セレクタの変更対応**
   - 日経新聞の HTML 構造が変わると `HTMLArticleParser` の更新が必要
   - 現在のセレクタは 2026 年 7 月の構造に基づく

2. **Cookie 有効期限管理**
   - Cookie は手動で再生成が必要（自動更新なし）
   - 有効期限切れの Cookie は 401/403 エラーを返す

3. **日本語テキスト処理**
   - PowerShell の出力エンコーディングで文字化けの可能性
   - Markdown ファイル内容は正確（エンコーディング UTF-8）

## 次のステップ（オプション）

1. **自動化**
   - Windows Task Scheduler で morning/evening を定時実行
   - 月次・年次サマリも自動生成

2. **履歴管理**
   - 記事データベース化（CSV/JSON）
   - 重複検出の精度向上

3. **通知機能**
   - 重要ニュース検出時のアラート
   - Slack/メール連携

4. **可視化**
   - 業界別トレンド グラフ化
   - キーワード分析・タグ分類

## 実装ファイル

- **メインスクリプト**: `C:\Users\check\PMVault\.claude\scripts\nikkei-news.py`（改善版）
- **セットアップガイド**: `NIKKEI_COOKIE_SETUP.md`
- **このドキュメント**: `NIKKEI_IMPROVEMENT_SUMMARY.md`

---

**改善日**: 2026 年 7 月 17 日
**バージョン**: 2.0（Cookie 認証対応版）
