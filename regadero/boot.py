# boot file of the regadero project
import json
import network

print("Initializing board...")
print("> Getting settings")
SETTINGS = json.loads(open('settings.json', 'r').read())

print("> Configuring wifi")

wlan = network.WLAN(network.STA_IF)
