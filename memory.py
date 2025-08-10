import psutil
import os
import time

ram = psutil.virtual_memory()

import tracemalloc

tracemalloc.start()  # Start tracing memory allocations

# ... (Your code here, performing memory-intensive operations) ...

#tracemalloc.stop()  # Stop tracing

while True:
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {round(current_memory / (1024**2), 2)} MB")
    print(f"Peak memory usage: {round(peak_memory / (1024**2), 2)} MB")
    
    target_script_name = "test.py"  # Or part of its command line arguments
    pid = None
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if target_script_name in ' '.join(proc.info['cmdline']):
            print(f"PID of {target_script_name}: {proc.info['pid']}")
            pid = proc.info['pid']
        break

    process = psutil.Process(pid)
    mem_info = process.memory_info()
    print(f"Process RSS (Resident Set Size): {round(mem_info.rss / (1024**2), 2)} MB")
    print(f"Process VMS (Virtual Memory Size): {round(mem_info.vms / (1024**2), 2)} MB")
    time.sleep(4)
    pass