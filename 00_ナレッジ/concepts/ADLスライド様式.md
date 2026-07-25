---
type: 規約
status: 参照用
date: 2026-07-25
topic: スライド様式
tags: [規約, スライド, ブランド, PPT, ADL]
source: _templates/ADLスライド様式/ADL_Slide_User_Guide.pptx（ADL公式 User guideline、UPDATED JANUARY 2026、全71枚）
last_verified: 2026-07-25
certainty: 確実
---

# ADLスライド様式

要約：Arthur D. Little 公式のPPTデザイン規約。**Claude CodeでPPT・スライドを作るときは、着手前にこのページを読み、ここの数値どおりに作る**。原本は [[_templates/ADLスライド様式/ADL_Slide_User_Guide.pptx]]（71枚・31MB）。このページは原本から機械抽出した仕様の要約で、数値はテーマXML・レイアウト実測から取ったもの。図の文法は [[エグジビット・パターン]]、資料の論理構造は [[ピラミッド原則とSCQA]] を併用する。

<!-- 抽出方法：pptxをunzipし ppt/theme/theme1.xml の clrScheme/fontScheme、slideMaster/slideLayout のプレースホルダ座標、全71枚の本文テキストをpython-pptxで読み出した。ガイドライン本文の記述と実測値が一致した項目のみ「確実」として記載し、一致を確認できなかった項目は「未確認」と明記した。 -->

## ブランドの5本柱
PREMIUM / MODERN / DYNAMIC / DIFFERENT / OPEN。書式・ロゴ・フォント・配色・ブリッジ・グラデーションのすべてがこの5つの反映。

## 配色（テーマ名 "ADL"）
テーマパレット以外の色を使わない。MS Office標準の「標準の色」行は**絶対に使わない**（ブランド非準拠）。

| 役割（PowerPoint上の名称） | HEX | 用途 |
|---|---|---|
| Dark blue, Text 1 | `#0D003F` | 既定の文字色。既定の罫線色。図形・プルアウトの主色 |
| White, Background 1 | `#FFFFFF` | 背景 |
| Purple, Text 2 | `#6E668C` | 表の内側罫線。Think-cell外テキストボックス（11pt） |
| Light Blue, Background 2 | `#D1E0FB` | 表の第1列。図形の既定塗り |
| Bright Blue, Accent 1 | `#1774F5` | 強調文字。表の合計行。ハイパーリンク |
| Accent 2 | `#6CB0FF` | チャート系列 |
| Accent 3 | `#8EF4FF` | チャート系列 |
| Periwinkle, Accent 4 | `#C3C3DA` | 表の小見出し行 |
| Accent 5 | `#0D003F` | Text 1と同値 |
| Accent 6 | `#A336DE` | チャート系列・番号装飾 |
| 訪問済リンク | `#00AAC1` | — |

- コア色にはtint値（濃淡）があり、選択肢を増やすときはtintを使う。カスタムカラーは補助パレット
- 強調は Bright Blue（Accent 1）か Dark blue（Text 1）の**太字**、またはその組み合わせ
- Accent 2 / Accent 3 / Accent 5 の英語名称はガイドライン本文に明記がない（HEXはテーマXMLの実測値なので確実）

## フォント
- **ブランドフォントは Arial（regular か bold）のみ**。ダークブルー。システムフォントなので表示崩れとフォント埋め込み問題が起きない
- 副フォントは **Freestyle Script**。数字に使う。**太字にしない**。ブランドの一部ではないので多用しない
- 「ADL Notes」フォントは Brand Portal から取得（`https://brand.adlittle.com/media/?mediaId=DE36196E-5805-4FF5-B9A4DBADC329101C`）
- 既定言語は US English
- 注意：原本ファイルには `Bad Script` が埋め込まれているが、これはGoogle Slides経由で往復した際の Freestyle Script の代替であり**ブランドフォントではない**。生成物で使わない

## 判組み（type levels）
- 本文は **16pt から始めて段階的に下げる**。テキストレベルは**5段**（Shift+Alt+左右矢印で切替）
  - レベル1：一般本文 / レベル2：本文内の小見出し / レベル3：第1階層の箇条書き / レベル4：第2階層 / レベル5：第3階層
