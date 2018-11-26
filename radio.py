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
        
# weather
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
    # build a dict of stations from playlist.txt
    values=[]
    stations={}

    lines = open('playlist.txt', 'r', 444).readlines()
    for line in lines:
        for line in lines:
            line = line.rstrip("\n")
            values.append(line)
     
    keys = range((len(values)))
     
    for i in keys:
        stations[i+1] = values[i]

    return (stations)
    
def get_current_station():
        # get playlist position from mpc
    station = subprocess.check_output('mpc -f %position%', shell=True)
        # and return it's number
    return(station[0])

def is_online():
        # connected to the internet?
    IP = subprocess.check_output("hostname -I", shell=True )
    IP=IP[:3]
    if IP =="192":
        # online
        pygame.draw.circle(screen, darkgreen, (310, 10), 2, 0)
    else:
        # offline
        pygame.draw.circle(screen, red, (310, 10), 2, 0)
    pygame.display.flip()


#end_clicks = 0  #Are you sure you want to turn off radio?
def on_click():
    click_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
    # print ("Can't quit'")
    '''
    if 270 <= click_pos[0] <= 320 and 180 <= click_pos[1] <=250:
        #global end_clicks
        #end_clicks = end_clicks +1
        #print (end_clicks)
        
        screen.fill(black)
        subprocess.call("mpc pause", shell=True)
        # restart
        if 0 <= click_pos[0] <= 320 and 0 <= click_pos[1] <=240:
            print ('Restarting')
            subprocess.call("mpc play", shell=True)
            refresh_menu_screen()
            
        
        
        #   Shutdown on 2 clicks
        if end_clicks == 2:
            print ("Shutting Down !")
            screen.fill(black)
            restart=pygame.image.load("play.png")
            screen.blit(restart, (70, 180))
            subprocess.call("mpc stop", shell=True)
            #subprocess.call("clear", shell=True)
            #sys.exit()
            #subprocess.call("shutdown -h now >/dev/null", shell=True)
            if 70 <= click_pos[0] <= 120 and 180 <= click_pos[1] <=230:
                subprocess.call("mpc play", shell=True)
                refresh_menu_screen()
        else:    
            screen.fill(black)
            font=pygame.font.Font(None, 36)
            label=font.render("Press  to shut down", 1, (red))
            screen.blit(label,(10,90))
            exit=pygame.image.load("exit.png")
            screen.blit(exit, (265,185))
            pygame.display.flip()
            time.sleep(5)
            refresh_menu_screen()
            #sys.exit()
    '''
    #   Exit
    if 270 <= click_pos[0] <= 320 and 180 <= click_pos[1] <=250:
        print ('Exit routine')
        screen.fill(black)
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
            #screen.fill(black)
            #pygame.display.update()
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
        pos = int(get_current_station())
        end_of_list = len(stations)
        print (pos, end_of_list)
        if pos <= end_of_list:
            subprocess.call("mpc next ", shell=True)
            #subprocess.call("mpc play" + str(pos+1), shell=True)
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
    screen.fill(darkgrey) #change the colours if needed
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
    pygame.draw.rect(screen, red, (8, 70, 304, 108),1)
    pygame.draw.line(screen, red, (8,142),(310,142),1)
    pygame.draw.rect(screen, black, (10, 143, 300, 33),0)
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
    
    pygame.draw.rect(screen, darkgreen, (0,0,320,240),1)
    
    number = int(get_current_station())
    name = (stations[number])
    station_name = station_font.render(name, 1, (red))
 
    
    #additional_data = title_font.render(statn()[2], 1, (blue))
    screen.blit(station_name,(12,6))   #13,145
    #screen.blit(additional_data,(12,45)) #12, 160

    is_online()
    
        #  Weather and date
    wthr= weather()
    date = time.ctime()[:11]
    msg = date + ',' + wthr
    label=font.render(msg, 1, (red))
    screen.blit(label,(20,150))
    pygame.display.flip()

# ************************************************Main Loop **************
def main():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                #print "screen pressed" #for debugging purposes
                pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
                #print pos #for checking
                #pygame.draw.circle(screen, white, pos, 2, 0) #for debugging purposes - adds a small dot where the screen is pressed
                on_click()

#ensure there is always a safe way to end the program if the touch screen fails

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
    time.sleep(0.2)        
    pygame.display.update()


#################### EVERTHING HAS NOW BEEN DEFINED ###########################

#set size of the screen
size = width, height = 320, 240
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(False)
subprocess.call("mpc play ", shell=True)         # start with radio on
blue = 26, 0, 255
cream = 254, 255, 25
black = 0, 0, 0
darkgrey = 37, 37, 37
white = 255, 255, 255
yellow = 255, 255, 0
red = 255, 0, 0
green = 0, 255, 0
darkgreen = 0, 128, 0
stations = station_list()   
refresh_menu_screen()  #refresh the menu interface
# Download weather on startup if file is older than an hour
#wget  -q -O - "http://api.openweathermap.org/data/2.5/weather?id=5131321&units=imperial&APPID=abfabebe9f6f95d0bd9bda048799910b"

 
main() #check for key presses and start emergency exit


