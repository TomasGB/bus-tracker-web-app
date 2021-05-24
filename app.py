from flask import Flask, jsonify, render_template
import requests
from utils import render_map


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

#FRONTEND ROUTES
@app.route('/')
def index():
    rendered_map=render_map()

    return render_template('home.html',map=rendered_map)


#API ROUTES
@app.route('/api/bus', methods=['GET'])
def BusData():

    api_endpoint='https://www.gpsbahia.com.ar/frontend/track_data/1.json?hash=0.225134251739882'
    res = requests.get(api_endpoint).json()
    res_list={'buses':[]}

    for i in range(0,len(res['data'])):
        bus_data_response = res['data'][i]
        result = {'interno':bus_data_response['interno'],'direccion':bus_data_response['direccion'],'lat':bus_data_response['lat'],'lng':bus_data_response['lng']}
        res_list['buses'].append(result)

    return jsonify(res_list)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
    