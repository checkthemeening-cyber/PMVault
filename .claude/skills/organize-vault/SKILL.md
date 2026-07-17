---
name: organize-vault
description: 散らかった保管庫を、決まったフォルダ構造（00_ナレッジ / 10_業界と事例 / 20_案件 / 30_インプット / 40_運用 / _templates / _研修）へ、4つの手がかりを保ったまま整え直す。「整理」「organize」「フォルダを整頓して」で発火。
---

# organize-vault ― 保管庫の整理整頓

このVaultを、決まった構造に整え直すためのSkill。ファイルが増えて直下が煩雑になったときに呼ぶ。1回きりの整理ではなく、崩れるたびに繰り返し使うことを前提にする。

## 目標の構造

直下には入口と制御ファイルだけを置き、中身はグループに分ける。

- 直下（動かさない）: `README.md` / `CLAUDE.md` / `AGENTS.md` / `WIKI.md` / `index.md` / `_templates/` / `.claude/` / `.obsidian/`
- `00_ナレッジ/` … concepts・frameworks・benchmarks・plays（概念・手法・型・進め方のプレイブック）
- `10_業界と事例/` … industries・cases・trends（業界プロファイル・事例バンク・動向）
- `20_案件/` … engagements・sessions・decisions・entities（案件ワーク・会話ログ・意思決定・人物組織）
- `30_インプット/` … .raw・sources（取り込み元・そこから生成したソース）
- `40_運用/` … persona・domain・OWNERS・overview・hot・log（AI設定・私の情報・責任マップ・概要・キャッシュ・操作ログ）
- `_研修/` … exercise・hints・docs・_setup・_実績（研修で使うもの）

## 手順

1. 現状把握
   直下と各フォルダを一覧する。各ノートの frontmatter（type / topic / status）を確認する。

2. 分類（type と topic で振り分け）
   - 概念・手法・型・プレイブック → `00_ナレッジ`
   - 業界・事例・動向 → `10_業界と事例`
   - 案件・会話ログ・意思決定・人物組織 → `20_案件`
   - 取り込み元・調査ソース → `30_インプット`
   - AI設定・私の情報・責任マップ・概要・キャッシュ・操作ログ（persona / domain / OWNERS / overview / hot / log）→ `40_運用`
   - 雛形（*_テンプレ）→ `_templates`
   - 演習・ヒント・案件背景・セットアップ・実績・研修メモ → `_研修`
   - どのグループにも当てはまらないものは動かさず「未分類」として提案時に確認する

3. 移動計画の提示
   旧パス → 新パス を表で出す。どの type / topic からそう判断したか、理由を1行添える。

4. 承認 → 実行
   人の承認を得てから、フォルダを作り、ファイルを移動する。削除はしない。

5. 参照の更新
   移動に合わせて、`index.md`・`WIKI.md`・`CLAUDE.md` / `AGENTS.md` の起動時参照・各ノートの `[[リンク]]`・`OWNERS` のパスを新しい場所に直す。ファイル名だけの `[[リンク]]` は変えなくてよい（Obsidianがファイル名で解決する）。パス付きの `[[folder/file]]` だけ直す。

6. 点検
   `lint` で孤立ノート・リンク切れ・重複を洗う。`update-hot` で hot.md を最新の文脈にする。

## 守ること

- `.obsidian` と `.claude` は触らない
- 承認なしに移動・削除しない（提案 → 承認 → 実行）
- 4つの手がかり（type / when / topic / status）と命名規則 `YYYY-MM-DD-種類-主題` は保つ
- 直下は入口の5ファイルと `_templates` だけに保つ。ノートを直下に散らかさない
