from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt
import logging
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)

# References to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Context manager for session handling
@contextmanager
def session_scope():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

# Homepage route
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    with session_scope() as session:
        # Find the most recent date in the data set
        latest_date = session.query(func.max(Measurement.date)).scalar()
        
        logging.debug(f"Latest date in the dataset: {latest_date}")

        # Check if latest_date is None
        if latest_date is None:
            return jsonify({"error": "No data available."}), 404
        
        # Calculate the date one year ago from the latest date
        one_year_ago = dt.datetime.strptime(latest_date, '%Y-%m-%d') - dt.timedelta(days=365)
        
        # Query for precipitation data
        precip_data = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= one_year_ago).\
            filter(Measurement.date <= latest_date).all()

        logging.debug(f"Precipitation Query Results: {precip_data}")
        
        if not precip_data:
            return jsonify({"error": "No data found"}), 404
        
        # Convert query results to a dictionary
        precip_dict = {date: prcp for date, prcp in precip_data}
        return jsonify(precip_dict)

# Stations route
@app.route("/api/v1.0/stations")
def stations():
    with session_scope() as session:
        results = session.query(Station.station, Station.name).all()
        logging.debug(f"Stations Query Results: {results}")
        
        stations_list = [{station: name} for station, name in results]
        return jsonify(stations_list)

# Temperature observations route
@app.route("/api/v1.0/tobs")
def tobs():
    with session_scope() as session:
        # Find the most active station
        most_active_station = session.query(Measurement.station).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).first()[0]

        logging.debug(f"Most active station: {most_active_station}")

        # Get the latest date and calculate one year ago
        latest_date = session.query(func.max(Measurement.date)).scalar()
        logging.debug(f"Latest date in the dataset: {latest_date}")

        if latest_date is None:
            return jsonify({"error": "No data available."}), 404
        
        one_year_ago = dt.datetime.strptime(latest_date, '%Y-%m-%d') - dt.timedelta(days=365)
        
        # Query for temperature observations
        results = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.station == most_active_station).\
            filter(Measurement.date >= one_year_ago).all()

        logging.debug(f"TOBS Query Results: {results}")
        
        if not results:
            return jsonify({"error": "No data found"}), 404
        
        # Create list of temperature observations
        tobs_list = [{date: tobs} for date, tobs in results]
        return jsonify({
            "most_active_station": most_active_station,
            "recent_temperatures": tobs_list
        })

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start, end=None):
    session = Session(engine)
    
    try:
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')
        end_date = dt.datetime.strptime(end, '%Y-%m-%d') if end else dt.datetime.now()
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD."}), 400
    
    # Log the parsed dates for debugging
    logging.debug(f"Start Date: {start_date}, End Date: {end_date}")

    # Query for temperature statistics
    min_temp = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).scalar()
    
    avg_temp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).scalar()
    
    max_temp = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).scalar()
    
    session.close()
    
    # Log the results for debugging
    logging.debug(f"Min: {min_temp}, Avg: {avg_temp}, Max: {max_temp}")
    
    if min_temp is None or avg_temp is None or max_temp is None:
        return jsonify({"error": "No data found for the given date range."}), 404
    
    return jsonify({
        "Minimum Temperature": min_temp,
        "Average Temperature": avg_temp,
        "Maximum Temperature": max_temp
    })

if __name__ == "__main__":
    app.run(debug=True)