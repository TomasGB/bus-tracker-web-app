from flask import Flask, jsonify, render_template
import requests
import folium
import os
from math import sin, cos, sqrt, atan2, radians


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

#FRONTEND ROUTES
@app.route('/')
def index():
    def calculate_distance(user_lat,user_lng,lat,lng):
        #Haversine formula for distances
        # approximate radius of earth in km
        R = 6373.0

        #user location
        lat1 = radians(user_lat)
        lon1 = radians(user_lng)

        #target location
        lat2 = radians(lat)
        lon2 = radians(lng)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        distance = "{:.2f}".format(distance)

        return distance

    def render_map():
        user_position=[-38.69403135950687,-62.29086757471586]
        start_coords = (user_position[0], user_position[1])

        folium_map = folium.Map(width='100%',height='70%',location=start_coords, zoom_start=13, tiles="OpenStreetMap")

        data = requests.get('https://www.gpsbahia.com.ar/frontend/track_data/1.json?hash=0.225134251739882').json()
        #data={'data':[]}

        #my position
        folium.Marker(
                location=[user_position[0], user_position[1]], 
                popup=f'You are here', 
                icon=folium.Icon(icon="user",prefix='fa',color='blue',icon_color='white')
                ).add_to(folium_map)

        #Showing all buses on map
        buses_amount=len(data['data'])

        if buses_amount == 0:
            print('No buses currently')
        else:
            for i in range(0,buses_amount):
                bus_data = data['data'][i]
                bus_route = bus_data['direccion']
                bus_number = bus_data['interno']

                if bus_route=='ida':
                    marker_color='#119c52'
                else:
                    marker_color='#c71212'

                distance=calculate_distance(float(user_position[0]), float(user_position[1]),float(bus_data['lat']),float(bus_data['lng']))

                folium.Marker(location=[bus_data['lat'], bus_data['lng']],
                            tooltip='Click for info',
                            popup=f'<strong>Linea:</strong> 509<br><strong>ruta:</strong> {bus_route}<br><strong>interno:</strong> {bus_number}<br><strong>distancia: </strong>{distance}Km',
                            icon=folium.Icon(icon="bus",prefix='fa',color='black',icon_color=f'{marker_color}')
                            ).add_to(folium_map)

        #Render routes
        going_route = os.path.join('./routes/going_route.json')
        comeback_route = os.path.join('./routes/comeback_route.json')
        style_going = {'fillColor': '#119c52', 'color': '#119c52'}
        style_comeback = {'fillColor': '#c71212', 'color': '#c71212'}
        folium_map.add_child(folium.features.GeoJson(going_route,name='ida', style_function=lambda x:style_going))
        folium_map.add_child(folium.features.GeoJson(comeback_route,name='vuelta', style_function=lambda x:style_comeback))

        #Checks if the map exists to update it
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

    for i in range(0,len(res['data'])):
        bus_data_response = res['data'][i]
        result = {'interno':bus_data_response['interno'],'direccion':bus_data_response['direccion'],'lat':bus_data_response['lat'],'lng':bus_data_response['lng']}
        res_list['buses'].append(result)

    return jsonify(res_list)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
    