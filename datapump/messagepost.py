import os
import sys
import re
import requests
from requests.exceptions import HTTPError
import json
import logging
import datetime
import time
import pytz
from time import mktime
from operator import itemgetter
from itertools import groupby
#from m2x.client import M2XClient
#from geopy.distance import vincenty
from array import *
from astral import *

# *******************************************************************
# Debug Output defines
# Comment to enable/disable
# ********************************************************************
#debug_all = False
debug_all = True


requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.INFO)

logging.basicConfig(level=logging.INFO)
log = logging


from influxdb.influxdb08 import InfluxDBClient

from influxdb import InfluxDBClient as InfluxDBCloud
from influxdb.client import InfluxDBClientError

import psycopg
from psycopg_pool import ConnectionPool
#db_pool = ThreadedConnectionPool( 1,  **connection_from(os.environ['DATABASE_URL']))
#db_pool = ConnectionPool( 1,  **connection_from(os.environ['DATABASE_URL']))
db_pool = ConnectionPool(os.environ.get('DATABASE_URL'))



# ****************************************************************
# converts database standard sensor units to specified units
# *************************************************************************
def convertunits(value, units):
  units = int(units)


  if not value:
    return "---"

  if value is None:
    return "---"

  if value == 'None':
    return "---"

  if units == 0: #//="0">Fahrenheit</option>
      return float("{0:.2f}".format((value * 1.8) - 459) )


  elif units ==  1: #//="1">Celsius</option>
      return float("{0:.2f}".format((value * 1.0) - 273) )


  elif units == 2: #//e="2">Kelvin</option>
      return value 


  #//  case 3: //="3">- - -</option> 


  elif units == 4: #//="4">Knots</option>
      return float("{0:.2f}".format(value * 1.94384449))


  elif units == 5: #//="5">MPH</option>
      return float("{0:.2f}".format(value * 2.23694) )


  elif units == 6: #//e="6">KPH</option>
      return float("{0:.2f}".format(value * 1.0) )



  #// case 7: //="7">- - -</option>
  elif units == 8: #//="8">PSI</option>
      return float("{0:.2f}".format(value * 0.145037738007) )



  elif units == 9: #//e="9">KPASCAL</option>
      return float("{0:.2f}".format(value * 1.0))



  elif units == 10: #//="10">INHG</option>
      return float("{0:.2f}".format(value * 0.295229) )


  #//  case 11: //="11">- - -</option>
  # //  case 12: //="12">TRUE</option>
  #//   case 13: //="13">MAGNETIC</option>
  #//   case 14: //="14">- - -</option>
  #//   case 15: //="15">- - -</option>
  elif units == 16:            #//   case 16: //="16">DEGREES</option>
    return float("{0:.6f}".format(value * 1.0 ) )
  
  elif units == 17:            #//   case 17: //="17">Radians</option>
    return float("{0:.6f}".format(value * 0.0174533 ) )
  
  
  elif units == 18: #//="18">Gallons/hs</option>
      return float("{0:.2f}".format(value * 0.264172052 ) )


  elif units == 19: #//="19">Liters/hr</option>
      return float("{0:.2f}".format(value * 1.0 ) )


  elif units == 20:# //="20">Liters</option>
       return float("{0:.2f}".format(value * 0.1 ) )
      
  elif units == 21:# //="21">Gallons</option>
      return float("{0:.2f}".format(value * 0.264172052 ) )
    
  #case 22: //="22">CubicMeter</option>
  #case 23: //="23">- - -</option>
  #case 24: //="24">RPM</option>
  #case 25: //="25">RPS</option>   
  #case 26: //="26">%</option>
  elif units == 27: #//="27">Volts</option>
      return float("{0:.2f}".format(value *1.00))


  elif units == 31: #//="31">kWhrs</option>
      return float("{0:.2f}".format(value *1.00))
  # case 28: //="28">Amps</option>
  
  elif units == 32: #//="32">Feet</option>
      return float("{0:.2f}".format(value * 3.28084)) 

  elif units == 33: #//="33">Meters</option>
      return float("{0:.2f}".format(value * 1.0))


  elif units == 44: #//= RAIN IN mm
       return float("{0:.2f}".format(value * 1000.0))  

  elif units == 45: #//=RAIN in inches
      return float("{0:.2f}".format(value * 39.3))
    

  elif units == 34: #//="34">Miles</option>
      return float("{0:.2f}".format(value * 0.000621371))              

  elif units == 35: #//="35">Nautical Mile</option>
      return float("{0:.2f}".format(value * 0.0005399568))                
  
  elif units == 36: #//="36">Fathoms</option>
      return float("{0:.2f}".format(value * 0.546806649))


  elif units == 37: #//="37">Time</option>
      #log.info('HeartBeat time %s:', datetime.datetime.fromtimestamp(int(value)).strftime('%H:%M:%S'))
      return (datetime.datetime.fromtimestamp(int(value)).strftime('%H:%M:%S'))

  elif units == 38: #//="38">Date/time</option>
      #log.info('HeartBeat time %s:', datetime.datetime.fromtimestamp(int(value)).strftime('%m/%d/%Y %H:%M:%S'))
      return (datetime.datetime.fromtimestamp(int(value)).strftime('%m/%d/%Y %H:%M:%S'))
    
  elif units == 39: #//="39">Hours</option>
    #Engine Hours (value / (60*60))
    return float("{0:.2f}".format(value * 0.000277777))

  elif units == 43: #//="43">Volts 10</option>
    return float("{0:.2f}".format(value * 0.1))

  else:
      return float("{0:.2f}".format(value * 1.0))

    
