#!/bin/bash

# api.openweathermap.org/data/2.5/forecast/city?id=5131321&APPID=abfabebe9f6f95d0bd9bda048799910b
# 5131321
 
YOUR_API_KEY=abfabebe9f6f95d0bd9bda048799910b
YOUR_CITY_ID=5131321
 
temps=`date +%s`;
data=`wget  -q -O - "http://api.openweathermap.org/data/2.5/weather?id=${YOUR_CITY_ID}&appid=${YOUR_API_KEY}&lang=en&units=imperial&lol=$temps" --delete-after`
temperature=`echo ${data} | sed -n 's#.*{"temp":\(.*\),"pressure".*#\1#p'`
temperaturetext=`echo ${data} | sed -n 's#.*"description":"\(.*\)","icon":.*#\1#p'`
if [[ ${temperature} =~ "." ]]; then
  temperature=`expr $(echo "$temperature" |cut -f1 -d\.) + 1`;
fi
 
echo "$temperature" 
echo "$temperaturetext"  
 
#weather files are now in /dev/shm/ for your conky. ;)
#thanks @nazgullien !
