# Realtime city bus tracker 🚌 🗺

Python based web application to track in realtime city buses showing specific data.
Utilized Flask microframework as backend and Folium to display the map.

## How to use?

+ Clone this repository with `git clone https://github.com/TomasGB/bus-tracker-web-app.git`

+ Install the requirements `pip install -r requirements.txt`

+ Run the flask server with `python app.py`


## Project structure

* Routes/
    * `<line_number>`: Folder containing json files with buses routes.

* Static/
    * Styles: CSS file with styles.

* Templates: Folder with html templates and where the rendered map gets saved.

* `app.py` : File containing Flask routes related code.

* `utils.py` : File containg functions utilized to render the map.

* requirements.txt: File with all dependencies used.

## Routes

* `http://127.0.0.1:5000/` : Inital route to select wich bus line you want to track.

* `http://127.0.0.1:5000/line/<line>/` : Route where a map is rendered displaying all buses in their current position.

* `http://127.0.0.1:5000/api/buses-data/<line>/` : Route where all buses data is displayed as json.