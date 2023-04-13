# -*- mode: python ; coding: utf-8 -*-
"""Usage:
pyinstaller ./main.spec
This will create a binary in dist/
"""

import os

block_cipher = None


a = Analysis(  # type: ignore
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

for subdir, dirs, files in os.walk("jeu/assets"):
    for file in files:
        path = os.path.abspath(f"{subdir}/{file}")
        print(f"{subdir}/{file}", path)
        a.datas += [(f"{subdir}/{file}", path, "DATA")]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)  # type: ignore

exe = EXE(  # type: ignore
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="Pipopipette",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
