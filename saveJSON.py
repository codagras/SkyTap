#Functions for saving data for current weather display and graphin
from datetime import datetime
from datetime import timedelta as td
import configparser
import json
import time
import calendar

def toGraph(current):

    date_time = datetime.strptime(current[0] + ' ' + current[1],"%d/%m/%y %H:%M")
    dayStart = calendar.timegm((date_time-td(days=1)).timetuple())*1000.
    currentTime = calendar.timegm(date_time.timetuple())*1000.

    for i in range(2,len(current)):
        current[i] = float(current[i])

    try:
        with open('webFiles/tempData.json', 'r') as tempFile:
            tempData = json.load(tempFile)
        tempFile.close()

        with open('webFiles/presData.json', 'r') as presFile:
            presData = json.load(presFile)
        presFile.close()

        with open('webFiles/windData.json', 'r') as windFile:
            windData = json.load(windFile)
        windFile.close()

        with open('webFiles/humidityData.json', 'r') as humidFile:
            humidityData = json.load(humidFile)
        humidFile.close()
    except FileNotFoundError:           #When program is started for first time
        tempData = {}
        tempData["temp"] = [[currentTime,current[2]]]
        tempData["inTemp"] = [[currentTime,current[8]]]
        tempData["dew"] = [[currentTime,current[4]]]
        presData = {}
        presData["pres"] = []
        windData = {}
        windData["wind"] = []
        windData["ave_wind"] = []
        windData["gust"] = []
        humidityData = {}
        humidityData["relH"] = []
        humidityData["inRelH"] = []

        with open('webFiles/dailyTempData.json', 'w') as dailyTempFile:
            dailyTempData = {}
            dailyTempData["max"] = []
            dailyTempData["min"] = []
            dailyTempData["ave"] = []
            json.dump(dailyTempData, dailyTempFile)
        dailyTempFile.close()
        
        with open('webFiles/dailyInTempData.json', 'w') as dailyInTempFile:
            dailyInTempData = {}
            dailyInTempData["max"] = []
            dailyInTempData["min"] = []
            dailyInTempData["ave"] = []
            json.dump(dailyInTempData, dailyInTempFile)
        dailyInTempFile.close()
        
        with open('webFiles/dailyWindRunData.json', 'w') as dailyWindRunFile:
            dailyWindRunData = {}
            dailyWindRunData["windRun"] = []
            json.dump(dailyWindRunData, dailyWindRunFile)
        dailyWindRunFile.close()

    try:
        lastSync_long = tempData["temp"][len(tempData["temp"])-1][0]
        lastSync = time.gmtime(lastSync_long/1000.)
    except Exception:
        lastSync = time.gmtime(currentTime/1000.)
        
    if date_time.day == lastSync[2]:
        pass
    else:
        with open('webFiles/dailyTempData.json', 'r+') as dailyTempFile:
            dailyTempData = json.load(dailyTempFile)
            while len(dailyTempData["max"]) > 30:
                del dailyTempData["max"][0]
                del dailyTempData["min"][0]
                del dailyTempData["ave"][0]
            tempList = [i[1] for i in tempData["temp"]]
            dailyTempFile.seek(0)
            dailyTempData["max"].append([lastSync_long,max(tempList)])
            dailyTempData["min"].append([lastSync_long,min(tempList)])
            dailyTempData["ave"].append([lastSync_long,sum(tempList)/float(len(tempList))])
            json.dump(dailyTempData, dailyTempFile)
            dailyTempFile.truncate()
        dailyTempFile.close()
        
        with open('webFiles/dailyInTempData.json', 'r+') as dailyInTempFile:
            dailyInTempData = json.load(dailyInTempFile)
            while len(dailyInTempData["max"]) > 30:
                del dailyInTempData["max"][0]
                del dailyInTempData["min"][0]
                del dailyInTempData["ave"][0]
            tempList = [i[1] for i in tempData["inTemp"]]
            dailyInTempFile.seek(0)
            dailyInTempData["max"].append([lastSync_long,max(tempList)])
            dailyInTempData["min"].append([lastSync_long,min(tempList)])
            dailyInTempData["ave"].append([lastSync_long,sum(tempList)/float(len(tempList))])
            json.dump(dailyInTempData, dailyInTempFile)
            dailyInTempFile.truncate()
        dailyInTempFile.close()
        
        with open('webFiles/dailyWindRunData.json', 'r+') as dailyWindRunFile:
            dailyWindRunData = json.load(dailyWindRunFile)
            while len(dailyWindRunData["windRun"]) > 30:
                del dailyWindRunData["windRun"][0]
            windList = [i[1] for i in windData["ave_wind"]]
            dailyWindRunFile.seek(0)
            dailyWindRunData["windRun"].append([lastSync_long,sum(windList)/float(len(windList))*24.0])
            json.dump(dailyWindRunData, dailyWindRunFile)
            dailyWindRunFile.truncate()
        dailyWindRunFile.close()

    try:
        while dayStart >= tempData["temp"][0][0]:
            del tempData["temp"][0]
            del tempData["inTemp"][0]
            del tempData["dew"][0]
            del presData["pres"][0]
            del windData["wind"][0]
            del windData["ave_wind"][0]
            del windData["gust"][0]
            del humidityData["relH"][0]
            del humidityData["inRelH"][0]
    except IndexError:
        pass
            

    tempData["temp"].append([currentTime,current[2]])
    tempData["inTemp"].append([currentTime,current[8]])
    tempData["dew"].append([currentTime,current[4]])
    presData["pres"].append([currentTime,current[11]])
    windData["wind"].append([currentTime,current[5]])
    windData["ave_wind"].append([currentTime,current[6]])
    windData["gust"].append([currentTime,current[7]])
    humidityData["relH"].append([currentTime,current[3]])
    humidityData["inRelH"].append([currentTime,current[9]])

    with open('webFiles/tempData.json', 'w') as outfile:
        json.dump(tempData, outfile)
    outfile.close()

    with open('webFiles/presData.json', 'w') as outfile:
        json.dump(presData, outfile)
    outfile.close()

    with open('webFiles/windData.json', 'w') as outfile:
        json.dump(windData, outfile)
    outfile.close()

    with open('webFiles/humidityData.json', 'w') as outfile:
        json.dump(humidityData, outfile)
    outfile.close()

	
