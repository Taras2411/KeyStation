from threading import Thread
from time import sleep

def func():
    for i in range(255):
        print(f"from child thread: {i}")
        sleep(0.5)
        
th = Thread(target=func, daemon=True)
th.start()
print("app stop...")
for i in range(5):
    #print(f"from main thread: {i}")
    sleep(1)
print("app stoped")
