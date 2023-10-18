import RPi.GPIO as GPIO
import board
import adafruit_sht4x
import time
from noaa_sdk import NOAA

# Settings for thermostat
relaypin = 23 # Pin that relay is hooked up to
maxtemp = 71 # Temp to stop call for heat
mintemp = 69 # Temp to start call for heat
checktime = 1 # Number of seconds to wait before checking temperature
zipcode = '26505'
countrycode = 'US'

# Set GPIO Settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(relaypin,GPIO.OUT)
GPIO.output(relaypin,False)

while 1:
    # Get Inside Temp
    sht = adafruit_sht4x.SHT4x(board.I2C())
    roomtemperature = (9/5)*sht.temperature+32
    print(roomtemperature)

    # Determine whether or not to call heat
    if roomtemperature < mintemp:
        GPIO.output(relaypin, True)
        print("The thermostat is calling.")
    elif roomtemperature > maxtemp:
        GPIO.output(relaypin,False)
        print("The thermostat is no longer calling")

    # Get NOAA Temp
    n = NOAA()
    observations = n.get_observations(zipcode, countrycode)
    
    time.sleep(checktime)