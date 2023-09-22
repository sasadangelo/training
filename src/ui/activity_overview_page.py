# ActivityOverviewPage - Display Athlete's Running Activities
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
import streamlit as st
import pandas as pd
from src.lib.activity import Activity
from src.ui.page import Page

# This class is responsible for displaying an overview of running activities using Streamlit.
# It loads and processes activity data from GPX files, including metrics such as date, name, distance,
# duration, pace, average heart rate, and elevation gain. It also handles the rendering of the data in a table format.
class ActivityOverviewPage(Page):
    # Initializes the ActivityOverviewPage and loads running activities from GPX files.
    def __init__(self, session):
        super().__init__(session)

    # Renders the overview of running activities, displaying the data in a table.
    def render(self):
        st.title("Activities Overview")

        # if there are no activities in the gpx folder a warning message aappears,
        # otherwise a dataframe is created with an overview of all the activities
        # that are displayed on the streamlit page.
        if not self.session.get_logged_in_user():
            st.warning("No GPX activities found in the 'gpx' folder.")
        else:
            df = self.__create_dataframe(self.session.get_logged_in_user().get_activities())
            self.__display_table(df)

    # Creates a pandas DataFrame from the loaded activity data and performs sorting and formatting.
    def __create_dataframe(self, activities):
        # Create a pandas DataFrame with the data and column headers
        df = pd.DataFrame(activities, columns=["Date", "Name", "Distance (Km)", "Duration", "Pace (min/Km)", "Avg HR", "Elev. Gain"])
        
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