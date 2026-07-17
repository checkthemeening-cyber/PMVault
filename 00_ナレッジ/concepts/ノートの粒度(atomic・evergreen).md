---
type: 概念
status: 参照用
date: 2026-07-01
topic: ノートの粒度
tags: [evergreen, Zettelkasten, 運用ルール]
source: 本文に各URL併記
last_verified: 2026-07-01
certainty: 有力
---

# ノートの粒度（atomic・evergreen）

要約：1ノート1概念で書き、出典に縛られた要約と自分の言葉の永久ノートを分ける。この粒度で書くと、AI は必要なノートだけを開けばよく、余分なトークンを読まずに済む。

## 常緑ノートの3原則（Andy Matuschak）
- atomic … 1ノート1概念。長い記事に概念を詰め込まない
- concept-oriented … フォルダ構造でなくアイデア単位で分ける。タイトルがそのまま主張になる
- densely linked … 関連を必ず [[ ]] で繋ぐ。リンクが薄ければ概念の切り出しが甘い

階層タクソノミーより連想オントロジーを優先し、評価のためでなく自分の思考のために書く … https://notes.andymatuschak.org/Evergreen_notes

## Zettelkasten の4段階
- Fleeting … 走り書き・即時キャプチャ。あとで捨ててよい
- Literature … 出典を読んだ要約。どの資料の何かを残す
- Permanent … 自分の言葉に直した永久ノート。1ノート1アイデア
- Index / MOC … 永久ノートを俯瞰する地図

Fleeting をためずに Permanent へ上げ続けるのがこの方式の肝 … https://zenn.dev/kentakashima/articles/25c51a1c9eb510 （2025-09-01）, https://zenn.dev/mitarashi07/articles/b710eb4c3a03e2 （2025-07-16）

## このVaultでの対応
| Zettel の段階 | このVaultの場所 | 書き方 |
|---|---|---|
| Fleeting | _研修/memo.md / 40_運用/hot.md / 30_インプット/.raw/ への即時メモ | 形式は問わない。取りこぼさない |
| Literature | 30_インプット/.raw/（取り込み元）→ 30_インプット/sources/（取り込み要約） | 出典URLと日付を必ず残す |
| Permanent | 00_ナレッジ/concepts/ や 20_案件/entities/ の常設ページ | 1ノート1概念。自分の言葉。密にリンク |
| Index / MOC | index.md ＋ [[コンテンツ地図（MOC）]] | 永久ノートを束ねて俯瞰する |

- 30_インプット/.raw/ は不変の取り込み元。AI は読むだけで書き換えない（Literature の素材）
- 00_ナレッジ/concepts/ と 20_案件/entities/ が Permanent。常緑ノートの3原則を満たす品質バーで書く
- 同じ topic の Permanent が増えたら MOC を1枚切る

## 粒度を守る効き目
- AI は説明的なタイトルと topic を見て、開く前に関連を判定できる。atomic だと無駄なトークンを読まずに済む
- 1ノートが複数の文脈で再利用でき、複数の MOC から同じノートを指せる

## 関連
- [[命名と4手がかり]]
- [[PKM手法カタログ]]
- [[コンテンツ地図（MOC）]]
- [[プロパティ統制語彙]]

> 出典: 常緑ノートの3原則 Andy Matuschak https://notes.andymatuschak.org/Evergreen_notes ／ Zettelkasten 4段階 https://zenn.dev/kentakashima/articles/25c51a1c9eb510 （2025-09-01）, https://zenn.dev/mitarashi07/articles/b710eb4c3a03e2 （2025-07-16）。研修用に整理。
