from machine import I2C, SoftI2C, SPI, Pin, Signal
import ssd1306
import utime

class OLED:
  def __init__(self):
    self.i2c = SoftI2C(scl=Pin.cpu.B8, sda=Pin.cpu.B9)
    self.i2z = I2C('Y', freq=500000)
    self.disp = ssd1306.SSD1306_I2C(128, 32, self.i2c)
    # pixel offsets for the each of the text rows and data fields
    # from above, this display is 32 pixels tall x 64 pixels wide
    self.disp_rows = [2, 15]
    self.disp_tabs = [2, 64]

  def display_splash_screen(self):
    """Welcome screen."""
    self.disp.fill(0)
    self.disp.text("Welcome to", 2,1)
    self.disp.text("to the very late", 2,11)
    self.disp.text("TartePy", 2,21)
    self.disp.show()

  def display_time( self, hms, mdy):
    self.disp.fill(0)
    self.disp.text(hms, 2, 1)
    self.disp.text(mdy, 2, 11)
    self.disp.show()

