param([switch]$SkipChecks)
$ErrorActionPreference = 'Stop'
if (-not $SkipChecks) {
  if (-not (Test-Path .venv)) { py -3.12 -m venv .venv }
  & .\.venv\Scripts\python -m pip install -e ".[dev]"
  & .\.venv\Scripts\ruff check .
  & .\.venv\Scripts\mypy src
  $env:QT_QPA_PLATFORM='offscreen'; & .\.venv\Scripts\pytest
  $Python = '.\.venv\Scripts\python'
} else { $Python = 'python' }
$Version = & $Python -c "from cleantext_studio import __version__; print(__version__)"
Remove-Item build, 'dist\CleanText Studio' -Recurse -Force -ErrorAction SilentlyContinue
& $Python -m PyInstaller --clean -y cleantext-studio.spec
$Release = 'dist\release'
if (Test-Path $Release) { Remove-Item $Release -Recurse -Force }
New-Item $Release -ItemType Directory -Force | Out-Null
$Stage = "dist\portable"
Remove-Item $Stage -Recurse -Force -ErrorAction SilentlyContinue
New-Item $Stage -ItemType Directory | Out-Null
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
if ($Iscc) { & $Iscc "/DAppVersion=$Version" installer.iss }
Get-ChildItem dist\release -File | Where-Object Name -ne 'SHA256SUMS.txt' | ForEach-Object { "{0}  {1}" -f (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower(), $_.Name } | Set-Content dist\release\SHA256SUMS.txt
Copy-Item CHANGELOG.md dist\release\release-notes.md -Force
