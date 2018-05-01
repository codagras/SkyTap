# Author: Coltin Grasmick
# Date: 30/04/2018
# Purpose: Intercept 433 mHz weather station signal, decode, store, and display data
# -----------------------------------------------------------------------------
from datetime import datetime
from datetime import timedelta as td
from met_functions2 import *
import RPi.GPIO as GPIO
import numpy as np
import math
import csv
from bme280 import *
from saveJSON import toDisplay, toGraph
from editConfigFiles import *
from SimpleServer import *

#Functions---------------------------------------------------------------------

def BIN2DEC(bin_value):
    N = len(bin_value)
    if bin_value[0] == 1:   #two's compliment
        decimal = -1
        for i in range(1,N):
            decimal -= math.pow(2,N-i-1)*(1-bin_value[i])
    else:
        decimal = 0
        for i in range(1,N):
            decimal += math.pow(2,N-i-1)*bin_value[i]
    return(decimal)
    
def decodeSignal(MAX_DURATION):

    global stationFound
    RECEIVED_SIGNAL = [[], []]                               #[[time of reading], [signal reading]]
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RECEIVE_PIN, GPIO.IN)
    cumulative_time = 0
    signalTime = datetime.now()
    while cumulative_time < MAX_DURATION:
        time_delta = datetime.now() - signalTime
        RECEIVED_SIGNAL[0].append(time_delta)
        RECEIVED_SIGNAL[1].append(GPIO.input(RECEIVE_PIN))
        cumulative_time = time_delta.seconds
    GPIO.cleanup()

    dx = []                 #length of signal high
    dy = []                 #length of signal low
    ind_rec = []
    high_count = 0
    low_count = 0

    #Convert raw singal to length of time signal is high and low
    for i in range(len(RECEIVED_SIGNAL[0])):
        if RECEIVED_SIGNAL[1][i] ==1:
            high_count += 1
            if low_count > 0:                                #recievers with poor signal to noise ratio need this raised
                dy.append(low_count)
                low_count = 0
        else:
            low_count +=1
            if high_count > 0:
                dx.append(high_count)
                high_count = 0
                ind_rec.append(i)
            

    #Search for sync signal (usually a long high)
    dx = np.array(dx)
    possibles = np.where(dx > 90)[0]                        #May need adjusted based on sensor type
    
    #Confirm sync (my sensors sync signal has the initial long high >90 followed by three more between 15 and 30)
    solns = []
    for p in possibles:
        check = dx[p+1:p+4]
        if np.all(check >= 15) and np.all(check <= 30) and p <= len(dx) - 68:
            low_check = dy[p+1:p+65]            #check for any gaps in the signal
            if max(low_check) < 35:
                solns.append(p)

    #Convert confirmed signals to Binary
    for i in range(len(solns)-1,-1,-1):         #Runs through signals in reverse (later ones are better)
        binary = []
        for j in range(solns[i]+4, solns[i]+68):
            if dx[j] > 10:                      #Any high longer than 10 is considered a 1, otherwisea 0
                binary.append(1)
            else:
                binary.append(0)
        check = binary[0:24]                    #The first three bytes identify the sensor, may change on any resets
        if check == [1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0]:
            if (stationFound == 0):
                print('**Connected to Station')
                stationFound = 1
                
            #This section identifies the bits for temp, hum and wspd
            bin_relH = binary[25:32]
            bin_temp_p1 = binary[36:40]
            bin_temp_p2 = binary[41:48]
            bin_temp = bin_temp_p1 + bin_temp_p2
            bin_wspd = binary[49:56]

            if (sum(bin_relH)%2 == binary[24]):       #Use parity bit to check good signal  
                bin_relH.insert(0,0)
                relH = BIN2DEC(bin_relH)
            else:
                relH = -999

            if (sum(binary[33:40])%2 == binary[32]) and (sum(bin_temp_p2)%2 == binary[40]):             #Use parity bits to check good signal 
                temp = (BIN2DEC(bin_temp)*0.1 + 56.891)                                                 #My sensors relationship between binary temp and actual temp
            else: temp = -999
            
            if (binary[49] == 0):
                wspd = BIN2DEC(bin_wspd)
            else: wspd = -999
            
            return signalTime,temp,relH,wspd
    return signalTime,-999,-999,-999

def checkForSpikes(temp, relH, lastTemp, lastRelH, SR_TempDiff, SR_RelHDiff, dt):
    if (lastTemp != -999) and (lastRelH != -999):
        if (abs(temp - lastTemp) <= SR_TempDiff*dt) and (abs(relH - lastRelH) <= SR_RelHDiff*dt):
            return(True)
        else:
            return(False)
    else:
        return(True)
                
    
    
