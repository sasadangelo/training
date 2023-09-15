# Elevation Module - Elevation Gain/Loss Calculation Strategies
#
# This module defines various strategies for calculating elevation gain and loss in running workouts.
# It provides implementations of different elevation calculation algorithms, including cumulative elevation
# and threshold-based elevation gain/loss calculations.
#
# Copyright (c) 2023 Salvatore D'Angelo
# Maintainer: Your Name sasadangelo@gmail.com
#
# This file is part of the Running Data Analysis project.
#
# SPDX-License-Identifier: MIT

# ElevationCalculator Interface - Defines methods for calculating elevation gain and loss.
# Multiple strategies for elevation gain/loss calculation are available, and this interface serves
# as a common interface for all of them. Programmers can choose the strategy that best fits their requirements.
class ElevationCalculator:
    def calculate(self, elevation_data):
        pass

# CumulativeElevationCalculator Class - Implements elevation gain and loss calculation by comparing elevation
# data point by point and summing the positive differences as gain and the negative differences as loss.
#
# This calculation method is straightforward: for each elevation data point, it computes the difference between
# the elevation at that point and the previous one. Positive differences are accumulated as elevation gain,
# while negative differences are accumulated as elevation loss. While this method is simple and easy to implement,
# it may produce inflated values, particularly on flat terrains, due to background noise in elevation data.
#
# Use this method when a basic and straightforward elevation gain/loss calculation is sufficient.
class CumulativeElevationCalculator(ElevationCalculator):
    def calculate(self, elevation_data):
        if 'elevation' in elevation_data.columns:
            elevation_values = elevation_data['elevation'].tolist()
            if elevation_values:
                elevation_gain = 0
                elevation_loss = 0
                previous_elevation = elevation_values[0]

                for elevation in elevation_values[1:]:
                    if elevation > previous_elevation:
                        elevation_gain += elevation - previous_elevation
                    elif elevation < previous_elevation:
                        elevation_loss += previous_elevation - elevation

                    previous_elevation = elevation

                return elevation_gain, elevation_loss
        return None, None

# ThresholdElevationCalculator Class - Implements elevation gain and loss calculation while considering a
# user-defined threshold. Elevations below the threshold are excluded from calculations.
#
# This calculator improves upon the cumulative elevation calculation method by introducing a threshold value.
# It effectively filters out minor elevation fluctuations, reducing the impact of noise in elevation data.
# Elevations below the threshold are considered insignificant and are not counted towards elevation gain or loss.
# This approach is useful in scenarios where elevation data may contain considerable noise or variations in flat terrains.
#
# Usage: Create an instance of this class with a specified threshold value and use it for elevation calculations.
class ThresholdElevationCalculator(ElevationCalculator):
    def __init__(self, threshold):
        self.threshold = threshold

    def calculate(self, elevation_data):
        if 'elevation' in elevation_data.columns:
            elevation_values = elevation_data['elevation'].tolist()
            if elevation_values:
                elevation_gain = max(0, sum(max(0, elevation_values[i] - elevation_values[i - 1]) if elevation_values[i] - elevation_values[i - 1] > self.threshold else 0 for i in range(1, len(elevation_values))))
                elevation_loss = max(0, sum(max(0, elevation_values[i - 1] - elevation_values[i]) if elevation_values[i - 1] - elevation_values[i] > self.threshold else 0 for i in range(1, len(elevation_values))))
                return elevation_gain, elevation_loss
        return None, None
