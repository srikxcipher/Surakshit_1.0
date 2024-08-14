import serial
import time
import RPi.GPIO as GPIO

# Configure serial port
ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

# Configure GPIO pins for buttons and define SMS messages
BUTTONS = {
    17: "Button 1 pressed! This is SMS 1.",
    18: "Button 2 pressed! This is SMS 2.",
    27: "Button 3 pressed! This is SMS 3."
}

# Function to send AT command and wait for response
def send_at_command(command, timeout=1):
    ser.write(command.encode() + b'\r\n')
    time.sleep(timeout)
    response = ser.read_all().decode('utf-8')
    return response.strip()

# Function to send SMS
def send_sms(phone_number, message):
    try:
        # Set SMS text mode
        send_at_command('AT+CMGF=1')
        
        # Specify recipient phone number
        send_at_command('AT+CMGS="{}"'.format(phone_number))
        
        # Enter SMS message content
        send_at_command(message)
        
        # Send Ctrl+Z to indicate end of message
        ser.write(b'\x1A')
        time.sleep(1)
        return True
    except Exception as e:
        print("Error sending SMS:", e)
        return False

# Callback function for button press event
def button_callback(channel):
    if channel in BUTTONS.keys():
        if send_sms("7077800397", BUTTONS[channel]):
            print("SMS sent successfully!")
        else:
            print("Failed to send SMS.")

try:
    # Setup GPIO mode and pins
    GPIO.setmode(GPIO.BCM)
    for pin in BUTTONS.keys():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(pin, GPIO.RISING, callback=button_callback(pin), bouncetime=300)
    
    print("Press buttons to send SMS...")

    # Keep script running
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting program...")
    GPIO.cleanup()
    ser.close()

except serial.SerialException as e:
    print("Serial port error:", e)

finally:
    # Ensure serial connection is closed
    ser.close()
