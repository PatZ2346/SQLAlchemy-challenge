# SQLAlchemy Climate Analysis and API (SurfsUp)  
  
## Overview  
This project performs a climate analysis of Honolulu, Hawaii, using SQLAlchemy, Pandas, Matplotlib, and Flask. The analysis includes precipitation and temperature data exploration followed by designing a Flask API to provide this climate data.  
  
### Setup Instructions  
1. Prerequisites  
2. Python 3.6+  
3. Virtual Environment (optional but recommended)  
  
### Precipitation Analysis  
* Most Recent Date: Identify the most recent date in the dataset.  
  
* Previous 12 Months of Data: Retrieve and plot the last 12 months of precipitation data.  
  
* Summary Statistics: Display summary statistics for the precipitation data.  
  
### Station Analysis  
* Total Number of Stations: Query the total number of stations in the dataset.  
  
* Most-Active Stations: List stations by observation count in descending order.  
  
* Temperature Stats: Calculate the minimum, maximum, and average temperatures for the most active station.  
  
* Histogram: Plot a histogram of the last 12 months of temperature observations for the most active station.  
  
### Flask  
Available Routes  
1. Homepage: /  
* Lists all available routes.  
  
2. Precipitation Data: /api/v1.0/precipitation  
* Returns the previous 12 months of precipitation data as a JSON dictionary.  
  
3. Station Data: /api/v1.0/stations  
* Returns a JSON list of all stations in the dataset.  
  
4. Temperature Observations (tobs): /api/v1.0/tobs  
* Returns the dates and temperature observations of the most active station for the previous year.  
  
5. Temperature Stats for a Date Range: /api/v1.0/<start> - /api/v1.0/<start>/<end>  
* Returns the minimum, average, and maximum temperatures for a specified start date or a specified start-end range.  
  
### Running the Flask App
* Start the Flask Server  
* Example API Calls:   
1. Precipitation Data:  
http://127.0.0.1:5000/api/v1.0/precipitation  
  
2. Stations Data:  
http://127.0.0.1:5000/api/v1.0/stations  
  
3. Temperature Observations (tobs):  
http://127.0.0.1:5000/api/v1.0/tobs  
  
4. Temperature Stats for a Date Range:  
http://127.0.0.1:5000/api/v1.0/2017-08-23  
http://127.0.0.1:5000/api/v1.0/2017-08-23/2017-09-23  