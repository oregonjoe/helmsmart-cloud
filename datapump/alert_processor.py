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
from astral import LocationInfo
from astral.geocoder import lookup, database

# *******************************************************************
# Debug Output defines
# Comment to enable/disable
# ********************************************************************
#debug_all = False
debug_all = True


logging.basicConfig(level=logging.INFO)
log = logging

def get_timmer_alert(parameters, value):

    #initialize return
    result={}
    result['status']="error"
    result['message']=""

    text_body= "error in timmer alert"
    alerttype = parameters.get('alerttype',"mean")

    log.info("get_timmer_alert  deviceID: %s", parameters['deviceid'])


    # extract the series alarm paramterts
    series_parameters = parameters.get('series_1',"")
    # check for errors
    if series_parameters == "":
        result['status']="error"
        result['message']="missing series parameters"
        return result    

    try:
        
        if str(parameters[series_number]["alarmlow"]) != "off" :
                      
            try:
                locationcity= parameters["locationcity"]

            except:
                locationcity= 'Seattle'

                    
            log.info('get_timmer_alert: get timmer once location->%s  ', locationcity)
            #a = Astral()
            if locationcity == 'Brookings':
                    
                location  = lookup("Seattle", database())
                #location.name = 'Brookings'    

            else:
                #location  = lookup("Seattle", database())
                try:
                    location  = lookup(locationcity, database())
                except:
                    location  = lookup("Seattle", database())
            
            log.info("get_timmer_alert: process_emailalert timmer once  Astral location: %s", location)

            timezone = location.timezone

            log.info('get_timmer_alert: process_emailalert timmer once  timezone ->%s ',   timezone)

            #get timezone for current sunset/sunrise location
            mylocal = pytz.timezone(timezone)

            currenttime = datetime.datetime.now()
            log.info('get_timmer_alert: process_emailalert timmer once alert %s  ', currenttime)
    
            #need to make time value timezone aware
            utccurrenttime = pytz.utc.localize(currenttime)
            log.info('get_timmer_alert: process_emailalert timmer once utccurrenttime secs %s  ', utccurrenttime)  
            
            # adjust time to sunset/sunrise local time
            localcurrenttime = utccurrenttime.astimezone(mylocal)
            

            #currenttime = datetime.datetime.now()
            currenttime = localcurrenttime
            #currentsecounds = (mytime.hour * 60 * 60) + (mytime.minute * 60)  + mytime.second
            log.info('get_timmer_alert: process_emailalert timmer once localcurrenttime %s  ', currenttime)


            #now remove timezone info so we can compare to start and end times
            currenttime = currenttime.replace(tzinfo=None)
            #currentsecounds = (mytime.hour * 60 * 60) + (mytime.minute * 60)  + mytime.second
            log.info('get_timmer_alert: process_emailalert timmer once currenttime without timezone info %s  ', currenttime)
            
            starttime = datetime.datetime.fromtimestamp(int(series_parameters["alarmlow"]))
            log.info('get_timmer_alert: process_emailalert timmer once starttime %s  : %s  ', str(series_parameters["alarmlow"]), starttime)

            #need to make time value timezone aware
            endtime = datetime.datetime.fromtimestamp(int(series_parameters["alarmhigh"]))
            log.info('get_timmer_alert: process_emailalert timmer once endtime %s : %s  ', str(series_parameters["alarmhigh"]), endtime)

            log.info('get_timmer_alert: process_emailalert timmer once times %s:  %s:   %s  ', currenttime, starttime, endtime)                

            try:

                if currenttime >=  starttime and currenttime <=  endtime:
                    text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                    text_body = text_body  + series_parameters["alarmmode"] + ": " + parameters[series_number]["title"] + '\n'
                    text_body = text_body + 'is low - ' + alerttype + ' = ' + str(currenttime) + " threshold: " + str(series_parameters["alarmlow"]) + " timestamp is:" + timestamp + '\n'
                    result['status']="active"
                    log.info('get_timmer_alert: process_emailalert timmer alerttext %s:%s  ', text_body, currenttime)
                    
                else:
                    result['status']="inactive"

            except TypeError as e:
                if debug_all: log.info('get_timmer_alert: TypeError in timmer once compare %s  ', text_body)
                if debug_all: log.info('get_timmer_alert: TypeError in timmer once compare %s:  ' % str(e))  

            except:
                log.info('get_timmer_alert: Error1.1 in get timmer once compare %s  ', text_body)
                e = sys.exc_info()[0]
                log.info("Error1.1: %s" % e)
                result['status']="error 1.1"


        result['message']=text_body              
        return result

    except ValueError as e:
        if debug_all: log.info('get_timmer_alert: ValueError in timmer once %s  ', text_body)
        if debug_all: log.info('get_timmer_alert: ValueError in timmer once %s:  ' % str(e))

    except NameError, e:
        if debug_all: log.info('get_timmer_alert: NameError in timmer once %s  ', text_body)
        if debug_all: log.info('get_timmer_alert: NameError in timmer once %s:  ' % str(e))

    except AttributeError, e:
        if debug_all: log.info('get_timmer_alert: AttributeError in timmer once %s  ', text_body)
        if debug_all: log.info('get_timmer_alert: AttributeError in timmer once %s:  ' % str(e))

    except TypeError, e:
        if debug_all: log.info('get_timmer_alert: TypeError in timmer once %s  ', text_body)
        if debug_all: log.info('get_timmer_alert: TypeError in timmer once %s:  ' % str(e))                     
        
    except:
        log.info('get_timmer_alert: Error1 in get timmer once %s  ', text_body)
        e = sys.exc_info()[0]
        log.info("Error1: %s" % e)
        result['status']="error 1"

        return result


    

 

