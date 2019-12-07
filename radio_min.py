#import sys
import time
import subprocess
import os
#import glob
#from stat import * # ST_SIZE etc
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"
"""
"""
def station_list():
    lines = open('playlist.txt', 'r', 444).readlines()
    stations =[]
    for line in lines:
        line = line.rstrip("\n")
        stations.append(line)
    return (stations)


subprocess.call("mpc play ", shell=True)         # start with radio on
number_of_stations = len(station_list())
stations = station_list()
print ("\n")


for station in stations:
    """ Scroll thru stations

    Station number is for mpc, station for display
    """
    n = stations.index(station) + 1
    print (n, station)
    #subprocess.run("mpc next ", shell = True)
    subprocess.call("mpc play "+ str(n), shell = True)
    print ("\n")
    time.sleep(3)
