#!/usr/bin/python3
import warnings

import subprocess

import gtc

from flask import Flask, jsonify, request, abort

warnings.filterwarnings("ignore")

app = Flask(__name__)

items = []

gtc1 = gtc.gtc()
relay1 = gtc1.relay(25)
relay2 = gtc1.relay(8)
relay3 = gtc1.relay(5)
relay4 = gtc1.relay(6)
ultrasonic1 = gtc1.ultrasonic(14, 15)
rain1 = gtc1.rain(17)
rain2 = gtc1.rain(27)

@app.route('/api/gtc_status', methods=['GET'])
def get_status():
    result = {"Depth":[], "Relais":[], "Pluviometre":[]}
    result["Depth"].append(ultrasonic1.average_depth())
    result["Relais"].append(relay1.status())
    result["Relais"].append(relay2.status())
    result["Relais"].append(relay3.status())
    result["Relais"].append(relay4.status())
    result["Pluviometre"].append(rain1.status())
    result["Pluviometre"].append(rain2.status())
    return jsonify({'item': result}), 201

@app.route('/api/relay<id>_<action>', methods=['GET'])
def relay(id, action):
    print(id)
    if (action == "on"):
        if (id == "1"):
            relay1.on()
            result = relay1.status()
        elif (id == "2"):
            relay2.on()
            result = relay2.status()
        elif (id == "3"):
            relay3.on()
            result = relay3.status()
        elif (id == "4"):
            relay4.on()
            result = relay4.status()
    elif (action == "off"):
        if (id == "1"):
            relay1.off()
            result = relay1.status()
        elif (id == "2"):
            relay2.off()
            result = relay2.status()
        elif (id == "3"):
            relay3.off()
            result = relay3.status()
        elif (id == "4"):
            relay4.off()
            result = relay4.status()
    else:
        result = "NC"
    
    return jsonify({'Relay status' : result}), 201

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)
