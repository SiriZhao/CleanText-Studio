from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('emoji') + [('assets/icon.png', 'assets')]
a = Analysis(['src/cleantext_studio/main.py'], pathex=['src'], binaries=[], datas=datas, hiddenimports=['PySide6.QtSvg'], hookspath=[], runtime_hooks=[], excludes=[], noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name='CleanText Studio', icon='assets/icon.ico', debug=False, bootloader_ignore_signals=False, strip=False, upx=False, console=False)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name='CleanText Studio')
