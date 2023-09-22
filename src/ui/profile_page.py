# ProfilePage - Display the Athlete's Profile
#
# This class is responsible for displaying the Athlete's profile. 
#
# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo sasadangelo@gmail.com
#
# This file is part of the Running Data Analysis project.
#
# SPDX-License-Identifier: MIT
import streamlit as st
from src.ui.page import Page

# This class is responsible for displaying the athlete's profile.
# The page will show information like:
# - First name
# - Last name
# - Birth date
# - Gender
# - Location
# - Bio
class ProfilePage(Page):
    # Renders the profile page
    def render(self):
        # the session contains the leogged in athlete
        athlete = st.session_state.logged_in_user

        # if the user is logged we show his information, 
        # otherwise we show a warning message.
        if athlete:
            st.title(athlete.get_first_name() + " " + athlete.get_last_name() + " Profile")

            st.write(f"Welcome, {athlete.get_first_name()} {athlete.get_last_name()}!")
            st.subheader(f"{athlete.get_first_name()} {athlete.get_last_name()} Data:")
            st.write(f"First Name: {athlete.get_first_name()}")
            st.write(f"Last Name: {athlete.get_last_name()}")
            st.write(f"Birth Date: {athlete.get_birth_date()}")
            st.write(f"Gender: {athlete.get_gender()}")
            st.write(f"Location: {athlete.get_location()}")
            st.write(f"Bio: {athlete.get_bio()}")
        else:
            st.warning("You must login to visualize the profile.")





