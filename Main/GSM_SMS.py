from machine import Pin
import time

# Import UART library
from machine import UART
led=Pin(15,Pin.OUT)
# Define UART pins
TX_PIN = 4  # Replace with the actual TX pin number connected to GSM module
RX_PIN = 5  # Replace with the actual RX pin number connected to GSM module

# Define the phone number to send the SMS to
PHONE_NUMBER = "+919999999999"  # Replace this with the recipient's phone number

# Define GPIO pin connected to the button
BUTTON_PIN = 16  # Example pin number, replace with the actual pin number you're using

# Initialize UART
uart = UART(1, baudrate=9600, tx=machine.Pin(TX_PIN), rx=machine.Pin(RX_PIN))

# Function to send AT command and wait for response
def send_at_command(command, timeout=1000):
    uart.write(command + '\r\n')
    time.sleep(0.1)  # Wait for command to be sent
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
    # Enter text mode
    send_at_command("AT+CMGF=1")
    
    # Set the phone number
    send_at_command('AT+CMGS="{}"'.format(PHONE_NUMBER))
    
    # Send the message
    send_at_command(message + chr(26), timeout=15000)  # ASCII code for Ctrl+Z
    
    print("SMS sent successfully.")

# Initialize GPIO pin for button
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# Main loop
while True:
    # Check if the button is pressed
    if button.value() == 0:
        led.value(1)
        send_sms("-------YOUR MESSAGE-------.")
        time.sleep(1)  # Add a debounce delay
    else:
        led.value(0)
