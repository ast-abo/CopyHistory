from Gui import *
from Memory import MemoryUsage
from Config import TextMemoryLimit
import gc

LastClip = None
TextMemoryUsage = 0
After = 0
Before = 0

def text_handler(text):
    global LastClip, Before, After, TextMemoryUsage
    Before = MemoryUsage()
    
    if text != LastClip:
        LastClip = text
        TextList.insert(0, text)
        After = MemoryUsage()
        TextMemoryUsage += After - Before
    while (ImageMemoryUsage > TextMemoryLimit and TextList.index("end") > 0):
        Before = MemoryUsage()
        TextList.delete(END)
        gc.collect()
        After = MemoryUsage()
        ImageMemoryUsage -= Before - After

        if ImageMemoryUsage <= TextMemoryLimit * 0.8:
            break