- レベル2〜5の各ptは原本が往復変換でフラット化されており復元できない（**未確認**）。厳密な値が必要なときは原本の各プレースホルダをPowerPointで実測する
- 手動で箇条書きを付けるときの記号：**丸ビュレット = 文字コード183（`·`）／サブビュレット = 通常文字の 文字コード2013（`–`）**
- 既定テキストボックス：**余白ゼロ**・Dark Blue Text 1・Arial **14pt**
- 既定図形：**四方 0.2cm 余白**・塗り Light Blue Background 2・Dark Blue Text 1・Arial **14pt**

## 版面（16:9 ワイドスクリーンが既定）
| 項目 | 値 |
|---|---|
| スライド全体 | 33.87 × 19.05 cm（13.333 × 7.5 in） |
| ワークスペース（作業領域） | 幅 **28.8 cm** × 高さ **12.91 cm**（全ページ共通） |
| 左右マージン | 各 2.53 cm |
| タイトル枠 | left 2.53 / top 2.38 / 28.80 × 1.85 cm |
| 本文枠 | left 2.53 / top 4.45 / 28.80 × 12.91 cm |
| 出所（Source）枠 | left 2.53 / top 17.43 / 27.60 × 1.32 cm |

- **タイトルは最大2行**。ワークスペースに食い込ませない
- マージンには本文を置かない。図を強調したいときだけ例外を許す
- 出所は左マージンに揃え、行が増えたら**上へ伸ばす**
- 本文スライドの上端には**グラデーションのタイトルバー**が入る（openness の表現）。ナビゲーション（トラッカー）として使える
- 詰め込まない。標準の文字サイズを大きくしない

## 表
- **内側罫線のみ**。外枠を引かない
- タイトル行：Dark blue Text 1・**14pt 太字**
- 第1列：Light Blue Background 2
- 内側罫線：**0.75pt**・Purple Text 2。**塗りのあるセルには罫線を引かない**
- 小見出し行：Periwinkle Accent 4 ／ 合計行：Bright Blue Accent 1

## 線・数字・矢印
- 既定は **0.75pt**・Dark Blue。表では Purple Text 2
- 強調は **2pt または 3pt**
- 数字と矢印は線と同じ色域を使う

## チャート
- 作図ツールは **Think-cell**。**6つのアクセント色を第一選択**とする
- 色が足りなければカスタムパレット、または Think-cell の smoke 色
- 2社比較はコントラスト色で明確に分ける
- Think-cell外のテキストボックスは **Purple Text 2・11pt**、単位ボックスは**左上**に置く

## 文章の作法
### 句読点
- **既定は「短いフレーズ＋句点なし」**（PPTの標準スタイル）。Sentence case。例：`Market overview` / `Key takeaways` / `Next steps`
- 完全文の箇条書きは**必要なときだけ**。大文字始まり＋句点で終える
- **同じリスト・同じスライド内でスタイルを混ぜない**

### Source と Note
- `Source` / `Note` を**複数形にしない**
- 順序は **Note 行が Source 行の上**。Source はスライド下部
- Sourceプレースホルダはレイアウトに自動で入る。消えたら Home タブの **Reset**
- 複数出所はカンマ区切り。ただし個々の項目自体にカンマを含む場合はセミコロン区切り
- 注番号は**図中では括弧なしの上付き数字**、Sourceボックス内では括弧付き。例：`Note: (1) Not applicable; (2) see page XX`
- 略語の説明は Note の上に置く

### 数値・通貨
- 小数は必要なときだけ**1桁**、小数点は**ドット**。例：`€2.5m`（`€2.543m` にしない）
- 数値と単位の間は**ノーブレークスペース**。例：`€2.5 million`
- 通貨記号は数字に隣接させる。表では通貨と数値を**左揃え**
- 本文では**通貨コード**（EUR / USD / GBP）＋ million / billion を綴る。例：`EUR 2.5 million`
- **thousand は綴らず `k`**。例：`USD 850,000` または `USD 850k`
- チャート・表では**通貨記号**を使う。略記スタイルは資料内で統一する

