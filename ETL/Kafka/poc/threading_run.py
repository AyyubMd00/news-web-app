import threading
from time import sleep
def fire_and_forget_task():
    print('starts...')
    sleep(10)
    print('ends...')

thread = threading.Thread(target=fire_and_forget_task)
thread.start()