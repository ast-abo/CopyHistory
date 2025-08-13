from Gui import *
from PIL import Image, ImageGrab, ImageTk
import numpy as np
import cv2
from Config import ImageMemoryLimit
import hashlib
from datetime import datetime
import json
import base64

ImageData = []
LastImageClip = None
ImageMemoryUsage = 0
FavoriteCount = 0
SavedData = None
with open('Storage.json', "r") as File:
    SavedData = json.load(File)

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
    global LastImageClip, ImageMemoryUsage, FavoriteCount, SavedData

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

    ImageData.insert(FavoriteCount, [
        base64.b64encode(CompressedImage).decode("utf-8"),
        MegaBytes,
        False,
        f"Image taken at: {datetime.now()}"
    ])
    SavedData[1].insert(FavoriteCount, ImageData[FavoriteCount])
    with open('Storage.json', "w") as File:
        json.dump(SavedData, File)

    ImageList.insert(FavoriteCount, ImageData[FavoriteCount][3])
    ImageList.selection_clear(0, END)
    ImageList.select_set(0)
    ImageList.see(0)
    ImageMemoryUsage += len(CompressedImage) / (1024**2) + MegaBytes
    while (ImageMemoryUsage > ImageMemoryLimit and len(ImageData) > 0):
        Data = ImageData.pop()
        SavedData[1].pop()
        ImageList.delete(END)
        with open('Storage.json', "w") as File:
            json.dump(SavedData, File)
        ImageMemoryUsage -= len(Data[0]) / (1024**2) + Data[1]
        
        if ImageMemoryUsage <= ImageMemoryLimit * 0.8:
            break

def OnSelect(event):
    global Selection, ImageMemoryUsage
    Selection = ImageList.curselection()
    
    try:
        value = ImageData[Selection[0]]
    except IndexError:
        if not Selection:
            return

    DecodedImage = base64.b64decode(ImageData[Selection[0]][0])
    DecompressedImage = Decompress(DecodedImage)
    RgbImage = cv2.cvtColor(DecompressedImage, cv2.COLOR_BGR2RGB)
    PilImage = Image.fromarray(RgbImage)
    TkinterImage = ImageTk.PhotoImage(PilImage)
    ImageDisplay.config(image=TkinterImage)
    ImageDisplay.image = TkinterImage

def SelectFavorite(Event):
    global FavoriteCount, SavedData

    ListIndex = ImageList.curselection()[0]
    DataValue = ImageData[ListIndex]
    IsFavorite = DataValue[2]

    if IsFavorite:
        DataValue[2] = False
        FavoriteCount -= 1

        del ImageData[ListIndex]
        del SavedData[1][ListIndex]
        ImageList.delete(ListIndex)

        ImageList.insert(FavoriteCount, DataValue[3])
        ImageData.insert(FavoriteCount, DataValue)
        SavedData[1].insert(FavoriteCount, DataValue)

        with open('Storage.json', "w") as File:
            json.dump(SavedData, File)
    else:
        if FavoriteCount == 5:
            return
        FavoriteCount += 1
        DataValue[2] = True

        del ImageData[ListIndex]
        del SavedData[1][ListIndex]
        ImageList.delete(ListIndex)

        ImageList.insert(0, "*" + DataValue[3])
        ImageData.insert(0, DataValue)
        SavedData[1].insert(0, DataValue)
        with open('Storage.json', "w") as File:
            json.dump(SavedData, File)
        
    
def LoadData():
    global FavoriteCount, ImageMemoryUsage, SavedData

    for Item in reversed(SavedData[1]):
        if Item[2]:
            FavoriteCount += 1
            ImageData.insert(0, Item)
            ImageList.insert(0, "*" + Item[3])
        else:
            ImageData.insert(FavoriteCount, Item)
            ImageList.insert(FavoriteCount, Item[3])

    # ImageMemoryUsage
        
LoadData()

ImageList.bind("<<ListboxSelect>>", OnSelect)
ImageList.bind("<f>", SelectFavorite)