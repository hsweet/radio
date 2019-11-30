#import urllib.request  #needs python 3
import json
import os
from stat import * # ST_SIZE etc

(last_update, oldtime) =(0,0)

# Download weather once an hour to file
key  = 'abfabebe9f6f95d0bd9bda048799910b'
city = '5131321'
#url = 'http://api.openweathermap.org/data/2.5/forecast/city?id=5131321&APPID=abfabebe9f6f95d0bd9bda048799910b'

url = "http://api.openweathermap.org/data/2.5/weather?id=5131321&units=imperial&APPID=abfabebe9f6f95d0bd9bda048799910b"
file = 'weather.json'

st = os.stat(file)
last_update = (st[ST_MTIME])

if oldtime < last_update:
    print ('new info')

oldtime = last_update
print (oldtime, last_update)

def getweather():
    f = open(file, 'r')
    w = f.read() 
    f.close
    return t

# Download the weather, but not too frequently    
#x = urllib.request.urlopen(url)  
#print(x.read())
f = open(file, 'r')
t = f.read() 
f.close
    
#print (t)
parsed=json.loads(t)
weather = (parsed['main'])
wind = (parsed['wind'])
print (wind)
print (int(weather['temp']))
print (wind['speed'])

# print (int(weather ['temp_max']))

# get Pine Bush Weather..
# wget  -q -O - "http://api.openweathermap.org/data/2.5/weather?id=5131321&units=imperial&APPID=abfabebe9f6f95d0bd9bda048799910b"


# wget  -q -O - "http://api.openweathermap.org/data/2.5/forecast/city?id=5131321&APPID=abfabebe9f6f95d0bd9bda048799910b"

 
#  wget  -q -O - "http://api.openweathermap.org/data/2.5/weather?id=5131321&APPID=abfabebe9f6f95d0bd9bda048799910b"
# wget  -q -O - "http://api.openweathermap.org/data/2.5/weather?id=5131321&units=imperial&APPID=abfabebe9f6f95d0bd9bda048799910b"

