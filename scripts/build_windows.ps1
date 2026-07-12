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
Remove-Item build, 'dist\CleanText Studio' -Recurse -Force -ErrorAction SilentlyContinue
& $Python -m PyInstaller --clean -y cleantext-studio.spec
if ($LASTEXITCODE -ne 0) { throw 'PyInstaller build failed.' }
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
Compress-Archive "$Stage\*" $Zip
$Iscc = Get-Command iscc -ErrorAction SilentlyContinue
if (-not $Iscc) {
  $LocalIscc = Join-Path $env:LOCALAPPDATA 'Programs\Inno Setup 6\ISCC.exe'
  if (Test-Path $LocalIscc) { $Iscc = $LocalIscc }
}
if ($Iscc) {
  & $Iscc "/DAppVersion=$Version" installer.iss
  if ($LASTEXITCODE -ne 0) { throw 'Inno Setup build failed.' }
}
Get-ChildItem dist\release -File | Where-Object Name -ne 'SHA256SUMS.txt' | ForEach-Object { "{0}  {1}" -f (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower(), $_.Name } | Set-Content dist\release\SHA256SUMS.txt
Copy-Item CHANGELOG.md dist\release\release-notes.md -Force
