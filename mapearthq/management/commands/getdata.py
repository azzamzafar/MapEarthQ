import requests
from datetime import date, datetime, timedelta
import csv
from geopy.geocoders import Nominatim
#import classes from models
from mapearthq.models import WorldData
#make this file a command for django using manage.py
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):

        end=date.today()
        self.stdout.write(str(end))
        start = end-timedelta(days=7)
        #self.stdout.write(type(start))

        data = requests.get(f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime={start}&endtime={end}&minmagnitude=4.5')
        #filepath = 'MapEarthQ/data.csv'
        with open('data.csv', 'w') as writefile:
            writefile.write(data.text)

        def name_country(lat,lon):
            geolocator = Nominatim(user_agent="my_app")
            location = geolocator.reverse(f'{lat},{lon}',language='en')
            #print(location)
            if location is None:
                return None
            country = location.raw.get('address').get('country')
            return country



        WorldData.objects.all().delete()

        with open('data.csv', 'r') as datafile:
            csvreader=csv.reader(datafile)
            header=next(csvreader)
            self.stdout.write(str([header[0],header[1],header[2],header[4]]))
            i=0
            newrow=[]
            for row in csvreader:
                if i==10:
                    break

                time=row[0]
                lat=row[1]
                lon=row[2]
                mag=row[4]
                country=name_country(lat,lon)
                if country is None:
                    continue
                else:
                    
                    #newrow=[row[0],row[1],row[2],row[4],country]
                    newrow.append(
                        WorldData(Mag=mag,lat=lat,lon=lon,country=country,time=time)
                        )
                    self.stdout.write(str(newrow))

                i+=1
            WorldData.objects.bulk_create(newrow)
        
