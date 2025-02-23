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
debug_all = False



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

  elif pgn_type == 'Heating': 
    path = 'environment.inside.heating.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Dew Point': 
    path = 'environment.outside.' + pgninstanceString + 'dewPointTemperature'

  elif pgn_type == 'Wind Chill A': 
    path = 'environment.outside.' + pgninstanceString + 'apparentWindChillTemperature'

  elif pgn_type == 'Wind Chill T': 
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
# Converts NMEA 2000 field descriptions to Signal
# Wind Data
# ********************************************************************************************
def createSIGKpathPGN130306(n2kkey, pgn_payload):

  try:
    
    if n2kkey == 'wind_speed':
      skpath = getSKWindSpeedInstance(pgn_payload.get('wind_reference'))
      if pgn_payload.get('wind_speed') is not None:
        skvalue = pgn_payload.get('wind_speed') /100
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'wind_direction':
      skpath = getSKWindDirectionInstance(pgn_payload.get('wind_reference'))
      if pgn_payload.get('wind_direction') is not None:
        skvalue = pgn_payload.get('wind_direction')  / 57.30659025787966
        return {"path":skpath,"value":skvalue}
      else:
        return {}    

  except:
    if debug_all: log.info('sync: createSIGKpathPGN130306 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}

# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# SystemTime
# ********************************************************************************************
def createSIGKpathPGN126992(n2kkey, pgn_payload):

  try:
    
    if n2kkey == 'datetime' and pgn_payload.get('time_source') == 'GPS':
      skpath = 'navigation.datetime'
      skvalue = pgn_payload.get('datetime')
      return {"path":skpath,"value":skvalue}
    else:
      return {}  

  except:
    if debug_all: log.info('sync: createSIGKpathPGN126992 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}


# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Water Depth
# ********************************************************************************************
def createSIGKpathPGN128267(n2kkey, pgn_payload):

  try:
    
    if n2kkey == 'depth':
      skpath = 'environment.depth.belowSurface'
      if pgn_payload.get('depth') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('depth') * 10))
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'transducer_offset':
      skpath = 'environment.depth.belowTransducer'
      if pgn_payload.get('transducer_offset') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('transducer_offset') * 10))
        return {"path":skpath,"value":skvalue}
      else:
        return {} 

  except:
    if debug_all: log.info('sync: createSIGKpathPGN128267 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}


# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# COG/SOG
# ********************************************************************************************
def createSIGKpathPGN129026(n2kkey, pgn_payload):

  try:
    
    if n2kkey == 'speed_over_ground':
      skpath = 'navigation.speedOverGround'
      if pgn_payload.get('course_over_ground') is not None:
        skvalue = pgn_payload.get('speed_over_ground')
        skvalue = float("{0:.2f}".format(pgn_payload.get('speed_over_ground') ))
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'course_over_ground':
      skpath = getSKCOGInstance(pgn_payload.get('cog_reference'))
      if pgn_payload.get('course_over_ground') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('course_over_ground') / 57.30659025787966))
        return {"path":skpath,"value":skvalue}
      else:
        return {}

  except:
    if debug_all: log.info('sync: createSIGKpathPGN128267 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}

# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Heading 0x1F112
# ********************************************************************************************
def createSIGKpathPGN127250(n2kkey, pgn_payload):

  try:
    
    skreference =  pgn_payload.get('heading_reference')

    if n2kkey == 'heading' and skreference =='True':
      skpath = 'navigation.headingTrue'
      if pgn_payload.get('heading') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('heading') / 57.30659025787966))
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'heading' and skreference =='Magnetic':
      skpath = 'navigation.headingMagnetic'
      if pgn_payload.get('heading') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('heading') / 57.30659025787966))
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'variation':
      skpath ='navigation.magneticVariation'
      if pgn_payload.get('variation') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('variation') / 57.30659025787966))
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'deviation':
      skpath ='navigation.magneticDeviation'
      if pgn_payload.get('deviation') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('deviation') / 57.30659025787966))
        return {"path":skpath,"value":skvalue}
      else:
        return {}

  except:
    if debug_all: log.info('sync: createSIGKpathPGN127250 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}

# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Rate of Turn 0x1F113
# ********************************************************************************************
def createSIGKpathPGN127251(n2kkey, pgn_payload):

  try:
    
    if n2kkey == 'rate_of_turn':
      skpath = 'navigation.rateOfTurn'
      if pgn_payload.get('rate_of_turn') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('rate_of_turn') / 57.30659025787966))
        return {"path":skpath,"value":skvalue}
      else:
        return {}

  except:
    if debug_all: log.info('sync: createSIGKpathPGN127251 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}


# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Rudder 0x1F10D
# ********************************************************************************************
def createSIGKpathPGN127245(n2kkey, pgn_payload):

  try:
    
    if n2kkey == 'rate_of_turn':
      skpath = 'navigation.rateOfTurn'
      if pgn_payload.get('rate_of_turn') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('rate_of_turn') / 57.30659025787966))
        return {"path":skpath,"value":skvalue}
      else:
        return {}

  except:
    if debug_all: log.info('sync: createSIGKpathPGN127245 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}







# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Position Rapid 0x1F119
# ********************************************************************************************
def createSIGKpathPGN129025(n2kkey, pgn_payload):

  try:
    
    if n2kkey == 'lat' :
      
      # check if we it least have one value
      if pgn_payload.get('lat') is None and  pgn_payload.get('lng') is None :
        return {}

      #set path fpr all 2 values
      skpath = 'navigation.position'
      
      skvalues = {}
      #Now get values

      if pgn_payload.get('lat') is not None:
        skvalues['latitude'] = float("{0:.8f}".format(pgn_payload.get('lat') ))
         
      if pgn_payload.get('lng') is not None:
        skvalues['longitude'] = float("{0:.8f}".format(pgn_payload.get('lng') ))

      return  {"path":skpath,"value":skvalues}
      
    else:
      return {}

  except:
    if debug_all: log.info('sync: createSIGKpathPGN129025 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}


# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Attitude 0x1F119
# ********************************************************************************************
def createSIGKpathPGN127257(n2kkey, pgn_payload):

  try:
    
    skYaw = None
    skPitch = None
    skRoll = None

    if n2kkey == 'yaw' or n2kkey == 'pitch' or n2kkey == 'roll':
      
      # check if we it least have one value
      if pgn_payload.get('yaw') is None and  pgn_payload.get('pitch') is None and  pgn_payload.get('roll') is None:
        return {}

      #set path fpr all 3 values
      skpath = 'navigation.attitude'
      
      skvalues = {}
      #Now get values

      if pgn_payload.get('yaw') is not None:
        skvalues['yaw'] = float("{0:.2f}".format(pgn_payload.get('yaw') / 57.30659025787966))
         
      if pgn_payload.get('pitch') is not None:
        skvalues['pitch'] = float("{0:.2f}".format(pgn_payload.get('pitch') / 57.30659025787966))

      if pgn_payload.get('roll') is not None:
        skvalues['roll'] = float("{0:.2f}".format(pgn_payload.get('roll') / 57.30659025787966))

      return {"path":skpath,"value":skvalues}
      
    else:
      return {}

  except:
    if debug_all: log.info('sync: createSIGKpathPGN127257 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}



# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Water Speed  0x1F503
# ********************************************************************************************
def createSIGKpathPGN128259(n2kkey, pgn_payload):

  try:
    
    if n2kkey == 'waterspeed':
      skpath = 'navigation.speedThroughWater'
      if pgn_payload.get('waterspeed') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('waterspeed') * 100))
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'groundspeed':
      skpath = 'navigation.speedOverGround'
      if pgn_payload.get('groundspeed') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('groundspeed') * 100))
        return {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'type_reference':
      skpath = 'navigation.speedThroughWaterReferenceType'
      if pgn_payload.get('type_reference') is not None:
        skvalue = pgn_payload.get('type_reference') 
        return {"path":skpath,"value":skvalue}
      else:
        return {}


  except:
    if debug_all: log.info('sync: createSIGKpathPGN128259 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}


# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Engine Rapid Data  0x1200
# ********************************************************************************************
def createSIGKpathPGN127488(n2kkey, pgn_payload):

  try:
    
    skEngineId = pgn_payload.get('engine_id')
    
    if n2kkey == 'speed':
      skpath = 'propulsion.' + str(skEngineId) + '.revolutions'
      if pgn_payload.get('speed') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('speed') / 240))
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    
    elif n2kkey == 'boost_presure':
      skpath = 'propulsion.' + str(skEngineId)  + '.boostPressure'
      if pgn_payload.get('boost_presure') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('boost_presure') * 100))
        return {"path":skpath,"value":skvalue}
      else:
        return {}
      
    elif n2kkey == 'tilt_or_trim':
      skpath = 'propulsion.' + str(skEngineId)  + '.drive.trimState'
      if pgn_payload.get('tilt_or_trim') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('tilt_or_trim') * 0.01))
        return {"path":skpath,"value":skvalue}
      else:
        return {}


  except:
    if debug_all: log.info('sync: createSIGKpathPGN127488 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}


# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Engine Rapid Dynamic Data  0x1201
# ********************************************************************************************
def createSIGKpathPGN127489(n2kkey, pgn_payload):

  try:
    
    skEngineId = pgn_payload.get('engine_id')
    
    if n2kkey == 'oil_pressure':
      skpath = 'propulsion.' + str(skEngineId) + '.oilPressure'
      if pgn_payload.get('oil_pressure') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('oil_pressure') * 100)) 
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'oil_temp':
      skpath = 'propulsion.' + str(skEngineId) + '.oilTemperature'
      if pgn_payload.get('oil_temp') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('oil_temp') * 0.01))
        return {"path":skpath,"value":skvalue}
      else:
        return {}
      
    elif n2kkey == 'engine_temp':
      skpath = 'propulsion.' + str(skEngineId) + '.temperature'
      if pgn_payload.get('engine_temp') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('engine_temp') * 0.01))
        return {"path":skpath,"value":skvalue}
      else:
        return {}
  
    
    elif n2kkey == 'alternator_potential':
      skpath = 'propulsion.' + str(skEngineId) + '.alternatorVoltage'
      if pgn_payload.get('alternator_potential') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('alternator_potential') * 0.01))
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'fuel_rate':
      skpath = 'propulsion.' + str(skEngineId) + '.fuel.rate'
      if pgn_payload.get('fuel_rate') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('fuel_rate') / 3600000))
        return {"path":skpath,"value":skvalue}
      else:
        return {}
      
    elif n2kkey == 'total_engine_hours':
      skpath = 'propulsion.' + str(skEngineId) + '.runTime'
      if pgn_payload.get('total_engine_hours') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('total_engine_hours') * 1))
        return {"path":skpath,"value":skvalue}
      else:
        return {}
  
    
    elif n2kkey == 'coolant_pressure':
      skpath = 'propulsion.' + str(skEngineId) + '.coolantPressures'
      if pgn_payload.get('coolant_pressure') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('coolant_pressure') * 1000))
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'fuel_pressure':
      skpath = 'propulsion.' + str(skEngineId) + '.fuel.pressure'
      if pgn_payload.get('fuel_pressure') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('fuel_pressure') * 1000))
        return {"path":skpath,"value":skvalue}
      else:
        return {}
      
    elif n2kkey == 'percent_engine_load':
      skpath = 'propulsion.' + str(skEngineId) + '.engineLoad'
      if pgn_payload.get('percent_engine_load') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('percent_engine_load') * 0.01))
        return {"path":skpath,"value":skvalue}
      else:
        return {}
  
     
    elif n2kkey == 'percent_engine_torque':
      skpath = 'propulsion.' + str(skEngineId) + '.engineTorque'
      if pgn_payload.get('percent_engine_torque') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('percent_engine_torque') * 0.01))
        return {"path":skpath,"value":skvalue}
      else:
        return {}



  except:
    if debug_all: log.info('sync: createSIGKpathPGN127489 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}



# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Trip Parameters, Engine 0x1F209
# ********************************************************************************************
def createSIGKpathPGN127497(n2kkey, pgn_payload):

  try:
    
    skinstance = pgn_payload.get('instance')

    #SignalK Fuel Rates are Cubic Meter/sec
    # NMEA 2000 is liters / hour  =( 1/(60*60))/1000
    
    if n2kkey == 'instantaneous_fuel_economy':
      skpath = 'propulsion.' + str(skinstance) + '.fuel.rate'
      if pgn_payload.get('instantaneous_fuel_economy') is not None:
        skvalue = float("{0:.8f}".format(pgn_payload.get('instantaneous_fuel_economy') * .00000002777))
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'fuel_rate_economy':
      skpath = 'propulsion.' + str(skinstance)+ '.fuel.economyRate'
      if pgn_payload.get('fuel_rate_economy') is not None:
        skvalue = float("{0:.8f}".format(pgn_payload.get('fuel_rate_economy') *  .00000002777))  
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'fuel_rate_average':
      skpath = 'propulsion.' + str(skinstance)+ '.fuel.avarageRate'
      if pgn_payload.get('fuel_rate_average') is not None:
        skvalue = float("{0:.8f}".format(pgn_payload.get('fuel_rate_average') *  .00000002777))  
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'trip_fuel_used':
      skpath = 'propulsion.' + str(skinstance)+ '.fuel.used'
      if pgn_payload.get('trip_fuel_used') is not None:
        skvalue = float("{0:.4f}".format(pgn_payload.get('trip_fuel_used') * 0.001))  
        return {"path":skpath,"value":skvalue}
      else:
        return {}


  except:
    if debug_all: log.info('sync: createSIGKpathPGN127497 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}


# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Transmission Parameters, Dynamic 0x1F205
# ********************************************************************************************
def createSIGKpathPGN127493(n2kkey, pgn_payload):

  try:
    
    skinstance = pgn_payload.get('instance')
    
    if n2kkey == 'oil_pressure':
      skpath = 'propulsion.' + str(skinstance) + '.transmission.oilPressure'
      if pgn_payload.get('oil_pressure') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('oil_pressure') * 100))
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'oil_temp':
      skpath = 'propulsion.' + str(skinstance)+ '.transmission.oilTemperature'
      if pgn_payload.get('oil_temp') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('oil_temp') * 0.1))  
        return {"path":skpath,"value":skvalue}
      else:
        return {}
      


  except:
    if debug_all: log.info('sync: createSIGKpathPGN127493error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}




# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Battery Status Data 0x1F214
# ********************************************************************************************
def createSIGKpathPGN127508(n2kkey, pgn_payload):

  try:
    
    skinstance = pgn_payload.get('instance')
    
    if n2kkey == 'voltage':
      skpath = 'electrical.batteries.' + str(skinstance) + '.voltage'
      if pgn_payload.get('voltage') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('voltage') * 0.01))
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'current':
      skpath = 'electrical.batteries.' + str(skinstance)+ '.current'
      if pgn_payload.get('current') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('current') * 0.01))  
        return {"path":skpath,"value":skvalue}
      else:
        return {}
      
    elif n2kkey == 'temperature':
      skpath = 'electrical.batteries.' + str(skinstance) + '.temperature'
      if pgn_payload.get('temperature') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('temperature') * 0.01))
        return {"path":skpath,"value":skvalue}
      else:
        return {}

  except:
    if debug_all: log.info('sync: createSIGKpathPGN127508 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}

# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Temperature Data 0x1FD08
# ********************************************************************************************
def createSIGKpathPGN130312(n2kkey, pgn_payload):

  try:
    
      if n2kkey == 'actual_temperature':
        skpath = getSKTemperatureInstance(pgn_payload.get('temperature_source'), pgn_payload.get('temperature_instance'))
        if pgn_payload.get('actual_temperature') is not None:
          skvalue = float("{0:.2f}".format(pgn_payload.get('actual_temperature') * 1.0))
          return {"path":skpath,"value":skvalue}
        else:
          return {}

  except:
    if debug_all: log.info('sync: createSIGKpathPGN130312 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}

# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Humidity Data 0x1FD09
# ********************************************************************************************
def createSIGKpathPGN130313(n2kkey, pgn_payload):

  try:


    if n2kkey == 'humidity':
      skpath = getSKHumidityInstance(pgn_payload.get('humidity_instance'))        
      if pgn_payload.get('humidity') is not None:
        skvalue = ( pgn_payload.get('humidity') / 100)
        return {"path":skpath,"value":skvalue}
      else:
        return {}


  except:
    if debug_all: log.info('sync: createSIGKpathPGN130313 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}


# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Pressure Data 0x1FD0A
# ********************************************************************************************
def createSIGKpathPGN130314(n2kkey, pgn_payload):

  try:
    
    if n2kkey == 'atmospheric_pressure':
      skpath = 'environment.outside.pressure'
      if pgn_payload.get('atmospheric_pressure') is not None:
        skvalue = pgn_payload.get('atmospheric_pressure')
        return {"path":skpath,"value":skvalue}
      else:
        return {}

  except:
    if debug_all: log.info('sync: createSIGKpathPGN130314 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}



# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Temperature Extended Data 0x1FD0C
# ********************************************************************************************
def createSIGKpathPGN130316(n2kkey, pgn_payload):

  try:
    
      if n2kkey == 'actual_temperature':
        skpath = getSKTemperatureInstance(pgn_payload.get('temperature_source'), pgn_payload.get('temperature_instance'))
        if pgn_payload.get('actual_temperature') is not None:
          skvalue = float("{0:.2f}".format(pgn_payload.get('actual_temperature') * 1.0))
          return {"path":skpath,"value":skvalue}
        else:
          return {}

  except:
    if debug_all: log.info('sync: createSIGKpathPGN130316 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}

# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Fluid Level Data 0x1F211
# ********************************************************************************************
def createSIGKpathPGN127505(n2kkey, pgn_payload):

  try:
    
    skinstance = pgn_payload.get('instance')
    n2ktype = str(pgn_payload.get('type'))

    if n2ktype == '0':
      sktype = 'fuel'
    elif n2ktype == '1':
      sktype = 'freshWater'
    elif n2ktype == '2':
      sktype = 'wasteWater'
    elif n2ktype == '3':
      sktype = 'liveWell'
    elif n2ktype == '4':
      sktype = 'lubrication'
    elif n2ktype == '5':
      sktype = 'blackWater'
    else:
      sktype = 'reserved'


    
    if n2kkey == 'level':
      skpath = 'tanks.' + sktype + '.' + str(skinstance) + '.currentLevel'
      if pgn_payload.get('level') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('level') * 0.00004))
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'tank_capacity':
      skpath = 'tanks.' + sktype + '.' + str(skinstance) + '.capacity'
      if pgn_payload.get('tank_capacity') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('tank_capacity') * 0.01))
        return {"path":skpath,"value":skvalue}
      else:
        return {}
      

  except:
    if debug_all: log.info('sync: createSIGKpathPGN127505 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}


# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Switch State Data 0x1F20D
# ********************************************************************************************
def createSIGKpathPGN127501(n2kkey, pgn_payload):

  try:
    
    skinstance = pgn_payload.get('instance')

    if int(skinstance) >= 128:
      sktype = "mesh."
    else:
      sktype = "hub."

    if n2kkey == 'indic01':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.0.state'
      if pgn_payload.get('indic01') is not None:
        skvalue = int(pgn_payload.get('indic01'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'indic02':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.1.state'
      if pgn_payload.get('indic02') is not None:
        skvalue = int(pgn_payload.get('indic02'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}

      

    elif n2kkey == 'indic03':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.2.state'
      if pgn_payload.get('indic03') is not None:
        skvalue = int(pgn_payload.get('indic03'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic04':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.3.state'
      if pgn_payload.get('indic04') is not None:
        skvalue = int(pgn_payload.get('indic04'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic05':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.4.state'
      if pgn_payload.get('indic05') is not None:
        skvalue = int(pgn_payload.get('indic05'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic06':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.5.state'
      if pgn_payload.get('indic06') is not None:
        skvalue = int(pgn_payload.get('indic06'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic07':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.6.state'
      if pgn_payload.get('indic07') is not None:
        skvalue = int(pgn_payload.get('indic07'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic08':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.7.state'
      if pgn_payload.get('indic08') is not None:
        skvalue = int(pgn_payload.get('indic08'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic09':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.8.state'
      if pgn_payload.get('indic09') is not None:
        skvalue = int(pgn_payload.get('indic09'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic10':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.9.state'
      if pgn_payload.get('indic10') is not None:
        skvalue = int(pgn_payload.get('indic10'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic11':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.10.state'
      if pgn_payload.get('indic11') is not None:
        skvalue = int(pgn_payload.get('indic11'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic12':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.11.state'
      if pgn_payload.get('indic12') is not None:
        skvalue = int(pgn_payload.get('indic12'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic13':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.12.state'
      if pgn_payload.get('indic13') is not None:
        skvalue = int(pgn_payload.get('indic13'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic14':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.13.state'
      if pgn_payload.get('indic14') is not None:
        skvalue = int(pgn_payload.get('indic14'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic15':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.14.state'
      if pgn_payload.get('indic15') is not None:
        skvalue = int(pgn_payload.get('indic15'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic16':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.15.state'
      if pgn_payload.get('indic16') is not None:
        skvalue = int(pgn_payload.get('indic16'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic17':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.16.state'
      if pgn_payload.get('indic17') is not None:
        skvalue = int(pgn_payload.get('indic17'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic18':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.17.state'
      if pgn_payload.get('indic18') is not None:
        skvalue = int(pgn_payload.get('indic18'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic19':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.18.state'
      if pgn_payload.get('indic19') is not None:
        skvalue = int(pgn_payload.get('indic19'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic20':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.19.state'
      if pgn_payload.get('indic20') is not None:
        skvalue = int(pgn_payload.get('indic20'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic21':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.20.state'
      if pgn_payload.get('indic21') is not None:
        skvalue = int(pgn_payload.get('indic01'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic22':
      skpath = 'electrical.switches..' + sktype + str(skinstance) + '.21.state'
      if pgn_payload.get('indic22') is not None:
        skvalue = int(pgn_payload.get('indic22'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic23':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.22.state'
      if pgn_payload.get('indic23') is not None:
        skvalue = int(pgn_payload.get('indic23'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic24':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.23.state'
      if pgn_payload.get('indic24') is not None:
        skvalue = int(pgn_payload.get('indic24'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic25':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.24.state'
      if pgn_payload.get('indic25') is not None:
        skvalue = int(pgn_payload.get('indic25'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic26':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.25.state'
      if pgn_payload.get('indic26') is not None:
        skvalue = int(pgn_payload.get('indic26'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic27':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.26.state'
      if pgn_payload.get('indic27') is not None:
        skvalue = int(pgn_payload.get('indic27'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


    elif n2kkey == 'indic28':
      skpath = 'electrical.switches.' + sktype + str(skinstance) + '.27.state'
      if pgn_payload.get('indic28') is not None:
        skvalue = int(pgn_payload.get('indic28'))
        if skvalue != 0 and skvalue != 1:
          return {}
        return  {"path":skpath,"value":skvalue}
      else:
        return {}


  except:
    if debug_all: log.info('sync: createSIGKpathPGN1127501 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}


# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# dimmer Data 0x0FF06
# ********************************************************************************************
def createSIGKpathPGN65286(n2kkey, pgn_payload):

  try:
    
    skinstance = int(pgn_payload.get('instance')) 

    n2ktype = pgn_payload.get('dimmertype')

    if n2ktype == 'LED 1 Channel':
      sktype = "mesh"
      skindex=0

    elif n2ktype == 'LED 1 Channel 01':
      sktype = "mesh"
      skindex=1

    elif n2ktype == 'LED 1 Channel 02':
      sktype = "mesh"
      skindex=2

    elif n2ktype == 'LED 1 Channel 03':
      sktype = "mesh"
      skindex=3

    elif n2ktype == 'LED 1 Channel 04':
      sktype = "mesh"
      skindex=4

    elif n2ktype == 'LED 1 Channel 05':
      sktype = "mesh"
      skindex=5

    elif n2ktype == 'LED 1 Channel 06':
      sktype = "mesh"
      skindex=6

    elif n2ktype == 'LED 1 Channel 07':
      sktype = "mesh"
      skindex=7


    elif n2ktype == 'RGB 1 Channel':
      sktype = "rgbwhub"
      skindex=0

    elif n2ktype == 'RGB 1 Channel 01':
      sktype = "rgbwhub"
      skindex=1

    elif n2ktype == 'RGB 1 Channel 02':
      sktype = "rgbwhub"
      skindex=2

    elif n2ktype == 'RGB 1 Channel 03':
      sktype = "rgbwhub"
      skindex=3


    elif n2ktype == 'LED 1 Channel':
      sktype = "hub"
      skindex=0

    elif n2ktype == 'LED 1 Channel 01':
      sktype = "hub"
      skindex=1

    elif n2ktype == 'LED 1 Channel 02':
      sktype = "hub"
      skindex=2

    elif n2ktype == 'LED 1 Channel 03':
      sktype = "hub"
      skindex=3

    else:
      sktype = "hub"
      skindex=0

    if sktype == 'mesh':

      if n2kkey == 'dimmer0':
        skpath = 'electrical.dimmers.mesh.' + str(skindex) + '.'   + str(int(skinstance) & 0x0F) +  '.dimmingLevel'
        if pgn_payload.get('dimmer0') is not None:
          skvalue = float("{0:.2f}".format(pgn_payload.get('dimmer0') * 0.01))
          if (int(pgn_payload.get('control')  ) & 0x0F)  != 0:
            null = None
            #skpath_json = json.loads(json.dumps( {"path":skpath,"value":null}))
            return {"path":skpath,"value":255}
          else:
            return  {"path":skpath,"value":skvalue}
        else:
          return {}

      elif n2kkey == 'dimmer2':
        skpath = 'electrical.dimmers.mesh.'  + str(int(skinstance) >> 4) + '.'   + str(int(skinstance) & 0x0F) +   '.dimmingState'
        if pgn_payload.get('dimmer2') is not None:
          skvalue = float("{0:.2f}".format(pgn_payload.get('dimmer2') * 1.0))  
          return  {"path":skpath,"value":skvalue}
        else:
          return {}

      elif n2kkey == 'dimmer3':
        skpath = 'electrical.dimmers.mesh.'  + str(int(skinstance) >> 4) + '.'   + str(int(skinstance) & 0x0F) +   '.dimmingAmps'
        if pgn_payload.get('dimmer3') is not None:
          skvalue = float("{0:.2f}".format(pgn_payload.get('dimmer3') * 0.1))  
          return  {"path":skpath,"value":skvalue}
        else:
          return {}

        

      elif n2kkey == 'control':
        skpath = 'electrical.dimmers.mesh.'  + str(int(skinstance) >> 4) + '.'   + str(int(skinstance) & 0x0F) +   '.dimmingStatus'
        if pgn_payload.get('control') is not None:
          dimmercontrol = int(pgn_payload.get('control')) & 0x0F
          skvalue = float("{0:.2f}".format(dimmercontrol * 1.0))  
          return  {"path":skpath,"value":skvalue}
        else:
          return {}


    elif sktype == 'rgbwhub':

      #skinstance = int(skinstance) & 0x03

      if n2kkey == 'dimmer0':
        skpath = 'electrical.dimmers.hub.' + str(skindex) + '.0.dimmingLevelRed'
        if pgn_payload.get('dimmer0') is not None:
          skvalue = float("{0:.2f}".format(pgn_payload.get('dimmer0') * 0.01))
          return  {"path":skpath,"value":skvalue}
        else:
          return {}

      elif n2kkey == 'dimmer1':
        skpath = 'electrical.dimmers.hub.' + str(skindex) + '.1.dimmingLevelGreen'
        if pgn_payload.get('dimmer1') is not None:
          skvalue = float("{0:.2f}".format(pgn_payload.get('dimmer1') * 0.01))      
          return  {"path":skpath,"value":skvalue}
        else:
          return {}
        

      elif n2kkey == 'dimmer2':
        skpath = 'electrical.dimmers.hub.' + str(skindex) + '.2.dimmingLevelBlue'
        if pgn_payload.get('dimmer2') is not None:
          skvalue = float("{0:.2f}".format(pgn_payload.get('dimmer2') * 0.01))
          return  {"path":skpath,"value":skvalue}
        else:
          return {}

      elif n2kkey == 'dimmer3':
        skpath = 'electrical.dimmers.hub.' + str(skindex) + '.3.dimmingLevelWhite'
        if pgn_payload.get('dimmer3') is not None:
          skvalue = float("{0:.2f}".format(pgn_payload.get('dimmer3') * 0.01))        
          return  {"path":skpath,"value":skvalue}
        else:
          return {}

      elif n2kkey == 'control':
        skpath = 'electrical.dimmers.hub.' + str(skindex) + '.4.dimmingStatus'
        if pgn_payload.get('control') is not None:
          skvalue = pgn_payload.get('control')
          skvalue = float("{0:.2f}".format(pgn_payload.get('control') * 1.0))  
          return  {"path":skpath,"value":skvalue}
        else:
          return {}
       


    elif sktype == 'hub':

      #skinstance = int(skinstance) & 0x03

      if n2kkey == 'dimmer0':
        skpath = 'electrical.dimmers.hub.' + str(skindex) + '.0.dimmingLevel'
        if pgn_payload.get('dimmer0') is not None:
          skvalue = float("{0:.2f}".format(pgn_payload.get('dimmer0') * 0.01))
          return  {"path":skpath,"value":skvalue}
        else:
          return {}

      elif n2kkey == 'dimmer1':
        skpath = 'electrical.dimmers.hub.' + str(skindex) + '.1.dimmingLevel'
        if pgn_payload.get('dimmer1') is not None:
          skvalue = float("{0:.2f}".format(pgn_payload.get('dimmer1') * 0.01))      
          return  {"path":skpath,"value":skvalue}
        else:
          return {}
        

      elif n2kkey == 'dimmer2':
        skpath = 'electrical.dimmers.hub.' + str(skindex) + '.2.dimmingLevel'
        if pgn_payload.get('dimmer2') is not None:
          skvalue = float("{0:.2f}".format(pgn_payload.get('dimmer2') * 0.01))
          return  {"path":skpath,"value":skvalue}
        else:
          return {}

      elif n2kkey == 'dimmer3':
        skpath = 'electrical.dimmers.hub.' + str(skindex) + '.3.dimmingLevel'
        if pgn_payload.get('dimmer3') is not None:
          skvalue = float("{0:.2f}".format(pgn_payload.get('dimmer3') * 0.01))        
          return  {"path":skpath,"value":skvalue}
        else:
          return {}

      elif n2kkey == 'control':
        skpath = 'electrical.dimmers.hub.' + str(skindex) + '.4.dimmingStatus'
        if pgn_payload.get('control') is not None:
          skvalue = pgn_payload.get('control')
          skvalue = float("{0:.2f}".format(pgn_payload.get('control') * 1.0))  
          return  {"path":skpath,"value":skvalue}
        else:
          return {}



  except:
    if debug_all: log.info('sync: createSIGKpathPGN65286 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}




# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Custom PGN  - SeaSmart ac status detail 0x0FF08
# ********************************************************************************************
def createSIGKpathPGN65288(n2kkey, pgn_payload):

  try:
    
    skinstance = int(pgn_payload.get('instance'))

    n2ktype = pgn_payload.get('ac_type')

    if n2ktype == 'UTIL':
      sktype = 0
    elif n2ktype == 'UTIL1':
      sktype = 16
    elif n2ktype == 'UTIL2':
      sktype = 32

    else:
      sktype = 0

    skinstance = skinstance + sktype

    if n2kkey == 'ac_volts_detail':
      skpath = 'electrical.ac.Bus' + str(skinstance) + '.0.lineNeutralVoltage'
      if pgn_payload.get('ac_volts_detail') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('ac_volts_detail') * 1.0))
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'ac_amps_detail':
      skpath = 'electrical.ac.Bus' + str(skinstance) + '.0.current'
      if pgn_payload.get('ac_amps_detail') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('ac_amps_detail') * 1.0))      
        return {"path":skpath,"value":skvalue}
      else:
        return {}

  except:
    if debug_all: log.info('sync: createSIGKpathPGN65288 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}




# ********************************************************************************************
# Converts NMEA 2000 field descriptions to Signal
# Custom PGN  - SeaSmart Indicator Runtime 0x0FF0C
# ********************************************************************************************
def createSIGKpathPGN65292(n2kkey, pgn_payload):

  try:
    
    skinstance = int(pgn_payload.get('instance'))
    n2kchannel = int(pgn_payload.get('channel'))

    if n2kkey == 'runtime_sec':
      skpath = 'electrical.indicator.' + str(skinstance) + '.' + str(n2kchannel) +'.runtime'
      if pgn_payload.get('runtime_sec') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('runtime_sec') * 1.0))
        return {"path":skpath,"value":skvalue}
      else:
        return {}

    elif n2kkey == 'cycles':
      skpath = 'electrical.indicator.' + str(skinstance) + '.' + str(n2kchannel) +'.cycles'
      if pgn_payload.get('cycles') is not None:
        skvalue = float("{0:.2f}".format(pgn_payload.get('cycles') * 1.0))      
        return {"path":skpath,"value":skvalue}
      else:
        return {}
        

  except:
    if debug_all: log.info('sync: createSIGKpathPGN65292 error %s:%s', n2kkey, pgn_payload)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return {}


# ********************************************************************************************
# Parses pgn_payload looking for vales based on n2kkey and fromats into signalk string
def parseSIGK(device, data):
  
  # **************************************************
  # For Signal K
  # **************************************************

  try:

    skupdates = []

    json_data = json.loads(data)
    
    for record in json_data:
      
      if debug_all: log.info('signalk: parseSIGK SignalK record %s:%s', device, record)
      
      json_record = {}
      if record != None:
        json_record = record
      
      if debug_all: log.info('signalk: parseSIGK SignalK record %s:%s', device, json_record)



      n2kpgn = int(json_record.get('pgn', 'NULL'), 16)
      if debug_all: log.info('signalk: parseSIGK SignalK n2kpgn %s:%s', device, n2kpgn)
      
      n2kdescription = json_record.get('description', 'NULL')
      if debug_all: log.info('signalk: parseSIGK SignalK n2kdescription %s:%s', device, n2kdescription)
      
      n2ksource = json_record.get('source', 'NULL')
      if debug_all: log.info('signalk: parseSIGK SignalK n2ksource %s:%s', device, n2ksource)
      
      n2ktimestamp = json_record.get('timestamp', 'NULL')
      if debug_all: log.info('signalk: parseSIGK SignalK n2ktimestamp %s:%s', device, n2ktimestamp)

      n2kpayload = json_record.get('payload', 'NULL')
      if debug_all: log.info('signalk: dump_pcdinfirebase SignalK n2kpayload %s:%s', device, n2kpayload)

      n2kkeys = n2kpayload.keys()
      if debug_all: log.info('signalk: parseSIGK SignalK n2kkeys %s:%s', device, n2kkeys)

      for n2kkey in n2kkeys:
        n2kvalue = n2kpayload.get(n2kkey, 'NULL')

        if debug_all: log.info('signalk: parseSIGK SignalK n2kvalue %s:%s', n2kkey, n2kvalue)
        

        #skupdates = []
        skvalues= []

        skcontext = "vessels.urn:mrn:imo:mmsi:338184312"
      

        #sksource = {"label":"antisense","type":"NMEA2000","pgn":127250,"src":"204"}
        #sktimestamp = "2019-07-12T18:32:54.134Z"

        sksource = {"label":"chetcodigital","type":"NMEA2000","pgn":n2kpgn,"src":n2ksource}
        #sktimestamp = "2019-07-12T18:32:54.134Z"
        sktimestamp = n2ktimestamp

        #skvalues.append({"path":"navigation.headingMagnetic","value":1.8979})
        #skpath =  n2kdescription + '.' + n2kkey
        #skvalues.append({"path":skpath,"value":n2kvalue})
        
        skpathjson =  createSIGKpath(n2kpgn, n2kkey, n2kpayload)
        #skpathjson =  ""
        
        if debug_all: log.info('signalk: parseSIGK SignalK skpathjson %s:%s', device, skpathjson)

        if skpathjson != {}:
          skvalues.append(skpathjson)

          skupdate_source = {'source': sksource, "timestamp":sktimestamp,"values":skvalues}
          skupdates.append( skupdate_source)

    skdata = {"updates":skupdates, "context":skcontext}

    if debug_all: log.info('signalk: parseSIGK SignalK json %s:%s', device, skdata)

    return skdata
    





  except ValueError as e:
    if debug_all: log.info('signalk: parseSIGK SignalK ValueError in data %s:  ', data)

    if debug_all: log.info('signalk: parseSIGK SignalK ValueError in data %s:  ' % str(e))

    pass

  except NameError as e:
    if debug_all: log.info('signalk: parseSIGK SignalK NameError in data %s:  ', data)

    if debug_all: log.info('signalk: parseSIGK SignalK NameError in data %s:  ' % str(e))
    
  except TypeError as e:
    if debug_all: log.info('signalk: parseSIGK SignalK TypeError in data %s:  ', data)

    if debug_all: log.info('signalk: parseSIGK SignalK TypeError in data %s:  ' % str(e))

  except AttributeError as e:
    if debug_all: log.info('signalk: parseSIGK SignalK AttributeError in data %s:  ', data)

    if debug_all: log.info('signalk: parseSIGK SignalK AttributeError in data %s:  ' % str(e))

  except:
    if debug_all: log.info('signalk: parseSIGK SignalK error %s:%s', partition, device)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % str(e))
    pass


# ********************************************************************************************
# Parses pgn_payload looking for vales based on n2kkey and fromats into signalk string
def createSIGKpath(pgn_number, n2kkey, pgn_payload):


  match pgn_number:

    # Environmental Data
    case 130311:
      return createSIGKpathPGN130311(n2kkey, pgn_payload)
    
    # Humidity Data
    case 130313:
      return createSIGKpathPGN130313(n2kkey, pgn_payload)

    # Pressure Data
    case 130314:
      return createSIGKpathPGN130314(n2kkey, pgn_payload)

    # Wind Data
    case 130306:
      return createSIGKpathPGN130306(n2kkey, pgn_payload)

    # System Time 1F010
    case 126992:
      return createSIGKpathPGN126992(n2kkey, pgn_payload)

    # Water Depth 0x1F50B
    case 128267:
      return createSIGKpathPGN128267(n2kkey, pgn_payload)
    
    # COG/SOG Data
    case 129026:
      return createSIGKpathPGN129026(n2kkey, pgn_payload)

    # Heading Data 0x1F112
    case 127250:
      return createSIGKpathPGN127250(n2kkey, pgn_payload)

    # Rate of Turn Data 0x1F113
    case 127251:
      return createSIGKpathPGN127251(n2kkey, pgn_payload)

    # Rudder Data 0x1F10D
    case 127245:
      return createSIGKpathPGN127245(n2kkey, pgn_payload)

    # Position Rapid 0x1F119
    case 126992:
      return createSIGKpathPGN126992(n2kkey, pgn_payload)

    # Attitude 0x1F119
    case 127257:
      return createSIGKpathPGN127257(n2kkey, pgn_payload)
    
    # Water Speed  0x1F503
    case 128259:
      return createSIGKpathPGN128259(n2kkey, pgn_payload)

    # Engine Rapid Data 0x1F200
    case 127488:
      return createSIGKpathPGN127488(n2kkey, pgn_payload)

    # Engine Rapid Dynamic 0x1F201
    case 127489:
      return createSIGKpathPGN127489(n2kkey, pgn_payload)

    # Trip Parameters, Engine 0x1F209
    case 127497:
      return createSIGKpathPGN127497(n2kkey, pgn_payload)
    
    # Transmission Parameters, Dynamic  0x1F205
    case 127493:
      return createSIGKpathPGN127493(n2kkey, pgn_payload)

    # Battery Status Data 0x1F214
    case 127508:
      return createSIGKpathPGN127508(n2kkey, pgn_payload)

    # Temperature Data 0x1FD08
    case 130312:
      return createSIGKpathPGN130312(n2kkey, pgn_payload)

    # Temperature Extended Data 0x1FD0C
    case 130316:
      return createSIGKpathPGN130316(n2kkey, pgn_payload)

    # Fluid Level Data 0x1F211
    case 127505:
      return createSIGKpathPGN127505(n2kkey, pgn_payload)

    #Switch State Data Data 0x1F20D
    case 127501:
      return createSIGKpathPGN127501(n2kkey, pgn_payload)
    
    # dimmerData 0x0FF06
    case 65286:
      return createSIGKpathPGN65286(n2kkey, pgn_payload)

    # Custom PGN  - SeaSmart ac status detail 0x0FF08
    case 65288:
      return createSIGKpathPGN65288(n2kkey, pgn_payload)
    
   # Custom PGN  - SeaSmart Indicator Runtime 0x0FF0C
    case 65292:
      return createSIGKpathPGN65292(n2kkey, pgn_payload)
    
     
    case _:
      return {}

# ********************************************************************************************





