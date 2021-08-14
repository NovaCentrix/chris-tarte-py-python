import utime

class Timestamp:
  MONTHS = [ 
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' ]
  DAYS = [
    'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun' 
    ]
  def __init__(self, t=None, ms=0):
    if t is None: self.now()
    else: self.set(t,ms)

  def now(self):
    t = utime.time() # now
    ms = utime.ticks_ms() % 1000 # ms: milliseconds
    self.set(t, ms)

  def set(self, t, ms=0):
    self.t = t
    self.ms = ms
    self.tm = utime.localtime(self.t) # tm: time structure

  def __str__(self):
    return '  '.join([ self.time_only(), self.date_only() ])
  def __repr__(self):
    return self.__str__()
  def __sub__(a,b):
    return (a.t + a.ms/1000.0) - (b.t + b.ms/1000.0)
  def __add__(a,b):
    return (a.t + a.ms/1000.0) + (b.t + b.ms/1000.0)
  def __eq__(a,b):
    return (1000 * a.t + a.ms) == (1000 * b.t + b.ms)

  def time_only(self):
    return '{:02d}:{:02d}:{:02d}.{:03d}'.format(\
              self.tm[3], self.tm[4],self.tm[5], self.ms)
  def date_only(self):
    return '{:02d}-{}-{:4d}'.format(\
              self.tm[2], self.MONTHS[self.tm[1]-1], self.tm[0] )

def testme():

  t0 = Timestamp()
  dt = 30
  t1 = Timestamp( t0.t+30 )

  print('t0:', t0)
  print('t1:', t1)
  print('dt:', dt)

  dtck = t1 - t0
  print('dtck:', dtck)

