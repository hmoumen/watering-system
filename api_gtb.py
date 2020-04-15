#!/usr/bin/python3
import warnings

import subprocess

import gtc

from flask import Flask, jsonify, request, abort

warnings.filterwarnings("ignore")

app = Flask(__name__)

items = []

gtc.init()

@app.route('/api/gtc', methods=['GET'])
def get_average_depth():
    result = gtc.average_depth()
    print (result)
    return jsonify({'item': result}), 201


if __name__ == '__main__':
    app.run(debug=True)
