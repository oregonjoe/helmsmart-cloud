import os
import requests
import sys
import base64
import json
import logging
import datetime
import time
import pytz
from pytz import utc
from time import mktime
from array import *
#from astral import *
#from astral import GoogleGeocoder

# *******************************************************************
# Debug Output defines
# Comment to enable/disable
# ********************************************************************
debug_all = False
debug_all = True


requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)

#logging.disable(logging.CRITICAL)
logging.basicConfig(level=logging.INFO)
log = logging

"""
from warehouse import connection_from

from psycopg2.pool import ThreadedConnectionPool
db_pool = ThreadedConnectionPool(
  1, # min connections,
  int(os.environ.get('MAX_DB_CONNECTIONS',13)),
  **connection_from(os.environ['DATABASE_URL'])
)
"""

from psycopg_pool import ConnectionPool
#db_pool = ThreadedConnectionPool( 1,  **connection_from(os.environ['DATABASE_URL']))
#db_pool = ConnectionPool( 1,  **connection_from(os.environ['DATABASE_URL']))
db_pool = ConnectionPool(os.environ.get('DATABASE_URL'))
#db_pool = ConnectionPool(os.environ.get('HEROKU_POSTGRESQL_MAUVE_URL'))

SECOND30 = 255
MINUTE1 = 0
MINUTE2 = 1
MINUTE5 = 2
MINUTE10 = 3
MINUTE15 = 4
MINUTE30 = 5
HOUR1 = 6
HOUR4 = 7
HOUR6 = 8
HOUR8 = 9
HOUR12 = 10
DAY1 = 11
WEEK1 = 12
MONTH1 = 13


APP = "pushsmartdata"
KEY = "cc7a7004-5c8b-46a5-b53a-fdd683aa10f2"
PROCESS = "web"
DYNO = "poller.1"

"""
# Generate Base64 encoded API Key
BASEKEY = base64.b64encode(":" + KEY)
# Create headers for API call
HEADERS = {
    "Accept": "application/vnd.heroku+json; version=3",
    "Authorization": BASEKEY
}

"""


from rq import Queue
from worker import conn

q = Queue(connection=conn)

from messagepost import process_message

#from apscheduler.scheduler import Scheduler
from apscheduler.schedulers.background import BackgroundScheduler


import botocore
import boto3
# Get the service resource
#sqs = boto3.resource('sqs')
#s3 = boto3.resource(service_name='sqs', region_name='REGION_NAME')

sqs_queue = boto3.client('sqs', region_name='us-east-1', aws_access_key_id=environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY'))

#queue_url = 'SQS_QUEUE_URL'
#queue_url = 'https://sqs.us-east-1.amazonaws.com/291312677175/helmsmart-cloud'
#queue_url = 'https://sqs.us-east-1.amazonaws.com/291312677175/SeaSmart'
#queue_url = os.environ.get('SQS_QUEUE_URL')
queue_url = os.environ.get('SQS_QUEUE_ALERTS_URL')

#Put Alert message in SQS que for processing
def put_SQS_Message(message_json):
    if debug_all: log.info('put_SQS_Message')

    try:
    # ######################################################
    # now place in SQS queue
    # #######################################################
    # Send message to SQS queue
    response = sqs_queue.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        #MessageAttributes={ 'Device': {  'deviceid':device_id} },
        MessageBody=(message_json)
    )

    #print(response['MessageId'])

    log.info("Send SQS:device_id %s:  response %s: ", device_id,response['MessageId'])

    except botocore.exceptions.ClientError as e:
    log.info("Send SQS:ClientError device_id %s:  ", device_id)
    log.info('Send SQS:ClientError  Error in que SQS %s:  ' % e)

    except botocore.exceptions.ParamValidationError as e:
    log.info("Send SQS:ParamValidationError device_id %s:  ", device_id)
    log.info('Send SQS:ParamValidationError  Error in que SQS %s:  ' % e)

    except NameError as e:
    log.info("Send SQS:NameError device_id %s:  ", device_id)
    log.info('Send SQS:NameError  Error in que SQS %s:  ' % e)    

    except:
    e = sys.exc_info()[0]
    log.info("Send SQS:device_id %s:  ", device_id)
    log.info('Send SQS: Error in que SQS %s:  ' % e)



