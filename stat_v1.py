import RPi.GPIO as GPIO
import board
import adafruit_sht4x
import time
from noaa_sdk import noaa
import csv
from datetime import datetime

# Settings for thermostat
relaypin = 23  # Pin that relay is hooked up to
setpoint = int(input("What setpoint do you wish: "))  # thermostat setpoint
overshoot = 0.5  # Maximum overshoot in degrees before stat no longer calls for heat
undershoot = 0.5  # Maximum undershoot in degrees before thermostat calls for heat
checktime = 60  # Number of seconds to wait before checking temperature
zip_code = '26505'
country_code = 'US'

# Initialize temperature, wind chill, and calling variables
temperature_celsius = 0  # Default value in Celsius
wind_chill_celsius = 0  # Default value in Celsius
calling = False

# CSV filename
csv_filename = 'trends.csv'

# Set GPIO Settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(relaypin, GPIO.OUT)
GPIO.output(relaypin, False)

# Initialize the SHT4x sensor
sht = adafruit_sht4x.SHT4x(board.I2C())

# Delay between NOAA API requests (in seconds, e.g., 15 minutes)
api_request_delay = 15 * 60

# Timestamp for the last NOAA API request
last_api_request_time = 0

while True:
    # Get current timestamp
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get Inside Temp
    roomtemperature = (9 / 5) * sht.temperature + 32

    # Determine mintemp and maxtemp based on setpoint and over/undershoot
    mintemp = setpoint - undershoot
    maxtemp = setpoint + overshoot

    # Determine whether or not to call for heat
    if roomtemperature < mintemp:
        GPIO.output(relaypin, True)
        calling = True
    elif roomtemperature > maxtemp:
        GPIO.output(relaypin, False)
        calling = False

    # Check if it's time to make an API request to NOAA
    current_timestamp = time.time()
    if current_timestamp - last_api_request_time >= api_request_delay:
        # Get NOAA Temp
        n = noaa.NOAA()
        observations = n.get_observations(zip_code, country_code)
        for observation in observations:
            temperature_info = observation['temperature']
            wind_chill_info = observation['windChill']
            temperature_celsius = temperature_info['value']
            wind_chill_celsius = wind_chill_info['value'] if wind_chill_info['value'] is not None else 0
            break  # Exit the loop after the first observation

        # Update the timestamp for the last API request
        last_api_request_time = current_timestamp

    # Check if temperature_celsius is not None before conversion
    if temperature_celsius is not None:
        temperature_fahrenheit = (temperature_celsius * 9 / 5) + 32
    else:
        temperature_fahrenheit = None

    # Convert wind chill to Fahrenheit
    if wind_chill_celsius == 0:
        wind_chill_fahrenheit = temperature_fahrenheit
    else:
        wind_chill_fahrenheit = (wind_chill_celsius * 9 / 5) + 32

    # Log the data to the CSV file
    with open(csv_filename, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write a header row if the file is empty
        if csv_file.tell() == 0:
            csv_writer.writerow(['Time', 'Room Temperature (F)', 'Outside Temperature (F)', 'Wind Chill (F)', 'Heater Status'])

        csv_writer.writerow([current_time, roomtemperature, temperature_fahrenheit, wind_chill_fahrenheit, calling])
        csv_file.flush()

    # Output data to the console
    print(f"Time: {current_time}")
    print(f"Room Temperature: {roomtemperature}F")
    print(f"Outside Temperature: {temperature_fahrenheit}F")
    print(f"Wind Chill: {wind_chill_fahrenheit}F")
    print(f"Heater Status: {'Running' if calling else 'Off'}")

    time.sleep(checktime)
