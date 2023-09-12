import os
from activity import Activity

def seconds_to_mmss(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f'{int(minutes):02d}:{int(seconds):02d}'

def seconds_to_hhmmss(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'

def main():
    folder = 'gpx'

    for filename in os.listdir(folder):
        if filename.endswith('.gpx'):
            file_path = os.path.join(folder, filename)
            try:
                activity = Activity(file_path)
                print(f'Metrics for file: {filename}')
                print(f'Activity name: {activity.get_name()}')
                print(f'Activity time: {seconds_to_hhmmss(activity.get_activity_time())}')
                print(f'Average pace (min/Km): {seconds_to_mmss(activity.get_average_pace())}')
                print(f'Distance (Km): {activity.get_distance():.2f}')
                print(f'Average heart rate: {activity.get_average_heart_rate()}')
                print(f'Max heart rate: {activity.get_max_heart_rate()}')
                print(f'Average cadence: {activity.get_average_cadence()}')
                print(f'Max cadence: {activity.get_max_cadence()}')
                print(f'Elevation Gain: {activity.get_elevation_gain():.1f}')
                print(f'Elevation Loss: {activity.get_elevation_loss():.1f}')
                print('-' * 30)
            except Exception as e:
                print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
