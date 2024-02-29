from globals import global_state
import threading
import time


class Timer:
    def __init__(self, update_function):
        self.update_function = update_function
        self.running = False
        self.paused = False  
        self.elapsed_time = 0
        self.start_time = None
        self.pause_start_time = None  
        self.timer_thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.paused = False
            self.start_time = time.time() - self.elapsed_time
            self.timer_thread = threading.Thread(target=self.run)
            self.timer_thread.start()

    def run(self):
        while self.running:
            if not self.paused:
                current_time = time.time()
                self.elapsed_time = current_time - self.start_time
                self.update_function(self.format_elapsed_time(self.elapsed_time))
            time.sleep(0.1)

    def pause(self):
        if self.running and not self.paused:
            self.paused = True
            self.pause_start_time = time.time()

    def resume(self):
        if self.running and self.paused:
            self.paused = False
            # Adjust the start time based on the pause duration
            pause_duration = time.time() - self.pause_start_time
            self.start_time += pause_duration

    def format_elapsed_time(self, seconds):
        # Format elapsed seconds to include three decimal places
        return '{:.3f}'.format(seconds)

    def reset(self):
        self.elapsed_time = 0
        self.start_time = time.time()
        if self.paused:
            self.paused = False
            self.pause_start_time = None

    def stop(self):
        self.running = False
        self.paused = False  
        if self.timer_thread:
            self.timer_thread.join()
