from noaa_sdk import noaa

# Create an instance of the NOAA class
n = noaa.NOAA()

# Define the zip code for the location you want to get weather data for
zip_code = '67801'  # Example zip code (Beverly Hills, CA)
country_code = 'US'

# Request the latest weather data for the specified zip code
observations = n.get_observations(zip_code, country_code)


# Initialize temperature and wind chill variables
temperature_celsius = 0  # Default value in Celsius
wind_chill_celsius = 0  # Default value in Celsius

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
wind_chill_fahrenheit = (wind_chill_celsius * 9/5) + 32
feels_like_temperature_fahrenheit = (temperature_celsius * 9/5) + 32 + wind_chill_celsius

print(f"Temperature: {temperature_fahrenheit} °F")
print(f"Wind Chill: {wind_chill_celsius} °C")
print(f"Feels Like: {feels_like_temperature_fahrenheit} °F")