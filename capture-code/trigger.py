import capture
import time
import math

class Trigger:

    def __init__(self):
        self.period = 60 #seconds
        self.duration = 15 #seconds
        self.maximum_captures = 1000 #captures before self-termination

    def timed_trigger_video(self):
        cap = capture.DogCapture()
        for i in range (self.maximum_captures):
            cap.record_func(record_duration = self.duration)
            now = time.localtime()
            #print("INFO: Video recorded at", now)
            time.sleep(abs(self.period - self.duration))




if __name__ == '__main__':
    t = Trigger()
    t.timed_trigger_video()
