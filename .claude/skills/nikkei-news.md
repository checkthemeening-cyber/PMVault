# 日経ニュース収集・サマリスキル

このスキルは日経新聞サイト（nikkei.com）から5カテゴリのニュースを収集・サマリし、
`C:\Users\check\PMVault\nikkei-news\` 以下にMarkdownファイルとして記録する。

## 監視カテゴリとURL

| カテゴリ名 | ニュースページURL |
|-----------|----------------|
| 資源エネルギー | https://www.nikkei.com/business/energy/ |
| 建設・不動産 | https://www.nikkei.com/business/realestate/ |
| 物流・運輸 | https://www.nikkei.com/business/logistics/ |
| 商社・卸売り | https://www.nikkei.com/business/wholesale/ |
| 自動車 | https://www.nikkei.com/business/vehicles-machinery/ |

## 実行モード

引数に以下のモードを指定する（引数なしの場合は `daily`）:

- **`daily`**: 本日分のニュースを収集・サマリして保存
- **`monthly`**: 前月の日次ファイルを読み込んで月次サマリを作成
- **`yearly`**: 前年の月次ファイルを読み込んで年次サマリを作成

## 保存先ディレクトリ構造

```
C:\Users\check\PMVault\nikkei-news\
  daily\
    YYYY\
      MM\
        DD\
          資源エネルギー.md
          建設・不動産.md
          物流・運輸.md
          商社・卸売り.md
          自動車.md
  monthly\
    YYYY\
      MM_summary.md    （例: 06_summary.md）
  yearly\
    YYYY_summary.md    （例: 2026_summary.md）
```

---

## daily モードの手順

### Step 1: 現在日時を把握する
- 今日の日付（YYYY, MM, DD）と時刻（HH:MM）を確認する
- JST（日本標準時）で処理する

### Step 2: 各カテゴリのニュースを収集する

5カテゴリそれぞれについて以下を実行する:

1. **WebFetch** でカテゴリページを取得する
   - 例: `https://www.nikkei.com/business/energy/`
   - ページには最新ニュースの一覧（見出し・日時）が表示される

2. **本日更新された記事を抽出する**
   - 記事一覧から「本日（今日）公開・更新」の記事を優先して抽出する
   - 最大10件を対象とする

3. **記事の内容をサマリする**
   - 見出しと、取得できた場合はリード文・概要から内容を把握する
   - 有料記事（ペイウォール）は見出しと日時のみ記録する

### Step 3: カテゴリごとにファイルを作成・保存する

以下のMarkdown形式で保存する。ファイルパス:
`C:\Users\check\PMVault\nikkei-news\daily\YYYY\MM\DD\{カテゴリ名}.md`

```markdown
# {カテゴリ名} ニュースサマリ

**収集日時**: YYYY年MM月DD日 HH:MM (JST)
**ソース**: {カテゴリページURL}

---

## 本日の主要ニュース

### 1. {記事タイトル}
- **公開日時**: {日時}
- **URL**: {記事URL}
- **概要**: {2〜4行のサマリ。有料記事の場合は「【有料記事】見出しのみ」と記載}

### 2. {記事タイトル}
...（最大10件）

---

## 本日のトレンド分析

{カテゴリ全体を通じた今日のキーワード・動向を3〜5行で記述する。
例：「原油価格の動向」「大型案件の発表」「規制の変化」など。}
```

- 保存前にディレクトリが存在しない場合は作成する（`New-Item -ItemType Directory -Force`）
- ファイルが既に存在する場合は上書きする（同一日に2回実行した場合は最新で更新）

---

## monthly モードの手順

### Step 1: 対象月を特定する
- 前月（現在の月の1か月前）を対象とする
- 例：7月1日実行 → 6月分（2026年6月）

### Step 2: 日次ファイルを読み込む

前月のディレクトリ内のファイルを全て読み込む:
`C:\Users\check\PMVault\nikkei-news\daily\YYYY\MM\**\*.md`

- **Glob** または **PowerShell** で対象ファイル一覧を取得する
- 各ファイルを **Read** ツールで読み込む

### Step 3: 月次サマリを作成する

以下の形式で保存する。ファイルパス:
`C:\Users\check\PMVault\nikkei-news\monthly\YYYY\MM_summary.md`

```markdown
# {YYYY年MM月} ニュース月次サマリ

**対象期間**: YYYY年MM月1日〜MM月末日
**作成日時**: {作成日}

---

## 資源エネルギー

### 月間主要ニュース Top5
1. ...
2. ...

### 月間トレンド・分析
{3〜5行: 月を通じた主要な動向、繰り返し登場したキーワード、重要な出来事など}

---

## 建設・不動産

...（各カテゴリ同様の構成）

---

## 全カテゴリ横断サマリ

### 共通テーマ・注目トピック
{全カテゴリを通じて見えてきたマクロ動向を3〜5行で記述}
```

---

## yearly モードの手順

### Step 1: 対象年を特定する
- 前年を対象とする（例：2027年1月1日実行 → 2026年分）

### Step 2: 月次ファイルを読み込む

前年の月次サマリを全て読み込む:
`C:\Users\check\PMVault\nikkei-news\monthly\YYYY\**_summary.md`

### Step 3: 年次サマリを作成する

以下の形式で保存する。ファイルパス:
`C:\Users\check\PMVault\nikkei-news\yearly\YYYY_summary.md`

```markdown
# {YYYY年} ニュース年次サマリ

**対象期間**: YYYY年1月〜12月
**作成日時**: {作成日}

---

## 資源エネルギー

### 年間重大ニュース Top10
1. ...

### 年間トレンド・分析
{5〜8行: 年間を通じた主要トレンド、構造変化、重要イベントなど}

---

## 建設・不動産
...（各カテゴリ同様）

---

## 年間総括

### カテゴリ横断トレンド
{全体を通じた年間の重要な変化・動向を5〜8行で記述}

### 来年への示唆
{各カテゴリの展望を箇条書きで記述}
```

---

## 注意事項

- 日経新聞は有料コンテンツが多い。ペイウォールで本文が取得できない場合は見出しと日時のみ記録し「【有料記事】」と明記する
- WebFetch でページが取得できない場合は WebSearch で `site:nikkei.com {カテゴリキーワード}` を検索してヘッドラインを収集する
- 全ての出力は日本語で作成する
- ファイルの保存には Write ツールを使用する
- ディレクトリ作成には PowerShell を使用する（`New-Item -ItemType Directory -Force "{パス}"`）
