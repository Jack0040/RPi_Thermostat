# RPi_Thermostat
Raspberry Pi smart thermostat

The goal of this software is to create a stable raspberry pi smart thermostat.

Currently, its only functionality is turning on and off the call for heat given the temperature, using a sht40 temp/humidity sensor to tell the room temperature.

Ultimately, this should include schedules, logic to optomize heat call start times given outdoor temperature, and a webui with historical logging and the ability to override the thermostat and change the schedules. 

This is my first dive into python, so don't expect my code to be any good. Hopefully it works though.


My Hardware: 
Raspberry Pi B mk2
SHT40 Temp Sensor
5V relay board

Prerequisite commands:
sudo pip3 install noaa-sdk 
sudo pip3 install adafruit-circuitpython-sht4x
