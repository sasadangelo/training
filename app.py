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
import streamlit as st
from src.ui.activity_overview_page import ActivityOverviewPage
from src.ui.profile_page import ProfilePage
from src.ui.session import Session
from streamlit_option_menu import option_menu

def Singleton(cls):
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

# This class is responsible for managing the Streamlit application
# and navigation between different pages. It initializes the initial page, handles page selection,
# and serves as the entry point for running the application.
@Singleton
class TrainingApp:
    # The constructor load all the activities in the gpx folder of the logged in user.
    def __init__(self):
        self.current_page = None
        self.session = Session() 

    # Runs the TrainingApp and initializes the first page as ActivityOverviewPage.
    def run(self):
        self.__create_sidebar_menu()

    # Selects and renders the current page based on user navigation logic.
    def select_page(self, page):
        # Here you can add logic for navigating between different pages.
        # For example, if you want to show the ActivityOverviewPage as the initial page:
        self.current_page = page
        self.current_page.render()

    # Login the input username in the session
    def login(self, username):
        self.session.login(username)

    # Logout the current user from the session
    def logout(self):
        self.session.logout()

    # Get the application session
    def get_session(self):
        return self.session

    # Create the sidebar menu with two options:
    # - Activities, it shows all the athlete's activities
    # - Profile, it shows the athlete's profile
    def __create_sidebar_menu(self):
        with st.sidebar:
            menu_choice = option_menu("Menu", ["Activities", 'Profile'], 
                icons=['list', 'person'], menu_icon="cast", default_index=0)

        # Select the page to show depending on the menu option the user selected
        if menu_choice == "Activities":
            self.select_page(ActivityOverviewPage(self.session))
        elif menu_choice == "Profile":
            self.select_page(ProfilePage(self.session))

if __name__ == "__main__":
    app = TrainingApp()
    app.login("sasadangelo")
    app.run()