#Initialize--------------------------------------------------------------------
    
if __name__ == '__main__':

    #Settings------------------
    logInterval = 1             #Minutes between data logging (minimum of 1)
    webUpdateInterval = 1       #Minutes between current weather update on display (minimum of logger interval)
    graphDataInterval = 5       #Minutes between data points on graph
    displayPort = 8000          #Port for webDisplay (i.e. http://localhost:8000)
    MAX_DURATION = 8            #Seconds of signal to record
    RECEIVE_PIN = 23            #Rasberry Pi pin reciever is sending data to
    SR_On_Off = 1               #Turn Spike Removal on(1) or off(0)
    SR_TempDiff = 5.0           #Spike Removal (temperature); acceptable change in degrees per minute
    SR_RelHDiff = 5.0           #Spike Removal (Relative Humidity); acceptable change in percent per minute
    #--------------------------
    
    version = 2.1
    startTime = datetime.now()
    
    print("**Begin SkyTap")
    print("**version " + str(version))
    print("**Start time: " + datetime.strftime(startTime,"%d-%m-%Y %H:%M:%S"))
    
    
    wspd_ave = -999
    gust = -999
    dewPoint = -999
    lastTemp = -999
    lastRelH = -999
    wspd_10min = []
    wind_dt = 1
    
    global stationFound
    stationFound = 0
    
    #initialize variables via today.ini
    lastSync,windRun = restoreDayFile()
    if lastSync == -999:
        lastSync = startTime - td(minutes=logInterval)
    nextSync = lastSync + td(minutes=logInterval)
    while datetime.now() < nextSync:
        time.sleep(1)
    
    elapsedTime = startTime - lastSync
    if (elapsedTime < td(minutes=15)) or (elapsedTime < td(minutes=logInterval)):
        wind_dt = elapsedTime/td(minutes=1)
    else:
        wind_dt = 1         #minutes since last wind record

    #Start webserver
    startWebserver(displayPort)

    #append data to the month log
    with open("/home/pi/SkyTap/log.txt", 'a') as logfile:
        logfile.write("SkyTap started at: " + datetime.strftime(startTime,"%d-%m-%Y %H:%M:%S\n"))
        logfile.write("---------------------------------------\n")
    logfile.close()


