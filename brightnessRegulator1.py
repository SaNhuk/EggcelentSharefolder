import RPi.GPIO as GPIO
from gpiozero import PWMLED
import numpy as np
import time

#---Variablen und Konstanten für Lichtmessung
messPin = 2
inPINS = [messPin]
smoothingWindowLength=4

#---Variablen und Konstanten für Lichtresponse
    #Uout = baseline - regelungsfaktor*Uin
baseline = 1
regelungsfaktor = 1
led = PWMLED("GPIO17")

#---Setup
GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)
GPIO.setup(messPin,GPIO.IN)

#---PWM-Berechnungen
def getTimex():
    return time.time()
GPIO.setmode(GPIO.BCM)
GPIO.setup(inPINS, GPIO.IN)
upTimes = [[0] for i in range(len(inPINS))]
downTimes = [[0] for i in range(len(inPINS))]
deltaTimes = [[0] for i in range(len(inPINS))]

def my_callback1(channel):
  i = inPINS.index(channel)
  v = GPIO.input(inPINS[i])
  #GPIO.output(outPINS[0], v) # mirror input state to output state directly (forward servo value only) - don't set PWM then for this pin
  if (v==0):
    downTimes[i].append(getTimex())
    if len(downTimes[i])>smoothingWindowLength: del downTimes[i][0]
  else:
    upTimes[i].append(getTimex())
    if len(upTimes[i])>smoothingWindowLength: del upTimes[i][0]
  deltaTimes[i].append( (downTimes[i][-1]-upTimes[i][-2])/(upTimes[i][-1]-downTimes[i][-1]) )
  if len(deltaTimes[i])>smoothingWindowLength: del deltaTimes[i][0]

GPIO.add_event_detect(inPINS[0], GPIO.BOTH, callback=my_callback1)
#GPIO.add_event_detect(inPINS[1], GPIO.BOTH, callback=my_callback1)


def readPWM(pin):
    try:
        ovl = deltaTimes[0][-smoothingWindowLength:] # output first pin PWM
        ov = sorted(ovl)[len(ovl) // 2] #ov = np.mean(ovl)
        #print(ov)
        time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()
    return ov

#---benötigten Output berechnen
def brightnessResponse(eingang):
    return baseline-regelungsfaktor*eingang

#---Loop
def regulateLight():
    lichtlevel = readPWM(messPin)
    benoetigterResponse = brightnessResponse(lichtlevel)
    led.value = benoetigterResponse
    print("pwm-input: "+str(lichtlevel)+", Response: "+str(benoetigterResponse))

while True:
    regulateLight()
    


