import sys, pygame
from pygame.locals import *
import time
import subprocess
import os
import glob
import socket   # to check if on network
#for weather below
import json
from stat import * # ST_SIZE etc
import thread
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"
pygame.init()

def online():
    # are we online?
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('192.168.0.1', 80))
        return ('Online')
    except socket.error as e:
        print "Error on connect: %s" % e
        return ("Offline")
    s.close()

def shutdown():
    # this is mostly event driven so either we need an event or a loop
    # or a thread to actually run
    t = time.strftime('%X')
    t = t[:2]       #just the hour
    if t == '24':
        print ('Shutting down')

def weather():
    file = 'weather.json'
    try:
        f = open(file, 'r')
    except:
        print ('Weather file not found')
    else:
        st = os.stat(file)
        #How long since last upload
        age = time.time() - (st[ST_MTIME])
        t = f.read()
        f.close
    #if age > 1200:  #20 minutes
    #    pass
        #download json file
        #subprocess.call(["ls", "-l"])
        #subprocess.call(["wget  -q -O -" , \
        #"http://api.openweathermap.org/data/2.5/weather?id=5131321&units=imperial&APPID=abfabebe9f6f95d0bd9bda048799910b"\
        # > weather.json], shell = TRUE)\\
    try:
        parsed=json.loads(t)
    except:
        print ('Problem loading weather data')
        return ('.. No Data')
    else:
        t = (parsed['main'])    #temperature
        t = int(t['temp'])
        t = str(t)
        w = (parsed['wind'])    #wind
        w = int(w['speed'])
        w = str(w)
        weather = t + u"\N{DEGREE SIGN}" + "" + w + " mph"
        return (weather)

def checkweather():
    while True:
        thread.start_new_thread(weather,())
        time.sleep(2)
        print ('temp')

def station_list():
    lines = open('playlist.txt', 'r', 444).readlines()
    stations =[]
    for line in lines:
        line = line.rstrip("\n")
        stations.append(line)
    return (stations)

def current_station_name():
    station_number = subprocess.check_output('mpc -f %position%', shell=True)
    station_number = int(station_number[0] ) - 1
    return (station_list()[station_number])

def scan():
    pass

def is_online():
        # connected to the internet?
    IP = subprocess.check_output("hostname -I", shell=True )
    IP=IP[:3]
    if IP =="192":
        # online
        pygame.draw.circle(screen, DARKGREEN, (310, 10), 2, 0)
    else:
        # offline
        pygame.draw.circle(screen, RED, (310, 10), 2, 0)
    pygame.display.flip()


#end_clicks = 0  #Are you sure you want to turn off radio?
def on_click():
    click_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
    # print ("Can't quit'")
    #   Exit
    if 270 <= click_pos[0] <= 320 and 180 <= click_pos[1] <=250:
        print ('Exit routine')
        screen.fill(BLACK)
        pygame.display.update()
        #subprocess.call("mpc stop", shell=False)
        time.sleep(2)
        #sys.exit()
        if 270 <= click_pos[0] <= 320 and 180 <= click_pos[1] <=250:
            refresh_menu_screen()  #refresh the menu interface

    #   Play/Pause
    if 70 <= click_pos[0] <= 120 and 180 <= click_pos[1] <=230:
        x = subprocess.check_output("mpc toggle", shell=True)
        #  x.find returns + or - number for play or pause
        if x.find('[paused') > 0:
            print ('Paused')
            subprocess.call("mpc stop ", shell=True)
            background = pygame.image.load('background.jpg')
            screen.blit(background, (0,0))
            pause=pygame.image.load("play.png")
            screen.blit(pause, (70, 180))
            pygame.display.flip()
        else:
            print ("Playing")
            # clear buffer after pause
            subprocess.call("mpc play ", shell=True)
            play=pygame.image.load("pause.png")
            screen.blit(play, (70, 180))
            pygame.display.flip()
            refresh_menu_screen()

    #   Refresh
    if 270 <= click_pos[0] <= 320 and 5 <= click_pos[1] <=55:
        subprocess.call("mpc stop ", shell=True)
        subprocess.call("mpc play ", shell=True)
        refresh_menu_screen()
    #   Previous
    elif 10 <= click_pos[0] <= 60 and 180 <= click_pos[1] <=230:
        #print ("You pressed button previous")
        subprocess.call("mpc prev ", shell=True)
        refresh_menu_screen()
     #  Next
    elif 130 <= click_pos[0] <= 180 and 180 <= click_pos[1] <=230:
        subprocess.call("mpc next ", shell=True)
        ##subprocess.call("mpc play" + str(pos+1), shell=True)
        refresh_menu_screen()
     #  KZE
    elif 15 <= click_pos[0] <= 67 and 80 <= click_pos[1] <=132:
        print ("Play WKZE")
        subprocess.call("mpc play 1", shell=True)
        refresh_menu_screen()
    #   NYC
    elif 75 <= click_pos[0] <= 127 and 80 <= click_pos[1] <=132:
        subprocess.call("mpc play 5", shell=True)
        refresh_menu_screen()
    #  VKR
    elif 135 <= click_pos[0] <= 187 and 80 <= click_pos[1] <=132:
        subprocess.call("mpc play 7", shell=True)
        refresh_menu_screen()
     #  MHT
    elif 195 <= click_pos[0] <= 247 and 80 <= click_pos[1] <=132:
        subprocess.call("mpc play 2", shell=True)
        refresh_menu_screen()
     #  QXR
    elif 255 <= click_pos[0] <= 307 and 80 <= click_pos[1] <=132:
        subprocess.call("mpc play 3", shell=True)
        refresh_menu_screen()

