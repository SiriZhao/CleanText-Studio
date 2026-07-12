from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('emoji') + collect_data_files('keyring') + [('assets/icon.png', 'assets'), ('src/cleantext_studio/llm/prompts/*.txt', 'cleantext_studio/llm/prompts'), ('src/cleantext_studio/resources/*.json', 'cleantext_studio/resources')]
a = Analysis(['src/cleantext_studio/main.py'], pathex=['src'], binaries=[], datas=datas, hiddenimports=['PySide6.QtSvg', 'keyring.backends.Windows', 'openai', 'anthropic', 'certifi'], hookspath=[], runtime_hooks=[], excludes=[], noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name='CleanText Studio', icon='assets/icon.ico', debug=False, bootloader_ignore_signals=False, strip=False, upx=False, console=False)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name='CleanText Studio')
