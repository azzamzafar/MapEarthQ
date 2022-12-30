from django_cron import CronJobBase, Schedule
import requests
from datetime import date,datetime, timedelta,timezone
import pandas as pd
from geopy.geocoders import Nominatim
#import classes from models
from mapearthq.models import WorldData


class GetWeekly(CronJobBase):
    schedule = Schedule(run_every_mins=720)
    code = "cron.GetWeekly"
    
    def do(self, *args, **options):
        
        # def hour_elapsed(self):
        #     latest_query = WorldData.objects.last()
        #     days = (datetime.now(timezone.utc) - latest_query.time).days
        #     seconds = (datetime.now(timezone.utc) - latest_query.time).seconds
        #     return (days*12 + seconds//3600)

        def name_country(lat,lon):
            geolocator = Nominatim(user_agent="my_app")
            location = geolocator.reverse(f'{lat},{lon}',language='en')
            #print(location)
            if location is None:
                return None
            country = location.raw.get('address').get('country')
            return country

        def create_data():
            df = pd.read_csv('data.csv').dropna(
                subset=['place']).sort_values(
                    'mag',ascending=False).reset_index(
                        drop=True).head(10)
            obj_row = []

            for i in range(len(df)):
                lat = df.iloc[i]['latitude']
                lon = df.iloc[i]['longitude']
                mag = df.iloc[i]['mag']
                time = df.iloc[i]['time']
                if country:=name_country(lat,lon):
                    print(country)
                    obj_row.append(WorldData(
                        Mag=mag,
                        lat=lat,
                        lon=lon,
                        country=country,
                        time = time
                    ))
                else:
                    print(df.iloc[i]['place'])
                    obj_row.append(WorldData(
                        Mag=mag,
                        lat=lat,
                        lon=lon,
                        country=df.iloc[i]['place'],
                        time = time
                    ))
            WorldData.objects.bulk_create(obj_row)

        # if self.hour_elapsed()>24:
        end=datetime.now()
        start = end-timedelta(days=7)

        data = requests.get(f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime={start}&endtime={end}&minmagnitude=4.5')
        #filepath = 'MapEarthQ/data.csv'
        if data.status_code==200:
            with open('data.csv', 'w') as writefile:
                writefile.write(data.text)
            create_data()
        else:
            print(data.status_code)
class DeleteOldWeekly(CronJobBase):
    schedule = Schedule(run_monthly_on_days=1)
    code = "cron.DeleteOldWeekly"

    def do(self):
        querylist = WorldData.objects.all()
        for query in querylist:
            days_passed = (datetime.now(timezone.utc) - query.time).days
            if days_passed>=7:
                print(f'{query.country} deleted!')
                query.delete()
                  