def toDisplay(current):

    date_time = datetime.strptime(current[0] + ' ' + current[1],"%d/%m/%y %H:%M")

    for i in range(2,len(current)):
        current[i] = float(current[i])
        
    with open('webFiles/now.json', 'w') as outfile:
        json.dump({"now":current}, outfile)
    outfile.close()
	
    recordList = []
    records = configparser.ConfigParser()
    records.read('records/today.ini')
    currentYear = records.get('General', 'CurrentYear')
    recordList.append(records.getfloat('Temp', 'High'))
    recordList.append(records.getfloat('Temp', 'Low'))
    recordList.append(records.getfloat('Wind', 'Speed'))
    recordList.append(records.getfloat('Wind', 'Gust'))
    recordList.append(records.getfloat('Pressure', 'High'))
    recordList.append(records.getfloat('Pressure', 'Low'))
	
    records = configparser.ConfigParser()
    month_file = 'records/month' + str(date_time.strftime("%Y%m") + '.ini')
    records.read(month_file)
    recordList.append(records.getfloat('Temp', 'High'))
    recordList.append(records.getfloat('Temp', 'Low'))
    recordList.append(records.getfloat('Temp', 'HighRange'))
    recordList.append(records.getfloat('Temp', 'LowMax'))
    recordList.append(records.getfloat('Wind', 'Speed'))
    recordList.append(records.getfloat('Wind', 'Gust'))
    recordList.append(records.getfloat('Wind', 'Windrun'))
    recordList.append(records.getfloat('Pressure', 'High'))
    recordList.append(records.getfloat('Pressure', 'Low'))
	
    records = configparser.ConfigParser()
    year_file = 'records/year' + currentYear + '.ini'
    if records.read(year_file) != []:
        recordList.append(records.getfloat('Temp', 'High'))
        recordList.append(records.getfloat('Temp', 'Low'))
        recordList.append(records.getfloat('Temp', 'HighRange'))
        recordList.append(records.getfloat('Temp', 'LowMax'))
        recordList.append(records.getfloat('Wind', 'Speed'))
        recordList.append(records.getfloat('Wind', 'Gust'))
        recordList.append(records.getfloat('Wind', 'Windrun'))
        recordList.append(records.getfloat('Pressure', 'High'))
        recordList.append(records.getfloat('Pressure', 'Low'))
    
    with open('webFiles/records.json', 'w') as outfile:
        json.dump({"records":recordList}, outfile)
    outfile.close()


