# Splicer parser for Seasmart NMEA data
# Author: Scott Robertson
# (c) triv.io all rights reserved

from datetime import datetime, timedelta
import time
from time import mktime
#import binascii
import calendar
from io import StringIO
import csv

import splicer

from splicer import Schema, Relation, Field
from splicer.codecs import decodes

import functools

import logging
requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)

#logging.disable(logging.CRITICAL)

logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.ERROR)
log = logging

# *******************************************************************
# Debug Output defines
# Comment to enable/disable
# ********************************************************************
debug_all = True
#debug_all = False


import sys

# Field positions
PGN=0
TIMESTAMP=1
SOURCE_ID=2
PAYLOAD=3

@decodes('application/x-nmea')
def nmea_stream(stream): 
  return Relation(
    SCHEMA,    
    interpeted(events(stream))
  )

def nmea_string(string):
  return nmea_stream(StringIO(string))

def loads(string):


  nmea_lines = events(string)
  if debug_all: log.info('NMEA : loads nmea_lines %s:  ' , nmea_lines)
  
  nmea_list = interpeted(nmea_lines)
  #return list(interpeted(events(string)))
  return list(nmea_list)


  #return list(interpeted(events(string)))
  #return list(interpeted(events(StringIO(string))))

def events(stream):

#To read data from a csv file, use the reader function to create a reader object. 
#
#The reader function will take each line of the file and make a list containing
#all that line's columns. 
#
#Then we can just pick the columns we are interested in.

  try:

    nmea_list = []
    #nmea_lines = csv.reader(stream)
    #nmea_lines = stream.splitlines()
    nmea_lines = stream.split("\\n")
    
    for line in nmea_lines:
      log.info("NMEA events line %s ", line)
      
      if valid(line):
        nmea_list.append(line.strip()[7:-2])

    return nmea_list

  except AttributeError as e:
    if debug_all: log.info('NMEA : AttributeError in events %s:  ' % str(e))

  except TypeError as e:
    if debug_all: log.info('NMEA : TypeError in events %s:  ' % str(e))
    
  except KeyError as e:
    if debug_all: log.info('NMEA :: KeyError in events %s:  ' % str(e))
    
  except NameError as e:
    if debug_all: log.info('NMEA :: NameError in events %s:  ' % str(e))

  except ValueError as e:
    if debug_all: log.info('NMEA :: ValueError in events %s:  ' % str(e))

  except IndexError as e:
    if debug_all: log.info('NMEA:: IndexError in events %s:  ' % str(e))

  except:
    e = sys.exc_info()[0]
    if debug_all: log.info("NMEA ::  Error: %s" % e)


"""
  return csv.reader(
    (
      #remove the first 7 and last 3 characters from the line
      #$PCDIN,01F205,6DOB845V,A7,007F803CD0150000*3F ->
      #01F205,6DOB845V,A7,007F803CD0150000
      #line.strip()[7:-3]

      #log.info("NMEA events - line %s ", line)      
      #line.strip()[7:-2]
      
      for line in stream:
        log.info("NMEA events line %s ", line)
      # Check that the line is formatted correctly and has a good checksum
      
      #if valid(line)
    )
  )
"""

def interpeted(records):
  """
  Decodes the payload if we can and then returns a
  fat record (where all nmea pgns are represented in 
  the record with a value of none except for the column
  the event represents)


  ['1234', 'AFAFAFA', '02', 'binary data'] ->
  ['1234', 'AFAFAFA', '02', 'binary data', None, ..., {...}, None]
  """

    
  # create a list of [None, ..., None]
  blank = [None] * len(DECODER_MAP)

  for nmea_record in records:
    
    try:
      
      record  = nmea_record.split(',')
      log.info("NMEA interpeted - record %s ", record)
      
      pgn = record[PGN]

      

      #if pgn == '00FF06':
      log.info("NMEA interpeted - PGN %s ", pgn)

      ps_ts =  seasmart_timestamp(record[TIMESTAMP])
      
      # check if we have a good timestamp
      if ps_ts != 0:

        record[TIMESTAMP] = ps_ts

        # check if pgn is in DECODER_MAP
        pos, decode = DECODER_MAP.get(pgn, (None, None))

        if decode:
          log.info("NMEA interpeted - decode %s pos %s ", decode, pos)

          #initialize c to size of blank array
          c = blank[:]
          
          #get raw pushsmart record source field and before checksum
          #$PCDIN,01F205,6DOB8460,A7,017F8035D0150000*2D
          #$PCDIN,01F205,6DOB8460,A7,[payload]*2D
          payload = record.pop()

          log.info("NMEA interpeted - payload %s ", payload)

          # decode payload
          #payload F201013D6EFAFFFF
          c[pos] = decode(payload)

          log.info("NMEA interpeted - decoded payload %s:%s ", pos, c[pos])
          #and add to pgn record map
          #payload 13:{'wind_speed': 257, 'wind_reference': 'Apparent Wind', 'sid': 242, 'wind_direction': 160.8597, 'reserved2': None, 'reserved1': 15}  
          record.extend(c)
          yield record
          
      else:
        log.info("NMEA interpeted - invalid timestamp %s ", record[TIMESTAMP])


    except TypeError as e:
      if debug_all: log.info('NMEA : TypeError in proc  interpeted %s:  ' % str(e))
      if debug_all: log.info('NMEA : TypeError message device %s:', record)

    except KeyError as e:
      if debug_all: log.info('NMEA :: KeyError in proc  interpeted %s:  ' % str(e))
      if debug_all: log.info('NMEA :: KeyError in proc  interpeted %s:  ', record)
      
    except NameError as e:
      if debug_all: log.info('NMEA :: NameError in proc  interpeted %s:  ' % str(e))
      if debug_all: log.info('NMEA :: NameError in proc  interpeted %s:  ', record)

    except ValueError as e:
      if debug_all: log.info('NMEA :: ValueError in proc  interpeted %s:  ' % str(e))
      if debug_all: log.info('NMEA :: ValueError in proc  interpeted %s:  ', record)

    except IndexError as e:
      if debug_all: log.info('NMEA:: IndexError in proc  interpeted %s:  ' % str(e))
      if debug_all: log.info('NMEA:: IndexError in proc  interpeted %s:  ', record)

      
    except:
      if debug_all: log.info('NMEA :: Error  interpeted%s:', record)

      e = sys.exc_info()[0]
      if debug_all: log.info("NMEA ::  Error: %s" % e)
      pass

      

def valid(sentence):
  """
  Returns True if the nema sentence starts with
  '$' and ends with a '*' followed by a 2 digit 
  hexnum whose value equals the xor character
  values of the character values between the $ and *

  """
  nema_checksum = ""
  checksum=255
  
  if not sentence.startswith('$'):
    log.info("NMEA valid error - wrong start $ %s ", sentence)
    return False


  valuepairs = sentence.split(",")
  # check if we have proper formatted pushsmart string
  if len(valuepairs) != 5:
    log.info("NMEA valid error - wrong length %s ", sentence)
    return False

  elif valuepairs[0] != '$PCDIN':
    log.info("NMEA valid error - wrong start $PCDIN %s ", sentence)
    return False

  #Check PGN length is correct
  elif len(valuepairs[1]) != 6:
    log.info("NMEA valid error - wrong PGN length %s ", sentence)
    return False

  #check if timestamp length is correct
  elif len(valuepairs[2]) != 8:
    log.info("NMEA valid error - wrong timestamp length %s ", sentence)
    return False

  #check if source length is correct
  elif len(valuepairs[3]) != 2:
    log.info("NMEA valid error - wrong source length %s ", sentence)
    return False

  #check if payload is terminated with * checksum
  elif len(valuepairs[4]) < 8:    
    log.info("NMEA valid error - wrong payload length min %s ", sentence)
    return False

  #check if payload is terminated with * checksum
  #elif (valuepairs[4][len(valuepairs[4])-3] != '*') and (valuepairs[4][len(valuepairs[4])-4] != '*'):
  elif valuepairs[4].find('*') == -1:    
    log.info("NMEA valid error - wrong payload * %s ", sentence)
    return False





  

  parts = sentence.split('*')
  if len(parts) != 2:
    log.info("NMEA valid cs error length - sentence %s ", sentence)
    return False

  data, checksum_str = parts
  #log.info("NMEA checksum - data %s:checksum_str %s ", data, checksum_str)
  
  # 031114 JLB
  # Added check for when checksum_str is not hexidecimal
  # return false if not
  try:
    checksum = functools.reduce(lambda checksum,c: checksum^ord(c), data[1:], 0)

    nema_checksum = int(checksum_str[:2], 16)
    #log.info("NMEA valid cs error - checksum %s:nema_checksum %s ", checksum, nema_checksum)

  # if error then return false as its not a good checksum
  except NameError as e:
    if debug_all: log.info('NMEA :: NameError in NMEA valid cs %s:  ' % str(e))

  except:
    log.info("NMEA valid cs error - sentence %s:checksum_str %s ", sentence, checksum_str)
    e = sys.exc_info()[0]
    if debug_all: log.info("NMEA valid cs error ::  Error: %s" % str(e))

    return False

  if checksum != nema_checksum:
    log.info("NMEA bad checksum - sentence %s ", sentence)
    return False
  else:
    #return checksum == nema_checksum
    return True
 
def seasmart_timestamp(timestamp, EPOCH=1262304000):
  """
  char(6), char(2) -> datetime
  """
  #Get TimeStamp from PushSmart record
  #$PCDIN,01F010,6DOB8463,A7,0007040040AE3E0A*22
  #$PCDIN,01F010,[TIMESTAMP],A7,0007040040AE3E0A*22
  #Timestamp is Hex32 from 1/1/2010 (EPOCH 1262304000)

  #initialize pushsmart timestamp to 0
  ps_ts = 0
  #ps_ts = int(timestamp[:6], 32) + EPOCH
  #return datetime.fromtimestamp(ps_ts)

  #But lets trap for a Hex32 format error just to be sure
  try:
    #ts = int(timestamp[:6], 32) + EPOCH
    ts = int(timestamp[:6], 32) 
  except:
    log.info("NMEA get timestamp format error - timestamp %s ", timestamp)
    return ps_ts

  #return datetime.fromtimestamp(ts +  EPOCH)

  # and check that we have a date between now and 1/1/2010
  if ts <= 0:
    log.info("NMEA get timestamp error - negitive timestamp %s ", timestamp)
    return ps_ts

  #return datetime.fromtimestamp(ts +  EPOCH)  
  # Get current time in seconds
  current_ts = int(time.time())
  #return datetime.fromtimestamp(ts +  EPOCH)
  # and be sure ts is not greater then current time as check
  if ts + EPOCH <= current_ts:
    ps_ts = ts + EPOCH
    return datetime.fromtimestamp(ps_ts)
  
  else:
    log.info("NMEA get timestamp error -  timestamp greater then current %s ", timestamp)
    return ps_ts


PGNS = []
def pgn(number, returns=[]):
  """
  Decorator that associates the specified pgn number
  with it's corresponding method.

  Example: To declare that some method intpeprets
  PGN 1234

  @pgn(1234)
  def some_method(data):
    ... do something with the data
    return dict()

  """
  #log.info("NMEA pgn - PGN %s ", number)

  def field_type(desc):
    parts = desc.split(':')
    if len(parts) < 2:
      parts.append('INTEGER')

    return dict(zip(
      ('name', 'type'),
      parts
    ))

  fields = [Field(**field_type(name)) for name in returns]
  def wrap(method):
    # the pgn is represented as hex
    # we'll 

    # hex(number) -> 0x123 -> 0123
    #h = hex(number).replace('x','').upper()
    # bad error here as string needs to be exactly 6 characters long - so zero pad
    h = format(number, '06X')
    #log.info("NMEA payload - HEX %s ",payload )    
    #log.info("NMEA pgn - HEX %s ", h)
    wrapped_method = lambda payload: method(StringIO(payload))
    wrapped_method.__name__ = method.__name__
    PGNS.append((h, wrapped_method, fields))
    return wrapped_method
  return wrap


