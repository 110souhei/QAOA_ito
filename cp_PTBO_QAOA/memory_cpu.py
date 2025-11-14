import psutil
import threading
import time

def monitor_cpu(initial_time,event):
    print("START monitor_cpu")
    while not event.wait(0.1):
        mem = psutil.virtual_memory() 
        print("memory: ", mem.percent)
    print("END monitor_cpu")

event = threading.Event()
initial_time = time.time()
m = threading.Thread(target=monitor_cpu,args=((initial_time,event)))
m.start()# 開始
tmp = 0

# 監視したい処理
a = 0
for i in range(100):
    a += i

event.set() # 終了