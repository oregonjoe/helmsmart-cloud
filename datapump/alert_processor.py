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
from astral.sun import sun

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

    timestamp = str(datetime.datetime.now())

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
        
        if str(series_parameters["alarmlow"]) != "off" :
                      
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
                    text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
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

    except NameError as e:
        if debug_all: log.info('get_timmer_alert: NameError in timmer once %s  ', text_body)
        if debug_all: log.info('get_timmer_alert: NameError in timmer once %s:  ' % str(e))

    except AttributeError as e:
        if debug_all: log.info('get_timmer_alert: AttributeError in timmer once %s  ', text_body)
        if debug_all: log.info('get_timmer_alert: AttributeError in timmer once %s:  ' % str(e))

    except TypeError as e:
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

    timestamp = str(datetime.datetime.now())

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
            #log.info('get_sunriseset_alert: process_emailalert timmerday modulo secs times %s:  %s:   %s  ', int(currentsecs % (24*60*60))     , int(startsecs % (24*60*60)),  int(endsecs % (24*60*60)))  
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
            #log.info('get_sunriseset_alert: process_emailalert timmerday compare secs times %s:  %s:   %s  ', currentsecs, startsecs, endsecs)                    
            #log.info('get_sunriseset_alert: process_emailalert timmerday offset  %s current secs  %s:   ', secoffset, (currentsecs - secoffset))

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

                except NameError as e:
                    if debug_all: log.info('get_timmerday_alert: NameError in  timmerday start < end %s:%s  ', text_body, value)
                    if debug_all: log.info('get_timmerday_alert: NameError in  timmerday start < end %s:  ' % str(e))
                        
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

                except NameError as e:
                    if debug_all: log.info('get_timmerday_alert: NameError in  timmerday start > end %s:%s  ', text_body, value)
                    if debug_all: log.info('get_timmerday_alert: NameError in  timmerday start > end %s:  ' % str(e))
                               
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
    timmerArray = []
    
    timestamp = str(datetime.datetime.now())

    text_body= "error in timmer alert"
    alerttype = parameters.get('alerttype',"mean")

    log.info("get_sunriseset_alert  deviceID: %s", parameters['deviceid'])


    # extract the series alarm paramterts
    series_parameters = parameters.get('series_1',"")
    # check for errors
    if series_parameters == "":
        result['status']="error"
        result['message']="missing series parameters"
        return result

    # Check if there is a duration and offset
    alertduration = 0
    alertoffset = 0
    try:
        log.info('get_sunriseset_alert: get sunrise-set duration parameter %s  ', parameters["alertduration"])
        log.info('get_sunriseset_alert: get sunrise-set offset parameter %s  ', parameters["alertoffset"])

        alertduration = durationsec(parameters["alertduration"])
        alertoffset = durationsec(parameters["alertoffset"])
        alertdefault_value = int(parameters.get('alertdefault_value',255))
        
    except:
        alertduration = 0
        alertoffset = 0
        alertdefault_value = 255

    log.info('get_sunriseset_alert: get sunrise-set duration parameter %s  ', alertduration)
    log.info('get_sunriseset_alert: get sunrise-set offset parameter %s  ', alertoffset)
    log.info('get_sunriseset_alert: get sunrise-set alertdefault_value parameter %s  ', alertdefault_value)

    
    log.info('get_sunriseset_alert:process_emailalert sunrise sunset Initialize Timmer array')

    for t_hours in range(0, 144):
        #timmerArray.append(255)
        timmerArray.append(alertdefault_value)
    
    try:
        sunriseset={}

        """
        location={}
        location['city']= 'San Francisco'
        location['lat']= 0
        location['lng']= 0
                  
        try:
            location['lat'] =float(series_parameters["alarmlow"])
            location['lat'] =float(series_parameters["alarmhigh"])

        except:
            location['lat']= 0
            location['lng']= 0
            
            if alerttype == "startsunrise" or alerttype == "startsunset" :
                location['city']= series_parameters["alarmhigh"]
            else:
                location['city']= series_parameters["alarmlow"]
        """

        
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

        #gets sunset sunrise for current location in local time not GMT or UTC                    
        #sunriseset = getSunRiseSet(location)
        #sunriseset = sun(location, timestamp)
        #get timezone for current sunset/sunrise location
        timezone = location.timezone
        mylocal = pytz.timezone(timezone)
        #get current local time for sunset/sunrise location
        lccurrenttime = datetime.datetime.now(mylocal)
        #need to calculate sunise and set for current day not tomorrow
        #currenttime = datetime.datetime.now()
        newdaytime = lccurrenttime.replace(hour=0, minute=0, second=0)
        log.info('get_sunriseset_alert:newdaytime-> %s ',newdaytime)

        
        # this gets in UTC
        #sunriseset = sun(location.observer, datetime.datetime.now())
        #this gets in local time
        sunriseset = sun(location.observer, newdaytime, tzinfo=location.timezone)
        log.info('get_sunriseset_alert: get sunrise-set type->%s  times-> %s ', alerttype , sunriseset)
        
        sunrise = sunriseset['sunrise']
        sunset =  sunriseset['sunset']
        #timezone =  sunriseset['timezone']
        timezone = location.timezone
        
        result['sunrise']=str(sunrise)
        result['sunset']=str(sunset)
                    
        log.info('get_sunriseset_alert: process_emailalert sunriseset local times %s:%s timezone ->%s ',  sunrise, sunset, timezone)

        #get timezone for current sunset/sunrise location
        mylocal = pytz.timezone(timezone)
        #get current local time for sunset/sunrise location
        currenttime = datetime.datetime.now(mylocal)

        #pushsmart gateways use UTC times for timmer compares
        sunrise_utc = sunrise.astimezone(pytz.utc)
        sunset_utc = sunset.astimezone(pytz.utc)
        log.info('get_sunriseset_alert: process_emailalert sunriseset times UTC %s:%s ',  sunrise_utc, sunset_utc)



        
        #currenttime = currenttime.replace(year=2000, month=1, day=1)
        #currentsecounds = (mytime.hour * 60 * 60) + (mytime.minute * 60)  + mytime.second
        #log.info('get_sunriseset_alert: process_emailalert sunriseset alert %s:%s  ', str(series_parameters["alarmlow"]), currentsecounds)
        log.info('get_sunriseset_alert: process_emailalert sunriseset currenttime %s ', currenttime)    
        #currenttime = todayAt (mytime.hour, mytime.minute , mytime.second)

        #starttime = datetime.datetime.now(int(series_parameters["alarmlow"]))
        #sunrisetime = datetime.datetime.fromtimestamp(sunrise)
        sunrisetime = sunrise
        #deltatime = currenttime - sunrisetime
        log.info('get_sunriseset_alert: process_emailalert sunriseset  current->%s  sunrise->%s  ', currenttime, sunrisetime)
        if currenttime >= sunrisetime:
            log.info('get_sunriseset_alert: process_emailalert sunriseset  sun is up %s',  currenttime)
        
        #sunrisetime = sunrisetime.replace(year=2000, month=1, day=1)
        #starthour = int(int(sunrise)  % (60*60))
        #startmin =int((int(sunrise) % (60*60)) / 60)
        #startsec= int(sunrise) % (60)
        log.info('get_sunriseset_alert: process_emailalert sunriseset sunrisetime %s:%s  ', currenttime, sunrisetime)  
        #starttime = todayAt (starthour, startmin, startsec)
        #starttime = todayAt(mytime.hour, mytime.minute , mytime.second)
        
        #endtime = datetime.datetime.now(int(series_parameters["alarmhigh"]))
        #sunsettime = datetime.datetime.fromtimestamp(sunset)
        sunsettime = sunset
        #deltatime = currenttime - sunsettime
        log.info('get_sunriseset_alert: process_emailalert sunriseset   current->%s  sunset->%s  ', currenttime, sunsettime)
        if currenttime >= sunsettime:
            log.info('get_sunriseset_alert: process_emailalert sunriseset  sun is down %s', currenttime)

            
        #sunsettime = sunsettime.replace(year=2000, month=1, day=1)
        #endhour = int(int(sunset) % (60*60))
        #endmin =int((int(sunset) % (60*60)) / 60)
        #endsec= int(sunset) % (60)
        log.info('get_sunriseset_alert: process_emailalert sunriseset sunsettime %s:%s  ', currenttime,  sunsettime)  
        #endtime = todayAt (endhour, endmin, endsec)
        #endtime = todayAt (mytime.hour, mytime.minute , mytime.second)

        log.info('get_sunriseset_alert: process_emailalert sunriseset times %s  :  %s  :  %s  ', currenttime, sunrisetime, sunsettime)           

        if currenttime >= sunrisetime and currenttime < sunsettime:
            log.info('get_sunriseset_alert: process_emailalert sunriseset  sun is up 2 %s',  currenttime)

        try:

            #The sunset and sunrise times have been adjusted to not change during the current local time
            #They only change at midnight
            #
            if alerttype == "sunriseset":
                log.info('get_sunriseset_alert: process_emailalert compare sun rise->set times %s  :  %s  :  %s  ', currenttime, sunrisetime, sunsettime)
                midnighttime = currenttime.replace(hour=23, minute=59, second=59)
                log.info('get_sunriseset_alert: process_emailalert compare sun rise->set times midnight %s  ', midnighttime)
                newdaytime = currenttime.replace(hour=0, minute=0, second=0)
                log.info('get_sunriseset_alert: process_emailalert compare sun rise->set times newdaytime %s  ', newdaytime)

                log.info('get_sunriseset_alert: process_emailalert compare sun rise->set times alertoffset %s  ', alertoffset)
                if alertoffset != 0:
                    sunrisetime = sunrisetime + datetime.timedelta(seconds = alertoffset)
                    sunsettime = sunsettime + datetime.timedelta(seconds = -alertoffset)
                    log.info('get_sunriseset_alert: process_emailalert adjusted sun rise->set times %s  :  %s  :  %s  ', alertoffset, sunrisetime, sunsettime)


                log.info('get_sunriseset_alert: process_emailalert compare sun rise->set times alertduration %s  ', alertduration)
                if alertduration != 0:
                    sunsettime = sunrisetime + datetime.timedelta(seconds = alertduration)
                    log.info('get_sunriseset_alert: process_emailalert adjusted sun rise->set times %s  :  %s  :  %s  ', alertduration, sunrisetime, sunsettime)

                sunrisesecs = int(time.mktime(sunrisetime.timetuple()) % (60*60*24))
                sunsetsecs = int(time.mktime(sunsettime.timetuple()) % (60*60*24))
                log.info('get_sunriseset_alert: process_emailalert compare sun rise ->set times  seconds %s  ', sunrisesecs)
                log.info('get_sunriseset_alert: process_emailalert compare sun rise ->set times  seconds %s  ', sunsetsecs)

                sunrise_utc_sec = int(time.mktime(sunrise_utc.timetuple()) % (60*60*24))
                sunset_utc_sec = int(time.mktime(sunset_utc.timetuple()) % (60*60*24))
                log.info('get_sunriseset_alert: process_emailalert sunriseset seconds UTC %s:%s ',  sunrise_utc_sec, sunset_utc_sec)
                
                alertaction_value = int(parameters.get('alertaction_value',255))
                log.info('get_sunriseset_alert: process_emailalert compare sun rise ->set times sunset alertaction_value %s  ', alertaction_value)

                if sunrise_utc_sec > sunset_utc_sec:
                    for t_tenmin in range(0, 6*24):                           
                        if t_tenmin <= sunset_utc_sec/(10*60):
                            timmerArray[t_tenmin] = alertaction_value                                 
                        elif t_tenmin >= sunrise_utc_sec/(10*60):
                            timmerArray[t_tenmin] =alertaction_value    
                else:
                    for t_tenmin in range(0, 6*24):
                        if t_tenmin >= sunrise_utc_sec/(10*60) and t_tenmin <= sunset_utc_sec/(10*60) :                                   
                            timmerArray[t_tenmin] =alertaction_value

                log.info('get_sunriseset_alert: process_emailalert compare sun rise ->set times timmerArray %s  ', timmerArray)                            
                    
                #current time can be greater then sunset and greater then sunrise on current day
                if currenttime >=  sunrisetime and currenttime <=  sunsettime:
                    text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                    text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                    text_body = text_body + 'is low - ' + alerttype + ' = ' + str(currenttime) + " threshold: " + str(sunrisetime) + " timestamp is:" + timestamp + '\n'
                    result['status']="active"
                    log.info('get_sunriseset_alert: process_emailalert sunriseset sun is up alerttext %s:%s  ', text_body, currenttime)
                    
                else:
                    result['status']="inactive"
                    text_body = "alert is inactive - current time is outside sunrise/sunset"
                    log.info('get_sunriseset_alert timmerday inactive sunriseset %s:%s  ', text_body, currenttime)

            if alerttype == "sunsetrise":
                log.info('get_sunriseset_alert: process_emailalert compare sun set ->rise times %s  :  %s  :  %s  ', currenttime, sunrisetime, sunsettime)
                midnighttime = currenttime.replace(hour=23, minute=59, second=59)
                log.info('get_sunriseset_alert: process_emailalert compare sun set ->rise times midnight %s  ', midnighttime)
                newdaytime = currenttime.replace(hour=0, minute=0, second=0)
                log.info('get_sunriseset_alert: process_emailalert compare sun set ->rise times newdaytime %s  ', newdaytime)

                log.info('get_sunriseset_alert: process_emailalert compare sun set ->rise times alertoffset %s  ', alertoffset)
                if alertoffset != 0:
                    sunsettime = sunsettime + datetime.timedelta(seconds = alertoffset)
                    sunrisetime = sunrisetime + datetime.timedelta(seconds = -alertoffset)
                    log.info('get_sunriseset_alert: process_emailalert adjusted sun set ->rise times %s  :  %s  :  %s  ', alertoffset, sunrisetime, sunsettime)

                #log.info('get_sunriseset_alert: process_emailalert compare sun set ->rise times alertduration %s  ', alertduration)

                sunrisesecs = int(time.mktime(sunrisetime.timetuple()) % (60*60*24))
                sunsetsecs = int(time.mktime(sunsettime.timetuple()) % (60*60*24))
                log.info('get_sunriseset_alert: process_emailalert compare sun set ->rise times sunrise seconds %s  ', sunrisesecs)
                log.info('get_sunriseset_alert: process_emailalert compare sun set ->rise times sunset seconds %s  ', sunsetsecs)


                sunrise_utc_sec = int(time.mktime(sunrise_utc.timetuple()) % (60*60*24))
                sunset_utc_sec = int(time.mktime(sunset_utc.timetuple()) % (60*60*24))
                log.info('get_sunriseset_alert: process_emailalert sunriseset seconds UTC %s:%s ',  sunrise_utc_sec, sunset_utc_sec)
                
                alertaction_value = int(parameters.get('alertaction_value',255))
                log.info('get_sunriseset_alert: process_emailalert compare sun set ->rise times sunset alertaction_value %s  ', alertaction_value)
                """                            
                for t_tenmin in range(0, 6*24):
                    
                    #if t_tenmin > sunsetsecs/(10*60):                               
                    if t_tenmin > sunset_utc_sec/(10*60):
                        timmerArray[t_tenmin] = alertaction_value
                    #elif t_tenmin < sunrisesecs/(10*60):                                    
                    elif t_tenmin < sunrise_utc_sec/(10*60):
                        timmerArray[t_tenmin] =alertaction_value
                """   
                #sunset to sun rise
                if sunrise_utc_sec < sunset_utc_sec:
                    for t_tenmin in range(0, 6*24):                           
                        if t_tenmin >= sunset_utc_sec/(10*60):
                            timmerArray[t_tenmin] = alertaction_value                                 
                        elif t_tenmin <= sunrise_utc_sec/(10*60):
                            timmerArray[t_tenmin] =alertaction_value    
                else:
                    for t_tenmin in range(0, 6*24):
                        if t_tenmin >= sunset_utc_sec/(10*60) and t_tenmin <= sunrise_utc_sec/(10*60) :                                   
                            timmerArray[t_tenmin] =alertaction_value

                        

                log.info('get_sunriseset_alert: process_emailalert compare sun set ->rise times timmerArray %s  ', timmerArray)

                
                #current time can be greater then sunset and greater then sunrise on current day
                if alertduration == 0:
                    if currenttime < midnighttime and  currenttime >=  sunsettime:
                        text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                        text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                        text_body = text_body + 'is low - ' + alerttype + ' = ' + str(currenttime) + " threshold: " + str(sunsettime) + " timestamp is:" + timestamp + '\n'
                        result['status']="active"
                        log.info('get_sunriseset_alert: process_emailalert sunsetrise sun is down alerttext %s:%s  ', text_body, currenttime)
                    
                    #current time can be before sunrise on the next day
                    elif currenttime > newdaytime and currenttime <= sunrisetime:                                
                        text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                        text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                        text_body = text_body + 'is low - ' + alerttype + ' = ' + str(currenttime) + " threshold: " + str(sunsettime) + " timestamp is:" + timestamp + '\n'
                        result['status']="active"
                        log.info('get_sunriseset_alert: process_emailalert sunsetrise sun is down alerttext %s:%s  ', text_body, currenttime)
                        
                    else:
                        result['status']="inactive"
                        text_body = "alert is inactive - current time is outside sunrise/sunset"
                        log.info('get_sunriseset_alert timmerday inactive sunsetrise %s:%s  ', text_body, currenttime)

               #if using duration then we just add to current sunset time 
                elif alertduration != 0:
                    
                    log.info('get_sunriseset_alert: process_emailalert compare sun set ->rise times alertduration %s  ', alertduration)
                    sunrisetime = sunsettime + datetime.timedelta(seconds = alertduration)
                    log.info('get_sunriseset_alert: process_emailalert adjusted sun set ->rise times %s  :  %s  :  %s  ', alertduration, sunsettime, sunrisetime )                              
                    
                    #current time can be before sunrise on the next day
                    if currenttime > sunsettime and currenttime <= sunrisetime:                                
                        text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                        text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                        text_body = text_body + 'is low - ' + alerttype + ' = ' + str(currenttime) + " threshold: " + str(sunsettime) + " timestamp is:" + timestamp + '\n'
                        result['status']="active"
                        log.info('get_sunriseset_alert: process_emailalert sunsetrise sun is down alerttext %s:%s  ', text_body, currenttime)
                        
                    else:
                        result['status']="inactive"
                        text_body = "alert is inactive - current time is outside sunrise/sunset"
                        log.info('get_sunriseset_alert timmerday inactive sunsetrise %s:%s  ', text_body, currenttime)

            # check for time greater then sunset but less then specified expires time
            if alerttype == "sunsetexpires" or alerttype == "sunriseexpires":
                #endsecs is based on UTC time and not local to sunsire/sunset
                endsecs = int(series_parameters["alarmhigh"])
                #get UTC time
                endtime = datetime.datetime.fromtimestamp(endsecs)
                log.info('get_sunriseset_alert: process_emailalert sunsetriseexpires endtime secs %s  -> %s', endtime, endsecs)

                #need to make time value timezone aeare
                utcendtime = pytz.utc.localize(endtime)
                log.info('get_sunriseset_alert: process_emailalert sunsetriseexpires endtime secs %s  -> %s', utcendtime, endsecs)

                #determine end time in UTC used by gateway timmers which are based on UTC
                endutcsecs_local  = mylocal.localize(endtime, is_dst=None) # No daylight saving time
                log.info('get_sunriseset_alert: process_emailalert sunsetriseexpires endtime  utcendtime local time %s ',endutcsecs_local)
                endutcsecs_utc = endutcsecs_local.astimezone(pytz.utc)
                log.info('get_sunriseset_alert: process_emailalert sunsetriseexpires endtime  utcendtime utc time %s ',endutcsecs_utc)                   
                endutcsecs = time.mktime(endutcsecs_utc.timetuple())
                log.info('get_sunriseset_alert: process_emailalert sunsetriseexpires endtime  endutcsecs %s  -> %s', endutcsecs, int(endutcsecs % (24*60*60)))



                sunrise_utc_sec = int(time.mktime(sunrise_utc.timetuple()) % (60*60*24))
                sunset_utc_sec = int(time.mktime(sunset_utc.timetuple()) % (60*60*24))
                log.info('get_sunriseset_alert: process_emailalert sunsetriseexpires seconds UTC %s:%s ',  sunrise_utc_sec, sunset_utc_sec)
                

                # adjust time to sunset/sunrise local time
                #localendtime = utcendtime.astimezone(mylocal)
                localendtime = endtime
                # get seconds so we can convert to 24 hour clock
                localendseconds = time.mktime(localendtime.timetuple())
                log.info('get_sunriseset_alert: process_emailalert sunsetriseexpires localendtime %s -> %s ', localendtime, localendseconds)     
                #only need 24 hours out of UTC time
                log.info('get_sunriseset_alert: process_emailalert sunsetriseexpires end secs %s  -> %s', localendseconds, int(localendseconds % (24*60*60)))

                #currenttime is based on location for sunset/sunrise and not UTC
                alertendtime = currenttime.replace(hour=0, minute=0, second=0)
                alertendtime =alertendtime + datetime.timedelta(seconds = int(localendseconds % (24*60*60)))
                
                log.info('get_sunriseset_alert: process_emailalert compare sun set ->expires times %s  :  %s  :  %s  ', currenttime, sunsettime, alertendtime)

                midnighttime = currenttime.replace(hour=23, minute=59, second=59)
                log.info('get_sunriseset_alert: process_emailalert compare sun set ->expires times midnight %s  ', midnighttime)
                newdaytime = currenttime.replace(hour=0, minute=0, second=0)
                log.info('get_sunriseset_alert: process_emailalert compare sun set ->expires times newdaytime %s  ', newdaytime)

                log.info('get_sunriseset_alert: process_emailalert compare sun set ->expires times alertoffset %s  ', alertoffset)
                if alertoffset != 0:
                    sunsettime = sunsettime + datetime.timedelta(seconds = alertoffset)
                    sunrisetime = sunrisetime + datetime.timedelta(seconds = -alertoffset)
                    log.info('get_sunriseset_alert: process_emailalert adjusted sun set ->expires times %s  :  %s  :  %s  ', alertoffset, sunsettime, alertendtime)

                #log.info('get_sunriseset_alert: process_emailalert compare sun set ->rise times alertduration %s  ', alertduration)



                # check from sunset to expire time
                if alerttype == "sunsetexpires":

                    #create timmer array
                    alertendutcsecs = int(endutcsecs % (60*60*24))
                    log.info('get_sunriseset_alert: process_emailalert compare sunsetexpires->end times  utc seconds %s  ', alertendutcsecs)
                    log.info('get_sunriseset_alert: process_emailalert compare sunsetexpires ->set times  utc seconds %s  ', sunset_utc_sec)

                    
                    alertaction_value = int(parameters.get('alertaction_value',255))
                    log.info('get_sunriseset_alert: process_emailalert compare sunsetexpires -> sunset alertaction_value %s  ', alertaction_value)
                    
                    log.info('get_sunriseset_alert: process_emailalert compare sunsetexpires ->alertendtime %s  sunsettime %s', alertendtime, sunsettime)

                    try:
                        #Timmer sunset to expires
                        if alertendutcsecs < sunset_utc_sec:
                            log.info('get_sunriseset_alert: process_emailalert timmer array sunsetexpires ->alertendutcsecs %s  sunsettime %s', alertendutcsecs, sunset_utc_sec)
                            for t_tenmin in range(0, 6*24):                           
                                if t_tenmin >= sunset_utc_sec/(10*60):
                                    timmerArray[t_tenmin] = alertaction_value                                 
                                elif t_tenmin <= alertendutcsecs/(10*60):
                                    timmerArray[t_tenmin] =alertaction_value    
                        else:
                            for t_tenmin in range(0, 6*24):
                                if t_tenmin >= sunset_utc_sec/(10*60) and t_tenmin <= alertendutcsecs/(10*60) :                                   
                                    timmerArray[t_tenmin] =alertaction_value

                    except UnboundLocalError as e:
                        #log.info('get_sunriseset_alert: UnboundLocalErrorr in sunsetexpires   ')
                        log.info('get_sunriseset_alert: UnboundLocalErrorr in sunsetexpires %s:  ' % str(e))
                        pass
                        
                    except:
                        e = sys.exc_info()[0]
                        log.info('get_sunriseset_alert: process_emailalert compare sunsetexpires ERROR %s  ' % e)
                        pass

                    log.info('get_sunriseset_alert: process_emailalert compare sunsetexpires -> timmerArray %s  ', timmerArray)



                    
                    #current time can be greater then sunset and greater then sunrise on current day
                    if alertendtime > sunsettime:

                        alertendsecs = int(time.mktime(alertendtime.timetuple()) % (60*60*24))
                        sunsetsecs = int(time.mktime(sunsettime.timetuple()) % (60*60*24))
                        log.info('get_sunriseset_alert: process_emailalert compare sunsetexpires->end times  seconds %s  ', alertendsecs)
                        log.info('get_sunriseset_alert: process_emailalert compare sunsetexpires ->set times  seconds %s  ', sunsetsecs)


                        alertaction_value = int(parameters.get('alertaction_value',255))
                        log.info('get_sunriseset_alert: process_emailalert compare sunsetexpires -> sunset alertaction_value %s  ', alertaction_value)
                        

                
                        if currenttime < midnighttime and  currenttime >=  sunsettime and  currenttime <  alertendtime:
                            text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                            text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                            text_body = text_body + 'is low - ' + alerttype + ' = ' + str(currenttime) + " threshold: " + str(sunsettime) + " timestamp is:" + timestamp + '\n'
                            result['status']="active"
                            log.info('get_sunriseset_alert: process_emailalert sunsetexpires sun is down and less then alertend time %s:%s  ', text_body, currenttime)
                        else:
                            result['status']="inactive"
                            text_body = "alert is inactive - current time is outside sunrise/sunset"
                            log.info('get_sunriseset_alert timmerday inactive sunsetexpires %s:%s  ', text_body, currenttime)

                    # if alertendtime is less then sunset time thne alert runs from current day after sunset till next day
                    if alertendtime < sunsettime:

                        alertendsecs = int(time.mktime(alertendtime.timetuple()) % (60*60*24))
                        sunsetsecs = int(time.mktime(sunsettime.timetuple()) % (60*60*24))
                        log.info('get_sunriseset_alert: process_emailalert compare sunsetexpires->end times  seconds %s  ', alertendsecs)
                        log.info('get_sunriseset_alert: process_emailalert compare sunsetexpires ->set times  seconds %s  ', sunsetsecs)
                        alertaction_value = int(parameters.get('alertaction_value',255))
                        log.info('get_sunriseset_alert: process_emailalert compare sunsetexpires -> sunset alertaction_value %s  ', alertaction_value)
                        

                        
                        #current time can be before sunrise on the next day
                        if currenttime > sunsettime and currenttime <= midnighttime:                                
                            text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                            text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                            text_body = text_body + 'is low - ' + alerttype + ' = ' + str(currenttime) + " threshold: " + str(sunsettime) + " timestamp is:" + timestamp + '\n'
                            result['status']="active"
                            log.info('get_sunriseset_alert: process_emailalert sunsetexpires sun is down alerttext %s:%s  ', text_body, currenttime)
                            
                        elif currenttime > newdaytime and currenttime <= alertendtime:                                
                            text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                            text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                            text_body = text_body + 'is low - ' + alerttype + ' = ' + str(currenttime) + " threshold: " + str(sunsettime) + " timestamp is:" + timestamp + '\n'
                            result['status']="active"
                            log.info('get_sunriseset_alert: process_emailalert sunsetexpires sun is down alerttext %s:%s  ', text_body, currenttime)
                            
                        else:
                            result['status']="inactive"
                            text_body = "alert is inactive - current time is outside sunrise/sunset"
                            log.info('get_sunriseset_alert timmerday inactive sunsetexpires %s:%s  ', text_body, currenttime)

                # check from sunsire to expire time
                elif alerttype == "sunriseexpires" : 
                    # just going to check the case when current time is greater then sunrise and less then endtime
                    # This will only work between sunrise and midnight


                    alertendutcsecs = int(endutcsecs % (60*60*24))
                    log.info('get_sunriseset_alert: process_emailalert compare sunriseexpires->end times  utc seconds %s  ', alertendutcsecs)
                    log.info('get_sunriseset_alert: process_emailalert compare sunriseexpires ->rise times  utc seconds %s  ', sunrise_utc_sec)

                    
                    alertaction_value = int(parameters.get('alertaction_value',255))
                    log.info('get_sunriseset_alert: process_emailalert compare sunriseexpires -> sunset alertaction_value %s  ', alertaction_value)
                    


                    #Timmer sunset to expires
                    if alertendutcsecs < sunrise_utc_sec:
                        for t_tenmin in range(0, 6*24):                           
                            if t_tenmin >= sunrise_utc_sec/(10*60):
                                timmerArray[t_tenmin] = alertaction_value                                 
                            elif t_tenmin <= alertendutcsecs/(10*60):
                                timmerArray[t_tenmin] =alertaction_value    
                    else:
                        for t_tenmin in range(0, 6*24):
                            if t_tenmin >= sunrise_utc_sec/(10*60) and t_tenmin <= alertendutcsecs/(10*60) :                                   
                                timmerArray[t_tenmin] =alertaction_value



                    log.info('get_sunriseset_alert: process_emailalert compare sunriseexpires -> timmerArray %s  ', timmerArray)


                    
                    if alertendtime > sunrisetime:

                        alertendsecs = int(time.mktime(alertendtime.timetuple()) % (60*60*24))
                        sunrisesecs = int(time.mktime(sunrisetime.timetuple()) % (60*60*24))
                        log.info('get_sunriseset_alert: process_emailalert compare sunriseexpires->end times  seconds %s  ', alertendsecs)
                        log.info('get_sunriseset_alert: process_emailalert compare sunriseexpires ->rise times  seconds %s  ', sunrisesecs)
                        alertaction_value = int(parameters.get('alertaction_value',255))
                        log.info('get_sunriseset_alert: process_emailalert compare sunriseexpires -> sunset alertaction_value %s  ', alertaction_value)
                        
                        for t_tenmin in range(0, 6*24):
                            
                            if t_tenmin > sunrisesecs/(10*60) and t_tenmin < alertendsecs/(10*60) :
                                timmerArray[t_tenmin] =alertaction_value

                        log.info('get_sunriseset_alert: process_emailalert compare sunriseexpires -> timmerArray %s  ', timmerArray)

                        
                        if  currenttime <  alertendtime:
                            text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                            text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                            text_body = text_body + 'is low - ' + alerttype + ' = ' + str(currenttime) + " threshold: " + str(sunrisetime) + " timestamp is:" + timestamp + '\n'
                            result['status']="active"
                            log.info('get_sunriseset_alert: process_emailalert sunsetexpires sun is up and less then alertend time %s:%s  ', text_body, currenttime)
                        else:
                            result['status']="inactive"
                            text_body = "alert is inactive - current time is outside sunrise/sunset"
                            log.info('get_sunriseset_alert timmerday inactive sunriseexpires %s:%s  ', text_body, currenttime)
                    """
                    #if end time is less thne current sunset then it for the next day after midnight
                    if alertendtime < sunrisetime:
                        #current time can be before sunrise on the next day
                        if currenttime > newdaytime and currenttime <= alertendtime:                                
                            text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                            text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                            text_body = text_body + 'is low - ' + alerttype + ' = ' + str(currenttime) + " threshold: " + str(sunrisetime) + " timestamp is:" + timestamp + '\n'
                            result['status']="active"
                            log.info('get_sunriseset_alert: process_emailalert sunsetexpires sun is up alerttext %s:%s  ', text_body, currenttime)
                            
                        else:
                            result['status']="inactive"
                    """


            # check for time greater then sunset but less then specified expires time
            if alerttype == "startsunrise" or alerttype == "startsunset":

                #startsecs is based on UTC time and not local to sunsire/sunset
                startsecs = int(series_parameters["alarmlow"])
                #get UTC time
                starttime = datetime.datetime.fromtimestamp(startsecs)
                log.info('get_sunriseset_alert: process_emailalert startsunrise starttime secs %s  -> %s', starttime, startsecs)



                #determine UTC start time for use with gateway Timmers which are based on UTC
                startutcsecs_local  = mylocal.localize(starttime, is_dst=None) # No daylight saving time
                log.info('get_sunriseset_alert: process_emailalert  startsunrise starttime utcstarttime local time %s ',startutcsecs_local)
                startutcsecs_utc = startutcsecs_local.astimezone(pytz.utc)
                log.info('get_sunriseset_alert: process_emailalert  startsunrise starttime utcstarttime utc time %s ',startutcsecs_utc)                   
                startutcsecs = time.mktime(startutcsecs_utc.timetuple())
                log.info('get_sunriseset_alert: process_emailalert  startsunrise starttime startutcsecs %s  -> %s', startutcsecs, int(startutcsecs % (24*60*60)))



                sunrise_utc_sec = int(time.mktime(sunrise_utc.timetuple()) % (60*60*24))
                sunset_utc_sec = int(time.mktime(sunset_utc.timetuple()) % (60*60*24))
                log.info('get_sunriseset_alert: process_emailalert startsunrise seconds UTC %s:%s ',  sunrise_utc_sec, sunset_utc_sec)                            

                #need to make time value timezone aeare
                utcstarttime = pytz.utc.localize(starttime)
                log.info('get_sunriseset_alert: process_emailalert startsunrise utcstarttime secs %s  -> %s', utcstarttime, startsecs)  

                # adjust time to sunset/sunrise local time
                #localstarttime = utcstarttime.astimezone(mylocal)
                localstarttime = starttime
                # get seconds so we can convert to 24 hour clock
                localstartsecs = time.mktime(localstarttime.timetuple())
                log.info('get_sunriseset_alert: process_emailalert startsunrise localstarttime %s -> %s ', localstarttime, localstartsecs)     
                #only need 24 hours out of UTC time
                log.info('get_sunriseset_alert: process_emailalert startsunrise start secs %s  -> %s', localstartsecs, int(localstartsecs % (24*60*60)))

                
                alertstarttime = currenttime.replace(hour=0, minute=0, second=0)
                alertstarttime =alertstarttime + datetime.timedelta(seconds = int(localstartsecs % (24*60*60)))
                
                log.info('get_sunriseset_alert: process_emailalert startsunsetrise compare start >- sun rise times %s  :  %s  :  %s  ', currenttime, sunrisetime, alertstarttime)

                midnighttime = currenttime.replace(hour=23, minute=59, second=59)
                log.info('get_sunriseset_alert: process_emailalert startsunsetrise compare start >- sun rise times midnight %s  ', midnighttime)
                newdaytime = currenttime.replace(hour=0, minute=0, second=0)
                log.info('get_sunriseset_alert: process_emailalert startsunsetrise compare start >- sun rise times newdaytime %s  ', newdaytime)

                log.info('get_sunriseset_alert: process_emailalert startsunsetrise compare start >- sun rise times alertoffset %s  ', alertoffset)
                if alertoffset != 0:
                    sunrisetime = sunrisetime + datetime.timedelta(seconds = -alertoffset)
                    sunsettime = sunsettime + datetime.timedelta(seconds = alertoffset)
                    log.info('get_sunriseset_alert: process_emailalert startsunsetrise adjusted start >- sun rise times %s  :  %s  :  %s  ', alertoffset, sunrisetime, alertstarttime)

                #log.info('get_sunriseset_alert: process_emailalert compare sun set ->rise times alertduration %s  ', alertduration)



                #>currenttime 2017-10-21 14:55:11.008807-07:00  : sunrisetime 2017-10-21 07:37:32-07:00  :alertstarttime  2017-10-21 19:30:25.008807-07:00   
                # currenttime  2017-10-21 15:26:11.778414-07:00  :                   2017-10-21 07:37:32-07:00  :                       2017-10-21 02:00:25.778414-07:00
                #current time can be greater then sunset and greater then sunrise on current day
                # check for start time to sunrise
                # start time can be from sunset to midnight or from newday to sunrise
                if alerttype == "startsunrise":

                    #create timmer array
                    alertstartutcsecs = int(startutcsecs % (60*60*24))
                    log.info('get_sunriseset_alert: process_emailalert compare startsunrise->start times  utc seconds %s  ', alertstartutcsecs)
                    log.info('get_sunriseset_alert: process_emailalert compare startsunrise ->sunrise times  utc seconds %s  ', sunrise_utc_sec)

                    
                    alertaction_value = int(parameters.get('alertaction_value',255))
                    log.info('get_sunriseset_alert: process_emailalert compare startsunrise -> sunset alertaction_value %s  ', alertaction_value)
                    


                    #Timmer sunset to expires
                    if int(alertstartutcsecs) > int(sunrise_utc_sec):
                        log.info('get_sunriseset_alert: process_emailalert compare startsunrise -> alertstartutcsecs > sunrise_utc_sec  ')
                        for t_tenmin in range(0, 6*24):                           
                            if t_tenmin >= alertstartutcsecs/(10*60):
                                timmerArray[t_tenmin] = alertaction_value                                 
                            elif t_tenmin <= sunrise_utc_sec/(10*60):
                                timmerArray[t_tenmin] =alertaction_value    
                    else:
                        log.info('get_sunriseset_alert: process_emailalert compare startsunrise -> alertstartutcsecs < sunrise_utc_sec  ')
                        for t_tenmin in range(0, 6*24):
                            if t_tenmin >= alertstartutcsecs/(10*60) and t_tenmin <= sunrise_utc_sec/(10*60) :                                   
                                timmerArray[t_tenmin] =alertaction_value



                    log.info('get_sunriseset_alert: process_emailalert compare startsunrise -> timmerArray %s  ', timmerArray)

                    
                    # check if start time is from new day to sunrise


                    
                    if alertstarttime < sunrisetime:

                        alertstartsecs = int(time.mktime(alertstarttime.timetuple()) % (60*60*24))
                        sunrisesecs = int(time.mktime(sunrisetime.timetuple()) % (60*60*24))
                        log.info('get_sunriseset_alert: process_emailalert compare sunrisestart->start times  seconds %s  ', alertstartsecs)
                        log.info('get_sunriseset_alert: process_emailalert compare sunrisestart ->rise times  seconds %s  ', sunrisesecs)
                        alertaction_value = int(parameters.get('alertaction_value',255))
                        log.info('get_sunriseset_alert: process_emailalert compare sunrisestart -> sunrise alertaction_value %s  ', alertaction_value)
                        

                        
                        if   currenttime > newdaytime and currenttime >=  alertstarttime and  currenttime <  sunrisetime:
                            text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                            text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                            text_body = text_body + 'is low - ' + alerttype + ' = ' + str(currenttime) + " threshold: " + str(sunrisetime) + " timestamp is:" + timestamp + '\n'
                            result['status']="active"
                            log.info('get_sunriseset_alert: process_emailalert startsunrise sun is down and less then alertend time %s:%s  ', text_body, currenttime)
                        else:
                            result['status']="inactive"
                            text_body = "alert is inactive - current time is outside sunrise/sunset"
                            log.info('get_sunriseset_alert timmerday inactive startsunrise %s:%s  ', text_body, currenttime)

                    # if alertstarttime is greater then sunrise we could be between sunset and midnight on the previous day
                    # sunrise and sunset times are adjusted at midnight on each new day
                    # so if starttime is after sunrise then it has to run till sunrise on the following day
                    # for example if sunrise is at 7:00AM on 1/1/2010 and start time is set to 11:00PM
                    # it must run to midnight on 1/1/2010 and also from 00:00 AM to sunrise on 1/2/2010
                    #
                    if alertstarttime > sunrisetime:


                        alertstartsecs = int(time.mktime(alertstarttime.timetuple()) % (60*60*24))
                        sunrisesecs = int(time.mktime(sunrisetime.timetuple()) % (60*60*24))
                        log.info('get_sunriseset_alert: process_emailalert compare sunrisestart->start times  seconds %s  ', alertstartsecs)
                        log.info('get_sunriseset_alert: process_emailalert compare sunrisestart ->rise times  seconds %s  ', sunrisesecs)
                        alertaction_value = int(parameters.get('alertaction_value',255))
                        log.info('get_sunriseset_alert: process_emailalert compare sunrisestart -> sunrise alertaction_value %s  ', alertaction_value)
                        

                        
                        #current time can be between starttime and midmight
                        if currenttime > alertstarttime and currenttime < midnighttime :                                
                            text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                            text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                            text_body = text_body + 'is low - ' + alerttype + ' = ' + str(currenttime) + " threshold: " + str(sunrisetime) + " timestamp is:" + timestamp + '\n'
                            result['status']="active"
                            log.info('get_sunriseset_alert: process_emailalert startsunrise sun is down before midnight and great then alertstarttime  %s:%s  ', text_body, currenttime)

                        # keep alert active from midnight to sunrise on the next day
                        elif currenttime > newdaytime and  currenttime <  sunrisetime:                               
                            text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                            text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                            text_body = text_body + 'is low - ' + alerttype + ' = ' + str(currenttime) + " threshold: " + str(sunrisetime) + " timestamp is:" + timestamp + '\n'
                            result['status']="active"
                            log.info('get_sunriseset_alert: process_emailalert startsunrise sun is down after midnight and before sunrise  %s:%s  ', text_body, currenttime)                                        
                        else:
                            result['status']="inactive"
                            text_body = "alert is inactive - current time is outside sunrise/sunset"
                            log.info('get_sunriseset_alert timmerday inactive startsunrise %s:%s  ', text_body, currenttime)

                elif alerttype == "startsunset":
                    #only going to check for when start time is before sunset
                    # so we only run from new day to sunset and not after sunset

                    #create timmer array
                    alertstartutcsecs = int(startutcsecs % (60*60*24))
                    log.info('get_sunriseset_alert: process_emailalert compare startsunset->start times  utc seconds %s  ', startutcsecs)
                    log.info('get_sunriseset_alert: process_emailalert compare startsunset ->sunset times  utc seconds %s  ', sunset_utc_sec)

                    
                    alertaction_value = int(parameters.get('alertaction_value',255))
                    log.info('get_sunriseset_alert: process_emailalert compare startsunset -> sunset alertaction_value %s  ', alertaction_value)
                    


                    #Timmer sunset to expires
                    if alertstartutcsecs > sunset_utc_sec:
                        for t_tenmin in range(0, 6*24):                           
                            if t_tenmin >= alertstartutcsecs/(10*60):
                                timmerArray[t_tenmin] = alertaction_value                                 
                            elif t_tenmin <= sunset_utc_sec/(10*60):
                                timmerArray[t_tenmin] =alertaction_value    
                    else:
                        for t_tenmin in range(0, 6*24):
                            if t_tenmin >= alertstartutcsecs/(10*60) and t_tenmin <= sunset_utc_sec/(10*60) :                                   
                                timmerArray[t_tenmin] =alertaction_value



                    log.info('get_sunriseset_alert: process_emailalert compare startsunset -> timmerArray %s  ', timmerArray)
                    
                    if alertstarttime < sunsettime:

                        alertstartsecs = int(time.mktime(alertstarttime.timetuple()) % (60*60*24))
                        sunrisesecs = int(time.mktime(sunrisetime.timetuple()) % (60*60*24))
                        log.info('get_sunriseset_alert: process_emailalert compare sunrisestart->start times  seconds %s  ', alertstartsecs)
                        log.info('get_sunriseset_alert: process_emailalert compare sunrisestart ->rise times  seconds %s  ', sunrisesecs)
                        alertaction_value = int(parameters.get('alertaction_value',255))
                        log.info('get_sunriseset_alert: process_emailalert compare sunrisestart -> sunrise alertaction_value %s  ', alertaction_value)
                        

                        
                        if   currenttime > newdaytime and currenttime >=  alertstarttime and  currenttime <  sunsettime:
                            text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                            text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                            text_body = text_body + 'is low - ' + alerttype + ' = ' + str(currenttime) + " threshold: " + str(sunsettime) + " timestamp is:" + timestamp + '\n'
                            result['status']="active"
                            log.info('get_sunriseset_alert: process_emailalert startsunset sun is up and greater then alertstart time but les then sunset %s:%s  ', text_body, currenttime)
                        else:
                            result['status']="inactive"
                            text_body = "alert is inactive - current time is outside sunrise/sunset"
                            log.info('get_sunriseset_alert timmerday inactive startsunset %s:%s  ', text_body, currenttime)
                            
                    """
                    #if end time is less thne current sunset then it for the next day after midnight
                    if alertstarttime > sunsettime:
                        #current time can be before sunrise on the next day
                        if currenttime < midnighttime and  currenttime > alertstarttime :                                
                            text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                            text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                            text_body = text_body + 'is low - ' + alerttype + ' = ' + str(currenttime) + " threshold: " + str(sunsettime) + " timestamp is:" + timestamp + '\n'
                            result['status']="active"
                            log.info('get_sunriseset_alert: process_emailalert startsunsetrise sun is down alerttext %s:%s  ', text_body, currenttime)
                            
                        else:
                            result['status']="inactive"
                    """
             
        except ValueError as e:
            if debug_all: log.info('get_sunriseset_alert: ValueError in sunrise %s  ', text_body)
            if debug_all: log.info('get_sunriseset_alert: ValueError in sunrise %s:  ' % str(e))

        except NameError as e:
            if debug_all: log.info('get_sunriseset_alert: NameError in sunrise %s  ', text_body)
            if debug_all: log.info('get_sunriseset_alert: NameError in sunrise %s:  ' % str(e))

        except AttributeError as e:
            if debug_all: log.info('get_sunriseset_alert: AttributeError in sunrise %s  ', text_body)
            if debug_all: log.info('get_sunriseset_alert: AttributeError in sunrise %s:  ' % str(e))

        except TypeError as e:
            if debug_all: log.info('get_sunriseset_alert: TypeError in sunrise %s  ', text_body)
            if debug_all: log.info('get_sunriseset_alert: TypeError in sunrise %s:  ' % str(e))                     

            
        except:
            log.info('get_sunriseset_alert: Error3 in get sunrise-set %s  ', text_body)
            e = sys.exc_info()[0]

            log.info("Error3: %s" % e)
            result['status']="error 3"

    except ValueError as e:
        if debug_all: log.info('get_sunriseset_alert: ValueError in sunrise %s  ', text_body)
        if debug_all: log.info('get_sunriseset_alert: NameError in sunrise %s:  ' % str(e)) 
        
    except NameError as e:
        if debug_all: log.info('get_sunriseset_alert: NameError in sunrise %s  ', text_body)
        if debug_all: log.info('get_sunriseset_alert: NameError in sunrise %s:  ' % str(e))

    except AttributeError as e:
        if debug_all: log.info('get_sunriseset_alert: AttributeError in sunrise %s  ', text_body)
        if debug_all: log.info('get_sunriseset_alert: AttributeError in sunrise %s:  ' % str(e))

    except TypeError as e:
        if debug_all: log.info('get_sunriseset_alert: TypeError in sunrise %s  ', text_body)
        if debug_all: log.info('get_sunriseset_alert: TypeError in sunrise %s:  ' % str(e))                     

    except:
        if debug_all: log.info('get_sunriseset_alert: Error in get sunrise-set %s  ', text_body)
        e = sys.exc_info()[0]

        if debug_all: log.info("Error: %s" % e)
        
        result['status']="error1"

        
    result['message']=text_body
    result['timmerArray']=timmerArray
    return result


