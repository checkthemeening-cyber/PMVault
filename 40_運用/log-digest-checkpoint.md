---
type: 参考
status: 参照用
date: 2026-07-25
topic: log-digest
tags: [運用, log]
---

# log.md 棚卸しチェックポイント

`update-hot` skill が log.md を棚卸しする際に読む状態ファイル。ここより新しい日付のエントリだけを次回の棚卸し対象にする。

最終処理日: 未処理（次回 update-hot 実行時に log.md 全体を初回棚卸しする）

## 関連
- update-hot skill（`.claude/skills/update-hot/SKILL.md`）
- [[40_運用/log]]
