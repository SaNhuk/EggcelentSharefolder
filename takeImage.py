from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (3280,2464)
camera.sharpness = 100
#camera.framerate = 1
#camera.shutter_speed = 120000
camera.iso = 20
print(camera.shutter_speed)
#camera.start_preview()
sleep(2)
camera.capture('testBilder/test88888.jpg')