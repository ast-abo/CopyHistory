from Gui import *
from Config import TextMemoryLimit
import gc
import sys
import pyperclip
import time
import threading
from pynput import keyboard, mouse
from datetime import datetime
import platform
CurrentKeys = set()
KeyboardController = keyboard.Controller()
MouseController = mouse.Controller()

LastClip = None
LastDisabled = 0
TextMemoryUsage = 0
CtrlKey = None
DisableTime = 0

if platform.system() == 'Darwin':
    CtrlKey = keyboard.Key.cmd_l
else:
    CtrlKey = keyboard.Key.ctrl_l

def Handler(text):
    global LastClip, TextMemoryUsage, DisableTime

    if DisableTime > 0:
        return
    
    if text != LastClip:
        LastClip = text
        TextList.insert(0, text)
        TextMemoryUsage += sys.getsizeof(text) / (1024**2)
        
    while TextMemoryUsage > TextMemoryLimit and TextList.index("end") > 0:
        TextMemoryUsage -= sys.getsizeof(TextList.get(TextList.size() - 1)) / (1024**2)
        TextList.delete(END)
        gc.collect()

        if TextMemoryUsage <= TextMemoryLimit * 0.8:
            break

def DoubleClickCopy(event):
    idx = TextList.curselection()
    global PauseMonitor, DisableTime

    if DisableTime > 0:
        return

    if idx:
        PauseMonitor = True
        selected = TextList.get(idx[0])
        root.clipboard_clear()
        root.clipboard_append(selected)
        DisableTime = 1
        # root.after(1000, disable_pause)

def SelectFavorite(Event):
    # print("Selected Favorite")
    pass

def Copy(Event):
    global DisableTime
    DisableTime = 1
    print("copy")
    pass

def ReleaseModifers():
    KeyboardController.release(keyboard.Key.ctrl)
    KeyboardController.release(keyboard.Key.alt)
    KeyboardController.release(keyboard.Key.shift)

    time.sleep(0.1)
    pass


KeyboardController = keyboard.Controller()
def PasteLast():
    ReleaseModifers()
    pyperclip.copy(TextList.get(1))

    try:
        KeyboardController.press(keyboard.Key.ctrl)
        KeyboardController.press('v')

        KeyboardController.release(keyboard.Key.ctrl)
        KeyboardController.release('v')
    except IndexError:
        print("rip")
    pass

def CopyLast():
    global DisableTime

    DisableTime = 1
    ReleaseModifers()
    pyperclip.copy(TextList.get(1))
    print("Copied Last")

    pass

def PasteLastFive():
    for i in range(5):
        print("Paste")
        pass
    pass

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