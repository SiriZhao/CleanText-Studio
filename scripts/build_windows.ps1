param([switch]$SkipChecks)
$ErrorActionPreference = 'Stop'
$Python = '.\.venv\Scripts\python.exe'
if (-not (Test-Path $Python)) {
  if ($SkipChecks) {
    $Python = 'python'
  } else {
    py -3.12 -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Unable to create the Python 3.12 virtual environment.' }
  }
}
$PythonVersion = & $Python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
if ($LASTEXITCODE -ne 0 -or $PythonVersion -ne '3.12') { throw "Python 3.12 is required; found $PythonVersion." }
if (-not $SkipChecks) {
  & .\.venv\Scripts\python -m pip install -e ".[dev]"
  if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
  & .\.venv\Scripts\ruff check .
  if ($LASTEXITCODE -ne 0) { throw 'Ruff failed.' }
  & .\.venv\Scripts\mypy src
  if ($LASTEXITCODE -ne 0) { throw 'MyPy failed.' }
  $env:QT_QPA_PLATFORM='offscreen'; & .\.venv\Scripts\pytest
  if ($LASTEXITCODE -ne 0) { throw 'Pytest failed.' }
}
$Version = & $Python -c "from cleantext_studio import __version__; print(__version__)"
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($Version)) { throw 'Unable to read package version.' }
New-Item 'dist\logs' -ItemType Directory -Force | Out-Null
Remove-Item build, 'dist\CleanText Studio' -Recurse -Force -ErrorAction SilentlyContinue
$PyInstallerProcess = Start-Process $Python -ArgumentList @('-m', 'PyInstaller', '--clean', '-y', 'cleantext-studio.spec') -Wait -PassThru -NoNewWindow -RedirectStandardOutput 'dist\logs\pyinstaller.log' -RedirectStandardError 'dist\logs\pyinstaller-error.log'
if ($PyInstallerProcess.ExitCode -ne 0) { throw 'PyInstaller build failed; see dist/logs/pyinstaller-error.log.' }
$Executable = 'dist\CleanText Studio\CleanText Studio.exe'
if (-not (Test-Path $Executable)) { throw 'Packaged executable is missing.' }
$Process = Start-Process $Executable -PassThru
Start-Sleep -Seconds 5
if ($Process.HasExited) { throw 'Packaged application exited during smoke test.' }
Stop-Process -Id $Process.Id
Wait-Process -Id $Process.Id -ErrorAction SilentlyContinue
"Packaged application started and remained responsive for 5 seconds." | Set-Content 'dist\logs\smoke-test.log'
$Release = 'dist\release'
if (Test-Path $Release) { Remove-Item $Release -Recurse -Force }
New-Item $Release -ItemType Directory -Force | Out-Null
$Stage = "dist\portable"
Remove-Item $Stage -Recurse -Force -ErrorAction SilentlyContinue
New-Item $Stage -ItemType Directory -Force | Out-Null
Copy-Item 'dist\CleanText Studio' "$Stage\CleanText Studio" -Recurse
Copy-Item LICENSE, README.md "$Stage"
Copy-Item docs\USER_GUIDE.md "$Stage"
$Zip = "dist\release\CleanText-Studio-v$Version-Windows-x64-Portable.zip"
Remove-Item $Zip -Force -ErrorAction SilentlyContinue
Add-Type -AssemblyName System.IO.Compression.FileSystem
for ($Attempt = 1; $Attempt -le 3; $Attempt++) {
  try {
    if (Test-Path $Zip) { Remove-Item $Zip -Force }
    [System.IO.Compression.ZipFile]::CreateFromDirectory((Resolve-Path $Stage), (Resolve-Path '.').Path + '\\' + $Zip, [System.IO.Compression.CompressionLevel]::Optimal, $false)
    break
  } catch {
    if ($Attempt -eq 3) { throw "Portable ZIP creation failed: $($_.Exception.Message)" }
    Start-Sleep -Seconds 2
  }
}
if (-not (Test-Path $Zip) -or (Get-Item $Zip).Length -lt 1MB) { throw 'Portable ZIP is missing or incomplete.' }
"Created $Zip" | Set-Content 'dist\logs\portable-package.log'
$Iscc = Get-Command iscc -ErrorAction SilentlyContinue
if (-not $Iscc) {
  $LocalIscc = Join-Path $env:LOCALAPPDATA 'Programs\Inno Setup 6\ISCC.exe'
  if (Test-Path $LocalIscc) { $Iscc = $LocalIscc }
}
if ($Iscc) {
  $InnoProcess = Start-Process $Iscc -ArgumentList @("/DAppVersion=$Version", 'installer.iss') -Wait -PassThru -NoNewWindow -RedirectStandardOutput 'dist\logs\inno-setup.log' -RedirectStandardError 'dist\logs\inno-setup-error.log'
  if ($InnoProcess.ExitCode -ne 0) { throw 'Inno Setup build failed; see dist/logs/inno-setup-error.log.' }
}
Get-ChildItem dist\release -File | Where-Object Name -ne 'SHA256SUMS.txt' | ForEach-Object { "{0}  {1}" -f (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower(), $_.Name } | Set-Content dist\release\SHA256SUMS.txt
Get-Content dist\release\SHA256SUMS.txt | Set-Content 'dist\logs\checksum.log'
Copy-Item CHANGELOG.md dist\release\release-notes.md -Force