# ****************************************************************
# Gets the start and end times based on the interval
# *************************************************************************
def getepochtimes(Interval):



    log.info('messagepost:  getepochtimes Interval %s:  ', Interval)

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
        log.info('messagepost: TypeError in geting getepochtimes parameters %s:  ', Interval)
        log.info('messagepost: TypeError in geting getepochtimes parameters %s:  ' % str(e))
            
    except KeyError as e:
        log.info('messagepost: KeyError in geting getepochtimes parameters %s:  ', Interval)
        log.info('messagepost: KeyError in geting getepochtimes parameters %s:  ' % str(e))

    except NameError as e:
        log.info('messagepost: NameError in geting getepochtimes parameters %s:  ', Interval)
        log.info('messagepost: NameError in geting getepochtimes parameters %s:  ' % str(e))
            
    except IndexError as e:
        log.info('messagepost: IndexError in geting getepochtimes parameters %s:  ', Interval)
        log.info('messagepost: IndexError in geting getepochtimes parameters %s:  ' % str(e))  


    except:
        log.info('messagepost: Error in geting  getepochtimes %s:  ', Interval)
        e = sys.exc_info()[0]
        log.info('messagepost: Error in geting getepochtimes parameters %s:  ' % str(e))

    return(epochtimes)

# ****************************************************************
# InfluxDB Sensor key
# takes alert message sensor key and returns the sensor values
# *************************************************************************
def getSensorParameter(sensorKey):

        seriesname = sensorKey
        seriestags = seriesname.split(".")

        seriesparametertag = seriestags[5]
        seriesparameter = seriesparametertag.split(":")    
        parameter = seriesparameter[1]

        return parameter

