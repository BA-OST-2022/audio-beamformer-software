
# ls /dev/i2c*
# /dev/i2c-0  /dev/i2c-1  /dev/i2c-10  /dev/i2c-20  /dev/i2c-21  /dev/i2c-22


import sys
import smbus

def _list_devices(_bus):
  sys.stdout.write ('   ')
  for _address in range(16):
    sys.stdout.write (' %2x' % _address) # Print header
  
  for _address in range(128):
    if not _address % 16:
      sys.stdout.write ('\n%02x:' % _address) # Print address
    if 2 < _address < 120 : # Skip reserved addresses
      try:
        _bus.read_byte(_address)
        sys.stdout.write (' %02x' % _address) # Device address
      except:
        sys.stdout.write (' --') # No device detected
    else:
      sys.stdout.write ('   ') # Reserved

  sys.stdout.write ('\n')

try:
  _list_devices(smbus.SMBus(20))
except KeyboardInterrupt:
  sys.stdout.write('\n')
except Exception as _error:
  sys.stderr.write('%s\n' % str(_error))
  sys.exit(1)
finally:
  sys.exit(0)