#Haltech Elite 0x360 -> 0xFF60 = 65376
#0 - 1 RPM RPM y = x
#2 - 3 Manifold Pressure kPa y = x/10
#4 - 5 Throttle Position % y = x/10
#6 - 7 Coolant Pressure kPa y = x/10
@pgn(65376, returns=['engine_speed', 'manifold_pressure', 'throttle_position', 'coolant_pressure'])
def haltec_engine_speed(data):


    
  return dict(
    engine_speed = uintBE16(data),
    manifold_pressure = uintBE16(data),
    throttle_position = uintBE16(data),
    coolant_pressure = uintBE16(data)

  )

#Haltech Elite 0x3E0 -> 0xFFE0 = 65504
#0 - 1 Coolant Temperature K y = x/10
#2 - 3 Air Temperature K y = x/10
#4 - 5 Fuel Temperature K y = x/10
#6 - 7 Oil Temperature K y = x/10
@pgn(65504, returns=['engine_temp', 'intake_temp', 'fuel_temp', 'oil_temp'])
def haltec_engine_temps(data):


    
  return dict(
    engine_temp = uintBE16(data),
    intake_temp = uintBE16(data),
    fuel_temp = uintBE16(data),
    oil_temp = uintBE16(data)

  )

#Haltech Elite 0x361 -> 0xFF61 = 65377
#0 - 1 Fuel Pressure kPa y = x/10
#2 - 3 Oil Pressure kPa y = x/10
#4 - 5 Engine Demand % y = x/10
#6 - 7 Wastegate Pressure kPa y = x/10
@pgn(65377, returns=['fuel_pressure', 'oil_pressure', 'engine_demand', 'wastegate_pressure'])
def haltec_engine_pressures(data):

  

    
  return dict(
    fuel_pressure= uintBE16(data),
    oil_pressure = uintBE16(data),
    engine_demand = uintBE16(data),
    wastegate_pressure = uintBE16(data)

  )

#Haltech Elite 0x372 -> 0xFF72 = 65394
#0 - 1 Battery Voltage Volts y = x/10
#2 - 3 Unused
#4 - 5 Target Boost Level kPa y = x/10
#6 - 7 Barometric Pressure kPa y = x/10
@pgn(65394, returns=['battery_volts', 'unused', 'target_boost', 'baro_pressure'])
def haltec_engine_volts(data):

  

    
  return dict(
    battery_volts = uintBE16(data),
    unused = uintBE16(data),
    target_boost = uintBE16(data),
    baro_pressure = uintBE16(data)

  )

#Haltech Elite 0x3E1 -> 0xFFE1 = 65505
#0 - 1 Gearbox Oil Temperature y = x/10
#2 - 3 Diff Oil Temperature
#4 - 5 Fuel Composition % y = x/10
@pgn(65505, returns=['gearbox_temperature', 'drift_oil_temperature', 'fuel_composition'])
def haltec_gearbox(data):

  return dict(
    gearbox_temperature = uintBE16(data),
    drift_oil_temperature = uintBE16(data),
    fuel_composition = uintBE16(data)

  )

#Haltech Elite 0x371 -> 0xFF71 = 65393
#0 - 1 fuel flow cc/min y = x
#2 - 3 fuel return cc/min
@pgn(65393, returns=['fuel_flow', 'fuel_return'])
def haltec_fuel_flow(data):

  return dict(
    fuel_flow = uintBE16(data),
    fuel_return = uintBE16(data)

  )

#Haltech Elite 0x3E2 -> 0xFFE2 = 65506
#0 - 1 Fuel Level % y = x/10
@pgn(65506, returns=['fuel_level'])
def haltec_fuel_level(data):
    
  return dict(
    fuel_level = uintBE16(data)

  )


@pgn(65262, returns=['engine_temp', 'fuel_temp', 'oil_temp', 'turbo_temp', 'intercool_temp', 'intercool_open','raw'])
def j1939_engine_temps(data):

  
  raw=getrawvalue(data)

  if raw[16] != '*':
    return None
    
  return dict(
    engine_temp = uint8(data),
    fuel_temp = uint8(data),
    oil_temp = uint16(data),
    turbo_temp = uint16(data),
    intercool_temp = uint8(data),
    intercool_open = uint8(data),
    raw=raw
  )


@pgn(61444, returns=['torque_mode', 'torque_demand', 'torque_actual', 'speed', 'source_address', 'starter_mode','torque_request','raw'])
def j1939_engine_eec1(data):

  
  raw=getrawvalue(data)

  if raw[16] != '*':
    return None
    
  return dict(
    torque_mode = uint8(data),
    torque_demand = uint8(data),
    torque_actual = uint8(data),
    speed = uint16(data),
    source_address = uint8(data),
    starter_mode = uint8(data),
    torque_request = uint8(data),
    raw=raw
  )





@pgn(65263, returns=['fuel_pressure', 'blowby_pressure', 'oil_level', 'oil_pressure', 'crankcase_pressure', 'coolant_pressure','coolant_level','raw'])
def j1939_engine_pressures(data):
  
  raw=getrawvalue(data)

  if raw[16] != '*':
    return None
    
  return dict(
    fuel_pressure = uint8(data),
    blowby_pressure = uint8(data),
    oil_level = uint8(data),
    oil_pressure = uint8(data),
    crankcase_pressure = uint16(data),
    coolant_pressure = uint8(data),    
    coolant_level = uint8(data),
    raw=raw
  )



@pgn(65271, returns=['battery_current', 'alternator_current', 'charging_voltage', 'battery_voltage', 'keyswitch_voltage','raw'])
def j1939_engine_voltages(data):
  
  raw=getrawvalue(data)

  if raw[16] != '*':
    return None
    
  return dict(
    battery_current = uint8(data),
    alternator_current = uint8(data),
    charging_voltage = uint16(data),
    battery_voltage= uint16(data),    
    keyswitch_voltage= uint16(data),
    raw=raw
  )


@pgn(65272, returns=['clutch_pressure', 'tran_oil_level', 'tran_diff_pressure', 'tran_oil_pressure', 'tran_oil_temp', 'tran_oil_warn','tran_oil_status','raw'])
def j1939_transmission(data):

  raw=getrawvalue(data)

  if raw[16] != '*':
    return None


  return dict(
    clutch_pressure = uint8(data),
    tran_oil_level = uint8(data),
    tran_diff_pressure = uint8(data),
    tran_oil_pressure = uint8(data),
    tran_oil_temp = uint16(data),
    tran_oil_warn= uint8(data),    
    tran_oil_status = uint8(data),
    raw=raw
  )



@pgn(65266, returns=['fuel_rate', 'instantaneous_fuel_economy', 'average_fuel_economy', 'throttle_position', 'demand_torque','raw'])
def j1939_fuel_economy(data):
  
  raw=getrawvalue(data)

  if raw[16] != '*':
    return None


  return dict(
    fuel_rate = uint16(data),
    instantaneous_fuel_economy = uint16(data),
    average_fuel_economy  = uint16(data),
    throttle_position= uint8(data),    
    demand_torque= uint8(data),
    raw=raw
  )


@pgn(65276, returns=['washer_level', 'fuel1_level', 'fuel_filter_differential_pressure', 'oil_filter_differential_pressure', 'cargo_temperature','fuel2_level','status','raw'])
def j1939_dash_display(data):

  raw=getrawvalue(data)

  if raw[16] != '*':
    return None


  return dict(
    washer_level = uint8(data),
    fuel1_level= uint8(data),
    fuel_filter_differential_pressure  = uint8(data),
    oil_filter_differential_pressure  = uint8(data),
    cargo_temperature = uint16(data),   
    fuel2_level= uint8(data),
    status= uint8(data),
    raw=raw
    
  )



@pgn(127488, returns=['engine_id', 'speed', 'boost_presure', 'tilt_or_trim', 'reserved_bits','raw'])
def engine_parameters_rapid_update(data):

  try:

    log.info('NMEA interpeted - engine_parameters_rapid_update data %s:  ', data)
    
    raw=getrawvalue(data)

    if raw[16] != '*':
      return None

    engine_id = uint8(data)
    log.info('NMEA interpeted - engine_parameters_rapid_update data %s:  ', engine_id)
    speed = uint16(data)
    log.info('NMEA interpeted - engine_parameters_rapid_update data %s:  ', speed)
    boost_presure = uint16(data)
    log.info('NMEA interpeted - engine_parameters_rapid_update data %s:  ',boost_presure)
    tilt_or_trim = int8(data)
    log.info('NMEA interpeted - engine_parameters_rapid_update data %s:  ' ,tilt_or_trim)
    reserved_bits = uint16(data)
    log.info('NMEA interpeted - engine_parameters_rapid_update data %s:  ', reserved_bits)
    raw=raw
    log.info('NMEA interpeted - engine_parameters_rapid_update data %s:  ' ,raw)
      
    return dict(
      engine_id = engine_id,
      speed = speed,
      boost_presure = boost_presure,
      tilt_or_trim = tilt_or_trim,
      reserved_bits = reserved_bits,
      raw=raw
    )

  except ValueError as e:
    log.info('NMEA interpeted - engine_parameters_rapid_update ValueError %s:  ' % str(e))

  except NameError as e:
    log.info('NMEA interpeted - engine_parameters_rapid_update NameError %s:  ' % str(e))
    
  except TypeError as e:
    log.info('NMEA interpeted - engine_parameters_rapid_update:  TypeError %s' % str(e))

  except AttributeError as e:
    log.info('NMEA interpeted - engine_parameters_rapid_update AttributeError %s:  ' % str(e))

  except:
    if debug_all: log.info('NMEA interpeted - engine_parameters_rapid_update %s:%s', partition, device)
    e = sys.exc_info()[0]


