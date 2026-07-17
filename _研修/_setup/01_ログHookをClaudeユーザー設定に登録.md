---
tags: [setup, hook]
category: 設定
---

# ログHookの登録

> 通常は `/setup` が自動で登録します。手動で確認・設定する場合はこの手順を参照してください。

このVaultでは、Claudeへのプロンプトを `40_運用/log.md` に自動で残します。記録はHookが担います。Hookは特定の操作を契機に実行されるスクリプトで、ここではプロンプト送信のたびに動きます。

演習プロジェクトディレクトリのプロンプト記録もこのVaultに集約するため、プロジェクト個別ではなくClaudeのユーザー設定に登録します。

## 手順

1. Vaultの場所を確認します。この手順は `~/Documents/PMVault` に置いた前提です。違う場所なら、後述の環境変数で指定します。

2. ユーザー設定ファイルを開きます。

   - 場所：`~/.claude/settings.json`
   - 無ければ新規作成します

3. 次の `hooks` を足します。すでに他の設定があるなら `hooks` の項目だけ追加してください。

   ~~~json
   {
     "hooks": {
       "UserPromptSubmit": [
         {
           "hooks": [
             {
               "type": "command",
               "command": "node ~/Documents/PMVault/.claude/hooks/log-prompt.mjs"
             }
           ]
         }
       ]
     }
   }
   ~~~

4. Vaultの場所が `~/Documents/PMVault` 以外のときは、コマンドの前に環境変数で場所を渡します。

   ~~~json
   "command": "OBSIDIAN_VAULT=\"$HOME/パス/あなたのVault\" node ~/パス/あなたのVault/.claude/hooks/log-prompt.mjs"
   ~~~

5. Claudeを再起動して、何かプロンプトを送ります。`40_運用/log.md` に追記されていれば登録完了です。

## Tips
- 記録されるのはプロンプトの本文だけです。長いプロンプトは先頭600文字までにまとめます
- カテゴリ（調査・作成・修正・整理・その他）はプロンプトの内容から自動で振り分けます。後からタグ検索や週次レビューに活用できます
- Hookが失敗してもClaudeの動作は止まりません

---
> ハーネス種別: Hook（UserPromptSubmit。プロンプト送信時に発火し 40_運用/log.md へ追記）
> セキュリティ: Givery によるセキュリティチェック済み（書き込み先はVault内 40_運用/log.md のみ、外部送信なし）
> 出典: 自作（Claude Code 公式 hooks 仕様 https://code.claude.com/docs/en/hooks）
