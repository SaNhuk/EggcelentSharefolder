from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (3280,2464)
#camera.start_preview()
for i in range(1,20):
    # Camera warm-up time
    sleep(10)
    print("cheese")
    sleep(0.1)
    camera.capture('testBilder/test'+str(i)+'.jpg')
print("done")