@pgn(127489, returns=['engine_id','oil_pressure', 'oil_temp', 
'engine_temp', 'alternator_potential', 'fuel_rate',
'total_engine_hours:BIGINT','coolant_pressure','fuel_pressure',
'not_available','discrete_status_1:STRING','discrete_status_2:STRING',
'percent_engine_load', 'percent_engine_torque','raw'])
def engine_parameters_dynamic(data):

  try:
    
    #log.info("NMEA interpeted - engine_parameters_dynamic Start ")

    raw=getrawvalue(data)

    #log.info("NMEA interpeted - engine_parameters_dynamic %s ", raw)
    #log.info("NMEA interpeted - engine_parameters_dynamic length %s ", len(raw))

    """
    #improper length
    if not((len(raw) == 53) or (len(raw) ==55)):
      return None

    # normal PGN length is 53
    if len(raw) == 53 and raw[52] != '*':
      return None

    #SmartCraft inserts an extra byte so length is 55
    if len(raw) == 55 and raw[54] != '*':
      return None

    """

    engine_id = uint8(data)
    oil_pressure = uint16(data)
    oil_temp = uint16(data)
    engine_temp = uint16(data)
    alternator_potential = int16(data)
    fuel_rate = int16(data)
    total_engine_hours = uint32(data)
    coolant_pressure = uint16(data)
    fuel_pressure = uint16(data)

    not_available = uint8(data)
    discrete_status_1 = bitmap(data,[
      'Check Engine',
      'Over Temperature',
      'Low Oil Pressure',
      'Low Oil Level',
      'Low Fuel Pressure',
      'Low System Voltage',
      'Low Coolant Level',
      'Water Flow',
      'Water in Fuel',
      'Charge Indicator',
      'Preheat Indicator',
      'High Boost Pressure',
      'Rev Limit Exceeded', 
      'EGR System',
      'Throttle Position Sensor',
      'Engine Emergency Stop Mode'
    ])

    discrete_status_2 = bitmap(data,[
      'Warning Level 1', 
      'Warning Level 2',
      'Power Reduction',
      'Maintenance Needed',
      'Engine Comm Error',
      'Sub or Secondary Throttle',
      'Neutral Start Protect',
      'Engine Shutting Down',
      'reserved1',
      'reserved2',
      'reserved3',
      'reserved4',
      'reserved5',
      'reserved6',
      'reserved7',
      'reserved8',
    ])

    percent_engine_load = int8(data)
    percent_engine_torque = int8(data)

    #log.info('NMEA interpeted - engine_parameters_dynamic fuel_rate %s:  ' , fuel_rate)


    return dict(
      engine_id = engine_id,
      oil_pressure = oil_pressure,
      oil_temp = oil_temp,
      engine_temp = engine_temp,
      alternator_potential = alternator_potential,
      fuel_rate = fuel_rate,
      total_engine_hours = total_engine_hours,
      coolant_pressure = coolant_pressure,
      fuel_pressure = fuel_pressure,

      not_available = not_available, # reserved field should equal 127
      discrete_status_1 = discrete_status_1,

      discrete_status_2 = discrete_status_2,

      percent_engine_load = percent_engine_load,
      percent_engine_torque = percent_engine_torque,
      raw=raw
    )


  except ValueError as e:
    #if debug_all: log.info('NMEA interpeted - engine_parameters_dynamic %s:  ', data)

    log.info('NMEA interpeted - engine_parameters_dynamic ValueError %s:  ' % str(e))

  except NameError as e:
    #if debug_all: log.info('Sync: dump_pcdinfirebase1 SignalK NameError in data %s:  ', data)

    log.info('NMEA interpeted - engine_parameters_dynamic NameError %s:  ' % str(e))
    
  except TypeError as e:
    #if debug_all: log.info('Sync: dump_pcdinfirebase1 SignalK TypeError in data %s:  ', data)

    log.info('NMEA interpeted - engine_parameters_dynamic:  TypeError %s' % str(e))

  except AttributeError as e:
    #if debug_all: log.info('Sync: dump_pcdinfirebase1 SignalK AttributeError in data %s:  ', data)

    log.info('NMEA interpeted - engine_parameters_dynamic AttributeError %s:  ' % str(e))

  except:
    if debug_all: log.info('NMEA interpeted - engine_parameters_dynamicerror %s:%s', partition, device)
    e = sys.exc_info()[0]

    log.info("Error: %s" % e)

  

# 127493: Transmission Parameters, Dynamic
# hex: 1F205
@pgn(127493, ['instance', 'gear', 'oil_pressure', 'oil_temp', 'discrete_status:STRING', 'reserved','raw'])
def transmission_parameters_dynamic(data):

  raw=getrawvalue(data)

  if raw[16] != '*':
    return None

  return dict(
    instance = uint8(data),
    gear = bit2(data),
    unused = bit4(data),
    oil_pressure = uint16(data),
    oil_temp = uint16(data),
    discrete_status = bitmap(data, [
      'Check Tranmission', 
      'Over Temperature', 
      'Low Oil Pressure', 
      'Low Oil Level',
      'Sail Drive',
      'reserved1',
      'reserved2',
      'reserved3'
    ]),
    reserved = uint8(data),
    raw=raw
  )
  
#127497: // Trip Parameters, Engine
@pgn(127497, ['instance', 'trip_fuel_used','fuel_rate_average', 'fuel_rate_economy', 'instantaneous_fuel_economy'])
def trip_parameters_engine(data):
  return dict(
    instance = uint8(data),
    trip_fuel_used = uint16(data),
    fuel_rate_average = int16(data),
    fuel_rate_economy = int16(data),
    instantaneous_fuel_economy = int16(data)
  )  

#127505: // Fluid Level
@pgn(127505, ['type','instance','level', 'tank_capacity:BIGINT', 'reserved','raw'])
def fluid_level(data):

  raw=getrawvalue(data)

  if raw[16] != '*':
    return None

  return dict(
    type = bit4(data),
    instance = bit4(data),   
    level = int16(data),
    tank_capacity = uint32(data),
    reserved = uint8(data)
    #raw=raw
  )

#127506: // Battery Status
@pgn(127506, ['sid', 'instance', 'dctype', 'stateofcharge','stateofhealth', 'timeremaining', 'ripplevoltage','raw'])
def battery_status_detail(data):

  raw=getrawvalue(data)

  if raw[18] != '*':
    return None

  return dict(
    sid = uint8(data),
    instance = uint8(data),

    dctype = {
        0: 'Battery',
        1: 'Alternator',      
        2: 'Convertor',
        3: 'Solar Cell',
        4: 'Wind Generator',
        5: 'Reserved',
        6: 'Reserved',
        7: 'Reserved',
        8: 'Reserved',
        9: 'Reserved',
        10:'Reserved',
        11:'Reserved',
        12:'Reserved',
        13:'Reserved',
        14:'Reserved',
        15:'Reserved',
        254:'Error',         
        255:'No Data'
      }.get(nint8(data)),


    stateofcharge = uint8(data),
    stateofhealth = uint8(data),
    timeremaining = uint16(data),
    ripplevoltage = uint16(data)
    #raw=raw
    
  )

#127508: // Battery Status
@pgn(127508, ['instance', 'voltage','current', 'temperature', 'sid','raw'])
def battery_status(data):

  raw=getrawvalue(data)

  if raw[16] != '*':
    return None

  return dict(
    instance = uint8(data),
    voltage = int16(data),
    current = int16(data),
    temperature = uint16(data),
    sid = uint8(data)
    #raw=raw
    
  )
 
 
#130306: // Wind Data 0x1FD02
@pgn(130306, ['sid', 'wind_speed','wind_direction', 'reserved1',  'wind_reference:STRING', 'reserved2'])
def wind_data(data):
  return dict(
    sid = uint8(data),
    wind_speed = int16(data),
    wind_direction = udegrees16(data),
    reserved1 = bit4(data),
    
    wind_reference = {
        0: 'TWIND True North',
        1: 'TWIND Mag North',      
        2:  'Apparent Wind',
        3: 'Error',
        4: 'Error',
        5: 'Error',
        6: 'Error',
        7: 'Error',
        8: 'TWIND True North',
        9: 'TWIND Mag North',
        10: 'Apparent Wind',
        11: 'TWIND VCGR',
        12: 'TWIND VCWR',
        13: 'Gust',
        14: 'Error',
        15: 'NULL'
      }.get(bit4(data)),
    

    reserved2 = uint16(data)
  )

#130323: // Metro Station  Data 0x1FD13
#127250: // Heading 0x1F112
@pgn(127250, ['sid', 'heading:real','deviation:real', 'variation:real',  'reserved', 'heading_reference:STRING' ])
def vessel_heading(data):
  return dict(
    sid = uint8(data),
    heading = hdegrees16(data),
    deviation =  degrees16(data),
    variation = degrees16(data),
    reserved = bit4(data),
    
    heading_reference = {
        0: 'Error',
        1: 'Error',      
        2: 'Error',
        3: 'Error',
        4: 'Error',
        5: 'Error',
        6: 'Error',
        7: 'Error',
        8: 'Error',
        9: 'Error',
        10: 'Error',
        11: 'Error',
        12: 'True',
        13: 'Magnetic',
        14: 'Error',
        15: 'NULL'
      }.get(bit4(data))
    
  )
#127251: // Rate of Turn 0x1F113
@pgn(127251, ['sid',  'rate_of_turn:real',  'reserved1', 'reserved2' ])
def rateofturn(data):
  return dict(
    sid = uint8(data),
    rate_of_turn = degrees32(data),
    reserved1 = uint8(data),
    reserved2 = int16(data)
   
    
  )

#127245: // Rudder 0x1F10D
@pgn(127245, ['instance', 'reserved1','direction_order:STRING', 'angle_order:real',  'position:real', 'reserved2' ])
def rudder(data):
  return dict(
    instance = uint8(data),
    reserved1 = bit4(data),
    direction_order = {
        0: 'Error',
        1: 'Error',      
        2: 'Error',
        3: 'Error',
        4: 'Error',
        5: 'Error',
        6: 'Error',
        7: 'Error',
        8: 'No Order',
        9: 'Move to Strbd',
        10: 'Move to Port',
        11: 'Error',
        12: 'True',
        13: 'Magnetic',
        14: 'Error',
        15: 'NULL'
      }.get(bit4(data)),
    
    angle_order = degrees16(data),
    position = degrees16(data),
    reserved2 = int16(data)
   
    
  )
#127257: // Attitude 0x1F119
@pgn(127257, ['sid', 'yaw:real','pitch:real', 'roll:real',  'reserved' ])
def attitude(data):
  return dict(
    sid = uint8(data),
    yaw = degrees16(data),
    pitch = degrees16(data),
    roll = degrees16(data),
    reserved = uint8(data)
    
  )

#130310: // Temperature Data 0x1FD06
@pgn(130310, ['sid',  'water_temperature', 'air_temperature', 'baro_pressure', 'reserved'])
def environmental_conditions(data):
  return dict(
    sid = uint8(data),
    
      water_temperature = decimal(uint16(data),2),
      air_temperature = decimal(uint16(data),2),
      baro_pressure = decimal(uint16(data),1),
      reserved = uint8(data) 
  )


