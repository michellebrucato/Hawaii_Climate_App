from flask import Flask, jsonify, request
from datetime import datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

past_year = "2016-08-23"


@app.route("/")
def welcome():
    return (
        f"<center><h1 style='color:#E9A8CB;'>ALOHA!</style></h1><br/>"
        f"<h1 style='color:#FF3379;'>Welcome to the Hawaii Climate API</style></h1><br/>"
        f"<h3 style='color:#34B9D9;'><u>Available Routes:</u><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end></h3><br/></center></style>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    """Query the precipitation from the past 12 months of the dataset"""
    past_year_prcp = (
        session.query(Measurement.date, func.avg(Measurement.prcp))
        .filter(Measurement.date >= past_year)
        .group_by(Measurement.date)
        .all()
    )
    return jsonify(past_year_prcp)


@app.route("/api/v1.0/stations")
def stations():
    """Query all of the stations from the dataset"""
    stats = session.query(Station.station, Station.name).all()
    return jsonify(stats)


@app.route("/api/v1.0/tobs")
def tobs():
    """Query Temperature Observations (tobs) from the last year of the dataset"""
    past_year_tobs = (
        session.query(Measurement.date, Measurement.station, Measurement.tobs)
        .filter(Measurement.date >= past_year)
        .all()
    )
    return jsonify(past_year_tobs)


@app.route("/api/v1.0/<start>")
def starttemp(start):
    """When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date."""
    start_temp = (
        session.query(
            Measurement.date,
            func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .group_by(Measurement.date)
        .all()
    )
    return jsonify(start_temp)


@app.route("/api/v1.0/<start>/<end>")
def startendtemp(start, end):
    """When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive."""
    range_temp = (
        session.query(
            Measurement.date,
            func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .filter(Measurement.date <= end)
        .group_by(Measurement.date)
        .all()
    )
    return jsonify(range_temp)


if __name__ == "__main__":
    app.run(debug=True)