#Normal running loop-----------------------------------------------------------
    while True:
        saveFile = datetime.now().strftime("/home/pi/SkyTap/data/%b%ylog.csv")
        
        signalTime,temp,relH,wspd = decodeSignal(MAX_DURATION)                 #retrieve outdoor temp, relH, and Wspd
        inTempC,inPresMb,inRelH = readBME280All()                   #retrieve indoor temp, relH, and pressure from BME280
        
        #If no spikes or missing data: determine derived values, log data, then rest till next sync
        if (SR_On_Off == 1):
            dt = round((signalTime-nextSync)/td(minutes=1)) + 1.
            noSpikes = checkForSpikes(temp, relH, lastTemp, lastRelH, SR_TempDiff, SR_RelHDiff, dt)
        else: noSpikes == True
        if (wspd != -999) and noSpikes:
            
            #Ten minute average wind speed (saves 10 minutes of wind data)
            if (len(wspd_10min) >= 10/logInterval):
                wspd_10min = wspd_10min[1:len(wspd_10min)]
                wspd_10min.append(wspd)
            else:
                wspd_10min.append(wspd)
            wspd_ave = sum(wspd_10min)/float(len(wspd_10min))
            gust = max(wspd_10min)

            #Add to windRun
            if signalTime.day == lastSync.day:
                windRun += wspd/60*wind_dt
            else:
                windRun = wspd/60*wind_dt
                
            #WindChill
            windChill = 35.74 + (0.6215*temp) - (35.75*pow(wspd_ave,0.16)) + (0.4275*temp*pow(wspd_ave,0.16))
            if windChill > temp:
                windChill = temp

            #DewPoint
            try:
                e = (relH/100.)*es((temp-32.)*5./9. + 273.15)
                dewPoint = (e_to_td(e) - 273.15)*9./5. + 32.
            except Exception:
                dewPoint = -999
                
            #Convert indoor temperature and dewpoint to Fahrenheit
            inTempF = inTempC*9./5.+32.
            inDewF = (e_to_td(inRelH/100.*es(inTempC + 273.15)) - 273.15)*9./5. + 32.
            
            #Format data for saving
            currentWx = [signalTime.strftime("%d/%m/%y"),signalTime.strftime("%H:%M"),
                         '{:.1f}'.format(temp),relH,'{:.1f}'.format(dewPoint),wspd,'{:.1f}'.format(wspd_ave),
                         gust,'{:.1f}'.format(inTempF),'{:.1f}'.format(inRelH),'{:.1f}'.format(inDewF),
                         '{:.2f}'.format(inPresMb),'{:.2f}'.format(windRun),'{:.1f}'.format(windChill),-999]
            
            #append data to the month log
            with open(saveFile, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(currentWx)
            csvfile.close()

            #Check/Update records in ini files            
            if signalTime.year == lastSync.year:
                if signalTime.month == lastSync.month:
                    if signalTime.day == lastSync.day:
                        updateToday(currentWx)
                        updateMonth(currentWx)
                    else:
                        newDay(currentWx)
                        updateYear(currentWx)
                        updateAllTime()
                else:
                    newDay(currentWx)
                    newMonth(currentWx)
                    updateYear(currentWx)
                    updateAllTime()
                    updateMonthlyAllTime()
            else:
                newDay(currentWx)
                newMonth(currentWx)
                newYear(currentWx)
                updateYear(currentWx)
                updateAllTime()
                
            #Save data in JSON files to be read by web display
            if signalTime.minute % graphDataInterval == 0:
                toGraph(currentWx)
            if signalTime.minute % webUpdateInterval == 0:
                toDisplay(currentWx)
                
            #reset windChill and dewpoint then update lastSync and nextSync times
            windChill = -999
            dewpoint = -999
            lastSync = signalTime.replace(second=0,microsecond=0)
            lastTemp = temp
            lastRelH = relH
            nextSync = lastSync + td(minutes=logInterval)
            
            #rest until nextSync time
            while datetime.now() < nextSync:
                time.sleep(1)
        
        #If logInterval time has been expended without good signal, save any data that was retrieved and 
        #move into next interval
        elif lastSync < (datetime.now().replace(second=0,microsecond=0) - td(minutes=1)):
            
            #Average wind speed and windRun
            if (len(wspd_10min) >= 10/logInterval) and (wspd != -999):
                wspd_10min = wspd_10min[1:len(wspd_10min)]
                wspd_10min.append(wspd)
                wspd_ave = sum(wspd_10min)/float(len(wspd_10min))
                gust = max(wspd_10min)
                if signalTime.day == lastSync.day:
                    windRun += wspd/60*wind_dt
                else:
                    windRun = wspd/60*wind_dt
            elif (wspd != -999):
                wspd_10min.append(wspd)
                wspd_ave = sum(wspd_10min)/float(len(wspd_10min))
                gust = max(wspd_10min)
                if signalTime.day == lastSync.day:
                    windRun += wspd/60*wind_dt
                else:
                    windRun = wspd/60*wind_dt
            else:
                try:
                    wspd_10min = wspd_10min[1:len(wspd_10min)]
                    wspd_ave = sum(wspd_10min)/float(len(wspd_10min))
                except Exception:
                    wspd_ave = -999
                wind_dt += 1
                
            if (wspd_ave != -999) and (temp != -999):
                windChill = 35.74 + (0.6215*temp) - (35.75*pow(wspd_ave,0.16)) + (0.4275*temp*pow(wspd_ave,0.16))
                if windChill > temp:
                    windChill = temp
            else:
                windChill = -999
                    
    
            if (relH != -999) and (temp != -999):
                try:
                    e = (relH/100.)*es((temp-32.)*5./9. + 273.15)
                    dewPoint = (e_to_td(e) - 273.15)*9./5. + 32.
                except Exception:
                    dewPoint = -999
    
            inTempC,inPresMb,inRelH = readBME280All()
            inTempF = inTempC*9./5.+32.
            inDewF = (e_to_td(inRelH/100.*es(inTempC + 273.15)) - 273.15)*9./5. + 32.
            
            currentWx = [signalTime.strftime("%d/%m/%y"),signalTime.strftime("%H:%M"),
                         '{:.1f}'.format(temp),relH,'{:.1f}'.format(dewPoint),wspd,'{:.1f}'.format(wspd_ave),
                         gust,'{:.1f}'.format(inTempF),'{:.1f}'.format(inRelH),'{:.1f}'.format(inDewF),
                         '{:.2f}'.format(inPresMb),'{:.2f}'.format(windRun),'{:.1f}'.format(windChill),-999]
            
            with open(saveFile, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(currentWx)
            csvfile.close()
            
            lastSync = lastSync + td(minutes=logInterval)
            windChill = -999
            dewPoint = -999
        
        
        
        
        
        
        
        
        
        
        
