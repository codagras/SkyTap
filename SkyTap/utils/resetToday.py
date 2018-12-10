# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 20:51:18 2018

@author: codagras
"""
from datetime import datetime
import configparser
date_time = datetime.now()

config = configparser.ConfigParser()
config.read('../records/today.ini')


config['Wind']['Speed'] = '-999.9'
config['Wind']['SpTime'] = date_time.strftime("%H:%M")
config['Wind']['Gust'] = '-999.9'
config['Wind']['Time'] = date_time.strftime("%H:%M")
config['Wind']['Windrun'] = '0.0'

config['Temp']['Low'] = '999.9'
config['Temp']['LTime'] = date_time.strftime("%H:%M")
config['Temp']['High'] = '-999.9'
config['Temp']['HTime'] = date_time.strftime("%H:%M")
config['Temp']['inLow'] = '999.9'
config['Temp']['inLTime'] = date_time.strftime("%H:%M")
config['Temp']['inHigh'] = '-999.9'
config['Temp']['inHTime'] = date_time.strftime("%H:%M")
config['Temp']['Total'] = '0.0'
config['Temp']['Samples'] = '0'

config['Pressure']['Low'] = '9999.9'
config['Pressure']['LTime'] = date_time.strftime("%H:%M")
config['Pressure']['High'] = '-9999.9'
config['Pressure']['HTime'] = date_time.strftime("%H:%M")

config['Humidity']['Low'] = '999.9'
config['Humidity']['LTime'] = date_time.strftime("%H:%M")
config['Humidity']['High'] = '-999.9'
config['Humidity']['HTime'] = date_time.strftime("%H:%M")
config['Humidity']['inLow'] = '999.9'
config['Humidity']['inLTime'] = date_time.strftime("%H:%M")
config['Humidity']['inHigh'] = '-999.9'
config['Humidity']['inHTime'] = date_time.strftime("%H:%M")

config['WindChill']['Low'] = '999.9'
config['WindChill']['LTime'] = date_time.strftime("%H:%M")

config['Dewpoint']['Low'] = '999.9'
config['Dewpoint']['LTime'] = date_time.strftime("%H:%M")
config['Dewpoint']['High'] = '-999.9'
config['Dewpoint']['HTime'] = date_time.strftime("%H:%M")
    
with open('../records/today.ini', 'w') as configfile:
    config.write(configfile)
configfile.close
