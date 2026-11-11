# Installs the reel-edit-style Claude Code skill and everything it needs on Windows 10/11.
# Run in PowerShell:  powershell -ExecutionPolicy Bypass -File .\install-windows.ps1
# Safe to run again: it skips what is already installed.
$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Dest = Join-Path $env:USERPROFILE ".claude\skills\reel-edit-style"
$Tools = Join-Path $env:USERPROFILE ".reel-tools"
function Have($c) { return [bool](Get-Command $c -ErrorAction SilentlyContinue) }
function Refresh-Path { $env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User") }

Write-Host "== 1/6 winget"
if (-not (Have winget)) { throw "winget is missing. Install 'App Installer' from the Microsoft Store, then run this again." }

Write-Host "== 2/6 Tools: Python, Node.js, FFmpeg, Git, yt-dlp"
$pkgs = @(
  @{id="Python.Python.3.12"; cmd="python"},
  @{id="OpenJS.NodeJS.LTS"; cmd="node"},
  @{id="Gyan.FFmpeg"; cmd="ffmpeg"},
  @{id="Git.Git"; cmd="git"},
  @{id="yt-dlp.yt-dlp"; cmd="yt-dlp"}
)
foreach ($p in $pkgs) {
  if (Have $p.cmd) { Write-Host "  $($p.cmd) already installed" }
  else { winget install --id $p.id -e --silent --accept-package-agreements --accept-source-agreements; Refresh-Path }
}

Write-Host "== 3/6 whisper.cpp (whisper-cli.exe)"
$WDir = Join-Path $Tools "whisper"
$have = (Have whisper-cli) -or (Test-Path (Join-Path $WDir "whisper-cli.exe")) -or (Test-Path (Join-Path $WDir "Release\whisper-cli.exe"))
if ($have) { Write-Host "  whisper-cli already installed" } else {
  New-Item -ItemType Directory -Force -Path $WDir | Out-Null
  $rel = Invoke-RestMethod "https://api.github.com/repos/ggml-org/whisper.cpp/releases/latest" -Headers @{ "User-Agent" = "reel-edit-style-installer" }
  $asset = $rel.assets | Where-Object { $_.name -eq "whisper-bin-x64.zip" } | Select-Object -First 1
  if (-not $asset) { throw "Could not find whisper-bin-x64.zip in the latest whisper.cpp release. Download it by hand from https://github.com/ggml-org/whisper.cpp/releases and unzip into $WDir" }
  $zip = Join-Path $env:TEMP "whisper-bin-x64.zip"
  Invoke-WebRequest $asset.browser_download_url -OutFile $zip
  Expand-Archive $zip -DestinationPath $WDir -Force
  $exe = Get-ChildItem $WDir -Recurse -Filter "whisper-cli.exe" | Select-Object -First 1
  $userPath = [Environment]::GetEnvironmentVariable("Path","User")
  if ($userPath -notlike "*$($exe.DirectoryName)*") { [Environment]::SetEnvironmentVariable("Path", "$userPath;$($exe.DirectoryName)", "User") }
  Refresh-Path
}

Write-Host "== 4/6 Whisper speech model (~550 MB, once)"
$MDir = Join-Path $env:USERPROFILE ".whisper-models"
$Model = Join-Path $MDir "ggml-large-v3-turbo-q5_0.bin"
if (Test-Path $Model) { Write-Host "  model already present" } else {
  New-Item -ItemType Directory -Force -Path $MDir | Out-Null
  Invoke-WebRequest "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin" -OutFile "$Model.part"
  Move-Item "$Model.part" $Model -Force
}

Write-Host "== 5/6 Skill -> $Dest"
New-Item -ItemType Directory -Force -Path (Join-Path $env:USERPROFILE ".claude\skills") | Out-Null
if (Test-Path $Dest) { Remove-Item $Dest -Recurse -Force }
Copy-Item (Join-Path $Here "skill\reel-edit-style") $Dest -Recurse

Write-Host "== 6/6 Hyperframes renderer (downloads itself once) + final check"
try { npx --yes hyperframes@0.9.7 --version | Out-Null } catch {}
python (Join-Path $Dest "scripts\check_setup.py")
Write-Host ""
Write-Host "Done. Close and reopen Claude Code (so the new PATH loads), then say: 'Make a reel from <file> using the reel-edit-style skill'."
