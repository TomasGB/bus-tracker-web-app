from flask import Flask, jsonify, render_template
import requests
import folium
import os


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

#FRONTEND ROUTES
@app.route('/')
def index():
    def render_map():

        start_coords = (-38.71959, -62.27243)
        folium_map = folium.Map(width='100%',height='70%',location=start_coords, zoom_start=13, tiles="OpenStreetMap")

        data = requests.get('https://www.gpsbahia.com.ar/frontend/track_data/1.json?hash=0.225134251739882').json()
        #data= requests.get('https://busgpsapi.herokuapp.com/api/bus').json()

        #Showing all buses on map
        for i in range(0,len(data)+1):
            bus_data = data['data'][i]
            bus_route = bus_data['direccion']
            bus_number = bus_data['interno']

            if bus_route=='ida':
                marker_color='#119c52'
            else:
                marker_color='#c71212'

            folium.Marker(location=[bus_data['lat'], bus_data['lng']],tooltip='Click for info' ,popup=f'<strong>Linea:</strong> 509<br><strong>ruta:</strong> {bus_route}<br><strong>interno:</strong> {bus_number}', icon=folium.Icon(icon="bus",prefix='fa',color='black',icon_color=f'{marker_color}')).add_to(folium_map)

        if os.path.exists('./templates/map.html'):
            os.remove('./templates/map.html')

        folium_map.save('./templates/map.html')
        return folium_map._repr_html_()

    rendered_map=render_map()

    return render_template('home.html',map=rendered_map)


#API ROUTES
@app.route('/api/bus', methods=['GET'])
def BusData():

    api_endpoint='https://www.gpsbahia.com.ar/frontend/track_data/1.json?hash=0.225134251739882'
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
    