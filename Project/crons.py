from django_cron import CronJobBase, Schedule
from django.conf import settings
from django.core.files.base import ContentFile
import requests
from datetime import date,datetime, timedelta,timezone
from os  import path,remove
import pandas as pd
from geopy.geocoders import Nominatim
#import classes from models
from mapearthq.models import WorldData,WeeklyCsvFile

class GetWeekly(CronJobBase):
    schedule = Schedule(run_every_mins=720)
    code = "cron.GetWeekly"

    # def hour_elapsed(self):
    #         latest_query = WorldData.objects.last()
    #         days = (datetime.now(timezone.utc) - latest_query.time).days
    #         seconds = (datetime.now(timezone.utc) - latest_query.time).seconds
    #         return (days*12 + seconds//3600)

    def save_csv(self):
        listings = WorldData.objects.order_by('-time')[:30]
        
        dict_list = [{'Magnitude':list.Mag,'latitude':list.lat,
        'longitude':list.lon,'country':list.country,'time':list.time} for list in listings]
        df = pd.DataFrame(dict_list)
        filestr = df.to_string()
        PATH= path.join(settings.MEDIA_ROOT, 'downloadable_csv', 'weekly_data.csv')
        remove(PATH)
        WeeklyCsvFile.objects.all().delete()

        # with open(path,'w+') as f:
        #     f.write(filestr)
        weekly_data = WeeklyCsvFile()    
        weekly_data.csv_file.save('weekly_data.csv',ContentFile(filestr)) 
        weekly_data.save()

    def name_country(self,lat,lon):
            geolocator = Nominatim(user_agent="my_app")
            location = geolocator.reverse(f'{lat},{lon}',language='en')
            #print(location)
            if location is None:
                return None
            country = location.raw.get('address').get('country')
            return country

    def create_data(self):
        df = pd.read_csv('data/data.csv').dropna(
            subset=['place']).sort_values(
                'mag',ascending=False).reset_index(
                    drop=True).head(30)
        obj_row = []
        WorldData.objects.all().delete()
        for i in range(len(df)):
            lat = df.iloc[i]['latitude']
            lon = df.iloc[i]['longitude']
            mag = df.iloc[i]['mag']
            time = df.iloc[i]['time']
            if country:=self.name_country(lat,lon):
                obj_row.append(WorldData(
                    Mag=mag,
                    lat=lat,
                    lon=lon,
                    country=country,
                    time = time
                ))
            else:
                obj_row.append(WorldData(
                    Mag=mag,
                    lat=lat,
                    lon=lon,
                    country=df.iloc[i]['place'],
                    time = time
                ))
        WorldData.objects.bulk_create(obj_row)

    def do(self, *args, **options):
        # if self.hour_elapsed()>24:
        end=datetime.now()
        start = end-timedelta(days=6)

        data = requests.get(f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime={start}&endtime={end}&minmagnitude=4.5')
        #filepath = 'MapEarthQ/data.csv'
        if data.status_code==200:
            with open('data/data.csv', 'w') as writefile:
                writefile.write(data.text)
            self.create_data()
            self.save_csv()

        else:
            print(data.status_code)

class DeleteOldWeekly(CronJobBase):
    schedule = Schedule(run_monthly_on_days=1)
    code = "cron.DeleteOldWeekly"

    def do(self):
        if WorldData.objects.exists():

            querylist = WorldData.objects.all()
            for query in querylist:
                days_passed = (datetime.now(timezone.utc) - query.time).days
                if days_passed>=7:
                    print(f'{query.country} deleted!')
                    query.delete()
                    