#130311: // ENviron Data 0x1FD07
@pgn(130311, ['sid', 'instance', 'humidity_instance:STRING', 'temperature_instance:STRING', 'temperature:real', 'humidity:real', 'atmospheric_pressure:real'])
def environmental_parameters(data):

  #log.info("NMEA ENviron Data  - PGN 0x1FD07 %s", data)
  
  try:
  
    sid = uint8(data)

    #instance = uint8(data)
    #041120 JLB Changed to allow value of 0xFF here since letting = NONE caused problems
    #There must always be an instance value
    instance = nint8(data)

    hinstance = ( instance >> 6 ) &  (0b00000011)
    tinstance = ( instance  ) &  (0b00111111)
    #log.info("NMEA ENviron Data  - PGN 0x1FD07 %s %s", hinstance, tinstance)
    
    #hinstance =4
    #tinstance =1
    # prior to 12/15/18 we only used the Type Fields and instance was always set to 0
    # Type was combination of humidity_instance and temperature_instance
    # Searches were done base only on types since we never set a instance for this PGN
    # when the record was added int he data base int he SYNC - the instance was missing so it defaulted to 0
    #
    # Now we wanted to expand the environment PGN to support multiple Zones created by the meshDimmer network sensors
    # Where we could multiple inside or outside temperature and humidity values.
    # Previous to 12/15/18 we only had two humidity choices (inside or outside)
    #
    # to expand this we needed to use the tinstance field beyond the first 16 choices.
    # to keep compatibility with existing records whihc only used the type fields and instance = 0
    # we will force instance to 0 when tinstance is less then 16 (0x0F) and set instance to non zero with tinstance greater = 0x0F
    # that way the old database searches will still work
    # not the best solution but done for backward compatibility
    #
    if tinstance < 16:
      instance = 0
    else:
      # mask of MSB because we dont want instance to be NO DATA when Humidity is missing
      # this would prevent temperatures to show up i the database search
      # This way the Humidity type will be maseked to either inside or outside
      instance =  ( instance  ) &  (0b01111111)

    humidity_instance = {
        0: 'Inside Humidity',
        1: 'Outside Humidity',      
        2: 'Reserved',
        3: 'No Data'
      }.get(hinstance)
    
    temperature_instance = {
      0: 'Sea Temperature',
      1: 'Outside Temperature',      
      2: 'Inside Temperature',
      3: 'Engine Room Temperature',
      4: 'Main Cabin Temperature',
      5: 'Live Well',
      6: 'Bait Well',
      7: 'Refrigeration',
      8: 'Heating',
      9: 'Dew Point',
      10:'Wind Chill A',
      11:'Wind Chill T',
      12:'Heat Index',
      13:'Freezer',
      14:'EGT',
      15:'Fuel Flow',
      16:'Inside Zone0',
      17:'Inside Zone1',
      18:'Inside Zone2',
      19:'Inside Zone3',
      20:'Inside Zone4',
      21:'Inside Zone5',
      22:'Inside Zone6',
      23:'Inside Zone7',
      24:'Inside Zone8',
      25:'Inside Zone9',
      26:'Inside Zone10',
      27:'Inside Zone11',
      28:'Inside Zone12',
      29:'Inside Zone13',
      30:'Inside Zone14',
      31:'Inside Zone15',
      32:'Outside Zone0',
      33:'Outside Zone1',
      34:'Outside Zone2',
      35:'Outside Zone3',
      36:'Outside Zone4',
      37:'Outside Zone5',
      38:'Outside Zone6',
      39:'Outside Zone7',
      40:'Outside Zone8',
      41:'Outside Zone9',
      42:'Outside Zone10',
      43:'Outside Zone11',
      44:'Outside Zone12',
      45:'Outside Zone13',
      46:'Outside Zone14',
      47:'Outside Zone15',
      63:'No Data'
    }.get(tinstance)

    #log.info("NMEA ENviron Data  - PGN 0x1FD07  instance %s humidity_instance %s temperature_instance %s",  instance, humidity_instance, temperature_instance)

    temperature = decimal(uint16(data),2)
    humidity = mul(int16(data), .004)
    atmospheric_pressure = decimal(uint16(data),1)

    #log.info("NMEA ENviron Data  - PGN 0x1FD07 temperature %s  humidity %s pressure %s" , temperature, humidity,atmospheric_pressure)

    return dict(
      sid =  sid,
      # new instance field add on 12/15/18
      # previously it was defaulted to 0
      instance = instance,
      humidity_instance = humidity_instance,
      
      temperature_instance = temperature_instance,
      
      temperature = temperature,
      humidity =  humidity ,
      atmospheric_pressure = atmospheric_pressure
      
    )

  except:
    e = sys.exc_info()[0]
    log.info("NMEA XBEE - PGN 0x00FF09 error data " % e)
    
#130312: // Temperature Data 0x1FD08
@pgn(130312, ['sid', 'temperature_instance', 'temperature_source:STRING', 'actual_temperature', 'set_temperature', 'reserved','raw'])
def temperature(data):

  raw=getrawvalue(data)

  if raw[16] != '*':
    return None
  
  return dict(
    sid = uint8(data),

    #nint8 allows for 0xFF whihc is normally undefined
    #but caues a problem later when we try to add to database
    #so we allow for case when instance =0xFF which it really should not be.
    temperature_instance = nint8(data),

      
     temperature_source = {
          0: 'Sea Temperature',
          1: 'Outside Temperature',      
          2: 'Inside Temperature',
          3: 'Engine Room Temperature',
          4: 'Main Cabin Temperature',
          5: 'Live Well',
          6: 'Bait Well',
          7: 'Refrigeration',
          8: 'Heating',
          9: 'Dew Point',
          10:'Wind Chill A',
          11:'Wind Chill T',
          12:'Heat Index',
          13:'Freezer',
          14:'EGT',
          15:'Fuel Flow',
          128:'Reserved 128',
          129:'Reserved 129',
          130:'Reserved 130',
          131:'Reserved 131',
          132:'Reserved 132',
          133:'Reserved 133',
          134:'Reserved 134',
          135:'Reserved 135',
          136:'Reserved 136',
          137:'Reserved 137',
          138:'Reserved 138',
          139:'Reserved 139',
          254:'Error',         
          255:'No Data'
        }.get(nint8(data)),
      
      actual_temperature = decimal(uint16(data),2),
      set_temperature = decimal(uint16(data),2),
      reserved = uint8(data),
      raw=raw

  )


#130316: // Temperature Data 0x1FD08
@pgn(130316, ['sid', 'temperature_instance', 'temperature_source:STRING', 'actual_temperature', 'set_temperature','raw'])
def temperature_extended(data):

  raw=getrawvalue(data)

  if raw[16] != '*':
    return None
  
  return dict(
    sid = uint8(data),

    #nint8 allows for 0xFF whihc is normally undefined
    #but caues a problem later when we try to add to database
    #so we allow for case when instance =0xFF which it really should not be.
    temperature_instance = nint8(data),

      
     temperature_source = {
          0: 'Sea Temperature',
          1: 'Outside Temperature',      
          2: 'Inside Temperature',
          3: 'Engine Room Temperature',
          4: 'Main Cabin Temperature',
          5: 'Live Well',
          6: 'Bait Well',
          7: 'Refrigeration',
          8: 'Heating',
          9: 'Dew Point',
          10:'Wind Chill A',
          11:'Wind Chill T',
          12:'Heat Index',
          13:'Freezer',
          14:'EGT',
          15:'Fuel Flow',

          254:'Error',         
          255:'No Data'
        }.get(nint8(data)),
      
      actual_temperature = decimal(uint24(data),3),
      set_temperature = decimal(uint16(data),2),
      raw=raw

  )


#130323: // Meteorological Station Data 0x1FD13
@pgn(130323, [ 'mode:STRING', 'reserved:STRING','days', 'ms:BIGINT', 'lat:real', 'lng:real', 'wind_speed', 'wind_direction',  'reserved1', 'wind_reference:STRING', 'wind_gusts', 'atmospheric_pressure:real',  'temperature:real'])
def meteorological_station_data(data):
  return dict(


    mode = {
        0: 'Autonomous mode',
        1: 'Differential, enhanced mode',      
        2: 'Estimated mode',
        3: 'Simulator mode',
        4: 'Manual mode',
        5: 'Reserved',
        6: 'Reserved',
        7: 'Reserved',
        8: 'Reserved',
        9: 'Reserved',
        10:'Reserved',
        11:'Reserved',
        12:'Reserved',
        13:'Reserved',
        14:'Error',
        15:'No Data'
      }.get(bit4(data)),
    
   reserved = {
        0: 'Reserved',
        1: 'Reserved',      
        2: 'Reserved',
        3: 'Reserved',
        4: 'Reserved',
        5: 'Reserved',
        6: 'Reserved',
        7: 'Reserved',
        8: 'Reserved',
        9: 'Reserved',
        10:'Reserved',
        11:'Reserved',
        12:'Reserved',
        13:'Reserved',
        14:'Reserved',
        15:'No Data'
      }.get(bit4(data)),

    days = int16(data), 
    ms = int32(data) * 100,

    
    lat = decimal(int32(data),7),
    lng = decimal(int32(data),7),

    wind_speed = uint16(data),
    wind_direction = udegrees16(data),
    reserved1 = bit4(data),
    
    wind_reference = {
        0: 'Error',
        1: 'Error',      
        2: 'Error',
        3: 'Error',
        4: 'Error',
        5: 'Error',
        6: 'Error',
        7: 'Error',
        8: 'TWIND True North',
        9: 'TWIND Mag North',
        10: 'Apparent Wind',
        11: 'TWIND VCGR',
        12: 'TWIND VCWR',
        13: 'Reserved',
        14: 'Error',
        15: 'NULL'
      }.get(bit4(data)),

    wind_gusts = uint16(data),

    atmospheric_pressure = decimal(uint16(data),1) ,   
    temperature = decimal(uint16(data),2)


    
  )




#129026: // COG and SOG
@pgn(129026, ['sid', 'reserved1', 'cog_reference:STRING', 'course_over_ground:real', 'speed_over_ground:real', 'reserved2'])
def cogsog(data):

  #log.info("NMEA COGSOG - data %s", data.getvalue())
  
  return dict(
   sid = uint8(data),
   reserved1 = bit4(data),
   cog_reference = {
        0: 'Error',
        1: 'Error',      
        2: 'Error',
        3: 'Error',
        4: 'Error',
        5: 'Error',
        6: 'Error',
        7: 'Error',
        8: 'Error',
        9: 'Error',
        10: 'Error',
        11: 'Error',
        12: 'True',
        13: 'Magnetic',
        14: 'Error',
        15: 'NULL'
      }.get(bit4(data)),

    #Problem here !!! 0 cause = none
    course_over_ground = udegrees16(data),
    #course_over_ground =  mul(xint16(data), .0057),
    speed_over_ground = decimal(uint16(data),2),
    #speed_over_ground = uint16(data)* 0.01,
    #speed_over_ground = xint16(data),
    reserved2 = uint16(data)
    
  )

#129025: // Position Rapid
@pgn(129025, ['lat:real', 'lng:real'])
def position_rapid(data):

  return dict(
    lat = decimal(int32(data),7),
    lng = decimal(int32(data),7)
  )




#129029: // GNSS Position Data 0x1F805
@pgn(129029, ['sid', 'days', 'ms:BIGINT', 'lat:real', 'lng:real', 'altitude:real', 'typeofsystem:STRING', 'method:STRING',  'integrity:STRING', 'reserved:STRING', 'siv'])
def gnss_position_data(data):
  return dict(


    sid = uint8(data),

    days = int16(data), 
    ms = int32(data) * 100,

    
    lat = decimal(int64(data),16),
    lng = decimal(int64(data),16),
    altitude = decimal(int64(data),6),

    method = {
        0: 'no GPS',
        1: 'GNSS fix',      
        2: 'DGNSS fix',
        3: 'Precise GNSS',
        4: 'RTK Fixed Integer',
        5: 'RTK Float',
        6: 'Estimated mode',
        7: 'Manual Input',
        8: 'Simulate mode',
        9: 'Reserved',
        10: 'Reserved',
        11: 'Reserved',
        12: 'Reserved',
        13: 'Reserved',
        14: 'Error',
        15: 'NULL'
      }.get(bit4(data)),
    
    typeofsystem = {
        0: 'GPS',
        1: 'GLONASS',      
        2: 'GPS+GLONASS',
        3: 'GPS+SBAS',
        4: 'GPS+SBAS+GLONASS',
        5: 'Reserved',
        6: 'Reserved',
        7: 'Reserved',
        8: 'Reserved',
        9: 'Reserved',
        10: 'Reserved',
        11: 'Reserved',
        12: 'Reserved',
        13: 'Reserved',
        14: 'Error',
        15: 'NULL'
      }.get(bit4(data)),

    reserved = {
        0: 'Reserved',
        1: 'Reserved',      
        2: 'Reserved',
        3: 'Reserved',
        4: 'Reserved',
        5: 'Reserved',
        6: 'Reserved',
        7: 'Reserved',
        8: 'Reserved',
        9: 'Reserved',
        10:'Reserved',
        11:'Reserved',
        12:'Reserved',
        13:'Reserved',
        14:'Reserved',
        15:'No Data'
      }.get(bit4(data)),

    integrity = {
        0: 'No Integrity',
        1: 'Safe,',      
        2: 'Caution,',
        3: 'Unsafe',
        4: 'No Integrity',
        5: 'Safe',
        6: 'Caution',
        7: 'Unsafe',
        8: 'No Integrity',
        9: 'Safe',
        10: 'Caution',
        11: 'Unsafe',
        12: 'No Integrity',
        13: 'Safe',
        14: 'Caution',
        15: 'Unsafe'
      }.get(bit4(data)),



    siv = uint8(data)


    
  )






#128267: // Water Depth  0x1F50B
@pgn(128267, ['sid', 'depth:real', 'transducer_offset',  'reserved' ])
def water_depth(data):
  return dict(
    sid = uint8(data),
    depth = decimal(uint32(data),2),
    transducer_offset = decimal(int16(data),3),

    reserved = uint8(data)
    
  )

