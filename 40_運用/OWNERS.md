---
type: 規約
status: 参照用
date: 2026-07-01
topic: 運用ルール
tags: [規約, 更新責任, ガバナンス]
last_verified: 2026-07-01
review_by: 2026-10-01
---

# OWNERS ― 更新責任マップ

要約：topic／フォルダごとに、誰が鮮度と整合性を保つかを1ファイルに集約する。CODEOWNERS式。1人運用でも、引き継ぎとチーム化に備えて雛形を置いておく。

## 責任表（記入見本）
| 対象 | 更新責任者 | レビュー頻度 | 最終棚卸し日 |
|---|---|---|---|
| 00_ナレッジ/concepts/ | （あなた） | 月次 | 2026-07-01 |
| 30_インプット/sources/ | （取り込み担当） | 取り込み時 | 2026-07-01 |
| 20_案件/entities/ | （あなた） | 四半期 | 2026-07-01 |
| index.md / hot.md | （あなた） | 週次 | 2026-07-01 |

氏名はこのVaultを使う人に置き換える。チームで使うなら行を足し、フォルダや topic 単位で責任者を分ける。

## 運用
- CODEOWNERS は放置するとそれ自体が古くなる。責任者が異動・交代したのに表が古いまま、という失敗を防ぐため、レビューのたびに必ず見直す … Aviator https://www.aviator.co/blog/code-ownership-using-codeowners-strategically/ （2025-06-10）
- 月次の [[レビュー記録_テンプレ]] 実施時に、この表の最終棚卸し日とowner欄を更新する

## 関連
- [[出所と確からしさ_テンプレ]]
- [[レビュー記録_テンプレ]]
- [[運用ルール_チーム共有とガバナンス]]
- [[共有の第二の脳]]

> 出典: Aviator「Code Ownership: Using CODEOWNERS Strategically」 https://www.aviator.co/blog/code-ownership-using-codeowners-strategically/ （2025-06-10、放置するとCODEOWNERSはstaleになる）。研修用に整理。