## アイコン
- ADLアイコン（アウトラインスタイルのベクター）を UpSlide ライブラリから使う。他のアイコンを混ぜない
- **1枚あたり最大 3〜5個**。文章量に関係なくこの上限
- 理想は**キーメッセージ／セクションごとに1個**
- **箇条書きの代わりに使わない**（3〜4点の設計されたリストの一部である場合を除く）
- テキストが先、アイコンが後。アイコンは物語を支えるもので、支配するものではない
- 迷ったら入れない（"If in doubt, leave it out."）

## 画像
- **Brand Portal の画像バンクからのみ**取得する。外部ストックサイト・インターネット画像は**使用禁止**（著作権）
- **1枚 1MB 以下**。必要なら PowerPoint の「図の圧縮」を使う（デジタル表示なら email 解像度が目安）
- 写真 **または** イラスト／3D。**両者を混ぜない**（人工的な印象になる）
- 高コントラスト・情報過多な構図を避ける。**画像の下に影を付けない**。写真の上にイラスト要素を重ねない
- ADLはマーケティング用途での**AI生成画像を推奨しない**
- 画像の3カテゴリ：①自社の人と顧客をつなぐ ②顧客の世界につなぐ ③大きな構想・解決策（グラデーション＋抽象要素）

## グラデーションとブリッジ
- グラデーションは openness（開放性）・流動性・色の収束＝アイデアと産業の統合の象徴。サイズや影響を削らない
- **プライマリグラデーション**：内容が濃いページの背景に使わない。前面に要素を多数置く背景として使わない
- **セカンダリグラデーション**：明るく他の画像と併用しやすい。コンテンツ領域の区切り・写真フレーム・ハイライトボックスに向く。ただし多用しない
- **ブリッジ・グラデーションはマーケティング資料とPPTの表紙のみ**に使う
- 素材の入手元は Brand Portal（`brand.adlittle.com`）

## ロゴ
- 表紙は**プライマリの Arthur D. Little ロゴ**
- **表紙以外の全ページは略式の "ADL" ロゴを右上**に置く
- ロゴ色は背景色に応じて変える
- クライアントロゴは表紙に置ける。本文には入れない

## ステッカー・機密表示
- **単体ステッカー**（illustrative 等）：12pt・太字なし・イタリック・**大文字**、Dark Blue、線 0.75pt、語の長さと線の長さを揃える。作業領域の**右上**に置く。1枚または特定コンテンツを指す
- **機密ステッカー／ウォーターマーク**：12pt・太字なし・イタリック・大文字、文字と線を**赤**、線 0.75pt。スライド**下部中央**。全ページに出すには**マスター（1ページ目）に手動でコピー**する

## レイアウト（26種・原本の名称そのまま）
表紙系：`Title Slide` / `Alternative Title Slide`（印刷向け白背景） / `Title Slide Image` / `Title Slide Full Bleed Image`
目次・区切り：`Contents` / `Section Header` / `Subsection` / `Appendix`
本文：`Title and Content` / `Title Only` / `Two column content` / `Content and Image` / `Chart and Text` / `Three Column Text` / `Four Column Text` / `Three Column Text and Images` / `Blank`
ページブレイク：`Full Bleed Image and Caption` / `Top bar with Image and Caption` / `Title Only Pale` / `Title and Content Pale` / `Title and Content Dark`
その他：`One Monopoly Card` / `Two Monopoly Card` / `About and Contact Details` / `Closing Slide`

- 表紙は4種類（塗り／白背景／写真あり／全面写真）。表紙タイトルは**大文字**でリーダーシップと確信を示す。最大3行まで折り返せる
- `Contents` / `Section Header` / `Subsection` / `Appendix` は UpSlide が自動生成する。**これらのレイアウトのプレースホルダを削除しない**（目次と章立ての制御に使われている）
- 締めは `Closing Slide`（"THE DIFFERENCE"）

