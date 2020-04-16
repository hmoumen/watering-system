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
def get_average_depth():
    result = {"Depth":[], "Relais":[], "Pluviometre":[]}
    result["Depth"].append(ultrasonic1.average_depth())
    result["Relais"].append(relay1.status())
    result["Relais"].append(relay2.status())
    result["Relais"].append(relay3.status())
    result["Relais"].append(relay4.status())
    result["Pluviometre"].append(rain1.status())
    result["Pluviometre"].append(rain2.status())
    return jsonify({'item': result}), 201


if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)
