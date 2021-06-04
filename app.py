from flask import Flask, jsonify , render_template
import requests
from utils import render_map, APIS_DICTIONARY


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

#FRONTEND ROUTES
@app.route('/', methods=['GET','POST'])
def index():
    
    return render_template('index.html')

@app.route('/line/<line>/', methods=['GET','POST'])
def lines(line):
    line_number=line
    rendered_map=render_map(line_number)
    return render_template('tracking.html',map=rendered_map, line=line_number)


#API ROUTES
@app.route('/api/buses-data/<line>/', methods=['GET'])
def BusData(line):

    res = requests.get(APIS_DICTIONARY[line]).json()
    res_list={'buses':[]}

    for i in range(0,len(res['data'])):
        bus_data_response = res['data'][i]
        result = {'interno':bus_data_response['interno'],'direccion':bus_data_response['direccion'],'lat':bus_data_response['lat'],'lng':bus_data_response['lng']}
        res_list['buses'].append(result)

    return jsonify(res_list)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
    