# Import dependencies
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import numpy as np
import datetime as dt


# Database Setup


# Create engine to connect to SQLite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Flask Setup

app = Flask(__name__)


# Flask Routes


# Homepage route
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session from Python to the database
    session = Session(engine)

    # Find the most recent date in the dataset
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    most_recent_date_dt = dt.datetime.strptime(most_recent_date, "%Y-%m-%d")
    
    # Calculate the date one year ago from the most recent date
    one_year_ago = most_recent_date_dt - dt.timedelta(days=365)
    
    # Query for the last 12 months of precipitation data
    precipitation_results = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= one_year_ago)\
        .all()
    
    # Close session
    session.close()

    # Create a dictionary with date as the key and prcp as the value
    precipitation_data = {date: prcp for date, prcp in precipitation_results}
    
    # Return the JSON representation of the dictionary
    return jsonify(precipitation_data)

# Stations route
@app.route("/api/v1.0/stations")
def stations():
    # Create session from Python to the database
    session = Session(engine)

    # Query all the stations
    stations_results = session.query(Station.station).all()

    # Close session
    session.close()

    # Unravel results into a list
    stations_list = list(np.ravel(stations_results))
    
    # Return JSON representation of the list
    return jsonify(stations_list)

# Temperature observations (TOBS) route for the most active station
@app.route("/api/v1.0/tobs")
def tobs():
    # Create session from Python to the database
    session = Session(engine)

    # Find the most recent date in the dataset
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    most_recent_date_dt = dt.datetime.strptime(most_recent_date, "%Y-%m-%d")
    
    # Calculate the date one year ago from the most recent date
    one_year_ago = most_recent_date_dt - dt.timedelta(days=365)

    # Find the station with the most observations
    most_active_station = session.query(Measurement.station)\
        .group_by(Measurement.station)\
        .order_by(func.count(Measurement.station).desc())\
        .first()[0]

    # Query the dates and temperature observations for the previous year of the most active station
    tobs_results = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == most_active_station)\
        .filter(Measurement.date >= one_year_ago)\
        .all()

    # Close session
    session.close()

    # Convert query results into a list of dictionaries
    tobs_list = [{date: tobs} for date, tobs in tobs_results]
    
    # Return JSON representation of the list
    return jsonify(tobs_list)

# Start date route (TMIN, TAVG, TMAX from start date onwards)
@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create session from Python to the database
    session = Session(engine)

    # Query the minimum, average, and maximum temperatures from the start date onward
    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start)\
        .all()

    # Close session
    session.close()

    # Return JSON representation of the temperature statistics
    temp_data = {
        "TMIN": temp_stats[0][0],
        "TAVG": temp_stats[0][1],
        "TMAX": temp_stats[0][2]
    }
    
    return jsonify(temp_data)

# Start and end date route (TMIN, TAVG, TMAX for the given date range)
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Create session from Python to the database
    session = Session(engine)

    # Query the minimum, average, and maximum temperatures between the start and end dates
    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start)\
        .filter(Measurement.date <= end)\
        .all()

    # Close session
    session.close()

    # Return JSON representation of the temperature statistics
    temp_data = {
        "TMIN": temp_stats[0][0],
        "TAVG": temp_stats[0][1],
        "TMAX": temp_stats[0][2]
    }
    
    return jsonify(temp_data)


# Run the Flask App

if __name__ == "__main__":
    app.run(debug=True)