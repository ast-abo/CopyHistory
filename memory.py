import psutil
import os

def MemoryUsage():
    pid = os.getpid()  # Get the PID of the current Python script
    Process = psutil.Process(pid)
    MemoryInfo = Process.memory_info()
    MemorySize = round(MemoryInfo.rss / (1024**2), 2)
    return MemorySize