powershell Stop-Service ssh-agent
powershell Stop-Service sshd
powershell Remove-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
powershell Remove-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
powershell Start-Sleep 10
