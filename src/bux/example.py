import time

def add_one(window):
    global running
    
    try:
        print('Experiment running!')
        last = time.time()
        while running:
            window.update() # Always process new events
            time.sleep(0.1)
            now = time.time()
            print(now)
    finally:
        pass

def task():
    time.sleep(0.1)
    now = time.time()
    print(now)


