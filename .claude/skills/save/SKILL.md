---
name: save
description: いまの会話で価値が出た内容を、wikiノートに変換して 20_案件/sessions に保存し、index.mdを更新する。「save」「これを残して」「会話をノートに」で発火。
---

# save ― 会話をwikiノートに残す

## やること
1. ここまでの会話を読み、要点・決めたこと・次の一手を抽出する
2. `20_案件/sessions/YYYY-MM-DD-種類-主題.md` を作り、4つの手がかりをfrontmatterに付ける
3. 既存の概念・人物ページへ `[[wikilink]]` を張る。新しい概念が出たら `00_ナレッジ/concepts/` にもページを作る
4. `index.md` と `40_運用/log.md` を更新する
5. 名前を指定されたら（save 〇〇）その主題で保存する

## ルール
- 出典・日付を残す

---
> ハーネス種別: Skill（手動発火 `/save`）
> セキュリティ: Givery 講師 安田によるセキュリティチェック済み（操作はVault内のみ）
> 出典: claude-obsidian（AgriciDaniel, MIT, https://github.com/AgriciDaniel/claude-obsidian ）を研修用に調整
