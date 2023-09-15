import os
from activity import Activity
from tabulate import tabulate
from datetime import datetime

def seconds_to_mmss(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f'{int(minutes):02d}:{int(seconds):02d}'

def seconds_to_hhmmss(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'

def main():
    folder = 'gpx'

    table_data = []
    headers = ["Date", "Name", "Distance (Km)", "Duration", "Pace (min/Km)", "Max HR", "Avg HR", "Max Cadence", "Avg Cadence", "Elev. Gain", "Elev. Loss"]

    for filename in os.listdir(folder):
        if filename.endswith('.gpx'):
            file_path = os.path.join(folder, filename)
            try:
                activity = Activity(file_path)
                table_data.append([
                    activity.get_activity_time().strftime('%Y-%m-%d'),  # Date (without time)
                    activity.get_name(),
                    f'{activity.get_distance():.2f}',
                    seconds_to_hhmmss(activity.get_duration()),
                    seconds_to_mmss(activity.get_average_pace()),
                    activity.get_max_heart_rate(),
                    activity.get_average_heart_rate(),
                    activity.get_max_cadence(),
                    activity.get_average_cadence(),
                    f'{activity.get_elevation_gain():.1f}',
                    f'{activity.get_elevation_loss():.1f}'
                ])
            except Exception as e:
                print(f"Error: {str(e)}")
    print(tabulate(table_data, headers=headers))

if __name__ == "__main__":
    main()