def get_timmerday_alert(parameters, value):

    #initialize return
    result={}
    result['status']="error"
    result['message']=""
    timmerArray = []

    text_body= "error in timmerday alert"
    alerttype = parameters.get('alerttype',"mean")

    # extract the series alarm paramterts
    series_parameters = parameters.get('series_1',"")
    # check for errors
    if series_parameters == "":
        result['status']="error"
        result['message']="missing series parameters"
        return result

    log.info("get_timmerday_alert  deviceID: %s", parameters['deviceid'])

    try:
        
        if str(series_parameters["alarmlow"]) != "off" :

            try:
                locationcity= parameters["locationcity"]

            except:
                locationcity= 'Seattle'

                    
            log.info('get_timmerday_alert location->%s  ', locationcity)

    
            #a = Astral()
            if locationcity == 'Brookings':
                    
                #location = a['Seattle']
                #location = LocationInfo("Seattle")
                location  = lookup("Seattle", database())
                #location.name = 'Brookings'    

            else:
                #location  = lookup("Seattle", database())
                try:
                    location  = lookup(locationcity, database())
                except:
                    location  = lookup("Seattle", database())

            log.info("get_timmerday_alert  Astral location: %s", location)

            timezone = location.timezone

            log.info('get_timmerday_alert: process_emailalert timmer day  timezone ->%s ',   timezone)

            #get timezone for current sunset/sunrise location
            mylocal = pytz.timezone(timezone)
            #get current local time for sunset/sunrise location
            #currenttime = datetime.datetime.now(mylocal)


            currenttime = datetime.datetime.now()
            log.info('get_timmerday_alert timmerday alert %s  ', currenttime)

            #need to make time value timezone aeare
            utccurrenttime = pytz.utc.localize(currenttime)
            log.info('get_timmerday_alert utcstarttime  %s  -', utccurrenttime)  
            
            # adjust time to sunset/sunrise local time
            localcurrenttime = utccurrenttime.astimezone(mylocal)
            log.info('get_timmerday_alert localcurrenttime  %s  -', localcurrenttime)
            #localcurrenttime.tm_isdst=0
            #localendtime = endtime
            log.info('get_timmerday_alert localcurrenttime.timetuple() %s  -', localcurrenttime.timetuple())

            #bad python 3 hack here...
            #seems as if is_dst (daylight savings time) is =1 for our localcurrenttime the following time.mktime function throws a overflow error for no reason
            #so we got to cleat the isdst vale in the time tupple before we call time.mktime
            lctt = localcurrenttime.timetuple()
            log.info('get_timmerday_alert localcurrenttime.timetuple() %s  -', lctt)
            t=(lctt.tm_year, lctt.tm_mon, lctt.tm_mday, lctt.tm_hour, lctt.tm_min, lctt.tm_sec, lctt.tm_wday, lctt.tm_yday, 0)  
            # get seconds so we can convert to 24 hour clock 
            currentsecs = time.mktime(t)         
            #currentsecs = time.mktime(localcurrenttime.timetuple())
            log.info('get_timmerday_alert currentsecs %s  -', currentsecs)  

            log.info('get_timmerday_alert localcurrenttime %s  -> %s', localcurrenttime, currentsecs)

            startsecs = int(series_parameters["alarmlow"])
            starttime = datetime.datetime.fromtimestamp(int(series_parameters["alarmlow"]))  
            log.info('get_timmerday_alert starttime secs %s  -> %s', starttime, startsecs)
            
            #need to make time value timezone aeare
            utcstarttime = pytz.utc.localize(starttime)
            log.info('get_timmerday_alert utcstarttime secs %s  -> %s', utcstarttime, startsecs)  

            # adjust time to sunset/sunrise local time
            #localstarttime = utcstarttime.astimezone(mylocal)
            #bad python 3 hack here...
            #seems as if is_dst (daylight savings time) is =1 for our localcurrenttime the following time.mktime function throws a overflow error for no reason
            #so we got to cleat the isdst vale in the time tupple before we call time.mktime
            localstarttime = utcstarttime
            lctt = localstarttime.timetuple()
            log.info('get_timmerday_alert localstarttime.timetuple() %s  -', lctt)
            t=(lctt.tm_year, lctt.tm_mon, lctt.tm_mday, lctt.tm_hour, lctt.tm_min, lctt.tm_sec, lctt.tm_wday, lctt.tm_yday, 0)
            #log.info('get_timmerday_alert localstarttime  %s ',localstarttime)
            
            # get seconds so we can convert to 24 hour clock
            #startsecs = time.mktime(localstarttime.timetuple())
            startsecs = time.mktime(t)
            log.info('get_timmerday_alert startsecs  %s ',startsecs)
                       
            startutcsecs_local  = mylocal.localize(starttime, is_dst=None) # No daylight saving time
            log.info('get_timmerday_alert utcstarttime local time %s ',startutcsecs_local)
            startutcsecs_utc = startutcsecs_local.astimezone(pytz.utc)
            log.info('get_timmerday_alert utcstarttime utc time %s ',startutcsecs_utc)                   
            startutcsecs = time.mktime(startutcsecs_utc.timetuple())
            log.info('get_timmerday_alert startutcsecs %s  -> %s', startutcsecs, int(startutcsecs % (24*60*60)))

            
            #sunset_utc = sunset.astimezone(pytz.utc)
            log.info('get_timmerday_alert starttime %s  : %s  ', str(series_parameters["alarmlow"]), localstarttime)
            log.info('get_timmerday_alert start secs %s  -> %s', startsecs, int(startsecs % (24*60*60)))
            

            endsecs = int(series_parameters["alarmhigh"])
            endtime = datetime.datetime.fromtimestamp(int(series_parameters["alarmhigh"]))
            log.info('get_timmerday_alert endtime secs %s  -> %s', endtime, endsecs)
                                
            #need to make time value timezone aeare
            utcendtime = pytz.utc.localize(endtime)
            log.info('get_timmerday_alert utcendtime secs %s  -> %s', utcendtime, endsecs)  

            # adjust time to sunset/sunrise local time
            #localendtime = utcendtime.astimezone(mylocal)
            localendtime = utcendtime

            lctt = localendtime.timetuple()
            log.info('get_timmerday_alert localendtime.timetuple() %s  -', lctt)
            t=(lctt.tm_year, lctt.tm_mon, lctt.tm_mday, lctt.tm_hour, lctt.tm_min, lctt.tm_sec, lctt.tm_wday, lctt.tm_yday, 0)
            # get seconds so we can convert to 24 hour clock
            #endsecs = time.mktime(localendtime.timetuple())
            endsecs = time.mktime(t)
            log.info('get_timmerday_alert endsecs %s ', endsecs)

            endutcsecs_local  = mylocal.localize(endtime, is_dst=None) # No daylight saving time
            log.info('get_timmerday_alert utcendtime local time %s ',endutcsecs_local)
            endutcsecs_utc = endutcsecs_local.astimezone(pytz.utc)
            log.info('get_timmerday_alert utcendtime utc time %s ',endutcsecs_utc)

            
            endutcsecs = time.mktime(endutcsecs_utc.timetuple())
            log.info('get_timmerday_alert endutcsecs %s  -> %s', endutcsecs, int(endutcsecs % (24*60*60)))

            
            log.info('get_timmerday_alert endtime %s : %s  ', str(series_parameters["alarmhigh"]), localendtime)
            log.info('get_timmerday_alert end secs %s  -> %s', endsecs, int(endsecs % (24*60*60)))


            log.info('get_timmerday_alert times %s:  %s:   %s  ', localcurrenttime, localstarttime, localendtime)

            #modulo start and end epoch times by 24 hours since we repeat daily
            #log.info('Telemetrypost: process_emailalert timmerday modulo secs times %s:  %s:   %s  ', int(currentsecs % (24*60*60))     , int(startsecs % (24*60*60)),  int(endsecs % (24*60*60)))  
            #before we do that....
            # be shure the epoch srart time is less then the end time or else things will get messed up
            # start time must always be less then end time for this check.
            """                    
            if startsecs > endsecs:
                tempsecs = endsecs
                endsecs = startsecs
                startsecs = tempsecs
            """       
            currentsecs = int(currentsecs % (24*60*60))     
            startsecs = int(startsecs % (24*60*60))
            endsecs = int(endsecs % (24*60*60))

            startutcsecs = int(startutcsecs % (24*60*60))
            endutcsecs = int(endutcsecs % (24*60*60))

            
            log.info('get_timmerday_alert modulo secs times %s:  %s:   %s  ', currentsecs, startsecs, endsecs)          
            # need to handle case when end time goes into the next day
            # which will mean the end time is less then start time when we modulo by 24 hours
            # if that happens we need to offset all epoch times so the endtime is at 23:54:54
            # which will force all times back into the same 24 hour period
            """                           
            secoffset = 0
            if endsecs < startsecs:
                secoffset = endsecs
                endsecs = (24*60*60)-1
                startsecs = startsecs - secoffset
            """       
            #log.info('Telemetrypost: process_emailalert timmerday compare secs times %s:  %s:   %s  ', currentsecs, startsecs, endsecs)                    
            #log.info('Telemetrypost: process_emailalert timmerday offset  %s current secs  %s:   ', secoffset, (currentsecs - secoffset))

            log.info('get_timmerday_alert Initialize Timmer array')
                                
            alertdefault_value = int(parameters.get('alertdefault_value',255))

            for t_hours in range(0, 144):
                #timmerArray.append(255)
                timmerArray.append(alertdefault_value)


            alertaction_value = int(parameters.get('alertaction_value',255))
            log.info('get_timmerday_alert compare timmerday start < end  alertaction_value %s  ', alertaction_value)
                
                
            # if start secs < endsec then both within saem 24 hours so its a simple compare                       
            if   startutcsecs <  endutcsecs:
                for t_tenmin in range(0, 6*24):
                    
                    if t_tenmin > startutcsecs/(10*60) and t_tenmin < endutcsecs/(10*60) :
                        timmerArray[t_tenmin] =alertaction_value

                log.info('get_timmerday_alert compare timmerday start < end  timmerArray %s  ', timmerArray)  

            # if strart secs > end sec then we span different 24 hours over midnight so we need to compare before midnight and after        
            elif   startutcsecs >  endutcsecs:                        
                for t_tenmin in range(0, 6*24):
                    
                    if t_tenmin > startutcsecs/(10*60) or t_tenmin < endutcsecs/(10*60) :
                        timmerArray[t_tenmin] =alertaction_value

                log.info('get_timmerday_alert compare timmerday start > end  timmerArray %s  ', timmerArray)
                
            # if start secs < endsec then both within saem 24 hours so its a simple compare
            if   startsecs <  endsecs:
                log.info('get_timmerday_alert: process_emailalert timmerday start < end  ', )                           
                try:

                    alertaction_value = int(parameters.get('alertaction_value',255))
                    log.info('get_timmerday_alert compare timmerday start < end  alertaction_value %s  ', alertaction_value)
                    


                    
                    if currentsecs >=  startsecs and currentsecs <=  endsecs:
                        text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                        text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                        text_body = text_body + 'is low - ' + alerttype + ' = ' + str(currenttime) + " threshold: " + str(series_parameters["alarmlow"]) + " timestamp is:" + timestamp + '\n'
                        result['status']="active"
                        log.info('get_timmerday_alert: process_emailalert timmerday active alerttext %s:%s  ', text_body, currenttime)
                        
                    else:
                        result['status']="inactive"
                        text_body = "alert is inactive - current time is outside start/end"
                        log.info('get_timmerday_alert timmerday inactive alerttext %s:%s  ', text_body, currenttime)
                        
                except:
                    if debug_all: log.info('get_timmerday_alert: Error in process_emailalert %s:%s  ', text_body, value)
                    e = sys.exc_info()[0]
                    if debug_all: log.info("Error: %s" % e)
                    result['status']="error"

            # if strart secs > end sec then we span different 24 hours over midnight so we need to compare before midnight and after        
            elif   startsecs >  endsecs:
                log.info('get_timmerday_alert timmerday start > end  ', )                           
                try:
                    
                    alertaction_value = int(parameters.get('alertaction_value',255))
                    log.info('get_timmerday_alert compare timmerday start > end  alertaction_value %s  ', alertaction_value)
                    

                    
                    #if currenttime >=  starttime and currenttime <=  midnight:
                    if  currentsecs  >=  startsecs and currentsecs  <=  (24*60*60):
                        text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                        text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                        text_body = text_body + 'is low - ' + alerttype + ' = ' + str(currenttime) + " threshold: " + str(series_parameters["alarmlow"]) + " timestamp is:" + timestamp + '\n'
                        result['status']="active"
                        log.info('get_timmerday_alert timmerday active alerttext %s:%s  ', text_body, currenttime)
                        
                    #if currenttime >=  newday and currenttime <=  endtime:
                    elif currentsecs  >=  0 and currentsecs  <=  endsecs:
                        text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                        text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                        text_body = text_body + 'is low - ' + alerttype + ' = ' + str(currenttime) + " threshold: " + str(series_parameters["alarmlow"]) + " timestamp is:" + timestamp + '\n'
                        result['status']="active"
                        log.info('get_timmerday_alert timmerday active alerttext %s:%s  ', text_body, currenttime)
                        
                    else:
                        result['status']="inactive"
                        text_body = "alert is inactive - current time is outside start/end"
                        log.info('get_timmerday_alert timmerday inactive alerttext %s:%s  ', text_body, currenttime)
                        
                except:
                    if debug_all: log.info('get_timmerday_alert: Error in process_emailalert %s:%s  ', text_body, value)
                    e = sys.exc_info()[0]
                    if debug_all: log.info("Error: %s" % e)
                    result['status']="error"

            #start time equals end time so do nothing        
            else:
                result['status']="inactive"
                text_body = "alert is inactive - current time is equal to start/end"
                log.info('get_timmerday_alert timmerday inactive alerttext %s:%s  ', text_body, currenttime)

        result['message']=text_body
        result['timmerArray']=timmerArray
        return result

    except TypeError as e:
        if debug_all: log.info('get_timmerday_alert: TypeError in process_emailaler %s:%s  ', text_body, value)
        if debug_all: log.info('get_timmerday_alert: TypeError in process_emailaler %s:  ' % str(e))

    except ValueError as e:
        if debug_all: log.info('get_timmerday_alert: ValueError in process_emailaler %s:%s  ', text_body, value)
        if debug_all: log.info('get_timmerday_alert: TypeError in process_emailaler %s:  ' % str(e))

    except AttributeError as e:
        if debug_all: log.info('get_timmerday_alert: AttributeError in process_emailaler %s:%s  ', text_body, value)
        if debug_all: log.info('get_timmerday_alert: AttributeError in process_emailaler %s:  ' % str(e))        
        
    except KeyError as e:
        if debug_all: log.info('get_timmerday_alert: KeyError in process_emailaler %s:%s  ', text_body, value)
        if debug_all: log.info('get_timmerday_alert: KeyError in process_emailaler %s:  ' % str(e))

    except NameError as e:
        if debug_all: log.info('get_timmerday_alert: NameError in process_emailaler %s:%s  ', text_body, value)
        if debug_all: log.info('get_timmerday_alert: NameError in process_emailaler %s:  ' % str(e))

    except OverflowError as e:
        if debug_all: log.info('get_timmerday_alert: OverflowError in process_emailaler %s:%s  ', text_body, value)
        if debug_all: log.info('get_timmerday_alert: OverflowError in process_emailaler %s:  ' % str(e))         

    except:
        if debug_all: log.info('get_timmerday_alert: Error in process_emailalert %s:%s  ', text_body, value)
        e = sys.exc_info()[0]

        if debug_all: log.info("Error: %s" % e)
        mymessage='Error in geting get_timmerday_alert'
        return result


  
