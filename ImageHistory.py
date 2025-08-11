from Gui import *
import gc
from PIL import Image, ImageGrab, ImageTk
import numpy as np
import cv2
from Config import ImageMemoryLimit
import hashlib

ImageData = []
LastImageClip = None
ImageMemoryUsage = 0

def Compress(Image):
    Array = np.array(Image, dtype=np.uint8)
    Success, Buffer = cv2.imencode(".jpg", cv2.cvtColor(Array, cv2.COLOR_RGB2BGR))
    return Buffer.tobytes()

def Decompress(ImageBytes):
    Array = np.frombuffer(ImageBytes, dtype=np.uint8)
    DecompresssedImage = cv2.imdecode(Array, cv2.IMREAD_COLOR)
    return DecompresssedImage
def ImageHash(Image):
    return hashlib.md5(Image.tobytes()).hexdigest()

def Handler():
    global LastImageClip, ImageMemoryUsage

    CopiedImage = ImageGrab.grabclipboard()
    if not isinstance(CopiedImage, Image.Image):
        return
    
    if CopiedImage.mode != "RGB":
        CopiedImage = CopiedImage.convert("RGB")
    
    CopiedImage.thumbnail((400, 400), Image.LANCZOS)
    CurrentHash = ImageHash(CopiedImage)
    if LastImageClip == CurrentHash:
        return
    LastImageClip = CurrentHash

    TkinterImage = ImageTk.PhotoImage(CopiedImage)
    ImageDisplay.config(image=TkinterImage)
    ImageDisplay.image = TkinterImage
    
    Bytes = CopiedImage.height * CopiedImage.width * 3
    MegaBytes = Bytes / (1024**2)

    CompressedImage = Compress(CopiedImage)

    ImageList.insert(0, "Image")
    ImageData.insert(0, [
        CompressedImage,
        MegaBytes
    ])

    ImageMemoryUsage += len(CompressedImage) / (1024**2) + MegaBytes
    while (ImageMemoryUsage > ImageMemoryLimit and len(ImageData) > 0):
        Data = ImageData.pop()
        ImageMemoryUsage -= len(Data[0]) / (1024**2) + Data[1]
        ImageList.delete(END)
        gc.collect()
        
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

def OnSelect(event):
    global Selection, ImageMemoryUsage
    Selection = ImageList.curselection()

    try:
        value = ImageData[Selection[0]]
    except IndexError:
        if not Selection:
            return
        print(f"Index {Selection[0]} is out of range.")

    DecompressedImage = Decompress(ImageData[Selection[0]][0])
    RgbImage = cv2.cvtColor(DecompressedImage, cv2.COLOR_BGR2RGB)
    PilImage = Image.fromarray(RgbImage)
    TkinterImage = ImageTk.PhotoImage(PilImage)
    ImageDisplay.config(image=TkinterImage)
    ImageDisplay.image = TkinterImage


ImageList.bind("<<ListboxSelect>>", OnSelect)
TextList.bind("<Double-Button-1>", double_click_copy)