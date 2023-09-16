# Activity Class - Manage Running Workout Data
#
# This module defines the Activity class, which is responsible for managing data related to running workouts.
# It provides methods to extract and analyze data from GPX files, including metrics like duration, distance, pace,
# elevation gain and loss, heart rate, and cadence.
#
# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo sasadangelo@gmail.com
#
# This file is part of the Running Data Analysis project.
#
# SPDX-License-Identifier: MIT
import gpxpy
import pandas as pd
from elevation import CumulativeElevationCalculator


# Represents a single running workout and manages associated data, including:
# - Workout Duration
# - Total Distance Covered
# - Average Pace
# - Elevation Gain and Loss (if terrain data is available in the GPX file)
# - Heart Rate (hr) and Cadence (if data is available in the GPX file)
# 
# Additionally, it stores a stream of data samples consisting of:
# - Latitude and Longitude
# - Timestamp
# - Elevation (if available)
# - Heart Rate (if available)
# - Cadence (if available)
# 
# This class is designed to handle and analyze individual running activities.
class Activity:
    def __init__(self, file_path):
        # Initialize the file path for the GPX file
        self.file_path = file_path
        # The activity_data attribute contains a tabular DataFrame with columns for latitude, longitude, time, 
        # and elevation. Additionally, if heart rate (hr) and cadence data are available in the GPX file, those 
        # columns are also included in the DataFrame. This tabular data is structured for various calculations 
        # and analysis related to the activity recorded in the GPX file. The DataFrame is dynamic and adapts 
        # to the presence of data in the GPX file, including optional hr and cadence information.
        self.activity_data = None
        
        # Initialize attributes for various activity metrics
        self.activity_time = None
        self.duration = None
        self.distance = None
        self.average_pace = None
        self.average_heart_rate = None
        self.max_heart_rate = None
        self.elevation_gain = None
        self.elevation_loss = None
        self.average_cadence = None
        self.max_cadence = None

        # Initialize an elevation calculator with the default CumulativeElevationCalculator
        # Various elevation gain and loss calculation strategies are available in elevation.py
        # Programmers can choose different techniques by using alternative classes from that file
        elevation_calculator = CumulativeElevationCalculator()

        try:
            # Open and parse the GPX file
            with open(file_path, 'r') as gpx_file:
                gpx = gpxpy.parse(gpx_file)

            # Extract key metrics for the workout, including activity type, duration, distance, and average pace
            self.activity_type = gpx.link_type
            self.duration = gpx.get_duration()
            self.distance = gpx.length_3d() / 1000
            self.average_pace = self.duration / self.distance
 
            # The goal with this piece of code is to create a DataFrame containing essential columns like longitude, 
            # latitude, and time. Optionally, if available in the GPX file, columns for elevation, cadence, and HR are 
            # added. Since DataFrames don't support dynamic column addition, we construct a list of data points
            # containing only available data. Finally, we convert the list of objects into a DataFrame,
            # resulting in a tabular data structure with only the available columns.
            activity_data = []
            for track in gpx.tracks:
                self.activity_name = track.name
                for segment in track.segments:
                    for point in segment.points:
                        data_point = {
                            'latitude': point.latitude,
                            'longitude': point.longitude,
                            'time': point.time
                        }
                        if point.has_elevation():
                            data_point['elevation'] = point.elevation
                        if point.extensions is not None and len(point.extensions) > 0:
                            data_point['hr'] = int(point.extensions[0][0].text)
                            data_point['cadence'] = int(point.extensions[0][1].text) * 2

                        activity_data.append(data_point)
            self.activity_data = pd.DataFrame(activity_data)

            # The activity_time attribute stores the timestamp of the initial data point captured during the 
            # workout session. This timestamp represents the starting time of the activity, as recorded in the 
            # GPX file. It is the time at which the workout session commenced.            
            self.activity_time = self.activity_data['time'].iloc[0]

            # Once the activity_data DataFrame is available, computing average and maximum values for
            # 'hr' (heart rate) and 'cadence' becomes straightforward. We use the mean() and max() functions
            # provided by DataFrames to calculate the average and maximum values for these columns.
            if not self.activity_data.empty:
                if 'hr' in self.activity_data.columns:
                    self.average_heart_rate = int(round(self.activity_data['hr'].mean()))
                    self.max_heart_rate = self.activity_data['hr'].max()
                if 'cadence' in self.activity_data.columns:
                    self.average_cadence = int(round(self.activity_data['cadence'].mean()))
                    self.max_cadence = self.activity_data['cadence'].max()

            # To calculate elevation gain and loss, we first extract the 'elevation' column from the activity_data DataFrame.
            # Then, we remove rows with missing elevation data using dropna(). Finally, we calculate elevation gain and loss
            # using the selected elevation calculator strategy (elevation_calculator.calculate()).
            elevation_data = self.activity_data[['elevation']].dropna()
            self.elevation_gain, self.elevation_loss = elevation_calculator.calculate(elevation_data)

        except Exception as e:
            # Raise an exception if there's an error while reading the GPX file
            raise Exception(f"Error while reading GPX file '{file_path}': {str(e)}")

    def get_activity_time(self):
        return self.activity_time

    def get_name(self):
        return self.activity_name

    def get_activity_data(self):
        return self.activity_data
    
    def get_duration(self):
        return self.duration

    def get_distance(self):
        return self.distance

    def get_average_pace(self):
        return self.average_pace

    def get_average_heart_rate(self):
        return self.average_heart_rate

    def get_max_heart_rate(self):
        return self.max_heart_rate

    def get_average_cadence(self):
        return self.average_cadence

    def get_max_cadence(self):
        return self.max_cadence

    def get_elevation_gain(self):
        return self.elevation_gain

    def get_elevation_loss(self):
        return self.elevation_loss

    def set_elevation_calculator(self, elevation_calculator):
        self.elevation_calculator = elevation_calculator