# setup-test-laptop.ps1 -- full build: get (or update) the course code on a Windows 11 test
# laptop, then pre-install every laptop script's Python packages so they run on the rover's
# internet-less WiFi later. Safe to run again: the second time it just pulls the latest code.
#
# First time (nothing cloned yet), in PowerShell:
#   powershell -ExecutionPolicy ByPass -c "irm https://raw.githubusercontent.com/jeffskinnerbox/physical_computing_for_beginners/main/full_build/setup-test-laptop.ps1 | iex"
# After that:
#   powershell -ExecutionPolicy ByPass -File $HOME\physical_computing_for_beginners\full_build\setup-test-laptop.ps1
#
# Clone somewhere else: set $env:ROVER_REPO_DIR first.

$ErrorActionPreference = "Stop"

$RepoUrl = "https://github.com/jeffskinnerbox/physical_computing_for_beginners.git"
$Dest = if ($env:ROVER_REPO_DIR) { $env:ROVER_REPO_DIR } else { Join-Path $HOME "physical_computing_for_beginners" }
$LaptopScripts = @("deploy.py", "test/system_test.py", "src/laptop/wireframe.py")

function Step($Message) { Write-Host "`n==> $Message" -ForegroundColor Cyan }

# Windows PowerShell 5.1 doesn't stop on a failed native command (git, uv), so check each one.
function Assert-Ok($What) { if ($LASTEXITCODE -ne 0) { throw "$What failed (exit code $LASTEXITCODE)" } }

# Installers change PATH for new windows only; reload it into this one.
function Update-Path {
    $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
                [Environment]::GetEnvironmentVariable("Path", "User")
}

Step "Checking for git"
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements
    Assert-Ok "Installing git"
    Update-Path
}
git --version

Step "Checking for uv"
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    Assert-Ok "Installing uv"
    Update-Path
    $env:Path = "$HOME\.local\bin;$env:Path"
} else {
    uv self update 2>$null | Out-Null  # needs uv 0.6+ for `uv sync --script`; skip if uv came from winget/pip
}
uv --version

Step "Getting the code into $Dest"
if (Test-Path (Join-Path $Dest ".git")) {
    git -C $Dest pull --ff-only
    if ($LASTEXITCODE -ne 0) { throw "Pull failed -- probably a file you edited here. See it with: git -C `"$Dest`" status" }
} else {
    git clone $RepoUrl $Dest
    Assert-Ok "git clone"
}
git -C $Dest log --oneline -1

Step "Pre-installing the laptop scripts' Python packages"
Set-Location (Join-Path $Dest "full_build")
foreach ($Script in $LaptopScripts) {
    Write-Host "  $Script"
    uv sync --quiet --script $Script
    Assert-Ok "uv sync --script $Script"
}

Write-Host @"

Done. Next, with the rover on its stand and the Pico plugged in by USB:
  cd "$Dest\full_build"
  uv run deploy.py rover          # first time needs internet: circup downloads the Pico libraries
  uv run deploy.py test           # device test runs on the Pico; watch it in the serial console
  uv run deploy.py restore        # put the rover code.py back
  uv run test/system_test.py      # whole-rover test over USB serial
  uv run src/laptop/wireframe.py  # 3D view -- join the rover's WiFi first
"@
