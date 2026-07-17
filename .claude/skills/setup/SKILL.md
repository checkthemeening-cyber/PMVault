---
name: setup
description: このVaultを受講者の環境に合わせて初期設定する。Vaultの場所・名前・OSを反映し、命令ログのHookを登録する。研修で最初に1回だけ実行する。「setup」「初期設定」「セットアップ」「環境に合わせて」「はじめに」で発火。
---

# setup ― 環境に合わせた初回セットアップ

配布状態のVaultを、あなたの環境に合わせて初期化する。研修の最初に1回だけ実行する。

## やること（この順で、受講者に確認しながら進める）

1. Vaultの場所を特定する
   - `pwd` でいまのフォルダ（＝このVaultの絶対パス）を確認する。これを VAULT とする。

2. 受講者に3点だけ聞く（AskUserQuestion でまとめて）
   - 名前（ノートの owner や domain に入れる。ニックネーム可）
   - OS（Mac / Windows）
   - 命令ログを取るか（既定：取る）

3. 命令ログHookを登録する（ここが環境依存の本体）
   - ユーザー設定 `~/.claude/settings.json` を読む（無ければ新規作成）。
   - `hooks.UserPromptSubmit` に、このVaultの `log-prompt.mjs` を VAULT のパスで呼ぶ command を1つ足す。既存の hooks は消さず追記だけ。同じ command が既にあれば重複させない。
   - command は OS に合わせる：
     - Mac / Linux : `OBSIDIAN_VAULT="<VAULT>" node "<VAULT>/.claude/hooks/log-prompt.mjs"`
     - Windows : `set OBSIDIAN_VAULT=<VAULT> && node "<VAULT>\.claude\hooks\log-prompt.mjs"`
   - 変更前に settings.json の差分を見せて、承認を得てから書き込む。
   - 「ログを取らない」を選んだら、この手順は飛ばす。

4. 名前を反映する
   - `_templates/出所と確からしさ_テンプレ.md` の `owner: （記入者）` を、受講者の名前に置き換える。
   - `40_運用/domain.md` の「役職 / 立場」に、聞けた範囲で1行だけ入れる（任意。空でもよい）。

5. Vaultの場所を控える
   - `40_運用/overview.md` の末尾に「Vaultの場所：<VAULT>」を1行足す（次回以降の自己参照用）。

6. 完了マーカーを置く
   - `_研修/_実績/.setup-done` を作り、実行日を1行書く。CLAUDE.md はこのファイルの有無で初回かどうかを判断する。

7. 変えた点を3〜5行で報告し、次のステップとして `/wiki` を案内する。

## ルール
- 追記のみ。`~/.claude/settings.json` は既存設定を消さず、この項目だけ足す。書き込み前に必ず差分の承認を取る。
- Vaultの外は触らない。書き込むのは `~/.claude/settings.json`（Hook登録）と このVault内だけ。
- 失敗しても止めない。Windowsでnodeが無い等でHook登録ができない場合、命令ログは任意機能なので飛ばして先へ進む。
- 個人情報は保存しない。名前はニックネームで構わない。

---
> ハーネス種別: Skill（手動発火 `setup`）。研修の最初に1回だけ実行する。
> セキュリティ: 書き込みは `~/.claude/settings.json`（追記）と Vault内のみ。外部送信なし。Givery によるチェック済み。
> 出典: Claude Code 公式 hooks / settings https://code.claude.com/docs/en/hooks
