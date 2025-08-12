from Gui import *
from tkinter import filedialog
import shutil
import os
import threading

FileData = []
FavoriteCount = 0

def Handler(Files):
    global FileData, FavoriteCount
    LastFile = None
    for File in Files:
        try:
            LastFile = FileData[FavoriteCount][0]
        except:
            pass
    
        if File == LastFile:
            continue

        FileData.insert(FavoriteCount, [
            File,
            False
        ])
        FileList.insert(FavoriteCount, FileData[0][0])


def DoubleClickCopy(event):
    Index = FileList.curselection()
    if Index:
        SelectedData = FileData[Index[0]]
        
        Source = SelectedData[0]
        Destination = PasteTo.cget("text")
        if not os.path.isfile(Source):
            return
        if not os.path.isdir(Destination):
            return
        threading.Thread(target=shutil.copy, args=(Source, Destination)).start()

def SelectFavorite(Event):
    global FavoriteCount

    ListIndex = FileList.curselection()[0]
    Data = FileData[ListIndex]
    IsFavorite = Data[1]
    Data[1] = not IsFavorite

    if IsFavorite:
        print("Unfavorited")
        FavoriteCount -= 1
        del FileData[ListIndex]
        FileList.delete(ListIndex)
        FileList.insert(FavoriteCount, Data[0])
        FileData.insert(FavoriteCount, Data)
    else:
        print("Favorited")
        del FileData[ListIndex]
        FileList.delete(ListIndex)
        FileList.insert(0, "*" + Data[0])
        FileData.insert(0, Data)
        FavoriteCount += 1
        pass

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
FileList.bind("<f>", SelectFavorite)