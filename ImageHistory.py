from Gui import *
from Memory import MemoryUsage
import gc
from PIL import Image, ImageGrab, ImageTk
from Config import ImageMemoryLimit

ImageData = []
LastImageClip = None
ImageMemoryUsage = 0
After = 0
Before = 0

def image_handler():
    global LastImageClip, ImageMemoryUsage, Before, After

    Before = MemoryUsage()

    CopiedImage = ImageGrab.grabclipboard()
    if LastImageClip == CopiedImage:
        return
    
    LastImageClip = CopiedImage
    print(ImageMemoryUsage)
    Width, Height = CopiedImage.size
    if Width > 600 or Height > 700:
        Ratio = min(600 / Width, 700 / Height)
        NewWidth = int(Width * Ratio)
        New_Height = int(Height * Ratio)
        CopiedImage = CopiedImage.resize((NewWidth, New_Height), Image.LANCZOS)
        
    TkinterImage = ImageTk.PhotoImage(CopiedImage)
    ImageDisplay.config(image=TkinterImage)
    ImageDisplay.image = TkinterImage
    
    ImageList.insert(0, CopiedImage)
    ImageData.insert(0, TkinterImage)

    After = MemoryUsage()
    print(MemoryUsage())
    ImageMemoryUsage += After - Before
    while (ImageMemoryUsage > ImageMemoryLimit and len(ImageData) > 0):
        Before = MemoryUsage()
        ImageData.pop()
        ImageList.delete(END)
        gc.collect()
        After = MemoryUsage()
        ImageMemoryUsage -= Before - After

        if ImageMemoryUsage <= ImageMemoryLimit * 0.8:
            break

def double_click_copy(event):
    idx = TextList.curselection()
    #global PauseMonitor

    if idx:
        #PauseMonitor = True
        selected = TextList.get(idx[0])
        root.clipboard_clear()
        root.clipboard_append(selected)
        #root.after(2000, disable_pause)


TextList.bind("<Double-Button-1>", double_click_copy)