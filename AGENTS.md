# AGENTS.md

このVaultでAIが守る前提は WIKI.md / CLAUDE.md と同じ。要点：
- 起動時に WIKI.md・index.md・40_運用/hot.md・40_運用/persona.md・40_運用/domain.md を読む
- 全ノートに4つの手がかり（type/when/topic/status）。命名は `YYYY-MM-DD-種類-主題`
- 引き出しは hot→index→関連ページの順で必要分だけ読む。根拠ノートを必ず添える
- 取り込みは ingest、繋ぎ直し・点検は lint。複製でなく `[[リンク]]` で繋ぐ
- 出典・日付を残し、未確認は明記
- .obsidian は触らない。40_運用/log.md は追記のみ。削除・大量改変は承認制
