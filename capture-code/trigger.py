import capture
import time
import math
import shutil

class Trigger:

    def __init__(self):
        self.period = 60 #seconds
        self.duration = 15 #seconds
        self.maximum_captures = 1000 #captures before self-termination
        self.record_dir = '/home/pi/record'
        self.final_dir = '/mnt/share'

    def timed_trigger_video(self):
        cap = capture.DogCapture()
        for i in range (self.maximum_captures):
            vid = cap.record_func(record_duration = self.duration, capture_location=self.record_dir)
            print("Moving file...")
            shutil.move(vid,self.final_dir)
            print("Moved file!")
            time.sleep(abs(self.period - self.duration))




if __name__ == '__main__':
    t = Trigger()
    t.timed_trigger_video()
