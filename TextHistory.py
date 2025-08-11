from Gui import *
from Config import TextMemoryLimit
import gc

LastClip = None
TextMemoryUsage = 0

def Handler(text):
    global LastClip, Before, After, TextMemoryUsage
    
    if text != LastClip:
        LastClip = text
        TextList.insert(0, text)
    while (TextMemoryUsage > TextMemoryLimit and TextList.index("end") > 0):
        TextList.delete(END)
        gc.collect()
        TextMemoryUsage -= abs(Before - After)

        if TextMemoryUsage <= TextMemoryLimit * 0.8:
            break
def double_click_copy(event):
    idx = TextList.curselection()
    global PauseMonitor
    if idx:
        PauseMonitor = True
        selected = TextList.get(idx[0])
        root.clipboard_clear()
        root.clipboard_append(selected)
        # root.after(1000, disable_pause)
        
TextList.bind("<Double-Button-1>", double_click_copy)