import os
from os import environ
from os import environ as env, path
#import pylibmc
import bmemcached
import sys
import re
#import pyarrow as pa
import json

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


def parse_idkey(deviceid, idkey):

    match idkey:

        case "Engine.0.RPM":

            instance = 0
            serieskeys=" deviceid='"
            serieskeys= serieskeys + deviceid + "' AND "
            serieskeys= serieskeys +  " (sensor='engine_parameters_rapid_update') AND "
            serieskeys= serieskeys +  " (instance='" + instance + "') "
            value = "speed"
            return value, serieskeys

        case "Engine.0.engineTemperature":

            instance = 0
            serieskeys=" deviceid='"
            serieskeys= serieskeys + deviceid + "' AND "
            serieskeys= serieskeys +  " (sensor='engine_parameters_dynamic') AND "
            serieskeys= serieskeys +  " (instance='" + instance + "') "
            value = "engine_temp"
            return value, serieskeys
        
        case "Engine.0.enginePressure":

            instance = 0
            serieskeys=" deviceid='"
            serieskeys= serieskeys + deviceid + "' AND "
            serieskeys= serieskeys +  " (sensor='engine_parameters_dynamic') AND "
            serieskeys= serieskeys +  " (instance='" + instance + "') "
            value = "oil_pressure"
            return value, serieskeys

        case "Engine.0.oilTemperature":

            instance = 0
            serieskeys=" deviceid='"
            serieskeys= serieskeys + deviceid + "' AND "
            serieskeys= serieskeys +  " (sensor='engine_parameters_dynamic') AND "
            serieskeys= serieskeys +  " (instance='" + instance + "') "
            value = "oil_temperature"
            return value, serieskeys
        
        case "Engine.0.FuelRate":

            instance = 0
            serieskeys=" deviceid='"
            serieskeys= serieskeys + deviceid + "' AND "
            serieskeys= serieskeys +  " (sensor='engine_parameters_dynamic') AND "
            serieskeys= serieskeys +  " (instance='" + instance + "') "
            value = "fuel_rate"
            return value, serieskeys        

        # If an exact match is not confirmed, this last case will be used if provided
        case _:
            return ""


def idkey_query(deviceid, idkey, interval):

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)    

    epochtimes = getepochtimes(interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]

    value, serieskeys = parse_idkey(deviceid, idkey):

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

    return query

 
