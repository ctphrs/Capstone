#https://picamera.readthedocs.io/en/release-1.13/recipes1.html
from picamera import PiCamera
from time import sleep

path = '/home/pi/Desktop/'
delay = 30
record_time = 5 #this number * delay seconds is the amounnt of time it will take images for
camera = PiCamera()

for i in range(record_time):
    sleep(delay)
    camera.capture(path+'image%s.jpg' % i)