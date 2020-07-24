from flask import Flask, render_template, json, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql, folium, os
#from redis import Redis

app = Flask(__name__)
#redis = Redis(host='redis', port=6379)

app.config['SQLALCHEMY_DATABASE_URI'] ="mysql+pymysql://root:qwer1234@localhost/test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Station(db.Model):
    name = db.Column(db.String(20), primary_key = True)
    x = db.Column(db.Float(20))
    y = db.Column(db.Float(20))

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

class cafe(db.Model):
    name = db.Column(db.String(20), primary_key = True)
    x = db.Column(db.Float(20))
    y = db.Column(db.Float(20))
    brand = db.Column(db.String(20))
        
    def __init__(self, name, x, y, brand):
        self.name = name
        self.x = x
        self.y = y
        self.brand = brand
        
@app.route("/")
def home():
    #redis.incr('hits')
    return render_template("index.html")

@app.route("/list")
def list():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, 'static', 'data/up_one_head.json')
    data = json.load(open(json_url))
    station, time = "", []
    for i in data['data']:
        station += i['역명']+","
        time.append([i['17~18'], i['18~19'], i['19~20'], i['20~21'], i['22~23'], i['23~24']])
    return render_template("list.html", station=station, time=time)

@app.route("/cafe")
def cafe():
    return render_template("cafescore.html")

@app.route("/test")
def test():
    result = cafe.query.all()
    return render_template("test.html", result = result)

@app.route('/map')
def test2():
    start_coords = (46.9540700, 142.7360300)
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    return folium_map._repr_html_()

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0")