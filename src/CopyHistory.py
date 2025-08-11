import tracemalloc

tracemalloc.start()

import ImageHistory
import FileHistory
import TextHistory
from Gui import *
import clipboard_monitor
import threading
from Gui import *

Selection = None

def upd():
    pass

clipboard_monitor.on_text(TextHistory.Handler)
clipboard_monitor.on_image(ImageHistory.Handler)
clipboard_monitor.on_files(FileHistory.Handler)
clipboard_monitor.on_update(upd)
ClipBoardMonitor = threading.Thread(target=clipboard_monitor.wait, daemon=True)
ClipBoardMonitor.start()

root.mainloop()