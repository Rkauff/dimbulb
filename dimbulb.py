
from urllib.request import urlopen as uReq
import urllib.request
from bs4 import BeautifulSoup as soup
import ssl
import json
from twilio.rest import Client

account_sid = "twilio account SID"
auth_token = "twilio auth token"
client = Client(account_sid, auth_token)

hue_username = 'hue username'
sensor_data = 'https://192.168.1.148/api/<hue username>/sensors/14'
#my Family room sensor is 2
#Basement sensor is 10
#Living Room sensor is 14
lights_data = 'https://192.168.1.148/api/<hue username>/lights/2'
#deck is light 2

light_on_off = 'https://192.168.1.148/api/<hue username>/lights/6/state'
#Deck is 2
#Office is 6

ssl._create_default_https_context = ssl._create_unverified_context

uClient = uReq(sensor_data)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")
parser = json.loads(page_html)
celsius = (parser['state']['temperature'])

# just a vanilla celsius to fahrenheit conversion function I wrote
def c_to_f_conversion(celsius):
    celsius = celsius/100
    t = (celsius * 1.8 + 32)
    return t
    print(t)

# round the temperature. No need for a bunch of bullshit digits after the decimal
fahrenheit = round(c_to_f_conversion(celsius),1)
#print("The temp in the family room is " + str(fahrenheit))

#This lines just sends me a text message to let me know what the temp is
client.messages.create(
    to="+16307889299",
    from_="+16305184064",
    body="The temperature in the family room is " + str(fahrenheit))


#Changing the state of lightbulbs.
DATA = b'{"on":true}' #THIS IS THE LINE THAT CHANGES THE BULBS TO BE ON OR OFF
#You could also just dim the bulb to 10% of something if you wanted 
req = urllib.request.Request(url=light_on_off, data=DATA,method='PUT')
with urllib.request.urlopen(req) as f:
    pass
print(f.status)
print(f.reason)

