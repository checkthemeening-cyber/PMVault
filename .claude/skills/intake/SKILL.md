---
name: intake
description: 人間の頭の中にある知識を、AIから質問して楽に引き出し、4つの手がかり付きのノートにして保存する。「intake」「ナレッジを入れたい」「メモを取って」「頭の中を出したい」で発火。
---

# intake ― 人間から知識を引き出してwikiに入れる

claude-obsidianの ingest は「資料」を取り込みますが、intake は「人間の頭の中」を引き出します。質問に選択肢で答えるだけで、4つの手がかり付きのノートになります。

## 進め方
1. 何についての知識かを一言もらう
2. AskUserQuestion で深掘りの質問を1〜4個まとめて出す。選択肢中心、自由記述は「その他」で受ける。3巡を上限
3. 集まった内容を、命名 `YYYY-MM-DD-種類-主題.md` ＋ frontmatter（type/status/date/topic/tags）で保存する
   - 議事・走り書きは `30_インプット/sources/`、概念として残るものは `00_ナレッジ/concepts/`、人物・組織は `20_案件/entities/`
4. 既存ページへ `[[wikilink]]` を張り、`index.md` を更新する

## 注意
- 一度に多く聞かない。答えやすい粒度にする
- 整形や相互リンクは `lint` と `ingest` に委ね、まずノート化する

---
> ハーネス種別: Skill（手動発火 `/intake`）
> セキュリティ: Givery 講師 安田によるセキュリティチェック済み（保存先はVault内のみ）
> 出典: 自作（claude-obsidian の取り込みループに、AskUserQuestion による人間からの引き出しを足したもの）
