from picamera import PiCamera
import time

camera = PiCamera()
camera.resolution = (768, 768)
camera.framerate = 24

default_capture_location = '/mnt/exdr'
default_record_duration = 5 #secondso

vtype = '.h264'
itype = '.png'

def time_naming():
    now = time.localtime()
    nowstr = ''+str(now.tm_year)+str(now.tm_mon)+str(now.tm_mday)+'-'+str(now.tm_hour)+str(now.tm_min)+str(now.tm_sec)
    return nowstr


def preview_func():
    camera.start_preview()
    time.sleep(5)
    camera.stop_preview()

def still_func(capture_location = None):
    if capture_location is None:
        capture_location = default_capture_location
    nowstr = time_naming()
    print('Capturing at:', nowstr)
    camera.capture(capture_location + '/' + nowstr + itype)
    print('Done!')

def record_func(capture_location = None, record_duration = None):
    if record_duration is None:
        record_duration = default_record_duration
    if capture_location is None:
        capture_location = default_capture_location
    nowstr = time_naming()
    print('Recording at:', nowstr)
    camera.start_recording(capture_location + '/' + nowstr + vtype)
    time.sleep(record_duration)
    camera.stop_recording()
    print('Done!')
    

if __name__ == '__main__':
    record_func()
