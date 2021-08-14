import usys
import utime
import oled
import pyb
import rotary
import pwm

def adjust( val, delta, lo, hi, wrap=False ):
  val += delta
  if wrap:
    if val > hi: val = lo
    if val < lo: val = hi
  else:
    if val > hi: val = hi
    if val < lo: val = lo
  return val

oled = oled.OLED()
oled.display_splash_screen()
utime.sleep_ms(2000)

out = pwm.PWM()
knob = rotary.Rotary()

DIAL_NONE = 0
DIAL_FREQ = 1
DIAL_DUTY = 2
DIAL_SIZE = 3

freq_mhz = 2.000
duty_pct = 50.0
freq_adj = 0.1
freq_max = 40.000
freq_min = 0.500
duty_adj = 5.0
duty_max = 100.0
duty_min = 0.0
dial = DIAL_FREQ
out.set_freq(freq_mhz * 1.0e6)
out.set_duty(duty_pct)
print(out)

MODE_SELECT=0
MODE_CHANGE=1
MODE_CHAR=[ '<', '*' ]

looping = True
mode = MODE_SELECT
while(looping):
  utime.sleep_ms(100)
  sfreq = '{:2.3f} MHz'.format(freq_mhz)
  sduty = '{:5.0f} %'.format(duty_pct)
  oled.display_pwm(sfreq, sduty, dial, MODE_CHAR[mode] )
  while len( knob.change ):
    change, val, sw = knob.change.pop(0)
    if change == knob.ROT_CW:
      if mode == MODE_SELECT:
        dial = adjust( dial, +1, DIAL_NONE, DIAL_SIZE-1, wrap=True )
      elif mode == MODE_CHANGE:
        if   dial == DIAL_FREQ: freq_mhz = adjust( freq_mhz, +freq_adj, freq_min, freq_max )
        elif dial == DIAL_DUTY: duty_pct = adjust( duty_pct, +duty_adj, duty_min, duty_max )
    elif change == knob.ROT_CCW:
      if mode == MODE_SELECT:
        dial = adjust( dial, -1, DIAL_NONE, DIAL_SIZE-1, wrap=True )
      elif mode == MODE_CHANGE:
        if   dial == DIAL_FREQ: freq_mhz = adjust( freq_mhz, -freq_adj, freq_min, freq_max )
        elif dial == DIAL_DUTY: duty_pct = adjust( duty_pct, -duty_adj, duty_min, duty_max )
    elif change == knob.SW_PRESS:
      if   dial == DIAL_NONE: 
        looping = False
      elif dial == DIAL_FREQ: 
        if mode == MODE_SELECT:
          mode = MODE_CHANGE
        elif mode == MODE_CHANGE:
          out.set_freq(freq_mhz * 1.0e6)
          out.set_duty(duty_pct)
          mode = MODE_SELECT
      elif dial == DIAL_DUTY: 
        if mode == MODE_SELECT:
          mode = MODE_CHANGE
        elif mode == MODE_CHANGE:
          out.set_duty(duty_pct)
          mode = MODE_SELECT
    elif change == knob.SW_RELEASE:
      print(out)
print('The End.')
usys.exit()

