# Session - Manage user session
#
# This module defines the Session class, which represents a user session within the application.
#
# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo sasadangelo@gmail.com
#
# This file is part of the Running Data Analysis project.
#
# SPDX-License-Identifier: MIT
from src.lib.athlete import Athlete 

# This class represents a user session within the application.
# It manages user login and logout and keeps track of the currently logged-in user.
class Session:
    # Initializes the logged-in user as None at the start of the session.
    def __init__(self):
        self.logged_in_user = None

    # Performs user login by setting the logged-in user with the specified username.
    def login(self, username):
        self.logged_in_user = Athlete(username)

    # Performs user logout by resetting the logged-in user to None.
    def logout(self):
        self.logged_in_user = None

    # Returns the currently logged-in user.
    def get_logged_in_user(self):
        return self.logged_in_user