#this is called from the CRON scheduler every 30 seconds
#Interval is passed into SQL query to find tasks that meet the schedule
def get_HS_Message(interval):
    if debug_all: log.info('Push_Scheduler job fired --')

    conn = db_pool.getconn()   

    
    # look for single shot messages every 30 seconds
    if interval == 255:
        query = "select messagekey, startdatetime, enddatetime, interval, message_json from post_messages where repeat = %s"
        myParameter = 0
    # fire repeated messages based on intervals
    else:
        query = "select messagekey, startdatetime, enddatetime, interval, message_json from post_messages where Interval = %s"
        myParameter = interval

    alert_message = {}
    messagekeys = []
    
    try:
        
        # query db to get matching messages to invervals
        cursor = conn.cursor()
        cursor.execute(query, (myParameter,) )

        records = cursor.fetchall()
            
        for row in records:
            if debug_all: log.info('Push_Scheduler key= %s start=%s end=%s', row[0], row[1], row[2])
            try:            
                starttime = int(row[1])
                endtime = int(row[2])
                myinterval = int(row[3])
                    
                if myinterval == 0:
                    interval_increment = 60
                elif myinterval == 1:
                    interval_increment = 60*2                    
                elif myinterval == 2:
                    interval_increment = 60*5
                elif myinterval == 3:
                    interval_increment = 60*10
                elif myinterval == 4:
                    interval_increment = 60*15
                elif myinterval == 5:
                    interval_increment = 60*30
                elif myinterval == 6:
                    interval_increment = 60*60
                elif myinterval == 7:
                    interval_increment = 60*60*4
                elif myinterval == 8:
                    interval_increment = 60*60*6
                elif myinterval == 9:
                    interval_increment = 60*60*8
                elif myinterval == 10:
                    interval_increment = 60*60*12
                elif myinterval == 11:
                    interval_increment = 60*60*24
                elif myinterval == 12:
                    interval_increment = 60*60*24*7
                elif myinterval == 13:
                    interval_increment = 60*60*24*30
                else:
                    interval_increment = 60*5


                # if start and end times are nonzero, we are going to que up a bunch of messages based on the interval
                # and send them on so we perform batch log updates
                # Used mainly for BoatLogger so we can import logs from SD upload

                if int(starttime) != 0 and int(endtime) !=0:
                    # loop through and create a new message based on log time increment
                    #messagekeys.append(int(row[0]))
                    
                    currenttime = datetime.datetime.now()
                    currentsecs = int(time.mktime(currenttime.timetuple()))
                    log.info('Push_Scheduler  timmer currentsecs %s  ', currentsecs)

                    
                    loopcount = 0
                    #while starttime < endtime and loopcount < 500:
                    if int(starttime) <= currentsecs and currentsecs < int(endtime) :
                        alert_message['key'] = row[0]
                        alert_message['starttime'] = starttime
                        alert_message['endtime'] = endtime
                        alert_message['parameters'] = json.loads(row[4])
    
                        #myresult = q.enqueue(process_message, alert_message, ttl=10000)
                        put_SQS_Message(alert_message):
                       
                        log.info('Push_Scheduler inserted logged messages %s:%s -- %s', starttime, endtime, alert_message)

                        
                else:  
                    alert_message['key'] = row[0]
                    #alert_message['starttime'] = 0
                    alert_message['starttime'] = starttime
                    alert_message['endtime'] = 0
                    alert_message['parameters'] = json.loads(row[4])
                    alerttype = alert_message['parameters'].get('alerttype',"")
                    alertseries = alert_message['parameters'].get('series_1',"")
                    alertend =alertseries.get('alarmhigh',"")
                    alertendutc =alert_message['parameters'].get('alertendtime_utc',"")
                    alertlocationcity =alert_message['parameters'].get('locationcity',"")

                    currenttime = datetime.datetime.now()
                    currentsecs = int(time.mktime(currenttime.timetuple()))
                    log.info('Push_Scheduler  timmer currentsecs %s  ', currentsecs)
                    # check if we have a alertendtime_utc value and use it
                    # otherwise use defaults
                    if alertendutc != "":
                        alertend = int(alertendutc)
                        
                    elif alertend == "":
                        alertend = currentsecs

                        
                    if debug_all: log.info('Push_Scheduler before insert realtime messages alerttype %s  alertend %s', alerttype, alertend)

                    if alerttype == 'timmer':
                        # if we have location thne we use local time
                        if alertlocationcity != "":
                            a = Astral()

                            if alertlocationcity == 'Brookings':
                                
                                location = a['Seattle']
                                location.name = 'Brookings'
                                """                                
                                location.name = 'Brookings'
                                location.region = 'US'
                                location.timezone = 'US/Pacific'
                                location.latitude = 42.05
                                location.longitude = -124.27
                                log.info("getSunRiseSet:  in proc getSunRiseSet Astral location: %s", location)
                                """        

                            else:
                                location = a[alertlocationcity]
                            
                            if debug_all: log.info("Push_Scheduler one shot timmer :  in  Astral location: %s", location)
                            
                            timezone = location.timezone
                            log.info("Push_Scheduler one shot timmer :  in  Astral timezone: %s", timezone)
                            mylocal = pytz.timezone(timezone)
                            #need to make time value timezone aware
                            utccurrenttime = pytz.utc.localize(currenttime)
                            if debug_all: log.info('Push_Scheduler one shot timmer :  timmer once utccurrenttime secs %s  ', utccurrenttime)  
                            
                            # adjust time to sunset/sunrise local time
                            localcurrenttime = utccurrenttime.astimezone(mylocal)

                            currenttime = localcurrenttime

                            if debug_all: log.info('Push_Scheduler one shot timmer :  timmer once localcurrenttime %s  ', currenttime)

                            #now remove timezone info so we can compare to start and end times
                            currenttime = currenttime.replace(tzinfo=None)
                            log.info('Push_Scheduler one shot timmer : timmer once currenttime without timezone info %s  ', currenttime)
                            
                            currentsecs = int(time.mktime(currenttime.timetuple()))
                        
                        if debug_all: log.info('Push_Scheduler one shot timmer currentsecs %s  alertend %s', currentsecs, alertend)
                        if int(currentsecs) > int(alertend):
                            # Delete Key
                            messagekeys.append(int(row[0]))
                            if debug_all: log.info('Push_Scheduler one shot timmer messagekeys %s', messagekeys)
                            #log.info('Push_Scheduler one shot timmer messagekeys %s', int(row[0]))
                            #messagekeys.append(int(row[0]))
                    
                    #071214 JLB added message to que for the worker (post) to process
                    
                    #myresult = q.enqueue(process_message, alert_message, ttl=10000)
                    put_SQS_Message(alert_message):
                    if debug_all: log.info('Push_Scheduler inserted realtime messages %s', alert_message)
                    
            except NameError as e:
                if debug_all: log.info('Push_Scheduler: queing message NameError  %s:  ' % str(e))
                
            except KeyError as e:
                if debug_all: log.info('Push_Scheduler: queing message KeyError  %s:  ' % str(e))
                
            except TypeError as e:
                if debug_all: log.info('Push_Scheduler: queing message TypeError  %s:  ' % str(e))
                
            except:
                if debug_all: log.info('ERROR: Push_Scheduler queing message ')
                e = sys.exc_info()[0]
                if debug_all: log.info("Error: %s" % e) 
                pass
        
        try:
            
            for key in messagekeys:
                if debug_all: log.info('Push_Scheduler deleting message %s', key)
                query = "delete from post_messages where messagekey = %s;"
                cursor.execute(query, (key,) )
                conn.commit()
                
        except:
            if debug_all: log.info('ERROR: Push_Scheduler deleting messages ')
            e = sys.exc_info()[0]
            if debug_all: log.info("Error: %s" % e) 
            pass
        
        
        if debug_all: log.info('Push_Scheduler completed pass ')
        db_pool.putconn(conn)

    except NameError as e:
        if debug_all: log.info('Push_Scheduler: NameError  %s:  ' % str(e))
        pass
    
    except:
        if debug_all: log.info('ERROR: Push_Scheduler database search error ')
        e = sys.exc_info()[0]

        if debug_all: log.info("Error: %s" % e)        
        #conn.rollback()
        db_pool.putconn(conn,close=True)
        #raise
        pass



