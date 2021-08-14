# Proof of concept: Tiny 2040 + 0.49 in OLED + Shift Register

import sys
import select
#from machine import I2C, SoftI2C
from machine import Pin
from pyb import UART
import ssd1306
import utime
import upacket as pkt

import pyb
bid = pyb.unique_id()
sid = bid.decode('ascii')
pyboard = sid.endswith('PSNN18 ')
tartepy = not pyboard

def display_splash_screen(disp):
  """Welcome screen."""
  disp.text("Welcome to", 2,1)
  disp.text("to the very late", 2,11)
  disp.text("TartePy", 2,21)
  disp.show()

def basic_loopback(ser):
  while True:
    nbytes = ser.any()
    if nbytes:
      buff = ser.read(16)
      ser.write(buff)


if tartepy:
#   i2c = SoftI2C(scl=Pin.cpu.B8, sda=Pin.cpu.B9)
#   i2z = I2C('Y', freq=500000)
#   disp = ssd1306.SSD1306_I2C(128, 32, i2c)
# 
#   display_splash_screen(disp)
  pass

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

# print("Basic loopback")
# basic_loopback(ser)
# sys.exit()


ser.write("Hello\n")
  
looping = True
pr=pkt.Packet('', 'pksend')
pe=pkt.Packet('', 'pkecho')
pa=pkt.Packet('', 'acknak')
while looping:
  buff = ser.read(1024)
  if buff is None: continue
  if( len(buff) ):
    #print(len(buff), end=' ')
    sbuff = buff.decode('latin-1')
    stats = pr.parse(sbuff)
    #print('Received Packet:')
    #print(pr.packet)
    #print(stats)
    
    ebuff = pkt.Packet.serialize(pr.packet)
    #print('Serialized:', ebuff)
    pe.generate(ebuff, 'pkecho')
    #print('Echoed Packet:')
    #print(pe.packet)
    #print('AckNak Packet:')
    #print(pa.packet)
    pa.generate( stats.serialize(), 'acknak' )
    # Prepare the reply
    # two packets separated by RS
    reply = pe.packet + pe.RSEP + pa.packet
    ser.write(reply.encode('latin-1'))

    if not stats:
      print('Received Packet:')
      print(pr.packet)
      print(stats)
      print('Echoed Packet:')
      print(pe.packet)
      print('AckNak Packet:')
      print(pa.packet)
      looping=False


