import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os"],
    "includes": [
    "random",
    "string",
    "tkinter",
    "csv",
    "threading",
    "datetime",
    "re",
    "faker"],
    "include_files": []
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="RandEmailAliasGenerator",
    version="0.3.1.0",
    description="R.E.A.G. ʕ º ᴥ ºʔ -BearBones ",
    options={"build_exe": build_exe_options},
    executables=[Executable("REAG.py", base=base)]
)
