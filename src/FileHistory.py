from Gui import *
from tkinter import filedialog
import shutil
FileData = []

def Handler(Files):
    for File in Files:
        FileData.insert(0, File)
        FileList.insert(0, File)
        pass

def DoubleClickCopy(event):
    Index = FileList.curselection()
    if Index:
        SelectedData = FileData[Index[0]]
        
        Source = SelectedData
        Destination = PasteTo.cget("text")
        shutil.copy(Source, Destination)
        # root.clipboard_clear()
        # root.clipboard_append(selected)
        # root.after(1000, disable_pause)

def OpenDirectory():
    Path = filedialog.askdirectory(
        initialdir="/",
        title="Select a directory"
    )
    if Path:
        print(f"Selected directory: {Path}")
        PasteTo.configure(text=Path)
        
OpenFileManager.configure(command=OpenDirectory)
FileList.bind("<Double-Button-1>", DoubleClickCopy)