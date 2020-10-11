#https://picamera.readthedocs.io/en/release-1.13/recipes1.html
from picamera import PiCamera
from time import sleep

path = '/home/pi/Desktop/video.h264'
camera = PiCamera()

camera.start_recording(path)
sleep(5)
camera.stop_recording()