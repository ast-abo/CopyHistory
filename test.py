from tkinter import *
from tkinter import ttk
import copykitten
import clipboard_monitor
import threading
from prettytable import PrettyTable
from PIL import Image
from PIL import ImageGrab

LastClip = None
PauseMonitor = False
# ClipTable = PrettyTable["Text", Button]
root = Tk()
root.title("Copy Paste Utilities")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True)

texts_list = Text(tabs)
texts_list.pack(fill="both", expand=True)

images_lists = Text(tabs)
images_lists.pack(expand=True, fill='both', padx=10, pady=10)

tabs.add(texts_list, text="Texts")
tabs.add(images_lists, text="Images")

def double_click_copy(event):
    idx = TextList.curselection()
    global PauseMonitor
    if idx:
        PauseMonitor = True
        selected = TextList.get(idx[0])
        root.clipboard_clear()
        root.clipboard_append(selected)
        root.after(1000, disable_pause)

def disable_pause():
    global PauseMonitor
    PauseMonitor = False

def handle_text(text):
    global LastClip
    global PauseMonitor
    if PauseMonitor:
        return
    
    if text != LastClip:
        print("Got Clip", text)
        LastClip = text
        TextList.insert(0, text)
def handle_image():
    print("image detected")
    image = ImageGrab.grabclipboard()
    if image:
        image.save("clipboard.png")
        ImageList.insert(0, "<Image from clipboard>")

# fixes issue with image not being detected for some reason
def onUpd():
    pass

clipboard_monitor.on_text(handle_text)
clipboard_monitor.on_image(handle_image)
clipboard_monitor.on_update(onUpd)
monitor_thread = threading.Thread(target=clipboard_monitor.wait, daemon=True)
monitor_thread.start()

TextList.bind("<Double-Button-1>", double_click_copy)
root.mainloop()