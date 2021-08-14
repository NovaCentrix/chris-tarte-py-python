import sys
import utime
import oled

def get_the_time():
  months = [ 
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' ]
  days = [
    'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun' 
    ]
  t = utime.localtime()
  ms = utime.ticks_ms() % 1000
  strtime = '{:02d}:{:02d}:{:02d}.{:03d}'.format(\
               t[3], t[4],t[5], ms)
  strdate = '{:02d}-{}-{:4d}'.format(\
             t[2], months[t[1]-1], t[0] )
  return strtime, strdate


oled = oled.OLED()
oled.display_splash_screen()
utime.sleep_ms(200)

while(True):
 #utime.sleep_ms(1000)
 hms, mdy = get_the_time()
 oled.display_time(hms, mdy)