# ****************************************************************
# InfluxDB Sensor key
# takes alert message sensor key and returns the sensor values
# *************************************************************************
def createInfluxDBCloudKeys(sensorKey):

    # example key 'key': 'deviceid:68271933E95E.sensor:seasmartdimmer.source:.*.instance:0.type:LED 1 Channel.parameter:value0.HelmSmart'

    if sensorKey.find(".*.") > 0:  
        sensorKey = sensorKey.replace(".*.","*.")
        #SERIES_KEY.replace("*.","??")
        #SERIES_KEY.replace(".",".")
        #if debug_all: log.info('convertInfluxDBCloudKeys: Error in convertInfluxDBCloudKeys %s:  ', SERIES_KEY)
                
    try:
        #if debug_all: log.info('convertInfluxDBCloudKeys: SERIES_KEY %s:  ', SERIES_KEY)
        seriesname = sensorKey
        seriestags = seriesname.split(".")

        #if debug_all: log.info('convertInfluxDBCloudKeys: seriestags %s:  ', seriestags)

        seriesdeviceidtag = seriestags[0]
        seriesdeviceid = seriesdeviceidtag.split(":")

        seriessensortag = seriestags[1]
        seriessensor = seriessensortag.split(":")

        seriessourcetag = seriestags[2]
        seriessource = seriessourcetag.split(":")

        seriesinstancetag = seriestags[3]
        seriesinstance = seriesinstancetag.split(":")

        seriestypetag = seriestags[4]
        seriestype = seriestypetag.split(":")

        seriesparametertag = seriestags[5]
        seriesparameter = seriesparametertag.split(":")    
        parameter = seriesparameter[1]

        
        if parameter == 'latlng':
            serieskeys="( deviceid='"
            serieskeys= serieskeys + seriesdeviceid[1] 
            serieskeys= serieskeys +  "' AND sensor='" +  seriessensor[1]
            if seriessource[1] != "*":
                serieskeys= serieskeys +  "' AND source='" +  seriessource[1] 
            serieskeys= serieskeys +  "' AND instance='" +  seriesinstance[1] 
            serieskeys= serieskeys +  "' AND type='" +  seriestype[1] 
            serieskeys= serieskeys +  "' AND parameter='lat') OR " 

            serieskeys=serieskeys + "( deviceid='"
            serieskeys= serieskeys + seriesdeviceid[1] 
            serieskeys= serieskeys +  "' AND sensor='" +  seriessensor[1]
            if seriessource[1] != "*":
                serieskeys= serieskeys +  "' AND source='" +  seriessource[1] 
            serieskeys= serieskeys +  "' AND instance='" +  seriesinstance[1] 
            serieskeys= serieskeys +  "' AND type='" +  seriestype[1] 
            serieskeys= serieskeys +  "' AND parameter='lng') "  

                
        else:
            serieskeys="( deviceid='"
            serieskeys= serieskeys + seriesdeviceid[1] 
            serieskeys= serieskeys +  "' AND sensor='" +  seriessensor[1]
            if seriessource[1] != "*":
                serieskeys= serieskeys +  "' AND source='" +  seriessource[1] 
            serieskeys= serieskeys +  "' AND instance='" +  seriesinstance[1] 
            serieskeys= serieskeys +  "' AND type='" +  seriestype[1] 
            serieskeys= serieskeys +  "' AND parameter='" +  seriesparameter[1] + "'   )"


        return serieskeys


    except TypeError as e:
        if debug_all: log.info('createInfluxDBCloudKeys: TypeError in convertInfluxDBCloudKeys %s:  ', sensorKey)
        #e = sys.exc_info()[0]

        if debug_all: log.info('createInfluxDBCloudKeys: TypeError in convertInfluxDBCloudKeys %s:  ' % str(e))
        
    except KeyError as e:
        if debug_all: log.info('createInfluxDBCloudKeys: KeyError in convertInfluxDBCloudKeys %s:  ', sensorKey)
        #e = sys.exc_info()[0]

        if debug_all: log.info('createInfluxDBCloudKeys: KeyError in convertInfluxDBCloudKeys %s:  ' % str(e))

    except NameError as e:
        if debug_all: log.info('createInfluxDBCloudKeys: NameError in convertInfluxDBCloudKeys %s:  ', sensorKey)
        #e = sys.exc_info()[0]

        if debug_all: log.info('createInfluxDBCloudKeys: NameError in convertInfluxDBCloudKeys %s:  ' % str(e))

    except IndexError as e:
        if debug_all: log.info('createInfluxDBCloudKeys: IndexError in convertInfluxDBCloudKeys %s:  ', sensorKey)
        #e = sys.exc_info()[0]

        if debug_all: log.info('createInfluxDBCloudKeys: IndexError in convertInfluxDBCloudKeys %s:  ' % str(e))          

    except:
        if debug_all: log.info('createInfluxDBCloudKeys: Error in convertInfluxDBCloudKeys %s:  ', sensorKey)
        e = sys.exc_info()[0]
        if debug_all: log.info("createInfluxDBCloudKeys: Error: %s" % e)




# ****************************************************************
# InfluxDB Sensor query
# takes alert message sensor key and returns the sensor values
# *************************************************************************
def getSensorValues(alertParameters):

    dchost = 'hilldale-670d9ee3.influxcloud.net' 
    dcport = 8086
    dcusername = 'helmsmart'
    dcpassword = 'Salm0n16'
    dcdatabase = 'pushsmart-cloud'

    sensorSeries = alertParameters.get('series_1',"")

    if sensorSeries == "":
        return None

    
    sensorKey = sensorSeries['key']
    sensorUnits = sensorSeries['units']
    sensorInterval = alertParameters['Interval']

    if debug_all: log.info('getSensorValues: sensor key %s: interval %s: units%s', sensorKey,sensorInterval , sensorUnits)


    try:


        #example queryQuery
        #select  median(temperature) AS temperature
        #from HS_68271935AFB5
        #where  deviceid='68271935AFB5'
        #AND  sensor='environmental_data'
        #AND instance='0'
        #AND (type='Outside Temperature' OR type='Outside Humidity')
        #AND time > 1698425630s and time < 1698426230s group by time(120s) 

        # get device to get sensor values from
        measurement = 'HS_' + str(alertParameters['deviceid'])

        #calculate start and end time from interval
        epochtimes = getepochtimes(sensorInterval)
    
        startepoch = epochtimes[0]
        endepoch = epochtimes[1]
        if resolution == "":
            resolution = epochtimes[2]

        # get sensor from key
        idbcseriesparameters = getSensorParameter(alertParameters['key'])

        # get select from key
        idbcserieskeys = createInfluxDBCloudKeys(alertParameters['key'])

        # setup query
        #dbc = InfluxDBCloud(dchost, dcport, dcusername, dcpassword, dcdatabase,  ssl=True)


        dbcquery = ('select {} FROM {} '
                         'where {} AND time > {}s and time < {}s '
                         'group by *, time({}s)') \
                    .format( idbcseriesparameters,  measurement, idbcserieskeys,
                            startepoch, endepoch,
                            resolution)
            
        log.info('getSensorValues: Influx Cloud Query String %s:  ', dbcquery)


    except KeyError as e:
        if debug_all: log.info('getSensorValues: KeyError in EmailAlertPost-Cloud %s:  ' % str(e))

    except ValueError as e:
        if debug_all: log.info('getSensorValues: ValueError in EmailAlertPost-Cloud %s:  ' % str(e))

    except TypeError as e:
        if debug_all: log.info('getSensorValues: TypeError in EmailAlertPost-Cloud %s:  ' % str(e))

    except NameError as e:
        if debug_all: log.info('getSensorValues: NameError in EmailAlertPost-Cloud %s:  ' % str(e))
    
    except UnboundLocalError as e:
        if debug_all: log.info('getSensorValues: UnboundLocalError in EmailAlertPost-Cloud %s:  ' % str(e))

    except:
        e = sys.exc_info()[0]
        if debug_all: log.info("getSensorValues: Error: %s" % e)


