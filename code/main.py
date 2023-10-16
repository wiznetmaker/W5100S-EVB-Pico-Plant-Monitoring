from usocket import socket
from machine import Pin,SPI, ADC
import network
import time
import statistics
import urequests

API = "YOUR TOKEN HERE"
ID = "YOUR CHAT ID HERE"
sensor = ADC(Pin(26))

#W5x00 chip init
def w5x00_init():
    spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
    nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin
    nic.active(True)
    
    #None DHCP
    nic.ifconfig(('192.168.11.40','255.255.255.0','192.168.11.1','8.8.8.8'))
    
    #DHCP
    #nic.ifconfig('dhcp')
    
    print('IP address :', nic.ifconfig())
    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())
        
def main():
    w5x00_init()
    
    readings = []
    try:
       while True:
           for i in range(5):
               reading = sensor.read_u16()
               readings.append(reading)
               print(readings) 
               time.sleep(1)
           median_value = statistics.median(readings)
           if median_value < 40000:
               urequests.get("https://api.telegram.org/bot"+API+"/sendMessage?text=Lady Bloomington is thirsty&chat_id="+ID)
               print("Message Sent")
           else:
               print("Lady Bloomington has enough water")
           time.sleep(3600)
    except OSError:
       print("Something went wrong")
    
if __name__ == "__main__":
    main()
