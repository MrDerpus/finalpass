# finalpass.spec
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('TOME.py',  '.'),
        ('file_handling.py', '.'),
        ('settings.py', '.')
    ],
    hiddenimports=['pyperclip'],
    hookspath=[],
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False
)
pyz = PYZ(a.pure, a.zipped_data)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='finalpass',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True
)