# -*- coding: utf-8 -*-

#currentWx[beginning_time.strftime("%d/%m/%y"),beginning_time.strftime("%H:%M"),
#temp,relH,dewPoint,wspd,wspd_ave,gust,inTempF,inRelH,inDewF,inPresMb,windRun,-999,-999]

import configparser
from datetime import datetime, timedelta

#Read ini files at startup
def restoreDayFile():
    config = configparser.ConfigParser()
    config.read('records/today.ini')
    lastSync = -999
    try:
        timestamp = config.get('General', 'timestamp', fallback=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
        lastSync = datetime.strptime(timestamp,"%Y-%m-%dT%H:%M:%S")
        lastSync = lastSync.replace(second=0,microsecond=0)
    except Exception:
        pass
    try:
        windRun = config.getfloat('Wind', 'windrun', fallback=1)
    except Exception:
        windRun = 0
    
    return lastSync,windRun


#update today.ini
def updateToday(currentWx):

    for i in range(2,len(currentWx)):
        currentWx[i] = float(currentWx[i])
    
    config = configparser.ConfigParser()
    date_time = datetime.strptime(currentWx[0] + ' ' + currentWx[1],"%d/%m/%y %H:%M")
    config.read('records/today.ini')
    
    if config.read('records/today.ini') == []:
        newDay(currentWx)
        return
    
    config['General']['Date'] = date_time.strftime("%d/%m/%y")
    config['General']['Timestamp'] = date_time.strftime("%Y-%m-%dT%H:%M:%S")
    config['General']['CurrentYear'] = str(date_time.year)
    config['General']['CurrentMonth'] = date_time.strftime("%m")
    config['General']['CurrentDay'] = date_time.strftime("%d")
    
    if currentWx[6] > config.getfloat('Wind', 'Speed'):
        config['Wind']['Speed'] = str(currentWx[6])
        config['Wind']['SpTime'] = date_time.strftime("%H:%M")
    if currentWx[7] > config.getfloat('Wind', 'Gust'):
        config['Wind']['Gust'] = str(currentWx[7])
        config['Wind']['Time'] = date_time.strftime("%H:%M")
    config['Wind']['Windrun'] = str(currentWx[12])
    
    if currentWx[2] < config.getfloat('Temp', 'Low'):
        config['Temp']['Low'] = str(currentWx[2])
        config['Temp']['LTime'] = date_time.strftime("%H:%M")
    if currentWx[2] > config.getfloat('Temp', 'High'):
        config['Temp']['High'] = str(currentWx[2])
        config['Temp']['HTime'] = date_time.strftime("%H:%M")
    if currentWx[8] < config.getfloat('Temp', 'inLow'):
        config['Temp']['inLow'] = str(currentWx[8])
        config['Temp']['inLTime'] = date_time.strftime("%H:%M")
    if currentWx[8] > config.getfloat('Temp', 'inHigh'):
        config['Temp']['inHigh'] = str(currentWx[8])
        config['Temp']['inHTime'] = date_time.strftime("%H:%M")
    config['Temp']['Total'] = str(config.getfloat('Temp', 'Total') + currentWx[2])
    config['Temp']['Samples'] = str(config.getint('Temp', 'Samples') + 1)

    if currentWx[11] < config.getfloat('Pressure', 'Low'):
        config['Pressure']['Low'] = str(currentWx[11])
        config['Pressure']['LTime'] = date_time.strftime("%H:%M")
    if currentWx[11] > config.getfloat('Pressure', 'High'):
        config['Pressure']['High'] = str(currentWx[11])
        config['Pressure']['HTime'] = date_time.strftime("%H:%M")
    
    if currentWx[3] < config.getfloat('Humidity', 'Low'):
        config['Humidity']['Low'] = str(currentWx[3])
        config['Humidity']['LTime'] = date_time.strftime("%H:%M")
    if currentWx[3] > config.getfloat('Humidity', 'High'):
        config['Humidity']['High'] = str(currentWx[3])
        config['Humidity']['HTime'] = date_time.strftime("%H:%M")
    if currentWx[9] < config.getfloat('Humidity', 'inLow'):
        config['Humidity']['inLow'] = str(currentWx[9])
        config['Humidity']['inLTime'] = date_time.strftime("%H:%M")
    if currentWx[9] > config.getfloat('Humidity', 'inHigh'):
        config['Humidity']['inHigh'] = str(currentWx[9])
        config['Humidity']['inHTime'] = date_time.strftime("%H:%M")
        
    if currentWx[13] < config.getfloat('WindChill', 'Low'):
        config['WindChill']['Low'] = str(currentWx[13])
        config['WindChill']['LTime'] = date_time.strftime("%H:%M")
    
    if currentWx[4] < config.getfloat('Dewpoint', 'Low'):
        config['Dewpoint']['Low'] = str(currentWx[4])
        config['Dewpoint']['LTime'] = date_time.strftime("%H:%M")
    if currentWx[4] > config.getfloat('Dewpoint', 'High'):
        config['Dewpoint']['High'] = str(currentWx[4])
        config['Dewpoint']['HTime'] = date_time.strftime("%H:%M")
        
    with open('records/today.ini', 'w') as configfile:
        config.write(configfile)
    configfile.close

#update month.ini
def updateMonth(currentWx):

    for i in range(2,len(currentWx)):
        currentWx[i] = float(currentWx[i])
    
    config = configparser.ConfigParser()
    time_stamp = currentWx[0] + ' ' + currentWx[1]
    date_time = datetime.strptime(time_stamp,"%d/%m/%y %H:%M")
    save_file = 'records/month' + str(date_time.strftime("%Y%m") + '.ini')
    
    if config.read(save_file) == []:
        newMonth(currentWx)
        return

    config['General']['Date'] = time_stamp    
    
    if currentWx[6] > config.getfloat('Wind', 'Speed'):
        config['Wind']['Speed'] = str(currentWx[6])
        config['Wind']['SpTime'] = time_stamp
    if currentWx[7] > config.getfloat('Wind', 'Gust'):
        config['Wind']['Gust'] = str(currentWx[7])
        config['Wind']['Time'] = time_stamp
    config['Wind']['Windrun'] = str(currentWx[12])      #daily windrun record
    config['Wind']['WindrunTime'] = time_stamp
    
    if currentWx[2] < config.getfloat('Temp', 'Low'):
        config['Temp']['Low'] = str(currentWx[2])
        config['Temp']['LTime'] = time_stamp
    if currentWx[2] > config.getfloat('Temp', 'High'):
        config['Temp']['High'] = str(currentWx[2])
        config['Temp']['HTime'] = time_stamp
    if currentWx[8] < config.getfloat('Temp', 'inLow'):
        config['Temp']['inLow'] = str(currentWx[8])
        config['Temp']['inLTime'] = time_stamp
    if currentWx[8] > config.getfloat('Temp', 'inHigh'):
        config['Temp']['inHigh'] = str(currentWx[8])
        config['Temp']['inHTime'] = time_stamp
    
    if currentWx[11] < config.getfloat('Pressure', 'Low'):
        config['Pressure']['Low'] = str(currentWx[11])
        config['Pressure']['LTime'] = time_stamp
    if currentWx[11] > config.getfloat('Pressure', 'High'):
        config['Pressure']['High'] = str(currentWx[11])
        config['Pressure']['HTime'] = time_stamp

    if currentWx[3] < config.getfloat('Humidity', 'Low'):
        config['Humidity']['Low'] = str(currentWx[3])
        config['Humidity']['LTime'] = time_stamp
    if currentWx[3] > config.getfloat('Humidity', 'High'):
        config['Humidity']['High'] = str(currentWx[3])
        config['Humidity']['HTime'] = time_stamp
    if currentWx[9] < config.getfloat('Humidity', 'inLow'):
        config['Humidity']['inLow'] = str(currentWx[9])
        config['Humidity']['inLTime'] = time_stamp
    if currentWx[9] > config.getfloat('Humidity', 'inHigh'):
        config['Humidity']['inHigh'] = str(currentWx[9])
        config['Humidity']['inHTime'] = time_stamp
    
    if currentWx[13] < config.getfloat('WindChill', 'Low'):
        config['WindChill']['Low'] = str(currentWx[13])
        config['WindChill']['LTime'] = time_stamp

    if currentWx[4] < config.getfloat('Dewpoint', 'Low'):
        config['Dewpoint']['Low'] = str(currentWx[4])
        config['Dewpoint']['LTime'] = time_stamp
    if currentWx[4] > config.getfloat('Dewpoint', 'High'):
        config['Dewpoint']['High'] = str(currentWx[4])
        config['Dewpoint']['HTime'] = time_stamp
    
    with open(save_file, 'w') as configfile:
        config.write(configfile)
    configfile.close
    
#update year.ini at the beginning of each day
def updateYear(currentWx):

    for i in range(2,len(currentWx)):
        currentWx[i] = float(currentWx[i])
    
    config = configparser.ConfigParser()
    config.read('records/today.ini')
    date = config.get('General', 'Date')
    currentYear = config.get('General', 'CurrentYear')
    year_file = 'records/year'+ currentYear + '.ini'
    
    Speed= config.getfloat('Wind', 'Speed')
    SpTime= config.get('Wind', 'SpTime')
    Gust= config.getfloat('Wind', 'Gust')
    Gust_Time= config.get('Wind', 'Time')
    Windrun= config.getfloat('Wind', 'Windrun')
    Temp_Low= config.getfloat('Temp', 'Low')
    Temp_LTime= config.get('Temp', 'LTime')
    Temp_High= config.getfloat('Temp', 'High')
    Temp_HTime= config.get('Temp', 'HTime')
    Temp_inLow= config.getfloat('Temp', 'inLow')
    Temp_inLTime= config.get('Temp', 'inLTime')
    Temp_inHigh= config.getfloat('Temp', 'inHigh')
    Temp_inHTime= config.get('Temp', 'inHTime')  
    Pres_Low= config.getfloat('Pressure', 'Low')
    Pres_LTime= config.get('Pressure', 'LTime')
    Pres_High= config.getfloat('Pressure', 'High')
    Pres_HTime= config.get('Pressure', 'HTime')
    Hum_Low= config.getfloat('Humidity', 'Low')
    Hum_High= config.getfloat('Humidity', 'High')
    Hum_LTime= config.get('Humidity', 'LTime')
    Hum_HTime= config.get('Humidity', 'HTime')
    Hum_inLow= config.getfloat('Humidity', 'inLow')
    Hum_inLTime= config.get('Humidity', 'inLTime')
    Hum_inHigh= config.getfloat('Humidity', 'inHigh')
    Hum_inHTime= config.get('Humidity', 'inHTime')
    Chill_Low= config.getfloat('WindChill', 'Low')
    Chill_LTime= config.get('WindChill', 'LTime')
    Dew_Low= config.getfloat('Dewpoint', 'Low')
    Dew_LTime= config.get('Dewpoint', 'LTime')
    Dew_High= config.getfloat('Dewpoint', 'High')
    Dew_HTime= config.get('Dewpoint', 'HTime')
    Temp_range= Temp_High - Temp_Low
    
    if config.read(year_file) == []:
        newYear(currentWx)

    config = configparser.ConfigParser()
    config.read(year_file)
        
    if Speed > config.getfloat('Wind', 'Speed'):
        config['Wind']['Speed'] = str(Speed)
        config['Wind']['SpTime'] = SpTime
    if Gust > config.getfloat('Wind', 'Gust'):
        config['Wind']['Gust'] = str(Gust)
        config['Wind']['Time'] = Gust_Time
    if Windrun > config.getfloat('Wind', 'Windrun'):
        config['Wind']['Windrun'] = str(Windrun)
        config['Wind']['WindrunTime'] = date
    
    if Temp_Low < config.getfloat('Temp', 'Low'):
        config['Temp']['Low'] = str(Temp_Low)
        config['Temp']['LTime'] = Temp_LTime
    if Temp_High > config.getfloat('Temp', 'High'):
        config['Temp']['High'] = str(Temp_High)
        config['Temp']['HTime'] = Temp_HTime
    if Temp_inLow < config.getfloat('Temp', 'inLow'):
        config['Temp']['inLow'] = str(Temp_inLow)
        config['Temp']['inLTime'] = Temp_inLTime
    if Temp_inHigh > config.getfloat('Temp', 'inHigh'):
        config['Temp']['inHigh'] = str(Temp_inHigh)
        config['Temp']['inHTime'] = Temp_inHTime
    if Temp_Low > config.getfloat('Temp', 'LowMax'):
        config['Temp']['LowMax'] = str(Temp_Low)
        config['Temp']['LMTime'] = date
    if Temp_High < config.getfloat('Temp', 'HighMin'):
        config['Temp']['HighMin'] = str(Temp_High)
        config['Temp']['HMTime'] = date
    if Temp_range < config.getfloat('Temp', 'lowrange'):
        config['Temp']['lowrange'] = str(Temp_range)
        config['Temp']['lowrangetime'] = date
    if Temp_range > config.getfloat('Temp', 'highrange'):
        config['Temp']['highrange'] = str(Temp_range)
        config['Temp']['highrangetime'] = date

    if Pres_Low < config.getfloat('Pressure', 'Low'):
        config['Pressure']['Low'] = str(Pres_Low)
        config['Pressure']['LTime'] = Pres_LTime
    if Pres_High > config.getfloat('Pressure', 'High'):
        config['Pressure']['High'] = str(Pres_High)
        config['Pressure']['HTime'] = Pres_HTime
    
    if Hum_Low < config.getfloat('Humidity', 'Low'):
        config['Humidity']['Low'] = str(Hum_Low)
        config['Humidity']['LTime'] = Hum_LTime
    if Hum_High > config.getfloat('Humidity', 'High'):
        config['Humidity']['High'] = str(Hum_High)
        config['Humidity']['HTime'] = Hum_HTime
    if Hum_inLow < config.getfloat('Humidity', 'inLow'):
        config['Humidity']['inLow'] = str(Hum_inLow)
        config['Humidity']['inLTime'] = Hum_inLTime
    if Hum_inHigh > config.getfloat('Humidity', 'inHigh'):
        config['Humidity']['inHigh'] = str(Hum_inHigh)
        config['Humidity']['inHTime'] = Hum_inHTime
        
    if Chill_Low < config.getfloat('WindChill', 'Low'):
        config['WindChill']['Low'] = str(Chill_Low)
        config['WindChill']['LTime'] = Chill_LTime
    
    if Dew_Low < config.getfloat('Dewpoint', 'Low'):
        config['Dewpoint']['Low'] = str(Dew_Low)
        config['Dewpoint']['LTime'] = Dew_LTime
    if Dew_High > config.getfloat('Dewpoint', 'High'):
        config['Dewpoint']['High'] = str(Dew_High)
        config['Dewpoint']['HTime'] = Dew_HTime
        
    with open(year_file, 'w') as configfile:
        config.write(configfile)
    configfile.close
    
#update monthlyalltime.ini -> do this at the beginning of each month
def updateMonthlyAllTime():
    config = configparser.ConfigParser()
    config.read('records/today.ini')
    currentYear = config.get('General', 'currentYear')
    currentMonth = config.get('General', 'CurrentMonth')
    month_file = 'records/month'+ currentYear + currentMonth + '.ini'
    
    config.read(month_file)
    Speed= config.getfloat('Wind', 'Speed')
    SpTime= config.get('Wind', 'SpTime')
    Gust= config.getfloat('Wind', 'Gust')
    Gust_Time= config.get('Wind', 'Time')
    Windrun= config.getfloat('Wind', 'Windrun')
    WindrunTime = config.get('Wind', 'WindrunTime')
    Temp_Low= config.getfloat('Temp', 'Low')
    Temp_LTime= config.get('Temp', 'LTime')
    Temp_High= config.getfloat('Temp', 'High')
    Temp_HTime= config.get('Temp', 'HTime')
    Temp_LowMax= config.getfloat('Temp', 'LowMax')
    Temp_LMTime= config.get('Temp', 'LMTime')
    Temp_HighMin= config.getfloat('Temp', 'HighMin')
    Temp_HMTime= config.get('Temp', 'HMTime')
    Temp_LowRange= config.getfloat('Temp', 'LowRange')
    Temp_LowRangeTime= config.get('Temp', 'LowRangeTime')
    Temp_HighRange= config.getfloat('Temp', 'HighRange')
    Temp_HighRangeTime= config.get('Temp', 'HighRangeTime')
    Pres_Low= config.getfloat('Pressure', 'Low')
    Pres_LTime= config.get('Pressure', 'LTime')
    Pres_High= config.getfloat('Pressure', 'High')
    Pres_HTime= config.get('Pressure', 'HTime')
    Hum_Low= config.getfloat('Humidity', 'Low')
    Hum_High= config.getfloat('Humidity', 'High')
    Hum_LTime= config.get('Humidity', 'LTime')
    Hum_HTime= config.get('Humidity', 'HTime')
    Chill_Low= config.getfloat('WindChill', 'Low')
    Chill_LTime= config.get('WindChill', 'LTime')
    Dew_Low= config.getfloat('Dewpoint', 'Low')
    Dew_LTime= config.get('Dewpoint', 'LTime')
    Dew_High= config.getfloat('Dewpoint', 'High')
    Dew_HTime= config.get('Dewpoint', 'HTime')
    
    config = configparser.ConfigParser()
    config.read('records/monthlyalltime.ini')
        
    if Speed > config.getfloat('Wind'+currentMonth, 'highwindvalue', fallback=-999):
        config['Wind'+currentMonth]['highwindvalue'] = str(Speed)
        config['Wind'+currentMonth]['highwindtime'] = SpTime
    if Gust > config.getfloat('Wind'+currentMonth, 'highgustvalue', fallback=-999):
        config['Wind'+currentMonth]['highgustvalue'] = str(Gust)
        config['Wind'+currentMonth]['highgusttime'] = Gust_Time
    if Windrun > config.getfloat('Wind'+currentMonth, 'highdailywindrunvalue', fallback=-999):
        config['Wind'+currentMonth]['highdailywindrunvalue'] = str(Windrun)
        config['Wind'+currentMonth]['highdailywindruntime'] = WindrunTime
    
    if Temp_Low < config.getfloat('Temperature'+currentMonth, 'lowtempvalue', fallback=999):
        config['Temperature'+currentMonth]['lowtempvalue'] = str(Temp_Low)
        config['Temperature'+currentMonth]['lowtemptime'] = Temp_LTime
    if Temp_High > config.getfloat('Temperature'+currentMonth, 'hightempvalue', fallback=-999):
        config['Temperature'+currentMonth]['hightempvalue'] = str(Temp_High)
        config['Temperature'+currentMonth]['hightemptime'] = Temp_HTime
    if Temp_LowMax > config.getfloat('Temperature'+currentMonth, 'lowmaxtempvalue', fallback=-999):
        config['Temperature'+currentMonth]['lowmaxtempvalue'] = str(Temp_LowMax)
        config['Temperature'+currentMonth]['lowmaxtemptime'] = Temp_LMTime
    if Temp_HighMin < config.getfloat('Temperature'+currentMonth, 'highmintempvalue', fallback=999):
        config['Temperature'+currentMonth]['highmintempvalue'] = str(Temp_HighMin)
        config['Temperature'+currentMonth]['highmintemptime'] = Temp_HMTime
    if Temp_LowRange < config.getfloat('Temperature'+currentMonth, 'lowtemprangevalue', fallback=999):
        config['Temperature'+currentMonth]['lowtemprangevalue'] = str(Temp_LowRange)
        config['Temperature'+currentMonth]['lowtemprangetime'] = Temp_LowRangeTime
    if Temp_HighRange > config.getfloat('Temperature'+currentMonth, 'hightemprangevalue', fallback=-999):
        config['Temperature'+currentMonth]['hightemprangevalue'] = str(Temp_HighRange)
        config['Temperature'+currentMonth]['hightemprangetime'] = Temp_HighRangeTime

    if Pres_Low < config.getfloat('Pressure'+currentMonth, 'lowpressurevalue', fallback=9999):
        config['Pressure'+currentMonth]['lowpressurevalue'] = str(Pres_Low)
        config['Pressure'+currentMonth]['lowpressuretime'] = Pres_LTime
    if Pres_High > config.getfloat('Pressure'+currentMonth, 'highpressurevalue', fallback=-9999):
        config['Pressure'+currentMonth]['highpressurevalue'] = str(Pres_High)
        config['Pressure'+currentMonth]['highpressuretime'] = Pres_HTime
    
    if Hum_Low < config.getfloat('Humidity'+currentMonth, 'lowhumidityvalue', fallback=999):
        config['Humidity'+currentMonth]['lowhumidityvalue'] = str(Hum_Low)
        config['Humidity'+currentMonth]['lowhumiditytime'] = Hum_LTime
    if Hum_High > config.getfloat('Humidity'+currentMonth, 'highhumidityvalue', fallback=-999):
        config['Humidity'+currentMonth]['highhumidityvalue'] = str(Hum_High)
        config['Humidity'+currentMonth]['highhumiditytime'] = Hum_HTime
        
    if Chill_Low < config.getfloat('Temperature'+currentMonth, 'lowchillvalue', fallback=999):
        config['Temperature'+currentMonth]['lowchillvalue'] = str(Chill_Low)
        config['Temperature'+currentMonth]['lowchilltime'] = Chill_LTime
    
    if Dew_Low < config.getfloat('Temperature'+currentMonth, 'lowdewpointvalue', fallback=999):
        config['Temperature'+currentMonth]['lowdewpointvalue'] = str(Dew_Low)
        config['Temperature'+currentMonth]['lowdewpointtime'] = Dew_LTime
    if Dew_High > config.getfloat('Dewpoint'+currentMonth, 'highdewpointvalue', fallback=-999):
        config['Temperature'+currentMonth]['highdewpointvalue'] = str(Dew_High)
        config['Temperature'+currentMonth]['highdewpointtime'] = Dew_HTime
        
    with open('records/monthlyalltime.ini', 'w') as configfile:
        config.write(configfile)
    configfile.close


#update alltime.ini -> do this iat the beginning of each day
def updateAllTime():
    config = configparser.ConfigParser()
    config.read('records/today.ini')
    date = config.get('General', 'Date')
    
    Speed= config.getfloat('Wind', 'Speed')
    SpTime= config.get('Wind', 'SpTime')
    Gust= config.getfloat('Wind', 'Gust')
    Gust_Time= config.get('Wind', 'Time')
    Windrun= config.getfloat('Wind', 'Windrun')
    Temp_Low= config.getfloat('Temp', 'Low')
    Temp_LTime= config.get('Temp', 'LTime')
    Temp_High= config.getfloat('Temp', 'High')
    Temp_HTime= config.get('Temp', 'HTime')  
    Pres_Low= config.getfloat('Pressure', 'Low')
    Pres_LTime= config.get('Pressure', 'LTime')
    Pres_High= config.getfloat('Pressure', 'High')
    Pres_HTime= config.get('Pressure', 'HTime')
    Hum_Low= config.getfloat('Humidity', 'Low')
    Hum_High= config.getfloat('Humidity', 'High')
    Hum_LTime= config.get('Humidity', 'LTime')
    Hum_HTime= config.get('Humidity', 'HTime')
    Chill_Low= config.getfloat('WindChill', 'Low')
    Chill_LTime= config.get('WindChill', 'LTime')
    Dew_Low= config.getfloat('Dewpoint', 'Low')
    Dew_LTime= config.get('Dewpoint', 'LTime')
    Dew_High= config.getfloat('Dewpoint', 'High')
    Dew_HTime= config.get('Dewpoint', 'HTime')
    Temp_range= Temp_High - Temp_Low

    config = configparser.ConfigParser()
    if config.read('records/alltime.ini') == []:
        config.read('records/default_ini/alltime.ini')
    
    if Speed > config.getfloat('Wind', 'highwindvalue', fallback=-999):
        config['Wind']['highwindvalue'] = str(Speed)
        config['Wind']['highwindtime'] = date + ' ' + SpTime
    if Gust > config.getfloat('Wind', 'highgustvalue', fallback=-999):
        config['Wind']['highgustvalue'] = str(Gust)
        config['Wind']['highgusttime'] = date + ' ' + Gust_Time
    if Windrun > config.getfloat('Wind', 'highdailywindrunvalue', fallback=-999):
        config['Wind']['highdailywindrunvalue'] = str(Windrun)
        config['Wind']['highdailywindruntime'] = date
    
    if Temp_Low < config.getfloat('Temperature', 'lowtempvalue', fallback=999):
        config['Temperature']['lowtempvalue'] = str(Temp_Low)
        config['Temperature']['lowtemptime'] = date + ' ' + Temp_LTime
    if Temp_High > config.getfloat('Temperature', 'hightempvalue', fallback=-999):
        config['Temperature']['hightempvalue'] = str(Temp_High)
        config['Temperature']['hightemptime'] = date + ' ' + Temp_HTime
    if Temp_High < config.getfloat('Temperature', 'lowmaxtempvalue', fallback=-999):
        config['Temperature']['lowmaxtempvalue'] = str(Temp_High)
        config['Temperature']['lowmaxtemptime'] = date + ' ' + Temp_LTime
    if Temp_Low > config.getfloat('Temperature', 'highmintempvalue', fallback=999):
        config['Temperature']['highmintempvalue'] = str(Temp_Low)
        config['Temperature']['highmintemptime'] = date + ' ' + Temp_HTime
    if Temp_range < config.getfloat('Temperature', 'lowtemprangevalue', fallback=999):
        config['Temperature']['lowtemprangevalue'] = str(Temp_range)
        config['Temperature']['lowtemprangetime'] = date
    if Temp_range > config.getfloat('Temperature', 'hightemprangevalue', fallback=-999):
        config['Temperature']['hightemprangevalue'] = str(Temp_range)
        config['Temperature']['hightemprangetime'] = date

    if Pres_Low < config.getfloat('Pressure', 'lowpressurevalue', fallback=9999):
        config['Pressure']['lowpressurevalue'] = str(Pres_Low)
        config['Pressure']['lowpressuretime'] = date + ' ' + Pres_LTime
    if Pres_High > config.getfloat('Pressure', 'highpressurevalue', fallback=-9999):
        config['Pressure']['highpressurevalue'] = str(Pres_High)
        config['Pressure']['highpressuretime'] = date + ' ' + Pres_HTime
    
    if Hum_Low < config.getfloat('Humidity', 'lowhumidityvalue', fallback=999):
        config['Humidity']['lowhumidityvalue'] = str(Hum_Low)
        config['Humidity']['lowhumiditytime'] = date + ' ' + Hum_LTime
    if Hum_High > config.getfloat('Humidity', 'highhumidityvalue', fallback=-999):
        config['Humidity']['highhumidityvalue'] = str(Hum_High)
        config['Humidity']['highhumiditytime'] = date + ' ' + Hum_HTime
        
    if Chill_Low < config.getfloat('Temperature', 'lowchillvalue', fallback=999):
        config['Temperature']['lowchillvalue'] = str(Chill_Low)
        config['Temperature']['lowchilltime'] = date + ' ' + Chill_LTime
    
    if Dew_Low < config.getfloat('Temperature', 'lowdewpointvalue', fallback=999):
        config['Temperature']['lowdewpointvalue'] = str(Dew_Low)
        config['Temperature']['lowdewpointtime'] = date + ' ' + Dew_LTime
    if Dew_High > config.getfloat('Dewpoint', 'highdewpointvalue', fallback=-999):
        config['Temperature']['highdewpointvalue'] = str(Dew_High)
        config['Temperature']['highdewpointtime'] = date + ' ' + Dew_HTime
        
    with open('records/alltime.ini', 'w') as configfile:
        config.write(configfile)
    configfile.close
    
#add any final temp records to month.ini
def tempRecords(currentWx):

    for i in range(2,len(currentWx)):
        currentWx[i] = float(currentWx[i])
    
    config = configparser.ConfigParser()
    date_time = datetime.strptime(currentWx[0] + ' ' + currentWx[1],"%d/%m/%y %H:%M")
    prev_day = date_time - timedelta(days=1)
    time_stamp = prev_day.strftime("%d/%m/%y")
    month_file = 'records/month' + str(prev_day.strftime("%Y%m") + '.ini')
    config.read('records/today.ini')
    lowTemp = config.getfloat('Temp', 'Low')
    highTemp = config.getfloat('Temp', 'High')
    tempRange = highTemp - lowTemp
    
    config = configparser.ConfigParser()
    config.read(month_file)
    config['General']['date'] = date_time.strftime("%d/%m/%y")
    config['General']['timestamp'] = date_time.strftime("%Y-%m-%dT%H:%M:%S")
    if highTemp < config.getfloat('Temp', 'LowMax'):
        config['Temp']['LowMax'] = str(highTemp)
        config['Temp']['LMTime'] = time_stamp
    if lowTemp > config.getfloat('Temp', 'HighMin'):
        config['Temp']['HighMin'] = str(lowTemp)
        config['Temp']['HMTime'] = time_stamp
    if tempRange < config.getfloat('Temp', 'LowRange'):
        config['Temp']['LowRange'] = str(tempRange)
        config['Temp']['LowRangeTime'] = time_stamp
    if tempRange > config.getfloat('Temp', 'HighRange'):
        config['Temp']['HighRange'] = str(tempRange)
        config['Temp']['HighRangeTime'] = time_stamp
    
    with open(month_file, 'w') as configfile:
        config.write(configfile)
    configfile.close

#reset today.ini
def newDay(currentWx):

    for i in range(2,len(currentWx)):
        currentWx[i] = float(currentWx[i])
    
    config = configparser.ConfigParser()
    date_time = datetime.strptime(currentWx[0] + ' ' + currentWx[1],"%d/%m/%y %H:%M")
    prev_day = date_time - timedelta(days=1)
    time_stamp = prev_day.strftime("%d/%m/%y")

    config = configparser.ConfigParser()
    if config.read('records/today.ini') == []:
        config.read('records/default_ini/today.ini')
    else:
        tempRecords(currentWx)
    
    #Save yesterday.ini--------------------------------------------------------
    with open('records/yesterday.ini', 'w') as configfile:
        config.write(configfile)
    configfile.close
    #--------------------------------------------------------------------------
    
    config['General']['Date'] = date_time.strftime("%d/%m/%y")
    config['General']['Timestamp'] = date_time.strftime("%Y-%m-%dT%H:%M:%S")
    config['General']['CurrentYear'] = str(date_time.year)
    config['General']['CurrentMonth'] = date_time.strftime("%m")
    config['General']['CurrentDay'] = date_time.strftime("%d")
    
    
    config['Wind']['Speed'] = str(currentWx[6])
    config['Wind']['SpTime'] = date_time.strftime("%H:%M")
    config['Wind']['Gust'] = str(currentWx[7])
    config['Wind']['Time'] = date_time.strftime("%H:%M")
    config['Wind']['Windrun'] = str(currentWx[12])
    
    
    config['Temp']['Low'] = str(currentWx[2])
    config['Temp']['LTime'] = date_time.strftime("%H:%M")
    config['Temp']['High'] = str(currentWx[2])
    config['Temp']['HTime'] = date_time.strftime("%H:%M")
    config['Temp']['inLow'] = str(currentWx[8])
    config['Temp']['inLTime'] = date_time.strftime("%H:%M")
    config['Temp']['inHigh'] = str(currentWx[8])
    config['Temp']['inHTime'] = date_time.strftime("%H:%M")
    config['Temp']['Total'] = str(config.getfloat('Temp', 'Total') + currentWx[2])
    config['Temp']['Samples'] = str(config.getint('Temp', 'Samples') + 1)

    config['Pressure']['Low'] = str(currentWx[11])
    config['Pressure']['LTime'] = date_time.strftime("%H:%M")
    config['Pressure']['High'] = str(currentWx[11])
    config['Pressure']['HTime'] = date_time.strftime("%H:%M")

    config['Humidity']['Low'] = str(currentWx[3])
    config['Humidity']['LTime'] = date_time.strftime("%H:%M")
    config['Humidity']['High'] = str(currentWx[3])
    config['Humidity']['HTime'] = date_time.strftime("%H:%M")
    config['Humidity']['inLow'] = str(currentWx[9])
    config['Humidity']['inLTime'] = date_time.strftime("%H:%M")
    config['Humidity']['inHigh'] = str(currentWx[9])
    config['Humidity']['inHTime'] = date_time.strftime("%H:%M")
    
    config['WindChill']['Low'] = str(currentWx[13])
    config['WindChill']['LTime'] = date_time.strftime("%H:%M")

    config['Dewpoint']['Low'] = str(currentWx[4])
    config['Dewpoint']['LTime'] = date_time.strftime("%H:%M")
    config['Dewpoint']['High'] = str(currentWx[4])
    config['Dewpoint']['HTime'] = date_time.strftime("%H:%M")
    
    with open('records/today.ini', 'w') as configfile:
        config.write(configfile)
    configfile.close
    
    
#New month
def newMonth(currentWx):

    for i in range(2,len(currentWx)):
        currentWx[i] = float(currentWx[i])
    
    config = configparser.ConfigParser()
    time_stamp = currentWx[0] + ' ' + currentWx[1]
    date_time = datetime.strptime(time_stamp,"%d/%m/%y %H:%M")
    save_file = 'records/month' + str(date_time.strftime("%Y%m") + '.ini')
    config.read('records/default_ini/month.ini')
    
    config['General']['Date'] = time_stamp    
    
    config['Wind']['Speed'] = str(currentWx[6])
    config['Wind']['SpTime'] = time_stamp
    config['Wind']['Gust'] = str(currentWx[7])
    config['Wind']['Time'] = time_stamp
    config['Wind']['Windrun'] = str(currentWx[12])      #daily windrun record
    config['Wind']['WindrunTime'] = time_stamp
    
    
    config['Temp']['Low'] = str(currentWx[2])
    config['Temp']['LTime'] = time_stamp
    config['Temp']['High'] = str(currentWx[2])
    config['Temp']['HTime'] = time_stamp
    config['Temp']['LowMax'] = str(currentWx[2])
    config['Temp']['LMTime'] = time_stamp
    config['Temp']['HighMin'] = str(currentWx[2])
    config['Temp']['HMTime'] = time_stamp
    config['Temp']['LowRange'] = '999.0'
    config['Temp']['LowRangeTime'] = time_stamp
    config['Temp']['HighRange'] = '0.0'
    config['Temp']['HighRangeTime'] = time_stamp
    config['Temp']['inLow'] = str(currentWx[8])
    config['Temp']['inLTime'] = time_stamp
    config['Temp']['inHigh'] = str(currentWx[8])
    config['Temp']['inHTime'] = time_stamp

    config['Pressure']['Low'] = str(currentWx[11])
    config['Pressure']['LTime'] = time_stamp
    config['Pressure']['High'] = str(currentWx[11])
    config['Pressure']['HTime'] = time_stamp

    config['Humidity']['Low'] = str(currentWx[3])
    config['Humidity']['LTime'] = time_stamp
    config['Humidity']['High'] = str(currentWx[3])
    config['Humidity']['HTime'] = time_stamp
    config['Humidity']['inLow'] = str(currentWx[9])
    config['Humidity']['inLTime'] = time_stamp
    config['Humidity']['inHigh'] = str(currentWx[9])
    config['Humidity']['inHTime'] = time_stamp
    
    config['WindChill']['Low'] = str(currentWx[13])
    config['WindChill']['LTime'] = time_stamp

    config['Dewpoint']['Low'] = str(currentWx[4])
    config['Dewpoint']['LTime'] = time_stamp
    config['Dewpoint']['High'] = str(currentWx[4])
    config['Dewpoint']['HTime'] = time_stamp
    
    with open(save_file, 'w') as configfile:
        config.write(configfile)
    configfile.close
    
#New year
def newYear(currentWx):

    for i in range(2,len(currentWx)):
        currentWx[i] = float(currentWx[i])
    
    config = configparser.ConfigParser()
    time_stamp = currentWx[0] + ' ' + currentWx[1]
    date_time = datetime.strptime(time_stamp,"%d/%m/%y %H:%M")
    currentYear = str(date_time.year)
    year_file = 'records/year'+ currentYear + '.ini'
    config.read('records/default_ini/year.ini')
    
    config['General']['Date'] = time_stamp    
    
    config['Wind']['Speed'] = str(currentWx[6])
    config['Wind']['SpTime'] = time_stamp
    config['Wind']['Gust'] = str(currentWx[7])
    config['Wind']['Time'] = time_stamp
    config['Wind']['Windrun'] = str(currentWx[12])      #daily windrun record
    config['Wind']['WindrunTime'] = time_stamp
    
    
    config['Temp']['Low'] = str(currentWx[2])
    config['Temp']['LTime'] = time_stamp
    config['Temp']['High'] = str(currentWx[2])
    config['Temp']['HTime'] = time_stamp
    config['Temp']['LowMax'] = str(currentWx[2])
    config['Temp']['LMTime'] = time_stamp
    config['Temp']['HighMin'] = str(currentWx[2])
    config['Temp']['HMTime'] = time_stamp
    config['Temp']['LowRange'] = '999.0'
    config['Temp']['LowRangeTime'] = time_stamp
    config['Temp']['HighRange'] = '0.0'
    config['Temp']['HighRangeTime'] = time_stamp
    config['Temp']['inLow'] = str(currentWx[8])
    config['Temp']['inLTime'] = time_stamp
    config['Temp']['inHigh'] = str(currentWx[8])
    config['Temp']['inHTime'] = time_stamp

    config['Pressure']['Low'] = str(currentWx[11])
    config['Pressure']['LTime'] = time_stamp
    config['Pressure']['High'] = str(currentWx[11])
    config['Pressure']['HTime'] = time_stamp

    config['Humidity']['Low'] = str(currentWx[3])
    config['Humidity']['LTime'] = time_stamp
    config['Humidity']['High'] = str(currentWx[3])
    config['Humidity']['HTime'] = time_stamp
    config['Humidity']['inLow'] = str(currentWx[9])
    config['Humidity']['inLTime'] = time_stamp
    config['Humidity']['inHigh'] = str(currentWx[9])
    config['Humidity']['inHTime'] = time_stamp
    
    config['WindChill']['Low'] = str(currentWx[13])
    config['WindChill']['LTime'] = time_stamp

    config['Dewpoint']['Low'] = str(currentWx[4])
    config['Dewpoint']['LTime'] = time_stamp
    config['Dewpoint']['High'] = str(currentWx[4])
    config['Dewpoint']['HTime'] = time_stamp
    
    with open(year_file, 'w') as configfile:
        config.write(configfile)
    configfile.close

    
if __name__=="__main__":
    currentWx=['02/02/18', '23:30', 5.0, 10, 15, 12, 10, 12, 70, 20, 23, 777, 250, 35., -999, -999]
    updateAllTime()
    
