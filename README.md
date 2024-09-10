# sqlalchemy-challenge

# Hawaii Climate Analysis and Flask API

# Overview
This project analyzes climate data from Hawaii to understand patterns in temperature and precipitation. The analysis involves preparing the data, calculating statistics, and creating various plots to visualize the results. Additionally, a Flask API is created to allow easy access to the climate data.

# Steps in the Project

# Data Preparation
- **Loaded Data**: Connected to the SQLite database to retrieve the data.
- **Merged Data**: Combined the measurement and station data for further analysis.
- **Data Cleaning**: Checked for missing or duplicate data and ensured data consistency.

# Precipitation Analysis
- **Most Recent Date**: Identified the most recent date in the dataset (August 23, 2017).
- **12-Month Precipitation**: Queried the precipitation data for the last 12 months from the most recent date.
- **Summary Statistics**: Calculated the mean, median, variance, and standard deviation for the precipitation data.
- **Plotting**: Created a line plot to visualize the trend in precipitation over time.

# Station Analysis
- **Station Count**: Calculated the total number of weather stations in the dataset.
- **Most Active Station**: Identified the station with the highest number of observations.
- **Temperature Stats**: Calculated the minimum, average, and maximum temperatures recorded at the most active station.
- **Temperature Observations**: Queried the last 12 months of temperature observations for the most active station and plotted the results as a histogram.

# Flask API
The Flask API provides various routes to access climate data:
- **Homepage (`/`)**: Lists all available API routes.
- **Precipitation (`/api/v1.0/precipitation`)**: Returns the last 12 months of precipitation data in JSON format.
- **Stations (`/api/v1.0/stations`)**: Returns a list of all weather stations in JSON format.
- **TOBS (`/api/v1.0/tobs`)**: Returns the temperature observations of the most active station for the last year in JSON format.
- **Start Date (`/api/v1.0/<start>`)**: Returns the minimum, average, and maximum temperatures from the start date onward.
- **Start-End Date (`/api/v1.0/<start>/<end>`)**: Returns the minimum, average, and maximum temperatures for the given date range.


# Conclusion
This project provides valuable insights into Hawaii's climate patterns, particularly in precipitation and temperature. Additionally, the Flask API enables easy access to climate data for further exploration.

