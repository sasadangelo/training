# ActivityOverviewPage - Display Overview of Running Activities
#
# This class is responsible for displaying an overview of running activities using Streamlit.
# It loads and processes activity data from GPX files, including metrics such as date, name, distance,
# duration, pace, average heart rate, and elevation gain. It also handles the rendering of the data in a table format.
#
# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo sasadangelo@gmail.com
#
# This file is part of the Running Data Analysis project.
#
# SPDX-License-Identifier: MIT
import os
import streamlit as st
import pandas as pd
from src.lib.activity import Activity

# This class is responsible for displaying an overview of running activities using Streamlit.
# It loads and processes activity data from GPX files, including metrics such as date, name, distance,
# duration, pace, average heart rate, and elevation gain. It also handles the rendering of the data in a table format.
class ActivityOverviewPage:
    # Initializes the ActivityOverviewPage and loads running activities from GPX files.
    def __init__(self):
        self.activities = self.__load_activities("gpx")

    # Renders the overview of running activities, displaying the data in a table.
    def render(self):
        st.title("Activities Overview")

        # if there are no activities in the gpx folder a warning message aappears,
        # otherwise a dataframe is created with an overview of all the activities
        # that are displayed on the streamlit page.
        if not self.activities:
            st.warning("No GPX activities found in the 'gpx' folder.")
        else:
            df = self.__create_dataframe()
            self.__display_table(df)

    # Loads running activities from GPX files and processes them into a structured format.
    # Returns a list of lists containing activity data.
    def __load_activities(self, folder):
        activities_data = []

        # for each file in the gpx folder an Activity object is created
        # and added to the activities_data list that will be returned in output
        for filename in os.listdir(folder):
            if filename.endswith('.gpx'):
                file_path = os.path.join(folder, filename)
                try:
                    activity = Activity(file_path)
                    activities_data.append([
                        activity.get_time(),  # Date (without time)
                        activity.get_name(),
                        f'{activity.get_distance():.2f}',
                        self.__seconds_to_hhmmss(activity.get_duration()),
                        self.__seconds_to_mmss(activity.get_average_pace()),
                        activity.get_average_heart_rate(),
                        f'{activity.get_elevation_gain():.1f}'
                    ])
                except Exception as e:
                    print(f"Error: {str(e)}")

        return activities_data

    # Converts seconds to the 'HH:MM:SS' format.
    def __seconds_to_hhmmss(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'

    # Converts seconds to the 'MM:SS' format.
    def __seconds_to_mmss(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f'{int(minutes):02d}:{int(seconds):02d}'

    # Creates a pandas DataFrame from the loaded activity data and performs sorting and formatting.
    def __create_dataframe(self):
        # Create a pandas DataFrame with the data and column headers
        df = pd.DataFrame(self.activities, columns=["Date", "Name", "Distance (Km)", "Duration", "Pace (min/Km)", "Avg HR", "Elev. Gain"])
        
        # Convert the "Date" column to datetime format for sorting
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Extract only the date from the "Date" column
        df['Date'] = df['Date'].dt.date
        
        # Sort the DataFrame based on the "Date" column in descending order
        df = df.sort_values(by='Date', ascending=False)
        
        return df

    # Displays the DataFrame in a Streamlit table format.
    def __display_table(self, df):
        st.table(df.reset_index(drop=True))

