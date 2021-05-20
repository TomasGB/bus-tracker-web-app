from flask import Flask, jsonify, render_template
import requests
import folium

app = Flask(__name__)

#FRONTEND ROUTES
@app.route('/')
def index():
    def render_map():
        start_coords = (-38.71959, -62.27243)
        folium_map = folium.Map(width='70%',height='60%',location=start_coords, zoom_start=13)

        data = requests.get('https://www.gpsbahia.com.ar/frontend/track_data/8.json?hash=0.9738513800231414').json()
        #data= requests.get('https://busgpsapi.herokuapp.com/api/bus').json()
        for i in range(0,len(data)):
            bus_data = data['data'][i]
            bus_route = bus_data['direccion']
            folium.Marker(location=[bus_data['lat'], bus_data['lng']], popup=f'<strong>509</strong><br>{bus_route}').add_to(folium_map)
        
        return folium_map._repr_html_()

    return f'<h1>Bus Tracker</h1><div>{render_map()}<div>'
#API ROUTES
@app.route('/api/bus', methods=['GET'])
def BusData():

    api_endpoint='https://www.gpsbahia.com.ar/frontend/track_data/8.json?hash=0.9738513800231414'
    res = requests.get(api_endpoint).json()
    res_list={'buses':[]}

    for i in range(0,len(res)):
        bus_data_response = res['data'][i]
        result = {'interno':bus_data_response['interno'],'direccion':bus_data_response['direccion'],'lat':bus_data_response['lat'],'lng':bus_data_response['lng']}
        res_list['buses'].append(result)

    return jsonify(res_list)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)