#128259: // Water Speed
@pgn(128259, ['sid', 'waterspeed:real', 'groundspeed', 'type_reference:STRING', 'reserved' ])
def water_speed(data):
  return dict(
    sid = uint8(data),
    waterspeed = decimal(int16(data),2),
    groundspeed = decimal(int16(data),2),
    
     type_reference = {

          0: 'Paddle Wheel',      
          1: 'Pitot Tube',
          2: 'Doppler Log',
          3: 'Correlation Log',
          4: 'EM Log',
          5: 'Reserved',
          6: 'Reserved',
          7: 'Reserved',
          8: 'Reserved',
          9: 'Reserved',
          10:'Reserved',
          11:'Reserved',
          12:'Reserved',
          13:'Reserved',
          14:'Reserved',
          15:'Reserved',
          
          254:'Error',         
          255:'No Data'
        }.get(uint8(data)),
    
    reserved = int16(data)
    
  )

#65286: // Custom PGN  - SeaSmart Dimmer 0x0FF06
@pgn(65286, ['pgntype','dimmertype','instance','dimmer0','dimmer1','dimmer2','dimmer3','control'])
def dimmer(data):
  #log.info("NMEA Dimmer - PGN 0x00FF06 %s", data)
  
  return dict(
    pgntype = uint16(data),
    dimmertype = {
        0: 'LED 1 Channel',
        1: 'LED 1 Channel 01',      
        2: 'LED 1 Channel 02',
        3: 'LED 1 Channel 03',
        4: 'LED 1 Channel 04',
        5: 'LED 1 Channel 05',
        6: 'LED 1 Channel 06',
        7: 'LED 1 Channel 07',
        8: 'RGB 1 Channel',
        9: 'RGB 1 Channel 01',
        10: 'RGB 1 Channel 02',
        11: 'RGB 1 Channel 03',
        12: 'LED 4 Channel',
        13: 'LED 4 Channel 01',
        14: 'LED 4 Channel 02',
        15: 'LED 4 Channel 03'
      }.get(bit4(data)),
    instance = bit4(data),
    #instance = nint8(data),
    dimmer0 = nint8(data),
    dimmer1 = nint8(data),
    dimmer2 = nint8(data),
    dimmer3 = nint8(data),
    control = nint8(data)
    )


#65292: // Custom PGN  - SeaSmart Indicator Runtime 0x0FF0C
@pgn(65292, ['pgntype','instance','channel','runtime_sec','cycles'])
def indicator_runtime(data):
  log.info("NMEA Indicator Runtime - PGN 0x00FF0C %s", data)
  
  return dict(
    pgntype = uint16(data),
    #nint8 allows for 0xFF whihc is normally undefined
    #but caues a problem later when we try to add to database
    #so we allow for case when instance =0xFF which it really should not be.
    instance = nint8(data),
    channel = nint8(data),
    #instance = nint8(data),
    runtime_sec = uint24(data),
    cycles = uint8(data)

    )      


#65289: // Custom PGN  - SeaSmart XBEE Dimmer 0x0FF09 Data Sample Rx Indicator frame - 0x92
@pgn(65289, ['pgntype','instance','mac','reserved','options','samples','dmask','amask','digital_value','analog_value','crc'])
def xbee_data_sample(data):
  #log.info("NMEA XBEE - PGN 0x00FF09 %s", data)
  try:
    pgntype0 = nint8(data)
    pgntype1 = nint8(data)
    instance = nint8(data)
    #mac = uint64(data),
    mac0 = nint8(data)
    mac1 = nint8(data)
    mac2 = nint8(data)
    mac3 = nint8(data)
    mac4 = nint8(data)
    mac5 = nint8(data)
    mac6 = nint8(data)
    mac7 = uint8(data)

        
    reserved0 = nint8(data)
    reserved1 = nint8(data)
    options = nint8(data)
    samples = nint8(data)
    dmask0 = nint8(data)
    dmask1 = nint8(data)
    amask = nint8(data)
    #digital_value = uint16(data)
    digital_value0 = nint8(data)
    digital_value1 = nint8(data)
    
    #analog_value = uint16(data)
    analog_value0 = nint8(data)
    analog_value1 = nint8(data)
    
    crc = nint8(data)


    #mac = "AABBCCDDEEFF0011"
    mac = str("{:02X}".format(int(mac0))) + str("{:02X}".format(int(mac1)) ) + str( "{:02X}".format(int(mac2)) ) + str( "{:02X}".format(int(mac3)) ) + str( "{:02X}".format(int(mac4)) ) + str( "{:02X}".format(int(mac5)) ) + str( "{:02X}".format(int(mac6)) ) + str( "{:02X}".format(int(mac7))  )

    digital_state = (int(digital_value0)*256) + int(digital_value1)

    if digital_state > 0:
      digital_state = 1

      
    #digital_value = str("{:02X}".format(int(digital_value0))) + str("{:02X}".format(int(digital_value1)) )
    
    #log.info("NMEA XBEE - PGN 0x00FF09 %s:%s", analog_value0, analog_value1)
    #log.info("NMEA XBEE - PGN 0x00FF09 analog_value:%s", analog_value)
    #log.info("NMEA XBEE - PGN 0x00FF09 digital_value:%s", digital_value)
    #log.info("NMEA XBEE - PGN 0x00FF09 analog_value:%s", dmask)
    #log.info("NMEA XBEE - PGN 0x00FF09 digital_value:%s", amask)
    
    
    #analog_value =  str("{:02X}".format(int(analog_value0))) + str("{:02X}".format(int(analog_value1)) )
    #analog_value =  0
    
    return dict(
      pgntype =  str("{:02X}".format(int(pgntype0))) + str("{:02X}".format(int(pgntype1)) ),
      #pgntype =  "99E1",
      instance = instance,
      mac = mac,
      
      reserved =  str("{:02X}".format(int(reserved0))) + str("{:02X}".format(int(reserved1)) ),
      #reserved  =  "FFFE",
      options = str("{:02X}".format(int(options))),
      #options = "00",
      samples = samples,
      dmask = str("{:02X}".format(int(dmask0))) + str("{:02X}".format(int(dmask1)) ),
      #dmask = "0000",
      amask = str("{:02X}".format(int(amask))),
      #amask = "00",
      #digital_value = str("{:02X}".format(int(digital_value0))) + str("{:02X}".format(int(digital_value1)) ),
      digital_value = int(digital_state),
      #analog_value =  str("{:02X}".format(int(analog_value0))) + str("{:02X}".format(int(analog_value1)) ),
      analog_value =  (int(analog_value0) *256)+ int(analog_value1) ,
      crc = crc
      
      )


  except:
    e = sys.exc_info()[0]
    log.info("NMEA XBEE - PGN 0x00FF09 error data " % e)



#65290: // Custom PGN  - SeaSmart XBEE Dimmer 0x0FF0A Remote Command Response frame - 0x97
@pgn(65290, ['pgntype','instance','mac','reserved','command','status','crc'])
def xbee_command_response(data):
  #log.info("NMEA XBEE - PGN 0x00FF0A ", data)

  #Need to use nint on these and not uint
  #Because these values may be FF which uint retuns NONE and not FF
  #nint returns actual value

  
  try:
    pgntype0 = nint8(data)
    pgntype1 = nint8(data)
    instance = nint8(data)
    #mac = uint64(data)
    
    mac0 = nint8(data)
    mac1 = nint8(data)
    mac2 = nint8(data)
    mac3 = nint8(data)
    mac4 = nint8(data)
    mac5 = nint8(data)
    mac6 = nint8(data)
    mac7 = nint8(data)

        
    reserved0 = nint8(data)
    reserved1 = nint8(data)
    #command = uint16(data)
    command0 = nint8(data)
    command1 = nint8(data)
    status = nint8(data)
    crc = nint8(data)


    mac = str("{:02X}".format(int(mac0))) + str("{:02X}".format(int(mac1)) ) + str( "{:02X}".format(int(mac2)) ) + str( "{:02X}".format(int(mac3)) ) + str( "{:02X}".format(int(mac4)) ) + str( "{:02X}".format(int(mac5)) ) + str( "{:02X}".format(int(mac6)) ) + str( "{:02X}".format(int(mac7))  )
    #mac = "AABBCCDDEEFF0011"

    #log.info("NMEA XBEE - PGN 0x00FF09 %s", mac0hex.decode("ascii"))
    
    return dict(
      pgntype =  str("{:02X}".format(int(pgntype0))) + str("{:02X}".format(int(pgntype1)) ),
      #pgntype =  "99E1",
      instance = instance,
      mac=mac,
      reserved  =  str("{:02X}".format(int(reserved0))) + str("{:02X}".format(int(reserved1)) ),
      #reserved  =  "A55A",
      command = str("{:02X}".format(int(command0))) + str("{:02X}".format(int(command1)) ),
      status = status,
      crc = crc
      
      )

  
  except:
      e = sys.exc_info()[0]
      log.info("NMEA XBEE - PGN 0x00FF09 error data " % e)

# 127501: Binary Switch Bank Status
# hex: 1F20D
@pgn(127501, ['instance', 'indic01', 'indic02', 'indic03', 'indic04', 'indic05', 'indic06', 'indic07', 'indic08','indic09', 'indic10', 'indic11', 'indic12', 'indic13', 'indic14', 'indic15', 'indic16', 'indic17', 'indic18','indic19', 'indic20', 'indic21', 'indic22', 'indic23', 'indic24', 'indic25', 'indic26', 'indic27', 'indic28','bank0', 'bank1', 'bank2','raw'])
def binary_switch_bank_status(data):

    raw=getrawvalue(data)

    if raw[16] != '*':
      return None
  
    instance = uint8(data)
    indic04, indic03 = getswitch(data)
    indic02, indic01 = getswitch(data)
    indic08, indic07 = getswitch(data)
    indic06, indic05 = getswitch(data)
    indic12, indic11 = getswitch(data)
    indic10, indic09 = getswitch(data)
    indic16, indic15 = getswitch(data)
    indic14, indic13 = getswitch(data)
    indic20, indic19 = getswitch(data)
    indic18, indic17 = getswitch(data)
    indic24, indic23 = getswitch(data)
    indic22, indic21 = getswitch(data)
    indic28, indic27 = getswitch(data)
    indic26, indic25 = getswitch(data)

    bank0=0
    bank1=0
    bank2=0

        
    if indic01 == 1:
      bank0 = bank0 | 0x01
    if indic02 == 1:
      bank0 = bank0 | 0x02
    if indic03 == 1:
      bank0 = bank0 | 0x04
    if indic04 == 1:
      bank0 = bank0 | 0x08
    if indic05 == 1:
      bank0 = bank0 | 0x10
    if indic06 == 1:
      bank0 = bank0 | 0x20
    if indic07 == 1:
      bank0 = bank0 | 0x40
    if indic08 == 1:
      bank0 = bank0 | 0x80

    if indic09 == 1:
      bank1 = bank1 | 0x01
    if indic10 == 1:
      bank1 = bank1 | 0x02
    if indic11 == 1:
      bank1 = bank1 | 0x04
    if indic12 == 1:
      bank1 = bank1 | 0x08
    if indic13 == 1:
      bank1 = bank1 | 0x10
    if indic14 == 1:
      bank1 = bank1 | 0x20
    if indic15 == 1:
      bank1 = bank1 | 0x40
    if indic16 == 1:
      bank1 = bank1 | 0x80

    if indic17 == 1:
      bank2 = bank2 | 0x01
    if indic18 == 1:
      bank2 = bank2 | 0x02
    if indic19 == 1:
      bank2 = bank2 | 0x04
    if indic20 == 1:
      bank2 = bank2 | 0x08
    if indic21 == 1:
      bank2 = bank2 | 0x10
    if indic22 == 1:
      bank2 = bank2 | 0x20
    if indic23 == 1:
      bank2 = bank2 | 0x40
    if indic24 == 1:
      bank2 = bank2 | 0x80
      
      
    return dict(
      instance  = instance,
      indic01 = indic01,
      indic02 = indic02,
      indic03 = indic03,
      indic04 = indic04,
      indic05 = indic05,
      indic06 = indic06,
      indic07 = indic07,
      indic08 = indic08,
      indic09 = indic09,
      indic10 = indic10,
      indic11 = indic11,
      indic12 = indic12,
      indic13 = indic13,
      indic14 = indic14,
      indic15 = indic15,
      indic16 = indic16,
      indic17 = indic17,
      indic18 = indic18,
      indic19 = indic19,
      indic20 = indic20,
      indic21 = indic21,
      indic22 = indic22,
      indic23 = indic23,
      indic24 = indic24,
      indic25 = indic25,
      indic26 = indic26,
      indic27 = indic27,
      indic28 = indic28,
      bank0=bank0,
      bank1=bank1,
      bank2=bank2,
      raw=raw
    
    )

