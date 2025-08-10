import psutil
import os
import time
import queue

MemorySize = None

def GetMemoryUse():
    global MemorySize
    while True:
        pid = os.getpid()  # Get the PID of the current Python script
        Process = psutil.Process(pid)
        MemoryInfo = Process.memory_info()
        MemorySize = round(MemoryInfo.vms / (1024**2), 2)
        # print(f"Process RSS (Resident Set Size): {round(mem_info.rss / (1024**2), 2)} MB")
        print(f"Process VMS (Virtual Memory Size): {MemorySize} MB")
        time.sleep(1)
        pass

