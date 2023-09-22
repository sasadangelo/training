# Athlete - Manage Athlete Profile and Activities
#
# This module defines the Athlete class, which is responsible for managing an athlete's profile
# information and activities.
#
# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo sasadangelo@gmail.com
#
# This file is part of the Running Data Analysis project.
#
# SPDX-License-Identifier: MIT
import os
import csv
from src.lib.activity import Activity

# This class which is responsible for managing an athlete's profile
# information and activities. It loads and stores the athlete's profile data from a profile.csv file,
# as well as their running activities from GPX files. The loaded profile data includes attributes
# such as username, first name, last name, birth date, gender, location, and bio.
class Athlete:
    # This constructor load the athlete profile information and activities
    def __init__(self, username):
        self.username = None
        self.first_name = None
        self.last_name = None
        self.birth_date = None
        self.gender = None
        self.location = None
        self.bio = None
        self.__load_profile(username)
        self.activities = self.__load_activities()

    # This method loads the profile information from the file data/<username>/profile.csv
    def __load_profile(self, username):
        profile_path = os.path.join("data", username, 'profile.csv')
        if os.path.exists(profile_path):
            with open(profile_path, 'r') as profile_file:
                reader = csv.DictReader(profile_file)
                for row in reader:
                    self.username = username
                    self.first_name = row['first_name']
                    self.last_name = row['last_name']
                    self.birth_date = row['birth_date']
                    self.gender = row['gender']
                    self.location = row['location']
                    self.bio = row['bio']

    # This method loads the athlete activities from the gox files in the /<username>/gox folder
    def __load_activities(self):
        activities_data = []
        activities_folder = os.path.join("data", self.username, 'gpx')

        # for each file in the gpx folder an Activity object is created
        # and added to the activities_data list that will be returned in output
        for filename in os.listdir(activities_folder):
            if filename.endswith('.gpx'):
                file_path = os.path.join(activities_folder, filename)
                try:
                    # load the activity from the GPX file
                    activity = Activity(file_path)
                    # append the activity to the list of the athlete activities
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

    # Returns the currently logged-in user.
    def get_activities(self):
        return self.activities

    def get_username(self):
        return self.username

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_birth_date(self):
        return self.birth_date

    def get_gender(self):
        return self.gender

    def get_location(self):
        return self.location

    def get_bio(self):
        return self.bio






