# Proof of concept: Tiny 2040 + 0.49 in OLED + Shift Register

import sys
import select
from machine import I2C, SoftI2C, Pin,
from pyb import UART
import ssd1306
import utime

def display_splash_screen(disp):
  """Welcome screen."""
  disp.text("Welcome to", 2,1)
  disp.text("to the very late", 2,11)
  disp.text("TartePy", 2,21)
  disp.show()

i2c = SoftI2C(scl=Pin.cpu.B8, sda=Pin.cpu.B9)
i2z = I2C('Y', freq=500000)
disp = ssd1306.SSD1306_I2C(128, 32, i2c)

display_splash_screen(disp)

ser = UART(3,
           timeout = 1,
           baudrate = 115200,
           # stopbits = serial.STOPBITS_ONE,
           # bytesize = serial.EIGHTBITS,
           # writeTimeout = 0,
           # rtscts = False,
           # dsrdtr = False 
           )
if ser is None:
  print('error opening serial port')
  exit(0)

ser.write("Hello\n")
  
looping = True
while looping:
  buff = ser.read(1024)
  if buff is None: continue
  if( len(buff) ):
    ser.write(buff)


