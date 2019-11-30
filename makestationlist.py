import subprocess

def station_list():
    
 # build a dict of stations from playlist.txt
    values=[]
    stations={}

    lines = open('playlist.txt', 'r').readlines()
    print (lines)
    for line in lines:
        for line in lines:
            line = line.rstrip("\n")
            values.append(line)
     
    keys = range((len(values)))
     
    for i in keys:
        stations[i+1] = values[i]
    return (stations)

def get_current_station():
    station = subprocess.check_output('mpc -f %position%', shell=True)
    return(station)


#######################################################

current_station = int(get_current_station()[0])
stations = station_list()     # dict
print (stations[current_station])
