import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os"],
    "includes": [
    "random",
    "string",
    "tkinter",
    "pyperclip",
    "threading",
    "datetime",
    "io",
    "re",
    "pystray",
    "urllib.request",
    "PIL.ImageTk",
    "PIL.Image"
    ],
    "include_files": ["C:\\Users\\Jake\\REAG-BG.jpg"]
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="RandEmailAlias",
    version="0.2.4",
    description="R.E.A.G. ʕ º ᴥ ºʔ -BearBones ",
    options={"build_exe": build_exe_options},
    executables=[Executable("REAG-Win-tray.py", base=base)]
)
