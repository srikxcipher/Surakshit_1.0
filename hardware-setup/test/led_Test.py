from machine import Pin
button=Pin(16,Pin.IN,Pin.PULL_UP)
led=Pin(15,Pin.OUT)
import time

while True:
    a=button.value()
#    print(a)
    if(a==0):
        led.value(1)
    else:
        led.value(0)

    #time.sleep(0)