def get_sunriseset_alert(parameters, value):

    #initialize return
    result={}
    result['status']="error"
    result['message']=""

    text_body= "error in timmer alert"
    alerttype = parameters.get('alerttype',"mean")

    log.info("get_sunriseset_alert  deviceID: %s", parameters['deviceid'])

    return result

def get_status_alert(parameters, value):

    #initialize return
    result={}
    result['status']="error"
    result['message']=""

    text_body= "error in get status alert"
    alerttype = parameters.get('alerttype',"mean")

    log.info("get_status_alert  deviceID: %s", parameters['deviceid'])

    # extract the series alarm paramterts
    series_parameters = parameters.get('series_1',"")
    # check for errors
    if series_parameters == "":
        result['status']="error"
        result['message']="missing series parameters"
        return result

    text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
    text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
    text_body = text_body + 'is = ' + str(value) + " threshold: " + str(series_parameters["alarmlow"]) + "/" + str(series_parameters["alarmhigh"])+ " timestamp is:" + timestamp + '\n'
    result['status']="status"
    result['message']=text_body
    return result


def get_alarms_alert(parameters, value):

    #initialize return
    #result['status']="error"
    result={}
    result['status']="inactive"
    result['message']=""

    text_body= "error in get_alarms alert"
    alerttype = parameters.get('alerttype',"mean")

    log.info("get_alarms_alert  deviceID: %s", parameters['deviceid'])

    # extract the series alarm paramterts
    series_parameters = parameters.get('series_1',"")
    # check for errors
    if series_parameters == "":
        result['status']="error"
        result['message']="missing series parameters"
        return result
    
    if alerttype == "missing":
        if value == "missing":
            text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
            text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
            text_body = text_body + "value is missing for Interval= " + parameters["Interval"] + " timestamp is:" + timestamp + '\n'
            result['status']="active"
            result['message']=text_body
        return result
            
    if alerttype == "error":
        if value == "error":
            text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
            text_body = text_body  + series_parameters["alarmmode"] + ": " +series_parameters["title"] + '\n'
            text_body = text_body + "value error for Interval= " + parameters["Interval"] + " timestamp is:" + timestamp + '\n'
            result['status']="active"
            result['message']=text_body
        return result
            
    if str(series_parameters["alarmlow"]) != "off" :
        try:
            if float(value) <= float(series_parameters["alarmlow"]):
                text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                text_body = text_body + 'is low - ' + alerttype + ' = ' + str(value) + " threshold: " + str(series_parameters["alarmlow"]) + " timestamp is:" + timestamp + '\n'
                result['status']="active"
                #http://www.helmsmart.net/getseriesdatabykey?serieskey=deviceid:0018E78B5121.sensor:engine_parameters_dynamic.source:08.instance:1.type:NULL.parameter:engine_temp.HelmSmart&devicekey=2a4731ac48c80ee3b4c17e7d74a6825f&startepoch=1405065555&endepoch=1405094365&resolution=60&format=csv
        except:
            result['status']="inactive"
    
    
    if str(series_parameters["alarmhigh"]) != "off" :
        #if value != "" or value != "missing" or value != "error":
        try:
            if float(value) >= float(series_parameters["alarmhigh"]):
                text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                text_body = text_body + 'is high - ' + alerttype + ' = ' + str(value) + " threshold: " + str(series_parameters["alarmhigh"]) + " timestamp is:" + timestamp + '\n'
                result['status']="active"
        except:
            result['status']="inactive"



    result['message']=text_body
    return result




