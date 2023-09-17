# TrainingApp - Manage Streamlit Application and Navigation
#
# This file defines the TrainingApp class, which is responsible for managing the Streamlit application
# and navigation between different pages. It initializes the initial page, handles page selection,
# and serves as the entry point for running the application.
#
# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo sasadangelo@gmail.com
#
# This file is part of the Running Data Analysis project.
#
# SPDX-License-Identifier: MIT
from src.ui.activity_overview_page import ActivityOverviewPage

# This class is responsible for managing the Streamlit application
# and navigation between different pages. It initializes the initial page, handles page selection,
# and serves as the entry point for running the application.
class TrainingApp:
    # The constructor load all the activities in the gpx folder.
    def __init__(self):
        self.current_page = None

    # Runs the TrainingApp and initializes the current page.
    def run(self):
        self.current_page = ActivityOverviewPage()
        self.select_page()

    # Selects and renders the current page based on user navigation logic.
    def select_page(self):
        # Here you can add logic for navigating between different pages.
        # For example, if you want to show the ActivityOverviewPage as the initial page:
        self.current_page = ActivityOverviewPage()
        self.current_page.render()

if __name__ == "__main__":
    app = TrainingApp()
    app.run()