# 127502: Binary Switch Bank Control
# hex: 1F20E
@pgn(127502, ['instance', 'switch01', 'switch02', 'switch03', 'switch04', 'switch05', 'switch06', 'switch07', 'switch08','switch09', 'switch10', 'switch11', 'switch12', 'switch13', 'switch14', 'switch15', 'switch16', 'switch17', 'switch18','switch19', 'switch20', 'switch21', 'switch22', 'switch23', 'switch24', 'switch25', 'switch26', 'switch27', 'switch28','raw'])
def switch_bank_control(data):

    raw=getrawvalue(data)

    if raw[16] != '*':
      return None

  
    instance = uint8(data)
    switch04, switch03 = getswitch(data)
    switch02, switch01 = getswitch(data)
    switch08, switch07 = getswitch(data)
    switch06, switch05 = getswitch(data)
    switch12, switch11 = getswitch(data)
    switch10, switch09 = getswitch(data)
    switch16, switch15 = getswitch(data)
    switch14, switch13 = getswitch(data)
    switch20, switch19 = getswitch(data)
    switch18, switch17 = getswitch(data)
    switch24, switch23 = getswitch(data)
    switch22, switch21 = getswitch(data)
    switch28, switch27 = getswitch(data)
    switch26, switch25 = getswitch(data)
  
    return dict(
      instance  = instance,
      switch01 = switch01,
      switch02 = switch02,
      switch03 = switch03,
      switch04 = switch04,
      switch05 = switch05,
      switch06 = switch06,
      switch07 = switch07,
      switch08 = switch08,
      switch09 = switch09,
      switch10 = switch10,
      switch11 = switch11,
      switch12 = switch12,
      switch13 = switch13,
      switch14 = switch14,
      switch15 = switch15,
      switch16 = switch16,
      switch17 = switch17,
      switch18 = switch18,
      switch19 = switch19,
      switch20 = switch20,
      switch21 = switch21,
      switch22 = switch22,
      switch23 = switch23,
      switch24 = switch24,
      switch25 = switch25,
      switch26 = switch26,
      switch27 = switch27,
      switch28 = switch28,
      raw=raw
    )


#130944: // Custom PGN  - SeaSmart ID/MAc Address
# Bytes 0 - 3 = Manufact ID 0xE199 (correct) or 0x099E1 (incorrect)
# Bytes 4-15 = MACID
# Bytes 16 - 39 = Device Name String
# Bytes 40-41 - Session ID
# Bytes 42-43 - HW Version
# Bytes 44-45 = FW Version


# 129039: AIS_Class_B_Position_Report
# hex: 1F80F
#@pgn(129039, ['messageid', 'repeat', 'userid', 'lat', 'lng', 'positionstate', 'timestamp', 'cog', 'sog','raw'])
@pgn(129039, ['raw'])
def AIS_Class_B_Position_Report(data):

  log.info("AIS_Class_B_Position_Report - PGN 0x1F80F ", data)

  try:
    raw=getrawvalue(data)


    #messageid = nint8(data)
    #userid = int32(data)
    
    return dict(raw=raw )
  
  except TypeError as e:
    log.info('AIS_Class_B_Position_Report - PGN 0x1F80F: TypeError  %s:  ' % str(e))
    pass

  except ValueError as e:
    log.info('AIS_Class_B_Position_Report - PGN 0x1F80F: ValueError  %s:  ' % str(e))
    pass
  
  except:
    e = sys.exc_info()[0]
    log.info("AIS_Class_B_Position_Report - PGN 0x1F80F error " % e)
    return dict( error='error',)
    pass


# 129040: AIS_Class_B_Position_Report
# hex: 1F810
#@pgn(129040, ['messageid', 'repeat', 'userid', 'lat', 'lng', 'positionstate', 'timestamp', 'cog', 'sog','raw'])
@pgn(129040, ['raw'])
def AIS_Class_B_ExtendedPosition_Report(data):

  log.info("AIS_Class_B_ExtendedPosition_Report - PGN 0x1F80F ", data)

  try:
    raw=getrawvalue(data)


    #messageid = nint8(data)
    #userid = int32(data)
    
    return dict(raw=raw )
  
  except TypeError as e:
    log.info('AIS_Class_B_ExtendedPosition_Report - PGN 0x1F80F: TypeError  %s:  ' % str(e))
    pass

  except ValueError as e:
    log.info('AIS_Class_B_ExtendedPosition_Report - PGN 0x1F80F: ValueError  %s:  ' % str(e))
    pass
  
  except:
    e = sys.exc_info()[0]
    log.info("AIS_Class_B_ExtendedPosition_Report - PGN 0x1F80F error " % e)
    return dict( error='error',)
    pass  

@pgn(130944, ['datetime:real'])
def heartbeat(data):
  #dt = datetime.datetime.now()
  # check if this is  CDI custom PGN type
  # 0xE199 (57753) or 0x99E1 (39393)

  #log.info("NMEA Heartbeat Data start - PGN 130944  ")
  mymacstr = ""
  mydevicestr = ""
  mysessionstr = ""
  myHWVerstr = ""
  myFWVerstr = ""





  try:
    """    
    return dict(
      mac_address = mymacstr,
      device_id= mydevicestr,
      session_id = mysessionstr,
      hw_ver = myHWVerstr,
      fw_ver = myFWVerstr )
    """           
    pgntype = uint16(data)

    
    #0xE199 or   0x99E1
    if pgntype == 57753 or pgntype == 39393:
      # good CDI custom ac watt hours PGN

#    for i in range(count):
#      val += int(data.read(2), 16) << (8*i)
      
      myvarch = 0
      for i in range (12):
        #myvarch = data.read(2)
        myvarch = format((int(data.read(1),16)), 'X')
        #myvarch += int(data.read(1), 16) << (4*i)
        mymacstr = mymacstr + str(myvarch)
        #mymacstr = mymacstr + str(int(myvarch, 16))
      #mymacstr = myvarch

      #log.info("NMEA Heartbeat Data start - PGN 130944  mymacstr %s", str(mymacstr))

      """
      return dict(
        mac_address = "DEDEDEDEDE",
        device_id= mydevicestr,
        session_id = mysessionstr,
        hw_ver = myHWVerstr,
        fw_ver = myFWVerstr )
      """

      for i in range (0,24):
        myvarch = data.read(2)
        mydevicestr = mydevicestr + chr(int(myvarch, 16))
        
      #log.info("NMEA Heartbeat Data start - PGN 130944  mydevicestr %s", mydevicestr)

      """
      return dict(
        mac_address = "DEDEDEDEDE",
        device_id= "SOMEDEVICE",
        session_id = "000112",
        hw_ver = myHWVerstr,
        fw_ver = myFWVerstr )      
      """

      for i in range (0,6):
        myvarch = data.read(2)
        mysessionstr = mysessionstr + chr(int(myvarch, 16))     

        
      log.info("NMEA Heartbeat Data start - PGN 130944  mysessionstr %s", str(mysessionstr))

      

      for i in range (0,10):
        myvarch = data.read(2)
        myHWVerstr = myHWVerstr + chr(int(myvarch, 16))

      #log.info("NMEA Heartbeat Data start - PGN 130944  myHWVerstr %s", str(myHWVerstr))
        

      for i in range (0,10):
        myvarch = data.read(2)
        myFWVerstr = myFWVerstr + chr(int(myvarch, 16))

      #log.info("NMEA Heartbeat Data start - PGN 130944  myFWVerstr %s", str(myFWVerstr))        





      
      return dict(
        mac_address = str(mymacstr),
        device_id= str(mydevicestr),
        session_id = int(mysessionstr),
        hw_ver = str(myHWVerstr),
        fw_ver = str(myFWVerstr) )


  # if error then return nulled (none) 0x7F or 0x7FFF 0r 0x7FFFFFF
  #except ValueError:
  except TypeError as e:
    log.info('NMEA Heartbeat Data start - PGN 130944: TypeError  %s:  ' % str(e))
    pass

  except ValueError as e:
    log.info('NMEA Heartbeat Data start - PGN 130944: ValueError  %s:  ' % str(e))
    pass
  
  except:
    e = sys.exc_info()[0]
    log.info("NMEA Heartbeat Data  - PGN 130944 " % e)
    return dict( error='error',)
    pass


@pgn(130942, ['imea_number', 'iccid_number', 'phone_number', 'db_status', 'ci_status', 'ai_status' ])
def seasmart_cellular_status(data):
  #dt = datetime.datetime.now()
  # check if this is  CDI custom PGN type
  # 0xE199 (57753) or 0x99E1 (39393)

  log.info("NMEA Cellular Connection Status - PGN 130942  Start  ")

  myimeastr = ""
  myiccidstr = ""
  myphonestr = ""
  myDBstr = "255"
  myCIstr = "255"
  myAIstr = "255"

  try:
        
               
    pgntype = uint16(data)

    log.info("NMEA Cellular Connection Status - PGN 130942  pgntype %s", str(pgntype))

    
    #0xE199 
    if pgntype == 39393:
      # good CDI custom cellular connection status PGN


      myvarch = 0
      for i in range (16):
        myvarch = format((int(data.read(1),16)), 'X')
        myimeastr = myimeastr + str(myvarch)


      log.info("NMEA Cellular Connection Status - PGN 130942  myimeastr %s", str(myimeastr))

        
      myvarch = 0
      for i in range (20):
        myvarch = format((int(data.read(1),16)), 'X')
        myiccidstr = myiccidstr + str(myvarch)


      log.info("NMEA Cellular Connection Status - PGN 130942  myiccidstr %s", str(myiccidstr))



      myvarch = 0
      for i in range (12):
        myvarch = format((int(data.read(1),16)), 'X')
        myphonestr = myphonestr + str(myvarch)


      log.info("NMEA Cellular Connection Status - PGN 130942  myphonestr %s", str(myphonestr))



      #myvarch = data.read(2)
      #myDBstr =  int(myvarch, 16)
      myDBstr =   format((int(data.read(2),16)), 'X')
        
      log.info("NMEA Cellular Connection Status - PGN 130942  myDBstr %s", myDBstr)




      #myvarch = data.read(2)
      #myCIstr =  int(myvarch, 16))
      myCIstr =   format((int(data.read(2),16)), 'X')
             
      log.info("MEA Cellular Connection Status - PGN 130942  myCIstr %s", myCIstr)



      #myvarch = data.read(2)
      #myAIstr =  int(myvarch, 16))
      myAIstr =   format((int(data.read(2),16)), 'X')
      
      log.info("MEA Cellular Connection Status - PGN 130942  myAIstr %s", myAIstr)

  
      return dict(
        imea_number = str(myimeastr),
        iccid_number= str(myiccidstr),
        phone_number = str(myphonestr),
        db_status = int(myDBstr,16),
        ci_status = int(myCIstr,16),
        ai_status = int(myAIstr,16) )



  except TypeError as e:
    log.info('MEA Cellular Connection Status - PGN 130942: TypeError  %s:  ' % str(e))
    pass

  except ValueError as e:
    log.info('NMEA Cellular Connection Status - PGN 130942: ValueError  %s:  ' % str(e))
    pass
  
  except:
    e = sys.exc_info()[0]
    log.info("MEA Cellular Connection Status - PGN 130942 " % e)
    return dict( error='error',)
    pass


