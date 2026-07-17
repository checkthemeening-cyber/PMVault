---
type: 概念
status: 参照用
date: 2026-07-01
topic: 第二の脳
tags: [第二の脳, AI連携, ClaudeCode, 設計パターン]
source: 各要点にURL併記
certainty: 有力
author: 協働
last_verified: 2026-07-01
---

# AI第二の脳の設計パターン

要約：このVaultが採る設計が、公開されているどの考え方に対応するかを出典付きで対照する参照ページ。

## このVaultとの対応（Karpathyの三層）
| 三層 | 役割 | このVaultの該当 |
|---|---|---|
| raw（不変の取込元） | AIは読むだけ・改変しない | `30_インプット/.raw/` |
| wiki（AIが生成・相互リンク） | 要約・概念・人物ページ | `30_インプット/sources/` `00_ナレッジ/concepts/` `20_案件/entities/` |
| schema（構造と規約の契約） | 命名・frontmatter・禁止事項 | `CLAUDE.md` `AGENTS.md` `WIKI.md` |

出典: Karpathy「llm-wiki」 https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f （2026、ingest/query/lint・index/logを含む）

## 要点
- CLAUDE.mdは人間とAIのAPI契約。新入社員をオンボードするように前提・規約・禁止事項を書く … Kenneth Reitz https://kennethreitz.org/essays/2026-03-06-obsidian_vaults_and_claude_code （2026-03-06、467ファイルの実運用）
- LLMが最初に読む。markdownは解析層なしでLLMが直接読めるので、説明的なファイル名とトピック別フォルダで、開く前に関連性を判定できる … Minibase https://www.minibase.md/blog/obsidian-ai-agent-mcp-markdown-workflow/ （2026-03-31）
- 引き出しは hot→index→必要ページの順で必要分だけ読む。hotは直近~500語のキャッシュ … claude-obsidian README＋Karpathy gist（Reitzはprogressive disclosureとして言及）
- 取り込みループ ingest→query→lint。8カテゴリのlint（孤立ノート・リンク切れ・抜け・矛盾）で、無警告の品質低下（孤立ノート・リンク切れ・矛盾）を検出する … claude-obsidian https://github.com/AgriciDaniel/claude-obsidian （MIT, v1.9.2, 8.3k★, 2026-05-28）
- 誰が書くか論争。(A)agents read, humans write＝AI生成物でVaultを汚さずClaudeのメモは ~/.claude に分離 / (B)LLMがwiki本体を保守。このVaultは(B)寄り。折衷は生成ページに出所・著者・鮮度を必ず付ける … starmorph https://blog.starmorph.com/blog/obsidian-claude-code-integration-guide （2026-03-10）
- 出所・鮮度メタデータ＋lintで「公開情報のみ・一次情報URL＋日付」を機械的に担保し、stale claim・矛盾を検出する … 仕組みはclaude-obsidianの8カテゴリlint＋このVaultのWIKI情報ルール（会議自動取込のyoutrust記事はこの点を扱わない）
- 記憶の二層構造。恒久ナレッジはObsidian wiki、技術議論やデバッグ履歴はローカルDB（SQLite FTS5+ベクトル）に自動保存。同期はpull→rsyncの順で分岐を防ぐ … 0rv3 https://zenn.dev/0rv3/articles/b6a7172bfda1ed （2026-06-11）

## 接続（MCP、業務移行時の選択肢）
研修はMarkdownのみモードを正とし、claude.ai/Desktop/モバイルや業務PCから触る段階でMCPを足す。
- MarkusPfundstein mcp-obsidian … Obsidian Local REST APIプラグイン必須、約4,000★ https://github.com/MarkusPfundstein/mcp-obsidian

## スケール（規模が大きくなった後）
- Obsidian CLI（1.12）の孤立ノート検出は grep比54倍（4,663ファイルで15.6s→0.26s） … starmorph（同上）
- ハイブリッド検索（BM25+contextual prefix+cosine rerank）は claude-obsidian が実装。精度の向上幅は出典で未確認のため数値は載せない

## 関連
- [[WIKI]]
- [[共有の第二の脳]]