# ****************************************************************
# Main message processor
# takes alert message parameters and does a InfluxDB lookup to get sensor values
# then preforms alert analytics to determine event
# *************************************************************************
def process_message(alert_message):

    parameters = alert_message['parameters']
    alertkey = alert_message['key']
    starttime = alert_message['starttime']

    posttype = parameters['posttype']
    alerttype=parameters.get('alerttype', "mean")

    if debug_all: log.info('Posting to Web Services %s:%s', posttype, starttime)
    #mymessage='returning from Telemetry post'  
    #return mymessage

    #conn = db_pool.getconn()

    #if debug_all: log.info('Device ID  = ' + records[0][0])
    #deviceid = records[0][0]

    API_KEY = '7be1d82569414dceaa82fd93fadd7940'
    API_SECRET = '0447ec319c3148cb98d96bfc96c787e1'
  
    points={}
    times={}
    timesiso={}

    posttypecloud=None


    if posttype == "EmailAlertPost":
        posttypecloud = "EmailAlertPost-Cloud"


    # get sensor values from influxdb
    sensorValues = getSensorValues(parameters)
    if sensorValues == None:
        mymessage='no Sensor Values'
        return mymessage

    if debug_all: log.info('process_message: sensor values %s:%s', sensorValues)

    
# **************************************************************************************
# If Email alert then check values for High/Low alarms and send out email if active
#****************************************************************************************
    try:

        if posttypecloud == "EmailAlertPost-Cloud":
            #if debug_all: log.info('Posting to AlertPosts :')
            log.info('Posting to EmailAlertPost-Cloud %s:', parameters)

            email_body = ""
            timmer_array = ""
            timmer_json={}
            distance = ""

            
    except KeyError as e:
        #if debug_all: log.info('process_message: KeyError in EmailAlertPost-Cloud %s:  ', SERIES_KEY1)

        if debug_all: log.info('process_message: KeyError in EmailAlertPost-Cloud %s:  ' % str(e))
        mymessage='KeyError in EmailAlertPost-Cloud'
        return mymessage

    except ValueError as e:
        #if debug_all: log.info('process_message: Value Error in EmailAlertPost-Cloud %s:  ', SERIES_KEY1)

        if debug_all: log.info('process_message: ValueError in EmailAlertPost-Cloud %s:  ' % str(e))
        mymessage='ValueError in EmailAlertPost-Cloud'
        return mymessage

    except TypeError as e:
        #if debug_all: log.info('process_message: TypeError in EmailAlertPost-Cloud %s:  ', SERIES_KEY1)

        if debug_all: log.info('process_message: TypeError in EmailAlertPost-Cloud %s:  ' % str(e))
        mymessage='TypeError in EmailAlertPost-Cloud'
        return mymessage
    
    except NameError as e:
        #if debug_all: log.info('process_message: TypeError in EmailAlertPost-Cloud %s:  ', SERIES_KEY1)

        if debug_all: log.info('process_message: NameError in EmailAlertPost-Cloud %s:  ' % str(e))
        mymessage='NameError in EmailAlertPost-Cloud'
        return mymessage
    
    except UnboundLocalError as e:
        #if debug_all: log.info('process_message: UnboundLocalError in EmailAlertPost-Cloud %s:  ', SERIES_KEY1)

        if debug_all: log.info('process_message: UnboundLocalError in EmailAlertPost-Cloud %s:  ' % str(e))
        mymessage='UnboundLocalError in EmailAlertPost-Cloud'
        return mymessage

    except:
        #if debug_all: log.info('process_message: Error in geting EmailAlertPost-Cloud parameters %s:  ', posttype)
        e = sys.exc_info()[0]

        if debug_all: log.info("Error: %s" % e)
        mymessage='Error in geting Alert Parameters'
        return mymessage
        #pass
    
# ****************************************************************
# end of Main message processor
# *************************************************************************
