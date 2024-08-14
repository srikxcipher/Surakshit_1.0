import machine
import time

# UART pins on Raspberry Pi Pico
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))

# Function to send AT command and wait for response
def send_command(cmd, timeout=1000):
    uart.write(cmd + b'\r\n')
    start_time = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_time) < timeout:
        response = uart.readline()
        if response:
            return response.decode().strip()
    return None

# Initialize GSM module
send_command(b'AT')
send_command(b'AT+CMGF=0')  # Set SMS mode to PDU mode

# Function to send flash message
def send_flash_message(number, message):
    pdu = '000100'
    # Convert message to PDU format
    for c in message:
        pdu += '{:02X}'.format(ord(c))
    pdu_len = len(pdu) // 2 - 1
    # Length in octets
    pdu_len_octets = '{:02X}'.format(pdu_len)
    # Recipient number in semi-octet format
    recipient = ''
    for i in range(0, len(number), 2):
        recipient += number[i+1] + number[i]
    # Length of recipient number
    recipient_len = '{:02X}'.format(len(number))
    
    pdu_command = 'AT+CMGS={}{}\r{}'.format(recipient_len, recipient, pdu)
    send_command(pdu_command.encode(), timeout=3000)
    time.sleep(1)  # Wait before sending message
    uart.write(bytes.fromhex('1A'))  # Send Ctrl+Z to indicate the end of message

# Example usage
recipient_number = "Recipient's Number"  # Replace with recipient's phone number
message = "Your flash message here"
send_flash_message(recipient_number, message)
