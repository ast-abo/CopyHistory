import tracemalloc

tracemalloc.start()

import ImageHistory
import TextHistory
import FileHistory
from Gui import *
import clipboard_monitor
import threading
from Gui import *
from Config import *

Selection = None

def upd():
    pass

def on_select(event):
    global Selection
    Selection = ImageList.curselection()

    try:
        value = ImageHistory.ImageData[Selection[0]]
    except IndexError:
        if not Selection:
            return
        print(f"Index {Selection[0]} is out of range.")
    
    ImageDisplay.config(image=ImageHistory.ImageData[Selection[0]])
    ImageDisplay.image = ImageHistory.ImageData[Selection[0]]

clipboard_monitor.on_text(TextHistory.text_handler)
clipboard_monitor.on_image(ImageHistory.image_handler)
clipboard_monitor.on_files(FileHistory.Handler)
clipboard_monitor.on_update(upd)
ClipBoardMonitor = threading.Thread(target=clipboard_monitor.wait, daemon=True)
ClipBoardMonitor.start()
ImageList.bind("<<ListboxSelect>>", on_select)

root.mainloop()

