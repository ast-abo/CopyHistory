from tkinter import *
from tkinter import ttk
import clipboard_monitor
import threading
from PIL import Image, ImageGrab, ImageTk
import memory
import queue

LastClip = None
PauseMonitor = False
Selection = None
ImageData = []
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
    ImageList.insert(0, CopiedImage)
    ImageData.insert(0, CopiedImage)

def upd():
    pass

def on_select(event):
    global Selection
    Selection = ImageList.curselection()
    SelectedImage = ImageData[Selection[0]]
    
    width, height = SelectedImage.size # Get original dimensions
    if width > 600 or height > 700:
        # Calculate the ratio needed to resize to max_width
        ratio = min(600 / width, 700 / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        SelectedImage = SelectedImage.resize((new_width, new_height), Image.LANCZOS)
        
    TkinterImage = ImageTk.PhotoImage(SelectedImage)
    ImageDisplay.config(image=TkinterImage)
    ImageDisplay.image = TkinterImage

clipboard_monitor.on_text(text_handler)
clipboard_monitor.on_image(image_handler)
clipboard_monitor.on_update(upd)
ClipBoardMonitor = threading.Thread(target=clipboard_monitor.wait, daemon=True)
MemoryMonitor = threading.Thread(target=memory.GetMemoryUse, daemon=True)

MemoryMonitor.start()
ClipBoardMonitor.start()
TextList.bind("<Double-Button-1>", double_click_copy)
ImageList.bind("<<ListboxSelect>>", on_select)
root.mainloop()