---
name: autoresearch
description: あるトピックを公開情報で自律的に3ラウンド調査し、出典付きwikiページとして 30_インプット/sources に保存する。「autoresearch」「自律調査」「〜を調べて保存して」で発火。
---

# autoresearch ― 自律リサーチ

## やること（3ラウンド）
1. 検索 … トピックを公開情報で検索し、一次情報を優先して候補を集める
2. 取得・精査 … 重要なものを読み、主張と出典URL（日付）の対にする。未確認は明記
3. 統合・ファイリング … `30_インプット/sources/` に出典付きwikiページを生成し、既存ページへ `[[リンク]]`、`index.md`/`40_運用/log.md` を更新

## ルール（公開情報・安全）
- まとめ記事より一次情報。古い情報は日付を添える
- 出典のない断定をしない

---
> ハーネス種別: Skill（手動発火 `/autoresearch`）
> セキュリティ: Givery 講師 安田によるセキュリティチェック済み（egress検証）
> 出典: claude-obsidian（AgriciDaniel, MIT, https://github.com/AgriciDaniel/claude-obsidian ）を研修用に調整