## 前提ツール（Claude Codeからは直接使えない）
- **UpSlide**：テンプレート・ライブラリ・目次自動生成・セクション区切り自動生成・Slide check・Smart painter・スライドコンバータ。ライブラリ内 User Guides に各種マニュアル
- **Think-cell**：チャート作成（CAGR自動計算・軸ブレーク・Excel同期・ガントチャート）
- **ADL PPT Tool**：UpSlide以前のアドオン。Working Space ツールが現役
- 素材：Brand Portal `brand.adlittle.com` ／ 社内SNS The Hive `hive.adlittle.com` ／ SmartApps `search.adlittle.com`
- 問い合わせ：ブランド `brand@adlittle.com` ／ グラフィック `graphics@adlittle.com`

## Claude CodeでPPTを作るときの適用方法
生成の実体は [[スライド生成キット]] の3方式（YAMLコンパイラ／単一HTML／SVG→pptx）。UpSlideもThink-cellも使えないので、上の規約のうち**手で守れる部分をすべて守る**。

守るもの（キット側の設定より**この公式値を優先**する）
1. 配色は上のHEXテーブルのみ。信号色（赤緑黄）とMS Office標準色を使わない
2. フォントは Arial。本文16pt起点、テキストボックス14pt、ステッカー12pt、Think-cell外注記11pt
3. 版面は 33.87×19.05cm、作業領域 28.8×12.91cm、左右マージン 2.53cm。タイトルは2行以内
4. 表は内側罫線のみ・0.75pt・Purple Text 2、塗りセルに罫線なし、タイトル行14pt太字
5. 箇条書きは短いフレーズ＋句点なしで統一。混在させない
6. 出所は左下・`Source:` 単数形、Noteはその上。ページ番号は右下
7. アイコンは1枚3〜5個まで。箇条書きの代わりにしない
8. 画像はBrand Portal由来のみ。AI生成画像・写真＋イラスト混在・影を使わない
9. ブリッジグラデーションは表紙のみ

置き換えが必要なもの
- Think-cellチャート → キットの `bar_chart` / `hbar_compare` / `quadrant_map` などで代替し、6アクセント色の順で配色
- UpSlideの目次・章区切り自動生成 → キットの `agenda` / `divider` パターンで手動構成
- ADLアイコン・Brand Portal画像 → 取得できないので `ph_image`（グレー破線枠＋何を/なぜ/推奨作図法）に退避し、人間に挿入を依頼する
- Freestyle Script（数字用） → 環境にない場合はArialのままにし、代替フォントを勝手に選ばない

## 既知の不整合（要対応）
[[スライド生成キット]] の各キットが持つ配色定義は、公式テーマと**5色すべてが微妙に違う**。今後は公式値に寄せる。

| 役割 | 公式（本ページ） | キットの現行値 |
|---|---|---|
| Dark blue / navy | `#0D003F` | `#0c0a3e` |
| Bright Blue / Accent 1 | `#1774F5` | `#2563eb` |
| Light Blue / Background 2 | `#D1E0FB` | `#d9e4f9` |
| Accent 3（cyan） | `#8EF4FF` | `#38d6ee` |
| Accent 6（magenta） | `#A336DE` | `#a933d4` |

## 関連
- [[スライド生成キット]] … 実際に生成する3キットの使い分け
- [[エグジビット・パターン]] … 図の文法（2×2/ウォーターフォール等）
- [[ピラミッド原則とSCQA]] … 縦の論理とデッキ順序
- [[提案ストーリーの型]] … 提案の骨格

> 出典: ADL公式 `ADL_Slide_User_Guide.pptx`（User guideline、PRESENTATION TO ADL STAFF、UPDATED JANUARY 2026、全71枚）。原本は [[_templates/ADLスライド様式/ADL_Slide_User_Guide.pptx]]。配色・版面の数値は同ファイルの theme1.xml / slideMaster1.xml / slideLayout*.xml から実測（2026-07-25 確認）。社内リンク（Brand Portal・Hive）はADLネットワーク接続時のみ到達可能。