def process_emailalert(text_body, parameters, timestamp, value):


    result={}
    result['status']="off"
    result['sunrise']="---"
    result['sunset']="---"
    result['message']=""
    result['timmer']=""
    timmerArray = []


    log.info('alert_processor:process_emailalert start: %s : %s', parameters, value)

    try:

        # Check alerts are enabled
        alertenabled = True

        try:
            log.info('alert_processor: alert enabled parameter %s  ', parameters["alertenabled"])


            alertenabled = parameters["alertenabled"]
            if alertenabled == "disabled":
                log.info('alert_processor process_emailalert: alert is disabled ' )
                result['status']="disabled"
                result['message']=""
                return result
                         
        except:
            alertenabled = True

        # alerts are enabled so continue
        log.info('alert_processor process_emailalert: alert is enabled ' )

        series_parameters = parameters.get('series_1',"")
        # check for error/missing series parameters and retutn
        if series_parameters == "":
            return result

        log.info('alert_processor series_parameters: %s ', series_parameters )
            
        #check if alarm mode is specified
        alarmmode = str(series_parameters["alarmmode"])

        log.info('alert_processor alarmmode: %s ', alarmmode )

        #  not enabled so just exit          
        if alarmmode == "disabled":
            result['status']="off"
            result['message']=""
            return result



        # check if we are doing a switch or dimmer event alarm
        elif alarmmode == "alarmswitchon" or alarmmode == "alarmswitchoff" or alarmmode == "alarmleddimmer" or alarmmode == "alarmrgbdimmer" or alarmmode == "alarmblinkdimmer" or alarmmode == "alarmblinkdimmeronoff" or alarmmode == "alarmdimmeroverride":

            #initialize default return values
            result['status']="error"
            result['message']=""
            #return result

            alerttype = parameters.get('alerttype',"timmer")

            log.info('alert_processor alerttype: %s ', alerttype )
            
            #timmer event once only
            if alerttype == "timmer":

                #create timmer array of dimmer values based on start and stop times            
                result = get_timmer_alert(parameters, value)

            #timmer event daily repeat
            elif alerttype == "timmerday":
                #create timmer array of dimmer values based on start and stop times            
                result = get_timmerday_alert(parameters, value)                

            #timmer event based on local sunrise sunset
            elif alerttype == "sunriseset" or alerttype == "sunsetrise" or alerttype == "sunriseexpires" or alerttype == "sunsetexpires" or alerttype == "startsunrise" or alerttype == "startsunset":
                log.info('alert_processor: get location %s  : %s', series_parameters["alarmlow"], series_parameters["alarmhigh"])

                #use location to determine sunrise and sunset times
                result = get_sunriseset_alert(parameters, value)


        # to do - need to handle serires status        
        elif str(series_parameters["alarmmode"]) == "status":
            result = get_status_alert(parameters, value)

        elif alarmmode == "alarm" or alarmmode == "alarmemail" or alarmmode == "alarmsms" or alarmmode == "alarmemailsms":

            # use alarmlow alarmhigh thresholds to trigger email/sms alerts
            result = get_alarms_alert(parameters, value)
        

        #result['message']=text_body
        return result
    
    except TypeError as e:
        if debug_all: log.info('alert_processor: TypeError in process_emailaler %s:%s  ', text_body, value)

        if debug_all: log.info('alert_processor: TypeError in process_emailaler %s:  ' % str(e))

    except ValueError as e:
        if debug_all: log.info('alert_processor: ValueError in process_emailaler %s:%s  ', text_body, value)

        if debug_all: log.info('alert_processor: TypeError in process_emailaler %s:  ' % str(e))

    except AttributeError as e:
        if debug_all: log.info('alert_processor: AttributeError in process_emailaler %s:%s  ', text_body, value)

        if debug_all: log.info('alert_processor: AttributeError in process_emailaler %s:  ' % str(e))        
        
    except KeyError as e:
        if debug_all: log.info('alert_processor: KeyError in process_emailaler %s:%s  ', text_body, value)

        if debug_all: log.info('alert_processor: KeyError in process_emailaler %s:  ' % str(e))

    except NameError as e:
        if debug_all: log.info('alert_processor: NameError in process_emailaler %s:%s  ', text_body, value)

        if debug_all: log.info('alert_processor: NameError in process_emailaler %s:  ' % str(e))     

    except:
        if debug_all: log.info('alert_processor: Error in process_emailalert %s:%s  ', text_body, value)
        e = sys.exc_info()[0]

        if debug_all: log.info("Error: %s" % e)
        mymessage='Error in geting process_emailalert'
        return result
