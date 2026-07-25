#!/usr/bin/env bash
set -u

# このスクリプトは .claude/hooks/ 配下にあるため、2階層上がVaultルート
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_FILE="$VAULT_DIR/40_運用/organize.log"

cd "$VAULT_DIR" || {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] cd失敗: $VAULT_DIR" >> "$LOG_FILE"
  exit 1
}

PROMPT='直下に散らかった新しいノートだけを、organize-vault の構造に沿って安全なフォルダへ移動する。既存のフォルダ構造は触らない。ファイルの削除は絶対にしない。これは自動実行なので、確認は求めず最後まで実行する。'

OUTPUT="$(claude -p "$PROMPT" \
  --allowedTools "Read,Glob,Grep,Bash(mv *),Bash(mkdir *)" \
  --disallowedTools "Bash(rm *),Bash(rmdir *),Bash(rd *),Bash(del *),Bash(Remove-Item *)" \
  2>&1)"
STATUS=$?

{
  echo "----------------------------------------"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] organize-vault-daily 実行"
  if [ "$STATUS" -eq 0 ]; then
    echo "結果: 成功"
  else
    echo "結果: 失敗 (exit code: $STATUS)"
  fi
  echo "--- Claude出力 ---"
  echo "$OUTPUT"
} >> "$LOG_FILE"

exit "$STATUS"
