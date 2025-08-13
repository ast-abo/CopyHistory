from Gui import *
from Config import TextMemoryLimit
import gc
import sys
import pyperclip
import time
import threading
from pynput import keyboard, mouse
import platform
import json
CurrentKeys = set()
KeyboardController = keyboard.Controller()
MouseController = mouse.Controller()

TextMemoryUsage = 0
CtrlKey = None
DisableTime = 0
FavoriteCount = 0
SavedData = None
with open('Storage.json', "r") as File:
    SavedData = json.load(File)

TextData = []

if platform.system() == 'Darwin':
    CtrlKey = keyboard.Key.cmd_l
else:
    CtrlKey = keyboard.Key.ctrl_l

def Handler(Text):
    global TextMemoryUsage, DisableTime, FavoriteCount
    LastClip = None

    if DisableTime > 0:
        return

    try:
        LastClip = TextData[FavoriteCount][0]
    except:
        pass
    
    if Text == LastClip:
        return
    
    TextData.insert(FavoriteCount, [
        Text,
        False
    ])
    SavedData[0].insert(FavoriteCount, TextData[FavoriteCount])
    with open("Storage.json", "w") as File:
        json.dump(SavedData, File)
    TextList.insert(FavoriteCount, Text)

    TextMemoryUsage += sys.getsizeof(Text) / (1024**2)
        
    while TextMemoryUsage > TextMemoryLimit and TextList.index("end") > 0:
        TextMemoryUsage -= sys.getsizeof(TextList.get(TextList.size() - 1)) / (1024**2)
        TextList.delete(END)
        TextData.pop()
        gc.collect()

        if TextMemoryUsage <= TextMemoryLimit * 0.8:
            break

def DoubleClickCopy(event):
    global DisableTime
    Index = TextList.curselection()

    if DisableTime > 0:
        return

    if Index:
        selected = TextList.get(Index[0])
        root.clipboard_clear()
        root.clipboard_append(selected)
        DisableTime = 1
        # root.after(1000, disable_pause)

def SelectFavorite(Event):
    global FavoriteCount

    try:
        ListIndex = TextList.curselection()[0]
    except:
        return
    Data = TextData[ListIndex]
    IsFavorite = Data[1]

    if IsFavorite:
        Data[1] = False
        FavoriteCount -= 1
        del TextData[ListIndex]
        del SavedData[0][ListIndex]
        TextList.delete(ListIndex)

        TextList.insert(FavoriteCount, Data[0])
        TextData.insert(FavoriteCount, Data)
        SavedData[0].insert(FavoriteCount, Data)
        with open("Storage.json", "w") as file:
            json.dump(SavedData, file)
        
    else:
        if FavoriteCount == 5:
            return
        Data[1] = True
        del TextData[ListIndex]
        del SavedData[0][ListIndex]
        TextList.delete(ListIndex)

        TextList.insert(0, "*" + Data[0])
        TextData.insert(0, Data)
        SavedData[0].insert(0, Data)
        with open("Storage.json", "w") as file:
            json.dump(SavedData, file)

        FavoriteCount += 1

def Copy(Event):
    global DisableTime
    DisableTime = 1
    pass


def Paste():
        KeyboardController.release(keyboard.Key.ctrl)
        KeyboardController.release(keyboard.Key.alt)
        KeyboardController.release(keyboard.Key.shift)

        time.sleep(0.1)

        KeyboardController.press(keyboard.Key.ctrl)
        KeyboardController.press('v')

        KeyboardController.release(keyboard.Key.ctrl)
        KeyboardController.release('v')

def PasteLast():
    global DisableTime

    DisableTime = 1

    pyperclip.copy(TextList.get(1))
    Paste()
    pyperclip.copy(TextList.get(0))

def CopyLast():
    global DisableTime
    DisableTime = 1

    pyperclip.copy(TextList.get(1))

    pass

def PasteLastFive():
    global DisableTime
    DisableTime = 1

    for i in range(5):
        Text = TextList.get(i)
        if Text == "":
            break
        pyperclip.copy(Text)
        KeyboardController.press(keyboard.Key.space)
        KeyboardController.release(keyboard.Key.space)

    pyperclip.copy(TextList.get(0))

def OnPress(Key):
    CurrentKeys.add(Key)
    alt = keyboard.Key.cmd_l in CurrentKeys or keyboard.Key.cmd_r in CurrentKeys or keyboard.Key.alt_l in CurrentKeys or keyboard.Key.alt_r in CurrentKeys
    ctrl = keyboard.Key.ctrl_l in CurrentKeys or keyboard.Key.ctrl_r in CurrentKeys or keyboard.Key.cmd_l in CurrentKeys or keyboard.Key.cmd_r in CurrentKeys
    v = hasattr(Key, 'vk') and Key.vk == 86 or hasattr(Key, 'char') and Key.char == 'v'
    c = hasattr(Key, 'vk') and Key.vk == 67 or hasattr(Key, 'char') and Key.char == 'c'
    Five = hasattr(Key, 'vk') and Key.vk == 53 or hasattr(Key, 'vk') and Key.vk == 23 or hasattr(Key, 'char') and Key.char == '5'

    try:
        if v and alt and ctrl:
            PasteLast()
        elif c and alt and ctrl:
            CopyLast()
        elif Five and alt and ctrl:
            PasteLastFive()

    except AttributeError:
        pass

def OnRelease(Key):
    CurrentKeys.discard(Key)

def DecreaseDisableTime():
    global DisableTime
    while True:
        if DisableTime > 0:
            time.sleep(0.1)
            DisableTime -= 0.1

def LoadData():
    global FavoriteCount, TextMemoryUsage

    for Item in reversed(SavedData[0]):
        if Item[1]:
            FavoriteCount += 1
            TextData.insert(0, Item)
            TextList.insert(0, "*" + Item[0])
        else:
            TextData.insert(FavoriteCount, Item)
            TextList.insert(FavoriteCount, Item[0])

    TextMemoryUsage += sys.getsizeof(Text) / (1024**2)
        
        
LoadData()

Listener = keyboard.Listener(on_press=OnPress, on_release=OnRelease)
DisableThread = threading.Thread(target=DecreaseDisableTime, daemon=True)

TextList.bind("<Double-Button-1>", DoubleClickCopy)
TextList.bind("<f>", SelectFavorite)
if platform.system() == "darwin":
    TextList.bind("<Command-c>", Copy)
else:
    TextList.bind("<Control-c>", Copy)

DisableThread.start()
Listener.start()