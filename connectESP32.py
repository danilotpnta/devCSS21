# import streams
import streams
import json

# import the wifi interface
from wireless import wifi

# import the http module
import requests

# the wifi module needs a networking driver to be loaded
# in order to control the board hardware.
# FOR THIS EXAMPLE TO WORK, A NETWORK DRIVER MUST BE SELECTED BELOW

# uncomment the following line to use the ESP8266 wifi driver
# from espressif.esp8266wifi import esp8266wifi as wifi_driver

# uncomment the following line to use the ESP32 wifi driver
from espressif.esp32net import esp32wifi as wifi_driver

streams.serial()

# init the wifi driver!
# The driver automatically registers itself to the wifi interface
# with the correct configuration for the selected board
wifi_driver.auto_init()

# use the wifi interface to link to the Access Point
# change network name, security and password as needed
print("Establishing Link...")
try:
    # FOR THIS EXAMPLE TO WORK, "Network-Name" AND "Wifi-Password" MUST BE SET
    # TO MATCH YOUR ACTUAL NETWORK CONFIGURATION
    wifi.link("Network-Name",wifi.WIFI_WPA2,"Wifi-Password")
except Exception as e:
    print("ooops, something wrong while linking :(", e)
    while True:
        sleep(1000)

# let's try to connect to timeapi.org to get the current UTC time
for i in range(3):
    try:
        print("Trying to connect...")
        # we need to impersonate a web browser: as easy as setting the http user-agent header
        user_agent = {"user-agent":"Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405"}
        # go get that time!
        # url resolution and http protocol handling are hidden inside the requests module
        response = requests.get("http://www.worldtimeserver.com/handlers/GetData.ashx",{"action":"GCTData"},headers=user_agent)
        # let's check the http response status: if different than 200, something went wrong
        print("Http Status:",response.status)
        # if we get here, there has been no exception, exit the loop
        break
    except Exception as e:
        print(e)


try:
    # check status and print the result
    if response.status==200:
        print("Success!!")
        print("-------------")
        print("And the result is:",response.content)
        print("-------------")
        js = json.loads(response.content)
        print("City:",js["City"])
        print("Date:",js["FormattedDate"])
        print("Time:",js["ThisTime"])
except Exception as e:
    print("ooops, something very wrong! :(",e)
