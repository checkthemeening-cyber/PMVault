Set-Location "C:\Users\check\PMVault"
$logFile = "C:\Users\check\PMVault\.claude\scripts\logs\nikkei-morning-" + (Get-Date -Format 'yyyyMMdd') + ".log"
New-Item -ItemType Directory -Force (Split-Path $logFile) | Out-Null
("[" + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + "] nikkei-news morning start") | Out-File -FilePath $logFile -Append -Encoding utf8
& "C:\Users\check\.local\bin\claude.exe" --dangerously-skip-permissions -p "Execute the nikkei-news skill in morning mode" 2>&1 | Out-File -FilePath $logFile -Append -Encoding utf8
("[" + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + "] nikkei-news morning done. exit=" + $LASTEXITCODE) | Out-File -FilePath $logFile -Append -Encoding utf8

# SIG # Begin signature block
# MIIFpAYJKoZIhvcNAQcCoIIFlTCCBZECAQExDzANBglghkgBZQMEAgEFADB5Bgor
# BgEEAYI3AgEEoGswaTA0BgorBgEEAYI3AgEeMCYCAwEAAAQQH8w7YFlLCE63JNLG
# KX7zUQIBAAIBAAIBAAIBAAIBADAxMA0GCWCGSAFlAwQCAQUABCCp3rDMvkGMEt0k
# S8GNe+zqt9kTbD9QFDPPGgLN1KAGXaCCAxQwggMQMIIB+KADAgECAhAZJRYA597D
# lUpVWTyk/jn3MA0GCSqGSIb3DQEBCwUAMCAxHjAcBgNVBAMMFVBNVmF1bHQgTG9j
# YWwgU2NyaXB0czAeFw0yNjA3MjQwMDEyNTRaFw0zMTA3MjQwMDIyNTRaMCAxHjAc
# BgNVBAMMFVBNVmF1bHQgTG9jYWwgU2NyaXB0czCCASIwDQYJKoZIhvcNAQEBBQAD
# ggEPADCCAQoCggEBANOsGWEVqSxhSUo3Yv4xGOXgDZZEebdymXrNhOBFQ5CvYoLx
# YUn+wR1Px0hoGPrpkDn00Y7GnJEf3Eet2riKnw5HozBQsEtJBh2xWemIkFxJRyDg
# 8DPmPtlaP8afisOyh+xlBbpesx3211nAZyYQcLabdo9JVO6X928/RQardmW2Z3bu
# M206n5ivO/10InsE4DWfvVV+v+akrddp6m7KeTDgMqvmgJloqPLkuGVNYr8in60Z
# pDqkh7JdQvkZt6e57nCp0Wfzth4sKblcmfk0z+1hs2PPFI6xn6phv4/yb/GljSuq
# 6Dz+Pj/jRR1aEy/zevHoYplKEbltdSuBE8lzq4UCAwEAAaNGMEQwDgYDVR0PAQH/
# BAQDAgeAMBMGA1UdJQQMMAoGCCsGAQUFBwMDMB0GA1UdDgQWBBShSWdyeewpGMlk
# MK7EmC8ESdCIYTANBgkqhkiG9w0BAQsFAAOCAQEAzS3MNsfLAnXxO60lPLYUAPZi
# mpFNutUI5EMXlFb2m8+VAoDuIvOwBn8/L2k3BPfDGbA8Pwh0axvzxhjwCvmof1Th
# L2eJ0WaOCBYETcaNS2deWKQs7m/KugyshAZrlacXU/LgbCYI4v9sRS4Qd5Vp8LWu
# MUBbGftMat7pTffx6nMN1GD0zAsVAGSNFUoUzF3ePTiT7scjo/iM/ycsduzFAoJb
# Ki5MhwAcARQqcFLc+b+voH6Shi++EUtyPUXlDnPKTob30SUP+M/wbShZcZEoXCHm
# yxYCsCFoiTK+UzeY38qwDf96wCsK90+WFe6yT0HHDCYBmzQZUUZlEPBNiJ2Y6zGC
# AeYwggHiAgEBMDQwIDEeMBwGA1UEAwwVUE1WYXVsdCBMb2NhbCBTY3JpcHRzAhAZ
# JRYA597DlUpVWTyk/jn3MA0GCWCGSAFlAwQCAQUAoIGEMBgGCisGAQQBgjcCAQwx
# CjAIoAKAAKECgAAwGQYJKoZIhvcNAQkDMQwGCisGAQQBgjcCAQQwHAYKKwYBBAGC
# NwIBCzEOMAwGCisGAQQBgjcCARUwLwYJKoZIhvcNAQkEMSIEIFrCg+HHzxbPBmsr
# zi9NaMYlfTE5oWntPl6GgfivW3TsMA0GCSqGSIb3DQEBAQUABIIBAC+p6vsPkLKI
# +S2IarDLpMkwowdX5DJGEV2GxiYkX33OFZPr0Vqnt/PPwo3cACSz6IKyTGQGJ3VX
# XVgfXqhC8OEvBvr4bko39bamH57qKl46F0K3al+Ae+yavdphbSu9B+EI9+qnoFDn
# nH4ztXbKW+tQmF9EVtoLhKBq8wsbe02UpVwvmz64uLIstQFHYWuAmJZ2tc4aCO4U
# F8e3IDTcI6CxEsVvrfiAZmakVgLri9MUU2rTAhXEyNeOMtOzFuU1W8rSEf5NHvvh
# aYR1HwlisEAhdUVTXPCanVXqq+XJ6/M7v2pAnaic2zcoHL3XEITzLKnp6mQdWF1g
# ztn4hTgu+6Y=
# SIG # End signature block