#130946: // CDI Custom PGN 130946 - (0x1FF82) Rain Detail
@pgn(130946, ['rainaccum','rainduration','rainrate','rainpeak'])
def rain_gauge(data):

    pgntype = uint16(data)

    log.info("CDI Custom PGN 130946 -  pgntype %s", str(pgntype))

    
    #0xE199 or   0x99E1
    if pgntype == 57753 or pgntype == 39393:
      # good CDI custom cellular connection status PGN
  
      rainaccum = uint16(data)
      rainduration = uint16(data)
      rainrate =uint16(data)
      rainpeak = uint16(data)

      
      return dict(
        pgntype=pgntype,
        rainaccum = rainaccum,
        rainduration = rainduration,
        rainrate = rainrate,
        rainpeak = rainpeak

        )  




#65287: // Custom PGN  - SeaSmart ac watt hours 0x0FF07
@pgn(65287, ['pgntype','instance','ac_type','ac_kwatt_hours'])
def ac_watt_hours(data):
  #log.info("NMEA ACWATTHOURS - PGN 0x00FF07 %s", data)


  # check if this is  CDI custom PGN type
  # 0xE199 (57753) or 0x99E1 (39393)
  
  pgntype = uint16(data)

  #0xE199 or   0x99E1
  if pgntype == 57753 or pgntype == 39393:
    # good CDI custom ac watt hours PGN
    return dict(
      pgntype = pgntype,
      instance = uint8(data),
      ac_type = {
            0: 'UTIL',
            1: 'GEN',      
            2: 'LED',
            254:'Error',         
            255:'No Data'
          }.get(uint8(data)),
      ac_kwatt_hours = decimal(int32(data),3)
      )  

  else:    
    return dict(
      pgntype = pgntype,
      status = "unknown custom PGN"

      )  

#65288: // Custom PGN  - SeaSmart ac status detail 0x0FF08
@pgn(65288, ['pgntype','ac_type','instance','ac_volts_detail','ac_amps_detail','status'])
def ac_status_detail(data):
  #log.info("NMEA ACDETAIL - PGN 0x00FF08 %s", data)



  # check if this is  CDI custom PGN type
  # 0xE199 (57753) or 0x99E1 (39393)
  
  pgntype = uint16(data)

  
  if pgntype == 57753 or pgntype == 39393:
    # good CDI custom ac watt hours PGN
  
    return dict(
      pgntype = pgntype,

       
      ac_type = {
          0: 'UTIL',
          1: 'UTIL2',      
          2: 'UTIL3',
          3: 'UTIL4',
          4: 'LIGHTS',
          5: 'LIGHTS2',
          6: 'LIGHTS3',
          7: 'LIGHTS4',
          8: 'HEAT',
          9: 'HEAT2',
          10: 'OUTDOOR',
          11: 'OUTDOOR2',
          12: 'APPLIANCE',
          13: 'APPLIANCE2',
          14: 'GEN',
          15: 'GEN2'
        }.get(bit4(data)),


      instance = bit4(data),

      
      ac_volts_detail = decimal(uint16(data),1),
      ac_amps_detail = decimal(uint16(data),1),
      status= uint8(data)    
      )


  else:     
    return dict(
      pgntype = pgntype,
      status = "unknown custom PGN"

      )    

#65005: // J1939 PGN 65005 - (0x00FDED) Utility Total Energy
@pgn(65005, ['export_kwatt_hours','import_kwatt_hours'])
def ac_utility_total_energy(data):
  
  return dict(
    export_kwatt_hours = uint32(data),
    import_kwatt_hours = uint32(data)

    )

#65018: // J1939 PGN 65018 - (0x0FDFA) Utility Total Energy
@pgn(65018, ['export_kwatt_hours','import_kwatt_hours'])
def ac_generator_total_energy(data):
  
  return dict(
    export_kwatt_hours = uint32(data),
    import_kwatt_hours = uint32(data)

    )


#65014: // J1939 PGN 65014 - (0x0FDF6) Utility Phase A Basic AC Quantities
@pgn(65014, ['ac_line_line_volts','ac_line_neutral_volts','ac_frequency','ac_amps','ac_watts'])
def ac_utility_basic_phase_a(data):
  

  log.info("ac_utility_basic_phase_a  ")

  try:

    ac_line_line_volts = uint16(data)
    ac_line_neutral_volts = uint16(data)
    ac_frequency =uint16(data)
    ac_amps = uint16(data)
    ac_watts = ac_line_neutral_volts * ac_amps

    return dict(
    ac_line_line_volts = ac_line_line_volts,
    ac_line_neutral_volts = ac_line_neutral_volts,
    ac_frequency =ac_frequency,
    ac_amps = ac_amps,
    ac_watts =  ac_watts
      )  


  except TypeError as e:
    log.info('ac_utility_basic_phase_a: TypeError  %s:  ' % str(e))
    pass

  except ValueError as e:
    log.info('ac_utility_basic_phase_a: ValueError  %s:  ' % str(e))
    pass
  
  except:
    e = sys.exc_info()[0]
    log.info("ac_utility_basic_phase_a error " % e)
    return dict( error='error',)
    pass



  
#65011: // J1939 PGN 65011 - (0x0FDF3) Utility Phase B Basic AC Quantities
@pgn(65011, ['ac_line_line_volts','ac_line_neutral_volts','ac_frequency','ac_amps','ac_watts'])
def ac_utility_basic_phase_b(data):

  log.info("ac_utility_basic_phase_b  ")

  try:

    ac_line_line_volts = uint16(data)
    ac_line_neutral_volts = uint16(data)
    ac_frequency =uint16(data)
    ac_amps = uint16(data)
    ac_watts = ac_line_neutral_volts * ac_amps

    return dict(
    ac_line_line_volts = ac_line_line_volts,
    ac_line_neutral_volts = ac_line_neutral_volts,
    ac_frequency =ac_frequency,
    ac_amps = ac_amps,
    ac_watts =  ac_watts
      )  


  except TypeError as e:
    log.info('ac_utility_basic_phase_b: TypeError  %s:  ' % str(e))
    pass

  except ValueError as e:
    log.info('ac_utility_basic_phase_b: ValueError  %s:  ' % str(e))
    pass
  
  except:
    e = sys.exc_info()[0]
    log.info("ac_utility_basic_phase_b error " % e)
    return dict( error='error',)
    pass





#65008: // J1939 PGN 65008 - (0x0FDF0) Utility Phase C Basic AC Quantities
@pgn(65008, ['ac_line_line_volts','ac_line_neutral_volts','ac_frequency','ac_amps','ac_watts'])
def ac_utility_basic_phase_c(data):
  
  log.info("ac_utility_basic_phase_c  ")

  try:

    ac_line_line_volts = uint16(data)
    ac_line_neutral_volts = uint16(data)
    ac_frequency =uint16(data)
    ac_amps = uint16(data)
    ac_watts = ac_line_neutral_volts * ac_amps

    return dict(
    ac_line_line_volts = ac_line_line_volts,
    ac_line_neutral_volts = ac_line_neutral_volts,
    ac_frequency =ac_frequency,
    ac_amps = ac_amps,
    ac_watts =  ac_watts
      )  


  except TypeError as e:
    log.info('ac_utility_basic_phase_c: TypeError  %s:  ' % str(e))
    pass

  except ValueError as e:
    log.info('ac_utility_basic_phase_c: ValueError  %s:  ' % str(e))
    pass
  
  except:
    e = sys.exc_info()[0]
    log.info("ac_utility_basic_phase_c error " % e)
    return dict( error='error',)
    pass





#65017: // J1939 PGN 65017 - (0x0FDF9) Utility Total Basic AC Quantities
@pgn(65017, ['ac_line_line_volts','ac_line_neutral_volts','ac_frequency','ac_amps','ac_watts'])
def ac_utility_basic_average(data):
  
  
  
  
  log.info("ac_utility_basic_average  ")

  try:

    ac_line_line_volts = uint16(data)
    ac_line_neutral_volts = uint16(data)
    ac_frequency =uint16(data)
    ac_amps = uint16(data)
    ac_watts = ac_line_neutral_volts * ac_amps

    return dict(
    ac_line_line_volts = ac_line_line_volts,
    ac_line_neutral_volts = ac_line_neutral_volts,
    ac_frequency =ac_frequency,
    ac_amps = ac_amps,
    ac_watts =  ac_watts
      )  


  except TypeError as e:
    log.info('ac_utility_basic_average: TypeError  %s:  ' % str(e))
    pass

  except ValueError as e:
    log.info('ac_utility_basic_average: ValueError  %s:  ' % str(e))
    pass
  
  except:
    e = sys.exc_info()[0]
    log.info("ac_utility_basic_average error " % e)
    return dict( error='error',)
    pass






#65027: // J1939 PGN 65027 - (0x0FE03) Utility Phase A Basic AC Quantities
@pgn(65027, ['ac_line_line_volts','ac_line_neutral_volts','ac_frequency','ac_amps','ac_watts'])
def ac_generator_basic_phase_a(data):
  
  log.info("ac_generator_basic_phase_a  ")

  try:

    ac_line_line_volts = uint16(data)
    ac_line_neutral_volts = uint16(data)
    ac_frequency =uint16(data)
    ac_amps = uint16(data)
    ac_watts = ac_line_neutral_volts * ac_amps

    return dict(
    ac_line_line_volts = ac_line_line_volts,
    ac_line_neutral_volts = ac_line_neutral_volts,
    ac_frequency =ac_frequency,
    ac_amps = ac_amps,
    ac_watts =  ac_watts
      )  


  except TypeError as e:
    log.info('ac_generator_basic_phase_a: TypeError  %s:  ' % str(e))
    pass

  except ValueError as e:
    log.info('ac_generator_basic_phase_a: ValueError  %s:  ' % str(e))
    pass
  
  except:
    e = sys.exc_info()[0]
    log.info("ac_generator_basic_phase_a error " % e)
    return dict( error='error',)
    pass


#65024: // J1939 PGN 65024 - (0x0FE00) Utility Phase B Basic AC Quantities
@pgn(65024, ['ac_line_line_volts','ac_line_neutral_volts','ac_frequency','ac_amps','ac_watts'])
def ac_generator_basic_phase_b(data):
  
  
  log.info("ac_generator_basic_phase_b  ")

  try:

    ac_line_line_volts = uint16(data)
    ac_line_neutral_volts = uint16(data)
    ac_frequency =uint16(data)
    ac_amps = uint16(data)
    ac_watts = ac_line_neutral_volts * ac_amps

    return dict(
    ac_line_line_volts = ac_line_line_volts,
    ac_line_neutral_volts = ac_line_neutral_volts,
    ac_frequency =ac_frequency,
    ac_amps = ac_amps,
    ac_watts =  ac_watts
      )  


  except TypeError as e:
    log.info('ac_generator_basic_phase_b: TypeError  %s:  ' % str(e))
    pass

  except ValueError as e:
    log.info('ac_generator_basic_phase_b: ValueError  %s:  ' % str(e))
    pass
  
  except:
    e = sys.exc_info()[0]
    log.info("ac_generator_basic_phase_b error " % e)
    return dict( error='error',)
    pass



