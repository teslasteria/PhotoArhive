from cx_Freeze import setup, Executable

setup(
    name="PhotoArchive",
    version="1.0",
    description="My Python App",
    executables=[
        Executable(
            "main.py",      
            #base="Win32GUI", 
            icon="resources/icon.ico")]
)