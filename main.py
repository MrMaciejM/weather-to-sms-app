from twilio.rest import Client
import requests
import datetime
import sys
from sms_data_folder import smsdata

# Tells Python to search root dir for modules
sys.path.append("./100DaysOfPython/")

data = smsdata.secret_data  # imported data

twilio_acc_sid = data["twilio_acc_sid"]
twilio_auth_token = data["twilio_auth_token"]
OWM_API_KEY = data["OWM_API_KEY"]
MY_NUMBER = data["MY_NUMBER"]
TWILIO_NUMBER = data["TWILIO_NUMBER"]
LAT = data["LAT"]
LON = data["LON"]
UNITS = data["UNITS"]

# import os #  needed for the os.environ.get() function
# API_KEY = os.environ.get("API_KEY")  # use this method for storing code in the cloud without exposing the keys

# API Endpoint and parameters needed to make the call
API_ENDPOINT = (f"https://api.openweathermap.org/data/2.5/forecast?"
                f"lat={LAT}&"
                f"lon={LON}&"
                f"appid={OWM_API_KEY}&"
                f"units={UNITS}")

# Send request to the API to get the weather data
response = requests.get(API_ENDPOINT)

# Weather data
hour_selection = 0  # 0 is current time (hour)
round_to = 1  # select to which decimal you want to round the temp number to, e.g 1 = 12.1, 2 = 12.11
weather_data = response.json()  # converts data from API call into JSON format

weather_timestamp = weather_data["list"][hour_selection]["dt"]
weather_temp = round(weather_data["list"][hour_selection]["main"]["temp"], round_to)
weather_min_temp = round(weather_data["list"][hour_selection]["main"]["temp_min"], round_to)
weather_max_temp = round(weather_data["list"][hour_selection]["main"]["temp_max"], round_to)
weather_short_desc = weather_data["list"][hour_selection]["weather"][0]["main"]
weather_long_desc = weather_data["list"][hour_selection]["weather"][0]["description"]

print(weather_temp)
# Convert Unix epoch time from the weather API
stamp = weather_timestamp
dt = datetime
formatted_time = dt.datetime.fromtimestamp(stamp)

client = Client(twilio_acc_sid, twilio_auth_token)
message = client.messages.create(
    body=f"\nHello! Here is your weather for today:\n"
         f"Time: {formatted_time}\n"
         f"Temp: {weather_temp}°C\n"
         f"Desc: {weather_short_desc}\n"
         f"Long desc: {weather_long_desc}\n"
         f"Min temp: {weather_min_temp}°C\n"
         f"Max temp: {weather_max_temp}°C\n",
    from_=f"{TWILIO_NUMBER}",
    to=f"{MY_NUMBER}",
)
