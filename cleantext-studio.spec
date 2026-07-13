from PyInstaller.utils.hooks import collect_data_files
from pathlib import Path
import runpy

version = runpy.run_path('src/cleantext_studio/version.py')['__version__']
version_tuple = tuple(int(part) for part in version.split('.')) + (0,)
version_file = Path('build/version_info.txt')
version_file.parent.mkdir(parents=True, exist_ok=True)
version_file.write_text(f'''VSVersionInfo(
  ffi=FixedFileInfo(filevers={version_tuple}, prodvers={version_tuple}, mask=0x3f,
    flags=0x0, OS=0x40004, fileType=0x1, subtype=0x0, date=(0, 0)),
  kids=[StringFileInfo([StringTable('080404b0', [
    StringStruct('CompanyName', 'SiriZhao'),
    StringStruct('FileDescription', 'CleanText Studio'),
    StringStruct('FileVersion', '{version}'),
    StringStruct('InternalName', 'CleanText Studio'),
    StringStruct('LegalCopyright', 'Copyright (c) 2026 SiriZhao'),
    StringStruct('OriginalFilename', 'CleanText Studio.exe'),
    StringStruct('ProductName', 'CleanText Studio'),
    StringStruct('ProductVersion', '{version}')])]),
    VarFileInfo([VarStruct('Translation', [2052, 1200])])]
)''', encoding='utf-8')

datas = collect_data_files('emoji') + collect_data_files('keyring') + [('assets/icon.png', 'assets'), ('assets/icons/*.svg', 'assets/icons'), ('src/cleantext_studio/llm/prompts/*.txt', 'cleantext_studio/llm/prompts')]
a = Analysis(['src/cleantext_studio/main.py'], pathex=['src'], binaries=[], datas=datas, hiddenimports=['PySide6.QtSvg', 'keyring.backends.Windows', 'openai', 'anthropic', 'certifi'], hookspath=[], runtime_hooks=[], excludes=[], noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name='CleanText Studio', icon='assets/icon.ico', version=str(version_file), debug=False, bootloader_ignore_signals=False, strip=False, upx=False, console=False)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name='CleanText Studio')
