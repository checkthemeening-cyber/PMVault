Set-Location "C:\Users\check\PMVault"
$logFile = "C:\Users\check\PMVault\.claude\scripts\logs\nikkei-evening-" + (Get-Date -Format 'yyyyMMdd') + ".log"
New-Item -ItemType Directory -Force (Split-Path $logFile) | Out-Null
("[" + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + "] nikkei-news evening start") | Out-File -FilePath $logFile -Append -Encoding utf8
& "C:\Users\check\.local\bin\claude.exe" --dangerously-skip-permissions -p "Execute the nikkei-news skill in evening mode" 2>&1 | Out-File -FilePath $logFile -Append -Encoding utf8
("[" + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + "] nikkei-news evening done. exit=" + $LASTEXITCODE) | Out-File -FilePath $logFile -Append -Encoding utf8
