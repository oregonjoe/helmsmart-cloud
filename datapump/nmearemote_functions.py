import os
from os import environ
from os import environ as env, path
#import pylibmc
import bmemcached
import sys
import re
#import pyarrow as pa
import json

import datetime
from datetime import timezone
import time
from time import mktime
from zoneinfo import ZoneInfo

import logging
# *******************************************************************
# Debug Output defines
# Comment to enable/disable
# ********************************************************************
#debug_all = False
debug_all = True

logging.basicConfig(level=logging.INFO)  
#logging.basicConfig(level=logging.DEBUG)
log = logging



def getepochtimes(Interval):



    log.info('nmearemote_functions:  getepochtimes Interval %s:  ', Interval)

    epochtimes=[]
    starttime = 0

    
    try:
        # if 0 then use current time 
        if starttime == 0:
            nowtime = datetime.datetime.now()
            endepoch =  int(time.time())

            if Interval== "1min":
                resolution = 60
                startepoch = endepoch - (resolution * 2)
                oldtime = datetime.datetime.now() - datetime.timedelta(minutes=2)
            elif Interval == "2min":
                resolution = 60*2
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(minutes=3)                
            elif Interval == "5min":
                resolution = 60*5
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(minutes=5)
            elif Interval== "10min":
                resolution = 60*10
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(minutes=10)
            elif Interval == "15min":
                resolution = 60*15
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(minutes=15)
            elif Interval== "30min":
                resolution = 60*30
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(minutes=30)
            elif Interval== "1hour":
                resolution = 60*60
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(hours=1)
                
            elif Interval == "2hour":
                resolution = 60*60*2
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(hours=2)

                
            elif Interval == "3hour":
                resolution = 60*60*3
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(hours=3)                
                
            elif Interval == "4hour":
                resolution = 60*60*4
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(hours=4)

                
            elif Interval == "6hour":
                resolution = 60*60*6
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(hours=6)
            elif Interval == "8hour":
                resolution = 60*60*8
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(hours=8)
            elif Interval == "12hour":
                resolution = 60*60*12
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(hours=12)
            elif Interval == "1day":
                resolution = 60*60*24
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(days=1)
            elif Interval == "2day":
                resolution = 60*60*24*2
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(days=2)                
            elif Interval== "7day":
                resolution = 60*60*24*7
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(days=7)
            elif Interval == "1month":
                resolution = 60*60*24*30
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(months=1)
            else:
                resolution = 60
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(minutes=2)

                
        epochtimes.append(startepoch)
        epochtimes.append(endepoch)
        epochtimes.append(resolution)

    except TypeError as e:
        log.info('nmearemote_functions: TypeError in geting getepochtimes parameters %s:  ', Interval)
        log.info('nmearemote_functions: TypeError in geting getepochtimes parameters %s:  ' % str(e))
            
    except KeyError as e:
        log.info('nmearemote_functions: KeyError in geting getepochtimes parameters %s:  ', Interval)
        log.info('nmearemote_functions: KeyError in geting getepochtimes parameters %s:  ' % str(e))

    except NameError as e:
        log.info('nmearemote_functions: NameError in geting getepochtimes parameters %s:  ', Interval)
        log.info('freeboard: NameError in geting getepochtimes parameters %s:  ' % str(e))
            
    except IndexError as e:
        log.info('nmearemote_functions: IndexError in geting getepochtimes parameters %s:  ', Interval)
        log.info('nmearemote_functions: IndexError in geting getepochtimes parameters %s:  ' % str(e))  


    except:
        log.info('nmearemote_functions: Error in geting  getepochtimes %s:  ', Interval)
        e = sys.exc_info()[0]
        log.info('nmearemote_functions: Error in geting getepochtimes parameters %s:  ' % str(e))

    return(epochtimes)



def parse_idkey(deviceid, idkey):

    match idkey:

        case "Engine.0.RPM":

            instance = "0"
            serieskeys=" deviceid='"
            serieskeys= serieskeys + deviceid + "' AND "
            serieskeys= serieskeys +  " (sensor='engine_parameters_rapid_update') AND "
            serieskeys= serieskeys +  " (instance='" + instance + "') "
            value = "speed"
            units = "Hz"
            return value, serieskeys, units

        case "Engine.0.engineTemperature":

            instance = "0"
            serieskeys=" deviceid='"
            serieskeys= serieskeys + deviceid + "' AND "
            serieskeys= serieskeys +  " (sensor='engine_parameters_dynamic') AND "
            serieskeys= serieskeys +  " (instance='" + instance + "') "
            value = "engine_temp"
            units = "°K"
            #units = chr(176).encode('utf-8') + "K"
            return value, serieskeys, units
        
        case "Engine.0.oilPressure":

            instance = "0"
            serieskeys=" deviceid='"
            serieskeys= serieskeys + deviceid + "' AND "
            serieskeys= serieskeys +  " (sensor='engine_parameters_dynamic') AND "
            serieskeys= serieskeys +  " (instance='" + instance + "') "
            value = "oil_pressure"
            units = "kPa"
            return value, serieskeys, units

        case "Engine.0.oilTemperature":

            instance = "0"
            serieskeys=" deviceid='"
            serieskeys= serieskeys + deviceid + "' AND "
            serieskeys= serieskeys +  " (sensor='engine_parameters_dynamic') AND "
            serieskeys= serieskeys +  " (instance='" + instance + "') "
            value = "oil_temperature"
            units = chr(176) + "K"
            return value, serieskeys, units
        
        case "Engine.0.FuelRate":

            instance = "0"
            serieskeys=" deviceid='"
            serieskeys= serieskeys + deviceid + "' AND "
            serieskeys= serieskeys +  " (sensor='engine_parameters_dynamic') AND "
            serieskeys= serieskeys +  " (instance='" + instance + "') "
            value = "fuel_rate"
            units = "l/h"
            return value, serieskeys, units  

        # If an exact match is not confirmed, this last case will be used if provided
        case _:
            return "","",""


def idkey_query(deviceid, idkey, interval):

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)    

    epochtimes = getepochtimes(interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]

    value, serieskeys, units = parse_idkey(deviceid, idkey)
    log.info("nmearemote_functions parse_idkey data value %s, serieskeys %s, units %s", value, serieskeys, units)

    
    if value == "" or serieskeys == "":
        return "",""

    #'select  percentile(temperature,50)
    """
    query = ('select  percentile({}, 50) AS value from {} '
               'where {} AND time > {}s and time < {}s '
               'group by time({}s)') \
          .format( value, measurement, serieskeys,
                  startepoch, endepoch,
                  resolution) 
    """
    
    query = ('select  percentile({}, 50) AS value from {} '
                   'where {} AND time > {}s and time < {}s ') \
              .format( value, measurement, serieskeys,
                      startepoch, endepoch)

    log.info("nmearemote_functions parse_idkey data Query %s", query)    

    return query, units

 
