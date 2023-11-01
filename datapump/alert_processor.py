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


logging.basicConfig(level=logging.INFO)
log = logging

def get_timmer_alert(parameters, value):

    #initialize return
    result['message']=""
    result['status']="error"

    return result

def get_timmerday_alert(parameters, value):

    #initialize return
    result['message']=""
    result['status']="error"

    return result

  
def get_sunriseset_alert(parameters, value):

    #initialize return
    result['status']="error"

    return result

def get_status_alert(parameters, value):

    #initialize return
    result['status']="error"
    result['message']=""

    text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
    text_body = text_body  + parameters[series_number]["alarmmode"] + ": " + parameters[series_number]["title"] + '\n'
    text_body = text_body + 'is = ' + str(value) + " threshold: " + str(parameters[series_number]["alarmlow"]) + "/" + str(parameters[series_number]["alarmhigh"])+ " timestamp is:" + timestamp + '\n'
    result['status']="status"
    result['message']=text_body
    return result


def get_alarms_alert(parameters, value):

    #initialize return
    #result['status']="error"
    result['status']="inactive"
    result['message']=""

    alerttype = parameters.get('alerttype',"mean")
    
    if alerttype == "missing":
        if value == "missing":
            text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
            text_body = text_body  + parameters[series_number]["alarmmode"] + ": " + parameters[series_number]["title"] + '\n'
            text_body = text_body + "value is missing for Interval= " + parameters["Interval"] + " timestamp is:" + timestamp + '\n'
            result['status']="active"
            result['message']=text_body
        return result
            
    if alerttype == "error":
        if value == "error":
            text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
            text_body = text_body  + parameters[series_number]["alarmmode"] + ": " + parameters[series_number]["title"] + '\n'
            text_body = text_body + "value error for Interval= " + parameters["Interval"] + " timestamp is:" + timestamp + '\n'
            result['status']="active"
            result['message']=text_body
        return result
            
    if str(parameters['series_1']["alarmlow"]) != "off" :
        try:
            if float(value) <= float(parameters['series_1']["alarmlow"]):
                text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                text_body = text_body  + parameters[series_number]["alarmmode"] + ": " + parameters[series_number]["title"] + '\n'
                text_body = text_body + 'is low - ' + alerttype + ' = ' + str(value) + " threshold: " + str(parameters[series_number]["alarmlow"]) + " timestamp is:" + timestamp + '\n'
                result['status']="active"
                #http://www.helmsmart.net/getseriesdatabykey?serieskey=deviceid:0018E78B5121.sensor:engine_parameters_dynamic.source:08.instance:1.type:NULL.parameter:engine_temp.HelmSmart&devicekey=2a4731ac48c80ee3b4c17e7d74a6825f&startepoch=1405065555&endepoch=1405094365&resolution=60&format=csv
        except:
            result['status']="inactive"
    
    
    if str(parameters[series_number]["alarmhigh"]) != "off" :
        #if value != "" or value != "missing" or value != "error":
        try:
            if float(value) >= float(parameters['series_1']["alarmhigh"]):
                text_body = text_body + '\n' + parameters['devicename'] + " ALARM Message \n"
                text_body = text_body  + parameters[series_number]["alarmmode"] + ": " + parameters[series_number]["title"] + '\n'
                text_body = text_body + 'is high - ' + alerttype + ' = ' + str(value) + " threshold: " + str(parameters[series_number]["alarmhigh"]) + " timestamp is:" + timestamp + '\n'
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


    log.info('alert_processor:process_emailalert start: %s :', parameters)

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
            
        #check if alarm mode is specified
        alarmmode = str(series_parameters["alarmmode"])

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


            #timmer event once only
            if alerttype == "timmer":

                #create timmer array of dimmer values based on start and stop times            
                result = get_timmer_alert(sparameters, value)

            #timmer event daily repeat
            elif alerttype == "timmerday":
                #create timmer array of dimmer values based on start and stop times            
                result = get_timmerday_alert(parameters, value)                

            #timmer event based on local sunrise sunset
            elif alerttype == "sunriseset" or alerttype == "sunsetrise" or alerttype == "sunriseexpires" or alerttype == "sunsetexpires" or alerttype == "startsunrise" or alerttype == "startsunset":
                log.info('alert_processor: get location %s  : %s', parameters[series_number]["alarmlow"], parameters[series_number]["alarmhigh"])

                #use location to determine sunrise and sunset times
                result = get_sunriseset_alert(parameters, value)


        # to do - need to handle serires status        
        elif str(parameters['series_1']["alarmmode"]) == "status":
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
