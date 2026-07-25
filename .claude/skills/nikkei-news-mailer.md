# 日経ニュース メール配信スキル

nikkei-news スキル（morning/evening）が収集した当該回の結果を HTML メールに整形し、
指定アドレスへ送信する。[[nikkei-news]] の実行後に続けて動く後段の仕組み。

## 位置づけ

- **Claudeは呼ばない**: 収集済みの Markdown（`## 本日のまとめ` を含め、既に Claude が
  Step 4.5 で解釈を書き直したもの）をそのまま機械的に HTML 化して送るだけの決定的な処理。
  トレンド解釈などの追加判断はしない。
- nikkei-news の収集タスク（`NikkeiNewsMorning` 9:00 / `NikkeiNewsEvening` 16:00）とは
  **独立した別タスク**として、収集完了後に十分な余裕を置いて実行する。

## 実装

- **スクリプト**: `.claude/scripts/nikkei-news-mailer.ps1`
- **実行**: `powershell -File nikkei-news-mailer.ps1 -Mode morning|evening`
- **対象データ**:
  - `morning`: `00_ナレッジ/nikkei-news/daily/YYYY/MM/DD/` 配下の当日6カテゴリ全文
    （資源エネルギー・建設・不動産・物流・運輸・商社・卸売り・自動車・素材）
  - `evening`: 各カテゴリファイル内の `## 夕刊更新` セクションのみ（差分がなければそのカテゴリは省略）
- **送信元/送信先**: matsuo.and.consultants@gmail.com → matsuo.and.consultants@gmail.com
- **送信方式**: Gmail SMTP（smtp.gmail.com:587, STARTTLS）。
  認証はアプリパスワードを使用（2段階認証必須。本体パスワードは不可）。
- **認証情報の保管**: `.claude/scripts/secrets/gmail-app-password.secure.txt`
  に Windows DPAPI で暗号化して保存（現在のWindowsユーザー・このPCでのみ復号可能）。
  このディレクトリは `.gitignore` で除外済み。**gitリポジトリには絶対にコミットしない**。
- **ログ**: `.claude/scripts/logs/nikkei-mailer-YYYYMMDD-{mode}.log`

## スケジュール（Windows タスクスケジューラ）

| タスク名 | 時刻 | 内容 |
|---|---|---|
| NikkeiNewsMailerMorning | 毎日 9:15 | `nikkei-news-mailer.ps1 -Mode morning` |
| NikkeiNewsMailerEvening | 毎日 16:15 | `nikkei-news-mailer.ps1 -Mode evening` |

nikkei-news本体（9:00 / 16:00）から15分後に設定し、収集完了を待ってから送信する。

## 認証情報を差し替える場合

```powershell
$secure = ConvertTo-SecureString "新しいアプリパスワード" -AsPlainText -Force
$secure | ConvertFrom-SecureString | Out-File -FilePath "C:\Users\check\PMVault\.claude\scripts\secrets\gmail-app-password.secure.txt" -Encoding utf8 -Force
```

## 注意事項

- 収集タスク自体が失敗し当日分のフォルダが無い場合も、その旨を記載したメールを送信する
  （無言で失敗しない）。
- HTML変換は nikkei-news が出力する定型フォーマット（見出し・`**field**: value`・引用・
  区切り線・Markdownリンク）のみを想定した簡易変換であり、汎用Markdownパーサーではない。
