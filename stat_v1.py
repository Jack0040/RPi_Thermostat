import RPi.GPIO as GPIO
import board
import adafruit_sht4x
import time
from noaa_sdk import noaa
import csv
from datetime import datetime

# Settings for thermostat
relaypin = 23  # Pin that relay is hooked up to
setpoint = 70 # thermostat setpoint
overshoot = 1 # Maximum overshoot in degrees before stat no longer calls for heat
undershoot = 1 # Maximum undershoot in degrees before thermostat calls for heat
checktime = 60  # Number of seconds to wait before checking temperature
zip_code = '26505'
country_code = 'US'

# Initialize temperature, wind chill, and calling variables
temperature_celsius = 0  # Default value in Celsius
wind_chill_celsius = 0  # Default value in Celsius
calling = False #not sure if I can do this

# CSV filename
csv_filename = 'trends.csv'

# Set GPIO Settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(relaypin, GPIO.OUT)
GPIO.output(relaypin, False)

# Initialize the SHT4x sensor
sht = adafruit_sht4x.SHT4x(board.I2C())

with open(csv_filename, mode='a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write a header row if the file is empty (first time running the script)
    if csv_file.tell() == 0:
        csv_writer.writerow(['Time', 'Room Temperature (°F)', 'Outside Temperature (°F)', 'Wind Chill (°F)'])

while True:
     # Get current timestamp
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get Inside Temp
    roomtemperature = (9 / 5) * sht.temperature + 32


    # Determine mintemp and maxtemp based on setpoint and over/undershoot (I want this in the loop so that it can be changed by override)
    mintemp = setpoint - undershoot
    maxtemp = setpoint + overshoot

    # Determine whether or not to call for heat
    if roomtemperature < mintemp:
        GPIO.output(relaypin, True)
        calling = True #not sure if I can do this

    elif roomtemperature > maxtemp:
        GPIO.output(relaypin, False)
        calling = False #not sure if I can do this


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
    temperature_fahrenheit = (temperature_celsius * 9 / 5) + 32
    if wind_chill_celsius == 0:
        wind_chill_fahrenheit = temperature_fahrenheit
    else:
        wind_chill_fahrenheit = (wind_chill_celsius * 9 / 5) + 32

    # Log the data to the CSV file
    csv_writer.writerow([current_time, roomtemperature, temperature_fahrenheit, wind_chill_fahrenheit])
    csv_file.flush()

    # Output data to the console
    print(f"Time: {current_time}")
    print(f"Room Temperature: {roomtemperature} °F")
    print(f"Outside Temperature: {temperature_fahrenheit} °F")
    print(f"Wind Chill: {wind_chill_fahrenheit} °F")
    print(f"Is Thermostat Calling: {calling}") #not sure if I can do this

    time.sleep(checktime)
