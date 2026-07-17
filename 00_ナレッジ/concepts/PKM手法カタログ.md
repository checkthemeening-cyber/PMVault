---
type: 概念
status: 参照用
date: 2026-07-01
topic: PKM手法
tags: [PKM, 運用ルール]
source: 各項目にURL併記
last_verified: 2026-07-01
certainty: 有力
---

# PKM手法カタログ（発展編）

要約：このVaultは LLM Wiki 型（取り込み→相互リンク→引き出し）と4つの手がかりで動く。第二の脳を別用途へ広げるとき選べる代表的手法を出典付きで並べる。手法は競合でなく層として重ねる。

## 手法は層で重ねる
- PARA … 今この情報はどの行動に属すか（実務レンズ）
- Johnny Decimal … 永遠にどこに置くか（恒久アドレス）
- Zettelkasten / LYT-MOC … どう繋がり、どう俯瞰するか（知識レンズ）
- このVaultの既定は『フォルダ最小・リンク中心・タグ控えめ』。下記は必要になった層だけ足す

## PARA（Projects / Areas / Resources / Archives）
- 何か … 締切のある短期=Projects、継続責任=Areas、参照=Resources、完了=Archives。トピックでなく今の行動で分ける … https://affine.pro/blog/second-brain （2025）
- いつ使う … 締切ありのデリバリ案件を扱うとき
- このVaultへの足し方 … フォルダは増やさず status（進行中/完了/保留）と project/ タグで表現。終了案件は AI から見えにくくなるので MOC で1枚残す
- 出典補足 … PARA×Zettelkasten 融合論 https://parazettel.com/articles/fusing-basb-zettelkasten-obsidian/ （2023-09-15）

## Zettelkasten（4段階＋1ノート1概念）
- 何か … Fleeting→Literature→Permanent→Index(MOC) の4段階。永久ノートは1ノート1アイデア、双方向リンクで非階層の網 … https://zenn.dev/kentakashima/articles/25c51a1c9eb510 （2025-09-01）
- いつ使う … 00_ナレッジ/concepts/ の品質基準として効かせる
- このVaultへの足し方 … 30_インプット/.raw/ 取り込み→ingest が Literature→Permanent に相当。memo.md 等の Fleeting を夜間に AI が永久ノート化候補として提示する運用に発展できる
- 出典補足 … Obsidian実装解説 https://zenn.dev/mitarashi07/articles/b710eb4c3a03e2 （2025-07-16）

## LYT / MOC（コンテンツ地図）
- 何か … テーマごとに手で束ねたリンク集。1ノートは複数MOCに属せる。ボトムアップの網にトップダウンの索引を重ねる … Nick Milo が2020提唱 https://yu-wenhao.com/en/blog/lyt-framework-guide/
- いつ使う … index.md が肥大化、案件/テーマ単位で俯瞰したいとき。AI が MOC 1枚でそのテーマの主要ノートを一度に参照できる点が効く
- このVaultへの足し方 … [[コンテンツ地図（MOC）]] と [[MOC_テンプレ]] を使い、index.md の概念欄に1行足す

## evergreen / atomic notes（常緑ノート）
- 何か … atomic（1ノート1概念）/ concept-oriented（アイデア中心）/ densely linked（密リンク）。階層タクソノミーより連想オントロジー優先 … https://notes.andymatuschak.org/Evergreen_notes
- いつ使う … 00_ナレッジ/concepts/ や 20_案件/entities/ の常設ページが満たす品質バー
- このVaultへの足し方 … wikiページ_テンプレの『要点＝主張＋出典』を1概念単位で書き、関連を必ず [[ ]] で繋ぐ。詳しくは [[ノートの粒度（atomic・evergreen）]]

## Johnny Decimal（恒久アドレス採番）
- 何か … 10カテゴリ×各10サブ=100の恒久アドレス。PARAが今どこ、JDが永遠にどこを答える … https://blog.shuvangkardas.com/johnny-decimal-obsidian-organization-method/
- いつ使う … ファイルが増えて毎回どこに置くか迷う規模になったとき
- このVaultへの足し方 … _研修/ 配下の _実績/ docs/ など物理フォルダの背番号付けに限定。知識ノート本体はリンク中心のまま。過剰適用しない

## フォルダ vs リンク vs タグ
- 何か … 書き物プロジェクト=フォルダ、知識=リンク中心、タグは控えめ。dog/dogs/pets の語彙ゆらぎでタグは曖昧になりやすい … https://forum.obsidian.md/t/folders-vs-linking-vs-tags-the-definitive-guide-extremely-short-read-this/78468
- 注意 … このスレは投稿者の一案で、コメント欄では『タグはフォルダと直交する別軸』とする反論も強い。合意でなく論争継続。検索優先・ハイブリッドが現実的な落としどころ
- このVaultへの足し方 … 既存ルール『5個以上のノートで使うタグだけ作る』『リンク中心』と整合。新フォルダ追加は最後の手段

## データ層（プラグイン解禁時の発展）
- Obsidian Bases … Markdown のまま表/カード/リストの DB ビューを作るコアプラグイン。セル編集が YAML frontmatter を双方向更新 … 公式 https://obsidian.md/help/bases ／ v1.9.10 で前面化 https://obsidian.md/changelog/2025-08-18-desktop-v1.9.10/ （2025-08-18）。現状は Table/Cards 中心でグルーピング未対応
- Dataview … DQL で問い合わせる老舗。inline フィールドや動的集計に強いが編集不可・構文が脆い。Bases へ移行する流れだが用途次第で併用 … https://practicalpkm.com/moving-to-obsidian-bases-from-dataview/ （2025-09-29）
- このVaultへの足し方 … 研修の基本路線は Markdown のみ。解禁時、index.md を動くダッシュボードへ昇格させたいなら Bases。複雑な集計が要るときだけ Dataview

## このVaultとの関係
- 既定（4手がかり＋LLM Wiki）は変えない。上の手法は足場で、必要になった層だけ重ねる
- 迷ったら：知識はリンクと MOC、実務の状態は status、置き場の固定が要れば Johnny Decimal

## 関連
- [[命名と4手がかり]]
- [[コンテンツ地図（MOC）]]
- [[プロパティ統制語彙]]
- [[ノートの粒度（atomic・evergreen）]]

> 出典は各項目に併記。手法を競合でなく層として重ねる整理は LYT https://yu-wenhao.com/en/blog/lyt-framework-guide/ と PARA×Zettel 融合論 https://parazettel.com/articles/fusing-basb-zettelkasten-obsidian/ に基づく。研修用に整理（2026-07-01 時点）。
