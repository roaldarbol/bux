from multiprocessing import freeze_support
from bux_recorder.main_window import BuxRecorder

if __name__ == "__main__":
    freeze_support()
    app = BuxRecorder()
    app.run()
