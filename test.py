from tkinter import *
from tkinter import ttk
import copykitten
import clipboard_monitor
import threading
from prettytable import PrettyTable
from PIL import Image, ImageGrab, ImageTk
import memory
import os
import psutil
import time

LastClip = None
PauseMonitor = False
Selection = None
ImageData = []
# ClipTable = PrettyTable["Text", Button]
root = Tk()
root.title("Copy Paste Utilities")
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True)

TextsFrame = ttk.Frame(tabs, padding="3 3 12 12")
TextList = Listbox(TextsFrame, height=6, width=25)
TextList.pack(expand=True, fill='both', padx=10, pady=10)

ImagesFrame = ttk.Frame(tabs, padding="3 3 12 12")
ImageList = Listbox(ImagesFrame, height=6, width=25)
ImageList.pack(side="left", expand=True, fill='both', padx=10, pady=10)

ImageDisplay = Label(ImagesFrame)
ImageDisplay.pack(side="right", expand=True, fill='both', padx=10, pady=10)

tabs.add(TextsFrame, text="Texts")
tabs.add(ImagesFrame, text="Images")

def double_click_copy(event):
    idx = TextList.curselection()
    global PauseMonitor

    if idx:
        PauseMonitor = True
        selected = TextList.get(idx[0])
        root.clipboard_clear()
        root.clipboard_append(selected)
        root.after(2000, disable_pause)

def disable_pause():
    global PauseMonitor
    PauseMonitor = False

def text_handler(text):
    global LastClip
    global PauseMonitor
    if PauseMonitor:
        return
    
    if text != LastClip:
        LastClip = text
        TextList.insert(0, text)

def image_handler():
    global PauseMonitor

    if PauseMonitor:
        return

    CopiedImage = ImageGrab.grabclipboard()
    ImageList.insert(0, Image)
    ImageData.append(CopiedImage)

def upd():
    pass

def on_select(event):
    global Selection
    Selection = ImageList.curselection()
    img = ImageData[Selection[0]]
    img_tk = ImageTk.PhotoImage(img)
    ImageDisplay.config(image=img_tk)
    ImageDisplay.image = img_tk

clipboard_monitor.on_text(text_handler)
clipboard_monitor.on_image(image_handler)
clipboard_monitor.on_update(upd)
monitor_thread = threading.Thread(target=clipboard_monitor.wait, daemon=True)

monitor_thread.start()
TextList.bind("<Double-Button-1>", double_click_copy)
ImageList.bind("<<ListboxSelect>>", on_select)

while True:
    pid = os.getpid()  # Get the PID of the current Python script
    process = psutil.Process(pid)
    mem_info = process.memory_info()
    print(f"Process RSS (Resident Set Size): {round(mem_info.rss / (1024**2), 2)} MB")
    print(f"Process VMS (Virtual Memory Size): {round(mem_info.vms / (1024**2), 2)} MB")
    pass


root.mainloop()