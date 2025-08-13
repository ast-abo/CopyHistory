from Gui import *
from tkinter import filedialog
import shutil
import os
import threading
import json
import sys
from Config import FileMemoryLimit

FileData = []
FavoriteCount = 0
SavedData = None
FileMemoryUsage = 0

with open('Storage.json', "r") as File:
    SavedData = json.load(File)

def Handler(Files):
    global FileData, FavoriteCount, FileMemoryUsage, SavedData
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
        FileList.insert(FavoriteCount, FileData[FavoriteCount][0])
        SavedData[2].insert(FavoriteCount, FileData[FavoriteCount])
        with open("Storage.json", "w") as file:
            json.dump(SavedData, file)

        while FileMemoryUsage > FileMemoryLimit and FileList.index("end") > 0:
            FileMemoryUsage -= sys.getsizeof(TextList.get(TextList.size() - 1)) / (1024**2)
            FileList.delete(END)
            FileData.pop()
            with open('Storage.json', "w") as File:
                json.dump(SavedData, File)

        if FileMemoryUsage <= FileMemoryLimit * 0.8:
            break


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
    global FavoriteCount, SavedData

    ListIndex = FileList.curselection()[0]
    Data = FileData[ListIndex]
    IsFavorite = Data[1]

    if IsFavorite:
        Data[1] = False
        FavoriteCount -= 1

        del FileData[ListIndex]
        del SavedData[2][ListIndex]
        FileList.delete(ListIndex)
        with open("Storage.json", "w") as file:
            json.dump(SavedData, file)

        FileList.insert(FavoriteCount, Data[0])
        FileData.insert(FavoriteCount, Data)
        SavedData[2].insert(FavoriteCount, Data)
        with open("Storage.json", "w") as file:
            json.dump(SavedData, file)
    else:
        if FavoriteCount == 5:
            return
        FavoriteCount += 1
        Data[1] = True

        del FileData[ListIndex]
        FileList.delete(ListIndex)
        del SavedData[2][ListIndex]
        with open("Storage.json", "w") as file:
            json.dump(SavedData, file)

        FileList.insert(0, "*" + Data[0])
        FileData.insert(0, Data)
        SavedData[2].insert(0, Data)
        with open("Storage.json", "w") as file:
            json.dump(SavedData, file)

def OpenDirectory():
    Path = filedialog.askdirectory(
        initialdir="/",
        title="Select a directory"
    )
    if Path:
        PasteTo.configure(text=Path)

def LoadData():
    global FavoriteCount, FileMemoryLimit
    ItemCount = 0
    for Item in reversed(SavedData[2]):
        if not os.path.isfile(Item[0]):
            del SavedData[2][ItemCount]
            with open("Storage.json", "w") as file:
                json.dump(SavedData, file)
            continue
        ItemCount += 1
        if Item[1]:
            FavoriteCount += 1
            FileData.insert(0, Item)
            FileList.insert(0, "*" + Item[0])
        else:
            FileData.insert(FavoriteCount, Item)
            FileList.insert(FavoriteCount, Item[0])
        
LoadData()
        
OpenFileManager.configure(command=OpenDirectory)
FileList.bind("<Double-Button-1>", DoubleClickCopy)
FileList.bind("<f>", SelectFavorite)