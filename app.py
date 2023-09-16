# Activities Overview
#
# This script loads and displays running activity data from GPX files in a tabular format using Streamlit.
# It extracts and presents information such as date, name, distance, duration, pace, average heart rate, and elevation gain.
#
# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo sasadangelo@gmail.com
#
# This script is part of the Running Data Analysis project.
#
# SPDX-License-Identifier: MIT
import os
import streamlit as st
from activity import Activity
from datetime import datetime
import pandas as pd

# Convert seconds to a string in 'MM:SS' format.
# Args:
#     seconds (int): The number of seconds to be converted.
# Returns:
#     str: A string representing the time in 'MM:SS' format.
def seconds_to_mmss(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f'{int(minutes):02d}:{int(seconds):02d}'

# Convert seconds to a string in 'HH:MM:SS' format.
# Args:
#     seconds (int): The number of seconds to be converted.
# Returns:
#     str: A string representing the time in 'HH:MM:SS' format.
def seconds_to_hhmmss(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'

# Load GPX files as Activity objects and extract relevant data.
# Args:
#     folder (str): The path to the folder containing GPX files.
# Returns:
#     list: A list of lists, each containing activity data extracted from GPX files as Activity objects.
#          The data includes date, name, distance, duration, pace, average heart rate, and elevation gain.
def load_activities(folder):
    activities_data = []

    for filename in os.listdir(folder):
        if filename.endswith('.gpx'):
            file_path = os.path.join(folder, filename)
            try:
                activity = Activity(file_path)
                activities_data.append([
                    activity.get_activity_time(),  # Date (without time)
                    activity.get_name(),
                    f'{activity.get_distance():.2f}',
                    seconds_to_hhmmss(activity.get_duration()),
                    seconds_to_mmss(activity.get_average_pace()),
                    activity.get_average_heart_rate(),
                    f'{activity.get_elevation_gain():.1f}'
                ])
            except Exception as e:
                print(f"Error: {str(e)}")
    
    return activities_data

# Launches a Streamlit app to display an overview of workouts.
# Args:
#     None
# Returns:
#     None
def main():
    st.title("Activities Overview")

    folder = 'gpx'
    activities = load_activities(folder)

    if not activities:
        st.warning("No GPX activities found in the 'gpx' folder.")
    else:
        # Create a pandas DataFrame with the data and column headers
        df = pd.DataFrame(activities, columns=["Date", "Name", "Distance (Km)", "Duration", "Pace (min/Km)", "Avg HR", "Elev. Gain"])
        
        # Convert the "Date" column to datetime format for sorting
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Extract only the date from the "Date" column
        df['Date'] = df['Date'].dt.date
        
        # Sort the DataFrame based on the "Date" column in descending order
        df = df.sort_values(by='Date', ascending=False)
        
        # Display the DataFrame with Streamlit without cluttering the numerical index
        st.table(df.reset_index(drop=True))

if __name__ == "__main__":
    main()
