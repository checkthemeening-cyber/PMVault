# nikkei-news Cookie 認証セットアップガイド

## 概要

`nikkei-news.py` スクリプトは Cookie ベース認証に対応しており、日経新聞の有料記事の本文を取得できるようになりました。このドキュメントは Cookie ファイルの設置と設定方法を説明します。

## Cookie ファイルの取得

### 方法 1: ブラウザから Cookie をエクスポート

1. **Chrome の場合**
   - Chrome Web Store から「EditThisCookie」拡張をインストール
   - `www.nikkei.com` にアクセス
   - 拡張アイコンをクリック → すべての Cookie をエクスポート → テキストとしてコピー

2. **Firefox の場合**
   - 開発者ツール（F12）→ ストレージ → Cookie → https://www.nikkei.com
   - または、「Cookies.txt」エクスポーター拡張を使用

### 方法 2: Netscape Cookie Jar 形式で保存

Cookie をエクスポートして、以下のフォーマットで保存します：

```
# Netscape HTTP Cookie File
.nikkei.com	TRUE	/	FALSE	1735689600	cookie_name_1	cookie_value_1
.nikkei.com	TRUE	/	FALSE	1735689600	cookie_name_2	cookie_value_2
```

## Cookie ファイルの配置

1. **ファイルパス**
   ```
   C:\Users\check\PMVault\.claude\scripts\nikkei-cookies.txt
   ```

2. **ファイル形式**
   - Netscape HTTP Cookie File 形式（標準フォーマット）
   - テキストエンコーディング: UTF-8
   - ヘッダー行: `# Netscape HTTP Cookie File`

3. **ファイル内容の例**
   ```
   # Netscape HTTP Cookie File
   # 自動生成: nikkei.com から Cookie をエクスポート
   .nikkei.com	TRUE	/	FALSE	1735689600	JSESSIONID	abc123def456
   .nikkei.com	TRUE	/	FALSE	1735689600	NIKKEI_SESSION	xyz789
   www.nikkei.com	FALSE	/	FALSE	1735689600	subscription_token	value_here
   ```

## スクリプト動作の確認

### morning モード（当日の全記事取得）

```bash
cd C:\Users\check\PMVault\.claude\scripts
python nikkei-news.py morning
```

**期待される出力:**
- `[morning] 2026年07月17日 09:50 の収集を開始します`
- 各カテゴリの記事取得ログ
- `**認証**: Cookie 認証有効` と表示（Cookie が正常に読み込まれた場合）
- 記事本文が Markdown ファイルに保存される

### evening モード（新着記事のみ追記）

```bash
python nikkei-news.py evening
```

**期待される出力:**
- morning モードで作成されたファイルに新着記事を追記
- 既知記事のスキップ
- 新規記事の本文付きで追加

## トラブルシューティング

### 1. Cookie ファイルが見つからない場合

**エラーメッセージ**
```
警告: Cookie ファイルが見つかりません: C:\Users\check\PMVault\.claude\scripts\nikkei-cookies.txt
```

**解決策:**
- Cookie ファイルをダウンロード・作成して指定のパスに配置
- スクリプト出力に `**認証**: Cookie なし（モック表示）` と表示される
- モックデータで動作を確認可能

### 2. Cookie が有効期限切れの場合

**症状:**
- スクリプト実行後も 401/403 エラーが返される
- 記事本文が取得できない

**解決策:**
- ブラウザから再度 Cookie をエクスポート
- `nikkei-cookies.txt` を更新

### 3. HTML パース エラーが発生する場合

**症状**
```
HTML パースエラー: ...
```

**解決策:**
- 日経新聞の HTML 構造が変更された可能性
- `HTMLArticleParser` クラスのセレクタを確認・更新

## Cookie 内容の保護

**重要**: Cookie ファイルは認証情報を含むため、以下の点に注意してください：

- `nikkei-cookies.txt` をバージョン管理に含めない（`.gitignore` に追加）
- 個人用の環境にのみ保管
- 他のユーザーと共有しない
- 定期的に有効期限を確認し、期限切れ Cookie を削除

## 出力ファイル構造

スクリプト実行後、以下のフォルダに Markdown ファイルが生成されます：

```
nikkei-news/
├── daily/
│   └── 2026/
│       └── 07/
│           └── 17/
│               ├── 資源エネルギー.md
│               ├── 建設・不動産.md
│               ├── 物流・運輸.md
│               ├── 商社・卸売り.md
│               └── 自動車.md
├── monthly/
│   └── 2026/
│       └── 07_summary.md
└── yearly/
    └── 2026_summary.md
```

## 記事本文の含まれる情報

各 Markdown ファイルには以下の情報が含まれます：

1. **メタデータ**
   - 収集日時
   - ソース URL
   - 記事数
   - 認証状態

2. **本日のまとめ**
   - カテゴリごとの要約

3. **記事一覧（本文付き）**
   - 記事タイトル
   - 公開日時
   - URL
   - リード文（要約）
   - **記事本文全体** ← 改善点
   - 有料記事表示（対応時）

## 自動化の推奨設定

### Windows Task Scheduler での定期実行

1. `タスク スケジューラ` を開く
2. `新しいタスクの作成` → `基本タスク`
3. **朝の実行**
   - トリガー: 毎日 06:00
   - アクション: `python C:\Users\check\PMVault\.claude\scripts\nikkei-news.py morning`

4. **夕方の実行**
   - トリガー: 毎日 18:00
   - アクション: `python C:\Users\check\PMVault\.claude\scripts\nikkei-news.py evening`

## 参考資料

- Netscape Cookie Format: https://curl.se/rfc/cookie_spec.html
- 日経新聞: https://www.nikkei.com/
- Python urllib: https://docs.python.org/3/library/urllib.request.html
