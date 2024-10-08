### Requirements
```
Flask==3.0.3   
Flask-SQLAlchemy==3.1.1
GeoAlchemy2==0.15.2
Jinja2==3.1.4
psycopg2==2.9.9
SQLAlchemy==2.0.35
Werkzeug==3.0.4
```
### Set up and create flask environment

**Bash**
```
mkdir flaskapphurricane
cd flaskapphurricane
python -m venv flaskvenv
flaskvenv\Scripts\activate
pip install flask
type nul>app.py (create a Python file for the Flask app, e.g., app.py:)
```
**Edit app.py and add the following folder/directory:**

1. create templates for app.html
2. static as a directory

**use python to execute your Flask app**
```
python app.py
```
### How to use

Add connection to your database server
```'postgresql://postgres:xxxx@localhost/postgres'``` is URI that tells Flask how to connect to the PostgreSQL database

```postgresql``` Specifies that you’re using the PostgreSQL database system.

```postgres``` The username for the database.

```xxxx``` The password for the postgres user.

```localhost``` Specifies that the database server is running locally on your machine.

```postgres``` The name of the database being connected to

Defines a route that responds to GET requests when a URL with a specific month, date, and time is accessed.
```
@app.route('/month=<string:month>&date=<string:mdt>&time=<string:hh>', methods=['GET'])
```
### Data source
NHC GIS Archive - Tropical Cyclone Best Track, NOAA

https://www.nhc.noaa.gov/gis/archive_besttrack_results.php?id=al09&year=2022&name=Hurricane%20IAN

![Screenshot (2482)](https://github.com/user-attachments/assets/09febfdc-2210-4510-9d2e-9cfdb227e1ff)

![Screenshot (2483)](https://github.com/user-attachments/assets/3a4d711f-ac15-42a5-9bc0-024d976e4fc0)

![Screenshot (2484)](https://github.com/user-attachments/assets/81d71ec1-ef35-4019-8803-a1c0b3c6e4ec)


