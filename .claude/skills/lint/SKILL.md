---
name: lint
description: Vault全体の健全性を点検する。孤立ノート・リンク切れ・知識の抜け・矛盾・4手がかりの欠落を検出して直し方を提案する。「lint」「点検して」「Vaultの健康診断」で発火。
---

# lint ― Vaultの健全性点検

旧 organize / sync-master の役割もここに統合しています。

## 検出するもの
- 孤立ノート（どこからもリンクされていない）
- リンク切れ（`[[存在しないページ]]`）
- 知識の抜け（言及はあるが詳細ページが無いトピック）
- 矛盾（食い違う記述）
- 4つの手がかりの欠落（type/when/topic/status やfrontmatterが無い、命名が型に従っていない）

## やること
1. 上記を洗い出し、重要度順に一覧化する
2. 直し方を提案する（リンクの張り直し、不足ページの作成、frontmatter追加、命名修正）
3. 承認を得てから直す。一括変換は避け、提案ベースで進める

---
> ハーネス種別: Skill（手動発火 `lint`）
> セキュリティ: Givery 講師 安田によるセキュリティチェック済み（操作はVault内のみ）
> 出典: claude-obsidian（AgriciDaniel, MIT, https://github.com/AgriciDaniel/claude-obsidian ）を研修用に調整