#sched = Scheduler()
#sched = BackgroundScheduler()

#@sched.cron_schedule(second='30')
#def timed_job_30s():
#    print 'This job is run every 30 seconds.'
#    get_HS_Message(SECOND30)
    
#@sched.cron_schedule(minute='*')
#@sched.cron_schedule(minute='1,2,3,4,6,7,8,9,11,12,13,14,16,17,18,19,21,22,23,24,26,27,28,29,31,32,33,34,36,37,38,39,41,42,43,44,46,47,48,49,51,52,53,54,56,57,58,59')
def timed_job_1m():
    r = requests.get('http://pushsmart-tcpserver.herokuapp.com/')

    print('This job is run every 1 minutes.')
    get_HS_Message(MINUTE1)

#@sched.cron_schedule(minute='2,4,6,7,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58')
def timed_job_2m():
    r = requests.get('http://pushsmart-tcpserver.herokuapp.com/')

    print('This job is run every 2 minutes.')
    get_HS_Message(MINUTE2)
    
#@sched.cron_schedule(minute='0,5,10,15,20,25,30,35,40,45,50,55')
def timed_job_5m():
    r = requests.get('http://pushsmart-nodejs-test.herokuapp.com/')
    
    print("I was fired every 5 minutes")
    get_HS_Message(MINUTE5)

