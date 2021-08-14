import utime as time
from pyb import Pin
import micropython

class Rotary:

  # defaults for my board
  PINQ1 = Pin.cpu.C6
  PINQ2 = Pin.cpu.C7
  PINSW = Pin.cpu.B3

  ROT_CW = 1
  ROT_CCW = 2
  SW_PRESS = 4
  SW_RELEASE = 8

  def __init__(self,q1=PINQ1,q2=PINQ2,sw=PINSW):
    self.val = 0
    self.sw = 0
    self.q1_pin = Pin(q1, Pin.IN)
    self.q2_pin = Pin(q2, Pin.IN)
    self.sw_pin = Pin(sw, Pin.IN)
    self.last_status = (self.q1_pin.value() << 1) | self.q2_pin.value()
    self.q1_pin.irq(handler=self.rotary_change, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING )
    self.q2_pin.irq(handler=self.rotary_change, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING )
    self.sw_pin.irq(handler=self.switch_detect, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING )
    self.handlers = []
    self.last_button_status = self.sw_pin.value()
    self.change = []

  def rotary_change(self, pin):
    new_status = (self.q1_pin.value() << 1) | self.q2_pin.value()
    if new_status == self.last_status: return
    transition = (self.last_status << 2) | new_status
    if transition == 0b1110:
      self.val += 1
      self.change.append( [ Rotary.ROT_CW, self.val, self.sw ] )
    elif transition == 0b1101:
      self.val -= 1
      self.change.append( [ Rotary.ROT_CCW, self.val, self.sw ] )
    self.last_status = new_status

  def switch_detect(self,pin):
    if self.last_button_status == self.sw_pin.value(): return
    self.last_button_status = self.sw_pin.value()
    if not self.sw_pin.value(): # active low
      self.sw = 1
      self.change.append( [ Rotary.SW_PRESS, self.val, self.sw ] )
    else:
      self.sw = 0
      self.change.append( [ Rotary.SW_RELEASE, self.val, self.sw ] )



def testme():
  knob = Rotary()
  while True:
    time.sleep(0.1)
    while len( knob.change ):
      change, val, sw = knob.change.pop(0)
      if change == Rotary.ROT_CW:
        print(val)
      elif change == Rotary.ROT_CCW:
        print(val)
      elif change == Rotary.SW_PRESS:
        print('PRESS')
      elif change == Rotary.SW_RELEASE:
        print('RELEASE')

