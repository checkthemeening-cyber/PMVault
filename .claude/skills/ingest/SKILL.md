---
name: ingest
description: 30_インプット/.raw/ の資料を読み込み、要点を抽出して相互リンクしたwikiページ（8〜15枚目安）を生成し、index.mdと40_運用/log.mdを更新する。「ingest」「取り込んで」「この資料をwiki化」で発火。
---

# ingest ― 資料の取り込みとwiki化

ingest は資料をwikiページに変換してVaultに追加する。

## やること
1. 対象（`30_インプット/.raw/` のファイル、または指定パス）を読む。複数なら「ingest all」で一括＋相互参照
2. エンティティ（人・組織・トピック）と概念を抽出し、wikiページに分けて生成する
   - 取り込んだ資料そのものの要約は `30_インプット/sources/` に、概念は `00_ナレッジ/concepts/`、人物・組織は `20_案件/entities/`
   - 1ソースから関連する複数ページ（目安8〜15枚）に分け、既存ページへ `[[wikilink]]` を張る
3. すべてのページに4つの手がかり（type/when/topic/status）をfrontmatterと命名で付ける
4. `index.md` のカタログと `40_運用/log.md`（取り込み記録）を更新する
5. 矛盾や未確認があれば、そのpage内に「未確認」「要確認」で明記する

## ルール
- 主張には出典（元ソース名・URL・日付）を残す。創作で埋めない
- リンクは複製でなく `[[ ]]` で繋ぐ

---
> ハーネス種別: Skill（手動発火 `ingest`）
> セキュリティ: Givery 講師 安田によるセキュリティチェック済み（操作はVault内のみ）
> 出典: LLM Wiki パターン（Karpathy）/ claude-obsidian（AgriciDaniel, MIT, https://github.com/AgriciDaniel/claude-obsidian ）を研修用に調整
