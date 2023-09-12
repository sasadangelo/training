import gpxpy
import pandas as pd

data = {
    'latitude': [],
    'longitude': [],
    'time': [],
    'elevation': [],
    'hr': [],
    'cadence': []
}

class Activity:
    def __init__(self, file_path):
        self.file_path = file_path
        self.activity_time = None
        self.distance = None
        self.average_pace = None
        self.average_heart_rate = None
        self.max_heart_rate = None
        self.elevation_gain = None
        self.elevation_loss = None
        self.average_cadence = None
        self.max_cadence = None

        df = pd.DataFrame(data)

        try:
            with open(file_path, 'r') as gpx_file:
                gpx = gpxpy.parse(gpx_file)

            self.activity_type = gpx.link_type
            self.activity_time = gpx.get_duration()
            self.distance = gpx.length_3d() / 1000
            self.average_pace = self.activity_time / self.distance

            total_hr = 0
            count_hr = 0
            
            total_cadence = 0
            count_cadence = 0

            previous_elevation = None
            
            for track in gpx.tracks:
                self.activity_name = track.name
                for segment in track.segments:
                    for point in segment.points:
                        if point.extensions is not None:
                            heart_rate = int(point.extensions[0][0].text)
                            cadence = int(point.extensions[0][1].text)*2
                            total_hr += heart_rate
                            total_cadence += cadence
                            count_hr+=1
                            count_cadence+=1
                            if self.max_heart_rate == None:
                                self.max_heart_rate = heart_rate
                            elif self.max_heart_rate < heart_rate:
                                self.max_heart_rate = heart_rate
                            if self.max_cadence == None:
                                self.max_cadence = cadence
                            elif self.max_cadence < cadence:
                                self.max_cadence = cadence
                        if point.has_elevation():
                            elevation = point.elevation
                            df.loc[len(df), 'elevation'] = elevation
                            #print("Elevation: ", elevation)
                            if previous_elevation is not None:
                                if elevation >= previous_elevation:
                                    if self.elevation_gain is None:
                                        self.elevation_gain = elevation - previous_elevation
                                    else:
                                        self.elevation_gain += elevation - previous_elevation
                                else:
                                    if self.elevation_loss is None:
                                        self.elevation_loss = previous_elevation - elevation
                                    else:
                                        self.elevation_loss += previous_elevation - elevation
                            previous_elevation = elevation

            if count_hr > 0:
                self.average_heart_rate=int(total_hr/count_hr)
            if count_cadence > 0:
                self.average_cadence=int(total_cadence/count_cadence)
            #print(df['elevation'].max())

        except Exception as e:
            raise Exception(f"Error while reading GPX file '{file_path}': {str(e)}")

    def get_name(self):
        return self.activity_name

    def get_activity_time(self):
        return self.activity_time

    def get_distance(self):
        return self.distance

    def get_average_pace(self):
        return self.average_pace

    def get_average_heart_rate(self):
        return self.average_heart_rate

    def get_max_heart_rate(self):
        return self.max_heart_rate

    def get_average_cadence(self):
        return self.average_cadence

    def get_max_cadence(self):
        return self.max_cadence

    def get_elevation_gain(self):
        return self.elevation_gain

    def get_elevation_loss(self):
        return self.elevation_loss
