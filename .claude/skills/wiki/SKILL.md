---
name: wiki
description: このVaultをLLM Wiki形式で初期化・整備する。index.md/40_運用/hot.md/40_運用/log.mdの骨格を整え、前回の続きから再開する。「wiki」「Vault初期化」「索引を整えて」「続きから」で発火。
---

# wiki ― Vaultの骨格を整える・再開する

最初に1回、またはindex.mdが最新でなくなったときに使う。

## やること
1. WIKI.md の規約に沿って、`index.md` / `40_運用/hot.md` / `40_運用/log.md` / `40_運用/overview.md` と `00_ナレッジ/concepts/` `20_案件/entities/` `30_インプット/sources/` `20_案件/sessions/` `30_インプット/.raw/` が揃っているか点検し、足りなければ作る
2. 既存ノートを走査し、`index.md` のカタログを最新化する（type/topic/status を拾って並べる）
3. `40_運用/hot.md` を読み、前回の続きがあれば「いまどこまで来ているか」を要約して提示する
4. 4つの手がかり（type/when/topic/status）が無いノートを一覧化し、付け方を提案する（一括変換はしない）

## 注意
- 既存ノートを勝手に大量改変しない。提案→承認→実行
- .obsidian は触らない

---
> ハーネス種別: Skill（手動発火 `/wiki`）
> セキュリティ: Givery 講師 安田によるセキュリティチェック済み（操作はVault内のみ、公開情報限定）
> 出典: LLM Wiki パターン（Karpathy）/ claude-obsidian（AgriciDaniel, MIT, https://github.com/AgriciDaniel/claude-obsidian ）を研修用にMarkdownのみモードへ調整