def get_status_alert(parameters, value):

    #initialize return
    result={}
    result['status']="error"
    result['message']=""

    timestamp = str(datetime.datetime.now())

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

    timestamp = str(datetime.datetime.now())
    
    text_body= "error in get_alarms alert"
    alerttype = parameters.get('alerttype',"mean")

    log.info("get_alarms_alert  deviceID: %s alerttype %s", parameters['deviceid'], alerttype)

    # extract the series alarm paramterts
    series_parameters = parameters.get('series_1',"")
    # check for errors
    if series_parameters == "":
        result['status']="error"
        result['message']="missing series parameters"
        return result


    try:


        
        #if alerttype == "missing":
        if value == "missing":
            text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
            text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
            text_body = text_body + "value is missing for Interval= " + parameters["Interval"] + " timestamp is:" + timestamp + '\n'

            if alerttype == "missing":
                result['status']="active"
            else :
                result['status']="inactive"
            
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

        
        if alerttype != "missing":               
            if str(series_parameters["alarmlow"]) != "off" :
                log.info("get_alarms_alert  low != off %s",  float(value), float(series_parameters["alarmhigh"]))
                try:
                    if float(value) <= float(series_parameters["alarmlow"]):
                        text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                        text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                        text_body = text_body + 'is low - ' + alerttype + ' = ' + str(value) + " threshold: " + str(series_parameters["alarmlow"]) + " timestamp is:" + timestamp + '\n'
                        result['status']="active"
                        #http://www.helmsmart.net/getseriesdatabykey?serieskey=deviceid:0018E78B5121.sensor:engine_parameters_dynamic.source:08.instance:1.type:NULL.parameter:engine_temp.HelmSmart&devicekey=2a4731ac48c80ee3b4c17e7d74a6825f&startepoch=1405065555&endepoch=1405094365&resolution=60&format=csv
                except:
                    result['status']="inactive"
                    if debug_all: log.info('get_alarms_alert: low Error  %s:%s  ', text_body, value)
                    e = sys.exc_info()[0]
                    if debug_all: log.info("Error: %s" % e)
            
            if str(series_parameters["alarmhigh"]) != "off" :
                #if value != "" or value != "missing" or value != "error":
                log.info("get_alarms_alert  high != off %s",  float(value), float(series_parameters["alarmhigh"]))
                try:
                    if float(value) >= float(series_parameters["alarmhigh"]):
                        text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                        text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                        text_body = text_body + 'is high - ' + alerttype + ' = ' + str(value) + " threshold: " + str(series_parameters["alarmhigh"]) + " timestamp is:" + timestamp + '\n'
                        result['status']="active"
                except:
                    result['status']="inactive"
                    if debug_all: log.info('get_alarms_alert: high Error  %s:%s  ', text_body, value)
                    e = sys.exc_info()[0]
                    if debug_all: log.info("Error: %s" % e)


            if str(series_parameters["alarmlow"]) == "off" and str(series_parameters["alarmhigh"]) == "off" :
                text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                text_body = text_body  + series_parameters["alarmmode"] + ": " + series_parameters["title"] + '\n'
                text_body = text_body + 'is = ' + str(value) + " threshold: " + str(series_parameters["alarmlow"]) + "/" + str(series_parameters["alarmhigh"])+ " timestamp is:" + timestamp + '\n'
                result['status']="status"
                result['message']=text_body                    

        result['message']=text_body
        return result

    except TypeError as e:
        if debug_all: log.info('get_alarms_alert: TypeError  %s:%s  ', text_body, value)
        if debug_all: log.info('get_alarms_alert: TypeError %s:  ' % str(e))

    except ValueError as e:
        if debug_all: log.info('get_alarms_alert: ValueError  %s:%s  ', text_body, value)
        if debug_all: log.info('get_alarms_alert: TypeError  %s:  ' % str(e))

    except AttributeError as e:
        if debug_all: log.info('get_alarms_alert: AttributeError %s:%s  ', text_body, value)
        if debug_all: log.info('get_alarms_alert: AttributeError %s:  ' % str(e))        
        
    except KeyError as e:
        if debug_all: log.info('get_alarms_alert: KeyError  %s:%s  ', text_body, value)
        if debug_all: log.info('get_alarms_alert: KeyError %s:  ' % str(e))

    except NameError as e:
        if debug_all: log.info('get_alarms_alert: NameError  %s:%s  ', text_body, value)
        if debug_all: log.info('get_alarms_alert: NameError  %s:  ' % str(e))     

    except:
        if debug_all: log.info('get_alarms_alert: Error  %s:%s  ', text_body, value)
        e = sys.exc_info()[0]

        if debug_all: log.info("Error: %s" % e)
        result['status']="error"
        result['message']='Error in geting get_alarms_alert'
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
