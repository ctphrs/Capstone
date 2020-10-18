from picamera import PiCamera
import time

class DogCapture:

    '''
    self.camera = None
    self.vtype = None
    self.itype = None
    self.default_capture_location = None
    self.default_record_duration = None
    '''

    def __init__(self): #in the future load these from a config file
        self.camera = PiCamera() #initialize camera object
        self.camera.resolution = (768, 768) #set resolution
        self.camera.framerate = 24 #set framerate
        self.vtype = '.h264' #video type
        self.itype = '.png' #image type
        self.default_capture_location = '/mnt/exdr'
        self.default_record_duration = 5 #seconds

    def time_naming(self):
        now = time.localtime()
        nowstr = ''+str(now.tm_year)+str(now.tm_mon)+\
                str(now.tm_mday)+'-'+str(now.tm_hour)+\
                str(now.tm_min)+str(now.tm_sec)
        return nowstr


    def preview_func(self):
        self.camera.start_preview()
        time.sleep(5)
        self.camera.stop_preview()
    
    def still_func(self, capture_location = None):
        if capture_location is None:
            capture_location = self.default_capture_location
        nowstr = self.time_naming()
        print('Capturing at:', nowstr)
        self.camera.capture(capture_location + '/' + nowstr + self.itype)
        print('Done!')

    def record_func(self, capture_location = None, record_duration = None):
        if record_duration is None:
            record_duration = self.default_record_duration
        if capture_location is None:
            capture_location = self.default_capture_location
        nowstr = self.time_naming()
        print('Recording at:', nowstr)
        self.camera.start_recording(capture_location + '/' + nowstr + self.vtype)
        time.sleep(record_duration)
        self.camera.stop_recording()
        print('Done!')
    

if __name__ == '__main__':
    cap = DogCapture()
    #cap.init()
    cap.record_func()
    cap.record_func()
    cap.still_func()