#@sched.cron_schedule(minute='0,10,20,30,40,50')
def timed_job_10m():
    print("I was fired every 10 minutes")
    if debug_all: log.info('Push_Scheduler: fired every 10 minutes')
#$ curl -n -X DELETE https://api.heroku.com/apps/$APP_ID_OR_NAME/dynos/$DYNO_ID_OR_NAME \
#-H "Accept: application/vnd.heroku+json; version=3"

    #payload = {'quantity': size}
    payload = {}
    json_payload = json.dumps(payload)
    #url = "https://api.heroku.com/apps/" + APP + "/formation/" + PROCESS
    url = "https://api.heroku.com/apps/" + APP + "/dynos/" + DYNO


    """
    try:
        #result = requests.patch(url, headers=HEADERS, data=json_payload)
        result = requests.delete(url, headers=HEADERS, data=json_payload)
    except:
        #print "test!"
        if debug_all: log.info('Push_Scheduler: Restart dyno error')
        e = sys.exc_info()[0]

        if debug_all: log.info("Push_Scheduler: Restart dyno error %s" % e)        

        #return None
    if result.status_code == 200 or result.status_code == 202:
        if debug_all: log.info('Push_Scheduler: Restart dyno SUCCESS ')
        #return "Success!"
    else:
        #return "Failure"
        if debug_all: log.info('Push_Scheduler: Restart dyno FAILURE %s', result.status_code)
        if debug_all: log.info('Push_Scheduler: Restart dyno FAILURE %s', result.text)
    """
    
    
    get_HS_Message(MINUTE10)

#@sched.cron_schedule(minute='0,15,30,45')
def timed_job_15m():
    print("I was fired every 15 minutes")
    get_HS_Message(MINUTE15)
    
#@sched.cron_schedule(minute='0,30')
def timed_job_30m():
    print("I was fired every 30 minutes")
    get_HS_Message(MINUTE30)
    
#@sched.cron_schedule(hour='*')
def timed_job_1h():
    print("I was fired every 1 hour")
    get_HS_Message(HOUR1)
    
#@sched.cron_schedule(hour='0,4,8,12,16,20')
def timed_job_4h():
    print("I was fired every 4 hour")
    get_HS_Message(HOUR4)
    
#@sched.cron_schedule(hour='0,6,12,18')
def timed_job_6h():
    print("I was fired every 6 hour")
    get_HS_Message(HOUR6)
    
#@sched.cron_schedule(hour='0,8,16')
def timed_job_8h():
    print("I was fired every 8 hour")
    get_HS_Message(HOUR8)

#@sched.cron_schedule(hour='0,12')
def timed_job_12h():
    print("I was fired every 12 hour")
    get_HS_Message(HOUR12)
    
#@sched.cron_schedule(day='*')
def timed_job_1d():
    print("I was fired every 1 day")
    get_HS_Message(DAY1)
    
#@sched.cron_schedule(week='*')
def timed_job_1w():
    print("I was fired every week")
    get_HS_Message(WEEK1)
                     
#@sched.cron_schedule(month='*')
def timed_job_1M():
    print("I was fired every month")
    get_HS_Message(MONTH1)
                     


if __name__ == '__main__':
    
    sched = BackgroundScheduler()
    sched.configure(timezone=utc)
    
    if debug_all: log.info('START: Push_Scheduler adding jobs ')
    sched.add_job(timed_job_1m, 'cron', minute='*')
    sched.add_job(timed_job_2m, 'cron', minute='2,4,6,7,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58')
    sched.add_job(timed_job_5m, 'cron', minute='0,5,10,15,20,25,30,35,40,45,50,55')
    sched.add_job(timed_job_10m, 'cron', minute='0,10,20,30,40,50')
    sched.add_job(timed_job_15m, 'cron', minute='0,15,30,45')
    sched.add_job(timed_job_30m, 'cron', minute='0,30')
    sched.add_job(timed_job_1h, 'cron', hour='*')
    sched.add_job(timed_job_4h, 'cron', hour='0,4,8,12,16,20')
    sched.add_job(timed_job_6h, 'cron', hour='0,6,12,18')
    sched.add_job(timed_job_8h, 'cron', hour='0,8,16')
    sched.add_job(timed_job_12h, 'cron', hour='0,12')
    sched.add_job(timed_job_1d, 'cron', day='*')
    sched.add_job(timed_job_1w, 'cron', week='*')
    sched.add_job(timed_job_1M, 'cron', month='*')                          
        
    sched.start()

    # This is here to simulate application activity (which keeps the main thread alive).
    while True:
        time.sleep(5)
    
