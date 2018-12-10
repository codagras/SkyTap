# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 15:45:09 2018

@author: codagras
"""
from datetime import datetime
import configparser
date_time = datetime.now()

config = configparser.ConfigParser()
time_stamp = datetime.strftime(date_time,"%d-%m-%Y %H:%M:%S")
save_file = '../records/month' + str(date_time.strftime("%Y%m") + '.ini')
config.read(save_file)
  

config['Wind']['Speed'] = '0.0'
config['Wind']['SpTime'] = time_stamp
config['Wind']['Gust'] = '0.0'
config['Wind']['Time'] = time_stamp
config['Wind']['Windrun'] = '0.0'      #daily windrun record
config['Wind']['WindrunTime'] = time_stamp

config['Temp']['Low'] = '999.9'
config['Temp']['LTime'] = time_stamp
config['Temp']['High'] = '-999.9'
config['Temp']['HTime'] = time_stamp
config['Temp']['inLow'] = '999.9'
config['Temp']['inLTime'] = time_stamp
config['Temp']['inHigh'] = '-999.9'
config['Temp']['inHTime'] = time_stamp
config['Temp']['lowmax'] = '999.9'
config['Temp']['lmtime'] = time_stamp
config['Temp']['highmin'] = '-999.9'
config['Temp']['hmtime'] = time_stamp
config['Temp']['lowrange'] = '999.9'
config['Temp']['lowrangetime'] = time_stamp
config['Temp']['highrange'] = '-999.9'
config['Temp']['highrangetime'] = time_stamp

config['Pressure']['Low'] = '9999.9'
config['Pressure']['LTime'] = time_stamp
config['Pressure']['High'] = '-9999.9'
config['Pressure']['HTime'] = time_stamp

config['Humidity']['Low'] = '999.9'
config['Humidity']['LTime'] = time_stamp
config['Humidity']['High'] = '-999.9'
config['Humidity']['HTime'] = time_stamp
config['Humidity']['inLow'] = '999.9'
config['Humidity']['inLTime'] = time_stamp
config['Humidity']['inHigh'] = '-999.9'
config['Humidity']['inHTime'] = time_stamp

config['WindChill']['Low'] = '999.9'
config['WindChill']['LTime'] = time_stamp

config['Dewpoint']['Low'] = '999.9'
config['Dewpoint']['LTime'] = time_stamp
config['Dewpoint']['High'] = '-999.9'
config['Dewpoint']['HTime'] = time_stamp

with open(save_file, 'w') as configfile:
    config.write(configfile)
configfile.close
