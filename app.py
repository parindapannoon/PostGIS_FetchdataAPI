from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from sqlalchemy import func

app = Flask(__name__)
app.config.update(
    SECRET_KEY='1234',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:xxxx@localhost/postgres',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)

class Hurricane(db.Model):
    __tablename__ = 'hurricane'
    gid = db.Column(db.Integer, primary_key=True)
    hh = db.Column(db.Integer)
    geom = db.Column(Geometry('POLYGON'))
    mdt = db.Column(db.Integer)
    month = db.Column(db.Integer)
    def __repr__(self):
        return f'The id is {self.gid}, HH is {self.hh}, mdt is {self.mdt}, month is {self.month}'

class PointHurricane(db.Model):
    __tablename__ = 'al092022_pts'
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    day = db.Column(db.Integer, nullable=False)  # Assuming day is stored as integer
    month = db.Column(db.Integer, nullable=False)  # Assuming month is stored as integer

    def __repr__(self):
        return f'Lat: {self.lat}, Lon: {self.lon}, Day: {self.day}, Month: {self.month}'

# Route to display data (Polygons)
@app.route('/show_polygons/hh=<string:hh>', methods=['GET'])
def show_polygons(hh):
    # Query to get polygon geometries from the database and transform them to GeoJSON format
    name_list = [name for name in hh.split('&')]
    polygons = db.session.query(func.ST_AsGeoJSON(Hurricane.geom)).filter(Hurricane.hh.in_(name_list)).all()
    # Convert list of Row objects to a list of GeoJSON strings
    polygon_geojson = [polygon[0] for polygon in polygons]
# Fetch points
    points = PointHurricane.query.with_entities(PointHurricane.lat, PointHurricane.lon, PointHurricane.day, PointHurricane.month).all()
    points_list = [{'lat': point.lat, 'lon': point.lon, 'day': point.day, 'month': point.month} for point in points]
    # Render template with both points and polygons
    return render_template('app.html', polygons=polygon_geojson, points=points_list)

# Route to display data (Points)
@app.route('/show_points', methods=['GET'])
def show_points():
    # Query to get coordinates from the database
    points = PointHurricane.query.with_entities(PointHurricane.lat, PointHurricane.lon, PointHurricane.day, PointHurricane.month).all()
    # Convert Row objects to a list of dictionaries or tuples
    points_list = [{'lat': point.lat, 'lon': point.lon, 'day': point.day, 'month': point.month} for point in points]
    print(points[0])
    print(type(points[0]))
    return render_template('app.html', polygons=[], points=points_list)


# Route to display month, date and time of the hurricane
@app.route('/month=<string:month>&date=<string:mdt>&time=<string:hh>', methods=['GET'])
def show_all(month, mdt, hh):
    # Fetch polygons
    polygons = db.session.query(func.ST_AsGeoJSON(Hurricane.geom)).filter(Hurricane.month==month, Hurricane.mdt==mdt, Hurricane.hh==hh).all()
    polygon_geojson = [polygon[0] for polygon in polygons]

    # Fetch points
    points = PointHurricane.query.with_entities(PointHurricane.lat, PointHurricane.lon, PointHurricane.day, PointHurricane.month).all()
    points_list = [{'lat': point.lat, 'lon': point.lon, 'day': point.day, 'month': point.month} for point in points]
    # Render template with both points and polygons
    return render_template('app.html', polygons=polygon_geojson, points=points_list)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
