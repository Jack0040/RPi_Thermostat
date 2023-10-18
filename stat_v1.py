import RPi.GPIO as GPIO
import board
import adafruit_sht4x
import time
from noaa_sdk import noaa

# Settings for thermostat
relaypin = 23 # Pin that relay is hooked up to
maxtemp = 71 # Temp to stop call for heat
mintemp = 69 # Temp to start call for heat
checktime = 1 # Number of seconds to wait before checking temperature
zip_code = '26505'
country_code = 'US'


# Set GPIO Settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(relaypin,GPIO.OUT)
GPIO.output(relaypin,False)
# Initialize temperature and wind chill variables
temperature_celsius = 0  # Default value in Celsius
wind_chill_celsius = 0  # Default value in Celsius

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
    # Create an instance of the NOAA class
    n = noaa.NOAA()
    # Request the latest weather data for the specified zip code
    observations = n.get_observations(zip_code, country_code)
    # Iterate through the generator to retrieve the first observation
    for observation in observations:
        temperature_info = observation['temperature']
        wind_chill_info = observation['windChill']
    
        # Extract the numerical values and set wind chill to 0 if it's None
        temperature_celsius = temperature_info['value']
        wind_chill_celsius = wind_chill_info['value'] if wind_chill_info['value'] is not None else 0
        break  # Exit the loop after the first observation

    # Convert Celsius to Fahrenheit
    temperature_fahrenheit = (temperature_celsius * 9/5) + 32
    if wind_chill_celsius == 0:
       wind_chill_fahrenheit = temperature_fahrenheit
    else:
       wind_chill_fahrenheit = (wind_chill_celsius * 9/5) + 32

    print(f"Temperature: {temperature_fahrenheit} °F")
    print(f"Wind Chill: {wind_chill_fahrenheit} °F")


    time.sleep(checktime)