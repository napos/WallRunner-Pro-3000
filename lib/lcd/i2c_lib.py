#!/usr/bin/env python

#
# I haven't been able to find the author of this driver. The same code is
# available all over the place and the forum thread I found it from said that
# it is basically the Arduino driver converted to Python by an Amazon reviewer(?).
# I got it from http://www.raspberrypi.org/phpBB3/viewtopic.php?f=32&t=34261&p=378524
#
# ATTN:
# I replaced everything concerning "from time import *" to use "import time" instead,
# since it's not really advisable to use the former import method. Also added a "unit test".
#
# - Siim Orasmae <siim dot orasmae at gmail dot com>
#

import smbus
import time

class i2c_device:
   def __init__(self, addr, port=1):
      self.addr = addr
      self.bus = smbus.SMBus(port)

# Write a single command
   def write_cmd(self, cmd):
      self.bus.write_byte(self.addr, cmd)
      time.sleep(0.0001)

# Write a command and argument
   def write_cmd_arg(self, cmd, data):
      self.bus.write_byte_data(self.addr, cmd, data)
      time.sleep(0.0001)

# Write a block of data
   def write_block_data(self, cmd, data):
      self.bus.write_block_data(self.addr, cmd, data)
      time.sleep(0.0001)

# Read a single byte
   def read(self):
      return self.bus.read_byte(self.addr)

# Read
   def read_data(self, cmd):
      return self.bus.read_byte_data(self.addr, cmd)

# Read a block of data
   def read_block_data(self, cmd):
      return self.bus.read_block_data(self.addr, cmd)
