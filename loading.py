import threading, time

class PrintThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(PrintThread, self).__init__(target=self.print, *args, **kwargs)
        self._stop_event = threading.Event()

    def print(self):
        print("")
        interval = 0.2
        frames = [".  ",".. ","..."," ..","  .","   "]
        while True:
            for frame in frames:
                print("\033[F"+frame)
                time.sleep(interval)
            if self.stopped(): return

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

class loader:
    def __init__(self):
        self.print_thread = None

    def start(self):
        self.print_thread = PrintThread(daemon=True)
        self.print_thread.start()

    def stop(self):
        self.print_thread.stop()
        self.print_thread.join()
        print("\033[F",end="\r")
                