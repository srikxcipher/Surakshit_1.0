from machine import Pin
import time

TX = 4  
RX = 5  

ph = "+91999999999"  
r=Pin(15,Pin.OUT)
y=Pin(13,Pin.OUT)
g=Pin(0,Pin.OUT)

br = 16  # Red
by = 21  # Yellow
bg = 27  # Green

Msg_1 = b"Serious Emergency! Call NOW!!!"
Msg_2 = b"Minor Emergency!Call ASAP!"
Msg_3 = b"Call Later!"

# Initialize UART
uart = machine.UART(1, baudrate=9600, tx=machine.Pin(TX), rx=machine.Pin(RX))

# Function to send AT command and wait for response
def send_at_command(command, timeout=1000):
    uart.write(command + b'\r\n')
    time.sleep(0.1)  
    response = b""
    start_time = time.ticks_ms()
    while (time.ticks_ms() - start_time) < timeout:
        if uart.any():
            response += uart.read(1)
            if b'OK' in response:
                return response
            elif b'ERROR' in response:
                return response
    return b"Timeout"

# Function to send SMS
def send_sms(message):
    send_at_command(b"AT+CMGF=1")
    send_at_command(b'AT+CMGS="{}"'.format(ph))
    send_at_command(message + chr(26).encode(), timeout=15000)  
    
    print("SMS sent successfully.")


btn1 = machine.Pin(br, machine.Pin.IN, machine.Pin.PULL_UP)
btn2 = machine.Pin(by, machine.Pin.IN, machine.Pin.PULL_UP)
btn3 = machine.Pin(bg, machine.Pin.IN, machine.Pin.PULL_UP)
                      
                      
btn1_pressed = False
btn2_pressed = False
btn3_pressed = False

# Interrupt handler for btn 1
def btn1_handler(pin):
    global btn1_pressed
    btn1_pressed = True

# Interrupt handler for btn 2
def btn2_handler(pin):
    global btn2_pressed
    btn2_pressed = True
    #y.value(1)

# Interrupt handler for btn 3
def btn3_handler(pin):
    global btn3_pressed
    btn3_pressed = True
    #g.value(1)

btn1.irq(trigger=machine.Pin.IRQ_FALLING, handler=btn1_handler)
btn2.irq(trigger=machine.Pin.IRQ_FALLING, handler=btn2_handler)
btn3.irq(trigger=machine.Pin.IRQ_FALLING, handler=btn3_handler)


while True:
    if btn1_pressed:
        r.value(1)
        send_sms(Msg_1)
        btn1_pressed = False  
        r.value(0)
    elif btn2_pressed:
        y.value(1)
        send_sms(Msg_2)
        btn2_pressed = False  
        y.value(0)
        
    elif btn3_pressed:
        g.value(1)
        send_sms(Msg_3)
        btn3_pressed = False  
        g.value(0)
    time.sleep(0.1)  
