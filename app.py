from flask import Flask, jsonify
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Bus Tracker API</h1>'

@app.route('/api/bus', methods=['GET'])
def BusData():
    api_endpoint='https://www.gpsbahia.com.ar/frontend/track_data/8.json?hash=0.9738513800231414'

    res = requests.get(api_endpoint).json()
    colectivos = res['data'][0]
    result = {'interno':colectivos['interno'],'direccion':colectivos['direccion'],'lat':colectivos['lat'],'lng':colectivos['lng']}

    return jsonify(result)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)