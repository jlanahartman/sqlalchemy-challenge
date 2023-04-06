# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


app = Flask(__name__)

# connect to database 
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# refelect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# create our session (link) from Python to the DB
session = Session(engine)

# home route
@app.route("/")
def home():
    return(
        f"<center><h2> Welcome to the Hawaii Climate Analysis Local API!<h2><center>"
        f"<center><h3>Select from one of the avaialable routes:<h3><center>"
        f"<center>/api/v1.0/precipitation<center>"
        f"<center>/api/v1.0/stations<center>"
        f"<center>/api/v1.0/tabs<center>"
        f"<center>/api/v1.0/start/end<center)"
        )

# /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precip():
    # return the previous year's precipitation as a json
    # calculate the date one year from the last date in the data set
    previousYear = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# preform a query to retrieve the date and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= previousYear).all()

    session.close()
# dicitionary with the date as the key
#  precipitation (prcp) as the value    
    precipitation = {date : prcp for date, prcp in results}
# convert to a json
    return jsonify(precipitation)

# /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    session.close()

    stationList = list(np.ravel(results))

    return jsonify(stationList)

# /api/v1.0/tabs route

@app.route("/api/v1.0/tabs")
def temperatures():
    previousYear = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    results = session.query(Measurement.tabs).\
             filter(Measurement.station == 'USC00519281').\
            filter(Measurement.date >= previousYear).all()
    
    session.close()

    temperatureList = list(np.ravel(results))

    return jsonify(temperatureList)

# /api/v1.0/start/end and /api/v1.0/start routes
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0<start>/<end>")
def dateStats(start=None, end=None):

    selection = [func.min(Measurement.tabs), func.min(Measurement.tabs), func.avg(Measurement.tabs)]

    if not end:
        startDate = dt.datetime.strptime(start, "%m%d%Y")

        results = session.query(*selection).filter(Measurement.date >= startDate).all()

        session.close()

        temperatureList = list(np.ravel(results))

        return jsonify(temperatureList)

    else: 

        startDate = dt.datetime.strptime(start, "%m%d%Y")
        endDate = dt.datetime.strptime(end, "%m%d%Y")
        
        results = session.query(*selection)\
                .filter(Measurement.date >= startDate)\
                .filter(Measurement.date <= endDate).all()
        
        session.close()

        temperatureList = list(np.ravel(results))

        return jsonify(temperatureList)

# app launcher 
if __name__ == '__main__':
    app.run(debug=True)