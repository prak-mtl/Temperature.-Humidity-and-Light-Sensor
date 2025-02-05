"""
My First Internet of Things Project - HOME AUTOMATION

Temperature/Humidity Light monitor using Raspberry Pi, DHT11, and photosensor 
Data is displayed at thingspeak.com

Project by Prakhar Mittal and Sandeep Bharghav

"""
# Import all the libraries we need to run
import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import Adafruit_DHT
import urllib2


DEBUG = 1
# Setup the pins we are connect to
RCpin = 24
DHTpin = 23

#Setup our API and delay
myAPI = "LZQ5SCANPN2MQ1D6"
myDelay = 15 #how many seconds between posting data

GPIO.setmode(GPIO.BCM)
GPIO.setup(RCpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def getSensorData():
    RHW, TW = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)
    
    #Convert from Celius to Farenheit
    TWF = 9/5*TW+32
   
    # return dict
    return (str(RHW), str(TW),str(TWF))

def RCtime(RCpin):
    LT = 0
    
    if (GPIO.input(RCpin) == True):
        LT += 1
    return (str(LT))
    
# main() function
def main():
    
    print 'starting...'

    baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
    print baseURL
    
    while True:
        try:
            RHW, TW, TWF = getSensorData()
            LT = RCtime(RCpin)
            f = urllib2.urlopen(baseURL + 
                                "&field1=%s&field2=%s&field3=%s" % (TW, TWF, RHW)+
                                "&field4=%s" % (LT))
            print f.read()
            print TW + " " + TWF+ " " + RHW + " " + LT
            f.close()
            

            sleep(int(myDelay))
        except:
            print 'exiting.'
            break

# call main
if __name__ == '__main__':
    main()