#65021: // J1939 PGN 65021 - (0x0FDFD) Utility Phase C Basic AC Quantities
@pgn(65021, ['ac_line_line_volts','ac_line_neutral_volts','ac_frequency','ac_amps','ac_watts'])
def ac_generator_basic_phase_c(data):
  
  
  log.info("ac_generator_basic_phase_c  ")

  try:

    ac_line_line_volts = uint16(data)
    ac_line_neutral_volts = uint16(data)
    ac_frequency =uint16(data)
    ac_amps = uint16(data)
    ac_watts = ac_line_neutral_volts * ac_amps

    return dict(
    ac_line_line_volts = ac_line_line_volts,
    ac_line_neutral_volts = ac_line_neutral_volts,
    ac_frequency =ac_frequency,
    ac_amps = ac_amps,
    ac_watts =  ac_watts
      )  


  except TypeError as e:
    log.info('ac_generator_basic_phase_c: TypeError  %s:  ' % str(e))
    pass

  except ValueError as e:
    log.info('ac_generator_basic_phase_c: ValueError  %s:  ' % str(e))
    pass
  
  except:
    e = sys.exc_info()[0]
    log.info("ac_generator_basic_phase_c error " % e)
    return dict( error='error',)
    pass



#650307: // J1939 PGN 65030 - (0x0FE06) Utility Total Basic AC Quantities
@pgn(65030, ['ac_line_line_volts','ac_line_neutral_volts','ac_frequency','ac_amps','ac_watts'])
def ac_generator_basic_average(data):
  
  
  
  
  log.info("ac_generator_basic_average  ")

  try:

    ac_line_line_volts = uint16(data)
    ac_line_neutral_volts = uint16(data)
    ac_frequency =uint16(data)
    ac_amps = uint16(data)
    ac_watts = ac_line_neutral_volts * ac_amps

    return dict(
    ac_line_line_volts = ac_line_line_volts,
    ac_line_neutral_volts = ac_line_neutral_volts,
    ac_frequency =ac_frequency,
    ac_amps = ac_amps,
    ac_watts =  ac_watts
      )  


  except TypeError as e:
    log.info('ac_generator_basic_average: TypeError  %s:  ' % str(e))
    pass

  except ValueError as e:
    log.info('ac_generator_basic_average: ValueError  %s:  ' % str(e))
    pass
  
  except:
    e = sys.exc_info()[0]
    log.info("ac_generator_basic_average error " % e)
    return dict( error='error',)
    pass




#130945: // GoFree data
# 041314 JLB
# Navico GoFree data
# hex:  1FF81
@pgn(130945, ['pgntype','dataid','instance','sysval:real'])
def gofree(data):



  pgntype = uint16(data)
  # check if field = 0x99E1 which is a SeaSMart Custom PGN
  if pgntype != 39393:
    # then not gofree data so just set defaults for now
    # need to fix this so we actually store the rest of the payload
    dataid = 65535,
    instance = 0,
    sysval = 0.0

    return dict(
      pgntype = pgntype,
      dataid = dataid,
      instance = instance,
      sysval = sysval

    )
    
  dataid = uint16(data)
  instance = uint8(data)
  
  sysval = getgofreevalue(data)

  # convert any units to a standard
  
  # temperature celsius to kelvin
  #if dataid in (49, 48, ):
  if dataid >= 49 and dataid <= 65:
    sysval = sysval + 274.15

  # pressure inHg to 0.1 Kpascals  
  elif dataid >= 66 and dataid <= 74:
    sysval = sysval * 3.386

  # pressure radians to degrees  
  elif dataid in(14, 15, 17, 37, 309, 310):
    sysval = sysval * 57.2957795

  # knots to meters/secs  
  elif dataid in(41, 42, 43, 44, 45, 46, 47):
    sysval = sysval * 0.514444
  
  #log.info(sysval)

  return dict(
    pgntype = pgntype,
    dataid = dataid,
    instance = instance,
    sysval = sysval

  )


#126992: // System Time
#System Time (126992)
# hex:  1F010

@pgn(126992, ['sid','time_source:STRING','days', 'ms:BIGINT', 'datetime:DATETIME'])
def system_time(data):
  sid = uint8(data)
  reserved = bit4(data)


  time_source = {
    0: 'GPS',
    1: 'GLONASS',
    2: 'Radio Station',
    3: 'Cesium/Rubid Clock',
    4: 'Cesium/Rubid Clock',
    5: 'Crystal Clock',
    6: 'SeaGauge',
    7: 'GNSS',
    8: 'HelmSmart',
    9: 'SeaSmart RTC',
    10: 'reserved',
    11: 'reserved',
    12: 'reserved',
    13: 'reserved',
    14: 'reserved',
    15: 'NULL'
    
  }.get(bit4(data))
 



  # cant use NONE for ms in timedelta function so
  # force to a value since sec can't be NULL

  #days = uint16(data)
  #  ms = mul( uint32(data)* 100)

  days = int16(data) 
  ms = int32(data) * 100

  dt = datetime.utcfromtimestamp(
    timedelta(days, 0, ms).total_seconds()
  )

  return dict(
    sid = sid,
    time_source = time_source,
    days = days,
    ms = ms,
    datetime = dt
  )



DECODER_MAP = {
  hex: (pos, method)
  for pos, (hex, method, fields) in enumerate(PGNS)
}

FIELDS = [
  dict(name='pgn',          type='STRING'), 
  dict(name='timestamp',    type='DATETIME'), 
  dict(name='source',     type='STRING'),
]

FIELDS.extend(
  [
    dict(name=method.__name__, type='RECORD', fields=fields)
    for hex, method, fields in PGNS
  ]
)

SCHEMA = Schema(FIELDS)

#Bytes are in Big endian order [MSB, LSB]
def readBEbytes(data, count):
  val = 0
  # 030614 JLB
  # added check for when data.read is not a hexadecial character pair
  try:
    for i in range(count):
      val = val << 8
      val = val + int(data.read(2), 16) 
    #log.info("NMEA - readbytes val %s ", val)
    return val
  
  # if error then return nulled (none) 0x7F or 0x7FFF 0r 0x7FFFFFF
  #except ValueError:
  except:
    e = sys.exc_info()[0]
    log.info("NMEA - readbytes error data " % e)
    return ( 2**((count*8)-1))

  
#Bytes are in little endian order [LSB, MSB]
def readbytes(data, count):
  val = 0
  # 030614 JLB
  # added check for when data.read is not a hexadecial character pair
  try:
    for i in range(count):
      val += int(data.read(2), 16) << (8*i)
    #log.info("NMEA - readbytes val %s ", val)
    return val
  
  # if error then return nulled (none) 0x7F or 0x7FFF 0r 0x7FFFFFF
  #except ValueError:
  except:
    e = sys.exc_info()[0]
    log.info("NMEA - readbytes error data " % e)
    return ( 2**((count*8)-1))

  


#Bytes are in little endian order [LSB, MSB]
def readbytes(data, count):
  val = 0
  # 030614 JLB
  # added check for when data.read is not a hexadecial character pair
  try:
    for i in range(count):
      val += int(data.read(2), 16) << (8*i)
    #log.info("NMEA - readbytes val %s ", val)
    return val
  
  # if error then return nulled (none) 0x7F or 0x7FFF 0r 0x7FFFFFF
  #except ValueError:
  except:
    e = sys.exc_info()[0]
    log.info("NMEA - readbytes error data " % e)
    return ( 2**((count*8)-1))

  

# create integer by reading Hex string
# integer length is based on num of bits
def readint(data, bits):
  # reads Hexadecial pair and checkes if = nulled (0XFF)
  val = nulled(readbytes(data, bits/8), bits-1)
  if val is not None:
    return twoscomplement(val,bits)

def twoscomplement(num,bits):
  val =  sum(2**x & num for x in range(bits-1))
  return  (-1 * (num & (2**(bits-1)))) + val

# For NMEA 2000 payload data
# Nulled data is either 0xFF or 0x7F
# for signed integers this is 0x7F
# This checks if value is 0x7F which is nulled or empty
def nulled(num, bits):
  if num == 0:
    return 0
  elif num == 2**bits-1:
    return None
  else:
    return num


def bit4(data):
  return int(data.read(1), 16)

#todo allow upacking pit fields that aren't byte aligned
bit2 = bit4

# 041314 JLB
# Routine to extract goFree sysVal from data stream
# Takes last N HEX values and converts to ACSII then creates a string
# String is then converted to float value
def getrawvalue(data):
  

  mystrvalue = ""
  mystrvalue = str(data.getvalue())
  """
  if data.seekable():

    mystart = data.tell()
      
    for i in range(count):
      myvarch = data.read(2)
      mystrvalue = mystrvalue + chr(int(myvarch, 16))

    data.seek(mystart)

 
  """
  return(mystrvalue)

# 041314 JLB
# Routine to extract goFree sysVal from data stream
# Takes last N HEX values and converts to ACSII then creates a string
# String is then converted to float value
def getgofreevalue(data):

  mystrvalue = ""
  myvarch = data.read(2)
  mystrvalue = chr(int(myvarch, 16))
  
  while myvarch != "":
    myvarch = data.read(2)
    if myvarch != "":
      mystrvalue = mystrvalue + chr(int(myvarch, 16))

  value = float(mystrvalue)

  return(value)


# unpack switch status bits 2 at  atime
def getswitch(data):
  swbyte = int(data.read(1), 16)
  swhb = (swbyte >> 2)  & (0b0011)
  swlb = swbyte & (0b0011)
  return(swhb, swlb)
  

def bitmap(data, labels):
  # skip for now

  bytes = len(labels) / 8
  readbytes(data, bytes)
  return ''

def nint8(data):
  return readbytes(data, 1)

def uint8(data):
  return nulled(readbytes(data, 1),8)

def xint16(data):
  return readbytes(data, 2)

def uint16(data):
  return nulled(readbytes(data, 2),16)

def uintBE16(data):
  return nulled(readBEbytes(data, 2),16)

def uint24(data):
  return nulled(readbytes(data, 3),24)
  

def uint32(data):
  return nulled(readbytes(data, 4),32)

def int8(data):
  return readint(data, 8)

def int16(data):
  return readint(data, 16)

def int32(data):
  return readint(data, 32)

def int64(data):
  return readint(data, 64)

def uint64(data):
  return nulled(readbytes(data, 8),64)

def xint64(data):
  return readbytes(data, 8)


def mul(a,b):
  """
  Returns the result of multiplying a*b  as long as a is not None.
  Otherwise return None.
  """
  if a is not None:
    
    if a == 0:
      return 0.0
    
    elif a:
      return float(a) * b

def decimal(num, places):
  """
  Convert the given number to a float with specified 
  number of decimal places as long as num is not None.
  """

  return mul(num, 10**-places)

def hdegrees16(data):  
  return mul(uint16(data), .0057)

def udegrees16(data):  
  return mul(uint16(data), .0057)

def degrees16(data):  
  return mul(int16(data), .0057)

def degrees32(data):  
  return mul(int32(data), .00000179)

def init(dataset):
  dataset.add_function(
    'seasmart_timestamp',
    seasmart_timestamp,
    returns=dict(name='timestamp', type='DATETIME')
  )



  def last(state, val):
    return val

  dataset.add_aggregate(
    "last", 
    func=last,
    returns=Field(name="last", type="INTEGER"),
    initial=None
  )


  for hex, method, fields in PGNS:
    pgn = method.__name__
    dataset.create_view(
      pgn,
      """
      select * from 
      flatten(
        select timestamp, {pgn} from fb_events where {pgn} != null, 
        '{pgn}'
      )
      
      """.format(pgn=pgn)
    )
