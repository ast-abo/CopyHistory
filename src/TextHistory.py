from Gui import *
from Config import TextMemoryLimit
import gc
import sys

LastClip = None
TextMemoryUsage = 0

def Handler(text):
    global LastClip, TextMemoryUsage
    
    if text != LastClip:
        LastClip = text
        TextList.insert(0, text)
        TextMemoryUsage += sys.getsizeof(text) / (1024**2)
        
    while (TextMemoryUsage > TextMemoryLimit and TextList.index("end") > 0):
        TextMemoryUsage -= sys.getsizeof(TextList.get(TextList.size() - 1)) / (1024**2)
        TextList.delete(END)
        gc.collect()

        if TextMemoryUsage <= TextMemoryLimit * 0.8:
            break

def DoubleClickCopy(event):
    idx = TextList.curselection()
    global PauseMonitor
    if idx:
        PauseMonitor = True
        selected = TextList.get(idx[0])
        root.clipboard_clear()
        root.clipboard_append(selected)
        # root.after(1000, disable_pause)

def SelectFavorite():
    print("Selected Favorite")

TextList.bind("<Double-Button-1>", DoubleClickCopy)
TextList.bind("<f>", SelectFavorite)