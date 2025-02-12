from cx_Freeze import setup, Executable

setup(
    name="Priority Number System",
    version="1.0",
    description="Priority Number Display System",
    executables=[Executable("priority_number_app.py", base="Win32GUI")],
    options={
        "build_exe": {
            "packages": ["tkinter"],
            "include_files": []
        }
    }
)