def refresh_menu_screen(state = 1):     #default to playing
    # Set up the fixed items on the menu
    screen.fill(DARKGREY) #change the colours if needed
    font=pygame.font.Font(None,24)
    title_font=pygame.font.Font(None,34)
    station_font=pygame.font.Font(None,50)  #was 20
    play=pygame.image.load("play.tiff")
    pause=pygame.image.load("pause.png")
    refresh=pygame.image.load("refresh.tiff")
    previous=pygame.image.load("previous.tiff")
    next=pygame.image.load("next.tiff")
    exit=pygame.image.load("exit.png")

    # Draw main elements.. Start with pause not play
    #screen.blit(play,(70,180))  #(20,80)
    screen.blit(pause,(70,180))
    pygame.draw.rect(screen, RED, (8, 70, 304, 108),1)
    pygame.draw.line(screen, RED, (8,142),(310,142),1)
    pygame.draw.rect(screen, BLACK, (10, 143, 300, 33),0)
    screen.blit(refresh,(270,5))  #270,70
    screen.blit(previous,(10,180))
    screen.blit(next, (130,180))  #70, 180
    screen.blit(exit, (265,185))  #270,5 or 270, 180

    # Favorite stations
    wkze=pygame.image.load("wkze.png")
    wvkr=pygame.image.load("wvkr.png")
    wmht=pygame.image.load("wmht.png")
    wqxr=pygame.image.load("wqxr.png")
    wvkr=pygame.image.load("wvkr.png")
    wnyc=pygame.image.load("wnyc.png")
    #wamc=pygame.image.load("wamc.png")

    # x positions 15, 75, 135, 195, 255
    screen.blit(wkze, (15,80))
    screen.blit(wnyc, (75,80))
    screen.blit(wvkr, (135,80))
    screen.blit(wmht, (195, 80))
    screen.blit(wqxr, (255,80))

    pygame.draw.rect(screen, DARKGREEN, (0,0,320,240),1)

    #   Print station Name
    name = current_station_name()
    station_name = station_font.render(name, 1, (RED))
    print ("Station is:" ,name)
    screen.blit(station_name,(12,6))   #13,145
    #screen.blit("Station", (12,6))
    is_online()

        #  Weather and date
    wthr= weather()
    date = time.ctime()[:11]
    msg = date + ',' + wthr
    label=font.render(msg, 1, (RED))
    screen.blit(label,(20,150))
    pygame.display.flip()

# ************************************************Main Loop **************
def main():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                #print "screen pressed" #for debugging purposes
                on_click()

#ensure there is always a safe way to end the program if the touch screen fails

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
    time.sleep(0.2)
    pygame.display.update()


#########################  Setup ####################
#set size of the screen
size = width, height = 320, 240
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(False)
subprocess.call("mpc play ", shell=True)         # start with radio on
number_of_stations = len(station_list())
stations = station_list()
BLUE = 26, 0, 255
CREAM = 254, 255, 25
BLACK = 0, 0, 0
DARKGREY = 37, 37, 37
WHITE = 255, 255, 255
YELLOW = 255, 255, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
DARKGREEN = 0, 128, 0

refresh_menu_screen()  #refresh the menu interface
# Download weather on startup if file is older than an hour
#wget  -q -O - "http://api.openweathermap.org/data/2.5/weather?id=5131321&units=imperial&APPID=abfabebe9f6f95d0bd9bda048799910b"


main() #check for key presses and start emergency exit
