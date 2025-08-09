from tkinter import *
from tkinter import ttk
import copykitten
import clipboard_monitor
import threading
from prettytable import PrettyTable
from PIL import Image

LastClip = None
PauseMonitor = False
# ClipTable = PrettyTable["Text", Button]
root = Tk()
root.title("Copy Paste Utilities")
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True)

TextsFrame = ttk.Frame(tabs, padding="3 3 12 12")
TextsFrame.grid(column=1, row=1, sticky=(N, W, E, S))
TextList = Listbox(TextsFrame, height=6, width=25)
TextList.pack(expand=True, fill='both', padx=10, pady=10)

ImagesFrame = ttk.Frame(tabs, padding="3 3 12 12")
ImagesFrame.grid(column=1, row=1, sticky=(N, W, E, S))

tabs.add(TextsFrame, text="Texts")
tabs.add(ImagesFrame, text="Images")
ImageList = Listbox(ImagesFrame, height=6, width=25)
ImageList.pack(expand=True, fill='both', padx=10, pady=10)

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

def handler(text):
    global LastClip
    global PauseMonitor
    if PauseMonitor:
        return
    
    if text != LastClip:
        print("Got Clip", text)
        LastClip = text
        TextList.insert(0, text)

clipboard_monitor.on_text(handler)
clipboard_monitor.on_image(handler)
monitor_thread = threading.Thread(target=clipboard_monitor.wait, daemon=True)

monitor_thread.start()
TextList.bind("<Double-Button-1>", double_click_copy)
root.mainloop()






# while True:
#     wait(1)
