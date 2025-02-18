import os
import requests
import sys
import json
from itertools import groupby, islice
from datetime import datetime, timedelta
import time
from time import mktime


import logging


# *******************************************************************
# Debug Output defines
# Comment to enable/disable
# ********************************************************************
debug_all = True
#debug_all = False



#logging.basicConfig(level=logging.INFO)
#log = logging

logging.basicConfig(level=logging.ERROR)
log = logging







from splicer import Schema, Field




#TODO: make these consistant with the constants
# defined in nmea module, which ignores the 
# partition column
DEVICE=0
PARTITION=1
URL = 2
PGN = 3
TIMESTAMP=4
SOURCE=5




# Used for PGs 130311
def getSKTemperatureInstance(pgn_type, pgn_instance):

  path = ""
  pgninstanceString = ""
  
  if pgn_instance != "":
    pgninstanceString = str(pgn_instance) + '.'
  
  if pgn_type == 'Sea Temperature': 
    path = 'environment.water.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Temperature': 
    path = 'environment.outside.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Temperature': 
    path = 'environment.inside.' + pgninstanceString + 'temperature'
    
  elif pgn_type == 'Engine Room Temperature': 
    path = 'environment.inside.engineRoom.' + pgninstanceString + 'temperature'
 
  elif pgn_type == 'Main Cabin Temperature': 
    path = 'environment.inside.mainCabin.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Live Well': 
    path= 'tanks.liveWell.default.' + pgninstanceString + 'temperature'
    #pathWithIndex: 'tanks.liveWell.<index>.temperature'

  elif pgn_type == 'Bait Well': 
    path = 'tanks.baitWell.default.' + pgninstanceString + 'temperature'
    #pathWithIndex: 'tanks.baitWell.<index>.temperature'

  elif pgn_type == 'Refridgeration': 
    path = 'environment.inside.refrigerator.' + pgninstanceString + 'temperature'

  elif pgn_instance == 'Heating': 
    path = 'environment.inside.heating.' + pgninstanceString + 'temperature'

  elif pgn_instance == 'Dew Point': 
    path = 'environment.outside.' + pgninstanceString + 'dewPointTemperature'

  elif pgn_instance == 'Wind Chill A': 
    path = 'environment.outside.' + pgninstanceString + 'apparentWindChillTemperature'

  elif pgn_instance == 'Wind Chill T': 
    path = 'environment.outside.' + pgninstanceString + 'theoreticalWindChillTemperature'

  elif pgn_type == 'Heat Index': 
    path = 'environment.outside.' + pgninstanceString + 'heatIndexTemperature'

  elif pgn_type == 'Freezer': 
    path = 'environment.inside.freezer.' + pgninstanceString + 'temperature'
 
  elif pgn_type == 'EGT': 
    path = 'propulsion.exhaust.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Reserved 128': 
    path = 'propulsion.manifold.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Reserved 129': 
    path = 'propulsion.fuel.supply.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Reserved 130': 
    path = 'propulsion.fuel.return.' + pgninstanceString + 'temperature'
    
    
  elif pgn_type == 'Reserved 134': 
    path = 'propulsion.egt.manifold.' + pgninstanceString + 'temperature'
    
  elif pgn_type == 'Fuel Flow': 
    path = 'propulsion.fuelflow.' + pgninstanceString + 'temperature'    

  elif pgn_type == 'Inside Zone0': 
    path = 'environment.inside.0.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone1': 
    path = 'environment.inside.1.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone2': 
    path = 'environment.inside.2.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone3': 
    path = 'environment.inside.3.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone4': 
    path = 'environment.inside.4.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone5': 
    path = 'environment.inside.5.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone6': 
    path = 'environment.inside.6.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone7': 
    path = 'environment.inside.7.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone8': 
    path = 'environment.inside.8.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone9': 
    path = 'environment.inside.9.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone10': 
    path = 'environment.inside.10.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone11': 
    path = 'environment.inside.11.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone12': 
    path = 'environment.inside.12.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone13': 
    path = 'environment.inside.13.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone14': 
    path = 'environment.inside.14.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone15': 
    path = 'environment.inside.15.' + pgninstanceString + 'temperature'
    
  elif pgn_type == 'Outside Zone0': 
    path = 'environment.outside.0.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone1': 
    path = 'environment.outside.1.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone2': 
    path = 'environment.outside.2.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone3': 
    path = 'environment.outside.3.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone4': 
    path = 'environment.outside.4.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone5': 
    path = 'environment.outside.5.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone6': 
    path = 'environment.outside.6.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone7': 
    path = 'environment.outside.7.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone8': 
    path = 'environment.outside.8.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone9': 
    path = 'environment.outside.9.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone10': 
    path = 'environment.outside.10.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone11': 
    path = 'environment.outside.11.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone12': 
    path = 'environment.outside.12.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone13': 
    path = 'environment.outside.13.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone14': 
    path = 'environment.outside.14.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone15': 
    path = 'environment.outside.15.' + pgninstanceString + 'temperature'
    

  return path

