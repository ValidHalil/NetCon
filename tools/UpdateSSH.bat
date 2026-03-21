powershell New-Item -Path $HOME\.ssh -ItemType Directory -Force
start /w pkgmgr /iu:"TelnetClient"
powershell Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
powershell Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
powershell powershell Set-Service -Name ssh-agent -StartupType Manual
powershell Start-Service ssh-agent
powershell powershell Set-Service -Name sshd -StartupType Manual
powershell Start-Service sshd