# Used for PGs 130311
def getSKHumidityInstance(pgn_instance):

  path = ""
  
  if pgn_instance == 'Inside Humidity': 
    path = 'environment.inside.humidity'

  elif pgn_instance == 'Outside Humidity': 
    path = 'environment.outside.humidity'

  elif pgn_instance == 'Reserved': 
    path = 'environment.outside.humidity'

  return path

# Used fro PGNs 130306
def getSKWindSpeedInstance(pgn_instance):

  path = ""
  
  if pgn_instance == 'TWIND True North': 
    path = 'environment.wind.speedTrue'

  elif pgn_instance == 'TWIND Mag North': 
    path = 'environment.wind.speedTrue'

  elif pgn_instance == 'Apparent Wind': 
    path = 'environment.wind.speedApparent'
    
  elif pgn_instance == 'TWIND VCGR': 
    path = 'environment.wind.speedOverGround'


  return path

# Used fro PGNs 130306
def getSKWindDirectionInstance(pgn_instance):

  path = ""
  
  if pgn_instance == 'TWIND True North': 
    path = 'environment.wind.directionTrue'

  elif pgn_instance == 'TWIND Mag North': 
    path = 'environment.wind.directionMagnetic'

  elif pgn_instance == 'Apparent Wind': 
    path = 'environment.wind.angleTrueWater'

  return path

# Used fro PGNs 129026
def getSKCOGInstance(pgn_instance):

  path = ""
  
  if pgn_instance == 'True': 
    path = 'navigation.courseOverGroundTrue'

  elif pgn_instance == 'Magnetic': 
    path = 'navigation.courseOverGroundMagnetic'


  return path

# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Environmential Data
# ********************************************************************************************
def createSIGKpathPGN130311(n2kkey, pgn_payload):

  try:
    
    if n2kkey == 'temperature':
      skpath = getSKTemperatureInstance(pgn_payload.get('temperature_instance'), "")
      if pgn_payload.get('temperature') is not None:
        skvalue = pgn_payload.get('temperature')
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'atmospheric_pressure':
      skpath = 'environment.outside.pressure'
      if pgn_payload.get('atmospheric_pressure') is not None:
        skvalue = pgn_payload.get('atmospheric_pressure')
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'humidity':
      skpath = getSKHumidityInstance(pgn_payload.get('humidity_instance'))        
      if pgn_payload.get('humidity') is not None:
        skvalue = ( pgn_payload.get('humidity') / 100)
        return {"path":skpath,"value":skvalue}
      else:
        return {}

  except:
    if debug_all: log.info('sync: createSIGKpathPGN130311 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}
 
# ********************************************************************************************
# Parses pgn_payload looking for vales based on n2kkey and fromats into signalk string
def createSIGKpath(pgn_number, n2kkey, pgn_payload):


  match pgn_number:

    # Environmental Data
    case 130311:
      return createSIGKpathPGN130311(n2kkey, pgn_payload)


    case _:
      return {}

# ********************************************************************************************





