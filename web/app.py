import os
from os import environ
from os import environ as env, path
#import pylibmc
import bmemcached
import sys
import re
#import pyarrow as pa
import json


#import md5
import hmac
import hashlib
import base64
from operator import itemgetter
from itertools import groupby

import requests
from requests.exceptions import HTTPError

import urllib 
#from urlparse import urlparse
from urllib.parse import urlparse,urlencode, quote_plus
import psycopg


from calendar import timegm
import datetime
from datetime import timezone
from dateutil.relativedelta import relativedelta
from datetime import date

import time
from time import mktime
from zoneinfo import ZoneInfo

#import pytz
#from pytz import timezone

#from geopy.distance import vincenty
from geopy.distance import geodesic


from influxdb.influxdb08 import InfluxDBClient

from influxdb import InfluxDBClient as InfluxDBCloud
from influxdb.client import InfluxDBClientError

from influxdb_client_3 import InfluxDBClient3, Point, WriteOptions


#from flask_awscognito import AWSCognitoAuthentication

from flask_cognito_lib import CognitoAuth
from flask_cognito_lib.decorators import (
    auth_required,
    cognito_login,
    cognito_login_callback,
    cognito_logout,
)


from flask_awscognito import AWSCognitoAuthentication


#import dashboard_routes
import botocore
import boto3
from botocore.exceptions import ClientError
# Get the service resource
#sqs = boto3.resource('sqs')
#s3 = boto3.resource(service_name='sqs', region_name='REGION_NAME')

sqs_queue = boto3.client('sqs', region_name=os.environ.get('AWS_REGION'), aws_access_key_id=environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY'))

#queue_url = 'SQS_QUEUE_URL'
#queue_url = 'https://sqs.us-east-1.amazonaws.com/291312677175/helmsmart-cloud'
#queue_url = 'https://sqs.us-east-1.amazonaws.com/291312677175/SeaSmart'
queue_url = os.environ.get('SQS_POSTS_URL')
alerts_queue_url = os.environ.get('SQS_ALERTS_URL')
psraw_queue_url = os.environ.get('SQS_PSRAW_URL')
#queue = boto3.connect_sqs().lookup(os.environ['SQS_QUEUE'])
#queue = boto3.connect_sqs().lookup('SeaSmart')

#email_ses_client = boto3.client('ses', aws_access_key_id=environ.get('AWS_ACCESS_KEY_ID'),  aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY'), region_name="us-east-2"  )
email_ses_client = boto3.client('ses', aws_access_key_id=environ.get('AWS_ACCESS_KEY_ID'),  aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY'), region_name="us-west-2"  )
sms_ses_client = boto3.client('sns', aws_access_key_id=environ.get('AWS_ACCESS_KEY_ID'),  aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY'), region_name="us-west-2"  )

import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import logging
# *******************************************************************
# Debug Output defines
# Comment to enable/disable
# ********************************************************************
#debug_all = False
debug_all = True
debug_info = True
debug_memcachier = False


#import helmsmartmodules.nmearemote_functions as nmearemote_functions
#from helmsmartmodules import user_db_functions
#from helmsmartmodules.user_db_functions import getdashboardlists
import helmsmartmodules.user_db_functions as user_db_functions
import datapump.nmearemote_functions as nmearemote_functions

#import datapump.signalk.createSIGKpath as createSIGKpath
#import datapump.signalk.parseSIGK as parseSIGK

import datapump.nmea as nmea
import datapump.signalk as signalk
import datapump.seagaugeg4 as seagaugeg4
#from signalk import createSIGKpath, parseSIGK


#from helmsmartmodules import user_db_functions

from splicer import Schema
SCHEMA=Schema([
  dict(name="device",type='STRING'),
  dict(name="partition",type='STRING'),
  dict(name="url",type='STRING'),
]+nmea.SCHEMA.fields)

requests_log = logging.getLogger("requests")
#requests_log.setLevel(logging.WARNING)
#requests_log.setLevel(logging.INFO)
requests_log.setLevel(logging.DEBUG)
#logging.disable(logging.DEBUG)

logging.basicConfig(level=logging.INFO)  
#logging.basicConfig(level=logging.DEBUG)
log = logging






#from flask import Flask
from flask import (
  Flask,
  session,
  render_template,
  url_for,
  make_response,
  Response,
  stream_with_context,
  redirect,
  request,  
  jsonify
)



from flask_socketio import SocketIO, emit


#from flask.ext.cors import CORS, cross_origin
from flask_cors import CORS, cross_origin


def connection_from(url):
  #config = urlparse.urlparse(url)
  config = urlparse(url)
  return dict(
    host=config.hostname, 
    port=config.port, 
    dbname=config.path[1:],
    user=config.username,
    password=config.password
  )


#from psycopg.pool import ThreadedConnectionPool
from psycopg_pool import ConnectionPool
#db_pool = ThreadedConnectionPool( 1,  **connection_from(os.environ['DATABASE_URL']))
#db_pool = ConnectionPool( 1,  **connection_from(os.environ['DATABASE_URL']))
db_pool = ConnectionPool(os.environ.get('DATABASE_URL'), timeout=90)
#db_pool = ConnectionPool(os.environ.get('HEROKU_POSTGRESQL_GOLD_URL'))
#db_pool = ConnectionPool(os.environ.get('HEROKU_POSTGRESQL_MAUVE_URL'))
#app = Flask(__name__)


app = Flask(__name__)
CORS(app) 
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['DEBUG'] = True
app.debug = True

#app.secret_key = 'super secret key'
app.secret_key = 'J0Zr27j/3yX L~SMP!jmN]CDI/,?RB'
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app)
#socketio = SocketIO(app,debug=True,cors_allowed_origins='*',async_mode='eventlet')


#app.add_url_rule('/dashboard', view_func=dashboard_routes.dashboard)

#sess.init_app(app)
#Adding auth0
#from auth0.v3.authentication import GetToken
#from auth0.v3.authentication import Users
# this is a new API 4/30/23
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

AUTH0_CALLBACK_URL = environ.get('AUTH0_CALLBACK_URL')
AUTH0_CLIENT_ID = environ.get('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = environ.get('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = environ.get('AUTH0_DOMAIN')

# this is a new API 4/30/23

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=environ.get("AUTH0_CLIENT_ID"),
    client_secret=environ.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

# end of auth0 init

app.config["AWS_DEFAULT_REGION"] = environ.get("AWS_REGION")
app.config["AWS_REGION"] = environ.get("AWS_REGION")
app.config["AWS_COGNITO_DOMAIN"] = environ.get("AWS_COGNITO_DOMAIN")
app.config["AWS_COGNITO_USER_POOL_ID"] = environ.get("AWS_COGNITO_USER_POOL_ID")
app.config["AWS_COGNITO_USER_POOL_CLIENT_ID"] = environ.get("AWS_COGNITO_USER_POOL_CLIENT_ID")
app.config["AWS_COGNITO_USER_POOL_CLIENT_SECRET"] = environ.get("AWS_COGNITO_USER_POOL_CLIENT_SECRET")
app.config["AWS_COGNITO_REDIRECT_URL"] = environ.get("AWS_COGNITO_REDIRECT_URL")

aws_auth = AWSCognitoAuthentication(app)

cognito = CognitoAuth(app)

cognito_client = boto3.client('cognito-idp',  region_name="us-west-2"  )






#from authlib.integrations.flask_client import OAuth


oauth_aws_admin = OAuth(app)


oauth_aws_admin.register(
  name='oidc',
  authority=environ.get("AWS_COGNITO_ADMIN_ISSUER_URL"),
  client_id=environ.get("AWS_COGNITO_ADMIN_POOL_CLIENT_ID"),
  client_secret=environ.get("AWS_COGNITO_ADMIN_POOL_CLIENT_SECRET"),
  server_metadata_url=environ.get("AWS_COGNITO_ADMIN_ISSUER_URL") + '/.well-known/openid-configuration',
  #max_age=0,
  client_kwargs={'scope': 'aws.cognito.signin.user.admin phone openid email'}
)

"""

oauth_aws.register(
  name='oidc',
  authority='https://cognito-idp.us-west-2.amazonaws.com/us-west-2_znf559qHG',
  client_id='46b1d86tgbv072ikdg4qh11ddo',
  client_secret="",
  server_metadata_url='https://cognito-idp.us-west-2.amazonaws.com/us-west-2_znf559qHG/.well-known/openid-configuration',
  max_age=0,
  client_kwargs={'scope': 'phone openid email'}
)

"""


#max_age: 0
"""
mcservers = os.environ.get('MEMCACHIER_SERVERS', '').split(',')
mcuser = os.environ.get('MEMCACHIER_USERNAME', '')
mcpass = os.environ.get('MEMCACHIER_PASSWORD', '')

mc = pylibmc.Client(mcservers, binary=True,
                    username=mcuser, password=mcpass,
                    behaviors={
                      # Faster IO
                      "tcp_nodelay": True,

                      # Keep connection alive
                      'tcp_keepalive': True,

                      # Timeout for set/get requests
                      'connect_timeout': 2000, # ms
                      'send_timeout': 750 * 1000, # us
                      'receive_timeout': 750 * 1000, # us
                      '_poll_timeout': 2000, # ms

                      # Better failover
                      'ketama': True,
                      'remove_failed': 1,
                      'retry_timeout': 2,
                      'dead_timeout': 30,
                    })


"""

mcservers = os.environ.get('MEMCACHIER_SERVERS', '').split(',')
mcuser = os.environ.get('MEMCACHIER_USERNAME', '')
mcpassw = os.environ.get('MEMCACHIER_PASSWORD', '')

mc = bmemcached.Client(mcservers, username=mcuser, password=mcpassw)

mc.enable_retry_delay(True)  # Enabled by default. Sets retry delay to 5s.

"""
def get_xml_value(postdata, tag):

  startStr = "<" + tag + ">";
  endStr = "</" + tag + ">";
  startPos = -1
  endPos = -1

  #log.info("get_xml_value startStr %s  endStr %s", startStr, endStr )  

  startPos = postdata.find(startStr)
  #log.info("get_xml_value startPos %s ", startPos )  
  if startPos == -1:
    return ""

  startPos = startPos + len(startStr)

  endPos = postdata.find(endStr)
  #log.info("get_xml_value endPos %s", endPos )  
  if endPos == -1:
    return ""

  return postdata[startPos:endPos]

"""


class DateEncoder(json.JSONEncoder):
  def default(self, obj):
    if hasattr(obj, 'isoformat'):
      return obj.isoformat()
    else:
      return str(obj)


# Application routes for web server


#@app.route("/")
#def hello_world():
#    return "<p>Hello, Joe World 4!</p>"

def get_secret_hash(username, client_id, client_secret):
    """
    Calculates the SECRET_HASH for AWS Cognito authentication.

    :param username: The username of the user.
    :param client_id: The App Client ID from the Cognito User Pool.
    :param client_secret: The App Client Secret from the Cognito User Pool.
    :return: The Base64-encoded SECRET_HASH.
    """
    msg = username + client_id
    dig = hmac.new(client_secret.encode('utf-8'), 
                  msg.encode('utf-8'), 
                  hashlib.sha256).digest()
    return base64.b64encode(dig).decode('utf-8')


def dump_json(schema, records):
  field_pos = list(enumerate(schema.fields[3:]))
  
  def to_dict(record):
 
    data =  {
      f.name:record[i]
      for i,f in field_pos[:3]
    }

    for i,f in field_pos[3:]:
      v = record[i]
      if v:
        data['payload'] = v
        data['description'] = f.name
        return data



  data = [to_dict(r) for r in records]
  #if debug_all: log.info('data =  %s ', data)
  return json.dumps(data, cls=DateEncoder)


@app.route('/')
@cross_origin()
def index():

    log.info("index.html: Start")
    #log.info("index.html: session %s", session)
      
    try:
      
      if session['profile'] is not None:
        try:
          mydata = session['profile']
          log.info("index.html: customdata:%s", mydata)
         

          if mydata['name'] is not None:
            #myusername = mydata['name']
            myusername = mydata['email']
            log.info("index.html: myusername:%s", myusername)


          """
          if mydata['devices'] is not None:
            mydevices = mydata['devices']
            log.info("index.html: mydevices:%s", mydevices)

            for device in mydevices:
              log.info("index.html: mydevice  %s:%s", device['devicename'], device['deviceid'])
          """
          
        except:
          e = sys.exc_info()[0]
          log.info('index.html: Error in geting user.custom_data  %s:  ' % str(e))
          pass

        try:
          if myusername is not None:

            conn = db_pool.getconn()
            session['username'] = myusername
            
            log.info("index.html: email:%s", myusername )

            query = "select userid from user_devices where useremail = %s group by userid"

            cursor = conn.cursor()
            cursor.execute(query, [myusername])
            i = cursor.fetchone()       
            if cursor.rowcount > 0:

                session['userid'] = str(i[0])
                log.info('index.html: got user from database userid is  %s:  ' , session['userid'] )
                
            else:
                session['userid'] = hash_string('helmsmart@mockmyid.com')
                log.info('index.html: using default userid is  %s:  ' , session['userid'] )
                
            log.info('dashboards_list.html: userid is  %s:  ' , session['userid'] )
            # cursor.close
            db_pool.putconn(conn)
            
        except:
          e = sys.exc_info()[0]
          log.info('index.html: Error in geting user.email  %s:  ' % str(e))
          pass


        return render_template('index.html', user=session['profile'], env=env)
        #return render_template("authohome.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
      


    except TypeError as e:
      #log.info('dashboards_list: TypeError in  update pref %s:  ', userid)
      log.info('index: TypeError in  update pref  %s:  ' % str(e))

    except ValueError as e:
      #log.info('dashboards_list: ValueError in  update pref  %s:  ', userid)
      log.info('index: ValueError in  update pref %s:  ' % str(e))
      
    except KeyError as e:
      #log.info('dashboards_list: KeyError in  update pref  %s:  ', userid)
      log.info('index: KeyError in  update pref  %s:  ' % str(e))

    except NameError as e:
      #log.info('dashboards_list: NameError in  update pref  %s:  ', userid)
      log.info('index: NameError in  update pref %s:  ' % str(e))
          
    except IndexError as e:
      #log.info('dashboards_list: IndexError in  update pref  %s:  ', userid)
      log.info('index: IndexError in  update pref  %s:  ' % str(e))  

    except:
      e = sys.exc_info()[0]
      log.info('index.html: Error in geting user  %s:  ' % str(e))
      pass

    
    return render_template('index.html',  env=env)
    #return render_template("authohome.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

    #response = make_response(render_template('index.html', features = []))
    #response.headers['Cache-Control'] = 'public, max-age=0'
    #return response



@app.route('/nettimers') 
def nettimers():

  return render_template(
    'nettimers.html',
    features = [],
  )


@app.route('/netview')
def netview():

  return render_template(
    'netview.html',
    features = [],
  )

@app.route('/nethelm')
def nethelm():

  return render_template(
    'nethelm.html',
    features = [],
  )

@app.route('/netlog')
def netlog():

  return render_template(
    'netlog.html',
    features = [],
  )

"""
@app.route('/manage')
#@aws_auth.authentication_required
def manage():
  #claims = aws_auth.claims # also available through g.cognito_claims
  #return jsonify({'claims': claims})

  token = oauth_aws.oidc.authorize_access_token()
  user = token['userinfo']
  session['user'] = user

  return jsonify({'access_token': token, 'user': user})


"""

def aws_check_user_exists(username):

  log.info('aws_check_user_exists:start  ')
  
  UserPoolId=environ.get("AWS_COGNITO_USER_POOL_ID")
  
  log.info('aws_check_user_exists   UserPoolId %s: username %s:  ' , UserPoolId, username)

  
  try:
    
    cognito_client.admin_get_user(
          UserPoolId=UserPoolId,
          Username=username
      )

    log.info('aws_check_user_exists  - user already exist')      
    return True

    
  except cognito_client.exceptions.ResourceNotFoundException:
    log.info('aws_check_user_exists  - user dosnt exist')
    return False
  
  except cognito_client.exceptions.ParamValidationError:
    log.info('aws_check_user_exists  - ParamValidationError')
    return False

  except cognito_client.exceptions.UserNotFoundException:
    log.info('aws_check_user_exists  - UserNotFoundException')
    return False  

  except cognito_client.exceptions.UsernameExistsException:
    log.info("aws_check_user_exists: UsernameExistsException")
    return True
  
  except ClientError as e:
    log.info('aws_check_user_exists error:  %s:  ' % e)
    return False

  except:
    e = sys.exc_info()[0]
    log.info("aws_check_user_exists Error in checking username %s", username)
    log.info('aws_check_user_exists Error in checking username %s:  ' % e)
    return False

  
def aws_add_device(deviceid, devicename, useremail, smsemail, smsphone ):

  log.info('aws_add_device:start  ')  

  status = 1

  log.info('aws_add_device: deviceid %s  devicename %s:  ', deviceid, devicename)
  log.info('aws_add_device: useremail %s   ', useremail)
  log.info('aws_add_device: smsemail %s   ', smsemail)
  log.info('aws_add_device: smsphone %s   ', smsphone)

  conn = db_pool.getconn()


  userid=hash_string(useremail)
  log.info("aws_add_device- userid %s", userid)
  #deviceapikey=hash_string(userid+deviceid+"083019")
  deviceapikey=hash_string(userid+deviceid+"013024")
  log.info("aws_add_device - deviceapikey %s", deviceapikey)
  
  try:
    
    query  = "select deviceapikey from user_devices where useremail = %s and deviceid = %s"
    cursor = conn.cursor()

    cursor = conn.cursor()
    cursor.execute(query, ( useremail, deviceid))
    i = cursor.fetchone()       

    #no existing userid so need to use hashed email for userid and hashed deviceid for combined deviceapikey      
    if cursor.rowcount == 0:
      log.info("aws_add_device - deviceapikey does not exist so adding  deviceapikey %s", deviceapikey)
      userstatus = "dvice does not exist - adding"
      
      query  = "insert into user_devices ( deviceapikey, userid, useremail, deviceid, devicestatus, devicename, alertemail, smsnumber) Values (%s, %s, %s, %s, %s, %s, %s, %s)"



      # add new device record to DB
      cursor = conn.cursor()
      cursor.execute(query, (deviceapikey, userid, useremail, deviceid, status,  devicename, smsemail, smsphone))

      conn.commit()
        
      if cursor.rowcount == 0:
        userstatus = " Could not add user deviceid " + str(deviceid)
        return jsonify( message='Could not add device', status='error')
      
      userstatus = "new userid and deviceapikey added"
      return jsonify( message='Added user deviceid' , deviceapikey=deviceapikey, userstatus = userstatus )

    #userid exists so look up if deviceapikey has already been added
    else:
      userid= str(i[0])
      log.info("Add Device status userid  %s  already exists", userid )
      userstatus = "user already exists"
      return jsonify( message='Added user deviceid' , deviceapikey=deviceapikey, userstatus = userstatus )
    
  except TypeError as e:
    log.info("aws_add_device Device error -:TypeError deviceid %s ", deviceid)
    log.info('aws_add_device Device error -:TypeError  Error %s:  ' % e)
    return jsonify( message='Add user deviceid error - failed' , deviceapikey=deviceapikey, userstatus = "could not add deviceapikey" )

  except:
    e = sys.exc_info()[0]
    log.info("aws_add_device Device error - Error in adding device %s", deviceid)
    log.info('aws_add_device Device error: Error in adding device %s:  ' % e)
    return jsonify( message='Add user deviceid error - failed' , deviceapikey=deviceapikey, userstatus = "could not add deviceapikey" )
  
  finally:
    db_pool.putconn(conn)


def aws_update_device(deviceid, devicename, useremail, smsemail, smsphone, subscriptionKey, transactionID, devicestatus, email_verified, phone_verified ):

  log.info('aws_update_device:start  ')  

  #devicestatus = 1

  log.info('aws_update_device: deviceid %s  devicename %s:  ', deviceid, devicename)
  log.info('aws_update_device: useremail %s   ', useremail)
  log.info('aws_update_device: smsemail %s   ', smsemail)
  log.info('aws_update_device: smsphone %s   ', smsphone)
  log.info('aws_update_device: subscriptionkey %s   ', subscriptionKey)
  log.info('aws_update_device: transactionID %s   ', transactionID)
  log.info('aws_update_device: devicestatus %s   ', devicestatus)
  log.info('aws_update_device: email_verified %s   ', email_verified)
  log.info('aws_update_device: phone_verified %s   ', phone_verified)

  
  starttime = datetime.datetime.now()
  #startepoch =  int(time.time())

  if subscriptionKey == environ.get("SubscriptionKeyMonth"):
    endtime = datetime.datetime.now()  + relativedelta(months=1)
    SubscriptionType = "HelmSmart - Monthly"
  elif subscriptionKey == environ.get("SubscriptionKeyYear"):
    SubscriptionType = "HelmSmart - Yearly"
    endtime = datetime.datetime.now()  + relativedelta(months=12)
  elif subscriptionKey == environ.get("SubscriptionKeyWeekly"):
    SubscriptionType = "HelmSmart - Yearly"
    endtime = datetime.datetime.now()  + relativedelta(weeks=1)
  else:
    SubscriptionType = "HelmSmart - Expired"
    endtime = starttime

  log.info("aws_update_device - starttime %s endtime %s", starttime, endtime)

  
  conn = db_pool.getconn()
  
  try:
    
    query  = "select deviceapikey from user_devices where useremail = %s and deviceid = %s"
    cursor = conn.cursor()

    cursor = conn.cursor()
    cursor.execute(query, ( useremail, deviceid))
    i = cursor.fetchone()       

    #no existing userid so need to use hashed email for userid and hashed deviceid for combined deviceapikey      
    if cursor.rowcount == 0:

      userid=hash_string(useremail)
      log.info("aws_update_device- userid %s", userid)
      deviceapikey=hash_string(userid+deviceid+"013024")
      log.info("aws_update_device - deviceapikey %s", deviceapikey)
      
      log.info("aws_update_device - deviceapikey does not exist so adding  deviceapikey %s", deviceapikey)
      userstatus = "device does not exist - adding"

      query  = "insert into user_devices ( deviceapikey, userid, useremail, deviceid, devicestatus, devicename, alertemail, smsnumber, subscriptionid, transactionid, subscriptionstartdate, subscriptionenddate, email_verified,phone_verified) "
      query  = query + "Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

      log.info("aws_update_device update query %s ", query)

      # add new device record to DB
      cursor = conn.cursor()
      cursor.execute(query, (deviceapikey, userid, useremail, deviceid, devicestatus,  devicename, smsemail, smsphone, SubscriptionType, transactionID, starttime, endtime, email_verified, phone_verified))

      conn.commit()
        
      if cursor.rowcount == 0:
        #db_pool.putconn(conn)
        log.info("aws_update_device ADD DB ERROR deviceid %s ", deviceid)
        return False
        
      #db_pool.putconn(conn)
      log.info("aws_update_device ADD SUCCESS deviceid %s ", deviceid)
      return True

    #deviceid exists so look up if deviceapikey has already been added
    else:
      deviceapikey= str(i[0])
      log.info("Update Device status deviceapikey  %s  already exists", deviceapikey )

      query  = "update user_devices SET "
      query  = query + "devicename = %s, "
      query  = query + "alertemail = %s, "
      query  = query + "smsnumber = %s, "
      query  = query + "subscriptionid = %s, "
      query  = query + "transactionid = %s, "
      query  = query + "subscriptionstartdate = %s, "
      query  = query + "subscriptionenddate = %s "
      query  = query + "devicestatus = %s "
      query  = query + "email_verified = %s "
      query  = query + "phone_verified = %s "
      query  = query + "WHERE deviceapikey =  %s"

      log.info("aws_update_device update query %s ", query)
      
      # add new device record to DB
      cursor = conn.cursor()
      cursor.execute(query, (devicename, smsemail, smsphone, SubscriptionType, transactionID, starttime, endtime, email_verified, phone_verified, deviceapikey))

      conn.commit()

      if cursor.rowcount == 0:
        log.info("aws_update_device UPDATE DB ERROR deviceid %s ", deviceid)
        #db_pool.putconn(conn)
        return False
      
      #db_pool.putconn(conn)
      log.info("aws_update_device UPDATE SUCCESS deviceid %s ", deviceid)
      return True

  except psycopg.SyntaxError as e:
      log.info('aws_update_device: SyntaxError in  update deviceid %s:  ', deviceid)
      log.info('aws_update_device: SyntaxError in  update deviceid  %s:  ' % str(e))
      return False

  except psycopg.ProgrammingError as e:
      log.info('aws_update_device: ProgrammingError in  update deviceid %s:  ', deviceid)
      log.info('aws_update_device: ProgrammingError in  update deviceid  %s:  ' % str(e))
      return False

  except psycopg.DataError as e:
      log.info('aws_update_device: DataError in  update deviceid %s:  ', deviceid)
      log.info('aws_update_device: DataError in  update deviceid  %s:  ' % str(e))
      return False
    
  except TypeError as e:
    log.info("aws_update_device Device error -:TypeError deviceid %s ", deviceid)
    log.info('aws_update_device Device error -:TypeError  Error %s:  ' % e)
    return False

  except:
    e = sys.exc_info()[0]
    log.info("aws_update_device Device error - Error in update device %s", deviceid)
    log.info('aws_update_device Device error: Error in update device %s:  ' % e)
    return False
  
  finally:
    db_pool.putconn(conn)




@app.route('/aws_home')
def aws_home():
  
    log.info('aws_home: session %s:  ', session)
    
    user = session.get('user')

    log.info('aws_home: user %s:  ', user)

      
    if user:
        return  'Hello user = ' + user + '  <a href="/aws_alerts_logout">Logout</a>'
    else:
        return 'Welcome! Please <a href="/aws_login">Login</a>.'

@app.route('/auth_payment_completed' , methods=['GET','POST'])
def auth_payment_completed():

  log.info('auth_payment_completed:start  ')

  try:  
    dataList=list(request.form)
    log.info('auth_payment_completed:dataList %s  ' , dataList)


    data_dict = request.form.to_dict(flat=True)
    log.info("auth_payment_completed data_dict %s",data_dict)

    #mPayment = json.loads(request.form)
    #log.info("auth_payment_completed mPayment %s",mPayment)
    #mPaymentDeviceID = data_dict['x_invoice_num']
    mPaymentResponseCode = data_dict.get('x_response_code', "")

    if mPaymentResponseCode == "":
      return jsonify( message='Add user auth_payment_completed error - x_response_code failed'  )

    log.info('auth_payment_completed:mPaymentResponseCode %s  ' , mPaymentResponseCode)

    if mPaymentResponseCode != "1":
      mPaymentReasonCode = data_dict.get('x_response_reason_code', "")
      
      if mPaymentReasonCode == '44':
        return jsonify( message='Add User Error - payment declined - invalid CVC code ' )
      
      mPaymentReasonText = data_dict.get('x_response_reason_text', "")
      return jsonify( message='Add User Error - payment declined',  code =mPaymentReasonCode, reason = mPaymentReasonText )

    
    mPaymentDeviceID = data_dict.get('x_invoice_num', "")

    if mPaymentDeviceID == "":
      return jsonify( message='Add user auth_payment_completed error - x_invoice_num failed' )

    log.info('auth_payment_completed:mPaymentDeviceID %s  ' , mPaymentDeviceID)


    mPaymentEmail = data_dict.get('x_email', "")

    if mPaymentEmail == "":
      return jsonify( message='Add user auth_payment_completed error - x_email failed'  )

    log.info('auth_payment_completed:mPaymentEmail %s  ' , mPaymentEmail)

    mPaymentPhone = data_dict.get('x_phone', "")

    if mPaymentPhone != "":
      mPaymentPhone = '+' + mPaymentPhone

    log.info('auth_payment_completed:mPaymentPhone %s  ' , mPaymentPhone)



    mPaymentDeviceName = data_dict.get('x_description', "")

    if mPaymentDeviceName == "":
      return jsonify( message='Add user auth_payment_completed error - x_description failed'  )

    log.info('auth_payment_completed:mPaymentDeviceName %s  ' , mPaymentDeviceName)

    mPaymentSubscription = data_dict.get('x_catalog_link_id', "")

    if mPaymentSubscription == "":
      return jsonify( message='Add user auth_payment_completed error - x_catalog_link_id failed'  )

    log.info('auth_payment_completed:mPaymentSubscription %s  ' , mPaymentSubscription)

    mPaymentTransaction = data_dict.get('x_trans_id', "")

    if mPaymentTransaction == "":
      return jsonify( message='Add user auth_payment_completed error - x_trans_id failed'  )

    log.info('auth_payment_completed:mPaymentTransaction %s  ' , mPaymentTransaction)

    #########################################################
    ## check if user already exists
    #########################################################
    
    device_alreay_exists = aws_check_user_exists(mPaymentDeviceID)

    #########################################################

    # if does not exist then add new device

    if device_alreay_exists == False:
      
      #########################################################
      ## adding new device
      #########################################################
      log.info("auth_payment_completed: adding new device")
      
      try:
        
        response = cognito_client.admin_create_user(
            UserPoolId=environ.get("AWS_COGNITO_USER_POOL_ID"),
            Username=mPaymentDeviceID,
            DesiredDeliveryMediums=['EMAIL',],
            #DesiredDeliveryMediums=['SMS'|'EMAIL',],
            UserAttributes=[
                  {'Name': 'email', 'Value': mPaymentEmail},
                  {'Name': 'phone_number', 'Value': mPaymentPhone},
                  {'Name': 'name', 'Value': mPaymentDeviceName}
                  #{'Name': 'email_verified', 'Value': 'true'} # Set email as verified
              ]
           
        )
   
        errorcheck = response.get('x-amzn-ErrorType', 'noerror')
        log.info('auth_payment_completed:errorcheck %s  ' , errorcheck)

        if errorcheck != 'noerror':
          log.info('auth_payment_completed:errorcheck %s  ' , errorcheck)
          return jsonify( message='x-amzn-ErrorType', status=errorcheck)


        ######### add new device to helmsmart database #############
        #def aws_update_device(deviceid, devicename, useremail, smsemail, smsphone, subscriptionKey, transactionID, devicestatus, email_verified, phone_verified ):
        deviceupdate_check = aws_update_device(mPaymentDeviceID, mPaymentDeviceName, mPaymentEmail, mPaymentEmail, mPaymentPhone,mPaymentSubscription, mPaymentTransaction, 1, False, False   )

        if deviceupdate_check == True:
          return redirect(url_for('user_subscription_added'))

        else:
          return jsonify( message='aws_add_device error - failed'  )          
       ###############################################
          
        #return jsonify( json.dumps(response) )
        return redirect(url_for('newalertsuseradded'))  

      except cognito_client.exceptions.InvalidParameterException as e:
        log.info("auth_payment_completed - add device: InvalidParameterException")
        #print(f"Invalid parameter: {e.response['Error']['Message']}")
        log.info('auth_payment_completed  - add device error -InvalidParameterException  Error %s:  ' , e.response['Error']['Message'])
        return jsonify( message='Error Invalid Parameter', status=e.response['Error']['Message'])

      except cognito_client.exceptions.UsernameExistsException:
        log.info("auth_payment_completed - add device: UsernameExistsException")
        return jsonify( message='Username  already Exists', status='error')

      except cognito_client.exceptions.UserNotFoundException:
        log.info("auth_payment_completed - add device: UserNotFoundException")
        return jsonify( message='Username not found', status='error')
      
      except KeyError as e:
        log.info('auth_payment_completed error  - add device:KeyError  Error %s:  ' % e)
        return jsonify( message='Add user auth_payment_completed aws Key error - failed' )

      except AttributeError as e:
        log.info('auth_payment_completed error  - add device:AttributeError  Error %s:  ' % e)
        return jsonify( message='Add user auth_payment_completed aws AttributeError error - failed' )
      
      except TypeError as e:
        log.info('auth_payment_completed error  - add device:TypeError  Error %s:  ' % e)
        return jsonify( message='Add user auth_payment_completed aws Type error - failed'  )
      
      except:
        e = sys.exc_info()[0]
        log.info('aws_cognito_user_added aws error  - add device: Error in adding user %s:  ' % e)
        return jsonify( message='Add user auth_payment_completed aws error - failed'  )
      
      return jsonify( json.dumps(data_dict, indent=4) )

    else:
      
      #########################################################
      ## updating existing device
      #########################################################
      log.info("auth_payment_completed: updating existing device")
       
      try:
        
        response = cognito_client.admin_update_user_attributes(
            UserPoolId=environ.get("AWS_COGNITO_USER_POOL_ID"),
            Username=mPaymentDeviceID,

            UserAttributes=[
                  {'Name': 'email', 'Value': mPaymentEmail},
                  {'Name': 'phone_number', 'Value': mPaymentPhone},
                  {'Name': 'name', 'Value': mPaymentDeviceName}
                  #{'Name': 'email_verified', 'Value': 'true'} # Set email as verified
              ]
           
        )
   
        errorcheck = response.get('x-amzn-ErrorType', 'noerror')
        log.info('auth_payment_completed:errorcheck %s  ' , errorcheck)

        if errorcheck != 'noerror':
          log.info('auth_payment_completed:errorcheck %s  ' , errorcheck)
          return jsonify( message='x-amzn-ErrorType', status=errorcheck)


        ######### add update device to helmsmart database #############
         #def aws_update_device(deviceid, devicename, useremail, smsemail, smsphone, subscriptionKey, transactionID, devicestatus, email_verified, phone_verified ):       
        deviceupdate_check = aws_update_device(mPaymentDeviceID, mPaymentDeviceName, mPaymentEmail, mPaymentEmail, mPaymentPhone,mPaymentSubscription, mPaymentTransaction, 1, False, False   )
          
        if deviceupdate_check == True:
          return redirect(url_for('user_subscription_updated'))

        else:
          return jsonify( message='aws_update_device error - failed'  )
        
       ###############################################      

      except cognito_client.exceptions.InvalidParameterException as e:
        log.info("auth_payment_completed - update device: InvalidParameterException")
        #print(f"Invalid parameter: {e.response['Error']['Message']}")
        log.info('auth_payment_completed error -InvalidParameterException  Error %s:  ' , e.response['Error']['Message'])
        return jsonify( message='Error Invalid Parameter', status=e.response['Error']['Message'])

      except cognito_client.exceptions.UsernameExistsException:
        log.info("auth_payment_completed - update device : UsernameExistsException")
        return jsonify( message='Username  already Exists', status='error')
      
      except KeyError as e:
        log.info('auth_payment_completed error  - update device:KeyError  Error %s:  ' % e)
        return jsonify( message='Add user auth_payment_completed aws Key error - failed'  )

      except ValueError as e:
        log.info('auth_payment_completed error  - update device:ValueError  Error %s:  ' % e)
        return jsonify( message='Add user auth_payment_completed aws Value error - failed'  )
      
      except TypeError as e:
        log.info('auth_payment_completed error  - update device:TypeError  Error %s:  ' % e)
        return jsonify( message='Add user auth_payment_completed aws Type error - failed'  )
      
      except:
        e = sys.exc_info()[0]
        log.info('aws_cognito_user_added aws error  - update device: Error in adding user %s:  ' % e)
        return jsonify( message='Add user auth_payment_completed aws error - failed'  )
      
      return jsonify( json.dumps(data_dict, indent=4) )

  except ValueError as e:
    log.info('auth_payment_completed error -:ValueError  Error %s:  ' % e)
    return jsonify( message='Add user auth_payment_completed Value error - failed' )    

  except TypeError as e:
    log.info('auth_payment_completed error -:TypeError  Error %s:  ' % e)
    return jsonify( message='Add user auth_payment_completed Type error - failed'  )
  
  except:
    e = sys.exc_info()[0]
    log.info('aws_cognito_user_added Device error: Error in adding device %s:  ' % e)
    return jsonify( message='Add user auth_payment_completed error - failed'  )

@app.route('/aws_cognito_user_added')
def aws_cognito_user_added():

  log.info('aws_cognito_user_added:start  ')  
  log.info('aws_cognito_user_added:request  %s', request)  

  deviceid = request.args.get('username', '000000000000')
  deviceid = deviceid.upper()
  useremail = request.args.get('email', "")
  useremailverified = request.args.get('emailverified', "")
  userphone = request.args.get('phone', "")
  userphoneverified = request.args.get('phoneverified', "")
  devicename = request.args.get('device',  'SeaSmart')
  status = 1

  log.info('aws_cognito_user_added: deviceid %s  devicename %s:  ', deviceid, devicename)
  log.info('aws_cognito_user_added: useremail %s useremailverified %s:  ', useremail, useremailverified)
  log.info('aws_cognito_user_added: userphone %s userphoneverified %s:  ', userphone, userphoneverified)

  smsemail = None
  if useremailverified == "true":
    smsemail = useremail

  smsphone = None
  if userphoneverified == "true":
    smsphone = userphone
    
  log.info('aws_cognito_user_added: smsemail %s smsphone %s:  ', smsemail, smsphone)

  
  #aws_add_device(deviceid, devicename, useremail,  smsemail, smsphone )
  #def aws_update_device(deviceid, devicename, useremail, smsemail, smsphone, subscriptionKey, transactionID, devicestatus, email_verified, phone_verified ):
  aws_update_device(deviceid, devicename, useremail,  smsemail, smsphone, 'HelmSmart - Expired', '0000000000', 0, useremailverified, userphoneverified )

@app.route('/aws_alerts_logout')
#@cognito_login_callback
def aws_alerts_logout():

  session.pop('user', None)
  session.clear

  response = make_response(redirect(url_for('manage')))
  #cookie_name = app.config.get('SESSION_COOKIE_NAME', 'session')
  
  cookie_name = 'session'
  
  response.delete_cookie(
          cookie_name, 
          path='/', # Match the original cookie path
          httponly=True # It's good practice to keep the HttpOnly flag consistent
      )

  return response
  #return redirect(url_for('manage'))  

@app.route('/aws_delete_device')
def aws_delete_device():

  log.info('aws_delete_device: started')

  returncode="ERROR"
  
  deviceapikey = request.args.get('deviceapikey',"")
  #useremail = request.args.get('useremail', '')
  deviceid = request.args.get('deviceid', "")
  #devicename = request.args.get('name', '')

  log.info('aws_delete_device: deviceapikey %s:   deviceid %s:', deviceapikey, deviceid)

  if deviceapikey == "" or deviceid == "":
    return jsonify( message='aws_delete_user', status='error')     

  try:
    
    response = cognito_client.admin_delete_user(
        UserPoolId=environ.get("AWS_COGNITO_USER_POOL_ID"),
        Username=deviceid
    )


    log.info("aws_delete_device:admin_delete_user response %s:", response)

    HTTPstatus = response.get("ResponseMetadata", {}).get('HTTPStatusCode')
    log.info("aws_delete_device:admin_delete_user HTTPstatus %s:", HTTPstatus)

    if HTTPstatus != 200:
      return jsonify( message='aws_delete_user admin_delete_user', status='error') 

  except cognito_client.exceptions.ResourceNotFoundException:
    log.info("aws_delete_device: User or User Pool not found.")
    return jsonify( message='aws_delete_user', status='error')  

  except cognito_client.exceptions.InvalidParameterException:
    log.info("aws_delete_device: InvalidParameterException")
    e = sys.exc_info()[0]
    log.info('manage_details: Error InvalidParameterException in getting verify code %s:  ' % str(e))
    return jsonify( message='aws_delete_user', status='error')  

  except AttributeError as e:
    log.info('aws_delete_device: AttributeError Error in getting verify code  ' % str(e))
    return jsonify( message='aws_delete_user', status='error')  
    
  except:
    e = sys.exc_info()[0]
    log.info('aws_delete_device: Error in verify in getting verify code %s:  ' % str(e))  
    return jsonify( message='aws_delete_user', status='error')  

    log.info("aws_delete_device: AWS user deleted")



  conn = db_pool.getconn()
 
  query  = "delete from user_devices where deviceapikey = %s AND deviceid = %s  "
  
  try:
    # add new device record to DB
    cursor = conn.cursor()
    cursor.execute(query, (deviceapikey, deviceid))

    conn.commit()
    #i = cursor.fetchone()
    # if not then just exit
    #if cursor.rowcount == 0:
      
    if cursor.rowcount == 0:
          return jsonify( message='aws_delete_device Could not delete device', status='error')      
    else:
          return jsonify( message='aws_delete_device deleted', status='success') 
  
  except:
    e = sys.exc_info()[0]
    log.info('aws_delete_user : Error db delete %s:  ' % e)
    return jsonify( message='aws_delete_device', status='error')     

  finally:
    db_pool.putconn(conn)   

  return jsonify( message='aws_delete_device', status='error')     


@app.route('/aws_alerts_get_user_data')
#@cognito_login_callback
def aws_alerts_get_user_data():
  
  log.info('aws_alerts_get_user_data: request.args %s:  ', request.args)
  log.info('aws_alerts_get_user_data: session %s:  ', session)
  
  access_token = aws_auth.get_access_token(request.args)
  log.info('aws_alerts_get_user_data: access_token %s:  ', access_token) 
  #return jsonify({'access_token': access_token})
  #tokens = session.json()
  #tokens = session
  #access_token = tokens.get("access_token")
  #user_info = access_token.get("user_info")

  #tokens = oauth_aws.oidc.authorize_access_token()

  #log.info('manage_details: token %s:  ', tokens)

  response = cognito_client.get_user(  AccessToken=access_token  )



  log.info('aws_alerts_get_user_data: get_user %s:  ', response)




  username = response.get('Username', "")
  log.info('aws_alerts_get_user_data: username %s:  ', username)
  

  # Extract the email from the UserAttributes list
  useremail = None
  for attribute in response['UserAttributes']:
      if attribute['Name'] == 'email':
          useremail = attribute['Value']
          break

  log.info('aws_alerts_get_user_data: useremail %s:  ', useremail)

  # Extract the email from the UserAttributes list
  aws_phone = None
  for attribute in response['UserAttributes']:
      if attribute['Name'] == 'phone_number':
          aws_phone = attribute['Value']
          break

  log.info('aws_alerts_get_user_data: aws_phone %s:  ', aws_phone)

  # Extract the email from the UserAttributes list
  aws_name = None
  for attribute in response['UserAttributes']:
      if attribute['Name'] == 'name':
          aws_name = attribute['Value']
          break

  log.info('aws_alerts_get_user_data: aws_name %s:  ', aws_name)

  # Extract the email from the UserAttributes list
  aws_email_verified = 'false'
  for attribute in response['UserAttributes']:
      if attribute['Name'] == 'email_verified':
          aws_email_verified = attribute['Value']
          break

  log.info('aws_alerts_get_user_data: aws_email_verified %s:  ', aws_email_verified)

  # Extract the email from the UserAttributes list
  aws_phone_verified = 'false'
  for attribute in response['UserAttributes']:
      if attribute['Name'] == 'phone_number_verified':
          aws_phone_verified = attribute['Value']
          break

  log.info('aws_alerts_get_user_data: phone_number_verified %s:  ', aws_phone_verified)
  
        

  session.clear
  

  #user_info_json = json.dumps(userinfo)
  #log.info('aws_alerts_get_admin_data: TypeError in user_info %s:  ', user_info_json)
  
  #session['profile'] =json.loads(user_info_json)
  session['profile']={}
  session['profile']['email'] = useremail
  session['profile']['name'] = username
  session.modified = True
  log.info('aws_alerts_get_user_data: session user_info %s:  ', session)
  
  session['username'] = useremail
  session['aws_userid'] = username
  session['aws_email'] = useremail
  session['aws_phone'] = aws_phone
  session['aws_name'] = aws_name
  session['aws_email_verified'] = aws_email_verified
  session['aws_phone_verified'] = aws_phone_verified

  
  session['aws_clientid'] = environ.get("AWS_COGNITO_USER_POOL_CLIENT_ID")
  session['aws_domain'] = environ.get("AWS_COGNITO_DOMAIN")
  session['aws_access_token'] = access_token

  log.info('aws_alerts_get_user_data: exit session %s:  ', session)
  #return redirect(url_for('aws_home'))
  return redirect(url_for('manage'))    

@app.route('/aws_alerts_get_admin_data')
#@cognito_login_callback
def aws_alerts_get_admin_data():
  
  #log.info('aws_alerts_get_admin_data: request.args %s:  ', request.args)
  #log.info('aws_alerts_get_admin_data: session %s:  ', session)
  session.clear
  #access_token = aws_auth.get_access_token(request.args)
  #access_token = aws_auth.get_access_token()
  #log.info('aws_alerts_get_admin_data: access_token %s:  ', access_token) 
  #return jsonify({'access_token': access_token})
  #tokens = session.json()
  #tokens = session
  #access_token = tokens.get("access_token")
  #user_info = access_token.get("user_info")

  token = oauth_aws_admin.oidc.authorize_access_token()

  #log.info('aws_alerts_get_admin_data: token %s:  ', token)

  #response = cognito_client.get_user(  AccessToken=access_token  )



  #log.info('aws_alerts_get_admin_data: get_user %s:  ', response)

  userinfo = token['userinfo']
  #username = tokens.get('Username', "")
  log.info('aws_alerts_get_admin_data: userinfo %s:  ', userinfo)


  user_info_json = json.dumps(userinfo)
  log.info('aws_alerts_get_admin_data: TypeError in user_info %s:  ', user_info_json)
  
  session['profile'] =json.loads(user_info_json)
  log.info('aws_alerts_get_admin_data: TypeError in session user_info %s:  ', session)

  username = userinfo.get("cognito:username","")
  log.info('aws_alerts_get_admin_data: username %s:  ', username)
  
  useremail = userinfo.get("email","")
  log.info('aws_alerts_get_admin_data: useremail %s:  ', useremail)

  aws_phone = userinfo.get("phone_number","")
  log.info('aws_alerts_get_admin_data: aws_phone %s:  ', aws_phone)

  aws_name = userinfo.get("name","SeaGaugeG4")
  log.info('aws_alerts_get_admin_data: aws_name %s:  ', aws_name)

  aws_email_verified = userinfo.get("email_verified","")
  log.info('aws_alerts_get_admin_data: aws_email_verified %s:  ', aws_email_verified)

  aws_phone_verified = userinfo.get("phone_number_verified","")
  log.info('aws_alerts_get_admin_data: phone_number_verified %s:  ', aws_phone_verified)
  
        

  session['username'] = useremail
  session['aws_userid'] = username
  session['aws_email'] = useremail
  session['aws_phone'] = aws_phone
  session['aws_name'] = aws_name
  session['aws_email_verified'] = aws_email_verified
  session['aws_phone_verified'] = aws_phone_verified

  
  session['aws_clientid'] = environ.get("AWS_COGNITO_ADMIN_POOL_CLIENT_ID")
  session['aws_domain'] = environ.get("AWS_COGNITO_ADMIN_DOMAIN")
  #session['aws_access_token'] = token
  session['aws_access_token'] = ""

  log.info('aws_alerts_get_admin_data: exit session %s:  ', session)
  #return redirect(url_for('aws_home'))
  return redirect(url_for('manage')) 

@app.route('/aws_cognito_update_sms_number')
def aws_cognito_update_sms_number():

  log.info('aws_cognito_update_sms_number: started')

  log.info('aws_cognito_update_sms_number: request.args %s:  ', request.args)
  log.info('aws_cognito_update_sms_number: session %s:  ', session)
  
  #access_token = aws_auth.get_access_token(request.args)
  access_token = session.get("aws_access_token")
  log.info('aws_cognito_update_sms_number: access_token %s:  ', access_token) 

  returncode="ERROR"
  prefix = "+"

  userid = request.args.get('userid',"")
  smsnumber = request.args.get('smsnumber',"")

  if smsnumber.startswith("+") == False:
    smsnumber = prefix + smsnumber
  
  log.info('aws_cognito_update_sms_number: userid %s smsnumber %s' , userid, smsnumber)


  
  try:
    response = cognito_client.admin_update_user_attributes(
        UserPoolId=environ.get("AWS_COGNITO_USER_POOL_ID"),
        Username=userid,
        UserAttributes=[
            {
                'Name': 'phone_number',
                'Value': smsnumber
            }
        ]
    )

    log.info("aws_cognito_update_sms_number:Successfully updated phone number for user %s:", userid)   
    log.info("aws_cognito_update_sms_number:updated phone number response %s:", response)

    # Note: The phone number will be unverified by default.
    # Use AdminUpdateUserAttributes to set 'phone_number_verified' to 'true' if needed.
    #return jsonify( message='aws_cognito_validate_sms_number ', status='success') 

  except cognito_client.exceptions.ResourceNotFoundException:
    log.info("aws_cognito_update_sms_number: User or User Pool not found.")
    return jsonify( message='aws_cognito_validate_sms_number ', status='success') 
    
  except cognito_client.exceptions.InvalidParameterException:
    log.info("aws_cognito_update_sms_number: ParamValidationError")
    e = sys.exc_info()[0]
    log.info('aws_cognito_update_sms_number: Error ParamValidationError in geting adding phone number %s:  ' % str(e))
    return jsonify( message='aws_cognito_validate_sms_number ', status='success') 
        
  except AttributeError as e:
    log.info('aws_cognito_update_sms_number: AttributeError Error in geting adding phone number  ' % str(e))
    return jsonify( message='aws_cognito_validate_sms_number ', status='success') 
    
  except:
    e = sys.exc_info()[0]
    log.info('aws_cognito_update_sms_number: Error in geting adding phone number %s:  ' % str(e))
    return jsonify( message='aws_cognito_validate_sms_number ', status='success') 
  

  log.info("aws_cognito_update_sms_number: Getting verify code")
  
  try:
    response = cognito_client.get_user_attribute_verification_code(
            AccessToken=access_token,
            AttributeName='phone_number'
    )

    #log.info("manage_details:Successfully verification code for user %s:", username)   
    log.info("aws_cognito_update_sms_number:verification code response %s:", response)

    # Note: The phone number will be unverified by default.
    # Use AdminUpdateUserAttributes to set 'phone_number_verified' to 'true' if needed.

  except cognito_client.exceptions.ResourceNotFoundException:
    log.info("aws_cognito_update_sms_number: User or User Pool not found.")

  except cognito_client.exceptions.InvalidParameterException:
    log.info("aws_cognito_update_sms_number: InvalidParameterException")
    e = sys.exc_info()[0]
    log.info('aws_cognito_update_sms_number: Error InvalidParameterException in getting verify code %s:  ' % str(e))  

  except AttributeError as e:
    log.info('aws_cognito_update_sms_number: AttributeError Error in getting verify code %s ' % str(e))
    
  except:
    e = sys.exc_info()[0]
    log.info('aws_cognito_update_sms_number: Error in verify in getting verify code %s:  ' % str(e))  

    log.info("aws_cognito_update_sms_number: Got verify code")

  return jsonify( message='aws_cognito_update_sms_number ', status='success')


@app.route('/aws_cognito_confirm_sms_number')
def aws_cognito_confirm_sms_number():

  log.info('aws_cognito_confirm_sms_number: started')

  log.info('aws_cognito_confirm_sms_number: request.args %s:  ', request.args)
  log.info('aws_cognito_confirm_sms_number: session %s:  ', session)
  
  #access_token = aws_auth.get_access_token(request.args)
  access_token = session.get("aws_access_token")
  log.info('aws_cognito_confirm_sms_number: access_token %s:  ', access_token) 

  userid = request.args.get('userid',"")
  smscode = request.args.get('smscode',"")
  devicekey = request.args.get('devicekey',"")
  smsnumber = request.args.get('smsnumber',"")

  log.info('aws_cognito_confirm_sms_number: devicekey %s smsnumber %s' , devicekey, smsnumber)
  log.info('aws_cognito_confirm_sms_number: userid %s smscode %s' , userid, smscode)


  try:

    response = cognito_client.verify_user_attribute(
            AccessToken=access_token,
            AttributeName='phone_number',
            Code=smscode
    )

    #log.info("manage_details:Phone number successfully verified. user %s:", username)   
    log.info("aws_cognito_confirm_sms_number:verify_user_attribute response %s:", response)

    HTTPstatus = response.get("ResponseMetadata", {}).get('HTTPStatusCode')
    log.info("aws_cognito_confirm_sms_number:verify_user_attribute HTTPstatus %s:", HTTPstatus)

    if HTTPstatus != 200:
      return jsonify( message='aws_cognito_confirm_sms_number ', status='error')
    
    updatesmsnumber(devicekey, smsnumber)

  except cognito_client.exceptions.CodeMismatchException:
    log.info("aws_cognito_confirm_sms_number: Invalid verification code provided, please try again..")
    
  except cognito_client.exceptions.ExpiredCodeException:
    log.info("aws_cognito_confirm_sms_number: Verification code expired.")
    e = sys.exc_info()[0]
    log.info('aws_cognito_confirm_sms_number: Error ExpiredCodeException in verify phone number %s:  ' % str(e))  
      
  except AttributeError as e:
    log.info('aws_cognito_confirm_sms_number: AttributeError Error in verify phone number %s  ' % str(e))

  except NameError as e:
    log.info('aws_cognito_confirm_sms_number: NameError Error in verify phone number  %s' % str(e))
    
  except TypeError as e:
    log.info('aws_cognito_confirm_sms_number: NameError Error in verify phone number  %s' % str(e))
    

  except:
    e = sys.exc_info()[0]
    log.info('aws_cognito_confirm_sms_number: Error in verify phone number  %s ' % str(e))

    
  log.info("aws_cognito_confirm_sms_number: phone number verified")

  return jsonify( message='aws_cognito_confirm_sms_number ', status='success')

def updatesmsnumber(deviceapikey, smsnumber):

  log.info('updatesmsnumber: devicekey %s smsnumber %s' , deviceapikey, smsnumber)
  conn = db_pool.getconn()
  
  try:
    
    cursor = conn.cursor()
    #update user_devices SET smsnumber = %s where deviceapikey = %s;
    query  = "update user_devices set smsnumber = %s where deviceapikey = %s;"

    # add new device record to DB
    cursor = conn.cursor()
    cursor.execute(query, (smsnumber, deviceapikey))

    conn.commit()
      
    if cursor.rowcount == 0:
      userstatus = " Could not add user smsnumber " + str(deviceapikey)
      return jsonify( message='Could not add smsnumber', status='error')

    userstatus = "new  smsnumber added"
    return jsonify( message='Added smsnumber' , deviceapikey=deviceapikey, userstatus = userstatus )

  except TypeError as e:
    log.info("updatesmsnumber Device error -:TypeError deviceid %s ", deviceapikey)
    log.info('updatesmsnumber Device error -:TypeError  Error %s:  ' % e)
    return jsonify( message='Add user deviceid error - failed' , deviceapikey=deviceapikey, userstatus = "could not add smsnumber" )

  except NameError as e:
    log.info("updatesmsnumber Device error -:NameError deviceid %s ", deviceapikey)
    log.info('updatesmsnumber Device error -:NameError  Error %s:  ' % e)
    return jsonify( message='Add user deviceid error - failed' , deviceapikey=deviceapikey, userstatus = "could not add smsnumber" )


  except:
    e = sys.exc_info()[0]
    log.info("updatesmsnumber Device error - Error in adding device %s", deviceapikey)
    log.info('updatesmsnumber Device error: Error in adding device %s:  ' % e)
    return jsonify( message='Add user deviceid error - failed' , deviceapikey=deviceapikey, userstatus = "could not add smsnumber" )
  
  finally:
    db_pool.putconn(conn)



@app.route('/aws_cognito_update_sms_email')
def aws_cognito_update_sms_email():

  log.info('aws_cognito_update_sms_email: started')

  log.info('aws_cognito_update_sms_email: request.args %s:  ', request.args)
  log.info('aws_cognito_update_sms_email: session %s:  ', session)
  
  #access_token = aws_auth.get_access_token(request.args)
  access_token = session.get("aws_access_token")
  log.info('aws_cognito_update_sms_email: access_token %s:  ', access_token) 

  returncode="ERROR"

  userid = request.args.get('userid',"")
  smsemail = request.args.get('smsemail',"")

  
  log.info('aws_cognito_update_sms_email: userid %s smsnumber %s' , userid, smsemail)


  
  try:
    response = cognito_client.admin_update_user_attributes(
        UserPoolId=environ.get("AWS_COGNITO_USER_POOL_ID"),
        Username=userid,
        UserAttributes=[
            {
                'Name': 'email',
                'Value': smsemail
            }
        ]
    )

    log.info("aws_cognito_update_sms_email:Successfully updated phone number for user %s:", userid)   
    log.info("aws_cognito_update_sms_email:updated phone number response %s:", response)

    # Note: The phone number will be unverified by default.
    # Use AdminUpdateUserAttributes to set 'phone_number_verified' to 'true' if needed.
    #return jsonify( message='aws_cognito_validate_sms_number ', status='success') 

  except cognito_client.exceptions.ResourceNotFoundException:
    log.info("aws_cognito_update_sms_email: User or User Pool not found.")
    return jsonify( message='aws_cognito_validate_sms_email ', status='success') 
    
  except cognito_client.exceptions.InvalidParameterException:
    log.info("aws_cognito_update_sms_email: ParamValidationError")
    e = sys.exc_info()[0]
    log.info('aws_cognito_update_sms_email: Error ParamValidationError in geting adding smsemail %s:  ' % str(e))
    return jsonify( message='aws_cognito_validate_sms_number ', status='success') 
        
  except AttributeError as e:
    log.info('aws_cognito_update_sms_number: AttributeError Error in geting adding smsemail  ' % str(e))
    return jsonify( message='aws_cognito_validate_sms_number ', status='success') 
    
  except:
    e = sys.exc_info()[0]
    log.info('aws_cognito_update_sms_email: Error in geting adding smsemail %s:  ' % str(e))
    return jsonify( message='aws_cognito_validate_sms_number ', status='success') 
  

  log.info("aws_cognito_update_sms_email: Getting verify code")
  
  try:
    response = cognito_client.get_user_attribute_verification_code(
            AccessToken=access_token,
            AttributeName='email'
    )

    #log.info("manage_details:Successfully verification code for user %s:", username)   
    log.info("aws_cognito_update_sms_email:verification code response %s:", response)

    # Note: The phone number will be unverified by default.
    # Use AdminUpdateUserAttributes to set 'phone_number_verified' to 'true' if needed.

  except cognito_client.exceptions.ResourceNotFoundException:
    log.info("aws_cognito_update_sms_email: User or User Pool not found.")

  except cognito_client.exceptions.InvalidParameterException:
    log.info("aws_cognito_update_sms_email: InvalidParameterException")
    e = sys.exc_info()[0]
    log.info('aws_cognito_update_sms_email: Error InvalidParameterException in getting verify code %s:  ' % str(e))  

  except AttributeError as e:
    log.info('aws_cognito_update_sms_email: AttributeError Error in getting verify code %s ' % str(e))
    
  except:
    e = sys.exc_info()[0]
    log.info('aws_cognito_update_sms_email: Error in verify in getting verify code %s:  ' % str(e))  

    log.info("aws_cognito_update_sms_email: Got verify code")

  return jsonify( message='aws_cognito_update_sms_email ', status='success')


@app.route('/aws_cognito_confirm_sms_email')
def aws_cognito_confirm_sms_email():

  log.info('aws_cognito_confirm_sms_email: started')

  log.info('aws_cognito_confirm_sms_email: request.args %s:  ', request.args)
  log.info('aws_cognito_confirm_sms_email: session %s:  ', session)
  
  #access_token = aws_auth.get_access_token(request.args)
  access_token = session.get("aws_access_token")
  log.info('aws_cognito_confirm_sms_email: access_token %s:  ', access_token) 

  userid = request.args.get('userid',"")
  smscode = request.args.get('smscode',"")
  devicekey = request.args.get('devicekey',"")
  smsemail = request.args.get('smsemail',"")

  log.info('aws_cognito_confirm_sms_email: devicekey %s smsemail %s' , devicekey, smsemail)
  log.info('aws_cognito_confirm_sms_email: userid %s smscode %s' , userid, smscode)


  try:

    response = cognito_client.verify_user_attribute(
            AccessToken=access_token,
            AttributeName='email',
            Code=smscode
    )

    #log.info("manage_details:Phone number successfully verified. user %s:", username)   
    log.info("aws_cognito_confirm_sms_email:verify_user_attribute response %s:", response)

    HTTPstatus = response.get("ResponseMetadata", {}).get('HTTPStatusCode')
    log.info("aws_cognito_confirm_sms_email:verify_user_attribute HTTPstatus %s:", HTTPstatus)

    if HTTPstatus != 200:
      return jsonify( message='aws_cognito_confirm_sms_email ', status='error')
    
    updatesmsnumber(devicekey, smsnumber)

  except cognito_client.exceptions.CodeMismatchException:
    log.info("aws_cognito_confirm_sms_email: Invalid verification code provided, please try again..")
    
  except cognito_client.exceptions.ExpiredCodeException:
    log.info("aws_cognito_confirm_sms_email: Verification code expired.")
    e = sys.exc_info()[0]
    log.info('aws_cognito_confirm_sms_email: Error ExpiredCodeException in verify smsemail %s:  ' % str(e))  
      
  except AttributeError as e:
    log.info('aws_cognito_confirm_sms_email: AttributeError Error in verify smsemail %s  ' % str(e))

  except NameError as e:
    log.info('aws_cognito_confirm_sms_email: NameError Error in verify smsemail  %s' % str(e))
    
  except TypeError as e:
    log.info('aws_cognito_confirm_sms_email: NameError Error in verify smsemail  %s' % str(e))
    

  except:
    e = sys.exc_info()[0]
    log.info('aws_cognito_confirm_sms_email: Error in verify smsemail  %s ' % str(e))

    
  log.info("aws_cognito_confirm_sms_email: smsemail verified")

  return jsonify( message='aws_cognito_confirm_sms_email ', status='success')

def updatesmsemail(deviceapikey, smsemail):

  log.info('updatesmsemail: devicekey %s smsemail %s' , deviceapikey, smsemail)
  conn = db_pool.getconn()
  
  try:
    
    cursor = conn.cursor()
    #update user_devices SET smsnumber = %s where deviceapikey = %s;
    query  = "update user_devices set alertemail = %s where deviceapikey = %s;"

    # add new device record to DB
    cursor = conn.cursor()
    cursor.execute(query, (smsemail, deviceapikey))

    conn.commit()
      
    if cursor.rowcount == 0:
      userstatus = " Could not add user smsemail " + str(deviceapikey)
      return jsonify( message='Could not add smsemail', status='error')

    userstatus = "new  smsemail added"
    return jsonify( message='Added smsemail' , deviceapikey=deviceapikey, userstatus = userstatus )

  except TypeError as e:
    log.info("updatesmsemail Device error -:TypeError deviceid %s ", deviceapikey)
    log.info('updatesmsemail Device error -:TypeError  Error %s:  ' % e)
    return jsonify( message='Add user deviceid error - failed' , deviceapikey=deviceapikey, userstatus = "could not add smsemail" )

  except NameError as e:
    log.info("updatesmsemail Device error -:NameError deviceid %s ", deviceapikey)
    log.info('updatesmsemail Device error -:NameError  Error %s:  ' % e)
    return jsonify( message='Add user deviceid error - failed' , deviceapikey=deviceapikey, userstatus = "could not add smsemail" )


  except:
    e = sys.exc_info()[0]
    log.info("updatesmsemail Device error - Error in adding device %s", deviceapikey)
    log.info('updatesmsemail Device error: Error in adding device %s:  ' % e)
    return jsonify( message='Add user deviceid error - failed' , deviceapikey=deviceapikey, userstatus = "could not add smsemail" )
  
  finally:
    db_pool.putconn(conn)

@app.route('/aws_admin_login')
#@cognito_login
def aws_admin_login():
  
  session.clear()

  return oauth_aws_admin.oidc.authorize_redirect('https://www.helmsmart-cloud.com/aws_alerts_get_admin_data')
  #return oauth_aws.oidc.authorize_redirect('https://www.helmsmart-cloud.com/aws_alerts_get_user_data?login_hint=someone')
  #return oauth_aws.oidc.authorize_redirect('https://www.helmsmart-cloud.com/aws_alerts_get_user_data', authorize_params={'prompt': 'login'} )
  #return redirect(aws_auth.get_sign_in_url())
  pass


@app.route('/aws_login')
#@cognito_login
def aws_login():
  
  session.clear()

  #return oauth_aws.oidc.authorize_redirect('https://www.helmsmart-cloud.com/aws_alerts_get_user_data')
  #return oauth_aws.oidc.authorize_redirect('https://www.helmsmart-cloud.com/aws_alerts_get_user_data?login_hint=someone')
  #return oauth_aws.oidc.authorize_redirect('https://www.helmsmart-cloud.com/aws_alerts_get_user_data', authorize_params={'prompt': 'login'} )
  return redirect(aws_auth.get_sign_in_url())
  pass

@app.route('/authorize')
def authorize():
    token = oauth_aws.oidc.authorize_access_token()
    user = token['userinfo']
    session['user'] = user
    return redirect(url_for('aws_details'))

@app.route('/aws_details')
def aws_details():
    user = session.get('user')
    if user:
        return  f'Hello, {user["email"]}. <a href="/logout">Logout</a>'
    else:
        return f'Welcome! Please <a href="/login">Login</a>.'



@app.route('/user_subscription_updated')
def user_subscription_updated():

  return render_template(
    'user_subscription_updated.html',
    features = [],
  )

@app.route('/user_subscription_added')
def user_subscription_added():

  return render_template(
    'user_subscription_added.html',
    features = [],
  )


@app.route('/manage')
def manage():

  return render_template(
    'manage.html',
    features = [],
  )

@app.route('/adminmanage')
def adminmanage():

  return render_template(
    'adminmanage.html',
    features = [],
  )

@app.route('/downloads')
def downloads():

  return render_template(
    'downloads.html',
    features = [],
  )


@app.route('/alertsmart')
def alertsmart():
  #userid=""
  #userid = request.args.get('userid','')

  return render_template(
    'netalerts.html',
    #admin_userid=userid,
    features = [],
  )

@app.route('/mapsmart')
def mapsmart():

  return render_template(
    'mapsmart.html',
    features = [],
  )

@app.route('/graphsmart')
def graphsmart():

  return render_template(
    'graphsmart.html',
    features = [],
  )



@app.route('/meshdimmer')
def meshdimmer():

  return render_template(
    'meshdimmer.html',
    features = [],
  )

@app.route('/netgauges')
def netgauges():

  return render_template(
    'netgauges.html',
    features = [],
  )

@app.route('/netgauges_public')
def netgauges_public():

  deviceapikey = request.args.get('deviceapikey', '')
  prefkey = request.args.get('prefkey', 0)
  userid = request.args.get('userid', 'a91140300971bfb9244989a9bffde53c')
  
  deviceid, userid = getdevicekeys(deviceapikey)

  return render_template(
    'netgauges_public.html',
    deviceid=deviceid,
    userid=userid,
    pagetype=0,
    prefkey=prefkey
  )


@app.route('/netswitch')
def netswitch():

  return render_template(
    'netswitch.html',
    features = [],
  )


@app.route('/netdimmer')
def netdimmer():

  return render_template(
    'netdimmer.html',
    features = [],
  )

@app.route('/seagaugeg4_config')
def seagaugeg4_config():

  return render_template(
    'seagauge_conf.html',
    features = [],
  )

@app.route('/dashboard_api')
def dashboardapi():

  return render_template(
    'dashboard_api.html',
    features = [],
  )


@app.route('/dashboards_list')
@cross_origin()
def dashboards_list():

    log.info("dashboards_list.html: Start")

      
    try:
      
      if session['profile'] is not None:
        try:
          mydata = session['profile']
          log.info("dashboards_list.html: customdata:%s", mydata)
         

          if mydata['name'] is not None:
            #myusername = mydata['name']
            myusername = mydata['email']
            log.info("dashboards_list.html: myusername:%s", myusername)


          """
          if mydata['devices'] is not None:
            mydevices = mydata['devices']
            log.info("index.html: mydevices:%s", mydevices)

            for device in mydevices:
              log.info("index.html: mydevice  %s:%s", device['devicename'], device['deviceid'])
          """
          
        except:
          e = sys.exc_info()[0]
          log.info('dashboards_list.html: Error in geting user.custom_data  %s:  ' % str(e))
          pass

        try:
          if myusername is not None:

            conn = db_pool.getconn()
            session['username'] = myusername
            
            log.info("dashboards_list.html: email:%s", myusername )

            query = "select userid from user_devices where useremail = %s group by userid"

            cursor = conn.cursor()
            cursor.execute(query, [myusername])
            i = cursor.fetchone()       
            if cursor.rowcount > 0:

                session['userid'] = str(i[0])
                log.info('dashboards_list.html: got user from database userid is  %s:  ' , session['userid'] )
                
            else:
                session['userid'] = hash_string('helmsmart@mockmyid.com')
                log.info('dashboards_list.html: using default userid is  %s:  ' , session['userid'] )
                
            log.info('dashboards_list.html: userid is  %s:  ' , session['userid'] )
            # cursor.close
            db_pool.putconn(conn)
            
        except:
          e = sys.exc_info()[0]
          log.info('dashboards_list.html: Error in geting user.email  %s:  ' % str(e))
          pass


        return render_template('dashboards_list.html', user=session['profile'], env=env)
        #return render_template("authohome.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
      


    except TypeError as e:
      #log.info('dashboards_list: TypeError in  update pref %s:  ', userid)
      log.info('dashboards_list: TypeError in  update pref  %s:  ' % str(e))

    except ValueError as e:
      #log.info('dashboards_list: ValueError in  update pref  %s:  ', userid)
      log.info('dashboards_list: ValueError in  update pref %s:  ' % str(e))
      
    except KeyError as e:
      #log.info('dashboards_list: KeyError in  update pref  %s:  ', userid)
      log.info('dashboards_list: KeyError in  update pref  %s:  ' % str(e))

    except NameError as e:
      #log.info('dashboards_list: NameError in  update pref  %s:  ', userid)
      log.info('dashboards_list: NameError in  update pref %s:  ' % str(e))
          
    except IndexError as e:
      #log.info('dashboards_list: IndexError in  update pref  %s:  ', userid)
      log.info('dashboards_list: IndexError in  update pref  %s:  ' % str(e))  

    except:
      e = sys.exc_info()[0]
      log.info('dashboards_list.html: Error in geting user  %s:  ' % str(e))
      pass

    
    return render_template('dashboards_list.html',  env=env)
    #return render_template("authohome.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

    #response = make_response(render_template('index.html', features = []))
    #response.headers['Cache-Control'] = 'public, max-age=0'
    #return response







@app.route('/login')
@cross_origin()
#@login_required
def login():

    log.info('auth0login: AUTH0_CALLBACK_URL %s:  ' , AUTH0_CALLBACK_URL)
    
    #response = make_response(render_template('freeboard.html', features = []))

    #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, post-check=0, pre-check=0, max-age=0'
    #response.headers['Pragma'] = 'no-cache'
    #response.headers['Expires'] = '-1'
    #return response  
    #return render_template("authohome.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
    #return oauth.auth0.authorize_redirect( redirect_uri=url_for("callback", _external=True) )

    #return oauth.auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE, screen_hint=signup)
    return oauth.auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL)

@app.route('/oldauth0logout')
def auth0logout():
    session.clear()
    log.info('auth0logout: AUTH0_CALLBACK_URL %s:  ' , AUTH0_CALLBACK_URL)
    parsed_base_url = urlparse(AUTH0_CALLBACK_URL)
    #base_url = parsed_base_url.scheme + '://' + parsed_base_url.netloc
    base_url = 'http://' + parsed_base_url.netloc
    log.info('auth0logout: base_url %s:  ' , base_url)
    
    log.info('auth0logout: https://%s/v2/logout?returnTo=%s&client_id=%s' % (AUTH0_DOMAIN, base_url, AUTH0_CLIENT_ID))
    #return jsonify(status='ok' )
      
    return redirect('https://%s/v2/logout?returnTo=%s&client_id=%s' % (AUTH0_DOMAIN, base_url, AUTH0_CLIENT_ID))
  

@app.route("/auth0logout")
def logout():
    session.clear()

    parsed_base_url = urlparse(AUTH0_CALLBACK_URL)
    #base_url = parsed_base_url.scheme + '://' + parsed_base_url.netloc
    base_url = 'http://' + parsed_base_url.netloc
    log.info('auth0logout: base_url %s:  ' , base_url)

    
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": base_url,
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route('/callback')
def callback_handling():
    code = request.args.get('code')
    log.info('auth0callback: code %s:  ' , code)
    #get_token = GetToken(AUTH0_DOMAIN)
    #auth0_users = Users(AUTH0_DOMAIN)
    #token = get_token.authorization_code(AUTH0_CLIENT_ID,  AUTH0_CLIENT_SECRET, code, AUTH0_CALLBACK_URL)
    #user_info = auth0_users.userinfo(token['access_token'])


    token = oauth.auth0.authorize_access_token()
    session["user"] = token

    user_info = token.get('userinfo')
    
    log.info('auth0callback: user_info %s:  ' , user_info)



    try:
      #session['profile'] = json.loads(user_info)
      user_info_json = json.dumps(user_info)
      log.info('auth0callback: TypeError in user_info %s:  ', user_info_json)
      
      session['profile'] =json.loads(user_info_json)
      log.info('auth0callback: TypeError in session user_info %s:  ', session)
      
    except TypeError as e:
      log.info('auth0callback: TypeError in user_info %s:  ', user_info_json)
      #e = sys.exc_info()[0]

      log.info('auth0callback: TypeError in user_info %s:  ' % str(e))
      
    except:
      e = sys.exc_info()[0]
      log.info('auth0callback: Error in geting username  %s:  ' % str(e))
    
 

    
    
    if 'profile' in session:
      try:
        mydata = session['profile']   
        log.info("authcallback: customdata:%s", mydata)

        if 'name' in mydata:
          myusername = mydata['name']
          session['username'] = myusername
          log.info("authcallback: username:%s", myusername)

      except TypeError as e:
        log.info('auth0callback: TypeError in customdata %s:  ', mydata)
        #e = sys.exc_info()[0]
          
      except:
        e = sys.exc_info()[0]
        log.info('auth0callback: Error in geting username from profile  %s:  ' % str(e))
        pass

        
    #return redirect('/dashboards_list')
    return redirect('/')


@app.route('/dashboards')
@cross_origin()
def dashboards():



    response = make_response(render_template('dashboards.html', features = []))
    #response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    #response.headers['Cache-Control'] = 'public, no-cache, no-store, max-age=0'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
  

@app.route('/dashboard')
#@login_required
@cross_origin()
#@requires_auth

def dashboard():

  log.info("dashboard.html: START ****" )

  try:
    
    if session['profile'] is not None:
      
      try:
        mydata = session['profile']
        log.info("dashboard: customdata:%s", mydata)
        
      
        if mydata is not None:
          user_email = mydata['name']
          session['useremail']= mydata['name']
          log.info("dashboard.html: user exists:%s", user_email)
          
        else:
          user_email ="guest@helmsmart.com"
         
      except:
        e = sys.exc_info()[0]
        log.info('dashboard.html: Error in geting user.custom_data  %s:  ' % str(e))
        return render_template('dashboards_list.html', user=session['profile'], env=env) 

    session['userid'] = user_db_functions.getuserid(user_email)

    log.info("dashboard.html: userid:%s", session['userid'])

    response = make_response(render_template('dashboard.html', features = []))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
  
  except:
    e = sys.exc_info()[0]
    log.info('dashboard.html error: Error in adding device %s:  ' % e)
    return render_template('dashboards_list.html',  env=env)

#  finally:
#    return render_template('dashboards_list.html',  env=env)


@app.route('/freeboard_getdashboardjson')
@cross_origin()
def freeboard_getdashboardjson():

  prefuid = request.args.get('prefuid',1)


  #dashboardjson = getdashboardjson(prefuid)
  dashboardjson = user_db_functions.getdashboardjson(prefuid)

  
  log.info("freeboard_GetDashboardJSON prefuid %s -> %s", prefuid, dashboardjson)


  #return dashboardjson  
  #  result = json.dumps(r, cls=DateEncoder)

  response = make_response(dashboardjson)
  response.headers['Cache-Control'] = 'public, max-age=0'
  response.headers['content-type'] = "application/json"
  return response



@app.route('/freeboard_getdashboardlist')
@cross_origin()
def freeboard_getdashboardlist():

    userid = request.args.get('userid',1)


    #dashboardlists = helmsmartmodules.user_db_functions.getdashboardlists(userid)
    dashboardlists = user_db_functions.getdashboardlists(userid)
    
    log.info("freeboard_GetDashboardJSON prefuid %s ", userid)
    log.info("freeboard_GetDashboardJSON dashboardlists %s ",  jsonify(dashboardlists))


    return jsonify({'preferences':dashboardlists})
  #  result = json.dumps(r, cls=DateEncoder)

# ######################################################
# send test email
# #####################################################
def send_raw_email(source, destination, subject, text, html, reply_tos=None):

        message_id=""

        # The character encoding for the email.
        email_charset = "UTF-8"
        email_msg = MIMEMultipart('mixed')
        # Add subject, from and to lines.
        email_msg['Subject'] =subject
        email_msg['From'] = source
        email_msg['To'] = destination
        #email_msg['Cc'] = ', '.join(email Cc list)
        #email_msg['Bcc'] = ', '.join(email bcc list)
        email_msg_body = MIMEMultipart('alternative')
        textpart = MIMEText(text.encode(email_charset), 'plain', email_charset)
        htmlpart = MIMEText(html.encode(email_charset), 'html', email_charset)
        # Add the text and HTML parts to the child container.
        email_msg_body.attach(textpart)
        email_msg_body.attach(htmlpart)
        # Attach the multipart/alternative child container to the multipart/mixed
        # parent container.
        email_msg.attach(email_msg_body)

        
        try:
          #response = email_ses_client.send_email(**send_args)

          response = email_ses_client.send_raw_email(
                              Source=email_msg['From'],
                              #Destinations= email to list + emaom cc list + email bcc list,
                              Destinations= [],
                              RawMessage={
                                  'Data': email_msg.as_string(),
                              }
                          )

            
          message_id = response["MessageId"]
          log.info(  "Sent raw mail %s from %s to %s.", message_id, source, destination )
            
          return message_id
          
        #except ClientError as e:
        except botocore.exceptions.ClientError as e:
          log.info('send_email: ClientError  %s:  ' % str(e))

        except botocore.exceptions.ParamValidationError as e:
          log.info('send_email:ParamValidationError %s:  ' % e)
          
        except:
          e = sys.exc_info()[0]
          log.info('send_email error: ERROR %s:  ' % e)
  

def send_email(source, destination, subject, text, html, reply_tos=None):
        """
        Sends an email.

        Note: If your account is in the Amazon SES  sandbox, the source and
        destination email accounts must both be verified.

        :param source: The source email account.
        :param destination: The destination email account.
        :param subject: The subject of the email.
        :param text: The plain text version of the body of the email.
        :param html: The HTML version of the body of the email.
        :param reply_tos: Email accounts that will receive a reply if the recipient
                          replies to the message.
        :return: The ID of the message, assigned by Amazon SES.
        """

        message_id=""
        
        try:
            #response = email_ses_client.send_email(**send_args)

            response = email_ses_client.send_email(
                Destination={
                    'BccAddresses': [
                    ],
                    'CcAddresses': [
                    ],
                    'ToAddresses': [
                        destination,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': 'UTF-8',
                            'Data': html,
                        },
                        'Text': {
                            'Charset': 'UTF-8',
                            'Data': text,
                        },
                    },
                    'Subject': {
                        'Charset': 'UTF-8',
                        'Data': subject,
                    },
                },
                Source = source,
            )


            
            message_id = response["MessageId"]
            log.info(  "Sent mail %s from %s to %s.", message_id, source, destination )
            
            return message_id
          
        #except ClientError as e:
        except botocore.exceptions.ClientError as e:
          log.info('send_email: ClientError  %s:  ' % str(e))

        except botocore.exceptions.ParamValidationError as e:
          log.info('send_email:ParamValidationError %s:  ' % e)
          
        except:
          e = sys.exc_info()[0]
          log.info('send_email error: ERROR %s:  ' % e)
    






@app.route('/send_test_email')
def sendtestemail():

    #source = "joe@chetcodigital.com"
    source = "alerts@helmsmart-cloud.com"
    destination = "joe@seagauge.com"
    subject = "test aws ses raw email"
    text = "SSWIFIG2_SEADREAM ALARM Message alarmemail: /M2M/Battery/Battery Volts Port is low – mean = 14.38 threshold: 15 timestamp is:2019-02-13T20:48:00Z"
    html = "<p>SSWIFI4G_DD30 ALARM Message alarmemail: /General/Heartbeat value is missing for Interval= 1min timestamp is:2018-10-12 18:11:09</p>"



    log.info("sendtestemail_endpoint ")
    #message_id = send_email(source, destination, subject, text, html, reply_tos=None)
    message_id = send_raw_email(source, destination, subject, text, html, reply_tos=None)
    
    log.info("sendtestemail_endpoint message_id = %s", message_id)

    response = make_response("success")
    response.headers['content-type'] = "application/json"
    return response

@app.route('/send_test_sms')
def sendtestsms():

    source = "joe@chetcodigital.com"
    destination = "joe@seagauge.com"
    subject = "test aws ses raw email"
    text = "SSWIFIG2_SEADREAM ALARM Message alarmemail: /M2M/Battery/Battery Volts Port is low – mean = 14.38 threshold: 15 timestamp is:2019-02-13T20:48:00Z"
    html = "<p>SSWIFI4G_DD30 ALARM Message alarmemail: /General/Heartbeat value is missing for Interval= 1min timestamp is:2018-10-12 18:11:09</p>"



    log.info("sendtestsms ")
    #message_id = send_email(source, destination, subject, text, html, reply_tos=None)
    #message_id = send_raw_email(source, destination, subject, text, html, reply_tos=None)
    response = email_ses_client.publish( PhoneNumber="+15416612051", Message=text )
    log.info("sendtestsms message_id = %s", response)

    response = make_response("success")
    response.headers['content-type'] = "application/json"
    return response

"""
def create_seasmart_resets_xml(postdata):

  log.info("create_seasmart_device_xml postdata %s", postdata)


  xmlfile = ''
  
  xmlfile = xmlfile + '<configrecord version="24.12.20">\r\n'
  xmlfile = xmlfile + '<configgroup name = "XMLACTION">\r\n'
  xmlfile = xmlfile + '<configitem name="LOADXML"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Save_NVRAM"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'
  xmlfile = xmlfile + '<configgroup name = "DEVICE">\r\n'
  xmlfile = xmlfile + '<configitem name="DeviceID"><value>'+  get_xml_value(postdata, "DeviceID") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="VersionInfo"><value>'+  get_xml_value(postdata, "DeviceID") +'</value></configitem>\r\n'
  
  xmlfile = xmlfile + '<configgroup name = "RuntimePulse">\r\n'
  xmlfile = xmlfile + '<configitem name="PulseRTTotal00"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PulseRTTotal01"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PulseRTTotal02"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="FuelRTTotal00"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="FuelRTTotal01"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="FuelRTTotal02"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configgroup name = "RuntimePIO">\r\n'
  xmlfile = xmlfile + '<configitem name="PIORTTotal00"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PIORTTotal01"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PIORTTotal02"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PIORTTotal03"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PIOCycle00"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PIOCycle01"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PIOCycle02"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PIOCycle03"><value>0</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'

  return  xmlfile


def create_seasmart_pulse_xml(postdata):

  log.info("create_seasmart_pulse_xml postdata %s", postdata)

  xmlfile = ''
  xmlfile = xmlfile +  '<?xml version="1.0" standalone="yes"?>\r\n'
  xmlfile = xmlfile + '<configrecord version="24.12.20">\r\n'
  xmlfile = xmlfile + '<configgroup name = "XMLACTION">\r\n'
  xmlfile = xmlfile + '<configitem name="LOADXML"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Save_NVRAM"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'
  xmlfile = xmlfile + '<configgroup name = "DEVICE">\r\n'
  xmlfile = xmlfile + '<configitem name="DeviceID"><value>'+  get_xml_value(postdata, "DeviceID") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="VersionInfo"><value>'+  get_xml_value(postdata, "VersionInfo") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'

  xmlfile = xmlfile + '<configgroup name = "PULSE">\r\n'
  xmlfile = xmlfile + '<configitem name="PulseMode"><value>'+  get_xml_value(postdata, "PULSEMODE") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Pulse0Scale"><value>'+  get_xml_value(postdata, "PULSESCALE0") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Pulse1Scale"><value>'+  get_xml_value(postdata, "PULSESCALE2") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Pulse2Scale"><value>'+  get_xml_value(postdata, "PULSESCALE2") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PulseInterval"><value>'+  get_xml_value(postdata, "PINTERVAL") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="FlowPulseInterval"><value>'+  get_xml_value(postdata, "FINTERVAL") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Pulse0Filter"><value>'+  get_xml_value(postdata, "PFLT0") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Pulse1Filter"><value>'+  get_xml_value(postdata, "PFLT1") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Pulse2Filter"><value>'+  get_xml_value(postdata, "PFLT2") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'


  return  xmlfile


def set_seasmart_pulse_xml(postdata):

  log.info("set_seasmart_pulse_xml postdata", postdata)
  


  pulsexml = ""
  pulsexml = pulsexml +  '<DeviceID>'     +  request.args.get('DeviceIDXML','')       + '</DeviceID>'
  pulsexml = pulsexml +  '<VersionInfo>'  +  request.args.get('VersionXML','')          + '</VersionInfo>'
  pulsexml = pulsexml +  '<PULSEMODE>'    +  request.args.get('PULSEModeDD','')  + '</PULSEMODE>'
  pulsexml = pulsexml +  '<PULSESCALE0>'    +  request.args.get('PULSE0SCALE','')  + '</PULSESCALE0>'  
  pulsexml = pulsexml +  '<PULSESCALE1>'    +  request.args.get('PULSE1SCALE','')  + '</PULSESCALE1>'  
  pulsexml = pulsexml +  '<PULSESCALE2>'    +  request.args.get('PULSE2SCALE','')  + '</PULSESCALE2>'  
  #pulsexml = pulsexml +  '<PINTERVAL>'    +  request.args.get('SDLogFName','')  + '</PINTERVAL>'  
  #pulsexml = pulsexml +  '<FINTERVAL>'    +  request.args.get('SDLogFName','')  + '</FINTERVAL>'
  pulsexml = pulsexml +  '<PINTERVAL>'    +  '1000'  + '</PINTERVAL>'  
  pulsexml = pulsexml +  '<FINTERVAL>'    +  '4000'  + '</FINTERVAL>'  
  pulsexml = pulsexml +  '<PFLT0>'    +  request.args.get('PULSE0FILTER','')  + '</PFLT0>'  
  pulsexml = pulsexml +  '<PFLT1>'    +  request.args.get('PULSE1FILTER','')  + '</PFLT1>'  
  pulsexml = pulsexml +  '<PFLT2>'    +  request.args.get('PULSE2FILTER','')  + '</PFLT2>'  
  pulsexml = pulsexml +  '<FUELTOTAL>'    +  request.args.get('FUELTACHTOTAL','')  + '</FUELTOTAL>'  

 


  prefidkey=1

  try:  
    conn = db_pool.getconn()

  except:
    e = sys.exc_info()[0]
    #log.info("getuser_endpoint error - db_pool.getconn %s", deviceid)
    log.info("getuser_endpoint error - db_pool.getconn ")
    log.info('getuser_endpoint error: db_pool.getconn %s:  ' % e)
    db_pool.closeall()  
  
  cursor = conn.cursor()
  sqlstr = " update user_sgg4configxml SET pulsexml =%s where  prefidkey = %s;" 
  cursor.execute(sqlstr, (pulsexml, prefidkey, ))   
  conn.commit()



 
  log.info("set_seasmart_device_xml pulsexml %s", pulsexml)  
  return  




def get_hex2_from_tag(postdata, tag):

  try:
    
    index =int(get_xml_value(postdata, tag))

    log.info("get_hex2_from_tag index %s", index)  

    #return '0x' + format(index, '02x')
    return '0x' + '{:02X}'.format(index & ((1 << 8)-1))
  
  except:
    return '0xFF'

    
def get_hex4_from_tag(postdata, tag):
  
  try:

    log.info("get_hex4_from_tag index1 %s", get_xml_value(postdata, tag))
    
    index =int(get_xml_value(postdata, tag))  

    log.info("get_hex4_from_tag index2 %s", index)
    
    #return format(index, '#010x')
    return '0x' + '{:04X}'.format(index & ((1 << 16)-1))
  
  except:
    return '0xFFFF'
  
def get_hex8_from_tag(postdata, tag):
  
  try:
    
    index =int(get_xml_value(postdata, tag))  

    log.info("get_hex8_from_tag index %s", index)
    
    #return format(index, '#010x')
    return '0x' + '{:08X}'.format(index & ((1 << 32)-1))
  
  except:
    return '0xFFFFFFFF'
  
def get_pgnhex_from_tag(postdata, tag):


  index =int(get_xml_value(postdata, tag))

  if index == 0:
    return "0x000000"

  elif index ==1:
    return "0x1F201"

  elif index ==2:
    return "0x1F214"

  elif index ==3:
    return "0x1F211"

  elif index ==4:
    return "0x1F205"

  elif index ==5:
    return "0x1FD0A"

  elif index ==6:
    return "0x1FD07"

  elif index ==7:
    return "0x1FD08"

  elif index ==8:
    return "0x1FD0C"

  elif index ==9:
    return "0x1F10D"

  elif index == 10:
    return "0x1F200"

  elif index ==11:
    return "0x000000"

  elif index ==12:
    return "0x000000"

  elif index ==13:
    return "0x000000"

  elif index ==14:
    return "0x000000"

  elif index ==15:
    return "0x000000"

  elif index ==16:
    return "0x0FEEE"

  elif index ==17:
    return "0x0FEEF"

  elif index ==18:
    return "0x0FEF7"

  elif index ==19:
    return "0x0FEFC"
  
  elif index == 20:
    return "0x0FEF8"

  else:
    return "0x000000"

  
def create_seasmart_pgn_xml(postdata):

  log.info("create_seasmart_pgn_xml postdata %s", postdata)

  xmlfile = ''
  xmlfile = xmlfile +  '<?xml version="1.0" standalone="yes"?>\r\n'
  xmlfile = xmlfile + '<configrecord version="24.12.20">\r\n'
  xmlfile = xmlfile + '<configgroup name = "XMLACTION">\r\n'
  xmlfile = xmlfile + '<configitem name="LOADXML"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Save_NVRAM"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'
  xmlfile = xmlfile + '<configgroup name = "DEVICE">\r\n'
  xmlfile = xmlfile + '<configitem name="DeviceID"><value>'+  get_xml_value(postdata, "DeviceID") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="VersionInfo"><value>'+  get_xml_value(postdata, "VersionInfo") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'

  xmlfile = xmlfile + '<configgroup name = "N2KPGNLists">\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN00"><value>' + get_pgnhex_from_tag(postdata, "PGNN0") + ',' + get_hex2_from_tag(postdata, "PGNI0") + ',' +  get_hex2_from_tag(postdata, "PGNP0") +',' + get_hex8_from_tag(postdata, "PGNS0") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN1") + ',' + get_hex2_from_tag(postdata, "PGNI1") + ',' +  get_hex2_from_tag(postdata, "PGNP1") +',' + get_hex8_from_tag(postdata, "PGNS1") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN2") + ',' + get_hex2_from_tag(postdata, "PGNI2") + ',' +  get_hex2_from_tag(postdata, "PGNP2") +',' + get_hex8_from_tag(postdata, "PGNS2") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN3") + ',' + get_hex2_from_tag(postdata, "PGNI3") + ',' +  get_hex2_from_tag(postdata, "PGNP3") +',' + get_hex8_from_tag(postdata, "PGNS3") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN4") + ',' + get_hex2_from_tag(postdata, "PGNI4") + ',' +  get_hex2_from_tag(postdata, "PGNP4") +',' + get_hex8_from_tag(postdata, "PGNS4") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN5") + ',' + get_hex2_from_tag(postdata, "PGNI5") + ',' +  get_hex2_from_tag(postdata, "PGNP5") +',' + get_hex8_from_tag(postdata, "PGNS5") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN6") + ',' + get_hex2_from_tag(postdata, "PGNI6") + ',' +  get_hex2_from_tag(postdata, "PGNP6") +',' + get_hex8_from_tag(postdata, "PGNS6") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN7") + ',' + get_hex2_from_tag(postdata, "PGNI7") + ',' +  get_hex2_from_tag(postdata, "PGNP7") +',' + get_hex8_from_tag(postdata, "PGNS7") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN8") + ',' + get_hex2_from_tag(postdata, "PGNI8") + ',' +  get_hex2_from_tag(postdata, "PGNP8") +',' + get_hex8_from_tag(postdata, "PGNS8") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN9") + ',' + get_hex2_from_tag(postdata, "PGNI9") + ',' +  get_hex2_from_tag(postdata, "PGNP9") +',' + get_hex8_from_tag(postdata, "PGNS9") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN10") + ',' + get_hex2_from_tag(postdata, "PGNI10") + ',' +  get_hex2_from_tag(postdata, "PGNP10") +',' + get_hex8_from_tag(postdata, "PGNS10") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KPGN01"><value>' + get_pgnhex_from_tag(postdata, "PGNN11") + ',' + get_hex2_from_tag(postdata, "PGNI11") + ',' +  get_hex2_from_tag(postdata, "PGNP11") +',' + get_hex8_from_tag(postdata, "PGNS11") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'

  xmlfile = xmlfile + '<configgroup name = "N2KCalibrationTables">\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL00"><value>'+  get_xml_value(postdata, "CAL0") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL01"><value>'+  get_xml_value(postdata, "CAL1") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL02"><value>'+  get_xml_value(postdata, "CAL2") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL03"><value>'+  get_xml_value(postdata, "CAL3") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL04"><value>'+  get_xml_value(postdata, "CAL4") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL05"><value>'+  get_xml_value(postdata, "CAL5") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL06"><value>'+  get_xml_value(postdata, "CAL6") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL07"><value>'+  get_xml_value(postdata, "CAL7") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL08"><value>'+  get_xml_value(postdata, "CAL8") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL09"><value>'+  get_xml_value(postdata, "CAL9") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL10"><value>'+  get_xml_value(postdata, "CAL10") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2KCAL11"><value>'+  get_xml_value(postdata, "CAL11") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'

  xmlfile = xmlfile + '<configgroup name = "ADCAlarms">\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM00"><value>'+ get_hex2_from_tag(postdata, "ADCAM0") + ',' +  get_hex4_from_tag(postdata, "ADCAL0") + ',' + get_hex4_from_tag(postdata, "ADCAH0")+ ',' + get_hex2_from_tag(postdata, "ADCAA0") + ',' + get_hex2_from_tag(postdata, "ADCAP0") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM01"><value>'+ get_hex2_from_tag(postdata, "ADCAM1") + ',' +  get_hex4_from_tag(postdata, "ADCAL1") + ',' + get_hex4_from_tag(postdata, "ADCAH1")+ ',' + get_hex2_from_tag(postdata, "ADCAA1") + ',' + get_hex2_from_tag(postdata, "ADCAP1") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM02"><value>'+ get_hex2_from_tag(postdata, "ADCAM2") + ',' +  get_hex4_from_tag(postdata, "ADCAL2") + ',' + get_hex4_from_tag(postdata, "ADCAH2")+ ',' + get_hex2_from_tag(postdata, "ADCAA2") + ',' + get_hex2_from_tag(postdata, "ADCAP2") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM03"><value>'+ get_hex2_from_tag(postdata, "ADCAM3") + ',' +  get_hex4_from_tag(postdata, "ADCAL3") + ',' + get_hex4_from_tag(postdata, "ADCAH3")+ ',' + get_hex2_from_tag(postdata, "ADCAA3") + ',' + get_hex2_from_tag(postdata, "ADCAP3") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM04"><value>'+ get_hex2_from_tag(postdata, "ADCAM4") + ',' +  get_hex4_from_tag(postdata, "ADCAL4") + ',' + get_hex4_from_tag(postdata, "ADCAH4")+ ',' + get_hex2_from_tag(postdata, "ADCAA4") + ',' + get_hex2_from_tag(postdata, "ADCAP4") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM05"><value>'+ get_hex2_from_tag(postdata, "ADCAM5") + ',' +  get_hex4_from_tag(postdata, "ADCAL5") + ',' + get_hex4_from_tag(postdata, "ADCAH5")+ ',' + get_hex2_from_tag(postdata, "ADCAA5") + ',' + get_hex2_from_tag(postdata, "ADCAP5") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM06"><value>'+ get_hex2_from_tag(postdata, "ADCAM6") + ',' +  get_hex4_from_tag(postdata, "ADCAL6") + ',' + get_hex4_from_tag(postdata, "ADCAH6")+ ',' + get_hex2_from_tag(postdata, "ADCAA6") + ',' + get_hex2_from_tag(postdata, "ADCAP6") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM07"><value>'+ get_hex2_from_tag(postdata, "ADCAM7") + ',' +  get_hex4_from_tag(postdata, "ADCAL7") + ',' + get_hex4_from_tag(postdata, "ADCAH7")+ ',' + get_hex2_from_tag(postdata, "ADCAA7") + ',' + get_hex2_from_tag(postdata, "ADCAP7") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM08"><value>'+ get_hex2_from_tag(postdata, "ADCAM8") + ',' +  get_hex4_from_tag(postdata, "ADCAL8") + ',' + get_hex4_from_tag(postdata, "ADCAH8")+ ',' + get_hex2_from_tag(postdata, "ADCAA8") + ',' + get_hex2_from_tag(postdata, "ADCAP8") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM09"><value>'+ get_hex2_from_tag(postdata, "ADCAM9") + ',' +  get_hex4_from_tag(postdata, "ADCAL9") + ',' + get_hex4_from_tag(postdata, "ADCAH9")+ ',' + get_hex2_from_tag(postdata, "ADCAA9") + ',' + get_hex2_from_tag(postdata, "ADCAP9") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM10"><value>'+ get_hex2_from_tag(postdata, "ADCAM10") + ',' +  get_hex4_from_tag(postdata, "ADCAL10") + ',' + get_hex4_from_tag(postdata, "ADCAH10")+ ',' + get_hex2_from_tag(postdata, "ADCAA10") + ',' + get_hex2_from_tag(postdata, "ADCAP10") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM11"><value>'+ get_hex2_from_tag(postdata, "ADCAM11") + ',' +  get_hex4_from_tag(postdata, "ADCAL11") + ',' + get_hex4_from_tag(postdata, "ADCAH11")+ ',' + get_hex2_from_tag(postdata, "ADCAA11") + ',' + get_hex2_from_tag(postdata, "ADCAP11") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM12"><value>'+ get_hex2_from_tag(postdata, "ADCAM12") + ',' +  get_hex4_from_tag(postdata, "ADCAL12") + ',' + get_hex4_from_tag(postdata, "ADCAH12")+ ',' + get_hex2_from_tag(postdata, "ADCAA12") + ',' + get_hex2_from_tag(postdata, "ADCAP12") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM13"><value>'+ get_hex2_from_tag(postdata, "ADCAM13") + ',' +  get_hex4_from_tag(postdata, "ADCAL13") + ',' + get_hex4_from_tag(postdata, "ADCAH13")+ ',' + get_hex2_from_tag(postdata, "ADCAA13") + ',' + get_hex2_from_tag(postdata, "ADCAP13") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM14"><value>'+ get_hex2_from_tag(postdata, "ADCAM14") + ',' +  get_hex4_from_tag(postdata, "ADCAL14") + ',' + get_hex4_from_tag(postdata, "ADCAH14")+ ',' + get_hex2_from_tag(postdata, "ADCAA14") + ',' + get_hex2_from_tag(postdata, "ADCAP14") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM15"><value>'+ get_hex2_from_tag(postdata, "ADCAM15") + ',' +  get_hex4_from_tag(postdata, "ADCAL15") + ',' + get_hex4_from_tag(postdata, "ADCAH15")+ ',' + get_hex2_from_tag(postdata, "ADCAA15") + ',' + get_hex2_from_tag(postdata, "ADCAP15") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM16"><value>'+ get_hex2_from_tag(postdata, "ADCAM16") + ',' +  get_hex4_from_tag(postdata, "ADCAL16") + ',' + get_hex4_from_tag(postdata, "ADCAH16")+ ',' + get_hex2_from_tag(postdata, "ADCAA16") + ',' + get_hex2_from_tag(postdata, "ADCAP16") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM17"><value>'+ get_hex2_from_tag(postdata, "ADCAM17") + ',' +  get_hex4_from_tag(postdata, "ADCAL17") + ',' + get_hex4_from_tag(postdata, "ADCAH17")+ ',' + get_hex2_from_tag(postdata, "ADCAA17") + ',' + get_hex2_from_tag(postdata, "ADCAP17") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM18"><value>'+ get_hex2_from_tag(postdata, "ADCAM18") + ',' +  get_hex4_from_tag(postdata, "ADCAL18") + ',' + get_hex4_from_tag(postdata, "ADCAH18")+ ',' + get_hex2_from_tag(postdata, "ADCAA18") + ',' + get_hex2_from_tag(postdata, "ADCAP18") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="ADCALARM19"><value>'+ get_hex2_from_tag(postdata, "ADCAM19") + ',' +  get_hex4_from_tag(postdata, "ADCAL19") + ',' + get_hex4_from_tag(postdata, "ADCAH19")+ ',' + get_hex2_from_tag(postdata, "ADCAA19") + ',' + get_hex2_from_tag(postdata, "ADCAP19") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'



  return  xmlfile


def set_seasmart_pgn_xml(postdata):

  log.info("set_seasmart_pgn_xml postdata", postdata)
  


  pgnxml = ""
  pgnxml = pgnxml +  '<DeviceID>'     +  request.args.get('DeviceIDXML','')       + '</DeviceID>'
  pgnxml = pgnxml +  '<VersionInfo>'  +  request.args.get('VersionXML','')          + '</VersionInfo>'
  pgnxml = pgnxml +  '<ADCAA0>'    +  request.args.get('ADCAA0','')  + '</ADCAA0>'
  pgnxml = pgnxml +  '<ADCAA1>'    +  request.args.get('ADCAA1','')  + '</ADCAA1>'
  pgnxml = pgnxml +  '<ADCAA2>'    +  request.args.get('ADCAA2','')  + '</ADCAA2>'
  pgnxml = pgnxml +  '<ADCAA3>'    +  request.args.get('ADCAA3','')  + '</ADCAA3>'
  pgnxml = pgnxml +  '<ADCAA4>'    +  request.args.get('ADCAA4','')  + '</ADCAA4>'
  pgnxml = pgnxml +  '<ADCAA5>'    +  request.args.get('ADCAA5','')  + '</ADCAA5>'
  pgnxml = pgnxml +  '<ADCAA6>'    +  request.args.get('ADCAA6','')  + '</ADCAA6>'
  pgnxml = pgnxml +  '<ADCAA7>'    +  request.args.get('ADCAA7','')  + '</ADCAA7>'
  pgnxml = pgnxml +  '<ADCAA8>'    +  request.args.get('ADCAA8','')  + '</ADCAA8>'
  pgnxml = pgnxml +  '<ADCAA9>'    +  request.args.get('ADCAA9','')  + '</ADCAA9>'
  pgnxml = pgnxml +  '<ADCAA10>'    +  request.args.get('ADCAA10','')  + '</ADCAA10>'
  pgnxml = pgnxml +  '<ADCAA11>'    +  request.args.get('ADCAA11','')  + '</ADCAA11>'
  pgnxml = pgnxml +  '<ADCAA12>'    +  request.args.get('ADCAA12','')  + '</ADCAA12>'
  pgnxml = pgnxml +  '<ADCAA13>'    +  request.args.get('ADCAA13','')  + '</ADCAA13>'
  pgnxml = pgnxml +  '<ADCAA14>'    +  request.args.get('ADCAA14','')  + '</ADCAA14>'
  pgnxml = pgnxml +  '<ADCAA15>'    +  request.args.get('ADCAA15','')  + '</ADCAA15>'
  pgnxml = pgnxml +  '<ADCAA16>'    +  request.args.get('ADCAA16','')  + '</ADCAA16>'
  pgnxml = pgnxml +  '<ADCAA17>'    +  request.args.get('ADCAA17','')  + '</ADCAA17>'
  pgnxml = pgnxml +  '<ADCAA18>'    +  request.args.get('ADCAA18','')  + '</ADCAA18>'
  pgnxml = pgnxml +  '<ADCAA19>'    +  request.args.get('ADCAA19','')  + '</ADCAA19>'
  
  pgnxml = pgnxml +  '<ADCAH0>'    +  request.args.get('ADCAH0','')  + '</ADCAH0>'
  pgnxml = pgnxml +  '<ADCAH1>'    +  request.args.get('ADCAH1','')  + '</ADCAH1>'
  pgnxml = pgnxml +  '<ADCAH2>'    +  request.args.get('ADCAH2','')  + '</ADCAH2>'
  pgnxml = pgnxml +  '<ADCAH3>'    +  request.args.get('ADCAH3','')  + '</ADCAH3>'
  pgnxml = pgnxml +  '<ADCAH4>'    +  request.args.get('ADCAH4','')  + '</ADCAH4>'
  pgnxml = pgnxml +  '<ADCAH5>'    +  request.args.get('ADCAH5','')  + '</ADCAH5>'
  pgnxml = pgnxml +  '<ADCAH6>'    +  request.args.get('ADCAH6','')  + '</ADCAH6>'
  pgnxml = pgnxml +  '<ADCAH7>'    +  request.args.get('ADCAH7','')  + '</ADCAH7>'
  pgnxml = pgnxml +  '<ADCAH8>'    +  request.args.get('ADCAH8','')  + '</ADCAH8>'
  pgnxml = pgnxml +  '<ADCAH9>'    +  request.args.get('ADCAH9','')  + '</ADCAH9>'
  pgnxml = pgnxml +  '<ADCAH10>'    +  request.args.get('ADCAH10','')  + '</ADCAH10>'
  pgnxml = pgnxml +  '<ADCAH11>'    +  request.args.get('ADCAH11','')  + '</ADCAH11>'
  pgnxml = pgnxml +  '<ADCAH12>'    +  request.args.get('ADCAH12','')  + '</ADCAH12>'
  pgnxml = pgnxml +  '<ADCAH13>'    +  request.args.get('ADCAH13','')  + '</ADCAH13>'
  pgnxml = pgnxml +  '<ADCAH14>'    +  request.args.get('ADCAH14','')  + '</ADCAH14>'
  pgnxml = pgnxml +  '<ADCAH15>'    +  request.args.get('ADCAH15','')  + '</ADCAH15>'
  pgnxml = pgnxml +  '<ADCAH16>'    +  request.args.get('ADCAH16','')  + '</ADCAH16>'
  pgnxml = pgnxml +  '<ADCAH17>'    +  request.args.get('ADCAH17','')  + '</ADCAH17>'
  pgnxml = pgnxml +  '<ADCAH18>'    +  request.args.get('ADCAH18','')  + '</ADCAH18>'
  pgnxml = pgnxml +  '<ADCAH19>'    +  request.args.get('ADCAH19','')  + '</ADCAH19>'  
 
  pgnxml = pgnxml +  '<ADCAL0>'    +  request.args.get('ADCAL0','')  + '</ADCAL0>'
  pgnxml = pgnxml +  '<ADCAL1>'    +  request.args.get('ADCAL1','')  + '</ADCAL1>'
  pgnxml = pgnxml +  '<ADCAL2>'    +  request.args.get('ADCAL2','')  + '</ADCAL2>'
  pgnxml = pgnxml +  '<ADCAL3>'    +  request.args.get('ADCAL3','')  + '</ADCAL3>'
  pgnxml = pgnxml +  '<ADCAL4>'    +  request.args.get('ADCAL4','')  + '</ADCAL4>'
  pgnxml = pgnxml +  '<ADCAL5>'    +  request.args.get('ADCAL5','')  + '</ADCAL5>'
  pgnxml = pgnxml +  '<ADCAL6>'    +  request.args.get('ADCAL6','')  + '</ADCAL6>'
  pgnxml = pgnxml +  '<ADCAL7>'    +  request.args.get('ADCAL7','')  + '</ADCAL7>'
  pgnxml = pgnxml +  '<ADCAL8>'    +  request.args.get('ADCAL8','')  + '</ADCAL8>'
  pgnxml = pgnxml +  '<ADCAL9>'    +  request.args.get('ADCAL9','')  + '</ADCAL9>'
  pgnxml = pgnxml +  '<ADCAL10>'    +  request.args.get('ADCAL10','')  + '</ADCAL10>'
  pgnxml = pgnxml +  '<ADCAL11>'    +  request.args.get('ADCAL11','')  + '</ADCAL11>'
  pgnxml = pgnxml +  '<ADCAL12>'    +  request.args.get('ADCAL12','')  + '</ADCAL12>'
  pgnxml = pgnxml +  '<ADCAL13>'    +  request.args.get('ADCAL13','')  + '</ADCAL13>'
  pgnxml = pgnxml +  '<ADCAL14>'    +  request.args.get('ADCAL14','')  + '</ADCAL14>'
  pgnxml = pgnxml +  '<ADCAL15>'    +  request.args.get('ADCAL15','')  + '</ADCAL15>'
  pgnxml = pgnxml +  '<ADCAL16>'    +  request.args.get('ADCAL16','')  + '</ADCAL16>'
  pgnxml = pgnxml +  '<ADCAL17>'    +  request.args.get('ADCAL17','')  + '</ADCAL17>'
  pgnxml = pgnxml +  '<ADCAL18>'    +  request.args.get('ADCAL18','')  + '</ADCAL18>'
  pgnxml = pgnxml +  '<ADCAL19>'    +  request.args.get('ADCAL19','')  + '</ADCAL19>'  
 

  pgnxml = pgnxml +  '<ADCAM0>'    +  request.args.get('ADCAM0','')  + '</ADCAM0>'
  pgnxml = pgnxml +  '<ADCAM1>'    +  request.args.get('ADCAM1','')  + '</ADCAM1>'
  pgnxml = pgnxml +  '<ADCAM2>'    +  request.args.get('ADCAM2','')  + '</ADCAM2>'
  pgnxml = pgnxml +  '<ADCAM3>'    +  request.args.get('ADCAM3','')  + '</ADCAM3>'
  pgnxml = pgnxml +  '<ADCAM4>'    +  request.args.get('ADCAM4','')  + '</ADCAM4>'
  pgnxml = pgnxml +  '<ADCAM5>'    +  request.args.get('ADCAM5','')  + '</ADCAM5>'
  pgnxml = pgnxml +  '<ADCAM6>'    +  request.args.get('ADCAM6','')  + '</ADCAM6>'
  pgnxml = pgnxml +  '<ADCAM7>'    +  request.args.get('ADCAM7','')  + '</ADCAM7>'
  pgnxml = pgnxml +  '<ADCAM8>'    +  request.args.get('ADCAM8','')  + '</ADCAM8>'
  pgnxml = pgnxml +  '<ADCAM9>'    +  request.args.get('ADCAM9','')  + '</ADCAM9>'
  pgnxml = pgnxml +  '<ADCAM10>'    +  request.args.get('ADCAM10','')  + '</ADCAM10>'
  pgnxml = pgnxml +  '<ADCAM11>'    +  request.args.get('ADCAM11','')  + '</ADCAM11>'
  pgnxml = pgnxml +  '<ADCAM12>'    +  request.args.get('ADCAM12','')  + '</ADCAM12>'
  pgnxml = pgnxml +  '<ADCAM13>'    +  request.args.get('ADCAM13','')  + '</ADCAM13>'
  pgnxml = pgnxml +  '<ADCAM14>'    +  request.args.get('ADCAM14','')  + '</ADCAM14>'
  pgnxml = pgnxml +  '<ADCAM15>'    +  request.args.get('ADCAM15','')  + '</ADCAM15>'
  pgnxml = pgnxml +  '<ADCAM16>'    +  request.args.get('ADCAM16','')  + '</ADCAM16>'
  pgnxml = pgnxml +  '<ADCAM17>'    +  request.args.get('ADCAM17','')  + '</ADCAM17>'
  pgnxml = pgnxml +  '<ADCAM18>'    +  request.args.get('ADCAM18','')  + '</ADCAM18>'
  pgnxml = pgnxml +  '<ADCAM19>'    +  request.args.get('ADCAM19','')  + '</ADCAM19>'

  
  pgnxml = pgnxml +  '<ADCAP0>'    +  request.args.get('ADCAP0','')  + '</ADCAP0>'
  pgnxml = pgnxml +  '<ADCAP1>'    +  request.args.get('ADCAP1','')  + '</ADCAP1>'
  pgnxml = pgnxml +  '<ADCAP2>'    +  request.args.get('ADCAP2','')  + '</ADCAP2>'
  pgnxml = pgnxml +  '<ADCAP3>'    +  request.args.get('ADCAP3','')  + '</ADCAP3>'
  pgnxml = pgnxml +  '<ADCAP4>'    +  request.args.get('ADCAP4','')  + '</ADCAP4>'
  pgnxml = pgnxml +  '<ADCAP5>'    +  request.args.get('ADCAP5','')  + '</ADCAP5>'
  pgnxml = pgnxml +  '<ADCAP6>'    +  request.args.get('ADCAP6','')  + '</ADCAP6>'
  pgnxml = pgnxml +  '<ADCAP7>'    +  request.args.get('ADCAP7','')  + '</ADCAP7>'
  pgnxml = pgnxml +  '<ADCAP8>'    +  request.args.get('ADCAP8','')  + '</ADCAP8>'
  pgnxml = pgnxml +  '<ADCAP9>'    +  request.args.get('ADCAP9','')  + '</ADCAP9>'
  pgnxml = pgnxml +  '<ADCAP10>'    +  request.args.get('ADCAP10','')  + '</ADCAP10>'
  pgnxml = pgnxml +  '<ADCAP11>'    +  request.args.get('ADCAP11','')  + '</ADCAP11>'
  pgnxml = pgnxml +  '<ADCAP12>'    +  request.args.get('ADCAP12','')  + '</ADCAP12>'
  pgnxml = pgnxml +  '<ADCAP13>'    +  request.args.get('ADCAP13','')  + '</ADCAP13>'
  pgnxml = pgnxml +  '<ADCAP14>'    +  request.args.get('ADCAP14','')  + '</ADCAP14>'
  pgnxml = pgnxml +  '<ADCAP15>'    +  request.args.get('ADCAP15','')  + '</ADCAP15>'
  pgnxml = pgnxml +  '<ADCAP16>'    +  request.args.get('ADCAP16','')  + '</ADCAP16>'
  pgnxml = pgnxml +  '<ADCAP17>'    +  request.args.get('ADCAP17','')  + '</ADCAP17>'
  pgnxml = pgnxml +  '<ADCAP18>'    +  request.args.get('ADCAP18','')  + '</ADCAP18>'
  pgnxml = pgnxml +  '<ADCAP19>'    +  request.args.get('ADCAP19','')  + '</ADCAP19>'


  pgnxml = pgnxml +  '<PGNN0>'    +  request.args.get('PGNN0','')  + '</PGNN0>'
  pgnxml = pgnxml +  '<PGNN1>'    +  request.args.get('PGNN1','')  + '</PGNN1>'
  pgnxml = pgnxml +  '<PGNN2>'    +  request.args.get('PGNN2','')  + '</PGNN2>'
  pgnxml = pgnxml +  '<PGNN3>'    +  request.args.get('PGNN3','')  + '</PGNN3>'
  pgnxml = pgnxml +  '<PGNN4>'    +  request.args.get('PGNN4','')  + '</PGNN4>'
  pgnxml = pgnxml +  '<PGNN5>'    +  request.args.get('PGNN5','')  + '</PGNN5>'
  pgnxml = pgnxml +  '<PGNN6>'    +  request.args.get('PGNN6','')  + '</PGNN6>'
  pgnxml = pgnxml +  '<PGNN7>'    +  request.args.get('PGNN7','')  + '</PGNN7>'
  pgnxml = pgnxml +  '<PGNN8>'    +  request.args.get('PGNN8','')  + '</PGNN8>'
  pgnxml = pgnxml +  '<PGNN9>'    +  request.args.get('PGNN9','')  + '</PGNN9>'
  pgnxml = pgnxml +  '<PGNN10>'    +  request.args.get('PGNN10','')  + '</PGNN10>'
  pgnxml = pgnxml +  '<PGNN11>'    +  request.args.get('PGNN11','')  + '</PGNN11>'

  
  pgnxml = pgnxml +  '<PGNI0>'    +  request.args.get('PGNI0','')  + '</PGNI0>'
  pgnxml = pgnxml +  '<PGNI1>'    +  request.args.get('PGNI1','')  + '</PGNI1>'
  pgnxml = pgnxml +  '<PGNI2>'    +  request.args.get('PGNI2','')  + '</PGNI2>'
  pgnxml = pgnxml +  '<PGNI3>'    +  request.args.get('PGNI3','')  + '</PGNI3>'
  pgnxml = pgnxml +  '<PGNI4>'    +  request.args.get('PGNI4','')  + '</PGNI4>'
  pgnxml = pgnxml +  '<PGNI5>'    +  request.args.get('PGNI5','')  + '</PGNI5>'
  pgnxml = pgnxml +  '<PGNI6>'    +  request.args.get('PGNI6','')  + '</PGNI6>'
  pgnxml = pgnxml +  '<PGNI7>'    +  request.args.get('PGNI7','')  + '</PGNI7>'
  pgnxml = pgnxml +  '<PGNI8>'    +  request.args.get('PGNI8','')  + '</PGNI8>'
  pgnxml = pgnxml +  '<PGNI9>'    +  request.args.get('PGNI9','')  + '</PGNI9>'
  pgnxml = pgnxml +  '<PGNI10>'    +  request.args.get('PGNI10','')  + '</PGNI10>'
  pgnxml = pgnxml +  '<PGNI11>'    +  request.args.get('PGNI11','')  + '</PGNI11>'

  pgnxml = pgnxml +  '<PGNP0>'    +  request.args.get('PGNP0','')  + '</PGNP0>'
  pgnxml = pgnxml +  '<PGNP1>'    +  request.args.get('PGNP1','')  + '</PGNP1>'
  pgnxml = pgnxml +  '<PGNP2>'    +  request.args.get('PGNP2','')  + '</PGNP2>'
  pgnxml = pgnxml +  '<PGNP3>'    +  request.args.get('PGNP3','')  + '</PGNP3>'
  pgnxml = pgnxml +  '<PGNP4>'    +  request.args.get('PGNP4','')  + '</PGNP4>'
  pgnxml = pgnxml +  '<PGNP5>'    +  request.args.get('PGNP5','')  + '</PGNP5>'
  pgnxml = pgnxml +  '<PGNP6>'    +  request.args.get('PGNP6','')  + '</PGNP6>'
  pgnxml = pgnxml +  '<PGNP7>'    +  request.args.get('PGNP7','')  + '</PGNP7>'
  pgnxml = pgnxml +  '<PGNP8>'    +  request.args.get('PGNP8','')  + '</PGNP8>'
  pgnxml = pgnxml +  '<PGNP9>'    +  request.args.get('PGNP9','')  + '</PGNP9>'
  pgnxml = pgnxml +  '<PGNP10>'    +  request.args.get('PGNP10','')  + '</PGNP10>'
  pgnxml = pgnxml +  '<PGNP11>'    +  request.args.get('PGNP11','')  + '</PGNP11>'

  pgnxml = pgnxml +  '<PGNS0>'    +  request.args.get('PGNS0','')  + '</PGNS0>'
  pgnxml = pgnxml +  '<PGNS1>'    +  request.args.get('PGNS1','')  + '</PGNS1>'
  pgnxml = pgnxml +  '<PGNS2>'    +  request.args.get('PGNS2','')  + '</PGNS2>'
  pgnxml = pgnxml +  '<PGNS3>'    +  request.args.get('PGNS3','')  + '</PGNS3>'
  pgnxml = pgnxml +  '<PGNS4>'    +  request.args.get('PGNS4','')  + '</PGNS4>'
  pgnxml = pgnxml +  '<PGNS5>'    +  request.args.get('PGNS5','')  + '</PGNS5>'
  pgnxml = pgnxml +  '<PGNS6>'    +  request.args.get('PGNS6','')  + '</PGNS6>'
  pgnxml = pgnxml +  '<PGNS7>'    +  request.args.get('PGNS7','')  + '</PGNS7>'
  pgnxml = pgnxml +  '<PGNS8>'    +  request.args.get('PGNS8','')  + '</PGNS8>'
  pgnxml = pgnxml +  '<PGNS9>'    +  request.args.get('PGNS9','')  + '</PGNS9>'
  pgnxml = pgnxml +  '<PGNS10>'    +  request.args.get('PGNS10','')  + '</PGNS10>'
  pgnxml = pgnxml +  '<PGNS11>'    +  request.args.get('PGNS11','')  + '</PGNS11>'  


  pgnxml = pgnxml +  '<CAL0>'    +  request.args.get('CALFILE0','')  + '</CAL0>'
  pgnxml = pgnxml +  '<CAL1>'    +  request.args.get('CALFILE1','')  + '</CAL1>'
  pgnxml = pgnxml +  '<CAL2>'    +  request.args.get('CALFILE2','')  + '</CAL2>'
  pgnxml = pgnxml +  '<CAL3>'    +  request.args.get('CALFILE3','')  + '</CAL3>'
  pgnxml = pgnxml +  '<CAL4>'    +  request.args.get('CALFILE4','')  + '</CAL4>'
  pgnxml = pgnxml +  '<CAL5>'    +  request.args.get('CALFILE5','')  + '</CAL5>'
  pgnxml = pgnxml +  '<CAL6>'    +  request.args.get('CALFILE6','')  + '</CAL6>'
  pgnxml = pgnxml +  '<CAL7>'    +  request.args.get('CALFILE7','')  + '</CAL7>'
  pgnxml = pgnxml +  '<CAL8>'    +  request.args.get('CALFILE8','')  + '</CAL8>'
  pgnxml = pgnxml +  '<CAL9>'    +  request.args.get('CALFILE9','')  + '</CAL9>'
  pgnxml = pgnxml +  '<CAL10>'    +  request.args.get('CALFILE10','')  + '</CAL10>'
  pgnxml = pgnxml +  '<CAL11>'    +  request.args.get('CALFILE11','')  + '</CAL11>'

  
  prefidkey=1

  try:  
    conn = db_pool.getconn()

  except:
    e = sys.exc_info()[0]
    #log.info("getuser_endpoint error - db_pool.getconn %s", deviceid)
    log.info("getuser_endpoint error - db_pool.getconn ")
    log.info('getuser_endpoint error: db_pool.getconn %s:  ' % e)
    db_pool.closeall()  
  
  cursor = conn.cursor()
  sqlstr = " update user_sgg4configxml SET pgnsxml =%s where  prefidkey = %s;" 
  cursor.execute(sqlstr, (pgnxml, prefidkey, ))   
  conn.commit()

  db_pool.putconn(conn)

 
  log.info("set_seasmart_device_xml pgnxml %s", pgnxml)  
  return  

def create_seasmart_device_xml(postdata):

  log.info("create_seasmart_device_xml postdata %s", postdata)


  xmlfile = ''
  
  xmlfile = xmlfile + '<configrecord version="24.12.20">\r\n'
  xmlfile = xmlfile + '<configgroup name = "XMLACTION">\r\n'
  xmlfile = xmlfile + '<configitem name="LOADXML"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Save_NVRAM"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'
  xmlfile = xmlfile + '<configgroup name = "DEVICE">\r\n'
  xmlfile = xmlfile + '<configitem name="DeviceID"><value>'+  get_xml_value(postdata, "DeviceID") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="VersionInfo"><value>'+  get_xml_value(postdata, "DeviceID") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="N2K_STATUS_BUFF"><value>65535</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Dimmer_Type"><value>'+  get_xml_value(postdata, "DIMMERTYPE") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Switch_PGN_Instance"><value>'+  get_xml_value(postdata, "DIMMERINSTANCE") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="CAN_Mode"><value>'+  get_xml_value(postdata, "CANMODE") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="CANFILTERHB"><value>4294967295</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="CANFILTERLB"><value>4294967295</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Uart0_Mode"><value>'+  get_xml_value(postdata, "UART0MODE") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Uart1_Mode"><value>'+  get_xml_value(postdata, "UART1MODE") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Uart2_Mode"><value>'+  get_xml_value(postdata, "UART2MODE") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="SDLogEnable"><value>'+  get_xml_value(postdata, "SDLogEnable") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="SDLogInterval"><value>'+  get_xml_value(postdata, "SDLogInterval") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Sample_Interval"><value>2</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="RTCEnable"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="TimeSource"><value>'+  get_xml_value(postdata, "TimeSource") +'</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="HTTP_POST_BUFF"><value>4096</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="HTTP_SD_POST_BUFF"><value>4096</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="SD_LOG_BUFF"><value>4096</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'

  return  xmlfile

def set_seasmart_device_xml(postdata):

  log.info("set_seasmart_device_xml postdata", postdata)
  

  devicexml = ""
  devicexml = devicexml +  '<DeviceID>'     +  request.args.get('DeviceIDXML','')       + '</DeviceID>'
  devicexml = devicexml +  '<VersionInfo>'  +  request.args.get('VersionXML','')          + '</VersionInfo>'
  devicexml = devicexml +  '<SDLogEnable>'    +  request.args.get('SDLogFName','')  + '</SDLogEnable>'
  devicexml = devicexml +  '<SDLogInterval>'    +  request.args.get('SDLogInterval','')  + '</SDLogInterval>'
  devicexml = devicexml +  '<UartInterval>'    +  request.args.get('UartInterval','')  + '</UartInterval>'
  devicexml = devicexml +  '<UART0MODE>'    +  request.args.get('UART0ModeDD','')  + '</UART0MODE>'
  devicexml = devicexml +  '<UART1MODE>'    +  request.args.get('UART1ModeDD','')  + '</UART1MODE>'
  devicexml = devicexml +  '<UART2MODE>'    +  request.args.get('UART2ModeDD','')  + '</UART2MODE>'
  devicexml = devicexml +  '<CANMODE>'    +  request.args.get('CANModeDD','')  + '</CANMODE>'
  #devicexml = devicexml +  '<CANFILTERHB>'    +  request.args.get('WIFINetType_CB','')  + '</CANFILTERHB>'
  #devicexml = devicexml +  '<CANFILTERLB>'    +  request.args.get('WIFINetType_CB','')  + '</CANFILTERLB>'
  devicexml = devicexml +  '<CANFILTERHB>'    +  '4294967295'  + '</CANFILTERHB>'
  devicexml = devicexml +  '<CANFILTERLB>'    +  '4294967295'  + '</CANFILTERLB>'
  devicexml = devicexml +  '<DIMMERTYPE>'    +  request.args.get('DimmerTypeDD','')  + '</DIMMERTYPE>'
  devicexml = devicexml +  '<DIMMERINSTANCE>'    +  request.args.get('DimmerInstanceDD','')  + '</DIMMERINSTANCE>'
  devicexml = devicexml +  '<DIMMERSCALE>'    +  request.args.get('DIMMERSCALE','')  + '</DIMMERSCALE>'
  devicexml = devicexml +  '<DIMMERPON>'    +  request.args.get('DimmerPONDD','')  + '</DIMMERPON>'
  devicexml = devicexml +  '<DIMMERTXRATE>'    +  request.args.get('DimmerTXDD','')  + '</DIMMERTXRATE>'
  devicexml = devicexml +  '<TIMERMODE>'    +  request.args.get('TimerModeDD','')  + '</TIMERMODE>'
  devicexml = devicexml +  '<TimeSource>'    +  request.args.get('TimeStampSource','')  + '</TimeSource>'

 


  prefidkey=1

  try:  
    conn = db_pool.getconn()

  except:
    e = sys.exc_info()[0]
    #log.info("getuser_endpoint error - db_pool.getconn %s", deviceid)
    log.info("getuser_endpoint error - db_pool.getconn ")
    log.info('getuser_endpoint error: db_pool.getconn %s:  ' % e)
    db_pool.closeall()  
  
  cursor = conn.cursor()
  sqlstr = " update user_sgg4configxml SET devicexml =%s where  prefidkey = %s;" 
  cursor.execute(sqlstr, (devicexml, prefidkey, ))   
  conn.commit()

  db_pool.putconn(conn)

 
  log.info("set_seasmart_device_xml networkxml %s", devicexml)  
  return  

    

def create_seasmart_network_xml(postdata):

  log.info("create_seasmart_network_xml postdata %s", postdata)

  xmlfile = ''
  xmlfile = xmlfile +  '<?xml version="1.0" standalone="yes"?>\r\n'
  xmlfile = xmlfile + '<configrecord version="24.12.20">\r\n'
  xmlfile = xmlfile + '<configgroup name = "XMLACTION">\r\n'
  xmlfile = xmlfile + '<configitem name="LOADXML"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Save_NVRAM"><value>1</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'
  xmlfile = xmlfile + '<configgroup name = "DEVICE">\r\n'
  xmlfile = xmlfile + '<configitem name="DeviceID"><value>'+  get_xml_value(postdata, "DeviceID") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="VersionInfo"><value>'+  get_xml_value(postdata, "VersionInfo") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'
  xmlfile = xmlfile + '<configgroup name = "Network">\r\n'
  xmlfile = xmlfile + '<configitem name="DHCP"><value>'+  get_xml_value(postdata, "DHCP") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="IPAddress"><value>'+  get_xml_value(postdata, "IPAddress") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="SubNet"><value>'+  get_xml_value(postdata, "IPMask") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="Gateway"><value>'+  get_xml_value(postdata, "IPGateway") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="DNS1"><value>'+  get_xml_value(postdata, "DNS1") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="DNS2"><value>'+  get_xml_value(postdata, "DNS2") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'
  xmlfile = xmlfile + '<configgroup name = "WIFI">\r\n'
  xmlfile = xmlfile + '<configitem name="WiFiType"><value>'+  get_xml_value(postdata, "WIFIType") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="STASSID"><value>'+  get_xml_value(postdata, "STAWIFISSID") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="STASECTYPE"><value>'+  get_xml_value(postdata, "APWIFIMode") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="STASECKEY"><value>'+  get_xml_value(postdata, "STAWIFIPW") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="SAPSSID"><value>'+  get_xml_value(postdata, "APWIFISSID") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="SAPSECTYPE"><value>'+  get_xml_value(postdata, "APWIFIMode") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="SAPSECKEY"><value>'+  get_xml_value(postdata, "APWIFIPW") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'
  xmlfile = xmlfile + '<configgroup name = "UDP">\r\n'
  xmlfile = xmlfile + '<configitem name="UDPEnable"><value>'+  get_xml_value(postdata, "UDPBroadcastEnable") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="UDPPort"><value>'+  get_xml_value(postdata, "UDPClientPort") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configgroup name = "TCP">\r\n'
  xmlfile = xmlfile + '<configitem name="TCPEnable"><value>'+  get_xml_value(postdata, "TCPEnable") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="TCPPort"><value>'+  get_xml_value(postdata, "TCPServerPort") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'
  xmlfile = xmlfile + '<configgroup name = "HTTPPOST">\r\n'
  xmlfile = xmlfile + '<configitem name="PostType"><value>'+  get_xml_value(postdata, "HTTPPostMenu") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '<configitem name="PostInterval"><value>'+  get_xml_value(postdata, "HpptPostInterval") + '</value></configitem>\r\n'
  xmlfile = xmlfile + '</configgroup>\r\n'

  return  xmlfile

def set_seasmart_network_xml(postdata):

  log.info("set_seasmart_network_xml postdata", postdata)

  networkxml = ""
  networkxml = networkxml +  '<DeviceID>'     +  request.args.get('DeviceIDXML','')       + '</DeviceID>'
  networkxml = networkxml +  '<VersionInfo>'  +  request.args.get('VersionXML','')          + '</VersionInfo>'
  networkxml = networkxml +  '<WIFIType>'    +  request.args.get('WIFINetType_CB','')  + '</WIFIType>'
  networkxml = networkxml +  '<STAWIFISSID>'    +  request.args.get('SSID','')  + '</STAWIFISSID>\r\n'
  networkxml = networkxml +  '<STAWIFIPW>'    +  request.args.get('STAPASSWORD','')  + '</STAWIFIPW>'
  networkxml = networkxml +  '<APWIFISSID>'    +  request.args.get('APSSID','')  + '</APWIFISSID>'
  networkxml = networkxml +  '<APWIFIPW>'    +  request.args.get('APSECKEY','')  + '</APWIFIPW>'
  networkxml = networkxml +  '<APWIFIMode>'    +  request.args.get('APSECTYPE','')  + '</APWIFIMode>'
  networkxml = networkxml +  '<MESHCHANNEL>'    +  request.args.get('MESHCHANNEL','')  + '</MESHCHANNEL>'
  networkxml = networkxml +  '<MESHID>'    +  request.args.get('MESHID','')  + '</MESHID>'
  networkxml = networkxml +  '<CIPAddress>'    +  request.args.get('IPaddressXML','')  + '</CIPAddress>'
  networkxml = networkxml +  '<CIPMask>'    +  request.args.get('IPMaskXML','')  + '</CIPMask>'
  networkxml = networkxml +  '<CIPGW>'    +  request.args.get('IPGatewayXML','')  + '</CIPGW>'
  networkxml = networkxml +  '<DHCP>'    +  request.args.get('DHCPCLIENT_ON_CB','')  + '</DHCP>'
  networkxml = networkxml +  '<IPAddress>'    +  request.args.get('IPADDR','')  + '</IPAddress>'
  networkxml = networkxml +  '<IPMask>'    +  request.args.get('SUBNET','')  + '</IPMask>'
  networkxml = networkxml +  '<IPGateway>'    +  request.args.get('GATEWAY','')  + '</IPGateway>'
  networkxml = networkxml +  '<DNS1>'    +  request.args.get('DNS1','')  + '</DNS1>'
  networkxml = networkxml +  '<DNS2>'    +  request.args.get('DNS2','')  + '</DNS2>'
  networkxml = networkxml +  '<HpptPostInterval>'    +  request.args.get('HttpPostInterval','')  + '</HpptPostInterval>'
  networkxml = networkxml +  '<HTTPPostMenu>'    +  request.args.get('HTTPPostMenu','')  + '</HTTPPostMenu>'
  networkxml = networkxml +  '<SSIDDefault>'    +  request.args.get('SSID','')  + '</SSIDDefault>'
  networkxml = networkxml +  '<NETTYPE>'    +  request.args.get('NetTypeXML','')  + '</NETTYPE>'
  networkxml = networkxml +  '<TCPServerPort>'    +  request.args.get('TCPSERVERPORT','')  + '</TCPServerPort>'
  networkxml = networkxml +  '<TCPEnable>'    +  request.args.get('TCPSERVER_ON_CB','')  + '</TCPEnable>'
  networkxml = networkxml +  '<UDPClientPort>'    +  request.args.get('UDPBROADPORT','')  + '</UDPClientPort>'
  networkxml = networkxml +  '<UDPBroadcastEnable>'    +  request.args.get('UDPBROADCAST_ON_CB','')  + '</UDPBroadcastEnable>'

  prefidkey=1

  try:  
    conn = db_pool.getconn()

  except:
    e = sys.exc_info()[0]
    #log.info("getuser_endpoint error - db_pool.getconn %s", deviceid)
    log.info("getuser_endpoint error - db_pool.getconn ")
    log.info('getuser_endpoint error: db_pool.getconn %s:  ' % e)
    db_pool.closeall()  
  
  cursor = conn.cursor()
  sqlstr = " update user_sgg4configxml SET networkxml =%s where  prefidkey = %s;" 
  cursor.execute(sqlstr, (networkxml, prefidkey, ))   
  conn.commit()

  db_pool.putconn(conn)

 
  log.info("set_seasmart_network_xml networkxml %s", networkxml)  
  return  
"""

# ######################################################
# gets seagaugeg4 config POST parameters methods=['GET','POST'])
# #####################################################  
@app.route('/savesgg4calxml' , methods=['GET','POST'])
@cross_origin()
def savesgg4calxml():

  log.info("savesgg4calxml endpoint")

  log.info("savesgg4calxml request %s", request)
  #postdata = request.form
  #postdata = request.args.get('SSID')
  postdata = request.args

  log.info("savesgg4calxml postdata %s", postdata)
  
  useridkey = request.args.get('userid','')
  ssg4calname = request.args.get('ssg4calname','')
  ssg4calxml_binary = request.data

  ssg4calxml = ssg4calxml_binary.decode('utf-8')

  log.info("seasmartconfig postdata userid %s prefKey %s  ssg4calname %s", useridkey, ssg4calname, ssg4calxml)


  try:  
    conn = db_pool.getconn()

  except:
    e = sys.exc_info()[0]
    #log.info("getuser_endpoint error - db_pool.getconn %s", deviceid)
    log.info("getuser_endpoint error - db_pool.getconn ")
    log.info('getuser_endpoint error: db_pool.getconn %s:  ' % e)
    db_pool.closeall()  
  
  cursor = conn.cursor()
  sqlstr = "insert into sgg4calfiles ( useridkey, filename, filetype, filecontentsxml) values (%s, %s, 1, %s) ;" 
  cursor.execute(sqlstr, (useridkey, ssg4calname, ssg4calxml, ))  
  conn.commit()

  db_pool.putconn(conn)


  response = make_response(render_template('seagauge_conf.html', features = []))
  #response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
  response.headers['Cache-Control'] = 'public, max-age=0'
  return response


# ######################################################
# gets seagaugeg4 config POST parameters methods=['GET','POST'])
# #####################################################  
@app.route('/deletecalxml' , methods=['GET','POST'])
@cross_origin()
def deletecalxml():

  log.info("deletegg4calxml endpoint")


  
  useridkey = request.args.get('userid','')
  ssg4calkey =  request.args.get('ssg4calkey','')


  log.info("deletegg4calxml postdata userid %s ssg4calkey %s  ", useridkey, ssg4calkey)


  try:  
    conn = db_pool.getconn()

  except:
    e = sys.exc_info()[0]
    #log.info("getuser_endpoint error - db_pool.getconn %s", deviceid)
    log.info("getuser_endpoint error - db_pool.getconn ")
    log.info('getuser_endpoint error: db_pool.getconn %s:  ' % e)
    db_pool.closeall()  
  
  cursor = conn.cursor()
  sqlstr = "delete from sgg4calfiles where (useridkey = %s and prefidkey= %s);" 
  cursor.execute(sqlstr, (useridkey, ssg4calkey, ))  
  conn.commit()

  db_pool.putconn(conn)


  response = make_response(render_template('seagauge_conf.html', features = []))
  #response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
  response.headers['Cache-Control'] = 'public, max-age=0'
  return response


# ######################################################
# gets seagaugeg4 config POST parameters methods=['GET','POST'])
# #####################################################  
@app.route('/seasmartconfig' , methods=['GET','POST'])
@cross_origin()
def seasmartconfig():

  log.info("seasmartconfig endpoint")
  #postdata = request.form
  #postdata = request.args.get('SSID')
  postdata = request.args

  log.info("seasmartconfig postdata %s", postdata)
  
  prefAction = request.args.get('PrefUpdateXML','')
  prefKey = request.args.get('PrefKeyXML','')
  prefName = request.args.get('PrefNameXML','')
  adcCalChannel = request.args.get('adcCalChannel','')
  adcCalFile = request.args.get('adcCalFile','')

  log.info("seasmartconfig postdata prefAction %s prefKey %s  prefName %s", prefAction, prefKey, prefName)

  #log.info("seasmartconfig postdata %s", postdata)



  if prefAction == "delete" and int(prefKey) != 0:
    seagaugeg4.delete_seagauge_xml(request)

  elif prefAction == "add":
    seagaugeg4.add_seagauge_xml(request)

  elif prefAction == "update" and int(prefKey) != 0:
    
    prefidkey = request.args.get('PrefKeyXML',0)
    
    seagaugeg4.set_seasmart_network_xml(prefidkey, request)
    
    seagaugeg4.set_seasmart_device_xml(prefidkey, request)
    
    seagaugeg4.set_seasmart_pulse_xml(prefidkey, request)

    seagaugeg4.set_seasmart_pgn_xml(prefidkey, request)
  
  #return jsonify(result="OK", postdata = postdata)
  #data_for_template = ["Feature A", "Feature B", "Feature C"]
  #response = make_response(render_template('seagauge_conf.html', features = []))

  if adcCalChannel != "" and adcCalFile != "":
    myjson={"ADCChannel":int(adcCalChannel), "CALFile":adcCalFile}
    response = make_response(render_template('seagauge_conf.html', features = [myjson]))

  else:
    response = make_response(render_template('seagauge_conf.html'))


  #response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
  response.headers['Cache-Control'] = 'public, max-age=0'
  return response
  
# ######################################################
# gets seagaugeg4 config.xml parameters
# #####################################################  
@app.route('/getseagaugeg4configxml')
@cross_origin()
def getseagaugeg4configxml():


  #userid = request.args.get('userid', 'a91140300971bfb9244989a9bffde53c')
  prefidkey = request.args.get('prefidkey', 0)

  log.info('getseagaugeg4configxml: prefidkey %s:  ', prefidkey)   

  try:  
    conn = db_pool.getconn()

  except:
    e = sys.exc_info()[0]
    log.info("getuser_endpoint error - db_pool.getconn %s", deviceid)
    log.info('getuser_endpoint error: db_pool.getconn %s:  ' % e)
    db_pool.closeall()  

    return jsonify( message='Could not open a connection', status='error')
  
  cursor = conn.cursor()

  #select configxml from user_sgg4configxml where deviceidkey = '1f389afd27e33799752b11838e7bc4ef'
  #sqlstr = 'select configxml from user_sgg4configxml where deviceidkey = %s;'
  sqlstr = 'select devicexml, networkxml, pulsexml, runtimexml, pgnsxml from user_sgg4configxml where prefidkey = %s;'
  cursor.execute(sqlstr, (int(prefidkey),))

  records = cursor.fetchone()


  log.info('getuser_endpoint: records found for userid %s:  ', records)              

  sgg4config =str(records[0]) + str(records[1] )+ str(records[2]) + str(records[3]) + str(records[4])

  db_pool.putconn(conn)

  #return sgg4config
  return jsonify(result="OK", sgg4config=sgg4config)


# ######################################################
# gets seagaugeg4 config.xml parameters
# #####################################################  
@app.route('/createSGG4XMLfile')
@cross_origin()
def createSGG4XMLfile():

  prefidkey = request.args.get('prefidkey', 0)
  userid = request.args.get('userid', '00000000000000000000000000000000')
  
  deviceidkey = request.args.get('deviceidkey', '00000000000000000000000000000000')
  saveXML=request.args.get('saveXML', 0)

  log.info('createSGG4XMLfile: saveXML %s:  ', saveXML)              

  if int(prefidkey) == 0:
    return jsonify(result="Cant modify default")

  if userid == '00000000000000000000000000000000':
    return jsonify(result="only user can modify prefs")

  if int(saveXML) == 0:
    return jsonify(result="No file selected")
    
  try:  
    conn = db_pool.getconn()

  except:
    e = sys.exc_info()[0]
    log.info("getuser_endpoint error - db_pool.getconn %s", deviceid)
    log.info('getuser_endpoint error: db_pool.getconn %s:  ' % e)
    db_pool.closeall()  

    return jsonify( message='Could not open a connection', status='error')
  
  cursor = conn.cursor()

  #select configxml from user_sgg4configxml where deviceidkey = '1f389afd27e33799752b11838e7bc4ef'
  #sqlstr = 'select configxml from user_sgg4configxml where deviceidkey = %s;'

  if int(saveXML) == 1: 
    sqlstr = 'select networkxml from user_sgg4configxml where prefidkey = %s;'


  elif int(saveXML) == 2: 
    sqlstr = 'select devicexml from user_sgg4configxml where prefidkey = %s;'


  elif int(saveXML) == 3: 
    sqlstr = 'select pulsexml from user_sgg4configxml where prefidkey = %s;'


  elif int(saveXML) == 4: 
    sqlstr = 'select  pgnsxml from user_sgg4configxml where prefidkey = %s;'


  elif int(saveXML) == 5: 
    sqlstr = 'select  runtimexml from user_sgg4configxml where prefidkey = %s;'

    
  """
  else:
    sqlstr = 'select  runtimexml from user_sgg4configxml where prefidkey = %s;'
  """    
  cursor.execute(sqlstr, (prefidkey,))

  records = cursor.fetchone()


  log.info('createSGG4XMLfile: records found for userid %s:  ', records)              

  sgg4config =str(records[0]) 

  db_pool.putconn(conn)
  

  if int(saveXML) == 1: 
    xmlfile = seagaugeg4.create_seasmart_network_xml(sgg4config)
    filename = "network.xml"

  elif int(saveXML) == 2: 
    xmlfile = seagaugeg4.create_seasmart_device_xml(sgg4config)
    filename = "device.xml"

  elif int(saveXML) == 3: 
    xmlfile = seagaugeg4.create_seasmart_pulse_xml(sgg4config)
    filename = "pulse.xml"

  elif int(saveXML) == 4: 
    xmlfile = seagaugeg4.create_seasmart_pgn_xml(sgg4config)
    filename = "seagaugeg4_pgns_alarms.xml"

  elif int(saveXML) == 5: 
    xmlfile = seagaugeg4.create_seasmart_resets_xml(sgg4config)
    filename = "runtime_resets.xml"


  

  response = make_response(xmlfile)
  #response = make_response(json.dumps(outputcsv))
  #response = make_response(json.dumps(outputjson))
  response.headers['Content-Type'] = 'text/csv'
  response.headers["Content-Disposition"] = "attachment; filename=" + filename
  return response

  #return sgg4config
  #return jsonify(result="OK", sgg4config=sgg4config)

# ######################################################
# gets seagaugeg4 modifycaltable parameters
# #####################################################  
@app.route('/modifycaltable')
@cross_origin()
def modifycaltable():
  
  adcindex = request.args.get('adcindex', 0)

  log.info('modifycaltable: adcindex %s:  ', adcindex)        

  response = make_response(render_template('ModifyCalTable.html', features = []))
  #response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
  response.headers['Cache-Control'] = 'public, max-age=0'
  return response

# ######################################################
# gets seagaugeg4 modifycaltable parameters
# #####################################################  
@app.route('/getcaltable')
@cross_origin()
def getcaltable():


  response = make_response(render_template('ModifyCalTable.html', features = []))
  #response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
  response.headers['Cache-Control'] = 'public, max-age=0'
  return response

# ######################################################
# gets seagaugeg4 modifycaltable parameters
# #####################################################  
@app.route('/getcalfilelist')
@cross_origin()
def getcalfilelist():

  userid = request.args.get('userid', '00000000000000000000000000000000')
  log.info('getcalfilelist:  userid %s:  ', userid)
  
  try:  
    conn = db_pool.getconn()

  except:
    e = sys.exc_info()[0]
    log.info("getuser_endpoint error - db_pool.getconn %s", deviceid)
    log.info('getuser_endpoint error: db_pool.getconn %s:  ' % e)
    db_pool.closeall()  

    return jsonify( message='Could not open a connection', status='error')
  
  cursor = conn.cursor()

  sqlstr = "select prefidkey, filename, filetype from sgg4calfiles where (useridkey = '00000000000000000000000000000000' OR useridkey = %s);"

  cursor.execute(sqlstr, (userid,))

  records = cursor.fetchall()


  log.info('getcalfilelist: records found  %s:  ', records)              

  #sgg4calfiles =str(records) 
  sgg4calfiles =records
  
  db_pool.putconn(conn)
  
  def type_for(type_code):
    return {
      23: 'INTEGER',
      1043: 'STRING',
      1114: 'DATETIME'    
    }.get(type_code)


  schema = dict(
    fields= [
      dict(name=c.name, type=type_for(c.type_code))
      for c in cursor.description
    ]
  )

  result = json.dumps(
    dict(
      schema=schema,
      records=records
    ),
    cls=DateEncoder
  )


  log.info('getcalfilelist: result %s:  ', result)       
  
  response = make_response(result)
  response.headers['content-type'] = "application/json"
  return response

# ######################################################
# gets seagaugeg4 modifycaltable parameters
# #####################################################  
@app.route('/getcalfilexml')
@cross_origin()
def getcalfilexml():

  #userid = request.args.get('userid', '00000000000000000000000000000000')
  filekey = request.args.get('filekey', 0)
  mode = request.args.get('mode', 0)

  log.info('getcalfilexml:  filekey %s:  ', filekey)
  log.info('getcalfilexml:  mode %s:  ', mode)
   
  try:  
    conn = db_pool.getconn()

  except:
    e = sys.exc_info()[0]
    log.info("getuser_endpoint error - db_pool.getconn %s", deviceid)
    log.info('getuser_endpoint error: db_pool.getconn %s:  ' % e)
    db_pool.closeall()  

    return jsonify( message='Could not open a connection', status='error')
  
  cursor = conn.cursor()

  #sqlstr = "select filecontentsxml, filetype from sgg4calfiles where (useridkey = '00000000000000000000000000000000' OR useridkey = %s) and filename = %s;"
  sqlstr = "select filecontentsxml, filetype, filename from sgg4calfiles where prefidkey = %s;"
  
  cursor.execute(sqlstr, (filekey,))

  records = cursor.fetchone()


  log.info('getcalfilelist: records found for userid %s:  ', records)              

  
  db_pool.putconn(conn)
  

  result = json.dumps(
    dict(
      records=records
    ),
    cls=DateEncoder
  )


  log.info('getcalfilelist: records found for userid %s:  ', result)

  if int(mode) == 1:

    response = make_response(str(records[0]) )
    response.headers['Content-Type'] = 'text/csv'
    response.headers["Content-Disposition"] = "attachment; filename=" + str(records[2])
    return response
  
  else:
    
    response = make_response(result)
    response.headers['content-type'] = "application/json"
    return response


# ######################################################
# gets user info from a userid
# #####################################################
@app.route('/getuser')
@cross_origin()
def getuser_endpoint():

  try:  
    conn = db_pool.getconn()

  except:
    e = sys.exc_info()[0]
    #log.info("getuser_endpoint error - db_pool.getconn %s", deviceid)
    log.info('getuser_endpoint error: db_pool.getconn %s:  ' % e)
    db_pool.closeall()  

    return jsonify( message='Could not open a connection', status='error')


  gettype = request.args.get('gettype', 'devices')
  userid = request.args.get('userid', '4d231fb3a164c5eeb1a8634d34c578eb')
  deviceid = request.args.get('deviceid', '000000000000')
  pagetype = request.args.get('pagetype', 0)
  prefkey = request.args.get('prefkey', 0)

  query = "select devicename from user_devices where userid = %s"

  log.info('getuser_endpoint: deviceid %s:  ', deviceid)
  
  
  try:
    # first check db to see if user id is matched to device id
    cursor = conn.cursor()
    cursor.execute(query, (userid,))
    i = cursor.fetchone()
    # if not then just exit
    if cursor.rowcount == 0:
        log.info('getuser_endpoint: No devices found for userid %s:  ', userid)
        return jsonify( message='No Userid  match', status='error')


    log.info('getuser_endpoint: devices found for userid %s:  ', userid)

    
    if gettype == 'devices':
        sqlstr = 'select * from getuserdevices(%s);'   
        cursor.execute(sqlstr, (userid,))
    elif gettype == 'devicekeys':
        sqlstr = 'select devicename, deviceid, deviceapikey from user_devices where userid = %s;'
        cursor.execute(sqlstr, (userid,))
    elif gettype == 'values':
        sqlstr = 'select * from user_devices where userid = %s order by deviceid desc;'   
        cursor.execute(sqlstr, (userid,))
    elif gettype == 'pageprefnames':
        sqlstr = 'select * from getuserpageprefnames(%s,%s);'   
        cursor.execute(sqlstr, (userid, pagetype))
    elif gettype == 'pageprefs':
        sqlstr = 'select * from getuserpageprefs(%s,%s,%s);'   
        cursor.execute(sqlstr, (userid, pagetype, prefkey))
    elif gettype == 'tempodb_pageprefnames':
        sqlstr = 'select * from gettempodbuserpageprefnames(%s,%s, %s);'   
        cursor.execute(sqlstr, (userid, deviceid, pagetype))
    elif gettype == 'tempodb_pageprefs':
        sqlstr = 'select * from gettempodbuserpageprefs(%s,%s,%s);'   
        cursor.execute(sqlstr, (userid, pagetype, prefkey))
    elif gettype == 'AlertIDs':
        sqlstr = 'select messagekey, message_json, startdatetime, enddatetime from post_messages where DeviceID = %s;'   
        cursor.execute(sqlstr, (deviceid,))
        #cursor.execute(sqlstr, (userid,))
    elif gettype == 'AlertIDDetail':
        sqlstr = 'select message_json, startdatetime from post_messages where messagekey = %s;'   
        cursor.execute(sqlstr, (prefkey,))
        
    elif gettype == 'alexaprefs':
        sqlstr = 'select messagekey, message_json from alexa_prefs where userid = %s;'   
        cursor.execute(sqlstr, (userid,))

    elif gettype == 'meshdimmerprefnames':
        sqlstr = 'select prefidkey, prefname from user_meshdimmer_prefs where userid = %s and deviceid = %s;'   
        cursor.execute(sqlstr, (userid, deviceid))

    elif gettype == 'meshdimmerprefdetail':
        sqlstr = 'select prefidkey, prefname, gatewayinstance, SystemClockPGNID, DimmerLabels, scenes_json from user_meshdimmer_prefs where prefidkey  = %s;'   
        cursor.execute(sqlstr, (prefkey,))


        
    elif gettype == 'timmerprefs':
        sqlstr = 'select messagekey, message_json from timmer_prefs where userid = %s;'   
        cursor.execute(sqlstr, (userid,))

       
    elif gettype == 'scheduleprefs':
        sqlstr = 'select messagekey, message_json from timmer_prefs where userid = %s and deviceid = %s;'     
        cursor.execute(sqlstr, (userid, deviceid))

    #select devicexml,networkxml,pulsexml,runtimexml,pgnsxml from user_sgg4configxml where deviceidkey = '1f389afd27e33799752b11838e7bc4ef';
    elif gettype == 'sgg4prefnames':
        #sqlstr = 'select devicexml,networkxml,pulsexml,runtimexml,pgnsxml from user_sgg4configxml where userid = %s and deviceid = %s;'
        sqlstr = 'select prefidkey, deviceid, prefname from user_sgg4configxml where useridkey = %s and deviceid = %s;'    
        cursor.execute(sqlstr, (userid, deviceid))

    #select devicexml,networkxml,pulsexml,runtimexml,pgnsxml from user_sgg4configxml where deviceidkey = '1f389afd27e33799752b11838e7bc4ef';
    elif gettype == 'sgg4prefs':
        #sqlstr = 'select devicexml,networkxml,pulsexml,runtimexml,pgnsxml from user_sgg4configxml where userid = %s and deviceid = %s;'
        sqlstr = 'select devicexml, networkxml, pulsexml, pgnsxml, runtimexml from user_sgg4configxml where prefidkey = %s;'    
        cursor.execute(sqlstr, (prefkey,))

        
    else:
        return jsonify(result="OK")
    
    records = cursor.fetchall()


    log.info('getuser_endpoint: records found for userid %s:  ', records)    

    def type_for(type_code):
      return {
        23: 'INTEGER',
        1043: 'STRING',
        1114: 'DATETIME'    
      }.get(type_code)


    schema = dict(
      fields= [
        dict(name=c.name, type=type_for(c.type_code))
        for c in cursor.description
      ]
    )

    result = json.dumps(
      dict(
        schema=schema,
        records=records
      ),
      cls=DateEncoder
    )


    log.info('getuser_endpoint: result found for userid %s:  ', result)
    
    response = make_response(result)
    response.headers['content-type'] = "application/json"
    return response

  except TypeError as e:
      log.info('getuser_endpoint: TypeError in geting deviceid  %s:  ', deviceid)
      log.info('getuser_endpoint: TypeError in geting deviceid  %s:  ' % str(e))

  except KeyError as e:
      log.info('getuser_endpoint: KeyError in geting deviceid  %s:  ', deviceid)
      log.info('getuser_endpoint: KeyError in geting deviceid  %s:  ' % str(e))
      
  except:
    e = sys.exc_info()[0]
    log.info("getuser_endpoint error - deviceid %s", deviceid)
    log.info('getuser_endpoint error: Error in getting prefs %s:  ' % e)
  
  finally:
    db_pool.putconn(conn)    

# ######################################################
# gets user info from a userid
# #####################################################
@app.route('/getdevicesbyemail')
@cross_origin()
def getdevicesbyemail_endpoint():

  try:  
    conn = db_pool.getconn()

  except:
    e = sys.exc_info()[0]
    #log.info("getdevicesbyemail_endpoint error - db_pool.getconn %s", deviceid)
    log.info('getdevicesbyemail_endpoint error: db_pool.getconn %s:  ' % e)
    db_pool.closeall()  

    return jsonify( message='Could not open a connection', status='error')


  gettype = request.args.get('gettype', 'devices')
  useremail = request.args.get('useremail', 'guest@helmsmart.com')
  deviceid = request.args.get('deviceid', '000000000000')
  pagetype = request.args.get('pagetype', 0)
  prefkey = request.args.get('prefkey', 0)

  query = "select devicename from user_devices where useremail = %s"

  log.info('getdevicesbyemail_endpoint: useremail %s:  ', useremail)
  
  
  try:
    # first check db to see if user id is matched to device id
    cursor = conn.cursor()
    cursor.execute(query, (useremail,))
    i = cursor.fetchone()
    # if not then just exit
    if cursor.rowcount == 0:
        log.info('getdevicesbyemail_endpoint: No devices found for useremail %s:  ', useremail)
        return jsonify( message='No Userid  match', status='error')


    log.info('getuser_endpoint: devices found for useremail %s:  ', useremail)

    
    sqlstr = 'select * from user_devices where useremail = %s order by deviceid desc;'   
    cursor.execute(sqlstr, (useremail,))
        
    records = cursor.fetchall()


    log.info('getdevicesbyemail_endpoint: records found for useremail %s:  ', records)    

    def type_for(type_code):
      return {
        23: 'INTEGER',
        1043: 'STRING',
        1114: 'DATETIME'    
      }.get(type_code)


    schema = dict(
      fields= [
        dict(name=c.name, type=type_for(c.type_code))
        for c in cursor.description
      ]
    )

    result = json.dumps(
      dict(
        schema=schema,
        records=records
      ),
      cls=DateEncoder
    )


    log.info('getdevicesbyemail_endpoint: result found for useremail %s:  ', result)
    
    response = make_response(result)
    response.headers['content-type'] = "application/json"
    return response

  except TypeError as e:
      log.info('getdevicesbyemail_endpoint: TypeError in geting deviceid  %s:  ', useremail)
      log.info('getdevicesbyemail_endpoint: TypeError in geting deviceid  %s:  ' % str(e))
      return jsonify(result="TypeError")

  except KeyError as e:
      log.info('getdevicesbyemail_endpoint: KeyError in geting deviceid  %s:  ', useremail)
      log.info('getdevicesbyemail_endpoint: KeyError in geting deviceid  %s:  ' % str(e))
      return jsonify(result="KeyError")
    
  except NameError as e:
      log.info('getdevicesbyemail_endpoint: NameError in geting deviceid  %s:  ', useremail)
      log.info('getdevicesbyemail_endpoint: NameError in geting deviceid  %s:  ' % str(e))
      return jsonify(result="NameError")
      
  except:
    e = sys.exc_info()[0]
    log.info("getdevicesbyemail_endpoint error - deviceid %s", useremail)
    log.info('getdevicesbyemail_endpoint error: Error in getting prefs %s:  ' % e)
    return jsonify(result="ERROR")
  
  finally:
    db_pool.putconn(conn)    


    

@app.route('/prefs' , methods=['GET','POST'])
def prefs_endpoint():
  conn = db_pool.getconn()

  gettype = request.args.get('type', 'update')
  userid = request.args.get('userid', '')
  alexaemail = request.args.get('email', '')
  pagetype = request.args.get('pagetype', 0)
  prefkey = request.args.get('prefkey', 0)
  options = request.args.get('options', 0)
  deviceid = request.args.get('deviceid', '000000000000')
  start = request.args.get('start', 0)
  end = request.args.get('end', 0)
  interval = request.args.get('interval', 0)
  repeat = request.args.get('repeat', 0)
  instance = request.args.get('instance', '0')
  systemclock = request.args.get('systemclock', '0')
  labels = request.args.get('labels', '')
  prefname = request.args.get('prefname', 'default')
  

  if userid == "":
    try:
      session['userid']
    except:
      return jsonify( message='No Session exists', status='error')

    if session['userid'] != userid:
      return jsonify( message='No one is signed in', status='error')
    
  else:
    if userid == '0':
       return jsonify( message='Guest cannot modify prefs', status='error')
  
  
  query = "select devicename from user_devices where userid = %s"
  
  try:
    ## first check db to see if user id is matched to device id
    cursor = conn.cursor()
    #cursor.execute(query, (userid,))
    #i = cursor.fetchone()
    ## if not then just exit
    #if cursor.rowcount == 0:
    #    return jsonify( message='No Userid  match', status='error')

    if gettype == 'update':
        sqlstr = 'select * from updateuserpageprefs(%s, %s,'+ options + ');'   
        cursor.execute(sqlstr, (prefkey, userid))
    elif gettype == 'add':
        sqlstr = 'select * from setuserpageprefs(%s,%s,%s,'+ options + ');' 
        cursor.execute(sqlstr, (userid, pagetype, prefkey))
    elif gettype == 'delete':
        sqlstr = 'select * from deleteuserpageprefs(%s,%s);' 
        cursor.execute(sqlstr, (userid, prefkey))
    elif gettype == 'update_tempodb':
        sqlstr = 'select * from updatetempodbuserpageprefs(%s, %s,'+ options + ');'   
        cursor.execute(sqlstr, (prefkey, userid))
    elif gettype == 'add_tempodb':
        sqlstr = 'select * from settempodbuserpageprefs(%s,%s,%s,'+ options + ');' 
        cursor.execute(sqlstr, (userid, pagetype, prefkey))
    elif gettype == 'delete_tempodb':
        sqlstr = 'select * from deletetempodbuserpageprefs(%s,%s);' 
        cursor.execute(sqlstr, (userid, prefkey))



    elif gettype == 'add_alert':
        log.info("prefs add_alert%s : %s", deviceid, request.data)       
        sqlstr = 'select * from setalertprefs(%s,%s,%s,%s,%s,%s);' 
        cursor.execute(sqlstr, (deviceid, start, end, interval, repeat, options))


    elif gettype == 'update_alert':
        log.info("prefs update_alert %s : %s", deviceid, request.data)  
        sqlstr = 'select * from updatealertprefs(%s,%s,%s,%s,%s,%s,%s);'
        log.info("prefs update_alert deviveid %s : %s %s %s %s %s %s %s ", deviceid, prefkey, deviceid, start, end, interval, repeat, options)  
        cursor.execute(sqlstr, (prefkey, deviceid, start, end, interval, repeat, options))


    elif gettype == 'delete_alert':
        sqlstr = 'delete from post_messages where messagekey = %s;' 
        cursor.execute(sqlstr, (prefkey, ))

        
    elif gettype == 'add_alexa_pref':
        sqlstr = 'select * from setalexaprefs(%s,%s,%s,%s);' 
        cursor.execute(sqlstr, (userid, alexaemail, deviceid, options))
    elif gettype == 'update_alexa_pref':
        sqlstr = 'select * from updatealexaprefs(%s,%s,%s,%s,%s);' 
        cursor.execute(sqlstr, (prefkey, userid, alexaemail, deviceid,  options))
    elif gettype == 'delete_alexa_pref':
        sqlstr = 'delete from alexa_prefs where messagekey = %s;' 
        cursor.execute(sqlstr, (prefkey, ))

    elif gettype == 'add_meshdimmer_pref':
        sqlstr = 'select * from setmeshdimmerprefs(%s,%s,%s,%s,%s,%s,%s);' 
        cursor.execute(sqlstr, (userid, prefname, deviceid, instance, systemclock,labels,options))
    elif gettype == 'update_meshdimmer_pref':
        sqlstr = 'select * from updatemeshdimmerprefs(%s,%s,%s,%s,%s,%s,%s,%s);' 
        cursor.execute(sqlstr, (prefkey, userid, prefname, deviceid, instance, systemclock,labels,options))
    elif gettype == 'delete_meshdimmer_pref':
        sqlstr = 'delete from user_meshdimmer_prefs where prefidkey = %s;' 
        cursor.execute(sqlstr, (prefkey, ))         

    elif gettype == 'add_timmer_pref':

      
      log.info("prefs add timmer_prefs data %s : %s", deviceid, request.mimetype)
      log.info("prefs add timmer_prefs data %s : %s", deviceid, request.form.to_dict(flat=False))


      log.info("prefs add timmer_prefs data %s : %s", deviceid, request.data)
      #log.info("prefs add timmer_prefs form %s : %s", deviceid, request.form) 
      #myTimmerPrefs = json.loads(request.form)
      # myTimmerPrefs = request.form['timmerprefs']
      #myTimmerPrefs = request.form        
      #log.info("prefs add timmer_prefs myTimmerPrefs %s : %s", deviceid, myTimmerPrefs) 
      #options = json.loads(request.data)
      #log.info("prefs add timmer_prefs options %s : %s", deviceid, options)
      #log.info("prefs add timmer_prefs %s : %s", deviceid, json.dumps(options))



      
      sqlstr = 'select * from settimmerprefs(%s,%s,%s);' 
      #cursor.execute(sqlstr, (userid, deviceid, options))
      cursor.execute(sqlstr, (userid, deviceid, request.data))
      
    elif gettype == 'update_timmer_pref':
      log.info("prefs update timmer_prefs %s : %s", deviceid, request.data)      
      #myTimmerPrefs = json.loads(request.form)
      #options = myTimmerPrefs['timmerprefs']
      #log.info("prefs update timmer_prefs %s : %s", deviceid, json.dumps(options))
      
      sqlstr = 'select * from updatetimmerprefs(%s,%s,%s,%s);' 
      #cursor.execute(sqlstr, (prefkey, userid, deviceid,  options))
      #cursor.execute(sqlstr, (prefkey, userid, deviceid,  json.dumps(options)))
      cursor.execute(sqlstr, (prefkey, userid, deviceid,  request.data))
      
    elif gettype == 'delete_timmer_pref':
        sqlstr = 'delete from timmer_prefs where messagekey = %s;' 
        cursor.execute(sqlstr, (prefkey, ))         
        

        
    else:
        return jsonify( message='error updating pref - no type', status='error')

    conn.commit()
    #i = cursor.fetchone()
    # if not then just exit
    #if cursor.rowcount == 0:
    #    return jsonify( message='error updating pref', status='error')

  #try:
    #cursor = conn.cursor()
    #cursor.execute(request.args['i'])
    #conn.commit()

    #return jsonify( message=sqlstr, status='error')
    return jsonify(result="OK")
  #except:
  #  conn.rollback()
  finally:
    db_pool.putconn(conn)







@app.route('/help')
@cross_origin()
def help():

    response = make_response(render_template('index.html', features = []))
    #response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


### user functions #####

def getedeviceid(deviceapikey):

    deviceid = ""

    conn = db_pool.getconn()

    log.info("freeboard getedeviceid data Query %s", deviceapikey)
    #query = "select deviceid from user_devices where deviceapikey = %s"

    #query = ("select deviceid from user_devices where deviceapikey = '{}' ") \
    #            .format(deviceapikey )


    #log.info("freeboard getedeviceid Query %s", query)


    try:
    # first check db to see if deviceapikey is matched to device id

        cursor = conn.cursor()
        #cursor.execute(query, (deviceapikey,))
        #cursor.execute("select deviceid from user_devices where deviceapikey = '%s'" % deviceapikey)
        #key=('bfeba0c3c5244269b4c8d276872519a6',)
        cursor.execute("select deviceid from user_devices where deviceapikey = %s" , (deviceapikey,))
        #response= cursor.query(query)
        i = cursor.fetchone()
        log.info("freeboard getedeviceid response %s", i)            
        # see we got any matches
        if cursor.rowcount == 0:
        #if not response:
            # cursor.close
            db_pool.putconn(conn) 
            return ""
        
        else:
            deviceid = str(i[0])

            cursor.execute("update user_devices set api_queries = api_queries + 1 where deviceapikey = %s" , (deviceapikey,))
            conn.commit()
            log.info("freeboard getedeviceid updare apiquery response ") 

            db_pool.putconn(conn)
            
            return deviceid 


    except TypeError as e:
        log.info('freeboard: TypeError in geting deviceid  %s:  ', deviceapikey)
        log.info('freeboard: TypeError in geting deviceid  %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: KeyError in geting deviceid  %s:  ', deviceapikey)
        log.info('freeboard: KeyError in geting deviceid  %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: NameError in geting deviceid  %s:  ', deviceapikey)
        log.info('freeboard: NameError in geting deviceid  %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: IndexError in geting deviceid  %s:  ', deviceapikey)
        log.info('freeboard: IndexError in geting deviceid  %s:  ' % str(e))  


    except:
        log.info('freeboard: Error in geting  deviceid %s:  ', deviceapikey)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting deviceid  %s:  ' % str(e))

    # cursor.close
    db_pool.putconn(conn)                       

    return deviceid



def getedevicename(deviceapikey):

    conn = db_pool.getconn()

    log.info("freeboard getedevicename data Query %s", deviceapikey)
    #query = "select deviceid from user_devices where deviceapikey = %s"

    #query = ("select deviceid from user_devices where deviceapikey = '{}' ") \
    #            .format(deviceapikey )


    #log.info("freeboard getedeviceid Query %s", query)


    try:
    # first check db to see if deviceapikey is matched to device id

        cursor = conn.cursor()
        #cursor.execute(query, (deviceapikey,))
        #cursor.execute("select deviceid from user_devices where deviceapikey = '%s'" % deviceapikey)
        #key=('bfeba0c3c5244269b4c8d276872519a6',)
        cursor.execute("select devicename from user_devices where deviceapikey = %s" , (deviceapikey,))
        #response= cursor.query(query)
        i = cursor.fetchone()
        log.info("freeboard getedevicename response %s", i)            
        # see we got any matches
        if cursor.rowcount == 0:
        #if not response:
            # cursor.close
            db_pool.putconn(conn) 
            return ""
        
        else:
            devicename = str(i[0])
            db_pool.putconn(conn) 
            return devicename 


    except TypeError as e:
        log.info('freeboard: TypeError in geting devicename  %s:  ', deviceapikey)
        log.info('freeboard: TypeError in geting devicename  %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: KeyError in geting devicename  %s:  ', deviceapikey)
        log.info('freeboard: KeyError in geting devicename  %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: NameError in geting devicename  %s:  ', deviceapikey)
        log.info('freeboard: NameError in geting devicename  %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: IndexError in geting devicename  %s:  ', deviceapikey)
        log.info('freeboard: IndexError in geting devicename  %s:  ' % str(e))  


    except:
        log.info('freeboard: Error in geting  devicename %s:  ', deviceapikey)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting devicename  %s:  ' % str(e))

    # cursor.close
    db_pool.putconn(conn)                       

    return ""




def getuseremail(deviceapikey):

    conn = db_pool.getconn()

    log.info("freeboard getuseremail data Query %s", deviceapikey)
    #query = "select deviceid from user_devices where deviceapikey = %s"

    #query = ("select deviceid from user_devices where deviceapikey = '{}' ") \
    #            .format(deviceapikey )


    #log.info("freeboard getedeviceid Query %s", query)


    try:
    # first check db to see if deviceapikey is matched to device id

        cursor = conn.cursor()
        #cursor.execute(query, (deviceapikey,))
        #cursor.execute("select deviceid from user_devices where deviceapikey = '%s'" % deviceapikey)
        #key=('bfeba0c3c5244269b4c8d276872519a6',)
        cursor.execute("select useremail from user_devices where deviceapikey = %s" , (deviceapikey,))
        #response= cursor.query(query)
        i = cursor.fetchone()
        log.info("freeboard getuseremail response %s", i)            
        # see we got any matches
        if cursor.rowcount == 0:
        #if not response:
            # cursor.close
            db_pool.putconn(conn) 
            return ""
        
        else:
            useremail = str(i[0])
            db_pool.putconn(conn) 
            return useremail 


    except TypeError as e:
        log.info('freeboard: TypeError in geting useremail  %s:  ', deviceapikey)
        log.info('freeboard: TypeError in geting deviceid  %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: KeyError in geting useremail  %s:  ', deviceapikey)
        log.info('freeboard: KeyError in geting useremail  %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: NameError in geting useremail  %s:  ', deviceapikey)
        log.info('freeboard: NameError in geting useremail  %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: IndexError in geting useremail  %s:  ', deviceapikey)
        log.info('freeboard: IndexError in geting useremail  %s:  ' % str(e))  


    except:
        log.info('freeboard: Error in geting  useremail %s:  ', deviceapikey)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting useremail  %s:  ' % str(e))

    # cursor.close
    db_pool.putconn(conn)                       

    return ""


@app.route('/get_influxdbcloud_series')
def get_influxdbcloud_series():
  deviceid = request.args.get('deviceid', '000000000000')
  startepoch = request.args.get('startepoch', 0)
  endepoch = request.args.get('endepoch', 0)

  response  = None

  
  host = 'hilldale-670d9ee3.influxcloud.net' 
  port = 8086
  username = 'helmsmart'
  password = 'Salm0n16'
  database = 'pushsmart-cloud'

  measurement = "HS_" + str(deviceid)

  log.info("get_influxdbcloud_series deviceid %s", deviceid)
  
  #db = influxdb.InfluxDBClient(host, port, username, password, database)
  db = InfluxDBCloud(host, port, username, password, database,  ssl=True)

  if  startepoch == 0 or  endepoch == 0:
    query = ('select * from /deviceid:{}.*/  limit 1') \
            .format(deviceid, startepoch, endepoch)
  else:
    #query = ('select * from /deviceid:{}.*/ where time > {}s and time < {}s  limit 1') \
    #        .format(deviceid, startepoch, endepoch)

    query = ("select  * from {} "
           "where deviceid='{}'  AND  time > {}s AND  time < {}s group by * limit 1") \
        .format(measurement, deviceid,
              startepoch, endepoch)
    
  log.info("get_influxdbcloud_series Query %s", query)
    
  try:
    response= db.query(query)

  except InfluxDBClientError as e:
    log.info('get_influxdbcloud_series: Exception InfluxDBClientError in InfluxDB  %s:  ' % str(e))
    return jsonify( message='Error in inFluxDB series InfluxDBClientError', status='error')
    
  except InfluxDBServerError as e:
    log.info('get_influxdbcloud_series: Exception InfluxDBServerError in InfluxDB  %s:  ' % str(e))
    return jsonify( message='Error in inFluxDB series InfluxDBServerError', status='error')
    
  except:
    #log.info('Telemetrypost: Error in geting Telemetry parameters %s:  ', posttype)
    e = sys.exc_info()[0]
    log.info('get_influxdbcloud_series: Error in geting inFluxDB data %s:  ' % e)
    
    return jsonify( message='Error in inFluxDB series query 2', status='error')
    
  if not response:
    #print 'inFluxDB Exception1:', response.response.successful, response.response.reason 
    return jsonify( message='No response to return 1' , status='error')

  try:

 
    keys = response.raw.get('series',[])
    jsondata = []
    keyslen = len(keys)
    
    for key in keys:
      keytags = key['tags']
      keyvalues = key['values']
      keyvalue = keyvalues[0]


      fields = {}
      for keyi, val in zip(key['columns'], keyvalue):
        fields[keyi] = val
      #source = fields['source']
      source = fields.get('source', '.*')
      keytags['source']=source
          
      #jsondata.append({'tags':keytags, 'source':source} )
      jsondata.append(keytags)
          

    #return jsonify(keys = jsondata ,  status='success')
    return jsonify(series = jsondata, keyslen=keyslen ,  status='success')
    """  
    keys = response.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)

    
    jsondata=[]
    for series in keys:
      log.info("get_influxdbcloud_series Get InfluxDB series key %s", series)
      #log.info("freeboard Get InfluxDB series tag %s ", series[1])
      #log.info("freeboard Get InfluxDB series tag deviceid %s ", series[1]['deviceid'])
      #strvalue = {'deviceid':series[1]['deviceid'], 'sensor':series[1]['sensor'], 'source': series[1]['source'], 'instance':series[1]['instance'], 'type':series[1]['type'], 'parameter': series[1]['parameter'], 'epoch':endepoch}
      strvalue = {'deviceid':series[1]['deviceid'], 'sensor':series[1]['sensor'], 'source':'FF', 'instance':series[1]['instance'], 'type':series[1]['type'], 'parameter': series[1]['parameter'], 'epoch':endepoch}


      jsondata.append(strvalue)
      #for tags in series[1]:
      #  log.info("freeboard Get InfluxDB tags %s ", tags)
 
    #return jsonify( message='freeboard_createInfluxDB', status='error')
    return jsonify(series = jsondata, keyslen=keyslen ,  status='success')
    """
  
  except TypeError as e:
    #log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
    log.info('get_influxdbcloud_series: Type Error in InfluxDB  %s:  ' % str(e))

  except KeyError as e:
    #log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
    log.info('get_influxdbcloud_series: Key Error in InfluxDB  %s:  ' % str(e))

  except NameError as e:
    #log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
    log.info('get_influxdbcloud_series: Name Error in InfluxDB  %s:  ' % str(e))
            
  except IndexError as e:
    #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
    log.info('get_influxdbcloud_series: Index Error in InfluxDB  %s:  ' % str(e))  
            
  except ValueError as e:
    #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
    log.info('get_influxdbcloud_series: Value Error in InfluxDB  %s:  ' % str(e))

  except AttributeError as e:
    #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
    log.info('get_influxdbcloud_series: AttributeError in InfluxDB  %s:  ' % str(e))     

  #except InfluxDBCloud.exceptions.InfluxDBClientError as e:
    #log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))

  except InfluxDBClientError as e:
    log.info('get_influxdbcloud_series: Exception Error in InfluxDBClientError  %s:  ' % str(e))

  except InfluxDBServerError as e:
    log.info('get_influxdbcloud_series: Exception Error in InfluxDBServerError  %s:  ' % str(e))
   

  except:
    #log.info('freeboard: Error in InfluxDB mydata append %s:', response)
    e = sys.exc_info()[0]
    log.info("get_influxdbcloud_series: Error: %s" % e)

  return jsonify( message='freeboard_GetSeries', status='error')




@app.route('/get_influxdbcloud_data')
def get_influxdbcloud_data():
  conn = db_pool.getconn()



  pgnnumber = request.args.get('pgnnumber', '000000')
  userid = request.args.get('userid', '4d231fb3a164c5eeb1a8634d34c578eb')
  deviceid = request.args.get('deviceid', '000000000000')
  startepoch = request.args.get('startepoch', 0)
  endepoch = request.args.get('endepoch', 0)
  resolution = request.args.get('resolution', 60)
  rollup = request.args.get('rollup', 'mean')
  SERIES_KEY = request.args.get('serieskey', 0)

  response = None
  
  if SERIES_KEY.find(".*.") > 0:  
    SERIES_KEY = SERIES_KEY.replace(".*.","*.")

    
  query = "select devicename from user_devices where userid = %s AND deviceid = %s"
  sqlstr = 'select * from getpgn' + pgnnumber + '(%s,%s,%s,%s,%s,%s,%s);'


  try:
    ## first check db to see if user id is matched to device id
    cursor = conn.cursor()
    #cursor.execute(query, (userid, deviceid))
    #i = cursor.fetchone()
    ## if not then just exit
    #if cursor.rowcount == 0:
    #    return jsonify( message='No Userid = deviceid match', status='error')
        
    ## else run the query
  



    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'


    measurement = "HelmSmart"
    measurement = "HS_" + str(deviceid)

  
    #db = influxdb.InfluxDBClient(host, port, username, password, database)
    db = InfluxDBCloud(host, port, username, password, database,  ssl=True)
     
    #shim = Shim(host, port, username, password, database)
    
    #start = datetime.date(2014, 2, 24)
    #start = datetime.date(startepoch)
    #start = datetime.datetime.utcfromtimestamp(float(startepoch))

    #startepoch = 1393257600
    #endepoch = 1393804800
    #resolution="60"
    
    start = datetime.datetime.fromtimestamp(float(startepoch))
    

    end = datetime.datetime.fromtimestamp(float(endepoch))
    resolutionstr = "PT" + str(resolution) + "S"

    #rollup = "mean"

    #print 'inFlux Series Key:', SERIES_KEY
    log.info("inFlux SERIES_KEY %s", SERIES_KEY)
    #attrs = key_to_attributes(SERIES_KEY)  
    #name = "{}.{}.{}.{}.{}".format(attrs['deviceid'], attrs['sensor'], attrs['instance'], attrs['type'], attrs['parameter'])
    
    #query = 'select MEAN(value) from "001EC0B415BF.environmental_data.0.Outside Temperature.temperature" where time > now() - 1d group by time(10m);'

    seriesname = SERIES_KEY
    seriestags = seriesname.split(".")

    if len(seriestags) < 6:
      return jsonify( message='serieskey empty - No data to return' , status='error')

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

    if seriessource[1] == "*":
      serieskeys=" deviceid='"
      serieskeys= serieskeys + seriesdeviceid[1] + "' AND "
      serieskeys= serieskeys +  " sensor='" +  seriessensor[1] + "'  AND "
      serieskeys= serieskeys +  " instance='" +  seriesinstance[1] + "'  AND "

      
      if seriestype[1] != "*":
        serieskeys= serieskeys +  " type='" +  seriestype[1] + "'  AND "

        
      serieskeys= serieskeys +  " parameter='" +  seriesparameter[1] + "'   "

      log.info("inFlux-cloud serieskeys %s", serieskeys)


      query = ('select {}({}) AS {}, last(source) as source FROM {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by *, time({}s)') \
                  .format(rollup, parameter, parameter, measurement, serieskeys,
                          startepoch, endepoch,
                          resolution) 

    else:
      serieskeys=" deviceid='"
      serieskeys= serieskeys + seriesdeviceid[1] + "' AND "
      serieskeys= serieskeys +  " sensor='" +  seriessensor[1] + "'  AND "
      #serieskeys= serieskeys +  " source='" +  seriessource[1] + "'  AND "
      serieskeys= serieskeys +  " instance='" +  seriesinstance[1] + "'  AND "

      if seriestype[1] != "*":
        serieskeys= serieskeys +  " type='" +  seriestype[1] + "'  AND "

        
      serieskeys= serieskeys +  " parameter='" +  seriesparameter[1] + "'   "   

      log.info("inFlux-cloud serieskeys %s", serieskeys)


      query = ("select {}({}) AS {}, last(source) as source FROM {} "
                       "where {} AND source = '{}' AND time > {}s and time < {}s "
                       "group by *, time({}s)") \
                  .format(rollup, parameter, parameter, measurement, serieskeys, seriessource[1],
                          startepoch, endepoch,
                          resolution) 
      
    
    log.info("inFlux-cloud Query %s", query)
    

    try:
      response= db.query(query)

    except InfluxDBClientError as e:
      log.info('get_influxdbcloud_data: Exception Error in InfluxDB  %s:  ' % str(e))
      
    except:
      e = sys.exc_info()[0]
      log.info('inFluxDB: Error in geting inFluxDB data %s:  ' % e)
        
      return jsonify( message='Error in inFluxDB query 2', status='error')
      #raise

    
    #return jsonify(results=response)
    
    #response =  shim.read_multi(keys=[SERIES_KEY], start=start, end=end, period=resolutionstr, rollup="mean" )
    
    #print 'inFluxDB read :', response.response.successful

    
    if not response:
      #print 'inFluxDB Exception1:', response.response.successful, response.response.reason 
      return jsonify( message='No response to return 1' , status='error')

    try:
  
      #if not response.points:
      #  #print 'inFluxDB Exception2:', response.response.successful, response.response.reason 
      #  return jsonify( message='No data to return 2', status='error')

      #print 'inFluxDB processing data headers:'
      jsondata=[]
      jsonkey=[]
      #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
      #jsonkey.append(strvaluekey)
      #print 'inFluxDB start processing data points:'
      #log.info("freeboard Get InfluxDB response %s", response)

      keys = response.raw.get('series',[])
      #log.info("freeboard Get InfluxDB series keys %s", keys)




      strvalue=""
      
      for series in keys:
        #log.info("freeboard Get InfluxDB series key %s", series)
        #log.info("freeboard Get InfluxDB series tags %s ", series['tags'])
        #log.info("freeboard Get InfluxDB series columns %s ", series['columns'])
        #log.info("freeboard Get InfluxDB series values %s ", series['values'])

        """        
        values = series['values']
        for value in values:
          log.info("freeboard Get InfluxDB series time %s", value[0])
          log.info("freeboard Get InfluxDB series mean %s", value[1])
        """

        tag = series['tags']
        log.info("freeboard Get InfluxDB series tags2 %s ", tag)

        #mydatetimestr = str(fields['time'])
        strvaluekey = {'Series': series['tags'], 'start': startepoch,  'end': endepoch, 'resolution': resolution}
        jsonkey.append(strvaluekey)        

        #log.info("freeboard Get InfluxDB series tags3 %s ", tag['source'])

        
        for point in series['values']:
          fields = {}
          fields[parameter] = None
          
          for key, val in zip(series['columns'], point):
            fields[key] = val
            
          #log.info("freeboard Get InfluxDB series points %s , %s, %s", fields['time'], fields[parameter],  fields['source'])

          mydatetimestr = str(fields['time'])

          #mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')
          mydatetime =  int(time.mktime(time.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')))
          
          #strvalue = {'epoch': fields['time'], 'source':tag['source'], 'value': fields[parameter]}
          if fields[parameter] is not None:
            #strvalue = {'epoch': mydatetime, 'source':tag['source'], 'value': fields[parameter]}
            #strvalue = {'epoch': mydatetime, 'source':'FF', 'value': fields[parameter]}
            strvalue = {'epoch': mydatetime, 'source':fields['source'], 'value': fields[parameter]}
          
            jsondata.append(strvalue)





      jsondata = sorted(jsondata,key=itemgetter('epoch'))
      #print 'inFluxDB returning data points:'
      #return jsonify( results = jsondata)      
      return jsonify(serieskey = jsonkey, results = jsondata)
      #result = json.dumps(data.data, cls=DateEncoder)
    
      #response = make_response(result) 
      
      #response.headers['content-type'] = "application/json"
      #return response

    except TypeError as e:
        #log.info('get_influxdbcloud_data: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('get_influxdbcloud_data: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyErro as e:
        #log.info('get_influxdbcloud_data: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('get_influxdbcloud_data: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        #log.info('get_influxdbcloud_data: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('get_influxdbcloud_data: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        #log.info('get_influxdbcloud_data: Index error in InfluxDB mydata append %s:  ', response)
        log.info('get_influxdbcloud_data: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('get_influxdbcloud_data: Index error in InfluxDB mydata append %s:  ', response)
      log.info('get_influxdbcloud_data: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('get_influxdbcloud_data: Index error in InfluxDB mydata append %s:  ', response)
      log.info('get_influxdbcloud_data: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('get_influxdbcloud_data: Exception Error in InfluxDB  %s:  ' % str(e))     
    
    except:
      log.info('get_influxdbcloud_data: Error in geting freeboard response %s:  ', strvalue)
      e = sys.exc_info()[0]
      log.info('get_influxdbcloud_data: Error in geting freeboard ststs %s:  ' % e)
      return jsonify( message='error processing data 3' , status='error')        
  

  except InfluxDBClientError as e:
    log.info('get_influxdbcloud_data: Exception Error in InfluxDB  %s:  ' % str(e))
    
  except:
    log.info('get_influxdbcloud_data: Error in geting freeboard response %s:  ', strvalue)
    e = sys.exc_info()[0]
    log.info('get_influxdbcloud_data: Error in geting freeboard ststs %s:  ' % e)
    return jsonify( message='error processing data 4' , status='error')        

    #return jsonify(result = data.data)
    #return datasets[0].data
  finally:
    db_pool.putconn(conn)


#converts old InfluxDB Series Keys to InfluxDB_Cloud Keys
#returns string Set of tags
def convertInfluxDBCloudParameters(SERIES_KEY, name, rollup):

    if SERIES_KEY.find(".*.") > 0:  
        SERIES_KEY = SERIES_KEY.replace(".*.","*.")

    try:    

        seriesname = SERIES_KEY
        seriestags = seriesname.split(".")

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

        if debug_all: log.info('convertInfluxDBCloudParameters: STATUS %s:  ', parameter)

        if rollup == 'timmer':
            rollup = 'median'
            
        if rollup == 'timmerday':
            rollup = 'median'

        if rollup == 'sunriseset':
            rollup = 'median'
            
        if rollup == 'sunsetrise':
            rollup = 'median'


        if rollup == 'sunriseexpires':
            rollup = 'median'
            
        if rollup == 'sunsetexpires':
            rollup = 'median'


        if rollup == 'startsunrise':
            rollup = 'median'
            
        if rollup == 'startsunset':
            rollup = 'median'


        if parameter == 'latlng':
            return  "median(lat)  AS lat, median(lng) AS lng  "
        else:
            return rollup + "(" + parameter + ")  AS " + name + " "

    except TypeError as e:
        if debug_all: log.info('convertInfluxDBCloudParameters: TypeError in convertInfluxDBCloudParameters %s:  ', SERIES_KEY)
        #e = sys.exc_info()[0]

        if debug_all: log.info('convertInfluxDBCloudParameters: TypeError in convertInfluxDBCloudParameters %s:  ' % str(e))
        
    except KeyError as e:
        if debug_all: log.info('convertInfluxDBCloudParameters: KeyError in convertInfluxDBCloudParameters %s:  ', SERIES_KEY)
        #e = sys.exc_info()[0]

        if debug_all: log.info('convertInfluxDBCloudParameters: KeyError in convertInfluxDBCloudParameters %s:  ' % str(e))

    except NameError as e:
        if debug_all: log.info('convertInfluxDBCloudParameters: NameError in convertInfluxDBCloudParameters %s:  ', SERIES_KEY)
        #e = sys.exc_info()[0]

        if debug_all: log.info('convertInfluxDBCloudParameters: NameError in convertInfluxDBCloudParameters %s:  ' % str(e))

    except IndexError as e:
        if debug_all: log.info('convertInfluxDBCloudParameters: IndexError in convertInfluxDBCloudParameters %s:  ', SERIES_KEY)
        #e = sys.exc_info()[0]

        if debug_all: log.info('convertInfluxDBCloudParameters: IndexError in convertInfluxDBCloudParameters %s:  ' % str(e))          

    except:
        if debug_all: log.info('convertInfluxDBCloudParameters: Error in convertInfluxDBCloudParameters %s:  ', SERIES_KEY)
        e = sys.exc_info()[0]


        
#converts old InfluxDB Series Keys to InfluxDB_Cloud Keys
#returns string Set of tags
def convertInfluxDBCloudKeys(SERIES_KEY):

    if SERIES_KEY.find(".*.") > 0:  
        SERIES_KEY = SERIES_KEY.replace(".*.","*.")
        #SERIES_KEY.replace("*.","??")
        #SERIES_KEY.replace(".",".")
        if debug_all: log.info('convertInfluxDBCloudKeys: convertInfluxDBCloudKeys replace source %s:  ', SERIES_KEY)
                
    try:
        if debug_all: log.info('convertInfluxDBCloudKeys: SERIES_KEY %s:  ', SERIES_KEY)
        seriesname = SERIES_KEY
        seriestags = seriesname.split(".")

        if debug_all: log.info('convertInfluxDBCloudKeys: seriestags %s:  ', seriestags)

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
            
            if seriestype[1] != "*":
              serieskeys= serieskeys +  "' AND type='" +  seriestype[1]
              
            serieskeys= serieskeys +  "' AND parameter='lat') OR " 

            serieskeys=serieskeys + "( deviceid='"
            serieskeys= serieskeys + seriesdeviceid[1] 
            serieskeys= serieskeys +  "' AND sensor='" +  seriessensor[1]
            if seriessource[1] != "*":
                serieskeys= serieskeys +  "' AND source='" +  seriessource[1] 
            serieskeys= serieskeys +  "' AND instance='" +  seriesinstance[1] 

            if seriestype[1] != "*":
              serieskeys= serieskeys +  "' AND type='" +  seriestype[1]
              
            serieskeys= serieskeys +  "' AND parameter='lng') "  

                
        else:
            serieskeys="( deviceid='"
            serieskeys= serieskeys + seriesdeviceid[1] 
            serieskeys= serieskeys +  "' AND sensor='" +  seriessensor[1]
            
            if seriessource[1] != "*":
                serieskeys= serieskeys +  "' AND source='" +  seriessource[1]
                
            serieskeys= serieskeys +  "' AND instance='" +  seriesinstance[1]

            if seriestype[1] != "*":
              serieskeys= serieskeys +  "' AND type='" +  seriestype[1]
              
            serieskeys= serieskeys +  "' AND parameter='" +  seriesparameter[1] + "'   )"


        return serieskeys


    except TypeError as e:
        if debug_all: log.info('convertInfluxDBCloudKeys: TypeError in convertInfluxDBCloudKeys %s:  ', SERIES_KEY)
        #e = sys.exc_info()[0]

        if debug_all: log.info('convertInfluxDBCloudKeys: TypeError in convertInfluxDBCloudKeys %s:  ' % str(e))
        
    except KeyError as e:
        if debug_all: log.info('convertInfluxDBCloudKeys: KeyError in convertInfluxDBCloudKeys %s:  ', SERIES_KEY)
        #e = sys.exc_info()[0]

        if debug_all: log.info('convertInfluxDBCloudKeys: KeyError in convertInfluxDBCloudKeys %s:  ' % str(e))

    except NameError as e:
        if debug_all: log.info('convertInfluxDBCloudKeys: NameError in convertInfluxDBCloudKeys %s:  ', SERIES_KEY)
        #e = sys.exc_info()[0]

        if debug_all: log.info('convertInfluxDBCloudKeys: NameError in convertInfluxDBCloudKeys %s:  ' % str(e))

    except IndexError as e:
        if debug_all: log.info('convertInfluxDBCloudKeys: IndexError in convertInfluxDBCloudKeys %s:  ', SERIES_KEY)
        #e = sys.exc_info()[0]

        if debug_all: log.info('convertInfluxDBCloudKeys: IndexError in convertInfluxDBCloudKeys %s:  ' % str(e))          

    except:
        if debug_all: log.info('convertInfluxDBCloudKeys: Error in convertInfluxDBCloudKeys %s:  ', SERIES_KEY)
        e = sys.exc_info()[0]

        if debug_all: log.info('convertInfluxDBCloudKeys: IndexError in convertInfluxDBCloudKeys %s:  ' % str(e))   


  


 
  
@app.route('/getinfluxseriesmultibydeviceid')
def getinfluxseriesmultibydeviceid():

  deviceid = request.args.get('deviceid', '')
  startepoch = request.args.get('startepoch', 0)
  endepoch = request.args.get('endepoch', 0)
  resolution = request.args.get('resolution', 60)

  alerttype = request.args.get('rollup', 'mean')
  
  #SERIES_KEY1 = request.args.get('serieskey1', '')
  #UNITS_KEY1 = request.args.get('unitskey1', 255)
  #SERIES_KEY2 = request.args.get('serieskey2', '')
  #UNITS_KEY2 = request.args.get('unitskey2', 255)
  #SERIES_KEY3 = request.args.get('serieskey3', '')
  #UNITS_KEY3 = request.args.get('unitskey3', 255)
  #SERIES_KEY4 = request.args.get('serieskey4', '')
  #UNITS_KEY4 = request.args.get('unitskey4', 255)
  #SERIES_KEY5 = request.args.get('serieskey5', '')
  #UNITS_KEY5 = request.args.get('unitskey5', 255)
  #SERIES_KEY6 = request.args.get('serieskey6', '')
  #UNITS_KEY6 = request.args.get('unitskey6', 255)
  #SERIES_KEY7 = request.args.get('serieskey7', '')
  #UNITS_KEY7 = request.args.get('unitskey7', 255)
  #SERIES_KEY8 = request.args.get('serieskey8', '')
  #UNITS_KEY8 = request.args.get('unitskey8', 255)

  #alerttype=parameters.get('alerttype', "mean")

    
  influxdb_keys=[]
  influxdb_cloud_keys=[]
  influxdb_gpskeys=[]


  SERIES_KEYS=[]
  SERIES_KEY1 = ""
  SERIES_KEY2 = ""
  SERIES_KEY3 = ""
  SERIES_KEY4 = ""
  SERIES_KEY5 = ""
  SERIES_KEY6 = ""
  SERIES_KEY7 = ""  
  SERIES_KEY8 = ""
  SERIES_KEY9 = ""
  SERIES_KEY10 = ""
  SERIES_KEY11 = ""  
  SERIES_KEY12 = ""
  SERIES_KEY13 = ""
  SERIES_KEY14 = ""
  SERIES_KEY15 = ""  
  SERIES_KEY16 = ""
  series_elements = 0
  
  IDBC_KEYS=[]
  IDBC_SERIES_KEY1 = ""
  IDBC_SERIES_KEY2 = ""
  IDBC_SERIES_KEY3 = ""
  IDBC_SERIES_KEY4 = ""
  IDBC_SERIES_KEY5 = ""
  IDBC_SERIES_KEY6 = ""
  IDBC_SERIES_KEY7 = ""  
  IDBC_SERIES_KEY8 = ""


  IDBC_PARAMETERS=[]
  IDBC_SERIES_PARAMETERS1 = ""
  IDBC_SERIES_PARAMETERS2 = ""
  IDBC_SERIES_PARAMETERS3 = ""
  IDBC_SERIES_PARAMETERS4 = ""
  IDBC_SERIES_PARAMETERS5 = ""
  IDBC_SERIES_PARAMETERS6 = ""
  IDBC_SERIES_PARAMETERS7 = ""  
  IDBC_SERIES_PARAMETERS8 = ""

  UNITS_KEY1 = 255
  UNITS_KEY2 = 255
  UNITS_KEY3 = 255
  UNITS_KEY4 = 255
  UNITS_KEY5 = 255
  UNITS_KEY6 = 255
  UNITS_KEY7 = 255
  UNITS_KEY8 = 255
  
  series_elements = 0
        
  dataformat = request.args.get('format', 'json')
  #dataformat = request.args.get('format', 'csv')
  
  host = 'hilldale-670d9ee3.influxcloud.net' 
  port = 8086
  username = 'helmsmart'
  password = 'Salm0n16'
  database = 'pushsmart-cloud'


  measurement = "HelmSmart"
  measurement = "HS_" + str(deviceid)


  #db = influxdb.InfluxDBClient(host, port, username, password, database)
  dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)
  
  """
  startepoch = 1413569242
  endepoch = 1413742048
  resolution = 60
  startepoch = datetime.datetime.now() - datetime.timedelta(minutes=2)
  endepoch =  datetime.datetime.now()
  startepoch = int(time.time()) - (600)
  endepoch =  int(time.time())
  """

  names =[]

  keys = []
  units = {}
  serieskeys = ""

  Device_ID_Key = []
  Sensor_Key = []
  Source_Key = []
  Instance_Key = []
  Type_Key = []
  Parameter_Key = []
  Rollup_Key = []

  #initialize arry to empty strings
  for x in range(0, 9):
  
    Device_ID_Key.append("---")
    Sensor_Key.append("---")
    Source_Key.append("---")
    Instance_Key.append("---")
    Type_Key.append("---")
    Parameter_Key.append("---")
    Rollup_Key.append("---")

  series_elements = 0

  try:

    try:
        SERIES_KEY1= request.args.get('serieskey1', '')

        if SERIES_KEY1 != str(0):

          SERIES_KEYS.append(SERIES_KEY1)
          
          if SERIES_KEY1 != "":
            if SERIES_KEY1.find(".*.") > 0:  
              seriesname = SERIES_KEY1.replace(".*.","*.")
            else:
              seriesname = SERIES_KEY1
              
            seriestags = seriesname.split(".")

            serieslable = seriestags[0].split(":")
            Device_ID_Key[1] = serieslable[1]
            
            serieslable = seriestags[1].split(":")
            Sensor_Key[1]= serieslable[1]
            
            serieslable = seriestags[2].split(":")
            Source_Key[1]= serieslable[1]
            
            serieslable = seriestags[3].split(":")
            Instance_Key[1]= serieslable[1]
            
            serieslable = seriestags[4].split(":")
            Type_Key[1]= serieslable[1]

            serieslable = seriestags[5].split(":")
            Parameter_Key[1]= serieslable[1]        
            
            UNITS_KEY1 = request.args.get('unitskey1', 255)
            Rollup_Key[1] = alerttype

          
          IDBC_SERIES_KEY1 = convertInfluxDBCloudKeys(SERIES_KEY1)
          IDBC_KEYS.append(IDBC_SERIES_KEY1)
          
          IDBC_SERIES_PARAMETERS1 = convertInfluxDBCloudParameters(SERIES_KEY1, "value1", alerttype)
          IDBC_PARAMETERS.append(IDBC_SERIES_PARAMETERS1)

          
          if SERIES_KEY1.find("parameter:latlng.") > 0:
              influxdb_gpskeys.append(SERIES_KEY1)
          else:
              influxdb_keys.append(SERIES_KEY1)
              influxdb_cloud_keys.append(SERIES_KEY1)

              
          series_elements = series_elements + 1


    except TypeError as e:
        if debug_all: log.info('getinfluxseriesmultibydeviceid: TypeError in in geting series_1 parameters %s:  ', SERIES_KEY1)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getinfluxseriesmultibydeviceid: TypeError in in geting series_1 parameters %s:  ' % str(e))

        
    except KeyError as e:
        if debug_all: log.info('getinfluxseriesmultibydeviceid: KeyError in in geting series_1 parameters %s:  ', SERIES_KEY1)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getinfluxseriesmultibydeviceid: KeyError in in geting series_1 parameters %s:  ' % str(e))
        
    except ValueError as e:
        if debug_all: log.info('getinfluxseriesmultibydeviceid: ValueError in in geting series_1 parameters %s:  ', SERIES_KEY1)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getinfluxseriesmultibydeviceid: ValueError in in geting series_1 parameters %s:  ' % str(e))
    
    except NameError as e:
        if debug_all: log.info('getinfluxseriesmultibydeviceid: NameError in in geting series_1 parameters %s:  ', SERIES_KEY1)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getinfluxseriesmultibydeviceid: NameError in in geting series_1 parameters %s:  ' % str(e))

    except IndexError as e:
        if debug_all: log.info('getinfluxseriesmultibydeviceid: IndexError in in geting series_1 parameters %s:  ', SERIES_KEY1)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getinfluxseriesmultibydeviceid: IndexError in in geting series_1 parameters %s:  ' % str(e))                
   
    except:
        e = sys.exc_info()[0]
        if debug_all: log.info('getinfluxseriesmultibydeviceid: Error in geting series_1 parameters %s:  ' % e)
        pass
            
    try:
        SERIES_KEY2= request.args.get('serieskey2', '')
        


        if SERIES_KEY2 != str(0):

          SERIES_KEYS.append(SERIES_KEY2)
          
          if SERIES_KEY2 != "":
            if SERIES_KEY2.find(".*.") > 0:  
              seriesname = SERIES_KEY2.replace(".*.","*.")
            else:
              seriesname = SERIES_KEY2
              
            seriestags = seriesname.split(".")

            serieslable = seriestags[0].split(":")
            Device_ID_Key[2] = serieslable[1]
            
            serieslable = seriestags[1].split(":")
            Sensor_Key[2]= serieslable[1]
            
            serieslable = seriestags[2].split(":")
            Source_Key[2]= serieslable[1]
            
            serieslable = seriestags[3].split(":")
            Instance_Key[2]= serieslable[1]
            
            serieslable = seriestags[4].split(":")
            Type_Key[2]= serieslable[1]

            serieslable = seriestags[5].split(":")
            Parameter_Key[2]= serieslable[1]        
            
            UNITS_KEY2 = request.args.get('unitskey2', 255)         
            Rollup_Key[2] = alerttype


          
          IDBC_SERIES_KEY2 = convertInfluxDBCloudKeys(SERIES_KEY2)
          IDBC_KEYS.append(IDBC_SERIES_KEY2)            

          IDBC_SERIES_PARAMETERS2 = convertInfluxDBCloudParameters(SERIES_KEY2,  "value2", alerttype)
          IDBC_PARAMETERS.append(IDBC_SERIES_PARAMETERS2)

          


          if SERIES_KEY2.find("parameter:latlng.") > 0:
              influxdb_gpskeys.append(SERIES_KEY2)
          else:
              influxdb_keys.append(SERIES_KEY2)
              influxdb_cloud_keys.append(SERIES_KEY2)

              
          series_elements = series_elements + 1


    except TypeError as e:
        if debug_all: log.info('getinfluxseriesmultibydeviceid: TypeError in in geting series_2 parameters %s:  ', SERIES_KEY2)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getinfluxseriesmultibydeviceid: TypeError in in geting series_2 parameters %s:  ' % str(e))

        
    except KeyError as e:
        if debug_all: log.info('getinfluxseriesmultibydeviceid: KeyError in in geting series_2 parameters %s:  ', SERIES_KEY2)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getinfluxseriesmultibydeviceid: KeyError in in geting series_2 parameters %s:  ' % str(e))

    
    except NameError as e:
        if debug_all: log.info('getinfluxseriesmultibydeviceid: NameError in in geting series_2 parameters %s:  ', SERIES_KEY2)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getinfluxseriesmultibydeviceid: NameError in in geting series_2 parameters %s:  ' % str(e))

    except IndexError as e:
        if debug_all: log.info('getinfluxseriesmultibydeviceid: IndexError in in geting series_2 parameters %s:  ', SERIES_KEY2)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getinfluxseriesmultibydeviceid: IndexError in in geting series_2 parameters %s:  ' % str(e))                
   
        
    except:
        e = sys.exc_info()[0]
        if debug_all: log.info('Telemetrypost: Error in geting series_2 parameters %s:  ' % e)
        pass
    
    try:
        SERIES_KEY3= request.args.get('serieskey3', '')
        

        if SERIES_KEY3 != str(0):

          SERIES_KEYS.append(SERIES_KEY3)
          
          if SERIES_KEY3 != "":
            if SERIES_KEY3.find(".*.") > 0:  
              seriesname = SERIES_KEY3.replace(".*.","*.")
            else:
              seriesname = SERIES_KEY3
              
            seriestags = seriesname.split(".")

            serieslable = seriestags[0].split(":")
            Device_ID_Key[3] = serieslable[1]
            
            serieslable = seriestags[1].split(":")
            Sensor_Key[3]= serieslable[1]
            
            serieslable = seriestags[2].split(":")
            Source_Key[3]= serieslable[1]
            
            serieslable = seriestags[3].split(":")
            Instance_Key[3]= serieslable[1]
            
            serieslable = seriestags[4].split(":")
            Type_Key[3]= serieslable[1]

            serieslable = seriestags[5].split(":")
            Parameter_Key[3]= serieslable[1]        
            
            UNITS_KEY3 = request.args.get('unitskey3', 255)        
            Rollup_Key[3] = alerttype


         
          IDBC_SERIES_KEY3 = convertInfluxDBCloudKeys(SERIES_KEY3)
          IDBC_KEYS.append(IDBC_SERIES_KEY3)            

          IDBC_SERIES_PARAMETERS3 = convertInfluxDBCloudParameters(SERIES_KEY3, "value3", alerttype)
          IDBC_PARAMETERS.append(IDBC_SERIES_PARAMETERS3)

          


          if SERIES_KEY3.find("parameter:latlng.") > 0:
              influxdb_gpskeys.append(SERIES_KEY3)
          else:
              influxdb_keys.append(SERIES_KEY3)
              influxdb_cloud_keys.append(SERIES_KEY3)

            
        series_elements = series_elements + 1
    except TypeError as e:
        if debug_all: log.info('getinfluxseriesmultibydeviceid: TypeError in in geting series_3 parameters %s:  ', SERIES_KEY3)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getinfluxseriesmultibydeviceid: TypeError in in geting series_3 parameters %s:  ' % str(e))

        
    except KeyError as e:
        if debug_all: log.info('getinfluxseriesmultibydeviceid: KeyError in in geting series_3 parameters %s:  ', SERIES_KEY3)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getinfluxseriesmultibydeviceid: KeyError in in geting series_3 parameters %s:  ' % str(e))

    
    except NameError as e:
        if debug_all: log.info('getinfluxseriesmultibydeviceid: NameError in in geting series_3 parameters %s:  ', SERIES_KEY3)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getinfluxseriesmultibydeviceid: NameError in in geting series_3 parameters %s:  ' % str(e))

    except IndexError as e:
        if debug_all: log.info('getinfluxseriesmultibydeviceid: IndexError in in geting series_3 parameters %s:  ', SERIES_KEY3)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getinfluxseriesmultibydeviceid: IndexError in in geting series_3 parameters %s:  ' % str(e))                
   
    except:
        e = sys.exc_info()[0]
        if debug_all: log.info('getinfluxseriesmultibydeviceid: Error in geting series_3 parameters %s:  ' % e)
        pass
        
    
    try:
        SERIES_KEY4= request.args.get('serieskey4', '')
         

        if SERIES_KEY4 != str(0):

       
          SERIES_KEYS.append(SERIES_KEY4)


          if SERIES_KEY4 != "":
            if SERIES_KEY4.find(".*.") > 0:  
              seriesname = SERIES_KEY4.replace(".*.","*.")
            else:
              seriesname = SERIES_KEY4
              
            seriestags = seriesname.split(".")

            serieslable = seriestags[0].split(":")
            Device_ID_Key[4] = serieslable[1]
            
            serieslable = seriestags[1].split(":")
            Sensor_Key[4]= serieslable[1]
            
            serieslable = seriestags[2].split(":")
            Source_Key[4]= serieslable[1]
            
            serieslable = seriestags[3].split(":")
            Instance_Key[4]= serieslable[1]
            
            serieslable = seriestags[4].split(":")
            Type_Key[4]= serieslable[1]

            serieslable = seriestags[5].split(":")
            Parameter_Key[4]= serieslable[1]        
            
            UNITS_KEY4 = request.args.get('unitskey4', 255)
            Rollup_Key[4] = alerttype


            
          IDBC_SERIES_KEY4 = convertInfluxDBCloudKeys(SERIES_KEY4)
          IDBC_KEYS.append(IDBC_SERIES_KEY4)            


          IDBC_SERIES_PARAMETERS4 = convertInfluxDBCloudParameters(SERIES_KEY4, "value4", alerttype)
          IDBC_PARAMETERS.append(IDBC_SERIES_PARAMETERS4)

          
          
          if SERIES_KEY4.find("parameter:latlng.") > 0:
              influxdb_gpskeys.append(SERIES_KEY4)
          else:
              influxdb_keys.append(SERIES_KEY4)
              influxdb_cloud_keys.append(SERIES_KEY4)

              
          series_elements = series_elements + 1
          
    except:
        e = sys.exc_info()[0]
        if debug_all: log.info('getinfluxseriesmultibydeviceid: Error in geting series_4 parameters %s:  ' % e)
        pass
    
    try:
        SERIES_KEY5= request.args.get('serieskey5', '')
        

        if SERIES_KEY5 != str(0):

        
          SERIES_KEYS.append(SERIES_KEY5)

          if SERIES_KEY5 != "":
            if SERIES_KEY5.find(".*.") > 0:  
              seriesname = SERIES_KEY5.replace(".*.","*.")
            else:
              seriesname = SERIES_KEY5
              
            seriestags = seriesname.split(".")

            serieslable = seriestags[0].split(":")
            Device_ID_Key[5] = serieslable[1]
            
            serieslable = seriestags[1].split(":")
            Sensor_Key[5]= serieslable[1]
            
            serieslable = seriestags[2].split(":")
            Source_Key[5]= serieslable[1]
            
            serieslable = seriestags[3].split(":")
            Instance_Key[5]= serieslable[1]
            
            serieslable = seriestags[4].split(":")
            Type_Key[5]= serieslable[1]

            serieslable = seriestags[5].split(":")
            Parameter_Key[5]= serieslable[1]        
            
            UNITS_KEY5 = request.args.get('unitskey5', 255)
            Rollup_Key[5] = alerttype


            
          IDBC_SERIES_KEY5 = convertInfluxDBCloudKeys(SERIES_KEY5)
          IDBC_KEYS.append(IDBC_SERIES_KEY5)            

          IDBC_SERIES_PARAMETERS5 = convertInfluxDBCloudParameters(SERIES_KEY5, "value5", alerttype)
          IDBC_PARAMETERS.append(IDBC_SERIES_PARAMETERS5)

          

          
          if SERIES_KEY5.find("parameter:latlng.") > 0:
              influxdb_gpskeys.append(SERIES_KEY5)
          else:
              influxdb_keys.append(SERIES_KEY5)
              influxdb_cloud_keys.append(SERIES_KEY5)

              
          series_elements = series_elements + 1
    except:
        e = sys.exc_info()[0]
        if debug_all: log.info('getinfluxseriesmultibydeviceid: Error in geting series_5 parameters %s:  ' % e)
        pass
    
    try:
        SERIES_KEY6= request.args.get('serieskey6', '')
         

        if SERIES_KEY6 != str(0):

       
          SERIES_KEYS.append(SERIES_KEY6)


          if SERIES_KEY6 != "":
            if SERIES_KEY6.find(".*.") > 0:  
              seriesname = SERIES_KEY6.replace(".*.","*.")
            else:
              seriesname = SERIES_KEY6
              
            seriestags = seriesname.split(".")

            serieslable = seriestags[0].split(":")
            Device_ID_Key[6] = serieslable[1]
            
            serieslable = seriestags[1].split(":")
            Sensor_Key[6]= serieslable[1]
            
            serieslable = seriestags[2].split(":")
            Source_Key[6]= serieslable[1]
            
            serieslable = seriestags[3].split(":")
            Instance_Key[6]= serieslable[1]
            
            serieslable = seriestags[4].split(":")
            Type_Key[6]= serieslable[1]

            serieslable = seriestags[5].split(":")
            Parameter_Key[6]= serieslable[1]        
            
            UNITS_KEY6 = request.args.get('unitskey6', 255)          
            Rollup_Key[6] = alerttype

        
          IDBC_SERIES_KEY6 = convertInfluxDBCloudKeys(SERIES_KEY6)
          IDBC_KEYS.append(IDBC_SERIES_KEY6)            

          IDBC_SERIES_PARAMETERS6 = convertInfluxDBCloudParameters(SERIES_KEY6, "value6", alerttype)
          IDBC_PARAMETERS.append(IDBC_SERIES_PARAMETERS6)

          

          
          if SERIES_KEY6.find("parameter:latlng.") > 0:
              influxdb_gpskeys.append(SERIES_KEY6)
          else:
              influxdb_keys.append(SERIES_KEY6)
              influxdb_cloud_keys.append(SERIES_KEY6)

              

          series_elements = series_elements + 1
    except:
        e = sys.exc_info()[0]
        if debug_all: log.info('getinfluxseriesmultibydeviceid: Error in geting series_6 parameters %s:  ' % e)
        pass

    
    try:
        SERIES_KEY7= request.args.get('serieskey7', '')
        

        if SERIES_KEY7 != str(0):

        
          SERIES_KEYS.append(SERIES_KEY7)


          if SERIES_KEY7 != "":
            if SERIES_KEY7.find(".*.") > 0:  
              seriesname = SERIES_KEY7.replace(".*.","*.")
            else:
              seriesname = SERIES_KEY7
              
            seriestags = seriesname.split(".")

            serieslable = seriestags[0].split(":")
            Device_ID_Key[7] = serieslable[1]
            
            serieslable = seriestags[1].split(":")
            Sensor_Key[7]= serieslable[1]
            
            serieslable = seriestags[2].split(":")
            Source_Key[7]= serieslable[1]
            
            serieslable = seriestags[3].split(":")
            Instance_Key[7]= serieslable[1]
            
            serieslable = seriestags[4].split(":")
            Type_Key[7]= serieslable[1]

            serieslable = seriestags[5].split(":")
            Parameter_Key[7]= serieslable[1]        
            
            UNITS_KEY7 = request.args.get('unitskey7', 255)
            Rollup_Key[7] = alerttype


            
          IDBC_SERIES_KEY7 = convertInfluxDBCloudKeys(SERIES_KEY7)
          IDBC_KEYS.append(IDBC_SERIES_KEY7)            


          IDBC_SERIES_PARAMETERS7 = convertInfluxDBCloudParameters(SERIES_KEY7, "value7", alerttype)
          IDBC_PARAMETERS.append(IDBC_SERIES_PARAMETERS7)

          
          
          if SERIES_KEY7.find("parameter:latlng.") > 0:
              influxdb_gpskeys.append(SERIES_KEY7)
          else:
              influxdb_keys.append(SERIES_KEY7)
              influxdb_cloud_keys.append(SERIES_KEY7)

              

          series_elements = series_elements + 1
    except:
        e = sys.exc_info()[0]
        if debug_all: log.info('getinfluxseriesmultibydeviceid: Error in geting series_7 parameters %s:  ' % e)
        pass

    
    try:
        SERIES_KEY8= request.args.get('serieskey8', '')
        

        if SERIES_KEY8 != str(0):

        
          SERIES_KEYS.append(SERIES_KEY8)

          if SERIES_KEY8 != "":
            if SERIES_KEY8.find(".*.") > 0:  
              seriesname = SERIES_KEY8.replace(".*.","*.")
            else:
              seriesname = SERIES_KEY8
              
            seriestags = seriesname.split(".")

            serieslable = seriestags[0].split(":")
            Device_ID_Key[8] = serieslable[1]
            
            serieslable = seriestags[1].split(":")
            Sensor_Key[8]= serieslable[1]
            
            serieslable = seriestags[2].split(":")
            Source_Key[8]= serieslable[1]
            
            serieslable = seriestags[3].split(":")
            Instance_Key[8]= serieslable[1]
            
            serieslable = seriestags[4].split(":")
            Type_Key[8]= serieslable[1]

            serieslable = seriestags[5].split(":")
            Parameter_Key[8]= serieslable[1]        
            
            UNITS_KEY8 = request.args.get('unitskey8', 255)
            Rollup_Key[8] = alerttype


            
          IDBC_SERIES_KEY8 = convertInfluxDBCloudKeys(SERIES_KEY8)
          IDBC_KEYS.append(IDBC_SERIES_KEY8)            


          IDBC_SERIES_PARAMETERS8 = convertInfluxDBCloudParameters(SERIES_KEY8, "value8", alerttype)
          IDBC_PARAMETERS.append(IDBC_SERIES_PARAMETERS8)

          
          
          if SERIES_KEY8.find("parameter:latlng.") > 0:
              influxdb_gpskeys.append(SERIES_KEY8)
          else:
              influxdb_keys.append(SERIES_KEY8)
              influxdb_cloud_keys.append(SERIES_KEY8)

              

          series_elements = series_elements + 1
    except:
        e = sys.exc_info()[0]
        if debug_all: log.info('getinfluxseriesmultibydeviceid: Error in geting series_8 parameters %s:  ' % e)
        pass

    
    
    #print 'Series elements:', series_elements
    #if debug_all: log.info('Telemetrypost: influxdb_keys %s:  ', influxdb_keys)

  except:
      if debug_all: log.info('getinfluxseriesmultibydeviceid: Error in geting series parameters %s:  ', posttype)
      e = sys.exc_info()[0]

      if debug_all: log.info("Error: %s" % e)

      return jsonify( message='Error in geting series parameters', status='error')

  if debug_all: log.info('getinfluxseriesmultibydeviceid: Processed series parameters %s:  ', series_elements)


  if debug_all: log.info('getinfluxseriesmultibydeviceid: influxdb_GPSkeys %s:  ', influxdb_gpskeys)
  if debug_all: log.info('getinfluxseriesmultibydeviceid: influxdb_keys %s:  ', influxdb_keys)
  if debug_all: log.info('getinfluxseriesmultibydeviceid: influxdb_cloud_keys %s:  ', IDBC_KEYS)
  if debug_all: log.info('getinfluxseriesmultibydeviceid: influxdb_cloud_parameters %s:  ', IDBC_PARAMETERS)

  
  if IDBC_KEYS != []:
        
        if SERIES_KEY1 != "":
            seriesname = SERIES_KEY1
            seriestags = seriesname.split(".")

            seriesdeviceidtag = seriestags[0]
            seriesdeviceid = seriesdeviceidtag.split(":")
            measurement = "HS_" + seriesdeviceid[1]
        else:
            measurement = "HelmSmart"
            
        log.info('getinfluxseriesmultibydeviceid:: Influx Cloud measurement String %s:  ', measurement)
        
        idbcserieskeys = ' OR '.join(IDBC_KEYS)
        if debug_all: log.info('Telemetrypost: idbcserieskeys string %s:  ', idbcserieskeys)
        
        idbcseriesparameters = ' , '.join(IDBC_PARAMETERS)
        if debug_all: log.info('Telemetrypost: idbcseriesparameters string %s:  ', idbcseriesparameters)

        dbcquery = ('select {} FROM {} '
                         'where {} AND time > {}s and time < {}s '
                         'group by *, time({}s)') \
                    .format( idbcseriesparameters,  measurement, idbcserieskeys,
                            startepoch, endepoch,
                            resolution)
            
        log.info('getinfluxseriesmultibydeviceid:: Influx Cloud Query String %s:  ', dbcquery)

  else:
    return jsonify( message='getinfluxseriesmultibydeviceid: Empty keys', status='error')
  
  try:
    jsondata=[]
    jsonkey=[]
    dbcresult = None
    #"""                
    dbcresult = dbc.query(dbcquery)
    #dbresults.append(dbresult)
    #if debug_all: log.info('getinfluxseriesmultibydeviceid: InfluxDB-Cloud query result %s:  ', dbcresult)
    #log.info('getinfluxseriesmultibydeviceid: InfluxDB-Cloud query result %s:  ', dbcresult)

    keys = dbcresult.raw.get('series',[])
    #log.info("getinfluxseriesmultibydeviceid Get InfluxDB series keys %s", keys)

  except InfluxDBClientError as e:
    log.info('getinfluxseriesmultibydeviceid: inFlux error in InfluxDB query %s:  ' % str(e))

  except TypeError as e:
      if debug_all: log.info('getinfluxseriesmultibydeviceid: TypeError in in geting inFluxDB data %s:  ', dbcquery)
      #e = sys.exc_info()[0]

      if debug_all: log.info('getinfluxseriesmultibydeviceid: TypeError in in geting inFluxDB data %s:  ' % str(e))

      
  except KeyError as e:
      if debug_all: log.info('getinfluxseriesmultibydeviceid: KeyError in in geting inFluxDB data %s:  ', dbcquery)
      #e = sys.exc_info()[0]

      if debug_all: log.info('getinfluxseriesmultibydeviceid: KeyError in in geting inFluxDB data %s:  ' % str(e))
      
  except ValueError as e:
      if debug_all: log.info('getinfluxseriesmultibydeviceid: ValueError in in geting inFluxDB data %s:  ', dbcquery)
      #e = sys.exc_info()[0]

      if debug_all: log.info('getinfluxseriesmultibydeviceid: ValueError in in geting inFluxDB data %s:  ' % str(e))
  
  except NameError as e:
      if debug_all: log.info('getinfluxseriesmultibydeviceid: NameError in in geting inFluxDB data %s:  ', dbcquery)
      #e = sys.exc_info()[0]

      if debug_all: log.info('getinfluxseriesmultibydeviceid: NameError in in geting inFluxDB data %s:  ' % str(e))

  except IndexError as e:
      if debug_all: log.info('getinfluxseriesmultibydeviceid: IndexError in in geting inFluxDB data %s:  ', dbcquery)
      #e = sys.exc_info()[0]

      if debug_all: log.info('getinfluxseriesmultibydeviceid: IndexError in in geting inFluxDB data %s:  ' % str(e))                
 
    
  except:
    #log.info('Telemetrypost: Error in geting Telemetry parameters %s:  ', posttype)
    e = sys.exc_info()[0]
    log.info('inFluxDB: Error in geting inFluxDB data %s:  ' % e)
    
    return jsonify( message='Error in inFluxDB query 2', status='error')

  if not dbcresult:
    #print 'inFluxDB Exception1:', response.response.successful, response.response.reason 
    return jsonify( message='No response to return 1' , status='error')

  #return jsonify(result=dbcresult)

  # return csv formated data
  if dataformat == 'csv' or dataformat == 'json':
    #def generate():
    # create header row

    # create header row
    #yield strvalue + 'time, value1, value2, value3, value4 \r\n'
    #strvalue = strvalue + 'time, value1, value2, value3, value4 \r\n'
    
    #strnames = 'timestamp, ' + serieskeys +  ' \r\n'

    points = list(dbcresult.get_points())
    points = sorted(points,key=itemgetter('time'))

    #log.info('getinfluxseriesmultibydeviceid:  InfluxDB-Cloud points%s:', points)
    # get returned values and epoch times and add to a list
    #Sorting and grouping only works on lists and not json key pairs
    for point in points:
      #log.info('getinfluxseriesmultibydeviceid:  InfluxDB-Cloud point%s:', point)
      
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'
      value5 = '---'
      value6 = '---'
      value7 = '---'
      value8 = '---'

      try:
        
        if point['time'] is not None:
          mydatetimestr = str(point['time'])
          mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')
          dtt = mydatetime.timetuple()
          ts = int(mktime(dtt)*1000)

        if point['value1'] is not None:
          #log.info('getinfluxseriesmultibydeviceid:  InfluxDB-Cloud point value1_1 %s units %s:', point['value1'], UNITS_KEY1)
          value1 = convertunits( point['value1'], UNITS_KEY1)
          #log.info('getinfluxseriesmultibydeviceid:  InfluxDB-Cloud point value1_2 %s:', value1)
          # add to list if we mave a match to the key pair
          jsondata.append((ts, 'value1',value1 ))

        if point['value2'] is not None:
          value2 = convertunits( point['value2'], UNITS_KEY2)
          # add to list if we mave a match to the key pair
          jsondata.append((ts, 'value2',value2 ))

           
        if point['value3'] is not None:
          value3 = convertunits( point['value3'], UNITS_KEY3)
          # add to list if we mave a match to the key pair
          jsondata.append((ts, 'value3',value3 ))
           
        if point['value4'] is not None:
          value4 = convertunits( point['value4'], UNITS_KEY4)
          # add to list if we mave a match to the key pair
          jsondata.append((ts, 'value4',value4 ))

           
        if point['value5'] is not None:
          value5 = convertunits( point['value5'], UNITS_KEY5)
          # add to list if we mave a match to the key pair
          jsondata.append((ts, 'value5',value5 ))

           
        if point['value6'] is not None:
          value6 = convertunits( point['value6'], UNITS_KEY6)
          # add to list if we mave a match to the key pair
          jsondata.append((ts, 'value6',value6 ))

           
        if point['value7'] is not None:
          value7 = convertunits( point['value7'], UNITS_KEY7)
          # add to list if we mave a match to the key pair
          jsondata.append((ts, 'value7',value7 ))

           
        if point['value8'] is not None:
          value8 = convertunits( point['value8'], UNITS_KEY8)
          # add to list if we mave a match to the key pair
          jsondata.append((ts, 'value8',value8 ))


      except:
        #if debug_all: log.info('getinfluxseriesmultibydeviceid: IndexError in in geting inFluxDB point %s:  ', point)
        #log.info('inFluxDB: Error in geting inFluxDB data points%s:  ' % e)
        e = sys.exc_info()[0]
        pass
        #log.info('getinfluxseriesmultibydeviceid:  InfluxDB-Cloud point:')


    #jsondata = sorted(jsondata,key=itemgetter('epoch'))
    # sort list based on epoch time integer x[0] which is first element in list
    jsondata = sorted(jsondata, key=lambda x: x[0])
    log.info('getinfluxseriesmultibydeviceid:  InfluxDB-Cloud point%s:', jsondata)
    jsondataarray = []
    groups = []
    strvalues = ""
    strnames = ""
    
    try:          
      # group  values based on epoch times and get rid of repeated epoch times
      for key, valuesgroup in groupby(jsondata, lambda x: x[0]):

        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'
        value5 = '---'
        value6 = '---'
        value7 = '---'
        value8 = '---'

        #groups.append(list(valuesgroup))
        #log.info('getinfluxseriesmultibydeviceid:  InfluxDB-Cloud valuesgroup %s:', list(valuesgroup))
        #log.info('getinfluxseriesmultibydeviceid:  InfluxDB-Cloud key %s:', key)

        #go through the groups and find elements that match the key pairs labels and assign to values
        for csv_values in valuesgroup:       
          log.info('getinfluxseriesmultibydeviceid:  InfluxDB-Cloud csv_values %s:', csv_values)
          log.info('getinfluxseriesmultibydeviceid:  InfluxDB-Cloud csv_values[1] %s,  csv_values[2] %s:', csv_values[1], csv_values[2])

          if csv_values[1] == "value1":
            value1 = csv_values[2]

          elif csv_values[1] == "value2":
            value2 = csv_values[2]

          elif csv_values[1] == "value3":
            value3 = csv_values[2]


          elif csv_values[1] == "value4":
            value4 = csv_values[2]


          elif csv_values[1] == "value5":
            value5 = csv_values[2]


          elif csv_values[1] == "value6":
            value6 = csv_values[2]


          elif csv_values[1] == "value7":
            value7 = csv_values[2]


          elif csv_values[1] == "value8":
            value8 = csv_values[2]

        mytime = datetime.datetime.fromtimestamp(float(key/1000)).strftime('%Y-%m-%d, %H:%M:%SZ')
        
        log.info('getinfluxseriesmultibydeviceid:  InfluxDB-Cloud csv_values value1 %s:value2 %s:value3 %s:value4 %s', value1,value2,value3,value4)
                #creeat a CSV row string
        strvalues=  strvalues + str(key) + ", " + str(mytime) + ", " + str(value1)+ ", " +str(value2)+ ", " +str(value3)+ ", " +str(value4)+ ", " +str(value5)+ ", " +str(value6)+ ", " +str(value7)+ ", " +str(value8) +   '\r\n'
        log.info('getinfluxseriesmultibydeviceid:  InfluxDB-Cloud strvalues %s:', strvalues)
          #log.info('getinfluxseriesmultibydeviceid:  InfluxDB-Cloud valuesgroup %s:', csv_values[3])
          #log.info('getinfluxseriesmultibydeviceid:  InfluxDB-Cloud valuesgroup %s:', csv_values[4])
         

        #  log.info('getinfluxseriesmultibydeviceid:  InfluxDB-Cloud csv_values%s:', csv_values[0])
        #  #jsondataarray.append({'epoch':mydatetimestr, 'value1':value1,'value2':value2,'value3':value3,'value4':value4,'value5':value5,'value6':value6,'value7':value7,'value8':value8})
        
        # convert epoch time integer to date/time string
        #mytime = datetime.datetime.fromtimestamp(float(key/1000)).strftime('%Y-%m-%d %H:%M:%SZ')



      
        #create ajson row too
        jsondataarray.append({'epoch':key, 'value1':value1,'value2':value2,'value3':value3,'value4':value4,'value5':value5,'value6':value6,'value7':value7,'value8':value8})          
      
      log.info('getinfluxseriesmultibydeviceid:  InfluxDB-Cloud jsondataarray%s:', jsondataarray)          


    except TypeError as e:
        if debug_all: log.info('getinfluxseriesmultibydeviceid: TypeError in in geting inFluxDB data %s:  ', jsondata)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getinfluxseriesmultibydeviceid: TypeError in in geting inFluxDB data %s:  ' % str(e))

        
    except KeyError as e:
        if debug_all: log.info('getinfluxseriesmultibydeviceid: KeyError in in geting inFluxDB data %s:  ', jsondata)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getinfluxseriesmultibydeviceid: KeyError in in geting inFluxDB data %s:  ' % str(e))
        
    except ValueError as e:
        if debug_all: log.info('getinfluxseriesmultibydeviceid: ValueError in in geting inFluxDB data %s:  ', jsondata)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getinfluxseriesmultibydeviceid: ValueError in in geting inFluxDB data %s:  ' % str(e))
    
    except NameError as e:
        if debug_all: log.info('getinfluxseriesmultibydeviceid: NameError in in geting inFluxDB data %s:  ', jsondata)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getinfluxseriesmultibydeviceid: NameError in in geting inFluxDB data %s:  ' % str(e))

    except IndexError as e:
        if debug_all: log.info('getinfluxseriesmultibydeviceid: IndexError in in geting inFluxDB data %s:  ', jsondata)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getinfluxseriesmultibydeviceid: IndexError in in geting inFluxDB data %s:  ' % str(e))                
   
      
    except:
      #log.info('Telemetrypost: Error in geting Telemetry parameters %s:  ', posttype)
      e = sys.exc_info()[0]
      log.info('inFluxDB: Error in geting inFluxDB data %s:  ' % e)




  # return csv formated data
  if dataformat == 'csv':
    strnames = strnames + " Device_ID,,," + str(Device_ID_Key[1]) + ","  + str(Device_ID_Key[2]) + "," + str(Device_ID_Key[3]) + "," + str(Device_ID_Key[4]) + "," + str(Device_ID_Key[5]) + "," + str(Device_ID_Key[6]) + "," + str(Device_ID_Key[7]) + "," + str(Device_ID_Key[8]) +  '\r\n'
    strnames = strnames + " Sensor,,," + str(Sensor_Key[1]) + ","  + str(Sensor_Key[2]) + "," + str(Sensor_Key[3]) + "," + str(Sensor_Key[4]) + "," + str(Sensor_Key[5]) + "," + str(Sensor_Key[6]) + "," + str(Sensor_Key[7]) + "," + str(Sensor_Key[8]) +  '\r\n'
    strnames = strnames + " Source,,," + str(Source_Key[1]) + ","  + str(Source_Key[2]) + "," + str(Source_Key[3]) + "," + str(Source_Key[4]) + "," + str(Source_Key[5]) + "," + str(Source_Key[6]) + "," + str(Source_Key[7]) + "," + str(Source_Key[8]) +  '\r\n'
    strnames = strnames + " Instance,,," + str(Instance_Key[1]) + ","  + str(Instance_Key[2]) + "," + str(Instance_Key[3]) + "," + str(Instance_Key[4]) + "," + str(Instance_Key[5]) + "," + str(Instance_Key[6]) + "," + str(Instance_Key[7]) + "," + str(Instance_Key[8]) +  '\r\n'
    strnames = strnames + " Type,,," + str(Type_Key[1]) + ","  + str(Type_Key[2]) + "," + str(Type_Key[3]) + "," + str(Type_Key[4]) + "," + str(Type_Key[5]) + "," + str(Type_Key[6]) + "," + str(Type_Key[7]) + "," + str(Type_Key[8]) +  '\r\n'
    strnames = strnames + " Parameter,,," + str(Parameter_Key[1]) + ","  + str(Parameter_Key[2]) + "," + str(Parameter_Key[3]) + "," + str(Parameter_Key[4]) + "," + str(Parameter_Key[5]) + "," + str(Parameter_Key[6]) + "," + str(Parameter_Key[7]) + "," + str(Parameter_Key[8]) +  '\r\n'
    strnames = strnames + " Rollup,,," + str(Rollup_Key[1]) + ","  + str(Rollup_Key[2]) + "," + str(Rollup_Key[3]) + "," + str(Rollup_Key[4]) + "," + str(Rollup_Key[5]) + "," + str(Rollup_Key[6]) + "," + str(Rollup_Key[7]) + "," + str(Rollup_Key[8]) +  '\r\n'

    #strnames = strnames + " Epoch, Date ," + str(get_unit_label(UNITS_KEY1)) + ","  + str(get_unit_label(UNITS_KEY2)) + "," + str(get_unit_label(UNITS_KEY3)) + "," + str(get_unit_label(UNITS_KEY4)) + "," + str(get_unit_label(UNITS_KEY5))+ "," + str(get_unit_label(UNITS_KEY6)) + "," + str(get_unit_label(UNITS_KEY7)) + "," + str(get_unit_label(UNITS_KEY8)) +  '\r\n'
    strnames = strnames + " Epoch, Date, Time ," + str(get_unit_label(UNITS_KEY1)) + ","  + str(get_unit_label(UNITS_KEY2)) + "," + str(get_unit_label(UNITS_KEY3)) + "," + str(get_unit_label(UNITS_KEY4)) + "," + str(get_unit_label(UNITS_KEY5))+ "," + str(get_unit_label(UNITS_KEY6)) + "," + str(get_unit_label(UNITS_KEY7)) + "," + str(get_unit_label(UNITS_KEY8)) +  '\r\n'

    #strnames = strnames + "Epoch, Date ,Series_1 ,Series_2 ,Series_3 ,Series_4 ,Series_5 ,Series_6 ,Series_7 ,Series_8 " +   '\r\n'
  

    response = make_response(strnames + strvalues)
    #response = make_response(json.dumps(outputcsv))
    #response = make_response(json.dumps(outputjson))
    response.headers['Content-Type'] = 'text/csv'
    response.headers["Content-Disposition"] = "attachment; filename=HelmSmart.csv"
    return response

  # return json formated data
  if dataformat == 'json':
    return jsonify( data=jsondataarray , status="OK")

  else:
    return jsonify( data="format specification error" , status="ERROR")
  
  
### dashboard functions ####

  
@app.route('/freeboard_savedashboardjson' , methods=['POST'])
@cross_origin()
def freeboard_savedashboardjson():
    conn = db_pool.getconn()
  
    prefuid = request.args.get('prefuid',1)
    log.info('freeboard_savedashboardjson: prefuid  %s:  ', prefuid)

  
    mymessage = request.data
    #mymessage = request.args.get('data')
    #mymessage = json.loads(request.data)
    #mymessage = json.dumps(request.data)
    #response = requests.post(url, headers=header, json=data)
    #log.info('freeboard_savedashboardjson: data  %s:  ', mymessage)
    
    #mymessage  = request.get_json()

    #log.info('freeboard_savedashboardjson: json   %s:  ', mymessage)
    #log.info('freeboard_savedashboardjson: json   %s:  ', mymessage.decode("utf-8"))

    #mymessage = '{"version": 1,"allow_edit": true}'

    try:
        cursor = conn.cursor()
        sqlstr = " update dashboard_prefs SET jsondata =%s where  prefuid = %s;" 
        cursor.execute(sqlstr, (mymessage.decode("utf-8"), prefuid, ))   
        conn.commit()

        return jsonify(result="OK")  

    except psycopg.ProgrammingError as e:
        log.info('freeboard_savedashboardjson: ProgrammingError in  update pref %s:  ', prefuid)
        log.info('freeboard_savedashboardjson: ProgrammingError in  update pref  %s:  ' % str(e))
        return jsonify(result="ProgrammingError error")

    except psycopg.DataError as e:
        log.info('freeboard_savedashboardjson: DataError in  update pref %s:  ', prefuid)
        log.info('freeboard_savedashboardjson: DataError in  update pref  %s:  ' % str(e))
        return jsonify(result="DataError error")

    except TypeError as e:
        log.info('freeboard_savedashboardjson: TypeError in  update pref %s:  ', prefuid)
        log.info('freeboard_savedashboardjson: TypeError in  update pref  %s:  ' % str(e))

    except ValueError as e:
        log.info('freeboard_savedashboardjson: ValueError in  update pref  %s:  ', prefuid)
        log.info('freeboard_savedashboardjson: ValueError in  update pref %s:  ' % str(e))

    except KeyError as e:
        log.info('freeboard_savedashboardjson: KeyError in  update pref  %s:  ', prefuid)
        log.info('freeboard_savedashboardjson: KeyError in  update pref  %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard_savedashboardjson: NameError in  update pref  %s:  ', prefuid)
        log.info('freeboard_savedashboardjson: NameError in  update pref %s:  ' % str(e))
        
    except IndexError as e:
        log.info('freeboard_savedashboardjson: IndexError in  update pref  %s:  ', prefuid)
        log.info('freeboard_savedashboardjson: IndexError in  update pref  %s:  ' % str(e))  


    except:
        e = sys.exc_info()[0]
        log.info('freeboard_savedashboardjson: Error in update pref  %s:  ' % str(e))
        return jsonify(result="error") 


    finally:
        db_pool.putconn(conn)

@app.route('/freeboard_deletedashboard')
@cross_origin()
def freeboard_deletedashboard():
  conn = db_pool.getconn()
  

  prefuid = request.args.get('prefuid',1)



  log.info('freeboard_deletedashboard: prefuid  %s:  ', prefuid)
  


  try:
    cursor = conn.cursor()
    
    sqlstr = "delete from dashboard_prefs where prefuid = %s;"
                                                                                    
    cursor.execute(sqlstr, (prefuid,))   
    conn.commit()
    
    return jsonify(result="OK")  



  
  except TypeError as e:
    log.info('freeboard_editdashboard: TypeError in  edit pref %s:  ', prefuid)
    log.info('freeboard_editdashboard: TypeError in  edit pref  %s:  ' % str(e))

  except ValueError as e:
    log.info('freeboard_deletedashboard: ValueError in  edit pref  %s:  ', prefuid)
    log.info('freeboard_deletedashboard: ValueError in  edit pref %s:  ' % str(e))
    
  except KeyError as e:
    log.info('freeboard_deletedashboard: KeyError in  edit pref  %s:  ', prefuid)
    log.info('freeboard_deletedashboard: KeyError in  edit pref  %s:  ' % str(e))

  except NameError as e:
    log.info('freeboard_deletedashboard: NameError in  edit pref  %s:  ', prefuid)
    log.info('freeboard_deletedashboard: NameError in  edit pref %s:  ' % str(e))
        
  except IndexError as e:
    log.info('freeboard_deletedashboard: IndexError in  edit pref  %s:  ', prefuid)
    log.info('freeboard_deletedashboard: IndexError in  edit pref  %s:  ' % str(e))  


  except:
    e = sys.exc_info()[0]
    log.info('freeboard_deletedashboard: Error in edit pref  %s:  ' % str(e))
    return jsonify(result="error") 

  
  finally:
    db_pool.putconn(conn)


    

@app.route('/freeboard_editdashboard')
@cross_origin()
def freeboard_editdashboard():
  conn = db_pool.getconn()
  

  prefname = request.args.get('prefname',1)
  prefuid = request.args.get('prefuid',1)


  

  log.info('freeboard_editdashboard: prefname  %s:  ', prefname)
  log.info('freeboard_editdashboard: prefuid  %s:  ', prefuid)
  


  try:
    cursor = conn.cursor()
    
    sqlstr = "update dashboard_prefs set prefname = %s where prefuid = %s;"
                                                                                    
    cursor.execute(sqlstr, (prefname, prefuid))   
    conn.commit()
    
    return jsonify(result="OK")  



  
  except TypeError as e:
    log.info('freeboard_editdashboard: TypeError in  edit pref %s:  ', prefuid)
    log.info('freeboard_editdashboard: TypeError in  edit pref  %s:  ' % str(e))

  except ValueError as e:
    log.info('freeboard_editdashboard: ValueError in  edit pref  %s:  ', prefuid)
    log.info('freeboard_editdashboard: ValueError in  edit pref %s:  ' % str(e))
    
  except KeyError as e:
    log.info('freeboard_editdashboard: KeyError in  edit pref  %s:  ', prefuid)
    log.info('freeboard_editdashboard: KeyError in  edit pref  %s:  ' % str(e))

  except NameError as e:
    log.info('freeboard_editdashboard: NameError in  edit pref  %s:  ', prefuid)
    log.info('freeboard_editdashboard: NameError in  edit pref %s:  ' % str(e))
        
  except IndexError as e:
    log.info('freeboard_editdashboard: IndexError in  edit pref  %s:  ', prefuid)
    log.info('freeboard_editdashboard: IndexError in  edit pref  %s:  ' % str(e))  


  except:
    e = sys.exc_info()[0]
    log.info('freeboard_editdashboard: Error in edit pref  %s:  ' % str(e))
    return jsonify(result="error") 

  
  finally:
    db_pool.putconn(conn)


    
@app.route('/freeboard_addnewdashboard')
@cross_origin()
def freeboard_addnewdashboard():
  
  log.info('freeboard_addnewdashboard start:  ')
  #return jsonify(result="error")


  try:  
    conn = db_pool.getconn()
    
    userid = request.args.get('userid',1)
    useremail = request.args.get('useremail',1)
    prefname = request.args.get('prefname',1)

    defaultjson = '{"version": 1,"allow_edit": true}'
    
    log.info('freeboard_addnewdashboard: userid  %s:  ', userid)
    log.info('freeboard_addnewdashboard: useremail  %s:  ', useremail)
    log.info('freeboard_addnewdashboard: prefname  %s:  ', prefname)
    
    prefuid=hash_string(useremail+prefname)
    log.info('freeboard_addnewdashboard: prefuid  %s:  ', prefuid)


    cursor = conn.cursor()
    
    sqlstr = " insert into dashboard_prefs (prefuid, userid, useremail, prefname, jsondata ) Values (%s,%s,%s,%s,%s);"
                                                                                    
    cursor.execute(sqlstr, (prefuid, userid, useremail, prefname, defaultjson))   
    conn.commit()
    
    return jsonify(result="OK")  


  except psycopg.ProgrammingError as e:
    log.info('freeboard_addnewdashboard: ProgrammingError in  update pref %s:  ', userid)
    log.info('freeboard_addnewdashboard: ProgrammingError in  update pref  %s:  ' % str(e))
    return jsonify(result="ProgrammingError error")
  
  except TypeError as e:
    log.info('freeboard_addnewdashboard: TypeError in  update pref %s:  ', userid)
    log.info('freeboard_addnewdashboard: TypeError in  update pref  %s:  ' % str(e))

  except ValueError as e:
    log.info('freeboard_addnewdashboard: ValueError in  update pref  %s:  ', userid)
    log.info('freeboard_addnewdashboard: ValueError in  update pref %s:  ' % str(e))
    
  except KeyError as e:
    log.info('freeboard_addnewdashboard: KeyError in  update pref  %s:  ', userid)
    log.info('freeboard_addnewdashboard: KeyError in  update pref  %s:  ' % str(e))

  except NameError as e:
    log.info('freeboard_addnewdashboard: NameError in  update pref  %s:  ', userid)
    log.info('freeboard_addnewdashboard: NameError in  update pref %s:  ' % str(e))
        
  except IndexError as e:
    log.info('freeboard_addnewdashboard: IndexError in  update pref  %s:  ', userid)
    log.info('freeboard_addnewdashboard: IndexError in  update pref  %s:  ' % str(e))  


  except:
    e = sys.exc_info()[0]
    log.info('freeboard_addnewdashboard: Error in update pref  %s:  ' % str(e))
    return jsonify(result="error") 

  
  finally:
    db_pool.putconn(conn)

"""

def getdashboardjson(prefuid):


    conn = db_pool.getconn()

    log.info("freeboard getdashboardjson data Query %s", prefuid)

    try:
    # first check db to see if deviceapikey is matched to device id

        cursor = conn.cursor()
        #cursor.execute(query, (deviceapikey,))
        #cursor.execute("select deviceid from user_devices where deviceapikey = '%s'" % deviceapikey)
        #key=('bfeba0c3c5244269b4c8d276872519a6',)
        cursor.execute("select jsondata  from dashboard_prefs where prefuid = %s" , (prefuid,))
        #response= cursor.query(query)
        i = cursor.fetchone()
        log.info("freeboard getdashboardjson response %s", i)            
        # see we got any matches
        if cursor.rowcount == 0:
        #if not response:
            # cursor.close
            db_pool.putconn(conn) 
            return ""
        
        else:
            jsondata = str(i[0])
            db_pool.putconn(conn) 
            return jsondata 


    except TypeError as e:
        log.info('freeboard: getdashboardjson TypeError in geting deviceid  %s:  ', prefuid)
        log.info('freeboard: getdashboardjson TypeError in geting deviceid  %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: getdashboardjson KeyError in geting deviceid  %s:  ', prefuid)
        log.info('freeboard: getdashboardjson KeyError in geting deviceid  %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: getdashboardjson NameError in geting deviceid  %s:  ', prefuid)
        log.info('freeboard: getdashboardjson NameError in geting deviceid  %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: getdashboardjson IndexError in geting deviceid  %s:  ', prefuid)
        log.info('freeboard: getdashboardjson IndexError in geting deviceid  %s:  ' % str(e))  


    except:
        log.info('freeboard: getdashboardjson Error in geting  deviceid %s:  ', prefuid)
        e = sys.exc_info()[0]
        log.info('freeboard: getdashboardjson Error in geting deviceid  %s:  ' % str(e))

    # cursor.close
    db_pool.putconn(conn)                       

    return ""  
"""

"""

def getdashboardlists(userid):


    conn = db_pool.getconn()

    log.info("freeboard getdashboardlists data Query %s", userid)

    try:
    # first check db to see if deviceapikey is matched to device id

        cursor = conn.cursor()

        cursor.execute("select prefuid, prefname  from dashboard_prefs where userid = %s" , (userid,))

        #log.info("freeboard getdashboardlists response %s", cursor)            

        # see we got any matches
        if cursor.rowcount == 0:
            log.info("freeboard getdashboardlists no matches")
            #return jsonify( message='Could not get prefuids', status='error')
            db_pool.putconn(conn) 
            return ""
        
        else:
            #log.info("freeboard getdashboardlists got matches %s : %s", cursor.description[0][0], value)
            preferences = [dict((cursor.description[i][0], value) \
                for i, value in enumerate(row)) for row in cursor.fetchall()]

            log.info("freeboard getdashboardlists response %s", preferences)     
            db_pool.putconn(conn) 
            return preferences


    except TypeError as e:
        log.info('freeboard: getdashboardlists TypeError in geting deviceid  %s:  ', userid)
        log.info('freeboard: getdashboardlists TypeError in geting deviceid  %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: getdashboardlists KeyError in geting deviceid  %s:  ', userid)
        log.info('freeboard: getdashboardlists KeyError in geting deviceid  %s:  ' % str(e))

    except NameErro as e:
        log.info('freeboard: getdashboardlists NameError in geting deviceid  %s:  ', userid)
        log.info('freeboard: getdashboardlists NameError in geting deviceid  %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: getdashboardlists IndexError in geting deviceid  %s:  ', userid)
        log.info('freeboard: getdashboardlists IndexError in geting deviceid  %s:  ' % str(e))  


    except:
        log.info('freeboard: getdashboardlists Error in geting  deviceid %s:  ', userid)
        e = sys.exc_info()[0]
        log.info('freeboard: getdashboardlists Error in geting deviceid  %s:  ' % str(e))

    # cursor.close
    db_pool.putconn(conn)                       

    return ""
"""

### hash ###
def hash_string(string):
    #salted_hash = string + application.config['SECRET_KEY']
    salted_hash = string + app.secret_key
    log.info('freeboard: hash_string salted_hash %s:  ', salted_hash)

    dashboardid = hashlib.md5(salted_hash.encode())
    log.info('freeboard: hash_string salted_hash %s:  ', dashboardid.hexdigest())
    #return md5.new(salted_hash).hexdigest()
    return dashboardid.hexdigest()


### data conversion utilities #####
#calculate baro offset in milibars from altitude in feet
def getAtmosphericCompensation(feet):

  if feet == '---':
    return 0

  if int(feet) < 0:
    return 0
  
  if int(feet) > 10000:
    return 317
  
  index = 0
  
  try:
    # divide by 200
    index = int(feet * 0.005)
  except:
    return 0

  #index range is 0 to 50
  gAtmosphericCompensation = [0,7,15,22,29,36,43,50,57,64,71,78,85,92,98,105,112,118,125,132,138,145,151,157,164,170,176,183,189,195,201,207,213,219,225,231,237,243,249,255,261,266,272,278,283,289,295,300,306,311,316]

  baro_milibars = gAtmosphericCompensation[index]
  baro_pascals = float(baro_milibars * 0.1)
  # convert to pascals
  return baro_pascals


#Convert Units between US and Metric
def convertunittype(units, value):


  if units == 'temperature':
    if value == 'US':
      return 0
    elif value == 'metric':
      return 1
    elif value == 'si':
      return 2
    elif value == 'nautical':
      return 0


    

  elif units == 'pressure':
    if value == 'US':
      return 8
    elif value == 'metric':
      return 9
    elif value == 'nautical':
      return 4
    elif value == 'si':
      return 9

  elif units == 'baro_pressure':
    if value == 'US':
      return 10
    elif value == 'metric':
      return 11
    elif value == 'nautical':
      return 10
    elif value == 'si':
      return 9



    

  elif units == 'speed':
    if value == 'US':
      return 5
    elif value == 'metric':
      return 6
    elif value == 'nautical':
      return 4
    elif value == 'si':
      return 7


    

  elif units == 'volume':
    if value == 'US':
      return 21
    elif value == 'metric':
      return 20
    elif value == 'si':
      return 22
    elif value == 'nautical':
      return 20



    
    
  elif units == 'flow':
    if value == 'US':
      return 18
    elif value == 'metric':
      return 19
    elif value == 'nautical':
      return 19
    elif value == 'si':
      return 19




    

  elif units == 'depth':
    if value == 'US':
      return 32
    elif value == 'metric':
      return 33    
    elif value == 'nautical':
      return 36
    elif value == 'si':
      return 33


  elif units == 'rain':
    if value == 'US':
      return 45
    elif value == 'metric':
      return 44    
    elif value == 'nautical':
      return 32
    elif value == 'si':
      return 33


  elif units == 44: #//= RAIN IN mm
       return float("{0:.2f}".format(value * 1000))  

  elif units == 45: #//=RAIN in inches
      return float("{0:.2f}".format(value * 39.3))
    

  elif units == 'distance':
    if value == 'US':
      return 34
    elif value == 'metric':
      return 33    
    elif value == 'nautical':
      return 35
    elif value == 'si':
      return 33



  elif units == 'degree':
    return 16

  elif units == 'radian':
    return 17

  
  elif units == 'rpm':
    return 24
  
  elif units == 'rps':
    return 25

  elif units == '%':
    return 26


  elif units == 'volts':
    return 27
  
  elif units == 'amps':
    return 28

  elif units == 'watts':
    return 29
  
  elif units == 'watthrs':
    return 30

  elif units == 'count':
    return 100
  
  elif units == 'time':
    return 37
  
  elif units == 'date':
    return 38
  
  elif units == 'hours':
    return 39

  else:
    return 44
  
    
#Convert Units used for freeboard numerical displays
def convertfbunits(value, units):
  units = int(units)

  #if not value:
  #  return "---"

  if value is None:
    return "---"

  if value == 'None':
    return "---"



  if units == 0: #//="0">Fahrenheit</option>
      return float("{0:.0f}".format((value * 1.8) - 459) )


  elif units ==  1: #//="1">Celsius</option>
      return float("{0:.0f}".format((value * 1.0) - 273) )


  elif units == 2: #//e="2">Kelvin</option>
      return float("{0:.0f}".format((value * 1.0) ) )


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



  elif units == 11: #//e="9">HPASCAL</option>
      return float("{0:.2f}".format(value * 10.0))


  #//  case 11: //="11">- - -</option>
  # //  case 12: //="12">TRUE</option>
  #//   case 13: //="13">MAGNETIC</option>
  #//   case 14: //="14">- - -</option>
  #//   case 15: //="15">- - -</option>
  elif units == 15:            #//   case 15: //="15">Lat/Lng</option>
    return float("{0:.8f}".format(value * 1.0 ) )

  elif units == 16:            #//   case 16: //="16">DEGREES</option>
    return float("{0:.0f}".format(value * 1.0 ) )

  #//   case 17: //="17">Radians</option>
  elif units == 18: #//="18">Gallons/hs</option>
      return float("{0:.2f}".format(value * 0.264172052 ) )


  elif units == 19: #//="19">Liters/hr</option>
      return float("{0:.2f}".format(value * 1.0 ) )


  #case 20: //="20">Liters</option>
  elif units == 21: #//="18">Gallons/hs</option>
      return float("{0:.2f}".format(value * 0.264172052 ) )


  #case 22: //="22">CubicMeter</option>
  #case 23: //="23">- - -</option>
  #case 24: //="24">RPM</option>
    
  elif units == 24: #//="24">RPM</option>
      return float("{0:.0f}".format(value *1.0))

    
  #case 25: //="25">RPS</option>   
    
  elif units == 26: #//="26">%</option>
      return float("{0:.0f}".format(value *1.0))


    
  elif units == 27: #//="27">Volts</option>
      return float("{0:.2f}".format(value *1.00))


  elif units == 31: #//="31">kWhrs</option>
      return float("{0:.2f}".format(value *01.0))
  # case 28: //="28">Amps</option>
            
  elif units == 32: #//="32">Feet</option>
      return float("{0:.2f}".format(value * 3.28084)) 

  elif units == 33: #//="33">Meters</option>
      return float("{0:.2f}".format(value * 1.0))

  elif units == 34: #//="34">Miles</option>
      return float("{0:.2f}".format(value * 0.000621371))              

  elif units == 35: #//="35">Nautical Mile</option>
      return float("{0:.2f}".format(value * 0.0005399568))                
  
  elif units == 36: #//="36">Fathoms</option>
      return float("{0:.2f}".format(value * 0.546806649))



  elif units == 44: #//= RAIN IN mm
       return float("{0:.2f}".format(value * 1000))  

  elif units == 45: #//=RAIN in inches
      return float("{0:.2f}".format(value * 39.3))


  elif units == 37: #//="37">Time</option>
      #log.info('HeartBeat time %s:', datetime.datetime.fromtimestamp(int(value)).strftime('%H:%M:%S'))
      return datetime.datetime.fromtimestamp(int(value)).strftime('%H:%M:%S')

  elif units == 38: #//="38">Date/time</option>
      #log.info('HeartBeat time %s:', datetime.datetime.fromtimestamp(int(value)).strftime('%m/%d/%Y %H:%M:%S'))
      return (datetime.datetime.fromtimestamp(int(value)).strftime('%m/%d/%Y %H:%M:%S'))
    
  elif units == 39: #//="39">Hours</option>
      #Engine Hours (value / (60*60))
       return float("{0:.2f}".format(value * 0.000277777))  

  elif units == 43: #//="43">Volts 10</option>
      return float("{0:.2f}".format(value * 0.1))

  elif units ==100: #//=convert to integer
      return int(value)
    
  else:
      return float("{0:.2f}".format(value))

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


def getepochtimes(Interval):



    log.info('freeboard:  getepochtimes Interval %s:  ', Interval)

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
                oldtime = datetime.datetime.now() - relativedelta(months=1)
            elif Interval == "6month":
                resolution = 60*60*24*30*6
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - relativedelta(months=6)
            elif Interval == "12month":
                resolution = 60*60*24*30*12
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - relativedelta(months=12)                
                
            else:
                resolution = 60
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(minutes=2)

                
        epochtimes.append(startepoch)
        epochtimes.append(endepoch)
        epochtimes.append(resolution)

    except TypeError as e:
        log.info('freeboard: TypeError in geting getepochtimes parameters %s:  ', Interval)
        log.info('freeboard: TypeError in geting getepochtimes parameters %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: KeyError in geting getepochtimes parameters %s:  ', Interval)
        log.info('freeboard: KeyError in geting getepochtimes parameters %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: NameError in geting getepochtimes parameters %s:  ', Interval)
        log.info('freeboard: NameError in geting getepochtimes parameters %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: IndexError in geting getepochtimes parameters %s:  ', Interval)
        log.info('freeboard: IndexError in geting getepochtimes parameters %s:  ' % str(e))  


    except:
        log.info('freeboard: Error in geting  getepochtimes %s:  ', Interval)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting getepochtimes parameters %s:  ' % str(e))

    return(epochtimes)




def getendepochtimes(starttime, Interval):


    log.info('freeboard:  getendepochtimes starttime %s:  ', starttime)
    log.info('freeboard:  getendepochtimes Interval %s:  ', Interval)

    epochtimes=[]

    
    try:
        # if 0 then use current time
        # needs to be greater then 1/1/2010
        if starttime > 1262264399:
            #nowtime = datetime.datetime.now()
            #nowtime = datetime.datetime.utcfromtimestamp(starttime)
            endepoch =  int(time.time())
            startepoch = starttime

            if Interval== "1min":
                resolution = 60
                endepoch = startepoch + (resolution * 2)
                         
            elif Interval == "2min":
                resolution = 60*2
                endepoch = startepoch + (resolution * 1)
                         
            elif Interval == "5min":
                resolution = 60*5
                endepoch = startepoch + (resolution * 1)
                         
            elif Interval== "10min":
                resolution = 60*10
                endepoch = startepoch + (resolution * 1)
                         
            elif Interval == "15min":
                resolution = 60*15
                endepoch = startepoch + (resolution * 1)
                         
            elif Interval== "30min":
                resolution = 60*30
                endepoch = startepoch + (resolution * 1)
                         
            elif Interval== "1hour":
                resolution = 60*60
                endepoch = startepoch + (resolution * 1)
                         
            elif Interval== "2hour":
                resolution = 60*60*2
                endepoch = startepoch + (resolution * 1)
                         
            elif Interval== "3hour":
                resolution = 60*60*3
                endepoch = startepoch + (resolution * 1)
                         



            elif Interval == "4hour":
                resolution = 60*60*4
                endepoch = startepoch + (resolution * 1)
                         
            elif Interval == "6hour":
                resolution = 60*60*6
                endepoch = startepoch + (resolution * 1)
                         
            elif Interval == "8hour":
                resolution = 60*60*8
                endepoch = startepoch + (resolution * 1)
                         
            elif Interval == "12hour":
                resolution = 60*60*12
                endepoch = startepoch + (resolution * 1)
                         
            elif Interval == "1day":
                resolution = 60*60*24
                endepoch = startepoch + (resolution * 1)
                         
            elif Interval == "2day":
                resolution = 60*60*24*2
                endepoch = startepoch + (resolution * 1)
                         
            elif Interval== "7day":
                resolution = 60*60*24*7
                endepoch = startepoch + (resolution * 1)
                         
            elif Interval == "1month":
                resolution = 60*60*24*30
                endepoch = startepoch + (resolution * 1)
                         
            else:
                resolution = 60
                endepoch = startepoch + (resolution * 1)
                         
        else:
          endepoch =  int(time.time())
          startepoch = endepoch - 60
          resolution = 60
                
        epochtimes.append(startepoch)
        epochtimes.append(endepoch)
        epochtimes.append(resolution)

    except TypeError as e:
        log.info('freeboard: TypeError in geting getendepochtimes parameters %s:  ', Interval)
        log.info('freeboard: TypeError in geting getendepochtimes parameters %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: KeyError in geting getendepochtimes parameters %s:  ', Interval)
        log.info('freeboard: KeyError in geting getendepochtimes parameters %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: NameError in geting getendepochtimes parameters %s:  ', Interval)
        log.info('freeboard: NameError in geting getendepochtimes parameters %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: IndexError in geting Interval parameters %s:  ', Interval)
        log.info('freeboard: IndexError in geting Interval parameters %s:  ' % str(e))  


    except:
        log.info('freeboard: Error in geting  Intervalparameters %s:  ', Interval)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting Interval parameters %s:  ' % str(e))

    return(epochtimes)

def get_unit_label(units):
  
            units = int(units)

            if units == 0: #//="0">Fahrenheit</option>
                return str("Fahrenheit") 
            
            
            elif units ==  1: #//="1">Celsius</option>
                return str("Celsius" )
            

            elif units == 2: #//e="2">Kelvin</option>
                return str("Kelvin" )
            

            elif units == 3: # //="3">- - -</option> 
               return str("---" )
              
      
            elif units == 4: #//="4">Knots</option>
                return str("Knots" )
           

            elif units == 5: #//="5">MPH</option>
                return str("MPH" )
            
            
            elif units == 6: #//e="6">KPH</option>
                return str("KPH" )
           
      
            elif units ==  7: #//="7">- - -</option>
                 return str("Meters/sec" )             
              
            elif units == 8: #//="8">PSI</option>
                return str("PSI" )
          
            

            elif units == 9: #//e="9">KPASCAL</option>
                return str("KPASCAL" )

   
            
            elif units == 10: #//="10">INHG</option>
                return str("INHG" )
    

            elif units ==  11: #//="11">- - -</option>
               return str("---" )
              
            elif units == 12: #//="12">TRUE</option>
               return str("TRUE" )
              
            elif units ==  13: #//="13">MAGNETIC</option>
               return str("MAGNETIC" )
              
            elif units ==  14: #//="14">- - -</option>
               return str("---" )
              
            elif units ==  15: #//="15">- - -</option>
               return str("---" )
              
            elif units == 16:            #//   case 16: //="16">DEGREES</option>
              return str("DEGREES" )
            
            elif units ==  17: #//="17">#Radians</option>
              return str("Radians" )
            
            elif units == 18: #//="18">Gallons/hs</option>
                return str("Gallons/hr" )

            elif units == 19: #//="19">Liters/hr</option>
               return str("Gallons/hs" )

            elif units == 20: #//="20">Liters</option>
                return str("Liters/hr" )              
            elif units ==  21: #//="21">Gallons</option>
                return str("Gallons" )
              
            elif units ==  22: #//="22">CubicMeter</option>
                return str("CubicMeter" )
              
            elif units ==  23: #//="23">- - -</option>
                return str("Hertz" )
              
            elif units ==  24: #//="24">RPM</option>
                return str("RPM" )
              
            elif units ==  25: #//="25">RPS</option>
                return str("RPS" )
              
            elif units ==  26: #//="26">%</option>
                return str("%" )
              
            elif units == 27: #//="27">Volts</option>
                return str("Volts" )
              
            elif units == 28: #//="27">Volts</option>
                return str("Amps" )
              
            elif units == 29: #//="27">Volts</option>
                return str("Watts" )
              
            elif units == 30: #//="27">Volts</option>
                return str("Watts/hr" )

            elif units == 31: #//="31">kWhrs</option>
                return str("kWhrs" )  
            
            elif units == 32: #//="32">Feet</option>
                return str("Feet" )
      
            elif units == 33: #//="33">Meters</option>
                return str("Meters" )

            elif units == 45: #//="32">Feet</option>
                return str("Inches" )
      
            elif units == 44: #//="33">Meters</option>
                return str("millimeters" )
              

            elif units == 34: #//="34">Miles</option>
                return str("Miles" )            
  
            elif units == 35: #//="35">Nautical Mile</option>
                return str("Nautical Mile" )             
            
            elif units == 36: #//="36">Fathoms</option>
              return str("Fathoms" )

            elif units == 37: #//="37">Time</option>
                return str("Time" )

            elif units == 38: #//="38">Date/time</option>
                return str("Date/time" )
              
            elif units == 39: #//="39">Hours</option>
                return str("Hours" )

            elif units ==43: #//="27">Volts 10X</option>
                return str("Volts 10X" )
              
            
            else:
                return str("---" )


### INFLUX API CALLS #####




@app.route('/freeboard_environmental')
@cross_origin()
def freeboard_environmental():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    Instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    env_type = request.args.get('type',"outside")
    mytimezone = request.args.get('timezone',"UTC")
    units= request.args.get('units',"US")
    mode  = request.args.get('mode',"median")
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]


    strvalue = ""
    value1 = '---'
    value2 = '---'
    value3 = '---'
    value4 = '---'

    temperature=[]
    atmospheric_pressure=[]
    humidity=[]
    
    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")        

    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)
    
    #serieskeys={'deviceid'=deviceid, 'sensor'='environmental_data', 'instance'='0', 'type'='Outside_Temperature'}

    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    if env_type == "inside":
      serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Inside Temperature' OR type='Inside Humidity')"

    elif env_type == "inside mesh":
      serieskeys= serieskeys +  " sensor='environmental_data' AND instance='" + Instance + "' "

      
    elif env_type == "sea":
      serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Sea Temperature' OR type='Inside Humidity')"

      
    else:
      serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Outside Temperature' OR type='Outside Humidity')"





      
    #serieskeys= serieskeys +  " sensor='environmental_data'  AND type='Outside_Temperature'"
    #serieskeys= serieskeys +  " sensor='environmental_data'  "
    
    Key2="deviceid:001EC010AD69.sensor:environmental_data.source:0.instance:0.type:Outside_Temperature.parameter:humidity.HelmSmart"
    Key3="deviceid:001EC010AD69.sensor:environmental_data.source:0.instance:0.type:Outside_Temperature.parameter:atmospheric_pressure.HelmSmart"



    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)



    if serieskeys.find("*") > 0:
        serieskeys = serieskeys.replace("*", ".*")

    if mode == "median":
        query = ('select  median(temperature) AS temperature, median(atmospheric_pressure) AS  atmospheric_pressure, median(humidity) AS humidity , median(altitude) AS altitude from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

    elif mode == "max":
        query = ('select  max(temperature) AS temperature, max(atmospheric_pressure) AS  atmospheric_pressure, max(humidity) AS humidity, max(altitude) AS altitude from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

    elif mode == "min":
        query = ('select  min(temperature) AS temperature, min(atmospheric_pressure) AS  atmospheric_pressure, min(humidity) AS humidity, min(altitude) AS altitude from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

        
    else:
      
      query = ('select  mean(temperature) AS temperature, mean(atmospheric_pressure) AS  atmospheric_pressure, mean(humidity) AS humidity, mean(altitude) AS altitude from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
 

    """
    if serieskeys.find("*") > 0:
        serieskeys = serieskeys.replace("*", ".*")

        query = ('select  median(temperature) AS temperature, median(atmospheric_pressure) AS  atmospheric_pressure, median(humidity) AS humidity from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
    else:
      
      query = ('select  median(temperature) AS temperature, median(atmospheric_pressure) AS  atmospheric_pressure, median(humidity) AS humidity from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
 
    """    

    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))


            
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', response)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        pass

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing', 'update':'False','temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity))})     
      

    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing', 'update':'False','temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity))})     

    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)
    
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'

      temperature=[]
      atmospheric_pressure=[]
      atmospheric_pressure_sea=[]
      humidity=[]
      altitude=[]
      ts =startepoch*1000


      
      points = list(response.get_points())

      #log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'
        value5 = '---'
      
        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)

          
        if point['temperature'] is not None: 
          value1 = convertfbunits(point['temperature'],  convertunittype('temperature', units))
        temperature.append({'epoch':ts, 'value':value1})
          
        if point['atmospheric_pressure'] is not None:         
          value2 = convertfbunits(point['atmospheric_pressure'], convertunittype('baro_pressure', units))
        atmospheric_pressure.append({'epoch':ts, 'value':value2})
                    
        if point['humidity'] is not None:         
          value3 = convertfbunits(point['humidity'], 26)
        humidity.append({'epoch':ts, 'value':value3})

                    
        if point['altitude'] is not None:         
          value4 = convertfbunits(point['altitude'], 32)
        altitude.append({'epoch':ts, 'value':value4})

        if point['atmospheric_pressure'] is not None and point['altitude'] is not None:
          #get pressure in KPa
          value2 = convertfbunits(point['atmospheric_pressure'], 9)
          #get altitde in feet
          value4 = convertfbunits(point['altitude'], 32)
          # get adjustment for altitude in KPa
          #value5 = getAtmosphericCompensation(value4)
          value5 =0
          #add offset if any in KPa
          value5 = convertfbunits(value2 + value5, convertunittype('baro_pressure', units))
          
        atmospheric_pressure_sea.append({'epoch':ts, 'value':value5})        
 

          
        #mydatetimestr = str(point['time'])

        #mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')

      #log.info('freeboard: freeboard returning data values temperature:%s, baro:%s, humidity:%s  ', value1,value2,value3)

      """
      log.info('freeboard: before exosite write:')
      o = onep.OnepV1()

      cik = '5b38da024d8a1f252e575202afb431ef22d3eb66'
      #dataport_alias = 'Device'
      #val_to_write = 'Data'
      dataport_alias = 'air_temperature'
      val_to_write =float(value1)

      #testvar = o.write(cik, {"alias": dataport_alias}, val_to_write,{})
      #log.info('freeboard: fter exosite write:%s', testvar)
      o.write(cik, {"alias": dataport_alias}, val_to_write,{})
      log.info('freeboard: after exosite write:')

       """     

      callback = request.args.get('callback')
      myjsondatetz = mydatetime.strftime("%B %d, %Y %H:%M:%S")        
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','temperature':value1, 'baro':value2, 'humidity':value3})
      return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity)), 'altitude':list(reversed(altitude)), 'atmospheric_pressure_sea':list(reversed(atmospheric_pressure_sea))})     

    except AttributeError as e:
      #log.info('inFluxDB_GPS: AttributeError in freeboard_environmental %s:  ', SERIES_KEY1)
      #e = sys.exc_info()[0]

      log.info('freeboard_environmental: AttributeError in freeboard_environmental %s:  ' % str(e))
      
    except TypeError as e:
      log.info('freeboard_environmental:  TypeError in freeboard_environmental point %s:  ', point)
      #e = sys.exc_info()[0]
      log.info('freeboard_environmental: TypeError in freeboard_environmental %s:  ' % str(e))
      
    except ValueError as e:
      log.info('freeboard_environmental: ValueError in freeboard_environmental point %s:  ', point)
      #e = sys.exc_info()[0]

      log.info('freeboard_environmental: ValueError in freeboard_environmental point%s:  ' % str(e))            
      
    except NameError as e:
      #log.info('inFluxDB_GPS: NameError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
      #e = sys.exc_info()[0]
      log.info('freeboard_environmental: NameError in freeboard_environmental %s:  ' % str(e))           

    except IndexError as e:
      log.info('freeboard_environmental: IndexError in freeboard_environmental point %s:  ', point)
      #e = sys.exc_info()[0]
      log.info('freeboard_environmental: IndexError in freeboard_environmental %s:  ' % str(e))

    except OverflowError as e:
      log.info('freeboard_environmental: OverflowError in freeboard_environmental point %s:  ', point)
      #e = sys.exc_info()[0]
      log.info('freeboard_environmental: OverflowError in freeboard_environmental %s:  ' % str(e))

      
    #except pyonep.exceptions.JsonRPCRequestException as ex:
    #    print('JsonRPCRequestException: {0}'.format(ex))
        
    #except pyonep.exceptions.JsonRPCResponseException as ex:
    #    print('JsonRPCResponseException: {0}'.format(ex))
        
    #except pyonep.exceptions.OnePlatformException as ex:
    #    print('OnePlatformException: {0}'.format(ex))
       
    except:
        log.info('freeboard: Error in geting freeboard_environmental response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard_environmental ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error',  update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })



@app.route('/freeboard_environmental_calculated')
@cross_origin()
def freeboard_environmental_calculated():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    Instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    env_type = request.args.get('type',"outside")
    mytimezone = request.args.get('timezone',"UTC")
    units= request.args.get('units',"US")
    mode  = request.args.get('mode',"median")
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]


    strvalue = ""
    value1 = '---'
    value2 = '---'
    value3 = '---'
    value4 = '---'

    temperature=[]
    atmospheric_pressure=[]
    humidity=[]
    wind_speed=[]
    
    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")        

    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)
    
    #serieskeys={'deviceid'=deviceid, 'sensor'='environmental_data', 'instance'='0', 'type'='Outside_Temperature'}

    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    if env_type == "inside":
      serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Inside Temperature' OR type='Inside Humidity')"

    elif env_type == "inside mesh":
      serieskeys= serieskeys +  " sensor='environmental_data' AND instance='" + Instance + "' "

      
    elif env_type == "sea":
      serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Sea Temperature' OR type='Inside Humidity')"

      
    else:
      #serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Outside Temperature' OR type='Outside Humidity')"
      serieskeys= serieskeys +  " (sensor='wind_data' OR sensor='environmental_data') AND instance='0' AND (type='Apparent Wind'  OR type='Outside Temperature' OR type='Outside Humidity')"




      
    #serieskeys= serieskeys +  " sensor='environmental_data'  AND type='Outside_Temperature'"
    #serieskeys= serieskeys +  " sensor='environmental_data'  "
    
    Key2="deviceid:001EC010AD69.sensor:environmental_data.source:0.instance:0.type:Outside_Temperature.parameter:humidity.HelmSmart"
    Key3="deviceid:001EC010AD69.sensor:environmental_data.source:0.instance:0.type:Outside_Temperature.parameter:atmospheric_pressure.HelmSmart"



    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)



    if serieskeys.find("*") > 0:
        serieskeys = serieskeys.replace("*", ".*")

    if mode == "median":
        query = ('select  median(temperature) AS temperature, median(atmospheric_pressure) AS  atmospheric_pressure, median(humidity) AS humidity , median(altitude) AS altitude, median(wind_speed) AS  wind_speed from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

    elif mode == "max":
        query = ('select  max(temperature) AS temperature, max(atmospheric_pressure) AS  atmospheric_pressure, max(humidity) AS humidity, max(altitude) AS altitude, max(wind_speed) AS  wind_speed from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

    elif mode == "min":
        query = ('select  min(temperature) AS temperature, min(atmospheric_pressure) AS  atmospheric_pressure, min(humidity) AS humidity, min(altitude) AS altitude, min(wind_speed) AS  wind_speed from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

        
    else:
      
      query = ('select  mean(temperature) AS temperature, mean(atmospheric_pressure) AS  atmospheric_pressure, mean(humidity) AS humidity, mean(altitude) AS altitude, mean(wind_speed) AS  wind_speed from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
 

    """
    if serieskeys.find("*") > 0:
        serieskeys = serieskeys.replace("*", ".*")

        query = ('select  median(temperature) AS temperature, median(atmospheric_pressure) AS  atmospheric_pressure, median(humidity) AS humidity from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
    else:
      
      query = ('select  median(temperature) AS temperature, median(atmospheric_pressure) AS  atmospheric_pressure, median(humidity) AS humidity from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
 
    """    

    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))


            
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', response)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        pass

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing', 'update':'False','temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity))})     
      

    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing', 'update':'False','temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity))})     

    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)
    
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'

      temperature=[]
      atmospheric_pressure=[]
      atmospheric_pressure_sea=[]
      humidity=[]
      altitude=[]
      windchill=[]
      heatindex=[]
      dewpoint=[]
      feelslike=[]

      
      ts =startepoch*1000


      
      points = list(response.get_points())

      log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'
        value5 = '---'
        tempF='---'
        tempC='---'
        humidity100='---'
        windmph='---'
      
        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)

          
          
        if point['temperature'] is not None: 
          value1 = convertfbunits(point['temperature'],  convertunittype('temperature', units))
          tempF=convertfbunits(point['temperature'],  0)
          tempC=convertfbunits(point['temperature'],  1)          
        temperature.append({'epoch':ts, 'value':value1})
          
        if point['atmospheric_pressure'] is not None:         
          value2 = convertfbunits(point['atmospheric_pressure'], convertunittype('baro_pressure', units))
        atmospheric_pressure.append({'epoch':ts, 'value':value2})
                    
        if point['humidity'] is not None:         
          value3 = convertfbunits(point['humidity'], 26)
          humidity100 = convertfbunits(point['humidity'], 26)
        humidity.append({'epoch':ts, 'value':value3})

                    
        if point['altitude'] is not None:         
          value4 = convertfbunits(point['altitude'], 32)
        altitude.append({'epoch':ts, 'value':value4})

        if point['atmospheric_pressure'] is not None and point['altitude'] is not None:
          #get pressure in KPa
          value2 = convertfbunits(point['atmospheric_pressure'], 9)
          #get altitde in feet
          value4 = convertfbunits(point['altitude'], 32)
          # get adjustment for altitude in KPa
          value5 = getAtmosphericCompensation(value4)
          #add offset if any in KPa
          value5 = convertfbunits(value2 + value5, convertunittype('baro_pressure', units))
          
        atmospheric_pressure_sea.append({'epoch':ts, 'value':value5})        
 

        if point['wind_speed'] is not None:         
          value6 = convertfbunits(point['wind_speed'], convertunittype('speed', units))
          windmph = convertfbunits(point['wind_speed'], 5)
        wind_speed.append({'epoch':ts, 'value':value6})

        try:

          # calculate dew_point
          if tempC != '---' and  humidity100 != '---':
            #dp = dew_point(temperature=tempF, humidity=humidity100)
            dp = dew_point(temperature=tempC, humidity=humidity100)
            log.info('freeboard:  freeboard_environmental_calculated dew_point  %s:', dp.k)
            dewpoint.append({'epoch':ts, 'value':convertfbunits(dp.k,  convertunittype('temperature', units))})

            
          # calculate heat_index
          if tempF != '---' and  humidity100 != '---':        
            hi= heat_index(temperature=tempF, humidity=humidity100)
            log.info('freeboard:  freeboard_environmental_calculated heat_index %s:', hi.k)
            heatindex.append({'epoch':ts, 'value':convertfbunits(hi.k,  convertunittype('temperature', units))})

            
          # calculate feels_like
          if tempF != '---' and  humidity100 != '---' and  windmph != '---':
            fl = feels_like(temperature=tempF, humidity= humidity100 , wind_speed=windmph)
            log.info('freeboard:  freeboard_environmental_calculated feels_like  %s:', fl.k)
            feelslike.append({'epoch':ts, 'value':convertfbunits(fl.k,  convertunittype('temperature', units))})

          # calculate Wind Chill
          if tempF != '---' and  windmph != '---':
            wc = wind_chill(temperature=tempF, wind_speed=windmph)
            log.info('freeboard:  freeboard_environmental_calculated wind chill %s:', wc.k)
            windchill.append({'epoch':ts, 'value':convertfbunits(wc.k,  convertunittype('temperature', units))})
 

        except AttributeError as e:
          log.info('freeboard_environmental_calculated: AttributeError in calculated %s:  ' % str(e))
          
        except TypeError as e:
          log.info('freeboard_environmental_calculated: TypeError in calculated %s:  ' % str(e))
          
        except ValueError as e:
          log.info('freeboard_environmental_calculated: ValueError in calculated %s:  ' % str(e))            
          
        except NameError as e:
          log.info('freeboard_environmental_calculated: NameError in calculated %s:  ' % str(e))           

        except IndexError as e:
          log.info('freeboard_environmental_calculated: IndexError in calculated %s:  ' % str(e))
          
        except:
          e = sys.exc_info()[0]
          log.info('freeboard_environmental_calculated: Error in geting calculated ststs %s:  ' % e)



        
        #mydatetimestr = str(point['time'])

        #mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')

      #log.info('freeboard: freeboard returning data values temperature:%s, baro:%s, humidity:%s  ', value1,value2,value3)

      """
      log.info('freeboard: before exosite write:')
      o = onep.OnepV1()

      cik = '5b38da024d8a1f252e575202afb431ef22d3eb66'
      #dataport_alias = 'Device'
      #val_to_write = 'Data'
      dataport_alias = 'air_temperature'
      val_to_write =float(value1)

      #testvar = o.write(cik, {"alias": dataport_alias}, val_to_write,{})
      #log.info('freeboard: fter exosite write:%s', testvar)
      o.write(cik, {"alias": dataport_alias}, val_to_write,{})
      log.info('freeboard: after exosite write:')

       """     

      callback = request.args.get('callback')
      myjsondatetz = mydatetime.strftime("%B %d, %Y %H:%M:%S")        
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','temperature':value1, 'baro':value2, 'humidity':value3})
      return '{0}({1})'.format(callback, {'date_time':myjsondate,
                                          'update':'True','temperature':list(reversed(temperature)),
                                          'atmospheric_pressure':list(reversed(atmospheric_pressure)),

                                           'humidity':list(reversed(humidity)),
                                           'altitude':list(reversed(altitude)),
                                          
                                           'dewpoinr':list(reversed(dewpoint)),
                                           'heatindex':list(reversed(heatindex)),
                                           'feelslike':list(reversed(feelslike)),
                                           'windchill':list(reversed(windchill)),

                                           'atmospheric_pressure_sea':list(reversed(atmospheric_pressure_sea))})     

    except AttributeError as e:
      #log.info('inFluxDB_GPS: AttributeError in freeboard_environmental %s:  ', SERIES_KEY1)
      #e = sys.exc_info()[0]

      log.info('freeboard_environmental: AttributeError in freeboard_environmental %s:  ' % str(e))
      
    except TypeError as e:
      l#og.info('inFluxDB_GPS: TypeError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
      #e = sys.exc_info()[0]

      log.info('inFluxDB_GPS: TypeError in freeboard_environmental %s:  ' % str(e))
      
    except ValueError as e:
      log.info('freeboard_environmental: ValueError in freeboard_environmental point %s:  ', point)
      #e = sys.exc_info()[0]

      log.info('freeboard_environmental: ValueError in freeboard_environmental point%s:  ' % str(e))            
      
    except NameError as e:
      #log.info('inFluxDB_GPS: NameError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
      #e = sys.exc_info()[0]
      log.info('freeboard_environmental: NameError in freeboard_environmental %s:  ' % str(e))           

    except IndexError as e:
      log.info('freeboard_environmental: IndexError in freeboard_environmental point %s:  ', point)
      #e = sys.exc_info()[0]
      log.info('freeboard_environmental: IndexError in freeboard_environmental %s:  ' % str(e))
      
    except pyonep.exceptions.JsonRPCRequestException as ex:
        print('JsonRPCRequestException: {0}'.format(ex))
        
    except pyonep.exceptions.JsonRPCResponseException as ex:
        print('JsonRPCResponseException: {0}'.format(ex))
        
    except pyonep.exceptions.OnePlatformException as ex:
        print('OnePlatformException: {0}'.format(ex))
       
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error',  update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })



@app.route('/freeboard_environmental_metar')
@cross_origin()
def freeboard_environmental_metar():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"1min")
    Instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    env_type = request.args.get('type',"outside")
    mytimezone = request.args.get('timezone',"UTC")
    units= request.args.get('units',"US")
    mode  = request.args.get('mode',"median")
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]

    strvalue = ""
    value1 = '---'
    value2 = '---'
    value3 = '---'
    value4 = '---'

    temperature=[]
    atmospheric_pressure=[]
    humidity=[]
    wind_speed=[]
    
    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")        

    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })

    devicename = getedevicename(deviceapikey)
    
    log.info("freeboard devicename %s", devicename)

    if devicename == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'devicename error' })




    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)
    
    #serieskeys={'deviceid'=deviceid, 'sensor'='environmental_data', 'instance'='0', 'type'='Outside_Temperature'}

    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    if env_type == "inside":
      serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Inside Temperature' OR type='Inside Humidity')"

    elif env_type == "inside mesh":
      serieskeys= serieskeys +  " sensor='environmental_data' AND instance='" + Instance + "' "

      
    elif env_type == "sea":
      serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Sea Temperature' OR type='Inside Humidity')"

      
    else:
      #serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Outside Temperature' OR type='Outside Humidity')"
      serieskeys= serieskeys +  " (sensor='wind_data' OR sensor='environmental_data') AND instance='0' AND (type='Apparent Wind'  OR type='Outside Temperature' OR type='Outside Humidity')"




      
    #serieskeys= serieskeys +  " sensor='environmental_data'  AND type='Outside_Temperature'"
    #serieskeys= serieskeys +  " sensor='environmental_data'  "
    
    Key2="deviceid:001EC010AD69.sensor:environmental_data.source:0.instance:0.type:Outside_Temperature.parameter:humidity.HelmSmart"
    Key3="deviceid:001EC010AD69.sensor:environmental_data.source:0.instance:0.type:Outside_Temperature.parameter:atmospheric_pressure.HelmSmart"



    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)



    if serieskeys.find("*") > 0:
        serieskeys = serieskeys.replace("*", ".*")

    if mode == "median":
        query = ('select  median(temperature) AS temperature, median(atmospheric_pressure) AS  atmospheric_pressure, median(humidity) AS humidity , median(altitude) AS altitude, median(wind_speed) AS  wind_speed , median(wind_direction) AS  wind_direction from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

    elif mode == "max":
        query = ('select  max(temperature) AS temperature, max(atmospheric_pressure) AS  atmospheric_pressure, max(humidity) AS humidity, max(altitude) AS altitude, max(wind_speed) AS  wind_speed , max(wind_direction) AS  wind_direction from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

    elif mode == "min":
        query = ('select  min(temperature) AS temperature, min(atmospheric_pressure) AS  atmospheric_pressure, min(humidity) AS humidity, min(altitude) AS altitude, min(wind_speed) AS  wind_speed , min(wind_direction) AS  wind_direction from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

        
    else:
      
      query = ('select  mean(temperature) AS temperature, mean(atmospheric_pressure) AS  atmospheric_pressure, mean(humidity) AS humidity, mean(altitude) AS altitude, mean(wind_speed) AS  wind_speed , mean(wind_direction) AS  wind_direction from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
 

    """
    if serieskeys.find("*") > 0:
        serieskeys = serieskeys.replace("*", ".*")

        query = ('select  median(temperature) AS temperature, median(atmospheric_pressure) AS  atmospheric_pressure, median(humidity) AS humidity from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
    else:
      
      query = ('select  median(temperature) AS temperature, median(atmospheric_pressure) AS  atmospheric_pressure, median(humidity) AS humidity from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
 
    """    

    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))


            
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', response)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        pass

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing', 'update':'False','temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity))})     
      

    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing', 'update':'False','temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity))})     

    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)
    
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'
      value5 = '---'
      value6 = '---'
      value7 = '---'
      temperature=""
      atmospheric_pressure=""
      atmospheric_pressure_sea=""
      humidity=""
      altitude=""
      windchill=""
      wind_speed=""
      wind_dir=""
      heatindex=""
      dewpoint=""
      feelslike=""

      
      ts =startepoch*1000


      
      points = list(response.get_points())

      log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'
        value5 = '---'
        value6 = '---'
        value7 = '---'
        tempF='---'
        tempC='---'
        humidity100='---'
        windmph='---'
        winddir='---'
      
        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)

          
          
        if point['temperature'] is not None: 
          temperature = int(convertfbunits(point['temperature'],  1)   )
          temperature1hr = str(temperature * 10 ).zfill(4)
          temperature = str(temperature).zfill(2)

          tempF=convertfbunits(point['temperature'],  0)
          tempC=convertfbunits(point['temperature'],  1)          

          
        if point['atmospheric_pressure'] is not None:         
          atmospheric_pressure = int((convertfbunits(point['atmospheric_pressure'], convertunittype('baro_pressure', units))) * 100)
          atmospheric_pressure = str(atmospheric_pressure).zfill(4)
                    
        if point['humidity'] is not None:         
          humidity = convertfbunits(point['humidity'], 26)
          humidity100 = convertfbunits(point['humidity'], 26)


                    
        if point['altitude'] is not None:         
          altitude = convertfbunits(point['altitude'], 32)


        if point['atmospheric_pressure'] is not None and point['altitude'] is not None:
          #get pressure in KPa
          value2 = convertfbunits(point['atmospheric_pressure'], 9)
          #get altitde in feet
          value4 = convertfbunits(point['altitude'], 32)
          # get adjustment for altitude in KPa
          value5 = getAtmosphericCompensation(value4)
          #add offset if any in KPa
          atmospheric_pressure_sea = int((convertfbunits(value2 + value5, convertunittype('baro_pressure', units))) * 10)
          
   
 

        if point['wind_speed'] is not None:         
          wind_speed = int(convertfbunits(point['wind_speed'], 4))
          windmph = int(convertfbunits(point['wind_speed'], 5))
          wind_speed =str(wind_speed).zfill(2)
       

        if point['wind_direction'] is not None:         
          wind_dir = int(convertfbunits(point['wind_direction'], 16))
          wind_dir =str(wind_dir).zfill(3)

        try:

          # calculate dew_point
          if tempC != '---' and  humidity100 != '---':
            #dp = dew_point(temperature=tempF, humidity=humidity100)
            dp = dew_point(temperature=tempC, humidity=humidity100)
            log.info('freeboard:  freeboard_environmental_calculated dew_point  %s:', dp.k)
            dewpoint=int(convertfbunits(dp.k, 1))
            dewpoint1hr = str(dewpoint * 10).zfill(4)
            dewpoint = str(dewpoint).zfill(2)


            
          # calculate heat_index
          if tempF != '---' and  humidity100 != '---':        
            hi= heat_index(temperature=tempF, humidity=humidity100)
            log.info('freeboard:  freeboard_environmental_calculated heat_index %s:', hi.k)
            heatindex=convertfbunits(hi.k,  convertunittype('temperature', units))

            
          # calculate feels_like
          if tempF != '---' and  humidity100 != '---' and  windmph != '---':
            fl = feels_like(temperature=tempF, humidity= humidity100 , wind_speed=windmph)
            log.info('freeboard:  freeboard_environmental_calculated feels_like  %s:', fl.k)
            feelslike=convertfbunits(fl.k,  convertunittype('temperature', units))

          # calculate Wind Chill
          """
          if tempF != '---' and  windmph != '---':
            wc = wind_chill(temperature=tempF, wind_speed=windmph)
            log.info('freeboard:  freeboard_environmental_calculated wind chill %s:', wc.k)
            windchill=convertfbunits(wc.k,  convertunittype('temperature', units))
          """ 

        except AttributeError as e:
          log.info('freeboard_environmental_calculated: AttributeError in calculated %s:  ' % str(e))
          
        except TypeError as e:
          log.info('freeboard_environmental_calculated: TypeError in calculated %s:  ' % str(e))
          
        except ValueError as e:
          log.info('freeboard_environmental_calculated: ValueError in calculated %s:  ' % str(e))            
          
        except NameError as e:
          log.info('freeboard_environmental_calculated: NameError in calculated %s:  ' % str(e))           

        except IndexError as e:
          log.info('freeboard_environmental_calculated: IndexError in calculated %s:  ' % str(e))
          
        except:
          e = sys.exc_info()[0]
          log.info('freeboard_environmental_calculated: Error in geting calculated ststs %s:  ' % e)



        
        #mydatetimestr = str(point['time'])

        #mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')

      #log.info('freeboard: freeboard returning data values temperature:%s, baro:%s, humidity:%s  ', value1,value2,value3)

      """
      log.info('freeboard: before exosite write:')
      o = onep.OnepV1()

      cik = '5b38da024d8a1f252e575202afb431ef22d3eb66'
      #dataport_alias = 'Device'
      #val_to_write = 'Data'
      dataport_alias = 'air_temperature'
      val_to_write =float(value1)

      #testvar = o.write(cik, {"alias": dataport_alias}, val_to_write,{})
      #log.info('freeboard: fter exosite write:%s', testvar)
      o.write(cik, {"alias": dataport_alias}, val_to_write,{})
      log.info('freeboard: after exosite write:')

       """     

      callback = request.args.get('callback')
      myjsondatetz = mydatetime.strftime("%B %d, %Y %H:%M:%S")
      myjsondatetz = mydatetime.strftime("%d%H%M")

      stationid = devicename[0:4]

      if Interval == '1hour':
        metarstr = ('METAR %s %sZ AUTO %s%sKT %s/%s A%s RMK T%s%s' %  (stationid, myjsondatetz,  wind_dir, wind_speed, temperature, dewpoint, atmospheric_pressure, temperature1hr, dewpoint1hr))
        
      else:
        metarstr = ('METAR %s %sZ AUTO %s%sKT %s/%s A%s' %  (stationid, myjsondatetz,  wind_dir, wind_speed, temperature, dewpoint, atmospheric_pressure))
        
      return metarstr


    except AttributeError as e:
      #log.info('inFluxDB_GPS: AttributeError in freeboard_environmental %s:  ', SERIES_KEY1)
      #e = sys.exc_info()[0]

      log.info('freeboard_environmental: AttributeError in freeboard_environmental %s:  ' % str(e))
      
    except TypeError as e:
      l#og.info('inFluxDB_GPS: TypeError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
      #e = sys.exc_info()[0]

      log.info('inFluxDB_GPS: TypeError in freeboard_environmental %s:  ' % str(e))
      
    except ValueError as e:
      log.info('freeboard_environmental: ValueError in freeboard_environmental point %s:  ', point)
      #e = sys.exc_info()[0]

      log.info('freeboard_environmental: ValueError in freeboard_environmental point%s:  ' % str(e))            
      
    except NameError as e:
      #log.info('inFluxDB_GPS: NameError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
      #e = sys.exc_info()[0]
      log.info('freeboard_environmental: NameError in freeboard_environmental %s:  ' % str(e))           

    except IndexError as e:
      log.info('freeboard_environmental: IndexError in freeboard_environmental point %s:  ', point)
      #e = sys.exc_info()[0]
      log.info('freeboard_environmental: IndexError in freeboard_environmental %s:  ' % str(e))
      
    except pyonep.exceptions.JsonRPCRequestException as ex:
        print('JsonRPCRequestException: {0}'.format(ex))
        
    except pyonep.exceptions.JsonRPCResponseException as ex:
        print('JsonRPCResponseException: {0}'.format(ex))
        
    except pyonep.exceptions.OnePlatformException as ex:
        print('OnePlatformException: {0}'.format(ex))
       
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error',  update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })



def degToCompass(num):
    val=int((num/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return arr[(val % 16)]


def wind_deg_to_compass(deg):
  if    deg >= 0.0 and deg < 11.25: return 'NNE'
  elif deg >=  11.25 and deg <  33.75: return 'NNE'
  elif deg >=  33.75 and deg <  56.25: return 'NE'
  elif deg >=  56.25 and deg <  78.75: return 'ENE'
  elif deg >=  78.75 and deg < 101.25: return 'E'
  elif deg >= 101.25 and deg < 123.75: return 'ESE'
  elif deg >= 123.75 and deg < 146.25: return 'SE'
  elif deg >= 146.25 and deg < 168.75: return 'SSE'
  elif deg >= 168.75 and deg < 191.25: return 'S'
  elif deg >= 191.25 and deg < 213.75: return 'SSW'
  elif deg >= 213.75 and deg < 236.25: return 'SW'
  elif deg >= 236.25 and deg < 258.75: return 'WSW'
  elif deg >= 258.75 and deg < 281.25: return 'W'
  elif deg >= 281.25 and deg < 303.75: return 'WNW'
  elif deg >= 303.75 and deg < 326.25: return 'NW'
  elif deg >= 326.25 and deg < 348.75: return 'NNW'
  elif deg >= 348.75 and deg < 359.99: return 'N'
  else: return ''

@app.route('/helmsmart_environmental_baroncsv')
@cross_origin()
def helmsmart_environmental_baroncsv():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"1min")
    Instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    env_type = request.args.get('type',"outside")
    mytimezone = request.args.get('timezone',"UTC")
    units= request.args.get('units',"US")
    mode  = request.args.get('mode',"median")
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]


    strvalue = ""
    value1 = '---'
    value2 = '---'
    value3 = '---'
    value4 = '---'

    temperature=[]
    atmospheric_pressure=[]
    humidity=[]
    wind_speed=[]
    
    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")        

    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })

    devicename = getedevicename(deviceapikey)
    
    log.info("freeboard devicename %s", devicename)

    if devicename == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'devicename error' })




    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)
    
    #serieskeys={'deviceid'=deviceid, 'sensor'='environmental_data', 'instance'='0', 'type'='Outside_Temperature'}

    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    if env_type == "inside":
      serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Inside Temperature' OR type='Inside Humidity')"

    elif env_type == "inside mesh":
      serieskeys= serieskeys +  " sensor='environmental_data' AND instance='" + Instance + "' "

      
    elif env_type == "sea":
      serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Sea Temperature' OR type='Inside Humidity')"

      
    else:
      #serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Outside Temperature' OR type='Outside Humidity')"
      serieskeys= serieskeys +  " (sensor='wind_data' OR sensor='environmental_data') AND instance='0' AND (type='Apparent Wind'  OR type='Outside Temperature' OR type='Outside Humidity')"




      
    #serieskeys= serieskeys +  " sensor='environmental_data'  AND type='Outside_Temperature'"
    #serieskeys= serieskeys +  " sensor='environmental_data'  "
    
    Key2="deviceid:001EC010AD69.sensor:environmental_data.source:0.instance:0.type:Outside_Temperature.parameter:humidity.HelmSmart"
    Key3="deviceid:001EC010AD69.sensor:environmental_data.source:0.instance:0.type:Outside_Temperature.parameter:atmospheric_pressure.HelmSmart"



    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)



    if serieskeys.find("*") > 0:
        serieskeys = serieskeys.replace("*", ".*")

    if mode == "median":
        query = ('select  median(temperature) AS temperature, median(atmospheric_pressure) AS  atmospheric_pressure, median(humidity) AS humidity , median(altitude) AS altitude, median(wind_speed) AS  wind_speed , median(wind_direction) AS  wind_direction from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

    elif mode == "max":
        query = ('select  max(temperature) AS temperature, max(atmospheric_pressure) AS  atmospheric_pressure, max(humidity) AS humidity, max(altitude) AS altitude, max(wind_speed) AS  wind_speed , max(wind_direction) AS  wind_direction from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

    elif mode == "min":
        query = ('select  min(temperature) AS temperature, min(atmospheric_pressure) AS  atmospheric_pressure, min(humidity) AS humidity, min(altitude) AS altitude, min(wind_speed) AS  wind_speed , min(wind_direction) AS  wind_direction from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

        
    else:
      
      query = ('select  mean(temperature) AS temperature, mean(atmospheric_pressure) AS  atmospheric_pressure, mean(humidity) AS humidity, mean(altitude) AS altitude, mean(wind_speed) AS  wind_speed , mean(wind_direction) AS  wind_direction from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
 

    """
    if serieskeys.find("*") > 0:
        serieskeys = serieskeys.replace("*", ".*")

        query = ('select  median(temperature) AS temperature, median(atmospheric_pressure) AS  atmospheric_pressure, median(humidity) AS humidity from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
    else:
      
      query = ('select  median(temperature) AS temperature, median(atmospheric_pressure) AS  atmospheric_pressure, median(humidity) AS humidity from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
 
    """    

    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))


            
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', response)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        pass

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing', 'update':'False','temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity))})     
      

    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing', 'update':'False','temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity))})     

    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)
    
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'
      value5 = '---'
      value6 = '---'
      value7 = '---'
      temperature=""
      atmospheric_pressure=""
      atmospheric_pressure_sea=""
      humidity=""
      altitude=""
      windchill=""
      wind_speed=""
      wind_dir=""
      wind_gust=""
      heatindex=""
      dewpoint=""
      feelslike=""
      rain=""
      temphigh=""
      templow=""

      

      
      ts =startepoch*1000


      
      points = list(response.get_points())

      log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'
        value5 = '---'
        value6 = '---'
        value7 = '---'
        tempF='---'
        tempC='---'
        humidity100='---'
        windmph='---'
        winddir='---'
      
        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)
          
        if point['temperature'] is not None: 
          temperature = convertfbunits(point['temperature'],  0)   
          temperature1hr = str(temperature * 10 ).zfill(4)
          #temperature = str(temperature).zfill(2)

          tempF=convertfbunits(point['temperature'],  0)
          tempC=convertfbunits(point['temperature'],  1)          

          
        if point['atmospheric_pressure'] is not None:         
          atmospheric_pressure = ((convertfbunits(point['atmospheric_pressure'], convertunittype('baro_pressure', units))) )
          #atmospheric_pressure = str(atmospheric_pressure).zfill(4)
                    
        if point['humidity'] is not None:         
          humidity = convertfbunits(point['humidity'], 26)
          humidity100 = convertfbunits(point['humidity'], 26)


                    
        if point['altitude'] is not None:         
          altitude = convertfbunits(point['altitude'], 32)


        if point['atmospheric_pressure'] is not None and point['altitude'] is not None:
          #get pressure in KPa
          value2 = convertfbunits(point['atmospheric_pressure'], 9)
          #get altitde in feet
          value4 = convertfbunits(point['altitude'], 32)
          # get adjustment for altitude in KPa
          value5 = getAtmosphericCompensation(value4)
          #add offset if any in KPa
          atmospheric_pressure_sea = int((convertfbunits(value2 + value5, convertunittype('baro_pressure', units))) )
          
   
 

        if point['wind_speed'] is not None:         
          wind_speed = convertfbunits(point['wind_speed'], 4)
          windmph = int(convertfbunits(point['wind_speed'], 5))
          #wind_speed =str(wind_speed).zfill(2)
       

        if point['wind_direction'] is not None:         
          wind_dir = int(convertfbunits(point['wind_direction'], 16))
          #wind_dir = str(degToCompass(wind_dir))
          wind_dir = str(wind_deg_to_compass(wind_dir))
          #wind_dir =str(wind_dir).zfill(3)

        try:

          # calculate dew_point
          if tempC != '---' and  humidity100 != '---':
            #dp = dew_point(temperature=tempF, humidity=humidity100)
            dp = dew_point(temperature=tempC, humidity=humidity100)
            log.info('freeboard:  freeboard_environmental_calculated dew_point  %s:', dp.k)
            dewpoint=int(convertfbunits(dp.k, 0))
            dewpoint1hr = str(dewpoint * 10).zfill(4)
            dewpoint = str(dewpoint).zfill(2)


            
          # calculate heat_index
          if tempF != '---' and  humidity100 != '---':        
            hi= heat_index(temperature=tempF, humidity=humidity100)
            log.info('freeboard:  freeboard_environmental_calculated heat_index %s:', hi.k)
            heatindex=convertfbunits(hi.k,  0)

            
          # calculate feels_like
          if tempF != '---' and  humidity100 != '---' and  windmph != '---':
            fl = feels_like(temperature=tempF, humidity= humidity100 , wind_speed=windmph)
            log.info('freeboard:  freeboard_environmental_calculated feels_like  %s:', fl.k)
            #feelslike=convertfbunits(fl.k,  convertunittype('temperature', units))
            feelslike=convertfbunits(fl.k,  0)

          # calculate Wind Chill
          """
          if tempF != '---' and  windmph != '---':
            if temperature < 50 and wind_speed > 3:
              wc = wind_chill(temperature=tempF, wind_speed=windmph)
              log.info('freeboard:  freeboard_environmental_calculated wind chill %s:', wc.k)
              windchill=convertfbunits(wc.k,  convertunittype('temperature', units))
          """ 

        except AttributeError as e:
          log.info('freeboard_environmental_calculated: AttributeError in calculated %s:  ' % str(e))
          
        except TypeError as e:
          log.info('freeboard_environmental_calculated: TypeError in calculated %s:  ' % str(e))
          
        except ValueError as e:
          log.info('freeboard_environmental_calculated: ValueError in calculated %s:  ' % str(e))            
          
        except NameError as e:
          log.info('freeboard_environmental_calculated: NameError in calculated %s:  ' % str(e))           

        except IndexError as e:
          log.info('freeboard_environmental_calculated: IndexError in calculated %s:  ' % str(e))
          
        except:
          e = sys.exc_info()[0]
          log.info('freeboard_environmental_calculated: Error in geting calculated ststs %s:  ' % e)



        
        #mydatetimestr = str(point['time'])

        #mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')

      #log.info('freeboard: freeboard returning data values temperature:%s, baro:%s, humidity:%s  ', value1,value2,value3)

      """
      log.info('freeboard: before exosite write:')
      o = onep.OnepV1()

      cik = '5b38da024d8a1f252e575202afb431ef22d3eb66'
      #dataport_alias = 'Device'
      #val_to_write = 'Data'
      dataport_alias = 'air_temperature'
      val_to_write =float(value1)

      #testvar = o.write(cik, {"alias": dataport_alias}, val_to_write,{})
      #log.info('freeboard: fter exosite write:%s', testvar)
      o.write(cik, {"alias": dataport_alias}, val_to_write,{})
      log.info('freeboard: after exosite write:')

       """     

      callback = request.args.get('callback')
      #myjsondatetz = mydatetime.strftime("%m %d, %Y %H:%M:%S")
      #myjsondatetz = mydatetime.strftime("%d%H%M")

      mycsvdate = mydatetime.strftime("%m/%d/%Y")
      mycsvtime = mydatetime.strftime("%H:%M:%S")
      mycsvtime = mydatetime.strftime("%H:%M")
 
      stationid = devicename[0:4]

      """
      if Interval == '1hour':
        metarstr = ('METAR %s %sZ AUTO %s%sKT %s/%s A%s RMK T%s%s' %  (stationid, myjsondatetz,  wind_dir, wind_speed, temperature, dewpoint, atmospheric_pressure, temperature1hr, dewpoint1hr))
        
      else:
        metarstr = ('METAR %s %sZ AUTO %s%sKT %s/%s A%s' %  (stationid, myjsondatetz,  wind_dir, wind_speed, temperature, dewpoint, atmospheric_pressure))
        
      return metarstr

      """

      #csvstr ="ID,DATE,TIME,TEMP,RH,DEWPT,WINDCHILL,HEATINDEX,WDIR,WSPEED,WGUST,PRESSURE,PRECIP,HIGH,LOW\r\n"


      #csvstr = ('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\r\n' %  (stationid, mycsvdate, mycsvtime , temperature, humidity, dewpoint, windchill, heatindex, wind_dir, wind_speed, wind_gust, atmospheric_pressure, rain, temphigh, templow))

      csvstr = "ALBN,05/27/2020,12:20,76.0,68.0,64.0,76,76,S,7,12,,0.1,79,64"
      
      csvstr = "ALBN,05/27/2020,12:20,76.0,68.0,64.0,76,76,S,7,12,,0.1,79,64"

      csvstr = ('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' %  (stationid, mycsvdate, mycsvtime, temperature, humidity,dewpoint, windchill, heatindex, wind_dir, wind_speed, wind_gust, atmospheric_pressure,rain, temphigh, templow  ))

        
      csvout =  "ID,DATE,TIME,TEMP,RH,DEWPT,WINDCHILL,HEATINDEX,WDIR,WSPEED,WGUST,PRESSURE,PRECIP,HIGH,LOW" + '\r\n' + csvstr + '\r\n'


      return csvout


    except AttributeError as e:
      #log.info('inFluxDB_GPS: AttributeError in freeboard_environmental %s:  ', SERIES_KEY1)
      #e = sys.exc_info()[0]

      log.info('freeboard_environmental: AttributeError in freeboard_environmental %s:  ' % str(e))
      
    except TypeError as e:
      l#og.info('inFluxDB_GPS: TypeError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
      #e = sys.exc_info()[0]

      log.info('inFluxDB_GPS: TypeError in freeboard_environmental %s:  ' % str(e))
      
    except ValueError as e:
      log.info('freeboard_environmental: ValueError in freeboard_environmental point %s:  ', point)
      #e = sys.exc_info()[0]

      log.info('freeboard_environmental: ValueError in freeboard_environmental point%s:  ' % str(e))            
      
    except NameError as e:
      #log.info('inFluxDB_GPS: NameError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
      #e = sys.exc_info()[0]
      log.info('freeboard_environmental: NameError in freeboard_environmental %s:  ' % str(e))           

    except IndexError as e:
      log.info('freeboard_environmental: IndexError in freeboard_environmental point %s:  ', point)
      #e = sys.exc_info()[0]
      log.info('freeboard_environmental: IndexError in freeboard_environmental %s:  ' % str(e))
      
    except pyonep.exceptions.JsonRPCRequestException as ex:
        print('JsonRPCRequestException: {0}'.format(ex))
        
    except pyonep.exceptions.JsonRPCResponseException as ex:
        print('JsonRPCResponseException: {0}'.format(ex))
        
    except pyonep.exceptions.OnePlatformException as ex:
        print('OnePlatformException: {0}'.format(ex))
       
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error',  update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })


@app.route('/helmsmart_environmental_nmea0183')
@cross_origin()
def helmsmart_environmental_nmea0183():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"1min")
    Instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    env_type = request.args.get('type',"outside")
    mytimezone = request.args.get('timezone',"UTC")
    units= request.args.get('units',"US")
    mode  = request.args.get('mode',"median")
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]


    strvalue = ""
    value1 = '---'
    value2 = '---'
    value3 = '---'
    value4 = '---'

    temperature=[]
    atmospheric_pressure=[]
    humidity=[]
    wind_speed=[]
    
    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")        

    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })

    devicename = getedevicename(deviceapikey)
    
    log.info("freeboard devicename %s", devicename)

    if devicename == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'devicename error' })




    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)
    
    #serieskeys={'deviceid'=deviceid, 'sensor'='environmental_data', 'instance'='0', 'type'='Outside_Temperature'}

    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    if env_type == "inside":
      serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Inside Temperature' OR type='Inside Humidity')"

    elif env_type == "inside mesh":
      serieskeys= serieskeys +  " sensor='environmental_data' AND instance='" + Instance + "' "

      
    elif env_type == "sea":
      serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Sea Temperature' OR type='Inside Humidity')"

      
    else:
      #serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Outside Temperature' OR type='Outside Humidity')"
      serieskeys= serieskeys +  " (sensor='wind_data' OR sensor='environmental_data') AND instance='0' AND (type='Apparent Wind'  OR type='Outside Temperature' OR type='Outside Humidity')"




      
    #serieskeys= serieskeys +  " sensor='environmental_data'  AND type='Outside_Temperature'"
    #serieskeys= serieskeys +  " sensor='environmental_data'  "
    
    Key2="deviceid:001EC010AD69.sensor:environmental_data.source:0.instance:0.type:Outside_Temperature.parameter:humidity.HelmSmart"
    Key3="deviceid:001EC010AD69.sensor:environmental_data.source:0.instance:0.type:Outside_Temperature.parameter:atmospheric_pressure.HelmSmart"



    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)



    if serieskeys.find("*") > 0:
        serieskeys = serieskeys.replace("*", ".*")

    if mode == "median":
        query = ('select  median(temperature) AS temperature, median(atmospheric_pressure) AS  atmospheric_pressure, median(humidity) AS humidity , median(altitude) AS altitude, median(wind_speed) AS  wind_speed , median(wind_direction) AS  wind_direction from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

    elif mode == "max":
        query = ('select  max(temperature) AS temperature, max(atmospheric_pressure) AS  atmospheric_pressure, max(humidity) AS humidity, max(altitude) AS altitude, max(wind_speed) AS  wind_speed , max(wind_direction) AS  wind_direction from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

    elif mode == "min":
        query = ('select  min(temperature) AS temperature, min(atmospheric_pressure) AS  atmospheric_pressure, min(humidity) AS humidity, min(altitude) AS altitude, min(wind_speed) AS  wind_speed , min(wind_direction) AS  wind_direction from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

        
    else:
      
      query = ('select  mean(temperature) AS temperature, mean(atmospheric_pressure) AS  atmospheric_pressure, mean(humidity) AS humidity, mean(altitude) AS altitude, mean(wind_speed) AS  wind_speed , mean(wind_direction) AS  wind_direction from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
 

    """
    if serieskeys.find("*") > 0:
        serieskeys = serieskeys.replace("*", ".*")

        query = ('select  median(temperature) AS temperature, median(atmospheric_pressure) AS  atmospheric_pressure, median(humidity) AS humidity from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
    else:
      
      query = ('select  median(temperature) AS temperature, median(atmospheric_pressure) AS  atmospheric_pressure, median(humidity) AS humidity from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
 
    """    

    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))


            
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', response)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        pass

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing', 'update':'False','temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity))})     
      

    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing', 'update':'False','temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity))})     

    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)
    
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'
      value5 = '---'
      value6 = '---'
      value7 = '---'
      temperature=""
      atmospheric_pressure=""
      atmospheric_pressure_sea=""
      humidity=""
      altitude=""
      windchill=""
      wind_speed=""
      wind_dir=""
      wind_gust=""
      heatindex=""
      dewpoint=""
      feelslike=""
      rain=""
      temphigh=""
      templow=""

      

      
      ts =startepoch*1000


      
      points = list(response.get_points())

      log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'
        value5 = '---'
        value6 = '---'
        value7 = '---'
        tempF='---'
        tempC='---'
        humidity100='---'
        windmph='---'
        winddir='---'
      
        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)
          
        if point['temperature'] is not None: 
          temperature = convertfbunits(point['temperature'],  0)   
          temperature1hr = str(temperature * 10 ).zfill(4)
          #temperature = str(temperature).zfill(2)

          tempF=convertfbunits(point['temperature'],  0)
          tempC=convertfbunits(point['temperature'],  1)          

          
        if point['atmospheric_pressure'] is not None:         
          atmospheric_pressure = ((convertfbunits(point['atmospheric_pressure'], convertunittype('baro_pressure', units))) )
          #atmospheric_pressure = str(atmospheric_pressure).zfill(4)
                    
        if point['humidity'] is not None:         
          humidity = convertfbunits(point['humidity'], 26)
          humidity100 = convertfbunits(point['humidity'], 26)


                    
        if point['altitude'] is not None:         
          altitude = convertfbunits(point['altitude'], 32)


        if point['atmospheric_pressure'] is not None and point['altitude'] is not None:
          #get pressure in KPa
          value2 = convertfbunits(point['atmospheric_pressure'], 9)
          #get altitde in feet
          value4 = convertfbunits(point['altitude'], 32)
          # get adjustment for altitude in KPa
          value5 = getAtmosphericCompensation(value4)
          #add offset if any in KPa
          atmospheric_pressure_sea = int((convertfbunits(value2 + value5, convertunittype('baro_pressure', units))) )
          
   
 

        if point['wind_speed'] is not None:         
          wind_speed = convertfbunits(point['wind_speed'], 4)
          windmph = int(convertfbunits(point['wind_speed'], 5))
          #wind_speed =str(wind_speed).zfill(2)
       

        if point['wind_direction'] is not None:         
          wind_dir = int(convertfbunits(point['wind_direction'], 16))
          #wind_dir = str(degToCompass(wind_dir))
          wind_dir = str(wind_deg_to_compass(wind_dir))
          #wind_dir =str(wind_dir).zfill(3)

        try:

          # calculate dew_point
          if tempC != '---' and  humidity100 != '---':
            #dp = dew_point(temperature=tempF, humidity=humidity100)
            dp = dew_point(temperature=tempC, humidity=humidity100)
            log.info('freeboard:  freeboard_environmental_calculated dew_point  %s:', dp.k)
            dewpoint=int(convertfbunits(dp.k, 0))
            dewpoint1hr = str(dewpoint * 10).zfill(4)
            dewpoint = str(dewpoint).zfill(2)


            
          # calculate heat_index
          if tempF != '---' and  humidity100 != '---':        
            hi= heat_index(temperature=tempF, humidity=humidity100)
            log.info('freeboard:  freeboard_environmental_calculated heat_index %s:', hi.k)
            heatindex=convertfbunits(hi.k,  0)

            
          # calculate feels_like
          if tempF != '---' and  humidity100 != '---' and  windmph != '---':
            fl = feels_like(temperature=tempF, humidity= humidity100 , wind_speed=windmph)
            log.info('freeboard:  freeboard_environmental_calculated feels_like  %s:', fl.k)
            #feelslike=convertfbunits(fl.k,  convertunittype('temperature', units))
            feelslike=convertfbunits(fl.k,  0)

          # calculate Wind Chill
          """
          if tempF != '---' and  windmph != '---':
            if temperature < 50 and wind_speed > 3:
              wc = wind_chill(temperature=tempF, wind_speed=windmph)
              log.info('freeboard:  freeboard_environmental_calculated wind chill %s:', wc.k)
              windchill=convertfbunits(wc.k,  convertunittype('temperature', units))
          """ 

        except AttributeError as e:
          log.info('freeboard_environmental_calculated: AttributeError in calculated %s:  ' % str(e))
          
        except TypeError as e:
          log.info('freeboard_environmental_calculated: TypeError in calculated %s:  ' % str(e))
          
        except ValueError as e:
          log.info('freeboard_environmental_calculated: ValueError in calculated %s:  ' % str(e))            
          
        except NameError as e:
          log.info('freeboard_environmental_calculated: NameError in calculated %s:  ' % str(e))           

        except IndexError as e:
          log.info('freeboard_environmental_calculated: IndexError in calculated %s:  ' % str(e))
          
        except:
          e = sys.exc_info()[0]
          log.info('freeboard_environmental_calculated: Error in geting calculated ststs %s:  ' % e)



        
        #mydatetimestr = str(point['time'])

        #mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')

      #log.info('freeboard: freeboard returning data values temperature:%s, baro:%s, humidity:%s  ', value1,value2,value3)

      """
      log.info('freeboard: before exosite write:')
      o = onep.OnepV1()

      cik = '5b38da024d8a1f252e575202afb431ef22d3eb66'
      #dataport_alias = 'Device'
      #val_to_write = 'Data'
      dataport_alias = 'air_temperature'
      val_to_write =float(value1)

      #testvar = o.write(cik, {"alias": dataport_alias}, val_to_write,{})
      #log.info('freeboard: fter exosite write:%s', testvar)
      o.write(cik, {"alias": dataport_alias}, val_to_write,{})
      log.info('freeboard: after exosite write:')

       """     

      callback = request.args.get('callback')
      #myjsondatetz = mydatetime.strftime("%m %d, %Y %H:%M:%S")
      #myjsondatetz = mydatetime.strftime("%d%H%M")

      mycsvdate = mydatetime.strftime("%m/%d/%Y")
      mycsvtime = mydatetime.strftime("%H:%M:%S")
      mycsvtime = mydatetime.strftime("%H:%M")
 
      stationid = devicename[0:4]

      """
      if Interval == '1hour':
        metarstr = ('METAR %s %sZ AUTO %s%sKT %s/%s A%s RMK T%s%s' %  (stationid, myjsondatetz,  wind_dir, wind_speed, temperature, dewpoint, atmospheric_pressure, temperature1hr, dewpoint1hr))
        
      else:
        metarstr = ('METAR %s %sZ AUTO %s%sKT %s/%s A%s' %  (stationid, myjsondatetz,  wind_dir, wind_speed, temperature, dewpoint, atmospheric_pressure))
        
      return metarstr

      """

      #csvstr ="ID,DATE,TIME,TEMP,RH,DEWPT,WINDCHILL,HEATINDEX,WDIR,WSPEED,WGUST,PRESSURE,PRECIP,HIGH,LOW\r\n"


      #csvstr = ('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\r\n' %  (stationid, mycsvdate, mycsvtime , temperature, humidity, dewpoint, windchill, heatindex, wind_dir, wind_speed, wind_gust, atmospheric_pressure, rain, temphigh, templow))

      #csvstr = "ALBN,05/27/2020,12:20,76.0,68.0,64.0,76,76,S,7,12,,0.1,79,64"
      
      #csvstr = "ALBN,05/27/2020,12:20,76.0,68.0,64.0,76,76,S,7,12,,0.1,79,64"

      csvstr = ('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' %  (stationid, mycsvdate, mycsvtime, temperature, humidity,dewpoint, windchill, heatindex, wind_dir, wind_speed, wind_gust, atmospheric_pressure,rain, temphigh, templow  ))

      checksum =0

      for c in csvstr:
        checksum ^= ord(c)

      #checksumstr = format(checksum, "02X")
      checksumstr = ('%02X' % checksum)
      
      #csvout =  "ID,DATE,TIME,TEMP,RH,DEWPT,WINDCHILL,HEATINDEX,WDIR,WSPEED,WGUST,PRESSURE,PRECIP,HIGH,LOW" + '\r\n' + csvstr + '\r\n'
      csvout =  "$"  + csvstr + '*' + checksumstr + '\r\n'


      return csvout


    except AttributeError as e:
      #log.info('inFluxDB_GPS: AttributeError in freeboard_environmental %s:  ', SERIES_KEY1)
      #e = sys.exc_info()[0]

      log.info('freeboard_environmental: AttributeError in freeboard_environmental %s:  ' % str(e))
      
    except TypeError as e:
      l#og.info('inFluxDB_GPS: TypeError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
      #e = sys.exc_info()[0]

      log.info('inFluxDB_GPS: TypeError in freeboard_environmental %s:  ' % str(e))
      
    except ValueError as e:
      log.info('freeboard_environmental: ValueError in freeboard_environmental point %s:  ', point)
      #e = sys.exc_info()[0]

      log.info('freeboard_environmental: ValueError in freeboard_environmental point%s:  ' % str(e))            
      
    except NameError as e:
      #log.info('inFluxDB_GPS: NameError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
      #e = sys.exc_info()[0]
      log.info('freeboard_environmental: NameError in freeboard_environmental %s:  ' % str(e))           

    except IndexError as e:
      log.info('freeboard_environmental: IndexError in freeboard_environmental point %s:  ', point)
      #e = sys.exc_info()[0]
      log.info('freeboard_environmental: IndexError in freeboard_environmental %s:  ' % str(e))
      
    except pyonep.exceptions.JsonRPCRequestException as ex:
        print('JsonRPCRequestException: {0}'.format(ex))
        
    except pyonep.exceptions.JsonRPCResponseException as ex:
        print('JsonRPCResponseException: {0}'.format(ex))
        
    except pyonep.exceptions.OnePlatformException as ex:
        print('OnePlatformException: {0}'.format(ex))
       
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error',  update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })




@app.route('/helmsmart_environmental_baroncsv_text')
@cross_origin()
def helmsmart_environmental_baroncsv_text():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"1min")
    Instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    env_type = request.args.get('type',"outside")
    mytimezone = request.args.get('timezone',"UTC")
    units= request.args.get('units',"US")
    mode  = request.args.get('mode',"median")
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]


    strvalue = ""
    value1 = '---'
    value2 = '---'
    value3 = '---'
    value4 = '---'

    temperature=[]
    atmospheric_pressure=[]
    humidity=[]
    wind_speed=[]
    
    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")        

    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })

    devicename = getedevicename(deviceapikey)
    
    log.info("freeboard devicename %s", devicename)

    if devicename == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'devicename error' })




    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)
    
    #serieskeys={'deviceid'=deviceid, 'sensor'='environmental_data', 'instance'='0', 'type'='Outside_Temperature'}

    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    if env_type == "inside":
      serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Inside Temperature' OR type='Inside Humidity')"

    elif env_type == "inside mesh":
      serieskeys= serieskeys +  " sensor='environmental_data' AND instance='" + Instance + "' "

      
    elif env_type == "sea":
      serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Sea Temperature' OR type='Inside Humidity')"

      
    else:
      #serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Outside Temperature' OR type='Outside Humidity')"
      serieskeys= serieskeys +  " (sensor='wind_data' OR sensor='environmental_data') AND instance='0' AND (type='Apparent Wind'  OR type='Outside Temperature' OR type='Outside Humidity')"




      
    #serieskeys= serieskeys +  " sensor='environmental_data'  AND type='Outside_Temperature'"
    #serieskeys= serieskeys +  " sensor='environmental_data'  "
    
    Key2="deviceid:001EC010AD69.sensor:environmental_data.source:0.instance:0.type:Outside_Temperature.parameter:humidity.HelmSmart"
    Key3="deviceid:001EC010AD69.sensor:environmental_data.source:0.instance:0.type:Outside_Temperature.parameter:atmospheric_pressure.HelmSmart"



    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)



    if serieskeys.find("*") > 0:
        serieskeys = serieskeys.replace("*", ".*")

    if mode == "median":
        query = ('select  median(temperature) AS temperature, median(atmospheric_pressure) AS  atmospheric_pressure, median(humidity) AS humidity , median(altitude) AS altitude, median(wind_speed) AS  wind_speed , median(wind_direction) AS  wind_direction from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

    elif mode == "max":
        query = ('select  max(temperature) AS temperature, max(atmospheric_pressure) AS  atmospheric_pressure, max(humidity) AS humidity, max(altitude) AS altitude, max(wind_speed) AS  wind_speed , max(wind_direction) AS  wind_direction from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

    elif mode == "min":
        query = ('select  min(temperature) AS temperature, min(atmospheric_pressure) AS  atmospheric_pressure, min(humidity) AS humidity, min(altitude) AS altitude, min(wind_speed) AS  wind_speed , min(wind_direction) AS  wind_direction from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

        
    else:
      
      query = ('select  mean(temperature) AS temperature, mean(atmospheric_pressure) AS  atmospheric_pressure, mean(humidity) AS humidity, mean(altitude) AS altitude, mean(wind_speed) AS  wind_speed , mean(wind_direction) AS  wind_direction from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
 

    """
    if serieskeys.find("*") > 0:
        serieskeys = serieskeys.replace("*", ".*")

        query = ('select  median(temperature) AS temperature, median(atmospheric_pressure) AS  atmospheric_pressure, median(humidity) AS humidity from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
    else:
      
      query = ('select  median(temperature) AS temperature, median(atmospheric_pressure) AS  atmospheric_pressure, median(humidity) AS humidity from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
 
    """    

    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))


            
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', response)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        pass

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing', 'update':'False','temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity))})     
      

    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing', 'update':'False','temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity))})     

    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)
    
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'
      value5 = '---'
      value6 = '---'
      value7 = '---'
      temperature=""
      atmospheric_pressure=""
      atmospheric_pressure_sea=""
      humidity=""
      altitude=""
      windchill=""
      wind_speed=""
      wind_dir=""
      wind_gust=""
      heatindex=""
      dewpoint=""
      feelslike=""
      rain=""
      temphigh=""
      templow=""

      

      
      ts =startepoch*1000


      
      points = list(response.get_points())

      log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'
        value5 = '---'
        value6 = '---'
        value7 = '---'
        tempF='---'
        tempC='---'
        humidity100='---'
        windmph='---'
        winddir='---'
      
        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)
          
        if point['temperature'] is not None: 
          temperature = convertfbunits(point['temperature'],  0)   
          temperature1hr = str(temperature * 10 ).zfill(4)
          #temperature = str(temperature).zfill(2)

          tempF=convertfbunits(point['temperature'],  0)
          tempC=convertfbunits(point['temperature'],  1)          

          
        if point['atmospheric_pressure'] is not None:         
          atmospheric_pressure = ((convertfbunits(point['atmospheric_pressure'], convertunittype('baro_pressure', units))) )
          #atmospheric_pressure = str(atmospheric_pressure).zfill(4)
                    
        if point['humidity'] is not None:         
          humidity = convertfbunits(point['humidity'], 26)
          humidity100 = convertfbunits(point['humidity'], 26)


                    
        if point['altitude'] is not None:         
          altitude = convertfbunits(point['altitude'], 32)


        if point['atmospheric_pressure'] is not None and point['altitude'] is not None:
          #get pressure in KPa
          value2 = convertfbunits(point['atmospheric_pressure'], 9)
          #get altitde in feet
          value4 = convertfbunits(point['altitude'], 32)
          # get adjustment for altitude in KPa
          value5 = getAtmosphericCompensation(value4)
          #add offset if any in KPa
          atmospheric_pressure_sea = int((convertfbunits(value2 + value5, convertunittype('baro_pressure', units))) )
          
   
 

        if point['wind_speed'] is not None:         
          wind_speed = convertfbunits(point['wind_speed'], 4)
          windmph = int(convertfbunits(point['wind_speed'], 5))
          #wind_speed =str(wind_speed).zfill(2)
       

        if point['wind_direction'] is not None:         
          wind_dir = int(convertfbunits(point['wind_direction'], 16))
          #wind_dir = str(degToCompass(wind_dir))
          wind_dir = str(wind_deg_to_compass(wind_dir))
          #wind_dir =str(wind_dir).zfill(3)

        try:

          # calculate dew_point
          if tempC != '---' and  humidity100 != '---':
            #dp = dew_point(temperature=tempF, humidity=humidity100)
            dp = dew_point(temperature=tempC, humidity=humidity100)
            log.info('freeboard:  freeboard_environmental_calculated dew_point  %s:', dp.k)
            dewpoint=int(convertfbunits(dp.k, 0))
            dewpoint1hr = str(dewpoint * 10).zfill(4)
            dewpoint = str(dewpoint).zfill(2)


            
          # calculate heat_index
          if tempF != '---' and  humidity100 != '---':        
            hi= heat_index(temperature=tempF, humidity=humidity100)
            log.info('freeboard:  freeboard_environmental_calculated heat_index %s:', hi.k)
            heatindex=convertfbunits(hi.k,  0)

            
          # calculate feels_like
          if tempF != '---' and  humidity100 != '---' and  windmph != '---':
            fl = feels_like(temperature=tempF, humidity= humidity100 , wind_speed=windmph)
            log.info('freeboard:  freeboard_environmental_calculated feels_like  %s:', fl.k)
            #feelslike=convertfbunits(fl.k,  convertunittype('temperature', units))
            feelslike=convertfbunits(fl.k,  0)

          # calculate Wind Chill
          """
          if tempF != '---' and  windmph != '---':
            if temperature < 50 and wind_speed > 3:
              wc = wind_chill(temperature=tempF, wind_speed=windmph)
              log.info('freeboard:  freeboard_environmental_calculated wind chill %s:', wc.k)
              windchill=convertfbunits(wc.k,  convertunittype('temperature', units))
          """ 

        except AttributeError as e:
          log.info('freeboard_environmental_calculated: AttributeError in calculated %s:  ' % str(e))
          
        except TypeError as e:
          log.info('freeboard_environmental_calculated: TypeError in calculated %s:  ' % str(e))
          
        except ValueError as e:
          log.info('freeboard_environmental_calculated: ValueError in calculated %s:  ' % str(e))            
          
        except NameError as e:
          log.info('freeboard_environmental_calculated: NameError in calculated %s:  ' % str(e))           

        except IndexError as e:
          log.info('freeboard_environmental_calculated: IndexError in calculated %s:  ' % str(e))
          
        except:
          e = sys.exc_info()[0]
          log.info('freeboard_environmental_calculated: Error in geting calculated ststs %s:  ' % e)



        
        #mydatetimestr = str(point['time'])

        #mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')

      #log.info('freeboard: freeboard returning data values temperature:%s, baro:%s, humidity:%s  ', value1,value2,value3)

      """
      log.info('freeboard: before exosite write:')
      o = onep.OnepV1()

      cik = '5b38da024d8a1f252e575202afb431ef22d3eb66'
      #dataport_alias = 'Device'
      #val_to_write = 'Data'
      dataport_alias = 'air_temperature'
      val_to_write =float(value1)

      #testvar = o.write(cik, {"alias": dataport_alias}, val_to_write,{})
      #log.info('freeboard: fter exosite write:%s', testvar)
      o.write(cik, {"alias": dataport_alias}, val_to_write,{})
      log.info('freeboard: after exosite write:')

       """     

      callback = request.args.get('callback')
      #myjsondatetz = mydatetime.strftime("%m %d, %Y %H:%M:%S")
      #myjsondatetz = mydatetime.strftime("%d%H%M")

      mycsvdate = mydatetime.strftime("%m/%d/%Y")
      mycsvtime = mydatetime.strftime("%H:%M:%S")
      mycsvtime = mydatetime.strftime("%H:%M")
 
      stationid = devicename[0:4]

      """
      if Interval == '1hour':
        metarstr = ('METAR %s %sZ AUTO %s%sKT %s/%s A%s RMK T%s%s' %  (stationid, myjsondatetz,  wind_dir, wind_speed, temperature, dewpoint, atmospheric_pressure, temperature1hr, dewpoint1hr))
        
      else:
        metarstr = ('METAR %s %sZ AUTO %s%sKT %s/%s A%s' %  (stationid, myjsondatetz,  wind_dir, wind_speed, temperature, dewpoint, atmospheric_pressure))
        
      return metarstr

      """

      #csvstr ="ID,DATE,TIME,TEMP,RH,DEWPT,WINDCHILL,HEATINDEX,WDIR,WSPEED,WGUST,PRESSURE,PRECIP,HIGH,LOW\r\n"


      csvstr = ('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\r\n' %  (stationid, mycsvdate, mycsvtime , temperature, humidity, dewpoint, windchill, heatindex, wind_dir, wind_speed, wind_gust, atmospheric_pressure, rain, temphigh, templow))
        
      csvout =  "ID,DATE,TIME,TEMP,RH,DEWPT,WINDCHILL,HEATINDEX,WDIR,WSPEED,WGUST,PRESSURE,PRECIP,HIGH,LOW" + '\r\n' + csvstr + '\r\n'

      response = make_response(csvout)
      response.headers['Content-Type'] = 'text/csv'
      return response


    except AttributeError as e:
      #log.info('inFluxDB_GPS: AttributeError in freeboard_environmental %s:  ', SERIES_KEY1)
      #e = sys.exc_info()[0]

      log.info('freeboard_environmental: AttributeError in freeboard_environmental %s:  ' % str(e))
      
    except TypeError as e:
      l#og.info('inFluxDB_GPS: TypeError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
      #e = sys.exc_info()[0]

      log.info('inFluxDB_GPS: TypeError in freeboard_environmental %s:  ' % str(e))
      
    except ValueError as e:
      log.info('freeboard_environmental: ValueError in freeboard_environmental point %s:  ', point)
      #e = sys.exc_info()[0]

      log.info('freeboard_environmental: ValueError in freeboard_environmental point%s:  ' % str(e))            
      
    except NameError as e:
      #log.info('inFluxDB_GPS: NameError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
      #e = sys.exc_info()[0]
      log.info('freeboard_environmental: NameError in freeboard_environmental %s:  ' % str(e))           

    except IndexError as e:
      log.info('freeboard_environmental: IndexError in freeboard_environmental point %s:  ', point)
      #e = sys.exc_info()[0]
      log.info('freeboard_environmental: IndexError in freeboard_environmental %s:  ' % str(e))
      
    except pyonep.exceptions.JsonRPCRequestException as ex:
        print('JsonRPCRequestException: {0}'.format(ex))
        
    except pyonep.exceptions.JsonRPCResponseException as ex:
        print('JsonRPCResponseException: {0}'.format(ex))
        
    except pyonep.exceptions.OnePlatformException as ex:
        print('OnePlatformException: {0}'.format(ex))
       
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error',  update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })





@app.route('/freeboard_weather')
@cross_origin()
def freeboard_weather():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    resolution = request.args.get('resolution',"")
    windtype = request.args.get('type',"true")
    mytimezone = request.args.get('timezone',"UTC")
    units= request.args.get('units',"US")
    mode  = request.args.get('mode',"median")
    
    response = None


    wind_speed=[]
    wind_direction=[]
    temperature=[]
    atmospheric_pressure=[]
    atmospheric_pressure_sea=[]
    humidity=[]
    altitude=[]
      
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]

    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")      

    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)

    
    if  windtype =="apparent":
      serieskeys=" deviceid='"
      serieskeys= serieskeys + deviceid + "' AND "
      serieskeys= serieskeys +  " (sensor='wind_data' OR sensor='environmental_data') AND instance='0' AND (type='Apparent Wind'  OR type='Outside Temperature' OR type='Outside Humidity')"
      #serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Outside Temperature' OR type='Outside Humidity')"

    else  :
      serieskeys=" deviceid='"
      serieskeys= serieskeys + deviceid + "' AND "
      #serieskeys= serieskeys +  " sensor='wind_data' AND instance='0' AND type='TWIND True North' "
      serieskeys= serieskeys +  " (sensor='wind_data' OR sensor='environmental_data') AND instance='0' AND (type='TWIND True North' OR type='Outside Temperature' OR type='Outside Humidity')"
  
    #serieskeys= serieskeys +  " sensor='wind_data'  "


    #log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    #log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

  
    if serieskeys.find("*") > 0:
        serieskeys = serieskeys.replace("*", ".*")

    if mode == "median":
      
      query = ('select  median(wind_direction) AS wind_direction, median(wind_speed) AS  wind_speed, median(temperature) AS temperature, median(atmospheric_pressure) AS  atmospheric_pressure, median(humidity) AS humidity , median(altitude) AS altitude from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)  ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
      
    elif mode == "max":
      
      query = ('select  max(wind_direction) AS wind_direction, max(wind_speed) AS  wind_speed, max(temperature) AS temperature, max(atmospheric_pressure) AS  atmospheric_pressure, max(humidity) AS humidity , max(altitude) AS altitude  from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)  ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

      
    elif mode == "min":
      
      query = ('select  min(wind_direction) AS wind_direction, min(wind_speed) AS  wind_speed, min(temperature) AS temperature, min(atmospheric_pressure) AS  atmospheric_pressure, min(humidity) AS humidity , min(altitude) AS altitude  from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)  ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)      
      
    else:       
      query = ('select  mean(wind_direction) AS wind_direction, mean(wind_speed) AS  wind_speed, mean(temperature) AS temperature, mean(atmospheric_pressure) AS  atmospheric_pressure, mean(humidity) AS humidity , mean(altitude) AS altitude  from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)  ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)


    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))


            
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', response)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        pass

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        
        if  windtype =="apparent":
          return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing','apparentwindspeed':list(reversed(wind_speed)), 'apparentwinddirection':list(reversed(wind_direction)), 'temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity)), 'altitude':list(reversed(altitude)), 'atmospheric_pressure_sea':list(reversed(atmospheric_pressure_sea))})     
        else:
          return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing','truewindspeed':list(reversed(wind_speed)), 'truewinddir':list(reversed(wind_direction)), 'temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity)), 'altitude':list(reversed(altitude)), 'atmospheric_pressure_sea':list(reversed(atmospheric_pressure_sea))})     


    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
      
        if  windtype =="apparent":
          return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing','apparentwindspeed':list(reversed(wind_speed)), 'apparentwinddirection':list(reversed(wind_direction)), 'temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity)), 'altitude':list(reversed(altitude)), 'atmospheric_pressure_sea':list(reversed(atmospheric_pressure_sea))})     
        else:
          return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing','truewindspeed':list(reversed(wind_speed)), 'truewinddir':list(reversed(wind_direction)), 'temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity)), 'altitude':list(reversed(altitude)), 'atmospheric_pressure_sea':list(reversed(atmospheric_pressure_sea))})     
   

      

    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)


    #keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)
    
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'

      wind_speed=[]
      wind_direction=[]

      ts =startepoch*1000
 
      points = list(response.get_points())

      #log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'
        value5 = '---'
        value6 = '---'
        value7 = '---'
        value8 = '---'
        
        
        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)

        if point['wind_speed'] is not None:       
          value1 = convertfbunits(point['wind_speed'],  convertunittype('speed', units))
        wind_speed.append({'epoch':ts, 'value':value1})
          
        if point['wind_direction'] is not None:       
          value2 = convertfbunits(point['wind_direction'], 16)
        wind_direction.append({'epoch':ts, 'value':value2})

        if point['temperature'] is not None: 
          value3 = convertfbunits(point['temperature'],  convertunittype('temperature', units))
        temperature.append({'epoch':ts, 'value':value3})
          
        if point['atmospheric_pressure'] is not None:         
          value4 = convertfbunits(point['atmospheric_pressure'], convertunittype('baro_pressure', units))
        atmospheric_pressure.append({'epoch':ts, 'value':value4})
                    
        if point['humidity'] is not None:         
          value5 = convertfbunits(point['humidity'], 26)
        humidity.append({'epoch':ts, 'value':value5})

                    
        if point['altitude'] is not None:         
          value6 = convertfbunits(point['altitude'], 32)
        altitude.append({'epoch':ts, 'value':value6})

        if point['atmospheric_pressure'] is not None and point['altitude'] is not None:
          #get pressure in KPa
          value4 = convertfbunits(point['atmospheric_pressure'], 9)
          #get altitde in feet
          value6 = convertfbunits(point['altitude'], 32)
          # get adjustment for altitude in KPa
          value7 = getAtmosphericCompensation(value6)
          #add offset if any in KPa
          value7 = convertfbunits(value4 + value7, convertunittype('baro_pressure', units))
          
        atmospheric_pressure_sea.append({'epoch':ts, 'value':value7})    



        
       

      callback = request.args.get('callback')
      myjsondate = mydatetimetz.strftime("%B %d, %Y %H:%M:%S")

      
      if  windtype =="apparent":
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'status':'success','apparentwindspeed':list(reversed(wind_speed)), 'apparentwinddirection':list(reversed(wind_direction)),'temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity)), 'altitude':list(reversed(altitude)), 'atmospheric_pressure_sea':list(reversed(atmospheric_pressure_sea))})     
      else:
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'status':'success','truewindspeed':list(reversed(wind_speed)), 'truewinddir':list(reversed(wind_direction)),'temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity)), 'altitude':list(reversed(altitude)), 'atmospheric_pressure_sea':list(reversed(atmospheric_pressure_sea))})     
   

      

     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error',  update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })


@app.route('/freeboard_rain_gauge')
@cross_origin()
def freeboard_rain_gauge():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    resolution = request.args.get('resolution',"")
    windtype = request.args.get('type',"true")
    mytimezone = request.args.get('timezone',"UTC")
    units= request.args.get('units',"US")
    mode  = request.args.get('mode',"median")
    
    response = None


    accumulation=[]
    duration=[]
    rate=[]
    peak=[]

    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]
    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")      

    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)

    

    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " sensor='rain_gauge' "
  
    #serieskeys= serieskeys +  " sensor='wind_data'  "


    #log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    #log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

  
    if serieskeys.find("*") > 0:
        serieskeys = serieskeys.replace("*", ".*")

    if mode == "median":
      
      query = ('select  median(accumulation) AS accumulation, median("rainduration") AS  "duration", median(rate) AS rate, median(peak) AS  peak from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)  ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
      
    elif mode == "max":
      
      query = ('select  max(accumulation) AS accumulation, max("rainduration") AS  "duration", max(rate) AS rate, max(peak) AS  peak  from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)  ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

      
    elif mode == "min":
      
      query = ('select  min(accumulation) AS accumulation, min("rainduration") AS  "duration", min(rate) AS rate, min(peak) AS  peak from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)  ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)      
      
    else:       
      query = ('select  mean(accumulation) AS accumulation, mean("rainduration") AS  "duration", mean(rate) AS rate, mean(peak) AS  peak  from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)  ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)


    log.info("freeboard_rain_gauge data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard_rain_gauge: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard_rain_gauge: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard_rain_gauge: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard_rain_gauge: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard_rain_gauge: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard_rain_gauge: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard_rain_gauge: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard_rain_gauge: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_rain_gauge: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_rain_gauge: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_rain_gauge: Exception Error in InfluxDB  %s:  ' % str(e))


            
    except:
        log.info('freeboard_rain_gauge: Error in InfluxDB mydata append %s:', response)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        pass

    if response is None:
        log.info('freeboard_rain_gauge: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        

        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing','accumulation':list(reversed(accumulation)), 'duration':list(reversed(duration)), 'rate':list(reversed(rate)), 'peak':list(reversed(peak))})     


    if not response:
        log.info('freeboard_rain_gauge: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
      

        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing','accumulation':list(reversed(accumulation)), 'duration':list(reversed(duration)), 'rate':list(reversed(rate)), 'peak':list(reversed(peak))})     
   

      

    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)


    #keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)
    
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'

      accumulation=[]
      duration=[]
      duration_min=[]
      rate=[]
      peak=[]


      ts =startepoch*1000
 
      points = list(response.get_points())

      log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'
        value5 = '---'
        value6 = '---'
        value7 = '---'
        value8 = '---'
        
        
        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_rain_gauge:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            log.info('freeboard_rain_gauge:: ts %s:  ' % ts)

        if point['accumulation'] is not None:       
          value1 = convertfbunits((float(point['accumulation'])),  convertunittype('rain', units))
        accumulation.append({'epoch':ts, 'value':value1})


        # duration is in hours so scale to seconds = 1/(60*60 )
        #if point['rainduration'] is not None:  
        if point['duration'] is not None:       
          value2 = convertfbunits((point['duration'] * 3600), 37)
        duration.append({'epoch':ts, 'value':value2})

        # duration is in hours so scale to min
        if point['duration'] is not None:       
          #value5 = convertfbunits(point['duration'], 37)
          value5 = float("{0:.2f}".format(point['duration'] * 60))  
        duration_min.append({'epoch':ts, 'value':value5})

        if point['rate'] is not None: 
          value3 = convertfbunits((float(point['rate'])),  convertunittype('rain', units))
        rate.append({'epoch':ts, 'value':value3})
          
        if point['peak'] is not None:         
          value4 = convertfbunits((float(point['peak'])), convertunittype('rain', units))
        peak.append({'epoch':ts, 'value':value4})
                    
 

        
       

      callback = request.args.get('callback')
      myjsondate = mydatetimetz.strftime("%B %d, %Y %H:%M:%S")

      

      return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'status':'success','accumulation':list(reversed(accumulation)), 'duration':list(reversed(duration)), 'duration_minutes':list(reversed(duration_min)), 'rate':list(reversed(rate)), 'peak':list(reversed(peak))})     
   

      
    except KeyError as e:
        log.info('freeboard_rain_gauge: Key Error in InfluxDB mydata append %s:  ', strvalue)
        log.info('freeboard_rain_gauge: Key Error in InfluxDB mydata append %s:  ' % str(e))
     
    
    except:
        log.info('freeboard_rain_gauge: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard_rain_gauge: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error',  update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })






@app.route('/freeboard_rain_wung')
@cross_origin()
def freeboard_rain_wung():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')

    wunstation = request.args.get('wunstation','')
    wunpassword = request.args.get('wunpw','')
    
    Interval = request.args.get('interval',"5min")
    resolution = request.args.get('resolution',"")
    windtype = request.args.get('type',"true")
    mytimezone = request.args.get('timezone',"UTC")
    units= request.args.get('units',"US")
    mode  = request.args.get('mode',"last")
    
    response = None


    rain_hour=[]
    rain_day=[]

    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]

    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")      

    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)


    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " sensor='rain_gauge'"



    #log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    #log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

  
    if serieskeys.find("*") > 0:
        serieskeys = serieskeys.replace("*", ".*")

    query = ('select  difference(last(accumulation)) AS accumulation from {} '
                   'where {} AND time > {}s and time < {}s '
                   'group by time({}s)  ') \
              .format( measurement, serieskeys,
                      startepoch, endepoch,
                      resolution)

  

    log.info("freeboard freeboard_rain_wung data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))


            
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', response)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        pass

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        

        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing','accumulation':list(reversed(accumulation))})     


    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
      

        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing','accumulation':list(reversed(accumulation))})     
   

      

    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)


    #keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)
    
    try:
    
      strvalue = ""
      accumulation = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'

      wind_speed=[]
      wind_direction=[]

      ts =startepoch*1000
 
      points = list(response.get_points())

      #log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'
        value5 = '---'
        value6 = '---'
        value7 = '---'
        value8 = '---'
        
        
        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)

        if point['accumulation'] is not None:

          accumulation = float("{0:.2f}".format(point['accumulation'] * 0.0393701))


        
       

      callback = request.args.get('callback')
      myjsondate = mydatetimetz.strftime("%B %d, %Y %H:%M:%S")


      # Setup Weather Underground Post
      if wunstation != "" and wunpassword != "":

        mywundate = mydatetimetz.strftime("%Y-%m-%d %H:%M:%S")
        
        devicedataurl = " https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?ID=" + wunstation + "&PASSWORD=" + wunpassword + "&dateutc=" + str(mywundate)

 
        if accumulation != '---':        
          devicedataurl = devicedataurl + "&rainin=" + str(value1)

        
        devicedataurl = devicedataurl + "&action=updateraw" 

        

        log.info("freeboard_rain_wung:  WUNG HTTP GET: %s", devicedataurl)

        
        try:      
          headers = {'content-type': 'application/json'}
          response = requests.get(devicedataurl)

          if response.ok:
            log.info('freeboard_rain_wung:  WUNG HTTP GET OK %s: ', response.text )


          else:
            log.info('freeboard_rain_wung:  WUNG HTTP GET ERROR %s: ', response.text )


        except:
          e = sys.exc_info()[0]
          log.info("freeboard_rain_wung:: update_wun_url error: %s" % e)

      #End of  Weather Underground Post

      

        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'status':'success','accumulation':list(reversed(accumulation))})    
   

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard: Error in geting freeboard response  %s:  ' % str(e))     

      e = sys.exc_info()[0]
      log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
      #return jsonify(update=False, status='missing' )
      callback = request.args.get('callback')
      return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })
     
    
    except:
      log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
      e = sys.exc_info()[0]
      log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
      #return jsonify(update=False, status='missing' )
      callback = request.args.get('callback')
      return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error',  update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })






@app.route('/freeboard_weather_wung')
@cross_origin()
def freeboard_weather_wung():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')

    wunstation = request.args.get('wunstation','')
    wunpassword = request.args.get('wunpw','')
    
    Interval = request.args.get('interval',"5min")
    resolution = request.args.get('resolution',"")
    windtype = request.args.get('type',"true")
    mytimezone = request.args.get('timezone',"UTC")
    units= request.args.get('units',"US")
    mode  = request.args.get('mode',"last")
    
    response = None


    wind_speed=[]
    wind_direction=[]
    temperature=[]
    atmospheric_pressure=[]
    atmospheric_pressure_sea=[]
    humidity=[]
    altitude=[]
      
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]

    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")      

    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)

    
    if  windtype =="apparent":
      serieskeys=" deviceid='"
      serieskeys= serieskeys + deviceid + "' AND "
      serieskeys= serieskeys +  " (sensor='wind_data' OR sensor='environmental_data') AND instance='0' AND (type='Apparent Wind'  OR type='Outside Temperature' OR type='Outside Humidity')"
      #serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Outside Temperature' OR type='Outside Humidity')"

    else  :
      serieskeys=" deviceid='"
      serieskeys= serieskeys + deviceid + "' AND "
      #serieskeys= serieskeys +  " sensor='wind_data' AND instance='0' AND type='TWIND True North' "
      serieskeys= serieskeys +  " (sensor='wind_data' OR sensor='environmental_data') AND instance='0' AND (type='TWIND True North' OR type='Outside Temperature' OR type='Outside Humidity')"
  
    #serieskeys= serieskeys +  " sensor='wind_data'  "


    #log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    #log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

  
    if serieskeys.find("*") > 0:
        serieskeys = serieskeys.replace("*", ".*")

    if mode == "median":
      
      query = ('select  median(wind_direction) AS wind_direction, median(wind_speed) AS  wind_speed, median(temperature) AS temperature, median(atmospheric_pressure) AS  atmospheric_pressure, median(humidity) AS humidity , median(altitude) AS altitude from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)  ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
      
    elif mode == "max":
      
      query = ('select  max(wind_direction) AS wind_direction, max(wind_speed) AS  wind_speed, max(temperature) AS temperature, max(atmospheric_pressure) AS  atmospheric_pressure, max(humidity) AS humidity , max(altitude) AS altitude  from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)  ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

      
    elif mode == "min":
      
      query = ('select  min(wind_direction) AS wind_direction, min(wind_speed) AS  wind_speed, min(temperature) AS temperature, min(atmospheric_pressure) AS  atmospheric_pressure, min(humidity) AS humidity , min(altitude) AS altitude  from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)  ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)      
      
    elif mode == "mean":    
      query = ('select  mean(wind_direction) AS wind_direction, mean(wind_speed) AS  wind_speed, mean(temperature) AS temperature, mean(atmospheric_pressure) AS  atmospheric_pressure, mean(humidity) AS humidity , mean(altitude) AS altitude  from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)  ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

    elif mode == "last":        
      query = ('select  last(wind_direction) AS wind_direction, last(wind_speed) AS  wind_speed, last(temperature) AS temperature, last(atmospheric_pressure) AS  atmospheric_pressure, last(humidity) AS humidity , last(altitude) AS altitude  from {} '
                     'where {} AND time > {}s and time < {}s  ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch )


    else:       
      query = ('select  last(wind_direction) AS wind_direction, last(wind_speed) AS  wind_speed, last(temperature) AS temperature, last(atmospheric_pressure) AS  atmospheric_pressure, last(humidity) AS humidity , last(altitude) AS altitude  from {} '
                     'where {} AND time > {}s and time < {}s  ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch )

    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))


            
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', response)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        pass

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        
        if  windtype =="apparent":
          return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing','apparentwindspeed':list(reversed(wind_speed)), 'apparentwinddirection':list(reversed(wind_direction)), 'temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity)), 'altitude':list(reversed(altitude)), 'atmospheric_pressure_sea':list(reversed(atmospheric_pressure_sea))})     
        else:
          return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing','truewindspeed':list(reversed(wind_speed)), 'truewinddir':list(reversed(wind_direction)), 'temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity)), 'altitude':list(reversed(altitude)), 'atmospheric_pressure_sea':list(reversed(atmospheric_pressure_sea))})     


    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
      
        if  windtype =="apparent":
          return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing','apparentwindspeed':list(reversed(wind_speed)), 'apparentwinddirection':list(reversed(wind_direction)), 'temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity)), 'altitude':list(reversed(altitude)), 'atmospheric_pressure_sea':list(reversed(atmospheric_pressure_sea))})     
        else:
          return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing','truewindspeed':list(reversed(wind_speed)), 'truewinddir':list(reversed(wind_direction)), 'temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity)), 'altitude':list(reversed(altitude)), 'atmospheric_pressure_sea':list(reversed(atmospheric_pressure_sea))})     
   

      

    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)


    #keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)
    
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'

      wind_speed=[]
      wind_direction=[]

      ts =startepoch*1000
 
      points = list(response.get_points())

      #log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'
        value5 = '---'
        value6 = '---'
        value7 = '---'
        value8 = '---'
        
        
        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)

        if point['wind_speed'] is not None:       
          value1 = convertfbunits(point['wind_speed'],  convertunittype('speed', units))
        wind_speed.append({'epoch':ts, 'value':value1})
          
        if point['wind_direction'] is not None:       
          value2 = convertfbunits(point['wind_direction'], 16)
        wind_direction.append({'epoch':ts, 'value':value2})

        if point['temperature'] is not None: 
          value3 = convertfbunits(point['temperature'],  convertunittype('temperature', units))
        temperature.append({'epoch':ts, 'value':value3})
          
        if point['atmospheric_pressure'] is not None:         
          value4 = convertfbunits(point['atmospheric_pressure'], convertunittype('baro_pressure', units))
        atmospheric_pressure.append({'epoch':ts, 'value':value4})
                    
        if point['humidity'] is not None:         
          value5 = convertfbunits(point['humidity'], 26)
        humidity.append({'epoch':ts, 'value':value5})

                    
        if point['altitude'] is not None:         
          value6 = convertfbunits(point['altitude'], 32)
        altitude.append({'epoch':ts, 'value':value6})

        if point['atmospheric_pressure'] is not None and point['altitude'] is not None:
          #get pressure in KPa
          value8 = convertfbunits(point['atmospheric_pressure'], 9)
          #get altitde in feet
          value6 = convertfbunits(point['altitude'], 32)
          # get adjustment for altitude in KPa
          value7 = getAtmosphericCompensation(value6)
          #add offset if any in KPa
          value7 = convertfbunits(value8 + value7, convertunittype('baro_pressure', units))
          
        atmospheric_pressure_sea.append({'epoch':ts, 'value':value7})    



        
       

      callback = request.args.get('callback')
      myjsondate = mydatetimetz.strftime("%B %d, %Y %H:%M:%S")


      # Setup Weather Underground Post
      if wunstation != "" and wunpassword != "":

        mywundate = mydatetimetz.strftime("%Y-%m-%d %H:%M:%S")
        
        devicedataurl = " https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?ID=" + wunstation + "&PASSWORD=" + wunpassword + "&dateutc=" + str(mywundate)

        
        if value2 != '---':
          devicedataurl = devicedataurl + "&winddir=" + str(value2)
          
        if value1 != '---':        
          devicedataurl = devicedataurl + "&windspeedmph=" + str(value1)
          
        if value2 != '---':
          devicedataurl = devicedataurl + "&tempf=" + str(value3)
          
        if value4 != '---':
          devicedataurl = devicedataurl + "&baromin=" + str(value4)
          
        if value5 != '---':
          devicedataurl = devicedataurl + "&humidity=" + str(value5)
        
        devicedataurl = devicedataurl + "&action=updateraw" 

        

        log.info("freeboard_weather_wung:  WUNG HTTP GET: %s", devicedataurl)

        
        try:      
          headers = {'content-type': 'application/json'}
          response = requests.get(devicedataurl)

          if response.ok:
            log.info('freeboard_weather_wung:  WUNG HTTP GET OK %s: ', response.text )


          else:
            log.info('freeboard_weather_wung:  WUNG HTTP GET ERROR %s: ', response.text )


        except:
          e = sys.exc_info()[0]
          log.info("freeboard_weather_wung:: update_wun_url error: %s" % e)

      #End of  Weather Underground Post

      
      if  windtype =="apparent":
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'status':'success','apparentwindspeed':list(reversed(wind_speed)), 'apparentwinddirection':list(reversed(wind_direction)),'temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity)), 'altitude':list(reversed(altitude)), 'atmospheric_pressure_sea':list(reversed(atmospheric_pressure_sea))})     
      else:
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'status':'success','truewindspeed':list(reversed(wind_speed)), 'truewinddir':list(reversed(wind_direction)),'temperature':list(reversed(temperature)), 'atmospheric_pressure':list(reversed(atmospheric_pressure)), 'humidity':list(reversed(humidity)), 'altitude':list(reversed(altitude)), 'atmospheric_pressure_sea':list(reversed(atmospheric_pressure_sea))})     
   

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard: Error in geting freeboard response  %s:  ' % str(e))     

      e = sys.exc_info()[0]
      log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
      #return jsonify(update=False, status='missing' )
      callback = request.args.get('callback')
      return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })
     
    
    except:
      log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
      e = sys.exc_info()[0]
      log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
      #return jsonify(update=False, status='missing' )
      callback = request.args.get('callback')
      return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error',  update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })






@app.route('/freeboard_winddata')
@cross_origin()
def freeboard_winddata():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    resolution = request.args.get('resolution',"")
    windtype = request.args.get('type',"true")
    mytimezone = request.args.get('timezone',"UTC")
    units= request.args.get('units',"US")
    mode  = request.args.get('mode',"median")
    
    response = None


    wind_speed=[]
    wind_direction=[]
    wind_gusts=[]
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]

    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")      

    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)

    
    if  windtype =="apparent":
      serieskeys=" deviceid='"
      serieskeys= serieskeys + deviceid + "' AND "
      serieskeys= serieskeys +  " sensor='wind_data' AND instance='0' AND (type='Apparent Wind' OR type='Gust' ) "
    else  :
      serieskeys=" deviceid='"
      serieskeys= serieskeys + deviceid + "' AND "
      serieskeys= serieskeys +  " sensor='wind_data' AND instance='0' AND (type='TWIND True North' OR type='Gust' ) "
  
    #serieskeys= serieskeys +  " sensor='wind_data'  "


    #log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    #log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

  
    if serieskeys.find("*") > 0:
        serieskeys = serieskeys.replace("*", ".*")

    if mode == "median":
      
      query = ('select  median(wind_direction) AS wind_direction, median(wind_speed) AS  wind_speed , median(wind_gusts) AS  wind_gusts from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)  ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
      
    elif mode == "max":
      
      query = ('select  max(wind_direction) AS wind_direction, max(wind_speed) AS  wind_speed , max(wind_gusts) AS  wind_gusts from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)  ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

      
    elif mode == "min":
      
      query = ('select  min(wind_direction) AS wind_direction, min(wind_speed) AS  wind_speed, min(wind_gusts) AS  wind_gusts from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)  ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)      
      
    else:       
      query = ('select  mean(wind_direction) AS wind_direction, mean(wind_speed) AS  wind_speed, mean(wind_gusts) AS  wind_gusts from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)  ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)


    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))


            
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', response)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        pass

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        
        if  windtype =="apparent":
          return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing','apparentwindspeed':list(reversed(wind_speed)), 'apparentwinddirection':list(reversed(wind_direction))})
        else:
          return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing','truewindspeed':list(reversed(wind_speed)), 'truewinddir':list(reversed(wind_direction))})
   


    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
      
        if  windtype =="apparent":
          return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing','apparentwindspeed':list(reversed(wind_speed)), 'apparentwinddirection':list(reversed(wind_direction))})
        else:
          return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing','truewindspeed':list(reversed(wind_speed)), 'truewinddir':list(reversed(wind_direction))})
   

      

    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)


    #keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)
    
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'

      wind_speed=[]
      wind_direction=[]
      wind_gusts=[]
      windspeedavg=[]
      winddiravg=[]

      ts =startepoch*1000
 
      points = list(response.get_points())

      #log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'
        
        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)

        if point['wind_speed'] is not None:       
          value1 = convertfbunits(point['wind_speed'],  convertunittype('speed', units))
          windspeedavg.append(value1)
        wind_speed.append({'epoch':ts, 'value':value1})
          
        if point['wind_direction'] is not None:       
          value2 = convertfbunits(point['wind_direction'], 16)
          winddiravg.append(value2)
        wind_direction.append({'epoch':ts, 'value':value2})

        if point['wind_gusts'] is not None:       
          value3 = convertfbunits(point['wind_gusts'],  convertunittype('speed', units))
        wind_gusts.append({'epoch':ts, 'value':value3})
       

      avgwindspeed = sum(windspeedavg) / float(len(windspeedavg))
      avgwinddir = sum(winddiravg) / float(len(winddiravg))

      avgwindspeed = float("{0:.1f}".format(avgwindspeed))
      avgwinddir = float("{0:.1f}".format(avgwinddir))

      average_windspeed=[]
      average_winddir=[]
      
      for point in points:
        
        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)
          
            average_windspeed.append( {'epoch':ts, 'value':avgwindspeed})
            average_winddir.append( {'epoch':ts, 'value':avgwinddir})

      callback = request.args.get('callback')
      myjsondate = mydatetimetz.strftime("%B %d, %Y %H:%M:%S")


      
      if  windtype =="apparent":
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'status':'success','apparentwindspeed':list(reversed(wind_speed)), 'apparentwinddirection':list(reversed(wind_direction)), 'windgusts':list(reversed(wind_gusts)), 'averagewindspeed':list(reversed(average_windspeed)), "averagewinddir":list(reversed(average_winddir))})
      else:
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'status':'success','truewindspeed':list(reversed(wind_speed)), 'truewinddir':list(reversed(wind_direction)), 'windgusts':list(reversed(wind_gusts)), 'averagewindspeed':list(reversed(average_windspeed)), "averagewinddir":list(reversed(average_winddir))})
   

      
    except TypeError as e:
        #log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error',  update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

@app.route('/freeboard_winddata_apparent')
@cross_origin()
def freeboard_winddata_apparent():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('Interval',"5min")
    mytimezone = request.args.get('timezone',"UTC")
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]

    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"

    


    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " sensor='wind_data' AND instance='0' AND type='Apparent Wind' "
    #serieskeys= serieskeys +  " sensor='wind_data'  "


    #log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    #log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

  

      
    query = ('select  mean(wind_direction) AS wind_direction, mean(wind_speed) AS  wind_speed from {} '
                   'where {} AND time > {}s and time < {}s '
                   'group by time({}s)') \
              .format( measurement, serieskeys,
                      startepoch, endepoch,
                      resolution)
 


    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))


            
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', response)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        pass

    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })

    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)


    #keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)
    
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'
 
      points = list(response.get_points())

      log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        value1 = convertfbunits(point['wind_speed'],  4)
        value2 = convertfbunits(point['wind_direction'], 16)

        mydatetimestr = str(point['time'])

        mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')

      log.info('freeboard: freeboard returning data values wind_speed:%s, wind_direction:%s  ', value1,value2)            

      callback = request.args.get('callback')
      myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")        
      return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','wind_speed':value1, 'wind_direction':value2,})
      

     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error',  update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
@app.route('/freeboard_environmental2')
@cross_origin()
def freeboard_environmental2():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('Interval',"5min")

    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]




    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"

    #serieskeys={'deviceid'=deviceid, 'sensor'='environmental_data', 'instance'='0', 'type'='Outside_Temperature'}

    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Outside Temperature' OR type='Outside Humidity')"
    #serieskeys= serieskeys +  " sensor='environmental_data'  AND type='Outside_Temperature'"
    #serieskeys= serieskeys +  " sensor='environmental_data'  "
    
    Key2="deviceid:001EC010AD69.sensor:environmental_data.source:0.instance:0.type:Outside_Temperature.parameter:humidity.HelmSmart"
    Key3="deviceid:001EC010AD69.sensor:environmental_data.source:0.instance:0.type:Outside_Temperature.parameter:atmospheric_pressure.HelmSmart"



    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)


      

    query = ("select mean(value) from HelmSmart "
             "where  deviceid='001EC010AD69' and sensor='environmental_data' and time > {}s and time < {}s "
             "group by * limit 1") \
        .format(
                startepoch, endepoch
                )
    

    log.info("freeboard Get InfluxDB query %s", query)

    try:    
      result = dbc.query(query)

      log.info("freeboard Get InfluxDB results %s", result)

      keys = result.raw.get('series',[])
      #log.info("freeboard Get InfluxDB series keys %s", keys)

      """
      for series in response:
        #log.info("influxdb results..%s", series )
        for point in series['points']:
          fields = {}
          for key, val in zip(series['columns'], point):
            fields[key] = val
      """  



      strvalue=""
      
      for series in keys:
        #log.info("freeboard Get InfluxDB series key %s", series)
        log.info("freeboard Get InfluxDB series tags %s ", series['tags'])
        #log.info("freeboard Get InfluxDB series columns %s ", series['columns'])
        #log.info("freeboard Get InfluxDB series values %s ", series['values'])
        values = series['values']
        for value in values:
          log.info("freeboard Get InfluxDB series time %s", value[0])
          log.info("freeboard Get InfluxDB series mean %s", value[1])

        for point in series['values']:
          fields = {}
          for key, val in zip(series['columns'], point):
            fields[key] = val
            
        log.info("freeboard Get InfluxDB series points %s , %s", fields['time'], fields['mean'])

        tag = series['tags']
        log.info("freeboard Get InfluxDB series tags2 %s ", tag)

        mydatetimestr = str(fields['time'])
        
        if tag['type'] == 'Outside Temperature' and tag['parameter']== 'temperature':
            value1 = convertfbunits(fields['mean'],  0)
            strvalue = strvalue + ':' + str(value1)
            
        elif tag['type']  == 'Outside Temperature' and tag['parameter'] == 'atmospheric_pressure':
            value2 = convertfbunits(fields['mean'], 10)
            strvalue = strvalue + ':' + str(value2)
            
        elif tag['type']  == 'Outside Humidity' and tag['parameter'] == 'humidity':
            value3=  convertfbunits(fields['mean'], 26)
            strvalue = strvalue + ':' + str(value3)

        log.info("freeboard Get InfluxDB series tags3 %s ", strvalue)


      mydatetimestr = mydatetimestr.split(".")
      log.info("freeboard Get InfluxDB time string%s ", mydatetimestr[0])


      #mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S.%fZ')
      mydatetime = datetime.datetime.strptime(mydatetimestr[0], '%Y-%m-%dT%H:%M:%S')
      
      callback = request.args.get('callback')
      myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")        
      return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','temperature':value1, 'baro':value2, 'humidity':value3})

    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', query)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error',  update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

@app.route('/freeboard_winddataTrue')
@cross_origin()
def freeboard_winddataTrue():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    windtype = request.args.get('type',"true")
    Interval = request.args.get('Interval',"5min")

    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]




    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"

    #serieskeys={'deviceid'=deviceid, 'sensor'='environmental_data', 'instance'='0', 'type'='Outside_Temperature'}

    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " sensor='environmental_data' AND instance='0' AND (type='Outside Temperature' OR type='Outside Humidity')"
    #serieskeys= serieskeys +  " sensor='environmental_data'  AND type='Outside_Temperature'"
    #serieskeys= serieskeys +  " sensor='environmental_data'  "
    
    Key2="deviceid:001EC010AD69.sensor:environmental_data.source:0.instance:0.type:Outside_Temperature.parameter:humidity.HelmSmart"
    Key3="deviceid:001EC010AD69.sensor:environmental_data.source:0.instance:0.type:Outside_Temperature.parameter:atmospheric_pressure.HelmSmart"



    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)


      

    query = ("select mean(value) from HelmSmart "
             "where  deviceid='001EC010AD69' and sensor='wind_data' and time > {}s and time < {}s "
             "group by * limit 1") \
        .format(
                startepoch, endepoch
                )
    

    log.info("freeboard Get InfluxDB query %s", query)

    try:    
      result = dbc.query(query)

      log.info("freeboard Get InfluxDB results %s", result)

      keys = result.raw.get('series',[])
      #log.info("freeboard Get InfluxDB series keys %s", keys)

      """
      for series in response:
        #log.info("influxdb results..%s", series )
        for point in series['points']:
          fields = {}
          for key, val in zip(series['columns'], point):
            fields[key] = val
      """  



      strvalue=""
      
      for series in keys:
        #log.info("freeboard Get InfluxDB series key %s", series)
        log.info("freeboard Get InfluxDB series tags %s ", series['tags'])
        #log.info("freeboard Get InfluxDB series columns %s ", series['columns'])
        #log.info("freeboard Get InfluxDB series values %s ", series['values'])
        values = series['values']
        for value in values:
          log.info("freeboard Get InfluxDB series time %s", value[0])
          log.info("freeboard Get InfluxDB series mean %s", value[1])

        for point in series['values']:
          fields = {}
          for key, val in zip(series['columns'], point):
            fields[key] = val
            
        log.info("freeboard Get InfluxDB series points %s , %s", fields['time'], fields['mean'])

        tag = series['tags']
        log.info("freeboard Get InfluxDB series tags2 %s ", tag)

        mydatetimestr = str(fields['time'])
        


        if tag['type'] == 'TWIND True North' and tag['parameter'] == 'wind_speed':
            truewindspeed =  convertfbunits(fields['mean'], convertunittype('speed', units))
            strvalue = strvalue + ':' + str(truewindspeed)
            
        elif tag['type'] == 'Apparent Wind' and tag['parameter'] == 'wind_speed':
            appwindspeed =  convertfbunits(fields['mean'],  convertunittype('speed', units))
            strvalue = strvalue + ':' + str(appwindspeed)
            
        elif tag['type'] == 'TWIND True North' and tag['parameter'] == 'wind_direction':
            truewinddir=  convertfbunits(fields['mean'], 16)
            strvalue = strvalue + ':' + str(truewinddir)
            
        elif tag['type'] == 'Apparent Wind' and tag['parameter'] == 'wind_direction':
            appwinddir =  convertfbunits(fields['mean'], 16)
            strvalue = strvalue + ':' + str(appwinddir)
            

        log.info("freeboard Get InfluxDB series tags3 %s ", strvalue)


      mydatetimestr = mydatetimestr.split(".")
      log.info("freeboard Get InfluxDB time string%s ", mydatetimestr[0])


      #mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S.%fZ')
      mydatetime = datetime.datetime.strptime(mydatetimestr[0], '%Y-%m-%dT%H:%M:%S')
      
      callback = request.args.get('callback')
      myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")        
      return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','truewindspeed':truewindspeed,'appwindspeed':appwindspeed,'truewinddir':truewinddir, 'appwinddir':appwinddir})

    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', query)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error',  update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })




@app.route('/freeboard_location')
@cross_origin()
def freeboard_location():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    resolution = request.args.get('resolution',"")
    postype = request.args.get('type',"NULL")
    mytimezone = request.args.get('timezone',"UTC")
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]




    lat=[]
    lng=[]
    position=[]
    siv=[]

    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")



    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)
    #serieskeys={'deviceid'=deviceid, 'sensor'='environmental_data', 'instance'='0', 'type'='Outside_Temperature'}

    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " sensor='position_rapid' "
    serieskeys= serieskeys +  "  AND type='" + postype + "' "
 

    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    #log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)


      

    if serieskeys.find("*") > 0:
        serieskeys = serieskeys.replace("*", ".*")

        query = ('select  median(lat) AS lat, median(lng) AS  lng  , median(siv) AS  siv from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
    else:
      
      query = ('select  median(lat) AS lat, median(lng) AS  lng  , median(siv) AS  siv from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
 


    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))


            
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', response)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        pass

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing', 'lat':list(reversed(lat)), 'lng':list(reversed(lng)), 'position':list(reversed(position)), 'siv':list(reversed(siv))})     



    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing', 'lat':list(reversed(lat)), 'lng':list(reversed(lng)), 'position':list(reversed(position)), 'siv':list(reversed(siv))})     


    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)

    #keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'

      lat=[]
      lng=[]
      position=[]
      siv=[]
 
      points = list(response.get_points())

      #log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
       # log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'
        
        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)

        
        if (point['lat'] is not None)  :
          if (point['lng'] is not None) :
            
            value1 = convertfbunits(point['lat'], 15)
            #log.info("freeboard freeboard_location lat %s", value1)
            if abs(value1) > 0.1:
              #log.info("freeboard freeboard_location adding lat %s", value1)
              lat.append({'epoch':ts, 'value':value1})


            value2 = convertfbunits(point['lng'], 15)
            #log.info("freeboard freeboard_location lng %s", value2)
            if abs(value2) > 0.1:
              #log.info("freeboard freeboard_location adding lng %s", value2)
              lng.append({'epoch':ts, 'value':value2})

            #log.info("freeboard freeboard_location lat %s lng %s", value1, value2)
            if abs(value1) > 0.1 and abs(value2) > 0.1:
              #log.info("freeboard freeboard_location adding position %s", value2)
              position.append({'epoch':ts, 'lat':value1, 'lng':value2})


        if point['siv'] is not None:       
          value3 = int(point['siv'])
          siv.append({'epoch':ts, 'siv':value3})            
 
      """

      log.info('freeboard: before exosite write:')
      o = onep.OnepV1()

      cik = '5b38da024d8a1f252e575202afb431ef22d3eb66'
      #dataport_alias = 'Device'
      #val_to_write = 'Data'
      dataport_alias = 'GPDdata'
      
      latDD=int(value1)
      lngDD=int(value2)
      #latMM = 60*(value1 - latDD)
      #lngMM = 60*(value2 - lngDD)
      
      latMM = float("{0:.4f}".format(60*(value1 - latDD)) )
      lngMM = float("{0:.4f}".format(60*(value2 - lngDD)) )

      latlng = str((latDD*100) + latMM) + "_" + str((lngDD*100) + lngMM)
      
      val_to_write =str(latlng)
      log.info('freeboard: after exosite latlng:%s', val_to_write)

      
      #testvar = o.write(cik, {"alias": dataport_alias}, val_to_write,{})
      #log.info('freeboard: fter exosite write:%s', testvar)
      o.write(cik, {"alias": dataport_alias}, val_to_write,{})
      log.info('freeboard: after exosite write:')

      """
      

      callback = request.args.get('callback')
      myjsondate= mydatetimetz.strftime("%B %d, %Y %H:%M:%S")  


      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','lat':value1, 'lng':value2,})
      return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','lat':list(reversed(lat)), 'lng':list(reversed(lng)), 'position':list(reversed(position)), 'siv':list(reversed(siv))})     
        

     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error', update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })




@app.route('/freeboard_location_wind')
@cross_origin()
def freeboard_location_wind():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    resolution = request.args.get('resolution',"")
    windtype = request.args.get('type',"true")
    mytimezone = request.args.get('timezone',"UTC")
    units= request.args.get('units',"US")
    mode  = request.args.get('mode',"median")
    source  = request.args.get('source',"")

    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]




    lat=[]
    lng=[]
    position=[]
    siv=[]
    wind_speed=[]
    wind_direction=[]

    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")



    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)
    #serieskeys={'deviceid'=deviceid, 'sensor'='environmental_data', 'instance'='0', 'type'='Outside_Temperature'}

    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "

    if source != "":
      serieskeys= serieskeys + "source = '" + source + "' AND "








      
    serieskeys= serieskeys +  " sensor='position_rapid' OR sensor='wind_data'"


    
    #serieskeys= serieskeys +  "  AND type='" + postype + "' OR type='TWIND True North' "



    if  windtype =="apparent":
      serieskeys= serieskeys +  " AND (type='Apparent Wind' OR type='Gust' ) "
    else  :
      serieskeys= serieskeys +  " AND (type='TWIND True North' OR type='Gust' ) "

    
 

    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    #log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)


      

    if serieskeys.find("*") > 0:
        serieskeys = serieskeys.replace("*", ".*")

        query = ('select  median(lat) AS lat, median(lng) AS  lng  , median(wind_direction) AS wind_direction, median(wind_speed) AS  wind_speed  from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
    else:
      
      query = ('select  median(lat) AS lat, median(lng) AS  lng  , median(wind_direction) AS wind_direction, median(wind_speed) AS  wind_speed  from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
 


    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))


            
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', response)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        pass

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing', 'lat':list(reversed(lat)), 'lng':list(reversed(lng)), 'position':list(reversed(position)), 'siv':list(reversed(siv))})     



    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing', 'lat':list(reversed(lat)), 'lng':list(reversed(lng)), 'position':list(reversed(position)), 'siv':list(reversed(siv))})     


    log.info('freeboard_location_wind:  InfluxDB-Cloud response  %s:', response)

    #keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'

      lat=[]
      lng=[]
      position=[]
      position_wind=[]
      wind_speed=[]
      wind_direction=[]
 
      points = list(response.get_points())

      #log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
       # log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'
        
        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)

        
        if (point['lat'] is not None)  :
          if (point['lng'] is not None) :
            
            value1 = convertfbunits(point['lat'], 15)

            value2 = convertfbunits(point['lng'], 15)


            #log.info("freeboard freeboard_location lat %s lng %s", value1, value2)
            if abs(value1) > 0.1 and abs(value2) > 0.1:
              #log.info("freeboard freeboard_location adding position %s", value2)
              position.append({'epoch':ts, 'lat':value1, 'lng':value2})


              if point['wind_speed'] is not None:       
                value3 = convertfbunits(point['wind_speed'],  convertunittype('speed', units))
              wind_speed.append({'epoch':ts, 'value':value3})
                
              if point['wind_direction'] is not None:       
                value4 = convertfbunits(point['wind_direction'], 16)
              wind_direction.append({'epoch':ts, 'value':value4})

              position_wind.append({'epoch':ts, 'lat':value1, 'lng':value2, 'truewindspeed':value3, 'truewinddir':value4  })


       
 
      """

      log.info('freeboard: before exosite write:')
      o = onep.OnepV1()

      cik = '5b38da024d8a1f252e575202afb431ef22d3eb66'
      #dataport_alias = 'Device'
      #val_to_write = 'Data'
      dataport_alias = 'GPDdata'
      
      latDD=int(value1)
      lngDD=int(value2)
      #latMM = 60*(value1 - latDD)
      #lngMM = 60*(value2 - lngDD)
      
      latMM = float("{0:.4f}".format(60*(value1 - latDD)) )
      lngMM = float("{0:.4f}".format(60*(value2 - lngDD)) )

      latlng = str((latDD*100) + latMM) + "_" + str((lngDD*100) + lngMM)
      
      val_to_write =str(latlng)
      log.info('freeboard: after exosite latlng:%s', val_to_write)

      
      #testvar = o.write(cik, {"alias": dataport_alias}, val_to_write,{})
      #log.info('freeboard: fter exosite write:%s', testvar)
      o.write(cik, {"alias": dataport_alias}, val_to_write,{})
      log.info('freeboard: after exosite write:')

      """
      

      callback = request.args.get('callback')
      myjsondate= mydatetimetz.strftime("%B %d, %Y %H:%M:%S")  


      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','lat':value1, 'lng':value2,})
      return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'position':list(reversed(position)),'truewindspeed':list(reversed(wind_speed)), 'truewinddir':list(reversed(wind_direction)), 'location_wind':list(reversed(position_wind))})     
        

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error', update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })




@app.route('/freeboard_nav')
@cross_origin()
def freeboard_nav():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    resolution = request.args.get('resolution',"")
    navtype = request.args.get('type',"true")
    units= request.args.get('units',"US")
    mytimezone = request.args.get('timezone',"UTC")
    mode = request.args.get('mode',"mean")
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]



    cog=[]
    sog=[]
    heading=[]

    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")

    
    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)


    if navtype == "magnetic":
      serieskeys=" deviceid='"
      serieskeys= serieskeys + deviceid + "' AND "
      serieskeys= serieskeys +  " (sensor='cogsog' OR sensor='heading') AND "
      serieskeys= serieskeys +  " (type='Magnetic') " 

    else:
      serieskeys=" deviceid='"
      serieskeys= serieskeys + deviceid + "' AND "
      serieskeys= serieskeys +  " (sensor='cogsog' OR sensor='heading') AND "
      serieskeys= serieskeys +  " (type='True') " 


    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)


      

    if serieskeys.find("*") > 0:
      serieskeys = serieskeys.replace("*", ".*")

    if mode == "median":      

      query = ('select  median(course_over_ground) AS cog, median(speed_over_ground) AS  sog, median(heading) AS heading  from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
      
    elif mode == "max":      

      query = ('select  max(course_over_ground) AS cog, max(speed_over_ground) AS  sog, max(heading) AS heading  from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)
      
    elif mode == "min":      

      query = ('select  min(course_over_ground) AS cog, min(speed_over_ground) AS  sog, min(heading) AS heading  from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)      
      
    else:
      
      query = ('select  mean(course_over_ground) AS cog, mean(speed_over_ground) AS  sog, mean(heading) AS heading  from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution) 
 


    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))


            
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', response)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        pass

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        if navtype == "magnetic":
          return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing' ,'cog':list(reversed(cog)), 'sog':list(reversed(sog)), 'heading_mag':list(reversed(heading))})     
        else:
          return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing' ,'cog':list(reversed(cog)), 'sog':list(reversed(sog)), 'heading_true':list(reversed(heading))})     


    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        if navtype == "magnetic":
          return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing' ,'cog':list(reversed(cog)), 'sog':list(reversed(sog)), 'heading_mag':list(reversed(heading))})     
        else:
          return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing' ,'cog':list(reversed(cog)), 'sog':list(reversed(sog)), 'heading_true':list(reversed(heading))})     


    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)

    #keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'
      
      cog=[]
      sog=[]
      heading=[]
 
      points = list(response.get_points())

      #log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'

        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)

        
        if point['cog'] is not None: 
          value1 = convertfbunits(point['cog'], 16)
        cog.append({'epoch':ts, 'value':value1})
          
        if point['sog'] is not None:         
          value2 = convertfbunits(point['sog'], convertunittype('speed', units))
        sog.append({'epoch':ts, 'value':value2})
          
        if point['heading'] is not None:         
          value3 = convertfbunits(point['heading'], 16)
        heading.append({'epoch':ts, 'value':value3})
          


      #log.info('freeboard: freeboard returning data values wind_speed:%s, wind_direction:%s  ', value1,value2)            

      callback = request.args.get('callback')
      myjsondate= mydatetimetz.strftime("%B %d, %Y %H:%M:%S")  


      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','lat':value1, 'lng':value2,})
      if navtype == "magnetic":
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','cog':list(reversed(cog)), 'sog':list(reversed(sog)), 'heading_mag':list(reversed(heading))})     
      else:
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','cog':list(reversed(cog)), 'sog':list(reversed(sog)), 'heading_true':list(reversed(heading))})     
        

     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error', update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })




@app.route('/freeboard_water_depth')
@cross_origin()
def freeboard_water_depth():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    resolution = request.args.get('resolution',"")
    navtype = request.args.get('type',"Paddle Wheel")
    units= request.args.get('units',"US")
    dataformat = request.args.get('format', 'json')
    mytimezone = request.args.get('timezone',"UTC")
    mode = request.args.get('mode',"mean")
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]




    depth=[]
    speed=[]
    temperature=[]

    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")

    
    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)

    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    #serieskeys= serieskeys +  " (sensor='water_depth' )  "
    serieskeys= serieskeys +  " (sensor='water_depth' OR sensor='water_speed' OR sensor='temperature') AND "
    serieskeys= serieskeys +  " (type='Sea Temperature' OR type='Paddle Wheel' OR type='Correlation Log'  OR type='NULL' ) "

    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)


    if serieskeys.find("*") > 0:
      serieskeys = serieskeys.replace("*", ".*")

    if mode == "median":
      
      query = ('select  median(depth) AS depth, median(waterspeed) AS waterspeed, median(actual_temperature) AS temperature   from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

    elif mode == "max":
      
      query = ('select  max(depth) AS depth, max(waterspeed) AS waterspeed, max(actual_temperature) AS temperature    from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)

    elif mode == "min":
      
      query = ('select  min(depth) AS depth, min(waterspeed) AS waterspeed, min(actual_temperature) AS temperature    from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution)      
      
    else:

      query = ('select  mean(depth) AS depth, mean(waterspeed) AS waterspeed, mean(actual_temperature) AS temperature  from {} '            
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution) 
 


    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e: 
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))


            
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', response)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        pass

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #if navtype == "magnetic":
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing', 'depth':list(reversed(depth)), 'speed':list(reversed(speed)), 'temperature':list(reversed(temperature))})    
        #else:
        #  return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing' ,'cog':list(reversed(cog)), 'sog':list(reversed(sog)), 'heading_true':list(reversed(heading))})     


    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #if navtype == "magnetic":
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing' ,'depth':list(reversed(depth)), 'speed':list(reversed(speed)), 'temperature':list(reversed(temperature))})    
        #else:
        #  return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing' ,'cog':list(reversed(cog)), 'sog':list(reversed(sog)), 'heading_true':list(reversed(heading))})     


    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)

    #keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'
      
      depth=[]
      waterspeed=[]
      temperature=[]
 
      points = list(response.get_points())

      #log.info('freeboard:  InfluxDB-Cloud points%s:', points)
      csvout = "Time, Depth" + '\r\n'
      
      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'


        


        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)

        
        if point['depth'] is not None: 
          value1 = convertfbunits(point['depth'], convertunittype('depth', units))
        depth.append({'epoch':ts, 'value':value1})
        csvout = csvout + str(ts) + ', '+ str(value1)  + '\r\n'

        if point['waterspeed'] is not None:         
          value2 = convertfbunits(point['waterspeed'], convertunittype('speed', units))
        speed.append({'epoch':ts, 'value':value2})

          
        if point['temperature'] is not None:         
          value3 = convertfbunits(point['temperature'], convertunittype('temperature', units))
        temperature.append({'epoch':ts, 'value':value3})
               
        
        """                  
        if point['temperature'] is not None:          
          value3 = convertfbunits(point['temperature'], 0)
        temperature.append({'epoch':ts, 'value':value3})
        """              

      if dataformat == 'csv':
        response = make_response(csvout)
        response.headers['Content-Type'] = 'text/csv'
        response.headers["Content-Disposition"] = "attachment; filename=HelmSmart_WaterDepth.csv"
        return response

      #log.info('freeboard: freeboard returning data values wind_speed:%s, wind_direction:%s  ', value1,value2)
      
      #elif dataformat == 'json':
      callback = request.args.get('callback')
      myjsondate= mydatetimetz.strftime("%B %d, %Y %H:%M:%S")  


      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','lat':value1, 'lng':value2,})
      #if navtype == "magnetic":
      return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','depth':list(reversed(depth)), 'speed':list(reversed(speed)), 'temperature':list(reversed(temperature))})     
      #else:
       # return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','cog':list(reversed(cog)), 'sog':list(reversed(sog)), 'heading_true':list(reversed(heading))})     
        

     
    except KeyError as e: 
       #log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except TypeError as e: 
       #log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))        
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)


        
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error', update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })






@app.route('/freeboard_attitude')
@cross_origin()
def freeboard_attitude():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    Instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    units= request.args.get('units',"US")
    mytimezone = request.args.get('timezone',"UTC")
    mode  = request.args.get('mode',"median")
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]




    pitch=[]
    roll=[]
    yaw=[]      

    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")

    
    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)


    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " sensor='attitude' "
    #serieskeys= serieskeys +  " instance='" + Instance + "' "

    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

    if mode == "median":
      
      query = ('select  median(pitch) AS pitch, median(roll) AS  roll, median(yaw) AS yaw  from {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution)
      
    elif mode == "max":
      
      query = ('select  max(pitch) AS pitch, max(roll) AS  roll, max(yaw) AS yaw  from {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution)
      
    elif mode == "min":
      
      query = ('select  min(pitch) AS pitch, min(roll) AS  roll, min(yaw) AS yaw  from {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution)
      
    else:
      
      query = ('select  mean(pitch) AS pitch, mean(roll) AS  roll, mean(yaw) AS yaw  from {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution) 
 


    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))


            
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', response)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        pass

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate,  'status':'missing', 'update':'False', 'pitch':list(reversed(pitch)), 'roll':list(reversed(roll)), 'yaw':list(reversed(yaw))})     


    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate,  'status':'missing', 'update':'False', 'pitch':list(reversed(pitch)), 'roll':list(reversed(roll)), 'yaw':list(reversed(yaw))})     

    log.info('freeboard:  InfluxDB-Cloud response  %s:', response)

    keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'
      
      pitch=[]
      roll=[]
      yaw=[]

      ts =startepoch*1000

      points = list(response.get_points())

      #log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'


        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)

        if point['pitch'] is not None: 
          value1 = convertfbunits(point['pitch'], 16)
        pitch.append({'epoch':ts, 'value':value1})
          
        if point['roll'] is not None:         
          value2 = convertfbunits(point['roll'], 16)
        roll.append({'epoch':ts, 'value':value2})
          
        if point['yaw'] is not None:         
          value3 = convertfbunits(point['yaw'], 16)
        yaw.append({'epoch':ts, 'value':value3})
               

      callback = request.args.get('callback')
      myjsondate= mydatetimetz.strftime("%B %d, %Y %H:%M:%S")  


      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','lat':value1, 'lng':value2,})
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','voltage':value1, 'current':value2, 'temperature':value3})
      return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','pitch':list(reversed(pitch)), 'roll':list(reversed(roll)), 'yaw':list(reversed(yaw))})     
        

     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error', update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })







@app.route('/freeboard_battery')
@cross_origin()
def freeboard_battery():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    Instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    units= request.args.get('units',"US")
    mytimezone = request.args.get('timezone',"UTC")
    mode  = request.args.get('mode',"median")
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]




    voltage=[]
    current=[]
    temperature=[]
    stateofcharge=[]
    timeremaining=[]

    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")

    
    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)


    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " sensor='battery_status'  AND "
    serieskeys= serieskeys +  " instance='" + Instance + "' "

    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

    if mode == "median":
      
      query = ('select  median(voltage) AS voltage, median(current) AS  current, median(temperature) AS temperature,  median(stateofcharge) AS stateofcharge ,  median(timeremaining) AS timeremaining from {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution)
      
    elif mode == "max":
      
      query = ('select  max(voltage) AS voltage, max(current) AS  current, max(temperature) AS temperature,  max(stateofcharge) AS stateofcharge ,  max(timeremaining) AS timeremaining  from {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution)
      
    elif mode == "min":
      
      query = ('select  min(voltage) AS voltage, min(current) AS  current, min(temperature) AS temperature,  min(stateofcharge) AS stateofcharge ,  min(timeremaining) AS timeremaining  from {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution)
      
    else:
      
      query = ('select  mean(voltage) AS voltage, mean(current) AS  current, mean(temperature) AS temperature,  mean(stateofcharge) AS stateofcharge ,  mean(timeremaining) AS timeremaining  from {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution) 
 


    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))


            
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', response)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        pass

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate,  'status':'missing', 'update':'False', 'voltage':list(reversed(voltage)), 'current':list(reversed(current)), 'temperature':list(reversed(temperature)), 'stateofcharge':list(reversed(stateofcharge)), 'timeremaining':list(reversed(timeremaining))})     


    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate,  'status':'missing', 'update':'False', 'voltage':list(reversed(voltage)), 'current':list(reversed(current)), 'temperature':list(reversed(temperature)), 'stateofcharge':list(reversed(stateofcharge)), 'timeremaining':list(reversed(timeremaining))})     

    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)

    keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'
      value5 = '---'
      
      voltage=[]
      current=[]
      temperature=[]
      stateofcharge=[]
      timeremaining=[]

      ts =startepoch*1000

      points = list(response.get_points())

      #log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'
        value5 = '---'

        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)

        if point['voltage'] is not None: 
          value1 = convertfbunits(point['voltage'], convertunittype('volts', units))
        voltage.append({'epoch':ts, 'value':value1})
          
        if point['current'] is not None:         
          value2 = convertfbunits(point['current'], convertunittype('amps', units))
        current.append({'epoch':ts, 'value':value2})
          
        if point['temperature'] is not None:         
          value3 = convertfbunits(point['temperature'], convertunittype('temperature', units))
        temperature.append({'epoch':ts, 'value':value3})
                      
        if point['stateofcharge'] is not None:         
          value4 = convertfbunits(point['stateofcharge'], convertunittype('%', units))
        stateofcharge.append({'epoch':ts, 'value':value4})
          
        if point['timeremaining'] is not None:         
          value5 = convertfbunits(point['timeremaining'], convertunittype('time', units))
        timeremaining.append({'epoch':ts, 'value':value5})
               

      callback = request.args.get('callback')
      myjsondate= mydatetimetz.strftime("%B %d, %Y %H:%M:%S")  


      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','lat':value1, 'lng':value2,})
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','voltage':value1, 'current':value2, 'temperature':value3})
      return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','voltage':list(reversed(voltage)), 'current':list(reversed(current)), 'temperature':list(reversed(temperature)), 'stateofcharge':list(reversed(stateofcharge)), 'timeremaining':list(reversed(timeremaining))})     
        

     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error', update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })






@app.route('/freeboard_engine_aux')
@cross_origin()
def freeboard_engine_aux():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")

    Instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    units= request.args.get('units',"US")
    mytimezone = request.args.get('timezone',"UTC")
    mode =  request.args.get('mode',"mean")
    starttime = request.args.get('start','0')
    
    response = None
    
    try:
      
      if int(starttime) != 0:
        epochtimes = getendepochtimes(int(starttime), Interval)
        
      else:
        epochtimes = getepochtimes(Interval)

      
      startepoch = epochtimes[0]
      endepoch = epochtimes[1]
      if resolution == "":
        resolution = epochtimes[2]


      log.info("freeboard freeboard_engine_aux epochtimes %s %s %s", epochtimes[0], epochtimes[1],  epochtimes[2])

      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'
      value5 = '---'
      value6 = '---'
      value7 = '---'
      value8 = '---'
      value9 = '---'

      boost_pressure=[]
      coolant_pressure=[]
      fuel_pressure=[]
      oil_temp=[]
      egt_temperature=[]
      fuel_rate_average=[]
      instantaneous_fuel_economy=[]
      #tilt_or_trim=[]
      throttle_position=[]
      fuel_used=[]    

      mydatetime = datetime.datetime.now()
      myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")      


      deviceid = getedeviceid(deviceapikey)
      
      log.info("freeboard deviceid %s", deviceid)

      if deviceid == "":
          callback = request.args.get('callback')
          return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


      host = 'hilldale-670d9ee3.influxcloud.net' 
      port = 8086
      username = 'helmsmart'
      password = 'Salm0n16'
      database = 'pushsmart-cloud'

      measurement = "HelmSmart"
      measurement = 'HS_' + str(deviceid)




      serieskeys=" deviceid='"
      serieskeys= serieskeys + deviceid + "' AND "
      serieskeys= serieskeys +  " (sensor='engine_parameters_rapid_update' OR sensor='engine_parameters_dynamic'   OR  sensor='trip_parameters_engine') AND "   
      serieskeys= serieskeys +  " (instance='" + Instance + "') "

      """
      serieskeys=" deviceid='"
      serieskeys= serieskeys + deviceid + "' AND "
      serieskeys= serieskeys +  " (sensor='engine_parameters_rapid_update' OR sensor='engine_parameters_dynamic'  OR  sensor='temperature'  OR  sensor='trip_parameters_engine') AND "
      if Instance == 1:
        serieskeys= serieskeys +  " (type='NULL' OR type='Reserved 134')  AND "
      else:
        serieskeys= serieskeys +  " (type='NULL' OR type='Reserved 135')  AND "
        
      serieskeys= serieskeys +  " (instance='" + Instance + "') "
      """



      log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
      log.info("freeboard Create InfluxDB %s", database)


      dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

      if mode == "median":
        query = ('select  median(throttle_position) AS throttle_position, median(boost_pressure) AS  boost_pressure, median(coolant_pressure) AS coolant_pressure, median(fuel_pressure) AS fuel_pressure, median(oil_temp) AS oil_temp ,  median(egt_temp) AS egt_temperature , median(fuel_rate_average) AS fuel_rate_average  , median(instantaneous_fuel_economy) AS instantaneous_fuel_economy  , median(trip_fuel_used) AS fuel_used from {} '
                         'where {} AND time > {}s and time < {}s '
                         'group by time({}s)') \
                    .format( measurement, serieskeys,
                            startepoch, endepoch,
                            resolution) 

      elif mode == "max":
        query = ('select  max(throttle_position) AS throttle_position, max(boost_pressure) AS  boost_pressure, max(coolant_pressure) AS coolant_pressure, max(fuel_pressure) AS fuel_pressure, max(oil_temp) AS oil_temp ,  max(egt_temp) AS egt_temperature , max(fuel_rate_average) AS fuel_rate_average  , max(instantaneous_fuel_economy) AS instantaneous_fuel_economy, max(trip_fuel_used) AS fuel_used  from {} '
                         'where {} AND time > {}s and time < {}s '
                         'group by time({}s)') \
                    .format( measurement, serieskeys,
                            startepoch, endepoch,
                            resolution) 

      elif mode == "min":
        query = ('select  min(throttle_position) AS throttle_position, min(boost_pressure) AS  boost_pressure, min(coolant_pressure) AS coolant_pressure, min(fuel_pressure) AS fuel_pressure, min(oil_temp) AS oil_temp ,  min(egt_temp) AS egt_temperature , min(fuel_rate_average) AS fuel_rate_average  , min(instantaneous_fuel_economy) AS instantaneous_fuel_economy from, min(trip_fuel_used) AS fuel_used  from {} '
                         'where {} AND time > {}s and time < {}s '
                         'group by time({}s)') \
                    .format( measurement, serieskeys,
                            startepoch, endepoch,
                            resolution) 

      else:        
        query = ('select  mean(throttle_position) AS throttle_position, mean(boost_pressure) AS  boost_pressure, mean(coolant_pressure) AS coolant_pressure, mean(fuel_pressure) AS fuel_pressure, mean(oil_temp) AS oil_temp ,  mean(egt_temp) AS egt_temperature , mean(fuel_rate_average) AS fuel_rate_average  , mean(instantaneous_fuel_economy) AS instantaneous_fuel_economy, mean(trip_fuel_used) AS fuel_used from {} '
                         'where {} AND time > {}s and time < {}s '
                         'group by time({}s)') \
                    .format( measurement, serieskeys,
                            startepoch, endepoch,
                            resolution) 
     


      log.info("freeboard data Query %s", query)

      response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))

    except UnboundLocalError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))  

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))


    except InfluxDBServerError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))


    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', query)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing','update':'False','boost_pressure':list(reversed(boost_pressure)), 'coolant_pressure':list(reversed(coolant_pressure)), 'fuel_pressure':list(reversed(fuel_pressure)),'oil_temp':list(reversed(oil_temp)), 'egt_temperature':list(reversed(egt_temperature)), 'fuel_rate_average':list(reversed(fuel_rate_average)), 'instantaneous_fuel_economy':list(reversed(instantaneous_fuel_economy)),'fuel_used':list(reversed(fuel_used)), 'throttle_position':list(reversed(throttle_position))})     

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing','update':'False','boost_pressure':list(reversed(boost_pressure)), 'coolant_pressure':list(reversed(coolant_pressure)), 'fuel_pressure':list(reversed(fuel_pressure)),'oil_temp':list(reversed(oil_temp)), 'egt_temperature':list(reversed(egt_temperature)), 'fuel_rate_average':list(reversed(fuel_rate_average)), 'instantaneous_fuel_economy':list(reversed(instantaneous_fuel_economy)),'fuel_used':list(reversed(fuel_used)), 'throttle_position':list(reversed(throttle_position))})     

    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing','update':'False','boost_pressure':list(reversed(boost_pressure)), 'coolant_pressure':list(reversed(coolant_pressure)), 'fuel_pressure':list(reversed(fuel_pressure)),'oil_temp':list(reversed(oil_temp)), 'egt_temperature':list(reversed(egt_temperature)), 'fuel_rate_average':list(reversed(fuel_rate_average)), 'instantaneous_fuel_economy':list(reversed(instantaneous_fuel_economy)),'fuel_used':list(reversed(fuel_used)), 'throttle_position':list(reversed(throttle_position))})     

    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)

    keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'
      value5 = '---'
      value6 = '---'
      value7 = '---'
      value8 = '---'
      value9 = '---'

      boost_pressure=[]
      coolant_pressure=[]
      fuel_pressure=[]
      oil_temp=[]
      egt_temperature=[]
      fuel_rate_average=[]
      instantaneous_fuel_economy=[]
      throttle_position=[]
      fuel_used=[]
      
      ts =startepoch*1000
      
      points = list(response.get_points())


      #log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'
        value5 = '---'
        value6 = '---'
        value7 = '---'
        value8 = '---'
        value9 = '---'        

        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)
          
        if point['boost_pressure'] is not None:
          value1 = convertfbunits( point['boost_pressure'], convertunittype('pressure', units))
          boost_pressure.append({'epoch':ts, 'value':value1})
          
        
        if point['coolant_pressure'] is not None:
          value2 =  convertfbunits(point['coolant_pressure'], convertunittype('pressure', units))
        coolant_pressure.append({'epoch':ts, 'value':value2})
          
        
        if point['fuel_pressure'] is not None:
          value3=  convertfbunits(point['fuel_pressure'], convertunittype('pressure', units))
        fuel_pressure.append({'epoch':ts, 'value':value3})
          
        
        if point['oil_temp'] is not None:
          value4 =  convertfbunits(point['oil_temp'], convertunittype('temperature', units))
        oil_temp.append({'epoch':ts, 'value':value4})
          
        
        if point['egt_temperature'] is not None:
          value5 =  convertfbunits(point['egt_temperature'], convertunittype('temperature', units))
        egt_temperature.append({'epoch':ts, 'value':value5})
          
       
        if point['fuel_rate_average'] is not None:
          value6=  convertfbunits(point['fuel_rate_average'], convertunittype('flow', units))
        fuel_rate_average.append({'epoch':ts, 'value':value6})
          
        
        if point['instantaneous_fuel_economy'] is not None:
          value7 = convertfbunits(point['instantaneous_fuel_economy'],convertunittype('flow', units))
        instantaneous_fuel_economy.append({'epoch':ts, 'value':value7})

          
        
        if point['throttle_position'] is not None:
          value8 = convertfbunits(point['throttle_position'], convertunittype('%', units))
        throttle_position.append({'epoch':ts, 'value':value8})
          
         
        if point['fuel_used'] is not None:
          value9 = convertfbunits(point['fuel_used'], convertunittype('volume', units))
        fuel_used.append({'epoch':ts, 'value':value9})
          
         

      callback = request.args.get('callback')
      myjsondate= mydatetimetz.strftime("%B %d, %Y %H:%M:%S")  
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'rpm':value1, 'eng_temp':value2, 'oil_pressure':value3, 'alternator':value4, 'tripfuel':value5, 'fuel_rate':value6, 'fuel_level':value7, 'eng_hours':value8})
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'rpm':value1, 'eng_temp':value2, 'oil_pressure':value3, 'alternator':value4, 'tripfuel':value5, 'fuel_rate':value6, 'fuel_level':value7, 'eng_hours':value8})
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','rpm':list(reversed(speed)), 'eng_temp':list(reversed(engine_temp)), 'oil_pressure':list(reversed(oil_pressure)),'alternator':list(reversed(alternator_potential)), 'tripfuel':list(reversed(tripfuel)), 'fuel_rate':list(reversed(fuel_rate)), 'fuel_level':list(reversed(level)), 'eng_hours':list(reversed(total_engine_hours))})     
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'success','update':'True','boost_pressure':list(reversed(boost_pressure)), 'coolant_pressure':list(reversed(coolant_pressure)), 'fuel_pressure':list(reversed(fuel_pressure)),'oil_temp':list(reversed(oil_temp)), 'egt_temperature':list(reversed(egt_temperature)), 'fuel_rate_average':list(reversed(fuel_rate_average)), 'instantaneous_fuel_economy':list(reversed(instantaneous_fuel_economy)), 'throttle_position':list(reversed(throttle_position))})     
      return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'success','update':'True','boost_pressure':list(reversed(boost_pressure)), 'coolant_pressure':list(reversed(coolant_pressure)), 'fuel_pressure':list(reversed(fuel_pressure)),'oil_temp':list(reversed(oil_temp)), 'egt_temperature':list(reversed(egt_temperature)), 'fuel_rate_average':list(reversed(fuel_rate_average)), 'instantaneous_fuel_economy':list(reversed(instantaneous_fuel_economy)),  'fuel_used':list(reversed(fuel_used)), 'throttle_position':list(reversed(throttle_position))})     



    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error', update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })



@app.route('/freeboard_engine')
@cross_origin()
def freeboard_engine():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    Instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    units= request.args.get('units',"US")
    mytimezone = request.args.get('timezone',"UTC")
    mode = request.args.get('mode',"mean")
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]




    strvalue = ""
    value1 = '---'
    value2 = '---'
    value3 = '---'
    value4 = '---'
    value5 = '---'
    value6 = '---'
    value7 = '---'
    value8 = '---'


    speed=[]
    engine_temp=[]
    oil_pressure=[]
    alternator_potential=[]
    tripfuel=[]
    fuel_rate=[]
    level=[]
    total_engine_hours=[]

    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")      


    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)




    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " (sensor='engine_parameters_rapid_update' OR sensor='engine_parameters_dynamic'  OR  sensor='fluid_level') AND "
    serieskeys= serieskeys +  " (instance='" + Instance + "') "





    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

    if mode == "median":      
      query = ('select  median(speed) AS speed, median(engine_temp) AS  engine_temp, median(oil_pressure) AS oil_pressure, median(alternator_potential) AS alternator_potential, median(fuel_rate) AS fuel_rate ,  median(level) AS level , max(total_engine_hours) AS total_engine_hours from {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution)
      
    elif mode == "max":      
      query = ('select  max(speed) AS speed, max(engine_temp) AS  engine_temp, max(oil_pressure) AS oil_pressure, max(alternator_potential) AS alternator_potential, max(fuel_rate) AS fuel_rate ,  max(level) AS level , max(total_engine_hours) AS total_engine_hours from {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution) 

    elif mode == "min":      
      query = ('select  min(speed) AS speed, min(engine_temp) AS  engine_temp, min(oil_pressure) AS oil_pressure, min(alternator_potential) AS alternator_potential, min(fuel_rate) AS fuel_rate ,  min(level) AS level , max(total_engine_hours) AS total_engine_hours from {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution) 
  
    else:      
      query = ('select  mean(speed) AS speed, mean(engine_temp) AS  engine_temp, mean(oil_pressure) AS oil_pressure, mean(alternator_potential) AS alternator_potential, mean(fuel_rate) AS fuel_rate ,  mean(level) AS level , max(total_engine_hours) AS total_engine_hours from {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution) 

    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))

    except UnboundLocalError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))  

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))


    except InfluxDBServerError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))

      
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', query)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing','update':'False','rpm':list(reversed(speed)), 'eng_temp':list(reversed(engine_temp)), 'oil_pressure':list(reversed(oil_pressure)),'alternator':list(reversed(alternator_potential)), 'tripfuel':list(reversed(tripfuel)), 'fuel_rate':list(reversed(fuel_rate)), 'fuel_level':list(reversed(level)), 'eng_hours':list(reversed(total_engine_hours))})     

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing','update':'False','rpm':list(reversed(speed)), 'eng_temp':list(reversed(engine_temp)), 'oil_pressure':list(reversed(oil_pressure)),'alternator':list(reversed(alternator_potential)), 'tripfuel':list(reversed(tripfuel)), 'fuel_rate':list(reversed(fuel_rate)), 'fuel_level':list(reversed(level)), 'eng_hours':list(reversed(total_engine_hours))})     

    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing','update':'False','rpm':list(reversed(speed)), 'eng_temp':list(reversed(engine_temp)), 'oil_pressure':list(reversed(oil_pressure)),'alternator':list(reversed(alternator_potential)), 'tripfuel':list(reversed(tripfuel)), 'fuel_rate':list(reversed(fuel_rate)), 'fuel_level':list(reversed(level)), 'eng_hours':list(reversed(total_engine_hours))})     

    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)

    keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'
      value5 = '---'
      value6 = '---'
      value7 = '---'
      value8 = '---'


      speed=[]
      engine_temp=[]
      oil_pressure=[]
      alternator_potential=[]
      tripfuel=[]
      fuel_rate=[]
      level=[]
      total_engine_hours=[]

      ts =startepoch*1000       
      points = list(response.get_points())

      #log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'
        value5 = '---'
        value6 = '---'
        value7 = '---'
        value8 = '---'
        
        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)
          
        if point['speed'] is not None:
          value1 = convertfbunits( point['speed'], convertunittype('rpm', units))
          speed.append({'epoch':ts, 'value':value1})
          
        
        if point['engine_temp'] is not None:
          value2 =  convertfbunits(point['engine_temp'], convertunittype('temperature', units))
        engine_temp.append({'epoch':ts, 'value':value2})
          
        
        if point['oil_pressure'] is not None:
          value3=  convertfbunits(point['oil_pressure'], convertunittype('pressure', units))
        oil_pressure.append({'epoch':ts, 'value':value3})
          
        
        if point['alternator_potential'] is not None:
          value4 =  convertfbunits(point['alternator_potential'], convertunittype('volts', units))
        alternator_potential.append({'epoch':ts, 'value':value4})
          
        
        if point['fuel_rate'] is not None:
          value6 =  convertfbunits(point['fuel_rate'], convertunittype('flow', units))
        fuel_rate.append({'epoch':ts, 'value':value6})
          
       
        if point['level'] is not None:
          value7=  convertfbunits(point['level'], convertunittype('%', units))
        level.append({'epoch':ts, 'value':value7})
          
        
        if point['total_engine_hours'] is not None:
          value8 = convertfbunits(point['total_engine_hours'], convertunittype('hours', units))
        total_engine_hours.append({'epoch':ts, 'value':value8})
          

      callback = request.args.get('callback')
      myjsondate= mydatetimetz.strftime("%B %d, %Y %H:%M:%S")  
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'rpm':value1, 'eng_temp':value2, 'oil_pressure':value3, 'alternator':value4, 'tripfuel':value5, 'fuel_rate':value6, 'fuel_level':value7, 'eng_hours':value8})
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'rpm':value1, 'eng_temp':value2, 'oil_pressure':value3, 'alternator':value4, 'tripfuel':value5, 'fuel_rate':value6, 'fuel_level':value7, 'eng_hours':value8})
      return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','rpm':list(reversed(speed)), 'eng_temp':list(reversed(engine_temp)), 'oil_pressure':list(reversed(oil_pressure)),'alternator':list(reversed(alternator_potential)), 'tripfuel':list(reversed(tripfuel)), 'fuel_rate':list(reversed(fuel_rate)), 'fuel_level':list(reversed(level)), 'eng_hours':list(reversed(total_engine_hours))})     



    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error', update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })





@app.route('/freeboard_fluidlevels')
@cross_origin()
def freeboard_fluidlevels():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    Instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    units= request.args.get('units',"")
    mytimezone = request.args.get('timezone',"UTC")
    mode = request.args.get('mode',"mean")
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]



    strvalue = ""
    value1 = '---'
    value2 = '---'
    value3 = '---'
    value4 = '---'
    value5 = '---'
    value6 = '---'
    value7 = '---'
    value8 = '---'


    fuel_port=[]
    fuel_strbd=[]
    fuel_center=[]
    fuel_fwd=[]
    fuel_aft=[]
    fuel_day1=[]
    fuel_day2=[]
    fuel_day3=[]
    
    water_port=[]
    water_strbd=[]
    water_center=[]
    waste_port=[]
    waste_strbd=[]
    waste_center=[]

    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")      


    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)




    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " (sensor='fluid_level' ) "
    #serieskeys= serieskeys +  " (instance='" + Instance + "') "





    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

    if mode == "median":      
      query = ('select  median(level) AS level,  median(tank_capacity) AS capacity  from {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s), type, instance') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution)
      
    elif mode == "max":      
      query = ('select  max(level) AS level,  median(tank_capacity) AS capacity  from {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s), type, instance') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution) 

    elif mode == "min":      
      query = ('select  min(level) AS level,  median(tank_capacity) AS capacity  from {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s), type, instance') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution) 
  
    else:      
      query = ('select  mean(level) AS level,  median(tank_capacity) AS capacity  from {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s), type, instance') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution) 

    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))

    except UnboundLocalError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))  

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))


    except InfluxDBServerError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))

      
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', query)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'date_time':myjsondate,  'status':'missing','update':'False','fuel_port':list(reversed(fuel_port)), 'fuel_strbd':list(reversed(fuel_strbd)), 'fuel_center':list(reversed(fuel_center)),'water_port':list(reversed(water_port)), 'water_strbd':list(reversed(water_strbd)), 'water_center':list(reversed(water_center)), 'waste_port':list(reversed(waste_port)), 'waste_strbd':list(reversed(waste_strbd)), 'waste_center':list(reversed(waste_center))})     

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'date_time':myjsondate,  'status':'missing','update':'False','fuel_port':list(reversed(fuel_port)), 'fuel_strbd':list(reversed(fuel_strbd)), 'fuel_center':list(reversed(fuel_center)),'water_port':list(reversed(water_port)), 'water_strbd':list(reversed(water_strbd)), 'water_center':list(reversed(water_center)), 'waste_port':list(reversed(waste_port)), 'waste_strbd':list(reversed(waste_strbd)), 'waste_center':list(reversed(waste_center))})     

    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'date_time':myjsondate,  'status':'missing','update':'False','fuel_port':list(reversed(fuel_port)), 'fuel_strbd':list(reversed(fuel_strbd)), 'fuel_center':list(reversed(fuel_center)),'water_port':list(reversed(water_port)), 'water_strbd':list(reversed(water_strbd)), 'water_center':list(reversed(water_center)), 'waste_port':list(reversed(waste_port)), 'waste_strbd':list(reversed(waste_strbd)), 'waste_center':list(reversed(waste_center))})     

    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)

    keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)
    """
    for series in keys:
      log.info("freeboard Get InfluxDB series key %s", series)
      log.info("freeboard Get InfluxDB series tags %s ", series['tags'])
      tags = series['tags']

      log.info("freeboard Get InfluxDB series tag type  %s ", tags['type'])
      log.info("freeboard Get InfluxDB series tag instance  %s ", tags['instance'])

      fluidtype = tags['type']
      fluidinstance = tags['instance']
        #log.info("freeboard Get InfluxDB series values %s ", series['values'])
      
      log.info("freeboard Get InfluxDB series columns %s ", series['columns'])
      log.info("freeboard Get InfluxDB series values %s ", series['values'])
    """
      
    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    print('freeboard start processing data points:')
    
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'
      value5 = '---'
      value6 = '---'
      value7 = '---'
      value8 = '---'


      fuel_port=[]
      fuel_strbd=[]
      fuel_center=[]
      fuel_fwd=[]
      fuel_aft=[]
      fuel_day1=[]
      fuel_day2=[]
      fuel_day3=[]
      
      water_port=[]
      water_strbd=[]
      water_center=[]
      waste_port=[]
      waste_strbd=[]
      waste_center=[]

      ts =startepoch*1000       
      points = list(response.get_points())

      #log.info('freeboard:  InfluxDB-Cloud points%s:', points)


      for series in keys:
        #log.info("freeboard Get InfluxDB series key %s", series)
        #log.info("freeboard Get InfluxDB series tags %s ", series['tags'])
        tags = series['tags']

        #log.info("freeboard Get InfluxDB series tag type  %s ", tags['type'])
        #log.info("freeboard Get InfluxDB series tag instance  %s ", tags['instance'])

        fluidtype = int(tags['type'])
        fluidinstance = int(tags['instance'])

        #log.info("freeboard Get InfluxDB series tag type  %s ",fluidtype)
        #log.info("freeboard Get InfluxDB series tag instance  %s ", fluidinstance)


        points =  series['values']
        for point in points:
          #log.info('freeboard:  InfluxDB-Cloud point%s:', point)
          volume = '---'

          
          if point[0] is not None and  point[1] is not None:
            capacity = '---'
            level =  point[1] #is in percent 100% = 1.0

            # make asignment if not NULL
            if point[2] is not None:
              capacity = point[2] # is in liters
            
            mydatetimestr = str(point[0])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)
            

              
            if units == 'US': # we will calculate in gallons
              #check if we have a good capacity value before making volume calculation
              if capacity != '---':
                volgallons = convertfbunits( int(capacity), 21)
                volume =  float("{0:.1f}".format(level * 0.01 *  volgallons))
               
                
            elif units == 'metric': # we will calculate in liters
              #check if we have a good capacity value before making volume calculation
              if capacity != '---':
                volliters = capacity # is in liters
                volume =  float("{0:.1f}".format(level * 0.01 *  volliters))
                
            else : #default will be in %
                volume =  float("{0:.1f}".format(level * 1.0 ))

            
            if fluidtype == 0 and fluidinstance ==0 and volume != '---':
              fuel_port.append({'epoch':ts, 'value':volume})
            elif fluidtype == 0 and fluidinstance ==1 and volume != '---':
              fuel_strbd.append({'epoch':ts, 'value':volume})          
            elif fluidtype == 0 and fluidinstance ==2 and volume != '---':
              fuel_center.append({'epoch':ts, 'value':volume})

            elif fluidtype == 0 and fluidinstance ==3 and volume != '---':
              fuel_fwd.append({'epoch':ts, 'value':volume})          
            elif fluidtype == 0 and fluidinstance ==4 and volume != '---':
              fuel_aft.append({'epoch':ts, 'value':volume})

            elif fluidtype == 0 and fluidinstance ==5 and volume != '---':
              fuel_day1.append({'epoch':ts, 'value':volume})          
            elif fluidtype == 0 and fluidinstance ==6 and volume != '---':
              fuel_day2.append({'epoch':ts, 'value':volume})
            elif fluidtype == 0 and fluidinstance ==7 and volume != '---':
              fuel_day3.append({'epoch':ts, 'value':volume})          
 



              

            elif fluidtype == 1 and fluidinstance ==0 and volume != '---':
              water_port.append({'epoch':ts, 'value':volume})
            elif fluidtype == 1 and fluidinstance ==1 and volume != '---':
              water_strbd.append({'epoch':ts, 'value':volume})          
            elif fluidtype == 1 and fluidinstance ==2 and volume != '---':
              water_center.append({'epoch':ts, 'value':volume})          

            elif fluidtype == 2 and fluidinstance ==0 and volume != '---':
              waste_port.append({'epoch':ts, 'value':volume})
            elif fluidtype == 2 and fluidinstance ==1 and volume != '---':
              waste_strbd.append({'epoch':ts, 'value':volume})          
            elif fluidtype == 2 and fluidinstance ==2 and volume != '---':
              waste_center.append({'epoch':ts, 'value':volume})          

         
 
      callback = request.args.get('callback')
      myjsondate= mydatetimetz.strftime("%B %d, %Y %H:%M:%S")  
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'rpm':value1, 'eng_temp':value2, 'oil_pressure':value3, 'alternator':value4, 'tripfuel':value5, 'fuel_rate':value6, 'fuel_level':value7, 'eng_hours':value8})
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'rpm':value1, 'eng_temp':value2, 'oil_pressure':value3, 'alternator':value4, 'tripfuel':value5, 'fuel_rate':value6, 'fuel_level':value7, 'eng_hours':value8})
      return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','fuel_port':list(reversed(fuel_port)), 'fuel_strbd':list(reversed(fuel_strbd)), 'fuel_center':list(reversed(fuel_center)),'fuel_fwd':list(reversed(fuel_fwd)),'fuel_aft':list(reversed(fuel_aft)),'fuel_day1':list(reversed(fuel_day1)),'fuel_day2':list(reversed(fuel_day2)),'fuel_day3':list(reversed(fuel_day3)),'water_port':list(reversed(water_port)), 'water_strbd':list(reversed(water_strbd)), 'water_center':list(reversed(water_center)), 'waste_port':list(reversed(waste_port)), 'waste_strbd':list(reversed(waste_strbd)), 'waste_center':list(reversed(waste_center))})     


    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error', update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })



@app.route('/freeboard_ac_status')
@cross_origin()
def freeboard_ac_status():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    Instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    actype = request.args.get('type','UTIL')
    mytimezone = request.args.get('timezone',"UTC")
    mode = request.args.get('mode',"mean")
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]



    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)

    volts=[]
    amps=[]
    power=[]
    energy=[]
    energy_caluculated=[]

    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")      

    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    #serieskeys= serieskeys +  " (sensor='engine_parameters_rapid_update' OR sensor='engine_parameters_dynamic'  OR  sensor='fluid_level') AND "
    serieskeys= serieskeys +  " (sensor='ac_basic' OR sensor='ac_watthours'  ) "
    serieskeys= serieskeys +  "  AND type = '" + actype + "' AND "
    serieskeys= serieskeys +  " (instance='" + Instance + "') "





    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

    if mode == "median":
      
      query = ('select  median(ac_line_neutral_volts) AS volts, median(ac_amps) AS  amps, median(ac_watts) AS power, median(ac_kwatthours) AS energy, median(status) AS status FROM {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution)

      
    elif mode == "max":
      
      query = ('select  max(ac_line_neutral_volts) AS volts, max(ac_amps) AS  amps, max(ac_watts) AS power, max(ac_kwatthours) AS energy, max(status) AS status FROM {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution)


    elif mode == "min":
      
      query = ('select  min(ac_line_neutral_volts) AS volts, min(ac_amps) AS  amps, min(ac_watts) AS power, min(ac_kwatthours) AS energy, min(status) AS status FROM {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution)

    else:
      
      query = ('select  mean(ac_line_neutral_volts) AS volts, mean(ac_amps) AS  amps, mean(ac_watts) AS power, mean(ac_kwatthours) AS energy, mean(status) AS status FROM {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution) 
   


    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))

    except UnboundLocalError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))  

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))


    except InfluxDBServerError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))

      
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', query)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing' ,'volts':list(reversed(volts)), 'amps':list(reversed(amps)), 'power':list(reversed(power)), 'energy':list(reversed(energy)), 'energy_interval':list(reversed(energy_caluculated))})     

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing' ,'volts':list(reversed(volts)), 'amps':list(reversed(amps)), 'power':list(reversed(power)), 'energy':list(reversed(energy)), 'energy_interval':list(reversed(energy_caluculated))})     

    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'False', 'status':'missing' ,'volts':list(reversed(volts)), 'amps':list(reversed(amps)), 'power':list(reversed(power)), 'energy':list(reversed(energy)), 'energy_interval':list(reversed(energy_caluculated))})     

    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)

    keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'
      value5 = '---'
      value6 = '---'
      value7 = '---'
      value8 = '---'

      volts=[]
      amps=[]
      amps_rms=[]
      power=[]
      energy=[]
      status=[]
      energy_caluculated=[]
      energy_period = float(0.0)

      ts =startepoch*1000       
      points = list(response.get_points())

      #log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'
        value5 = '---'
        value6 = '---'
        value7 = '---'
        value8 = '---'

        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)
          
        
        if point['volts'] is not None:
          value1 = convertfbunits( point['volts'], 27)
        volts.append({'epoch':ts, 'value':value1})    
        
        if point['amps'] is not None:
          value2 =  convertfbunits(point['amps'],28)
          # Convert rms amps
          value8 = float(value2) * 0.7071
          energy_period = energy_period +(( float(value2)*float(value1)) * 0.001)
          
        amps.append({'epoch':ts, 'value':value2})
        amps_rms.append({'epoch':ts, 'value':value8})
        energy_caluculated.append({'epoch':ts, 'value':energy_period})
        
        if point['power'] is not None:
          value3=  convertfbunits(point['power'], 29)
        power.append({'epoch':ts, 'value':value3})

        if point['energy'] is not None:
          value4 =  convertfbunits(point['energy'], 31)
        energy.append({'epoch':ts, 'value':value4})
          
          
        if point['status'] is not None:
          value5=  convertfbunits(point['status'], 44)
        status.append({'epoch':ts, 'value':value5})
        
        

      #return jsonify(date_time=mydatetime, update=True, rpm=value1, eng_temp=value2, oil_pressure=value3, alternator=value4, boost=value5, fuel_rate=value6, fuel_level=value7, eng_hours=value8)
      callback = request.args.get('callback')
      myjsondate= mydatetimetz.strftime("%B %d, %Y %H:%M:%S")  
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'volts':value1, 'amps':value2, 'power':value3, 'energy':value4})
      return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','volts':list(reversed(volts)), 'amps':list(reversed(amps)), 'ampsrms':list(reversed(amps_rms)), 'power':list(reversed(power)), 'energy':list(reversed(energy)), 'status':list(reversed(status)), 'energy_interval':list(reversed(energy_caluculated))})     

    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error', update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })








@app.route('/freeboard_status')
@cross_origin()
def freeboard_status():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    Instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    mytimezone = request.args.get('timezone',"UTC")
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]




    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)

    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " sensor='seasmartswitch'  AND "
    serieskeys= serieskeys +  " (instance='" + Instance + "') "





    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

      
    query = ('select  median(bank0) AS bank0, median(bank1) AS  bank1 FROM {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution) 
 


    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))

    except UnboundLocalError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))  

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))


    except InfluxDBServerError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))

      
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', query)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })

    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })

    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)

    keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:
    
      strvalue = ""
      bankvalue1 = '---'
      bankvalue2 = '---'

      bank0=[]
      bank1=[]
      
      status0=[]
      status1=[]
      status2=[]
      status3=[]
      status4=[]
      status5=[]
      status6=[]
      status7=[]
      status8=[]
      status9=[]
      status10=[]
      status11=[]
      status12=[]
      status13=[]
      status14=[]
      status15=[]


      value0=0
      value1=0
      value2=0
      value3=0
      value4=0
      value5=0
      value6=0
      value7=0
      value8=0
      value9=0
      value10=0
      value11=0
      value12=0
      value13=0
      value14=0
      value15=0
       
      points = list(response.get_points())

      #log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)

        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)
  

        if point['bank0'] is not None:
          bankvalue1 =  point['bank0']
          bank0.append({'epoch':ts, 'value':bankvalue1})
          
          if bankvalue1 != '---':
            if bankvalue1 & 0x1 == 0x1:
              status0.append({'epoch':ts, 'value':1})
            else:
              status0.append({'epoch':ts, 'value':0})

              
            if bankvalue1 & 0x2 == 0x2:
              status1.append({'epoch':ts, 'value':1})
            else:
              status1.append({'epoch':ts, 'value':0})


            if bankvalue1 & 0x4 == 0x4:
              status2.append({'epoch':ts, 'value':1})
            else:
              status2.append({'epoch':ts, 'value':0})


            if bankvalue1 & 0x8 == 0x8:
              status3.append({'epoch':ts, 'value':1})
            else:
              status3.append({'epoch':ts, 'value':0})


            if bankvalue1 & 0x10 == 0x10:
              status4.append({'epoch':ts, 'value':1})
            else:
              status4.append({'epoch':ts, 'value':0})


            if bankvalue1 & 0x20 == 0x20:
              status5.append({'epoch':ts, 'value':1})
            else:
              status5.append({'epoch':ts, 'value':0})


            if bankvalue1 & 0x40 == 0x40:
              status6.append({'epoch':ts, 'value':1})
            else:
              status6.append({'epoch':ts, 'value':0})


            if bankvalue1 & 0x80 == 0x80:
              status7.append({'epoch':ts, 'value':1})
            else:
              status7.append({'epoch':ts, 'value':0})



        if point['bank1'] is not None:
          bankvalue2 =  point['bank1']
          bank1.append({'epoch':ts, 'value':bankvalue2})
          
          if bankvalue2 != '---':
            if bankvalue2 & 0x1 == 0x1:
              status8.append({'epoch':ts, 'value':1})
            else:
              status8.append({'epoch':ts, 'value':0})

              
            if bankvalue2 & 0x2 == 0x2:
              status9.append({'epoch':ts, 'value':1})
            else:
              status9.append({'epoch':ts, 'value':0})


            if bankvalue2 & 0x4 == 0x4:
              status10.append({'epoch':ts, 'value':1})
            else:
              status10.append({'epoch':ts, 'value':0})


            if bankvalue2 & 0x8 == 0x8:
              status11.append({'epoch':ts, 'value':1})
            else:
              status11.append({'epoch':ts, 'value':0})


            if bankvalue2 & 0x10 == 0x10:
              status12.append({'epoch':ts, 'value':1})
            else:
              status12.append({'epoch':ts, 'value':0})


            if bankvalue2 & 0x20 == 0x20:
              status13.append({'epoch':ts, 'value':1})
            else:
              status13.append({'epoch':ts, 'value':0})


            if bankvalue2 & 0x40 == 0x40:
              status146.append({'epoch':ts, 'value':1})
            else:
              status14.append({'epoch':ts, 'value':0})


            if bankvalue2 & 0x80 == 0x80:
              status15.append({'epoch':ts, 'value':1})
            else:
              status15.append({'epoch':ts, 'value':0})




      #return jsonify(date_time=mydatetime, update=True, rpm=value1, eng_temp=value2, oil_pressure=value3, alternator=value4, boost=value5, fuel_rate=value6, fuel_level=value7, eng_hours=value8)
      callback = request.args.get('callback')
      myjsondate= mydatetimetz.strftime("%B %d, %Y %H:%M:%S")  
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'bank0':value1, 'status0':status0, 'status1':status1, 'status2':status2, 'status3':status3, 'status4':status4, 'status5':status5, 'status6':status6, 'status7':status7, 'status8':status8, 'status9':status9, 'status10':status10, 'status11':status11, 'status12':status12, 'status13':status13, 'status14':status14, 'status15':status15})
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'status0':status0, 'status1':status1, 'status2':status2, 'status3':status3, 'status4':status4, 'status5':status5, 'status6':status6, 'status7':status7, 'status8':status8, 'status9':status9, 'status10':status10, 'status11':status11, 'status12':status12, 'status13':status13, 'status14':status14, 'status15':status15})
      return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','status0':list(reversed(status0)), 'status1':list(reversed(status1)), 'status2':list(reversed(status2)),'status3':list(reversed(status3)), 'status4':list(reversed(status4)), 'status5':list(reversed(status5)),'status6':list(reversed(status6)), 'status7':list(reversed(status7)), 'status8':list(reversed(status8)),'status9':list(reversed(status9)), 'status10':list(reversed(status10)), 'status11':list(reversed(status11)),'status12':list(reversed(status12)), 'status13':list(reversed(status13)), 'status14':list(reversed(status14)), 'status15':list(reversed(status15))})     

      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True',  'status0':status0, 'status1':status1, 'status2':status2, 'status3':status3, 'status4':status4, 'status5':status5, 'status6':status6, 'status7':status7})

    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error', update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })


@app.route('/freeboard_indicator_status')
@cross_origin()
def freeboard_indicator_status():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    Instance = request.args.get('instance','0')
    Indicator = request.args.get('indicator','0')
    resolution = request.args.get('resolution',"")
    mytimezone = request.args.get('timezone',"UTC")
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]



    switchstatus=[]
    mydatetime = datetime.datetime.now()
    myjsondate= mydatetime.strftime("%B %d, %Y %H:%M:%S")      
    


    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard freeboard_indicator_status deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)

    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " sensor='seasmartswitch'  AND "
    serieskeys= serieskeys +  " (instance='" + Instance + "') "


    parameter = "value" + str(Indicator)


    #log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    #log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

      
    #query = ('select  median(bank0) AS bank0, median(bank1) AS  bank1 FROM {} '
    query = ('select  median({}) as indicator '
                     ' FROM {} '             
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format(parameter,  measurement,  serieskeys,
                        startepoch, endepoch,
                        resolution) 
 


    log.info("freeboard freeboard_indicator_status data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))

    except UnboundLocalError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))  

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))


    except InfluxDBServerError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))

      
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', query)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','switch_bank':list(reversed(switchstatus))})    

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','switch_bank':list(reversed(switchstatus))})    

    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','switch_bank':list(reversed(switchstatus))})    

    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)

    keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:
    
      strvalue = ""


      switchstatus=[]
       
      points = list(response.get_points())

      #log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)

        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)
  
        
        if point['indicator'] is not None:
          statusvalues=(int(point['indicator']))
        else:
          statusvalues=(int(3))


        # check if array was all NONE  - if so disgard it
        if not (statusvalues == 3 ):
          switchstatus.append({'epoch':ts, 'value':statusvalues})
          #log.info('freeboard_switch_bank_status:  switchstatus%s:', switchstatus)          


      #return jsonify(date_time=mydatetime, update=True, rpm=value1, eng_temp=value2, oil_pressure=value3, alternator=value4, boost=value5, fuel_rate=value6, fuel_level=value7, eng_hours=value8)
      callback = request.args.get('callback')
      myjsondate= mydatetimetz.strftime("%B %d, %Y %H:%M:%S")  
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'bank0':value1, 'status0':status0, 'status1':status1, 'status2':status2, 'status3':status3, 'status4':status4, 'status5':status5, 'status6':status6, 'status7':status7, 'status8':status8, 'status9':status9, 'status10':status10, 'status11':status11, 'status12':status12, 'status13':status13, 'status14':status14, 'status15':status15})
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'status0':status0, 'status1':status1, 'status2':status2, 'status3':status3, 'status4':status4, 'status5':status5, 'status6':status6, 'status7':status7, 'status8':status8, 'status9':status9, 'status10':status10, 'status11':status11, 'status12':status12, 'status13':status13, 'status14':status14, 'status15':status15})
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','status0':list(reversed(status0)), 'status1':list(reversed(status1)), 'status2':list(reversed(status2)),'status3':list(reversed(status3)), 'status4':list(reversed(status4)), 'status5':list(reversed(status5)),'status6':list(reversed(status6)), 'status7':list(reversed(status7)), 'status8':list(reversed(status8)),'status9':list(reversed(status9)), 'status10':list(reversed(status10)), 'status11':list(reversed(status11)),'status12':list(reversed(status12)), 'status13':list(reversed(status13)), 'status14':list(reversed(status14)), 'status15':list(reversed(status15))})     
      return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','indicator':list(reversed(switchstatus))})     

      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True',  'status0':status0, 'status1':status1, 'status2':status2, 'status3':status3, 'status4':status4, 'status5':status5, 'status6':status6, 'status7':status7})

    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error', update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })




@app.route('/freeboard_indicator_runtime')
@cross_origin()
def freeboard_indicator_runtime():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    Instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    units= request.args.get('units',"US")
    mytimezone = request.args.get('timezone',"UTC")
    mode =  request.args.get('mode',"mean")
    indicator = request.args.get('indicator',"0")
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]




    strvalue = ""
    value1 = '---'
    value2 = '---'
    value3 = '---'
    value4 = '---'
    value5 = '---'
    value6 = '---'
    value7 = '---'
    value8 = '---'


    status=[]
    runtime=[]
    cycles=[]


    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")      


    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)




    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " (sensor='seasmartindicator') AND "
    serieskeys= serieskeys +  " (type='" + indicator + "') AND "   
    serieskeys= serieskeys +  " (instance='" + Instance + "') "

    """
    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " (sensor='engine_parameters_rapid_update' OR sensor='engine_parameters_dynamic'  OR  sensor='temperature'  OR  sensor='trip_parameters_engine') AND "
    if Instance == 1:
      serieskeys= serieskeys +  " (type='NULL' OR type='Reserved 134')  AND "
    else:
      serieskeys= serieskeys +  " (type='NULL' OR type='Reserved 135')  AND "
      
    serieskeys= serieskeys +  " (instance='" + Instance + "') "
    """



    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

    if mode == "median":
      query = ('select  median(value) AS status, median(runtime_sec) AS  runtime, median(cycles) AS cycles from {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution) 

    elif mode == "max":
      query = ('select  max(value) AS status, max(runtime_sec) AS  runtime, max(cycles) AS cycles from {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution) 

    elif mode == "min":
      query = ('select  min(value) AS status, min(runtime_sec) AS  runtime, min(cycles) AS cycles from {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution) 

    else:        
      query = ('select  mean(value) AS status, mean(runtime_sec) AS  runtime, mean(cycles) AS cycles from {} '
                       'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution) 
   


    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))

    except UnboundLocalError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))  

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))


    except InfluxDBServerError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))


    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', query)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing','update':'False','value':list(reversed(status)), 'runtime':list(reversed(runtime)), 'cycles':list(reversed(cycles ))}) 

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing','update':'False','value':list(reversed(status)), 'runtime':list(reversed(runtime)), 'cycles':list(reversed(cycles ))}) 
      
    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing','update':'False','value':list(reversed(status)), 'runtime':list(reversed(runtime)), 'cycles':list(reversed(cycles ))}) 
    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)

    keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'
      value5 = '---'
      value6 = '---'
      value7 = '---'
      value8 = '---'


      indicator=[]
      runtime=[]
      runtime_secs=[]
      cycles=[]


      ts =startepoch*1000
      
      points = list(response.get_points())


      #log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        value1 = '---'
        value2 = '---'
        value3 = '---'
        value4 = '---'
        value5 = '---'
        value6 = '---'
        value7 = '---'
        rttime = '---'

        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)
          
        if point['status'] is not None:
          value1 = convertfbunits( point['status'], convertunittype('', units))
        indicator.append({'epoch':ts, 'value':value1})
          
        
        if point['runtime'] is not None:
          #value2 = datetime.datetime.fromtimestamp(int(point['runtime'])).strftime('%H.%M')
          value2 = point['runtime']
          rthours = int(value2 / (60*60))
          rtmin = int((value2 % (60*60))/60)
          rttime = str(rthours) + "." + str(rtmin)
          #value2 =  convertfbunits(point['runtime'], convertunittype('time', units))
          #value2 =  convertfbunits(point['cycles'], convertunittype('', units))
        runtime.append({'epoch':ts, 'value':rttime})
        runtime_secs.append({'epoch':ts, 'value':value2})
          
        
        if point['cycles'] is not None:
          value3=  convertfbunits(point['cycles'], convertunittype('', units))
        cycles.append({'epoch':ts, 'value':value3})
          
        
                 

      callback = request.args.get('callback')
      myjsondate= mydatetimetz.strftime("%B %d, %Y %H:%M:%S")  
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'success','update':'True','indicator':list(reversed(status)), 'runtime':list(reversed(runtime)), 'cycles':list(reversed(cycles ))})     
      return '{0}({1})'.format(callback, {'date_time':myjsondate,  'status':'success','update':'True','indicator':list(reversed(indicator)), 'runtime_hours':list(reversed(runtime)), 'runtime_seconds':list(reversed(runtime_secs)), 'cycles':list(reversed(cycles ))})     
  






    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error', update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })




@app.route('/freeboard_dimmer_status')
@cross_origin()
def freeboard_dimmer_status():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    Instance = request.args.get('instance','0')
    dimmerIndex = request.args.get('indicator','0')
    resolution = request.args.get('resolution',"")
    mode =  request.args.get('mode',"mean")
    mytimezone = request.args.get('timezone',"UTC")
    response = None

    dimmerstatus=[]
    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")    
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]




    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard_dimmer_status deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)

    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " sensor='seasmartdimmer'  AND "
    serieskeys= serieskeys +  " (instance='" + Instance + "') "


    parameter = "value" + str(dimmerIndex)


    #log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    #log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

      
    #query = ('select  median(bank0) AS bank0, median(bank1) AS  bank1 FROM {} '


    if mode == "median":
      query = ('select  median({}) as dimmer '
                     ' FROM {} '             
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format(parameter,  measurement,  serieskeys,
                        startepoch, endepoch,
                        resolution) 
 
    elif mode == "max":
      query = ('select  max({}) as dimmer '
                     ' FROM {} '             
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format(parameter,  measurement,  serieskeys,
                        startepoch, endepoch,
                        resolution) 
 
    elif mode == "min":
      query = ('select  min({}) as dimmer '
                     ' FROM {} '             
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format(parameter,  measurement,  serieskeys,
                        startepoch, endepoch,
                        resolution) 
 

    else:        
      query = ('select  mean({}) as dimmer '
                     ' FROM {} '             
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format(parameter,  measurement,  serieskeys,
                        startepoch, endepoch,
                        resolution) 
 




    log.info("freeboard_dimmer_status data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard_dimmer_status: Type Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard_dimmer_status: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard_dimmer_status: Key Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard_dimmer_status: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard_dimmer_status: Index error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard_dimmer_status: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_dimmer_status: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_dimmer_status: AttributeError in InfluxDB  %s:  ' % str(e))

    except UnboundLocalError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))  

    except InfluxDBClientError as e:
      log.info('freeboard_dimmer_status: Exception Client Error in InfluxDB  %s:  ' % str(e))


    except InfluxDBServerError as e:
      log.info('freeboard_dimmer_status: Exception Client Error in InfluxDB  %s:  ' % str(e))

      
    except:
        log.info('freeboard_dimmer_status: Error in InfluxDB mydata append %s:', query)
        e = sys.exc_info()[0]
        log.info("freeboard_dimmer_status: Error: %s" % e)
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','dimmer_bank':list(reversed(dimmerstatus))})    

    if response is None:
        log.info('freeboard_dimmer_status: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','dimmer_bank':list(reversed(dimmerstatus))})    

    if not response:
        log.info('freeboard_dimmer_status: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','dimmer_bank':list(reversed(dimmerstatus))})    

    #log.info('freeboard_dimmer_status:  InfluxDB-Cloud response  %s:', response)

    keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:
    
      strvalue = ""


      dimmerstatus=[]
       
      points = list(response.get_points())

      #log.info('freeboard_dimmer_status:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard_dimmer_status:  InfluxDB-Cloud point%s:', point)

        if point['time'] is not None: 
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)
  
        
        if point['dimmer'] is not None:
          statusvalues=(int(point['dimmer']))
        else:
          statusvalues=(int(255))


        # check if array was all NONE  - if so disgard it
        if not (statusvalues == 255 ):
          dimmerstatus.append({'epoch':ts, 'value':statusvalues})
          #log.info('freeboard_switch_bank_status:  dimmerstatus%s:', dimmerstatus)          


      #return jsonify(date_time=mydatetime, update=True, rpm=value1, eng_temp=value2, oil_pressure=value3, alternator=value4, boost=value5, fuel_rate=value6, fuel_level=value7, eng_hours=value8)
      callback = request.args.get('callback')
      myjsondate= mydatetimetz.strftime("%B %d, %Y %H:%M:%S")  
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'bank0':value1, 'status0':status0, 'status1':status1, 'status2':status2, 'status3':status3, 'status4':status4, 'status5':status5, 'status6':status6, 'status7':status7, 'status8':status8, 'status9':status9, 'status10':status10, 'status11':status11, 'status12':status12, 'status13':status13, 'status14':status14, 'status15':status15})
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'status0':status0, 'status1':status1, 'status2':status2, 'status3':status3, 'status4':status4, 'status5':status5, 'status6':status6, 'status7':status7, 'status8':status8, 'status9':status9, 'status10':status10, 'status11':status11, 'status12':status12, 'status13':status13, 'status14':status14, 'status15':status15})
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','status0':list(reversed(status0)), 'status1':list(reversed(status1)), 'status2':list(reversed(status2)),'status3':list(reversed(status3)), 'status4':list(reversed(status4)), 'status5':list(reversed(status5)),'status6':list(reversed(status6)), 'status7':list(reversed(status7)), 'status8':list(reversed(status8)),'status9':list(reversed(status9)), 'status10':list(reversed(status10)), 'status11':list(reversed(status11)),'status12':list(reversed(status12)), 'status13':list(reversed(status13)), 'status14':list(reversed(status14)), 'status15':list(reversed(status15))})     
      return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','dimmer':list(reversed(dimmerstatus))})     

      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True',  'status0':status0, 'status1':status1, 'status2':status2, 'status3':status3, 'status4':status4, 'status5':status5, 'status6':status6, 'status7':status7})

    except TypeError as e:
        log.info('freeboard_dimmer_status: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard_dimmer_status: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard_dimmer_status: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard_dimmer_status: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard_dimmer_status: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard_dimmer_status: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard_dimmer_status: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard_dimmer_status: Index Error in InfluxDB mydata append %s:  ' % str(e))   

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_dimmer_status: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_dimmer_status: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_dimmer_status: Exception Error in InfluxDB  %s:  ' % str(e))     
    
    except:
        log.info('freeboard_dimmer_status: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard_dimmer_status: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error', update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })


@app.route('/freeboard_get_engine_values')
@cross_origin()
def freeboard_get_engine_values():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    mode= request.args.get('mode',"last")
    units= request.args.get('units',"US")
    mytimezone = request.args.get('timezone',"UTC")
    response = None

    dimmerstatus=[]
    temperature=[]
    dimmer1=[]
    dimmer2=[]
    dimmer3=[]
    dimmer4=[]

      
    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")    
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]




    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard freeboard_get_engine_values deviceid %s", deviceid)

    if deviceid == "":
      return jsonify(result="ERROR")

    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)


    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " (sensor='engine_parameters_rapid_update' OR sensor='engine_parameters_dynamic'  OR  sensor='fluid_level') AND "
    serieskeys= serieskeys +  " (instance='" + instance + "') "


    #log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    #log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

    #SELECT LAST()...WHERE time > now() - 1h       
    #query = ('select  median(bank0) AS bank0, median(bank1) AS  bank1 FROM {} '
    log.info("freeboard_get_engine_values mode = %s", mode)
    
    if mode == 'min':
      #log.info("freeboard_get_weather_values mode is min")
      query = ('select  min(engine_temp)  as engine_temp, '
                       'min(alternator_potential)  as alt_volts, '
                       'min(oil_pressure) as oil_pressure, '
                        'min(speed)  as rpm, '
                        'min(level)  as fuel_level '
                       ' FROM {} '             
                       'where {} AND time > {}s and time < {}s') \
                  .format( measurement, serieskeys, startepoch, endepoch ) 
   
    elif mode == 'max':      
      query = ('select  max(engine_temp)  as engine_temp, '
                       'max(alternator_potential)  as alt_volts, '
                       'max(oil_pressure) as oil_pressure, '
                        'max(speed)  as rpm, '
                        'max(level)  as fuel_level '
                       ' FROM {} '             
                       'where {} AND time > {}s and time < {}s') \
                  .format( measurement, serieskeys, startepoch, endepoch ) 
   


    elif mode == 'avg':      
      query = ('select  percentile(engine_temp, 50)  as engine_temp, '
                       'percentile(alternator_potential, 50)  as alt_volts, '
                       'percentile(oil_pressure, 50) as oil_pressure, '
                        'percentile(speed, 50)  as rpm, '
                        'percentile(level, 50)  as fuel_level '
                       ' FROM {} '             
                       'where {} AND time > {}s and time < {}s') \
                  .format( measurement, serieskeys, startepoch, endepoch ) 
   
   


    else:      
      query = ('select  last(engine_temp)  as engine_temp, '
                       'last(alternator_potential)  as alt_volts, '
                       'last(oil_pressure) as oil_pressure, '
                        'last(speed)  as rpm, '
                        'last(level)  as fuel_level '
                       ' FROM {} '             
                       'where {} AND time > {}s and time < {}s') \
                  .format( measurement, serieskeys, startepoch, endepoch ) 
  
   


    log.info("freeboard_get_engine_values data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))

    except UnboundLocalError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))  

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))


    except InfluxDBServerError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))

      
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', query)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        return jsonify(result="error")

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        return jsonify(result="error")

      
    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        return jsonify(result="error")


    keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'

    #log.info("freeboard jsonkey..%s", jsonkey )
    try:

      points = list(response.get_points())

      log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        
        if point['engine_temp'] is not None:
          engine_temp=convertfbunits(point['engine_temp'],  convertunittype('temperature', units))
        else:
          engine_temp='unavailable'

        if point['alt_volts'] is not None:
          alt_volts=convertfbunits(point['alt_volts'], convertunittype('volts', units))
        else:
          alt_volts='unavailable'

        if point['oil_pressure'] is not None:
          oil_pressure=convertfbunits(point['oil_pressure'], convertunittype('pressure', units))
        else:
          oil_pressure='unavailable'
          
        if point['rpm'] is not None:
          rpm=convertfbunits(point['rpm'], convertunittype('rpm', units))
        else:
          rpm='unavailable'

        if point['fuel_level'] is not None:
          fuel_level=convertfbunits(point['fuel_level'],  convertunittype('%', units)) 
        else:
          fuel_level='unavailable'


        
      return jsonify(result="OK",  instance=instance,  engine_temp=engine_temp, alt_volts=alt_volts, oil_pressure=oil_pressure, rpm=rpm, fuel_level=fuel_level)


    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)

        return jsonify(result="ERROR")

    return jsonify(result="ERROR")


@app.route('/freeboard_get_rain_gauge')
@cross_origin()
def freeboard_get_rain_gauge():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    mode= request.args.get('mode',"last")
    units= request.args.get('units',"US")
    mytimezone = request.args.get('timezone',"UTC")
    response = None

    accumulation=[]
    duration=[]
    rate=[]
    peak=[]


      
    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")    
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]




    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard freeboard_get_rain_gauge deviceid %s", deviceid)

    if deviceid == "":
      return jsonify(result="ERROR")

    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)


    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " sensor='rain_gauge' "



    #log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    #log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

    #SELECT LAST()...WHERE time > now() - 1h       
    #query = ('select  median(bank0) AS bank0, median(bank1) AS  bank1 FROM {} '
    log.info("freeboard_get_rain_gauge mode = %s", mode)
    
    if mode == 'min':
      #log.info("freeboard_get_weather_values mode is min")
      query = ('select  min(accumulation)  as accumulation, '
                       'min("duration")  as "duration", '
                        'min(rate)  as rate, '
                        'min(peak)  as peak '
                       ' FROM {} '             
                       'where {} AND time > {}s and time < {}s') \
                  .format( measurement, serieskeys, startepoch, endepoch ) 
   
    elif mode == 'max':      
      query = ('select  max(accumulation)  as accumulation, '
                       'max("duration")  as "duration", '
                        'max(rate)  as rate, '
                        'max(peak)  as peak '
                       ' FROM {} '             
                       'where {} AND time > {}s and time < {}s') \
                  .format( measurement, serieskeys, startepoch, endepoch ) 
   


    elif mode == 'avg':      
      query = ('select  percentile(accumulation,50)  as accumulation, '
                       'percentile("duration",50)  as "duration", '
                        'percentile(rate,50)  as rate, '
                        'percentile(peak,50)  as peak '
                       ' FROM {} '             
                       'where {} AND time > {}s and time < {}s') \
                  .format( measurement, serieskeys, startepoch, endepoch ) 
   
   


    else:      
      query = ('select  last(accumulation)  as accumulation, '
                       'last("duration)  as "duration", '
                        'last(rate)  as rate, '
                        'last(peak)  as peak '
                       ' FROM {} '             
                       'where {} AND time > {}s and time < {}s') \
                  .format( measurement, serieskeys, startepoch, endepoch ) 
  
   


    log.info("freeboard freeboard_get_rain_gauge data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))

    except UnboundLocalError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))  

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))


    except InfluxDBServerError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))

      
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', query)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        return jsonify(result="error")

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        return jsonify(result="error")

      
    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        return jsonify(result="error")


    keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:

      points = list(response.get_points())

      log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        
        if point['accumulation'] is not None:
          accumulation=convertfbunits(point['accumulation'],  convertunittype('accumulation', units))
        else:
          accumulation='unavailable'

        if point['duration'] is not None:
          duration=convertfbunits(point['duration'], 10)
        else:
          duration='unavailable'

        if point['rate'] is not None:
          rate=convertfbunits(point['rate'], 26)
        else:
          rate='unavailable'
          
        if point['peak'] is not None:
          peak=convertfbunits(point['peak'], 16)
        else:
          peak='unavailable'




        
      return jsonify(result="OK",  instance=instance,  accumulation=accumulation, duration=duration, rate=rate, peak=peak)


    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)

        return jsonify(result="ERROR")

    return jsonify(result="ERROR")



  

@app.route('/freeboard_get_weather_values')
@cross_origin()
def freeboard_get_weather_values():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    mode= request.args.get('mode',"last")
    units= request.args.get('units',"US")
    mytimezone = request.args.get('timezone',"UTC")
    response = None

    dimmerstatus=[]
    temperature=[]
    dimmer1=[]
    dimmer2=[]
    dimmer3=[]
    dimmer4=[]

      
    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")    
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]



    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard freeboard_get_weather_values deviceid %s", deviceid)

    if deviceid == "":
      return jsonify(result="ERROR")

    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)


    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " (sensor='environmental_data' OR sensor='wind_data') AND instance='0' AND (type='Outside Temperature' OR type='Outside Humidity' OR type='TWIND True North')"



    #log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    #log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

    #SELECT LAST()...WHERE time > now() - 1h       
    #query = ('select  median(bank0) AS bank0, median(bank1) AS  bank1 FROM {} '
    log.info("freeboard_get_weather_values mode = %s", mode)
    
    if mode == 'min':
      #log.info("freeboard_get_weather_values mode is min")
      query = ('select  min(temperature)  as temperature, '
                       'min(atmospheric_pressure)  as atmospheric_pressure, '
                       'min(humidity) as humidity, '
                        'min(wind_direction)  as wind_direction, '
                        'min(wind_speed)  as wind_speed '
                       ' FROM {} '             
                       'where {} AND time > {}s and time < {}s') \
                  .format( measurement, serieskeys, startepoch, endepoch ) 
   
    elif mode == 'max':      
      query = ('select  max(temperature)  as temperature, '
                       'max(atmospheric_pressure)  as atmospheric_pressure, '
                       'max(humidity) as humidity, '
                        'max(wind_direction)  as wind_direction, '
                        'max(wind_speed)  as wind_speed '
                       ' FROM {} '             
                       'where {} AND time > {}s and time < {}s') \
                  .format( measurement, serieskeys, startepoch, endepoch ) 
   


    elif mode == 'avg':      
      query = ('select  percentile(temperature,50)  as temperature, '
                       'percentile(atmospheric_pressure,50)  as atmospheric_pressure, '
                       'percentile(humidity,50) as humidity, '
                        'percentile(wind_direction,50)  as wind_direction, '
                        'percentile(wind_speed,50)  as wind_speed '
                       ' FROM {} '             
                       'where {} AND time > {}s and time < {}s') \
                  .format( measurement, serieskeys, startepoch, endepoch ) 
   
   


    else:      
      query = ('select  last(temperature)  as temperature, '
                       'last(atmospheric_pressure)  as atmospheric_pressure, '
                       'last(humidity) as humidity, '
                        'last(wind_direction)  as wind_direction, '
                        'last(wind_speed)  as wind_speed '
                       ' FROM {} '             
                       'where {} AND time > {}s and time < {}s') \
                  .format( measurement, serieskeys, startepoch, endepoch ) 
  
   


    log.info("freeboard freeboard_get_weather_values data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))

    except UnboundLocalError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))  

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))


    except InfluxDBServerError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))

      
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', query)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        return jsonify(result="error")

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        return jsonify(result="error")

      
    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        return jsonify(result="error")


    keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:

      points = list(response.get_points())

      log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        log.info('freeboard:  InfluxDB-Cloud point%s:', point)
        
        if point['temperature'] is not None:
          temperature=convertfbunits(point['temperature'],  convertunittype('temperature', units))
        else:
          temperature='unavailable'

        if point['atmospheric_pressure'] is not None:
          atmospheric_pressure=convertfbunits(point['atmospheric_pressure'], 10)
        else:
          atmospheric_pressure='unavailable'

        if point['humidity'] is not None:
          humidity=convertfbunits(point['humidity'], 26)
        else:
          humidity='unavailable'
          
        if point['wind_direction'] is not None:
          wind_direction=convertfbunits(point['wind_direction'], 16)
        else:
          wind_direction='unavailable'

        if point['wind_speed'] is not None:
          wind_speed=convertfbunits(point['wind_speed'],  convertunittype('speed', units)) 
        else:
          wind_speed='unavailable'


        
      return jsonify(result="OK",  instance=instance,  temperature=temperature, atmospheric_pressure=atmospheric_pressure, humidity=humidity, wind_direction=wind_direction, wind_speed=wind_speed)


    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)

        return jsonify(result="ERROR")

    return jsonify(result="ERROR")

  

@app.route('/freeboard_get_weather_minmax_value')
@cross_origin()
def freeboard_get_weather_minmax_value():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    instance = request.args.get('instance','0')
    parameter = request.args.get('parameter',"air temp")
    mode= request.args.get('mode',"last")
    units= request.args.get('units',"US")
    mytimezone= request.args.get('timezone',"UTC")
    response = None

    dimmerstatus=[]
    temperature=[]


      
    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")    
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]



    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard freeboard_get_weather_minmax_value deviceid %s", deviceid)

    if deviceid == "":
      return jsonify(result="ERROR")

    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)


    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "

    if parameter == 'air temp':
      serieskeys= serieskeys +  " (sensor='environmental_data' ) AND instance='0' AND (type='Outside Temperature' )"
      query_parameter = 'temperature'

    elif parameter == 'barometric pressure':
      serieskeys= serieskeys +  " (sensor='environmental_data' ) AND instance='0' AND (type='Outside Temperature' )"
      query_parameter = 'atmospheric_pressure'
      
    elif parameter == 'humidity':
      serieskeys= serieskeys +  " (sensor='environmental_data' ) AND instance='0' AND ( type='Outside Humidity' )"
      query_parameter = 'humidity'
      
    elif parameter == 'wind speed':
      serieskeys= serieskeys +  " (sensor='wind_data') AND instance='0' AND ( type='TWIND True North')"
      query_parameter = 'wind_speed'
      
    elif parameter == 'wind direction':
      serieskeys= serieskeys +  " ( sensor='wind_data') AND instance='0' AND ( type='TWIND True North')"
      query_parameter = 'wind_direction'

    else :
      serieskeys= serieskeys +  " (sensor='environmental_data' ) AND instance='0' AND (type='Outside Temperature' )"
      query_parameter = 'temperature'

      
    #log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    #log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

    #SELECT LAST()...WHERE time > now() - 1h       
    #query = ('select  median(bank0) AS bank0, median(bank1) AS  bank1 FROM {} '
    log.info("freeboard_get_weather_minmax_value mode = %s", mode)
    
    if mode == 'min':
      #log.info("freeboard_get_weather_values mode is min")
      query = ('select  min({})  as {}, '
                       ' time as time'
                       ' FROM {} '             
                       'where {} AND time > {}s and time < {}s') \
                  .format( query_parameter, query_parameter, measurement, serieskeys, startepoch, endepoch ) 
   
    elif mode == 'max':      
      query = ('select  max({})  as {}, '
                       ' time as time'
                       ' FROM {} '             
                       'where {} AND time > {}s and time < {}s') \
                  .format( query_parameter, query_parameter, measurement, serieskeys, startepoch, endepoch ) 
   


    elif mode == 'avg':      
      query = ('select  percentile({},50)  as {}, '
                       ' time as time'
                       ' FROM {} '             
                       'where {} AND time > {}s and time < {}s') \
                  .format( query_parameter, query_parameter, measurement, serieskeys, startepoch, endepoch ) 
   
   


    else:      
      query = ('select  last({})  as {}, '
                       'last(atmospheric_pressure)  as atmospheric_pressure, '
                       ' time as time'
                       ' FROM {} '             
                       'where {} AND time > {}s and time < {}s') \
                  .format( query_parameter, query_parameter, measurement, serieskeys, startepoch, endepoch ) 
  
   


    log.info("freeboard freeboard_get_weather_minmax_value data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))

    except UnboundLocalError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))  

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))


    except InfluxDBServerError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))

      
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', query)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        return jsonify(result="error")

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        return jsonify(result="error")

      
    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        return jsonify(result="error")


    keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:
      
      temperature='unavailable'
      atmospheric_pressure='unavailable'
      humidity='unavailable'
      wind_direction='unavailable'
      wind_speed='unavailable'
      myjsondate='unavailable'

      
      points = list(response.get_points())

      log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        log.info('freeboard:  InfluxDB-Cloud point%s:', point)

        if parameter == 'air temp':        
          if point['temperature'] is not None:
            temperature=convertfbunits(point['temperature'],  convertunittype('temperature', units))

            
        if parameter == 'barometric pressure':     
          if point['atmospheric_pressure'] is not None:
            atmospheric_pressure=convertfbunits(point['atmospheric_pressure'], 10)

            
        if parameter == 'humidity':     
          if point['humidity'] is not None:
            humidity=convertfbunits(point['humidity'], 26)

            
        if parameter == 'wind direction':                 
          if point['wind_direction'] is not None:
            wind_direction=convertfbunits(point['wind_direction'], 16)

            
        if parameter == 'wind speed':     
          if point['wind_speed'] is not None:
            wind_speed=convertfbunits(point['wind_speed'],  convertunittype('speed', units)) 


        if point['time'] is not None:
          #mydatetimestr = int(point['time']*1000)
          #mydatetime = datetime.datetime.fromtimestamp(mydatetimestr)
          #myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")
          #myjsondate = mydatetime.strftime("%A %B, %Y at %I,%M,%S, %Z")
          mydatetimestr = str(point['time'])
          #myjsondate = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')
          mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')
          log.info('freeboard_get_weather_minmax_value:  mydatetime %s:', mydatetime)
          #myjsondate = mydatetime.strftime( '%A, %B, %Y, at %I,%M,%p, %Z')
          #localtz = timezone('US/Pacific')
          #mydatetimetz = localtz.localize(mydatetime)

          mydatetime_utctz = mydatetime.replace(tzinfo=timezone('UTC'))
          log.info('freeboard_get_weather_minmax_value:  mydatetimetz %s:', mydatetime_utctz)

          #mytimezone= "US/Pacific"
          mydatetimetz = mydatetime_utctz.astimezone(timezone(mytimezone))
          log.info('freeboard_get_weather_minmax_value:  mydatetimetz %s:', mydatetimetz)
          
          #myjsondate = mydatetimetz.strftime( '%A,  at %I %M,%p, G M T')
          myjsondate = mydatetimetz.strftime( '%A,  at, %I:%M,%p, %Z')
          #from pytz import timezone
          #localtz = timezone('Europe/Lisbon')
          #dt_aware = localtz.localize(dt_unware)
          #def ms_to_datetime(epoch_ms):
          #return datetime.datetime.fromtimestamp(epoch_ms / 1.0, tz=pytz.utc)
          #location.timezone = 'US/Pacific'
          #timezone = location.timezone
          #log.info("getSunRiseSet:  in proc getSunRiseSet Astral timezone: %s", timezone)
          #mylocal = pytz.timezone(timezone)
          
          
      return jsonify(result="OK",  time=myjsondate, instance=instance,  temperature=temperature, atmospheric_pressure=atmospheric_pressure, humidity=humidity, wind_direction=wind_direction, wind_speed=wind_speed)


    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)

        return jsonify(result="ERROR")

    return jsonify(result="ERROR")

  



@app.route('/freeboard_get_dimmer_values')
@cross_origin()
def freeboard_get_dimmer_values():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    gwtype = request.args.get('type',"hub")
    Interval = request.args.get('interval',"5min")
    instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    mytimezone = request.args.get('timezone',"UTC")
    response = None

    dimmerstatus=[]
    dimmer0=[]
    dimmer1=[]
    dimmer2=[]
    dimmer3=[]
    dimmer4=[]

      
    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")    
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]



    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard_get_dimmer_values deviceid %s", deviceid)

    if deviceid == "":
      return jsonify(result="ERROR")

    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)

    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " sensor='seasmartdimmer'  AND "
    serieskeys= serieskeys +  " (instance='" + instance + "') "





    #log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    #log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

    #SELECT LAST()...WHERE time > now() - 1h       
    #query = ('select  median(bank0) AS bank0, median(bank1) AS  bank1 FROM {} '
    query = ('select  last(value0) as dv0, '
                     'last(value1) as dv1, '
                     'last(value2) as dv2, '
                      'last(value3) as dv3, '
                      'last(value4) as dv4 '
                     ' FROM {} '             
                     'where {} ') \
                .format( measurement, serieskeys ) 
 


    log.info("freeboard_get_dimmer_values data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard_dimmer_values: Type Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard_dimmer_values: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard_dimmer_values: Key Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard_dimmer_values: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard_dimmer_values: Name Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard_dimmer_values: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard_dimmer_values: Index error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard_dimmer_values: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_dimmer_values: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_dimmer_values: AttributeError in InfluxDB  %s:  ' % str(e))

    except UnboundLocalError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_dimmer_values: AttributeError in InfluxDB  %s:  ' % str(e))  

    except InfluxDBClientError as e:
      log.info('freeboard_dimmer_values: Exception Client Error in InfluxDB  %s:  ' % str(e))


    except InfluxDBServerError as e:
      log.info('freeboard_dimmer_values: Exception Client Error in InfluxDB  %s:  ' % str(e))

      
    except:
        log.info('freeboard_dimmer_values: Error in InfluxDB mydata append %s:', query)
        e = sys.exc_info()[0]
        log.info("freeboard_dimmer_values: Error: %s" % e)
        return jsonify(result="ERROR")

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        return jsonify(result="ERROR")

      
    if not response:
        log.info('freeboard_dimmer_values: InfluxDB Query has no data ')
        return jsonify(result="ERROR")


    keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:

      points = list(response.get_points())

      log.info('freeboard_get_dimmer_values:  InfluxDB-Cloud points%s:', points)

      for point in points:
        log.info('freeboard_get_dimmer_values:  InfluxDB-Cloud point%s:', point)
        
        if point['dv0'] is not None:
          dimmer0=int(point['dv0'])
        else:
          dimmer0='---'

        if point['dv1'] is not None:
          dimmer1=int(point['dv1'])
        else:
          dimmer1='---'

        if point['dv2'] is not None:
          dimmer2=int(point['dv2'])
        else:
          dimmer2='---'
          
        if point['dv3'] is not None:
          dimmer3=int(point['dv3'])
        else:
          dimmer3='---'

        if point['dv4'] is not None:
          dimmer4=int(point['dv4'])
        else:
          dimmer4='---'

        
      return jsonify(result="OK",  instance=instance, oldvalue0=dimmer0, oldvalue1=dimmer1, oldvalue2=dimmer2, oldvalue3=dimmer3, oldvalue4=dimmer4)


    except TypeError as e:
        log.info('freeboard_dimmer_values: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard_dimmer_values: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard_dimmer_values: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard_dimmer_values: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard_dimmer_values: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard_dimmer_values: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard_dimmer_values: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard_dimmer_values: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_dimmer_values: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_dimmer_values: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_dimmer_values: Exception Error in InfluxDB  %s:  ' % str(e))     
    
    except:
        log.info('freeboard_dimmer_values: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard_dimmer_values: Error in geting freeboard ststs %s:  ' % e)

        return jsonify(result="ERROR")

    return jsonify(result="ERROR")

  

@app.route('/freeboard_dimmer_values')
@cross_origin()
def freeboard_dimmer_values():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    gwtype = request.args.get('type',"hub")
    Interval = request.args.get('interval',"5min")
    Instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    mytimezone = request.args.get('timezone',"UTC")
    response = None

    dimmerstatus=[]
    dimmer0=[]
    dimmer1=[]
    dimmer2=[]
    dimmer3=[]
    dimmer4=[]

      
    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")    
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]



    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard freeboard_dimmer_values deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)

    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " sensor='seasmartdimmer'  AND "
    serieskeys= serieskeys +  " (instance='" + Instance + "') "





    #log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    #log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

      
    #query = ('select  median(bank0) AS bank0, median(bank1) AS  bank1 FROM {} '
    query = ('select  median(value0) as dv0, '
                     'median(value1) as dv1, '
                     'median(value2) as dv2, '
                      'median(value3) as dv3, '
                      'median(value4) as dv4 '
                     ' FROM {} '             
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution) 
 


    log.info("freeboard_dimmer_values data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))

    except UnboundLocalError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))  

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))


    except InfluxDBServerError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))

      
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', query)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing','update':'False','dimmer0_value':list(reversed(dimmer0)),'dimmer1_value':list(reversed(dimmer1)),'dimmer2_value':list(reversed(dimmer2)),'dimmer3_value':list(reversed(dimmer3)),'dimmer4_value':list(reversed(dimmer4))})     


    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing','update':'False','dimmer0_value':list(reversed(dimmer0)),'dimmer1_value':list(reversed(dimmer1)),'dimmer2_value':list(reversed(dimmer2)),'dimmer3_value':list(reversed(dimmer3)),'dimmer4_value':list(reversed(dimmer4))})     

    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'status':'missing','update':'False','dimmer0_value':list(reversed(dimmer0)),'dimmer1_value':list(reversed(dimmer1)),'dimmer2_value':list(reversed(dimmer2)),'dimmer3_value':list(reversed(dimmer3)),'dimmer4_value':list(reversed(dimmer4))})     

    #log.info('freeboard_dimmer_values:  InfluxDB-Cloud response  %s:', response)

    keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard_dimmer_values Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    
    #log.info("freeboard_dimmer_values jsonkey..%s", jsonkey )
    try:
    
      strvalue = ""

      
      status0=0x255
      status1=0x255
      status2=0x255
      status3=0x255
      status4=0x255


      dimmerstatus=[]
      dimmer0=[]
      dimmer1=[]
      dimmer2=[]
      dimmer3=[]
      dimmer4=[]
      dimmer_adc3=[]
      dimmer_override=[]
      dimmer_switchoverride=[]
      dimmer_photooverride=[]
      dimmer_status=[]
      dimmer_motion=[]
       
      points = list(response.get_points())

      #log.info('freeboard_dimmer_values:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard_dimmer_values:  InfluxDB-Cloud point%s:', point)
        
        if point['time'] is not None:
          mydatetimestr = str(point['time'])
          ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)

          # convert string to datetime opject
          mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
          ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

          # set timezone of new datetime opbect
          mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
          ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

          ## This dosnt work for python 3.11 anymore
          ## throws an OverFlow error
          ##dtt = mydatetimetz.timetuple()
          ##ts = int(mktime(dtt)*1000)
          ## So we need to convert datetime directly to seconds and add in timezone offesets

          # get seconds offset for selected timezone
          tzoffset = mydatetimetz.utcoffset().total_seconds()
          ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

          # adjust GMT time for slected timezone for display purposes
          ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
          ##log.info('freeboard_environmental:: ts %s:  ' % ts)

        statusvalues=[]
        
        if point['dv0'] is not None:
          dimmer0.append({'epoch':ts, 'value':int(point['dv0'])})
        else:
          dimmer0.append({'epoch':ts, 'value':'---'})

        
        if point['dv1'] is not None:
          if gwtype == "mesh":
            dimmer1.append({'epoch':ts, 'value':float("{0:.2f}".format(point['dv1'] * 0.1 ) )})

          else:
            dimmer1.append({'epoch':ts, 'value':int(point['dv1'])})
            
        else:
          dimmer1.append({'epoch':ts, 'value':'---'})

        
        if point['dv2'] is not None:

          if gwtype == "mesh":
            dimmer2.append({'epoch':ts, 'value':int(point['dv2'])})
            dimmer_adc3.append({'epoch':ts, 'value':float("{0:.2f}".format(point['dv2'] * 0.1 ) )})
          else:
            dimmer2.append({'epoch':ts, 'value':int(point['dv2'])})
          
        else:
          dimmer2.append({'epoch':ts, 'value':'---'})


        
        if point['dv3'] is not None:
          
          if gwtype == "mesh":
            dimmer3.append({'epoch':ts, 'value':float("{0:.2f}".format(point['dv3'] * 1.0 ) )})

          else:
            dimmer3.append({'epoch':ts, 'value':int(point['dv3'])})
            
        else:
          dimmer3.append({'epoch':ts, 'value':'---'})

        
        if point['dv4'] is not None:
          dimmer4.append({'epoch':ts, 'value':int(point['dv4'])})
          dimmer_override.append({'epoch':ts, 'value':((int(point['dv4']) & 0x40) )})
          dimmer_status.append({'epoch':ts, 'value':(int(point['dv4']) & 0x0F)})
          dimmer_motion.append({'epoch':ts, 'value':((int(point['dv4']) & 0x10) )})
          dimmer_photooverride.append({'epoch':ts, 'value':((int(point['dv4']) & 0x20) )})
          dimmer_switchoverride.append({'epoch':ts, 'value':((int(point['dv4']) & 0x80) )})

          
        else:
          dimmer4.append({'epoch':ts, 'value':'---'})
          dimmer_override.append({'epoch':ts, 'value':'---'})
          dimmer_status.append({'epoch':ts, 'value':'---'})
          dimmer_motion.append({'epoch':ts, 'value':'---'})
          dimmer_photooverride.append({'epoch':ts, 'value':'---'})       
          dimmer_switchoverride.append({'epoch':ts, 'value':'---'})   

        #log.info('freeboard_dimmer_values:  statusvalues%s:', statusvalues)
        #statusvalues.append(int(Instance))

        # check if array was all NONE  - if so disgard it
        #if not (statusvalues[0] == 255 and statusvalues[1] == 255 and statusvalues[2] == 255 and statusvalues[3] == 255 and statusvalues[4] == 255 ):
        #  dimmerstatus.append(statusvalues)
   

      callback = request.args.get('callback')
      myjsondate= mydatetimetz.strftime("%B %d, %Y %H:%M:%S")

      if gwtype == "mesh":

        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','dimmer_value':list(reversed(dimmer0)),'dimmer_dio':list(reversed(dimmer2)),'dimmer_adc3':list(reversed(dimmer_adc3)),'dimmer_adc':list(reversed(dimmer3)),'dimmer_adc2':list(reversed(dimmer1)),'dimmer_motion':list(reversed(dimmer_motion)),'dimmer_override':list(reversed(dimmer_override)), 'dimmer_switchoverride':list(reversed(dimmer_switchoverride)), 'dimmer_photooverride':list(reversed(dimmer_photooverride)), 'dimmer_status':list(reversed(dimmer_status))})     

      else:
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','dimmer0_value':list(reversed(dimmer0)),'dimmer1_value':list(reversed(dimmer1)),'dimmer2_value':list(reversed(dimmer2)),'dimmer3_value':list(reversed(dimmer3)),'dimmer4_value':list(reversed(dimmer4))})     

    except TypeError as e:
        log.info('freeboard_dimmer_values: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard_dimmer_values: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard_dimmer_values: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard_dimmer_values: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard_dimmer_values: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard_dimmer_values: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard_dimmer_values: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard_dimmer_values: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_dimmer_values: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_dimmer_values: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_dimmer_values: Exception Error in InfluxDB  %s:  ' % str(e))     
    
    except:
        log.info('freeboard_dimmer_values: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard_dimmer_values: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error', update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  

@app.route('/freeboard_switch_bank_status')
@cross_origin()
def freeboard_switch_bank_status():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('interval',"5min")
    Instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    mytimezone = request.args.get('timezone',"UTC")
    response = None

    switchstatus=[]
    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")    
    
    starttime = request.args.get('start','0')
    
    response = None
    

    if int(starttime) != 0:
      epochtimes = getendepochtimes(int(starttime), Interval)
      
    else:
      epochtimes = getepochtimes(Interval)

    
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    if resolution == "":
      resolution = epochtimes[2]




    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard freeboard_bank_status deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)

    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " sensor='seasmartswitch'  AND "
    serieskeys= serieskeys +  " (instance='" + Instance + "') "





    #log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    #log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

      
    #query = ('select  median(bank0) AS bank0, median(bank1) AS  bank1 FROM {} '
    query = ('select  median(value0) as sw0, '
                     'median(value1) as sw1, '
                     'median(value2) as sw2, '
                      'median(value3) as sw3, '
                      'median(value4) as sw4, '
                      'median(value5) as sw5, '
                      'median(value6) as sw6, '
                      'median(value7) as sw7, '
                      'median(value8) as sw8, '
                      'median(value9) as sw9, '
                      'median(value10) as sw10, '
                      'median(value11) as sw11, '
                      'median(value12) as sw12, '
                      'median(value13) as sw13, '
                      'median(value14) as sw14, '
                      'median(value15) as sw15 '
                     ' FROM {} '             
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution) 
 


    log.info("freeboard freeboard_bank_status data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))

    except UnboundLocalError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))  

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))


    except InfluxDBServerError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))

      
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', query)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','switch_bank':list(reversed(switchstatus))})    

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','switch_bank':list(reversed(switchstatus))})    

    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','switch_bank':list(reversed(switchstatus))})    

    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)

    keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:
    
      strvalue = ""
      bankvalue0 = 0xFFFF
      bankvalue1 = 0xFFFF

      byte0 = 0xFF
      byte1 = 0xFF
      byte2 = 0xFF
      byte3 = 0xFF
      
      status0=0x03
      status1=0x03
      status2=0x03
      status3=0x03
      status4=0x03
      status5=0x03
      status6=0x03
      status7=0x03
      status8=0x03
      status9=0x03
      status10=0x03
      status11=0x03
      status12=0x03
      status13=0x03
      status14=0x03
      status15=0x03

      switchstatus=[]
       
      points = list(response.get_points())

      #log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        #log.info('freeboard:  InfluxDB-Cloud point%s:', point)

        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)

          
  
        statusvalues=[]
        
        if point['sw0'] is not None:
          statusvalues.append(int(point['sw0']))
        else:
          statusvalues.append(int(3))

        
        if point['sw1'] is not None:
          statusvalues.append(int(point['sw1']))
        else:
          statusvalues.append(int(3))

        
        if point['sw2'] is not None:
          statusvalues.append(int(point['sw2']))
        else:
          statusvalues.append(int(3))

        
        if point['sw3'] is not None:
          statusvalues.append(int(point['sw3']))
        else:
          statusvalues.append(int(3))

        
        if point['sw4'] is not None:
          statusvalues.append(int(point['sw4']))
        else:
          statusvalues.append(int(3))

        
        if point['sw5'] is not None:
          statusvalues.append(int(point['sw5']))
        else:
          statusvalues.append(int(3))

        
        if point['sw6'] is not None:
          statusvalues.append(int(point['sw6']))
        else:
          statusvalues.append(int(3))

        
        if point['sw7'] is not None:
          statusvalues.append(int(point['sw7']))
        else:
          statusvalues.append(int(3))

        
        if point['sw8'] is not None:
          statusvalues.append(int(point['sw8']))
        else:
          statusvalues.append(int(3))

        
        if point['sw9'] is not None:
          statusvalues.append(int(point['sw9']))
        else:
          statusvalues.append(int(3))

        
        if point['sw10'] is not None:
          statusvalues.append(int(point['sw10']))
        else:
          statusvalues.append(int(3))

        
        if point['sw11'] is not None:
          statusvalues.append(int(point['sw11']))
        else:
          statusvalues.append(int(3))

        
        if point['sw12'] is not None:
          statusvalues.append(int(point['sw12']))
        else:
          statusvalues.append(int(3))

        
        if point['sw13'] is not None:
          statusvalues.append(int(point['sw13']))
        else:
          statusvalues.append(int(3))

        
        if point['sw14'] is not None:
          statusvalues.append(int(point['sw14']))
        else:
          statusvalues.append(int(3))

        
        if point['sw15'] is not None:
          statusvalues.append(int(point['sw15']))
        else:
          statusvalues.append(int(3))

        #log.info('freeboard_switch_bank_status:  statusvalues%s:', statusvalues)
        statusvalues.append(int(Instance))

        # check if array was all NONE  - if so disgard it
        if not (statusvalues[0] == 3 and statusvalues[1] == 3 and statusvalues[2] == 3 and statusvalues[3] == 3 and statusvalues[4] == 3 and statusvalues[5] == 3 and statusvalues[6] == 3 and statusvalues[7] == 3 and statusvalues[8] == 3 and statusvalues[9] == 3 and statusvalues[10] == 3 and statusvalues[11] == 3 and statusvalues[12] == 3 and statusvalues[13] == 3 and statusvalues[14] == 3 and statusvalues[15] == 3):
          switchstatus.append(statusvalues)
          #log.info('freeboard_switch_bank_status:  switchstatus%s:', switchstatus)          




          
        """
        if point['bank0'] is not None:
          bankvalue0 =  point['bank0']

          if bankvalue0 & 0x1 == 0x1:
            status0=0x01
          else:
            status0=0x00
            
          if bankvalue0 & 0x2 == 0x2:
            status1=0x04
          else:
            status1=0x00

          if bankvalue0 & 0x4 == 0x4:
            status2=0x10
          else:
            status2=0x00

          if bankvalue0 & 0x8 == 0x8:
            status3=0x40
          else:
            status3=0x00

          byte0= status0 | status1 | status2 | status3
            

          if bankvalue0 & 0x10 == 0x10:
            status4=0x01
          else:
            status4=0x00

          if bankvalue0 & 0x20 == 0x20:
            status5=0x04
          else:
            status5=0x00

          if bankvalue0 & 0x40 == 0x40:
            status6=0x10
          else:
            status6=0x00

          if bankvalue0 & 0x80 == 0x80:
            status7=0x40
          else:
            status7=0x00

          byte1= status4 | status5 | status6 | status7

        if point['bank1'] is not None:
          bankvalue1 =  point['bank1']


          if bankvalue1 & 0x1 == 0x1:
            status8=0x01
          else:
            status8=0x00
            
          if bankvalue1 & 0x2 == 0x2:
            status9=0x04
          else:
            status9=0x00

          if bankvalue1 & 0x4 == 0x4:
            status10=0x10
          else:
            status10=0x00

          if bankvalue1 & 0x8 == 0x8:
            status11=0x40
          else:
            status11=0x00

          byte2= status8 | status9 | status10 | status11
            

          if bankvalue1 & 0x10 == 0x10:
            status12=0x01
          else:
            status12=0x00

          if bankvalue1 & 0x20 == 0x20:
            status13=0x04
          else:
            status13=0x00

          if bankvalue1 & 0x40 == 0x40:
            status14=0x10
          else:
            status14=0x00

          if bankvalue1 & 0x80 == 0x80:
            status15=0x40
          else:
            status15=0x00

          byte3= status12 | status13 | status14 | status15    

        log.info('freeboard:  InfluxDB-Cloud bankvalues %s:%s', bankvalue0, bankvalue1)
        
        #switchstates =  "{:02X}".format(int(Instance))  +  "{:01X}".format(int(byte1))  +  "{:01X}".format(int(byte0)) +  "{:01X}".format(int(byte3)) +  "{:01X}".format(int(byte3))

        switchstates = []

        switchstates.append("{:02X}".format(int(Instance)))
        switchstates.append("{:01X}".format(int(byte0)))
        switchstates.append("{:01X}".format(int(byte1)))
        switchstates.append("{:01X}".format(int(byte2)))
        switchstates.append("{:01X}".format(int(byte3)))
  
        log.info('freeboard:  InfluxDB-Cloud switchstates %s:', switchstates)
          
        switchstatus.append({'epoch':ts, 'value':switchstates})
          
        """       


      #return jsonify(date_time=mydatetime, update=True, rpm=value1, eng_temp=value2, oil_pressure=value3, alternator=value4, boost=value5, fuel_rate=value6, fuel_level=value7, eng_hours=value8)
      callback = request.args.get('callback')
      myjsondate= mydatetimetz.strftime("%B %d, %Y %H:%M:%S")  
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'bank0':value1, 'status0':status0, 'status1':status1, 'status2':status2, 'status3':status3, 'status4':status4, 'status5':status5, 'status6':status6, 'status7':status7, 'status8':status8, 'status9':status9, 'status10':status10, 'status11':status11, 'status12':status12, 'status13':status13, 'status14':status14, 'status15':status15})
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'status0':status0, 'status1':status1, 'status2':status2, 'status3':status3, 'status4':status4, 'status5':status5, 'status6':status6, 'status7':status7, 'status8':status8, 'status9':status9, 'status10':status10, 'status11':status11, 'status12':status12, 'status13':status13, 'status14':status14, 'status15':status15})
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','status0':list(reversed(status0)), 'status1':list(reversed(status1)), 'status2':list(reversed(status2)),'status3':list(reversed(status3)), 'status4':list(reversed(status4)), 'status5':list(reversed(status5)),'status6':list(reversed(status6)), 'status7':list(reversed(status7)), 'status8':list(reversed(status8)),'status9':list(reversed(status9)), 'status10':list(reversed(status10)), 'status11':list(reversed(status11)),'status12':list(reversed(status12)), 'status13':list(reversed(status13)), 'status14':list(reversed(status14)), 'status15':list(reversed(status15))})     
      return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','switch_bank':list(reversed(switchstatus))})     

      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True',  'status0':status0, 'status1':status1, 'status2':status2, 'status3':status3, 'status4':status4, 'status5':status5, 'status6':status6, 'status7':status7})

    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error', update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  

@app.route('/get_dbstat')
@cross_origin()
def get_dbstat():

  deviceapikey = request.args.get('apikey','')
  Interval = request.args.get('interval',"5min")
  rollup = request.args.get('rollup',"sum")

  resolution = request.args.get('resolution',"")
  mytimezone = request.args.get('timezone',"UTC")
  response = None


  mydatetime = datetime.datetime.now()
  myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")    
  
  starttime = request.args.get('start','0')
  
  response = None
  

  if int(starttime) != 0:
    epochtimes = getendepochtimes(int(starttime), Interval)
    
  else:
    epochtimes = getepochtimes(Interval)

  
  startepoch = epochtimes[0]
  endepoch = epochtimes[1]
  if resolution == "":
    resolution = epochtimes[2]

  


  useremail = getuseremail(deviceapikey)
    
  log.info("freeboard get_dbstat useremail %s", useremail)



  deviceid = getedeviceid(deviceapikey)
  
  log.info("freeboard get_dbstat deviceid %s", deviceid)

  if deviceid == "":
      callback = request.args.get('callback')
      return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })

  measurement = "HelmSmart"
  measurement = 'HS_' + str(deviceid)


  devicename = getedevicename(deviceapikey)
  log.info("freeboard get_dbstat devicename %s", devicename)  

  response = None
  
  measurement = "HelmSmartDB"
  
  stat0 = '---'
  stat1 = '---'
  stat2 = '---'
  stat3 = '---'
  stat4 = '---'
  stat5 = '---'
  stat6 = '---'
  stat7 = '---'
  stat8 = '---'
  stat9 = '---'
  stat10 = '---'
  stat11 = '---'
  stat12 = '---'
  stat13 = '---'
  stat14 = '---'
  stat15 = '---'
  stat16 = '---'


  #conn = db_pool.getconn()

  #cursor = conn.cursor()
  #cursor.execute("select deviceid, devicename from user_devices")
  #records = cursor.fetchall()

  #db_pool.putconn(conn)   



  try:
   

    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'


    db = InfluxDBCloud(host, port, username, password, database,  ssl=True)
     

    
    start = datetime.datetime.fromtimestamp(float(startepoch))
    

    end = datetime.datetime.fromtimestamp(float(endepoch))
    resolutionstr = "PT" + str(resolution) + "S"

    #rollup = "mean"


    query = ('select {}(records) AS records FROM {} '
                     'where time > {}s and time < {}s '
                     'group by *, time({}s) ') \
                .format(rollup,  measurement, 
                        startepoch, endepoch,
                        resolution) 

    """         

    query = ('select {}(records) AS records FROM {} '
                     'where time > {}s and time < {}s '
                     'group by *, time({}s) LIMIT 1') \
                .format(rollup,  measurement, 
                        startepoch, endepoch,
                        resolution) 
    """        
    #query =(' select records as records from HelmSmartDB')      
      
    
    log.info("get_dbstat inFlux-cloud Query %s", query)
    

    try:
      response= db.query(query)
    except:
      e = sys.exc_info()[0]
      log.info('get_dbstat: Error in geting inFluxDB data %s:  ' % e)
        
      return jsonify( message='Error in inFluxDB query 2', status='error')
      #raise

    
    #return jsonify(results=response)
    
    #response =  shim.read_multi(keys=[SERIES_KEY], start=start, end=end, period=resolutionstr, rollup="mean" )
    
    #print 'inFluxDB read :', response.response.successful

    
    if not response:
      #print 'inFluxDB Exception1:', response.response.successful, response.response.reason 
      return jsonify( message='No response to return 1' , status='error')


    #if not response.points:
    #  #print 'inFluxDB Exception2:', response.response.successful, response.response.reason 
    #  return jsonify( message='No data to return 2', status='error')

    print('get_dbstat processing data headers:')
    jsondata=[]
    jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    print('get_dbstat start processing data points:')
    #log.info("freeboard Get InfluxDB response %s", response)

    keys = response.raw.get('series',[])
    #log.info("freeboard Get InfluxDB series keys %s", keys)




    strvalue=""
    
    for series in keys:
      #log.info("freeboard Get InfluxDB series key %s", series)
      #log.info("freeboard Get InfluxDB series tags %s ", series['tags'])
      #log.info("freeboard Get InfluxDB series columns %s ", series['columns'])
      #log.info("freeboard Get InfluxDB series values %s ", series['values'])

      """        
      values = series['values']
      for value in values:
        log.info("freeboard Get InfluxDB series time %s", value[0])
        log.info("freeboard Get InfluxDB series mean %s", value[1])
      """

      tag = series['tags']
      #log.info("freeboard Get InfluxDB series tags2 %s ", tag)

      #mydatetimestr = str(fields['time'])
      strvaluekey = {'Series': series['tags'], 'start': startepoch,  'end': endepoch}
      jsonkey.append(strvaluekey)        

      #log.info("freeboard Get InfluxDB series tags3 %s ", tag['deviceid'])
      # initialize datetime to default
      mydatetime = datetime.datetime.now()
      
      for point in series['values']:
        fields = {}
        for key, val in zip(series['columns'], point):
          fields[key] = val
          
        #log.info("freeboard Get InfluxDB series points %s , %s", fields['time'], fields['records'])

        if fields['records'] != None:

          #devicename = ""
          #deviceid = tag['deviceid']
          #for record in records:
          #log.info("get_dbstat deviceid %s - devicename %s", record[0], record[1])    
          if tag['deviceid'] == deviceid:
            #devicename = record[1]

            #strvalue = {'epoch': fields['time'], 'source':tag['deviceid'], 'name':devicename, 'value': fields['records']}        
            #strvalue = {'epoch': fields['time'],  'records': fields['records']}
            #strvalue = {'epoch': fields['time'],  'value': fields['records']}
            mydatetimestr = str(fields['time'])
            #log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            #log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            #log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            #log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            #log.info('freeboard_environmental:: ts %s:  ' % ts)
            
            strvalue = {'epoch': ts,  'value': fields['records']}
            jsondata.append(strvalue)





    jsondata = sorted(jsondata,key=itemgetter('epoch'), reverse=True)

    total = 0

    for stat in jsondata:
      if stat['value'] != None:
        total = total + float(stat['value'])

    """        
    if len(jsondata) > 0:
      mydatetimestr = str(jsondata[0]['epoch'])
      stat0 = str(jsondata[0]['source']) + ":" + str(jsondata[0]['name']) + " = " +  str(jsondata[0]['value'])
    """        

    #mydatetimestr = str(jsondata[0]['epoch'])
    #mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')

    #log.info('freeboard: freeboard returning data values wind_speed:%s, wind_direction:%s  ', stat1,stat2)            

    callback = request.args.get('callback')
    # use the last valid timestamp for the update
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")


    #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'Interval':str(Interval),'update':'True','total':int(total),'stat0':})
    return '{0}({1})'.format(callback, {'date_time':myjsondate, 'Interval':str(Interval),'Resolution':resolution, 'DeviceID':deviceid,'DeviceName':devicename,'total records':int(total),'records':jsondata})


  except TypeError as e:
      #log.info('get_dbstat: Type Error in InfluxDB mydata append %s:  ', response)
      log.info('get_dbstat: Type Error in InfluxDB mydata append %s:  ' % str(e))
          
  except KeyError as e:
      #log.info('get_dbstat: Key Error in InfluxDB mydata append %s:  ', response)
      log.info('get_dbstat: Key Error in InfluxDB mydata append %s:  ' % str(e))

  except NameError as e:
      #log.info('get_dbstat: Name Error in InfluxDB mydata append %s:  ', response)
      log.info('get_dbstat: Name Error in InfluxDB mydata append %s:  ' % str(e))
          
  except IndexError as e:
      #log.info('get_dbstat: Index error in InfluxDB mydata append %s:  ', response)
      log.info('get_dbstat: Index Error in InfluxDB mydata append %s:  ' % str(e))  

  except ValueError as e:
    #log.info('get_dbstat: Index error in InfluxDB mydata append %s:  ', response)
    log.info('get_dbstat: Value Error in InfluxDB  %s:  ' % str(e))

  except AttributeError as e:
    #log.info('get_dbstat: Index error in InfluxDB mydata append %s:  ', response)
    log.info('get_dbstat: AttributeError in InfluxDB  %s:  ' % str(e))     

  except InfluxDBClientError as e:
    log.info('get_dbstat: Exception Error in InfluxDB  %s:  ' % str(e))     
  
  except:
    log.info('get_dbstat: Error in geting freeboard response %s:  ', strvalue)
    e = sys.exc_info()[0]
    log.info('get_dbstat: Error in geting freeboard ststs %s:  ' % e)
    return jsonify( message='error processing data 3' , status='error')        

  callback = request.args.get('callback')
  return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  

@app.route('/get_dbstats')
@cross_origin()
def get_dbstats():

  deviceapikey = request.args.get('apikey','')
  Interval = request.args.get('Interval',"5min")
  rollup = request.args.get('rollup',"sum")

  response = None

  
  starttime = 0

  epochtimes = getepochtimes(Interval)
  startepoch = epochtimes[0]
  endepoch = epochtimes[1]
  resolution = epochtimes[2]

  useremail = getuseremail(deviceapikey)
    
  log.info("freeboard get_dbstats useremail %s", useremail)

  response = None
  
  measurement = "HelmSmartDB"
  stat0 = '---'
  stat1 = '---'
  stat2 = '---'
  stat3 = '---'
  stat4 = '---'
  stat5 = '---'
  stat6 = '---'
  stat7 = '---'
  stat8 = '---'
  stat9 = '---'
  stat10 = '---'
  stat11 = '---'
  stat12 = '---'
  stat13 = '---'
  stat14 = '---'
  stat15 = '---'
  stat16 = '---'


  conn = db_pool.getconn()

  cursor = conn.cursor()
  cursor.execute("select deviceid, devicename from user_devices")
  records = cursor.fetchall()

  db_pool.putconn(conn)   



  try:
   

    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'


    db = InfluxDBCloud(host, port, username, password, database,  ssl=True)
     

    
    start = datetime.datetime.fromtimestamp(float(startepoch))
    

    end = datetime.datetime.fromtimestamp(float(endepoch))
    resolutionstr = "PT" + str(resolution) + "S"

    #rollup = "mean"

 

    query = ('select {}(records) AS records FROM {} '
                     'where time > {}s and time < {}s '
                     'group by *, time({}s) LIMIT 1') \
                .format(rollup,  measurement, 
                        startepoch, endepoch,
                        resolution) 

    #query =(' select records as records from HelmSmartDB')      
      
    
    log.info("inFlux-cloud Query %s", query)
    

    try:
      response= db.query(query)
    except:
      e = sys.exc_info()[0]
      log.info('inFluxDB: Error in geting inFluxDB data %s:  ' % e)
        
      return jsonify( message='Error in inFluxDB query 2', status='error')
      #raise

    
    #return jsonify(results=response)
    
    #response =  shim.read_multi(keys=[SERIES_KEY], start=start, end=end, period=resolutionstr, rollup="mean" )
    
    #print 'inFluxDB read :', response.response.successful

    
    if not response:
      #print 'inFluxDB Exception1:', response.response.successful, response.response.reason 
      return jsonify( message='No response to return 1' , status='error')


    #if not response.points:
    #  #print 'inFluxDB Exception2:', response.response.successful, response.response.reason 
    #  return jsonify( message='No data to return 2', status='error')

    print('inFluxDB processing data headers:')
    jsondata=[]
    jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print('inFluxDB start processing data points:')
    #log.info("freeboard Get InfluxDB response %s", response)

    keys = response.raw.get('series',[])
    #log.info("freeboard Get InfluxDB series keys %s", keys)




    strvalue=""
    
    for series in keys:
      #log.info("freeboard Get InfluxDB series key %s", series)
      #log.info("freeboard Get InfluxDB series tags %s ", series['tags'])
      #log.info("freeboard Get InfluxDB series columns %s ", series['columns'])
      #log.info("freeboard Get InfluxDB series values %s ", series['values'])

      """        
      values = series['values']
      for value in values:
        log.info("freeboard Get InfluxDB series time %s", value[0])
        log.info("freeboard Get InfluxDB series mean %s", value[1])
      """

      tag = series['tags']
      #log.info("freeboard Get InfluxDB series tags2 %s ", tag)

      #mydatetimestr = str(fields['time'])
      strvaluekey = {'Series': series['tags'], 'start': startepoch,  'end': endepoch}
      jsonkey.append(strvaluekey)        

      #log.info("freeboard Get InfluxDB series tags3 %s ", tag['deviceid'])

      
      for point in series['values']:
        fields = {}
        for key, val in zip(series['columns'], point):
          fields[key] = val
          
        #log.info("freeboard Get InfluxDB series points %s , %s", fields['time'], fields['records'])
        
        if fields['records'] != None:

          devicename = ""
          deviceid = tag['deviceid']
          for record in records:
            #log.info("get_dbstats deviceid %s - devicename %s", record[0], record[1])    
            if deviceid == record[0]:
              devicename = record[1]
          
          strvalue = {'epoch': fields['time'], 'source':tag['deviceid'], 'name':devicename, 'value': fields['records']}
          jsondata.append(strvalue)





    jsondata = sorted(jsondata,key=itemgetter('value'), reverse=True)

    total = 0

    for stat in jsondata:
      if stat['value'] != None:
        total = total + float(stat['value'])

    if len(jsondata) > 0:
      mydatetimestr = str(jsondata[0]['epoch'])
      stat0 = str(jsondata[0]['source']) + ":" + str(jsondata[0]['name']) + " = " +  str(jsondata[0]['value'])

    if len(jsondata) > 1:
      stat1 = str(jsondata[1]['source']) + ":" + str(jsondata[1]['name']) + " = " +  str(jsondata[1]['value'])       

    if len(jsondata) > 2:
      stat2 = str(jsondata[2]['source']) + ":" + str(jsondata[2]['name']) + " = " +  str(jsondata[2]['value'])       

    if len(jsondata) > 3:
      stat3 = str(jsondata[3]['source']) + ":" + str(jsondata[3]['name']) + " = " +  str(jsondata[3]['value'])       

    if len(jsondata) > 4:
      stat4 = str(jsondata[4]['source']) + ":" + str(jsondata[4]['name']) + " = " +  str(jsondata[4]['value'])       

    if len(jsondata) > 5:
      stat5 = str(jsondata[5]['source']) + ":" + str(jsondata[5]['name']) + " = " +  str(jsondata[5]['value'])       

    if len(jsondata) > 6:
      stat6 = str(jsondata[6]['source']) + ":" + str(jsondata[6]['name']) + " = " +  str(jsondata[6]['value'])       

    if len(jsondata) > 7:
      stat7 = str(jsondata[7]['source']) + ":" + str(jsondata[7]['name']) + " = " +  str(jsondata[7]['value'])       

    if len(jsondata) > 8:
      stat8 = str(jsondata[8]['source']) + ":" + str(jsondata[8]['name']) + " = " +  str(jsondata[8]['value'])       

    if len(jsondata) > 9:
      stat9 = str(jsondata[9]['source']) + ":" + str(jsondata[9]['name']) + " = " +  str(jsondata[9]['value'])       

    if len(jsondata) > 10:
      stat10 = str(jsondata[10]['source']) + ":" + str(jsondata[10]['name']) + " = " +  str(jsondata[10]['value'])            

    if len(jsondata) > 11:
      stat11 = str(jsondata[11]['source']) + ":" + str(jsondata[11]['name']) + " = " +  str(jsondata[11]['value'])       

    if len(jsondata) > 12:
      stat12 = str(jsondata[12]['source']) + ":" + str(jsondata[12]['name']) + " = " +  str(jsondata[12]['value'])       

    if len(jsondata) > 13:
      stat13 = str(jsondata[13]['source']) + ":" + str(jsondata[13]['name']) + " = " +  str(jsondata[13]['value'])       

    if len(jsondata) > 14:
      stat14 = str(jsondata[14]['source']) + ":" + str(jsondata[14]['name']) + " = " +  str(jsondata[14]['value'])       

    if len(jsondata) > 15:
      stat15 = str(jsondata[15]['source']) + ":" + str(jsondata[15]['name']) + " = " +  str(jsondata[15]['value'])       

    if len(jsondata) > 16:
      stat16 = str(jsondata[16]['source']) + ":" + str(jsondata[16]['name']) + " = " +  str(jsondata[16]['value'])       

    mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')

    #log.info('freeboard: freeboard returning data values wind_speed:%s, wind_direction:%s  ', stat1,stat2)            

    callback = request.args.get('callback')
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")


    #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','lat':value1, 'lng':value2,})
    return '{0}({1})'.format(callback, {'date_time':myjsondate, 'Interval':str(Interval),'update':'True','total':int(total),'stat0':stat0,'stat1':stat1,'stat2':stat2,'stat3':stat3,'stat4':stat4,'stat5':stat5,'stat6':stat6,'stat7':stat7,'stat8':stat8,'stat9':stat9,'stat10':stat10,'stat11':stat11,'stat12':stat12,'stat13':stat13,'stat14':stat14,'stat15':stat15,'stat16':stat16})



  except TypeError as e:
      log.info('get_influxdbcloud_data: Type Error in InfluxDB mydata append %s:  ', response)
      log.info('get_influxdbcloud_data: Type Error in InfluxDB mydata append %s:  ' % str(e))
          
  except KeyError as e:
      log.info('get_influxdbcloud_data: Key Error in InfluxDB mydata append %s:  ', response)
      log.info('get_influxdbcloud_data: Key Error in InfluxDB mydata append %s:  ' % str(e))

  except NameError as e:
      log.info('get_influxdbcloud_data: Name Error in InfluxDB mydata append %s:  ', response)
      log.info('get_influxdbcloud_data: Name Error in InfluxDB mydata append %s:  ' % str(e))
          
  except IndexError as e:
      log.info('get_influxdbcloud_data: Index error in InfluxDB mydata append %s:  ', response)
      log.info('get_influxdbcloud_data: Index Error in InfluxDB mydata append %s:  ' % str(e))  

  except ValueError as e:
    log.info('get_influxdbcloud_data: Index error in InfluxDB mydata append %s:  ', response)
    log.info('get_influxdbcloud_data: Value Error in InfluxDB  %s:  ' % str(e))

  except AttributeError as e:
    log.info('get_influxdbcloud_data: Index error in InfluxDB mydata append %s:  ', response)
    log.info('get_influxdbcloud_data: AttributeError in InfluxDB  %s:  ' % str(e))     

  except InfluxDBClientError as e:
    log.info('get_influxdbcloud_data: Exception Error in InfluxDB  %s:  ' % str(e))     
  
  except:
    log.info('get_influxdbcloud_data: Error in geting freeboard response %s:  ', strvalue)
    e = sys.exc_info()[0]
    log.info('get_influxdbcloud_data: Error in geting freeboard ststs %s:  ' % e)
    return jsonify( message='error processing data 3' , status='error')        

  callback = request.args.get('callback')
  return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })




@app.route('/get_dbstats_html')
@cross_origin()
def get_dbstats_html():

  deviceapikey = request.args.get('apikey','')
  Interval = request.args.get('interval',"12hour")
  rollup = request.args.get('rollup',"sum")

  response = None

  period = 1
  
  starttime = 0

  epochtimes = getepochtimes(Interval)
  startepoch = epochtimes[0]
  endepoch = epochtimes[1]
  resolution = epochtimes[2]
  
  log.info("freeboard get_dbstats_html deviceapikey %s", deviceapikey)
  useremail = getuseremail(deviceapikey)
    
  log.info("freeboard get_dbstats_html useremail %s", useremail)

    

  response = None
  
  measurement = "HelmSmartDB"
  stat0 = '---'
  stat1 = '---'
  stat2 = '---'
  stat3 = '---'
  stat4 = '---'
  stat5 = '---'
  stat6 = '---'
  stat7 = '---'
  stat8 = '---'
  stat9 = '---'
  stat10 = '---'
  stat11 = '---'
  stat12 = '---'
  stat13 = '---'
  stat14 = '---'
  stat15 = '---'
  stat16 = '---'


  conn = db_pool.getconn()

  cursor = conn.cursor()
  #cursor.execute("select deviceid, devicename from user_devices where useremail = ")
  #query = "select deviceid, devicename from user_devices where useremail = %s "
  #cursor.execute(query,useremail)
  cursor.execute("select deviceid, devicename from user_devices where useremail = %s" , (useremail,))
  
  records = cursor.fetchall()

  db_pool.putconn(conn)   



  try:
   

    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'


    db = InfluxDBCloud(host, port, username, password, database,  ssl=True)
     

    
    start = datetime.datetime.fromtimestamp(float(startepoch))
    

    end = datetime.datetime.fromtimestamp(float(endepoch))


    resolution = 3600
    if Interval == "1hour":
      resolution = 300
    elif Interval == "2hour":
      resolution = 600
    elif Interval == "1day":
      resolution = 7200
    elif Interval == "1month":
      resolution = 86400
    elif Interval == "6month":
      resolution = 86400*30
    elif Interval == "12month":
      resolution = 86400*30
     
    resolutionstr = "PT" + str(resolution) + "S"

    #rollup = "mean"

 

    query = ('select {}(records) AS records FROM {} '
                     'where time > {}s and time < {}s '
                     'group by *, time({}s) ') \
                .format(rollup,  measurement, 
                        startepoch, endepoch,
                        resolution) 

    #query =(' select records as records from HelmSmartDB')      
      
    
    log.info("inFlux-cloud Query %s", query)
    

    try:
      response= db.query(query)
    except:
      e = sys.exc_info()[0]
      log.info('inFluxDB: Error in geting inFluxDB data %s:  ' % e)
        
      return jsonify( message='Error in inFluxDB query 2', status='error')
      #raise

    
    #return jsonify(results=response)
    
    #response =  shim.read_multi(keys=[SERIES_KEY], start=start, end=end, period=resolutionstr, rollup="mean" )
    
    #print 'inFluxDB read :', response.response.successful

    
    if not response:
      #print 'inFluxDB Exception1:', response.response.successful, response.response.reason 
      return jsonify( message='No response to return 1' , status='error')


    #if not response.points:
    #  #print 'inFluxDB Exception2:', response.response.successful, response.response.reason 
    #  return jsonify( message='No data to return 2', status='error')

    print('inFluxDB processing data headers:')
    jsondata=[]
    jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    print('inFluxDB start processing data points:')
    #log.info("freeboard Get InfluxDB response %s", response)

    keys = response.raw.get('series',[])
    #log.info("freeboard Get InfluxDB series keys %s", keys)




    strvalue=""
    
    for series in keys:
      #log.info("freeboard Get InfluxDB series key %s", series)
      #log.info("freeboard Get InfluxDB series tags %s ", series['tags'])
      #log.info("freeboard Get InfluxDB series columns %s ", series['columns'])
      #log.info("freeboard Get InfluxDB series values %s ", series['values'])

      """        
      values = series['values']
      for value in values:
        log.info("freeboard Get InfluxDB series time %s", value[0])
        log.info("freeboard Get InfluxDB series mean %s", value[1])
      """

      tag = series['tags']
      devicename = ""
      deviceid = tag['deviceid']
      for record in records:
        #log.info("get_dbstats deviceid %s - devicename %s", record[0], record[1])    
        if deviceid == record[0]:
          devicename = record[1]
              
      log.info("get_dbstats deviceid %s - devicename %s", deviceid, devicename)


      #mydatetimestr = str(fields['time'])
      #strvaluekey = {'Series': series['tags'], 'start': startepoch,  'end': endepoch}
      #jsonkey.append(strvaluekey)        

      log.info("freeboard Get InfluxDB series tags3 %s ", tag['deviceid'])
      log.info("freeboard Get InfluxDB series series['values'] %s ", series['values'])
      values=[]
      for point in reversed(series['values']):
        fields = {}
        for key, val in zip(series['columns'], point):
          fields[key] = val
          
        #log.info("freeboard Get InfluxDB series points %s , %s", fields['time'], fields['records'])
        
        if fields['records'] != None:
          values.append( fields['records'])
        else:
          values.append("---")
          
      strvalue = {'epoch': fields['time'], 'source':tag['deviceid'], 'name':devicename, 'value':values}

      if devicename != "":
        jsondata.append(strvalue)

      log.info("get_dbstats jsondata %s ", strvalue)

    #return jsonify( message=jsondata)


    #jsondata = sorted(jsondata,key=itemgetter('value'), reverse=True)
    totals=[0]*32

    
    total = 0
    stathtml = '<table border="0" cellspacing="5" cellpadding="5" style="width:100%; display: block">'
    
    stathtml = stathtml + "<tr> <td>" + "DeviceID" + "</td><td>" + "Device Name" + "</td>"
    stathtml = stathtml + "<td>" + "now" + "</td>"

    #log.info("get_dbstats header1 %s ", stathtml)
    units = "hr"
    period = 1
    
    if Interval == "1hour":
      period = 5
      units = "min"
      
      stathtml = stathtml + "<td>" +  str(int(period) * 1) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 2) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 3) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 4) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 5) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 6) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 7) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 8) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 9) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 10) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 11) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 12) +units + "</td>"

      stathtml = stathtml + "</tr>"

      

    elif Interval == "2hour":
      period = 10
      units = "min"
      stathtml = stathtml + "<td>" +  str(int(period) * 1) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 2) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 3) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 4) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 5) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 6) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 7) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 8) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 9) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 10) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 11) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 12) +units + "</td>"

      stathtml = stathtml + "</tr>"
      
    elif Interval == "1day":
      period = 2
      units = "hr"
      
      stathtml = stathtml + "<td>" +  str(int(period) * 1) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 2) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 3) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 4) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 5) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 6) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 7) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 8) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 9) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 10) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 11) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 12) +units + "</td>"

      stathtml = stathtml + "</tr>"


    elif Interval == "1month":
      period = 1
      units = "d"
      
      stathtml = stathtml + "<td>" +  str(int(period) * 1) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 2) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 3) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 4) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 5) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 6) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 7) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 8) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 9) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 10) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 11) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 12) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 13) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 14) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 15) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 16) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 17) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 18) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 19) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 20) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 21) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 22) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 23) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 24) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 25) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 26) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 27) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 28) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 29) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 30) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 31) +units + "</td>"
      stathtml = stathtml + "</tr>"

    elif Interval == "6month":
      period = 1
      units = "m"
      
      stathtml = stathtml + "<td>" +  str(int(period) * 1) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 2) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 3) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 4) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 5) +units + "</td>"
      stathtml = stathtml + "</tr>"

    elif Interval == "12month":
      period = 1
      units = "m"
      
      stathtml = stathtml + "<td>" +  str(int(period) * 1) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 2) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 3) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 4) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 5) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 6) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 7) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 8) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 9) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 10) +units + "</td>"
      stathtml = stathtml + "<td>" +  str(int(period) * 11) +units + "</td>"
      stathtml = stathtml + "</tr>"    
    log.info("get_dbstats header2 %s ", stathtml)

    
    for statdata in jsondata:
      stathtml = stathtml + "<tr> <td>" +  str(statdata['source']) + "</td><td>" + str(statdata['name']) + " </td>"

      tindex=0
      values = statdata['value']
      for value in values:
        
        if value != "---":
          stathtml = stathtml + "<td>" +  str(float("{0:.1f}".format(int(value) * 0.001) )) + "</td>"
          total = total + int(value)
          totals[tindex]=int(totals[tindex]) + int(value)
          
        else:
          stathtml = stathtml + "<td>" +  "---"  + "</td>"
          
        tindex = tindex + 1
        log.info("get_dbstats deviceid %s - tindex %s", statdata['source'], tindex)
        
      stathtml = stathtml + "  </tr>"

    
    stathtml = stathtml + "<tr> <td>" + "" + "</td><td>" + "Totals" + "</td>"

    log.info("get_dbstats header3 %s ", stathtml)
    
    try:
      if Interval == "1hour" or Interval == "2hour" or Interval == "1day":
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[0]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[1]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[2]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[3]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[4]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[5]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[6]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[7]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[8]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[9]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[10]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[11]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[12]) * 0.001) ))  + "</td>"
        
      elif  Interval == "1month":
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[0]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[1]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[2]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[3]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[4]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[5]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[6]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[7]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[8]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[9]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[10]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[11]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[12]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[13]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[14]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[15]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[16]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[17]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[18]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[19]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[20]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[21]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[22]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[23]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[24]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[25]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[26]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[27]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[28]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[29]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[30]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[31]) * 0.001) ))  + "</td>"

      elif  Interval == "6month":
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[0]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[1]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[2]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[3]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[4]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[5]) * 0.001) ))  + "</td>"

      elif  Interval == "12month":
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[0]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[1]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[2]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[3]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[4]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[5]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[6]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[7]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[8]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[9]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[10]) * 0.001) ))  + "</td>"
        stathtml = stathtml + "<td>" +    str(float("{0:.1f}".format(int(totals[11]) * 0.001) ))  + "</td>"

        
    except:
      pass
    
    stathtml = stathtml + "</tr>"      
    
    stathtml = stathtml + "</table>"
    
    log.info("get_dbstats header4 %s ", stathtml)

    #mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')

    #log.info('freeboard: freeboard returning data values wind_speed:%s, wind_direction:%s  ', stat1,stat2)            

    callback = request.args.get('callback')
    #myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")

    mydatetime = datetime.datetime.now()
    myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")    
    #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','lat':value1, 'lng':value2,})
    #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'Interval':str(Interval),'update':'True','total':int(total),'stat0':stat0,'stat1':stat1,'stat2':stat2,'stat3':stat3,'stat4':stat4,'stat5':stat5,'stat6':stat6,'stat7':stat7,'stat8':stat8,'stat9':stat9,'stat10':stat10,'stat11':stat11,'stat12':stat12,'stat13':stat13,'stat14':stat14,'stat15':stat15,'stat16':stat16})
    return '{0}({1})'.format(callback, {'date_time':myjsondate, 'Interval':str(Interval),'update':'True','total':int(total),'stats':stathtml})

 

  except TypeError as e:
      log.info('get_influxdbcloud_data: Type Error in InfluxDB mydata append %s:  ', response)
      log.info('get_influxdbcloud_data: Type Error in InfluxDB mydata append %s:  ' % str(e))
          
  except KeyError as e:
      log.info('get_influxdbcloud_data: Key Error in InfluxDB mydata append %s:  ', response)
      log.info('get_influxdbcloud_data: Key Error in InfluxDB mydata append %s:  ' % str(e))

  except NameError as e:
      log.info('get_influxdbcloud_data: Name Error in InfluxDB mydata append %s:  ', response)
      log.info('get_influxdbcloud_data: Name Error in InfluxDB mydata append %s:  ' % str(e))
          
  except IndexError as e:
      #log.info('get_influxdbcloud_data: Index error in InfluxDB mydata append %s:  ', response)
      log.info('get_influxdbcloud_data: Index Error in InfluxDB mydata append %s:  ' % str(e))
      pass

  except ValueError as e:
    log.info('get_influxdbcloud_data: Index error in InfluxDB mydata append %s:  ', response)
    log.info('get_influxdbcloud_data: Value Error in InfluxDB  %s:  ' % str(e))

  except AttributeError as e:
    log.info('get_influxdbcloud_data: Index error in InfluxDB mydata append %s:  ', response)
    log.info('get_influxdbcloud_data: AttributeError in InfluxDB  %s:  ' % str(e))     

  except InfluxDBClientError as e:
    log.info('get_influxdbcloud_data: Exception Error in InfluxDB  %s:  ' % str(e))     
  
  except:
    log.info('get_influxdbcloud_data: Error in geting freeboard response %s:  ', strvalue)
    e = sys.exc_info()[0]
    log.info('get_influxdbcloud_data: Error in geting freeboard ststs %s:  ' % e)
    return jsonify( message='error processing data 3' , status='error')        

  callback = request.args.get('callback')
  return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
# Gets GPS lat and lng with data overlay
@app.route('/getgpsseriesbydeviceid')
@cross_origin()
def getgpsseriesbydeviceid():
  conn = db_pool.getconn()

  devicekey = request.args.get('devicekey', '4d231fb3a164c5eeb1a8634d34c578eb')
  deviceid = request.args.get('deviceid', '')
  startepoch = request.args.get('startepoch', 0)
  endepoch = request.args.get('endepoch', 0)
  resolution = request.args.get('resolution', 60)
  SERIES_KEY1 = request.args.get('serieskey1', '')
  SERIES_KEY2 = request.args.get('serieskey2', '')

  dataformat = request.args.get('format', 'json')
  minthreshold = request.args.get('min', '0')
  maxthreshold = request.args.get('max', '1000000')
  maxinterval = request.args.get('maxinterval', '1440')
  
  query = "select deviceid from user_devices where deviceapikey = %s"

  response = None
  
  measurement = "HelmSmart"
  measurement = 'HS_' + str(deviceid)

  try:
  #if dataformat == 'json':
      # first check db to see if deviceapikey is matched to device id
      if deviceid == "":
        cursor = conn.cursor()
        cursor.execute(query, (devicekey,))
        i = cursor.fetchone()
        # if not then just exit
        if cursor.rowcount == 0:
            return jsonify( message='No device key found', status='error')
        else:
            deviceid = str(i[0]) 
  

      # Modify these with your settings found at: http://tempo-db.com/manage/
      API_KEY = '7be1d82569414dceaa82fd93fadd7940'
      API_SECRET = '0447ec319c3148cb98d96bfc96c787e1'

      host = 'hilldale-670d9ee3.influxcloud.net' 
      port = 8086
      username = 'helmsmart'
      password = 'Salm0n16'
      database = 'pushsmart-cloud'


      db = InfluxDBCloud(host, port, username, password, database,  ssl=True)    


      #rollup = "mean"
      rollup = "median"

      #print 'TempoDB Series Key:', SERIES_KEY

      if SERIES_KEY1.find(".*.") > 0:  
        SERIES_KEY1 = SERIES_KEY1.replace(".*.","*.")

      if SERIES_KEY2.find(".*.") > 0:  
        SERIES_KEY2 = SERIES_KEY2.replace(".*.","*.")        
      
      gpskey =SERIES_KEY1

      overlaykey =SERIES_KEY2




      seriesname = SERIES_KEY1
      seriestags = seriesname.split(".")

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
        serieskeys= serieskeys +  "'  ) " 

 

                
      else:
        serieskeys="( deviceid='"
        serieskeys= serieskeys + seriesdeviceid[1] 
        serieskeys= serieskeys +  "' AND sensor='" +  seriessensor[1]
        if seriessource[1] != "*":
          serieskeys= serieskeys +  "' AND source='" +  seriessource[1] 
        serieskeys= serieskeys +  "' AND instance='" +  seriesinstance[1] 
        serieskeys= serieskeys +  "' AND type='" +  seriestype[1] 
        serieskeys= serieskeys +  "' AND parameter='" +  seriesparameter[1] + "'   )"

        


      log.info("inFlux-cloud serieskeys %s", serieskeys)


 

      

      if SERIES_KEY2 == "":
      # Just get lat/lng

        query = ('select median(lat) as lat, median(lng) as lng from {} '
                        'where {} AND time > {}s and time < {}s '
                       'group by *, time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution)

        """
        query = ('select median(lat) as lat, median(lng) as lng from {} '
                        'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution)
        """
        
        log.info("inFlux-cloud gps: Position Query %s", query)
        
      else:
      # get lat/lng plus overlay series

        overlayname = SERIES_KEY2
        log.info("inFlux-cloud gps: overlayname Query %s", overlayname)
        
        overlaytags = overlayname.split(".")
        log.info("inFlux-cloud gps: overlaytags Query %s", overlaytags)
        
        overlaydeviceidtag = overlaytags[0]
        overlaydeviceid = overlaydeviceidtag.split(":")

        overlaysensortag = overlaytags[1]
        overlaysensor =overlaysensortag.split(":")

        overlaysourcetag = overlaytags[2]
        overlaysource = overlaysourcetag.split(":")

        overlayinstancetag = overlaytags[3]
        overlayinstance = overlayinstancetag.split(":")

        overlaytypetag = overlaytags[4]
        overlaytype = overlaytypetag.split(":")

        overlayparametertag = overlaytags[5]
        overlayparameter = overlayparametertag.split(":")    

        log.info("inFlux-cloud gps: overlayparameter Query %s", overlayparameter)
        
        overlaykey="( deviceid='"
        overlaykey= overlaykey + overlaydeviceid[1] 
        overlaykey= overlaykey +  "' AND sensor='" +  overlaysensor[1]
        if overlaysource[1] != "*":
          overlaykey= overlaykey +  "' AND source='" +  overlaysource[1] 
        overlaykey= overlaykey +  "' AND instance='" +  overlayinstance[1] 
        overlaykey= overlaykey +  "' AND type='" +  overlaytype[1] 
        overlaykey= overlaykey +  "' AND parameter='" +  overlayparameter[1] + "'   )"

        log.info("inFlux-cloud gps: overlaykey Query %s", overlaykey)

        serieskeys   =    serieskeys  + " OR " +   overlaykey
        log.info("inFlux-cloud gps: serieskeys Query %s", serieskeys)
      
        query = ('select median(lat) as lat, median(lng) as lng, mean({}) as {} from {} '
                        'where {} AND time > {}s and time < {}s '
                       'group by *, time({}s)') \
                  .format( overlayparameter[1], overlayparameter[1], measurement, serieskeys,
                          startepoch, endepoch,
                          resolution)

   
        log.info("inFlux gps: Overlay Query %s", query)

        

      try:
        data= db.query(query)
        
      except TypeError as e:
        log.info('get_influxdbcloud_data: Type Error in InfluxDB mydata append %s:  ', query)
        log.info('get_influxdbcloud_data: Type Error in InfluxDB mydata append %s:  ' % str(e))
              
      except KeyError as e:
        log.info('get_influxdbcloud_data: Key Error in InfluxDB mydata append %s:  ', query)
        log.info('get_influxdbcloud_data: Key Error in InfluxDB mydata append %s:  ' % str(e))

      except NameError as e:
        log.info('get_influxdbcloud_data: Name Error in InfluxDB mydata append %s:  ', query)
        log.info('get_influxdbcloud_data: Name Error in InfluxDB mydata append %s:  ' % str(e))
              
      except IndexError as e:
        log.info('get_influxdbcloud_data: Index error in InfluxDB mydata append %s:  ', query)
        log.info('get_influxdbcloud_data: Index Error in InfluxDB mydata append %s:  ' % str(e))  

      except ValueError as e:
        log.info('get_influxdbcloud_data: Index error in InfluxDB mydata append %s:  ', query)
        log.info('get_influxdbcloud_data: Value Error in InfluxDB  %s:  ' % str(e))

      except AttributeError as e:
        log.info('get_influxdbcloud_data: Index error in InfluxDB mydata append %s:  ', query)
        log.info('get_influxdbcloud_data: AttributeError in InfluxDB  %s:  ' % str(e))     

      except InfluxDBClientError as e:
        log.info('get_influxdbcloud_data: Exception Error in InfluxDB  %s:  ' % str(e))     
        
      except:
        #log.info('Telemetrypost: Error in geting Telemetry parameters %s:  ', posttype)
        e = sys.exc_info()[0]
        log.info('inFluxDB gps: Error in geting inFluxDB data %s:  ' % e)
        
        return jsonify( message='Error in inFluxDB query 2', status='error')
        #raise
      
      #return jsonify(results=data)
      #log.info('getgpsseriesbydeviceid: datad %s:  ', data)  

      if not data:
        return jsonify( message='No data object to return 1', status='error')

      #return jsonify( message='data object to return 1', status='success')
      # return csv formated data
      try:
        jsondata=[]
        jsonkey=[]
        strvaluekey = {'Series1': SERIES_KEY1, 'Series2': SERIES_KEY2,'start': startepoch,  'end': endepoch, 'resolution': resolution}
        jsonkey.append(strvaluekey)
        jsondataarray=[]

        #if overlaykey == "":
        # Just get lat/lng
        keys = data.raw.get('series',[])
        jsondata=[]
        for series in keys:
          #log.info("influxdb results..%s", series )
          #log.info("influxdb results..%s", series )
          strvalue ={}


          #name = series['name']
          name = series['tags']            
          #log.info("inFluxDB_GPS_JSON name %s", name )
          seriesname = series['tags'] 
          #seriestags = seriesname.split(".")
          #seriessourcetag = seriestags[2]
          #seriessource = seriessourcetag.split(":")
          source= seriesname['source']
          parameter = seriesname['parameter']
          #log.info("inFluxDB_GPS_JSON values %s", series['values'] )
          
          for point in  series['values']:
            fields = {}
            fields[parameter] = None
            for key, val in zip(series['columns'], point):
              fields[key] = val
              
            #strvalue = {'epoch': fields['time'], 'tag':seriesname, 'lat': fields['lat'], 'lng': fields['lng']}
            #log.info("freeboard Get InfluxDB series points %s , %s", fields['time'], fields[parameter])

            mydatetimestr = str(fields['time'])

            #mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')
            mydatetime =  int(time.mktime(time.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')))
            
            #strvalue = {'epoch': fields['time'], 'source':tag['source'], 'value': fields[parameter]}
            if fields[parameter] != None:
              #strvalues = []
              strvalue = {'epoch': mydatetime, 'tag':seriesname, 'value': fields[parameter]}
              strvalues = (mydatetime, source,  parameter, fields[parameter] )

              
              jsondata.append(strvalues)


            
        # here we have an array of seperated lat and lng values taged with epoch times and series tags
        # Like 
        #'(u'HelmSmart', {u'instance': u'0', u'parameter': u'lat', u'deviceid': u'001EC010AD69', u'source': u'06', u'sensor': u'position_rapid', u'type': u'NULL'})':
        # [{u'time': u'2016-08-18T11:00:00Z', u'lng': None, u'lat': 42.012865}],
        # '(u'HelmSmart', {u'instance': u'0', u'parameter': u'lng', u'deviceid': u'001EC010AD69', u'source': u'06', u'sensor': u'position_rapid', u'type': u'NULL'})':
        # [{u'time': u'2016-08-18T11:00:00Z', u'lng': -124.13088, u'lat': None}],
        #
        # We need to reorder this into joined lat and lng based on same epoch times

        #jsondata = sorted(jsondata,key=itemgetter('epoch'))
        # sort based on epoch times
        jsondata = sorted(jsondata, key=lambda latlng: latlng[0])
        #log.info("freeboard  jsondata   %s",jsondata)
        #return jsonify( message=jsondata, status='success')

      
        # group lat and lng values based on epoch times and get rid of repeated epoch times
        for key, latlnggroup in groupby(jsondata, lambda x: x[0]):

          valuelat = None
          valuelng = None
          valueoverlay = None
          
          for latlng_values in latlnggroup:
            if latlng_values[2] == 'lat':
              valuelat = latlng_values[3]
              valuesource = latlng_values[1]
              
              
            elif latlng_values[2] == 'lng':
              valuelng = latlng_values[3]

            elif latlng_values[2] != None:
              valueoverlay = latlng_values[3]              
              

            
          #strvalues=  {'epoch': key, 'source':thing[1], 'value': thing[3]}

          # if we have valid lat and lng - make a json array
          if  valuelat != None and valuelng != None and valueoverlay != None:
            strvalues=  {'epoch': key, 'source':valuesource, 'lat': valuelat, 'lng': valuelng,  'overlay':valueoverlay}
            jsondataarray.append(strvalues)
            
          elif  valuelat != None and valuelng != None:
            strvalues=  {'epoch': key, 'source':valuesource, 'lat': valuelat, 'lng': valuelng}
            jsondataarray.append(strvalues)
            
            #log.info("freeboard  jsondata group   %s",strvalues)


      except NameError as e:
        log.info('inFluxDB_GPS: NameError in geting gps data parsing  %s:  ', strvalues)
        log.info('inFluxDB_GPS: NameError in geting gps data parsing  %s:  ' % str(e))          
        #return jsonify( message=jsondataarray, status='success')
      except:
        #log.info('Telemetrypost: Error in geting Telemetry parameters %s:  ', posttype)
        e = sys.exc_info()[0]
        log.info('get_influxdbcloud_gpsdata: Error in geting gps data parsing %s:  ' % e)
      
        return jsonify( message='Error in inFluxDB_GPS  parsing', status='error')

      
      
      if dataformat == 'csv':
        try:
          #def generate():
          #if overlaykey == "":
          # Just get lat/lng
          # create header row
          strvalue ='TimeStamp, serieskey1: ' + SERIES_KEY1 + ', serieskey2: ' + SERIES_KEY2 +', start: ' + startepoch + ', end: ' + endepoch +  ', resolution: ' + resolution  + ' \r\n'

          # create header row
          if SERIES_KEY2 != "":      
            strvalue = strvalue + 'epoch, time, source, lat, lng, seg distance, speed, delta time, ' + overlayparameter[1] + ' \r\n'
          else:
            strvalue = strvalue + 'epoch, time, source, lat, lng, seg distance, speed, delta time \r\n'

       
          #get all other rows
          #for dataset in data:
          jsondata = jsondataarray

          list_length = len(jsondata)
          for i in range(list_length-1):
            oldvector = (jsondata[i]['lat'], jsondata[i]['lng'])
            oldsource = jsondata[i]['source']
            newvector = (jsondata[i+1]['lat'], jsondata[i+1]['lng'])
            newsource = jsondata[i+1]['source']
            
            if (newsource == oldsource) and (newvector != oldvector):
              oldtime = jsondata[i]['epoch']
              newtime = jsondata[i+1]['epoch']

              deltatime = abs(newtime - oldtime)
              
              delta = geodesic(oldvector, newvector).miles
              if deltatime == 0:
                speed = float(0)
              else:
                speed = float((delta/(float(deltatime)))*60*60)

              mytime = datetime.datetime.fromtimestamp(float(jsondata[i]['epoch'])).strftime('%Y-%m-%d %H:%M:%SZ')
                
              if SERIES_KEY2 == "":                
                strvalue = strvalue + str(jsondata[i]['epoch'])+ ', ' + str(mytime) + ', ' + str(jsondata[i]['source']) + ', ' + str(jsondata[i]['lat']) + ', ' + str(jsondata[i]['lng']) + ', ' + str(delta)+ ', ' + str(speed)+ ', ' + str(deltatime) + ' \r\n'
              else:
                strvalue = strvalue + str(jsondata[i]['epoch'])+ ', ' + str(mytime) + ', ' + str(jsondata[i]['source']) + ', ' + str(jsondata[i]['lat']) + ', ' + str(jsondata[i]['lng']) + ', ' + str(delta)+ ', ' + str(speed)+ ', ' + str(deltatime) + ', ' + str(jsondata[i]['overlay'])+ ' \r\n'

          response = make_response(strvalue)
          response.headers['Content-Type'] = 'text/csv'
          response.headers["Content-Disposition"] = "attachment; filename=HelmSmart.csv"
          return response

        
        except:
          #log.info('Telemetrypost: Error in geting Telemetry parameters %s:  ', posttype)
          e = sys.exc_info()[0]
          log.info('inFluxDB_GPS: Error in geting inFluxDB CSV data %s:  ' % e)
      
          return jsonify( message='Error in inFluxDB_GPS CSV parsing', status='error')

      elif dataformat == 'gpx':
        try:
          #def generate():
          # create header row
          #strvalue ='TimeStamp, serieskey1: ' + SERIES_KEY1 + ', serieskey2: ' + SERIES_KEY2 +', start: ' + startepoch + ', end: ' + endepoch +  ', resolution: ' + resolution  + ' \r\n'
          gpxpoints=[]
          # create header row
          #strvalue = strvalue + 'time, value1, value2, value3, value4 \r\n'
          strvalue = ""
          strvalue = '<?xml version="1.0" encoding="UTF-8"?>' + '\r\n'
          strvalue = strvalue + '<gpx creator="HelmSmart Visualizer http://www.helmsmart.com/" '
          strvalue = strvalue + 'version="1.1" xmlns="http://www.topografix.com/GPX/1/1" '
          strvalue = strvalue + 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
          strvalue = strvalue + 'xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">' + '\r\n'
          strvalue = strvalue + '<trk>' + '\r\n'
          strvalue = strvalue + '<name>Track001</name>' + '\r\n'
          strvalue = strvalue + '<trkseg>' + '\r\n'
          #get all other rows
          gpxpoints = jsondataarray


          #Next go through array and calculate the distance and speed vectors.
          list_length = len(gpxpoints)
          for i in range(list_length-1):
            
              oldvector = (gpxpoints[i]['lat'], gpxpoints[i]['lng'])
              newvector = (gpxpoints[i+1]['lat'], gpxpoints[i+1]['lng'])

              if newvector != oldvector:

                oldtime = gpxpoints[i]['epoch']
                newtime = gpxpoints[i+1]['epoch']

                deltatime = abs(newtime - oldtime)
                
                delta = geodesic(oldvector, newvector).miles

                if deltatime == 0:
                  speed = float(0)
     
                else:
                  speed = float((delta/(float(deltatime)))*60*60)

                # if speed vector less then threshold add to GPX file
                if speed < float(maxthreshold)/100:
                  mytime = datetime.datetime.fromtimestamp(float(gpxpoints[i]['epoch'])).strftime('%Y-%m-%dT%H:%M:%SZ')
                  strvalue = strvalue + '<trkpt lat="' + str(gpxpoints[i]['lat']) + '" lon="' + str(gpxpoints[i]['lng']) + '"> \r\n'
                  strvalue = strvalue + '<time>' + str(mytime) + '</time> \r\n'
                  strvalue = strvalue + '</trkpt> \r\n'

          #close out GPX file with footer
          strvalue = strvalue + '</trkseg> \r\n'
          strvalue = strvalue + '</trk> \r\n'
          strvalue = strvalue + '<extensions> \r\n'
          strvalue = strvalue + '</extensions> \r\n'
          strvalue = strvalue + '</gpx> \r\n'
          
          response = make_response(strvalue)
          response.headers['Content-Type'] = 'text/plain'
          response.headers["Content-Disposition"] = "attachment; filename=HelmSmart.gpx"
          return response
        except:
          #log.info('Telemetrypost: Error in geting Telemetry parameters %s:  ', posttype)
          e = sys.exc_info()[0]
          log.info('inFluxDB_GPS: Error in geting inFluxDB GPX data %s:  ' % e)
      
          return jsonify( message='Error in inFluxDB_GPS GPX parsing', status='error')

      elif dataformat == 'jsonf':
        try:
          jsondata=[]
          jsonkey=[]
          strvaluekey = {'Series1': SERIES_KEY1, 'Series2': SERIES_KEY2,'start': startepoch,  'end': endepoch, 'resolution': resolution}
          jsonkey.append(strvaluekey)

          gpsdata=[]
          jsondata=[]
          #for jsondata in jsondataarray:


          jsondata = jsondataarray


          list_length = len(jsondata)
          for i in range(list_length-1):
            oldvector = (jsondata[i]['lat'], jsondata[i]['lng'])
            oldsource = jsondata[i]['source']
            newvector = (jsondata[i+1]['lat'], jsondata[i+1]['lng'])
            newsource = jsondata[i+1]['source']
            
            if (newsource == oldsource) and (newvector != oldvector):
              oldtime = jsondata[i]['epoch']
              newtime = jsondata[i+1]['epoch']

              deltatime = abs(newtime - oldtime)
              
              delta = geodesic(oldvector, newvector).miles
              if deltatime == 0:
                speed = float(0)
              else:
                speed = float((delta/(float(deltatime)))*60*60)

              if SERIES_KEY2 == "":
                gpsjson = {'epoch': jsondata[i]['epoch'], 'source':jsondata[i]['source'], 'lat':jsondata[i]['lat'], 'lng': jsondata[i]['lng'], 'distance':delta, 'speed':speed, 'interval':deltatime}
              else:
                gpsjson = {'epoch': jsondata[i]['epoch'],  'source':jsondata[i]['source'],'lat':jsondata[i]['lat'], 'lng': jsondata[i]['lng'], 'distance':delta, 'speed':speed, 'overlay': jsondata[i]['overlay']}

              #mininterval
              if deltatime <  float(maxinterval) * 60:
                if speed < float(maxthreshold)/100:
                  gpsdata.append(gpsjson)
          
          #print('inFluxDB_GPS JSONF returning data points:')

          #return jsonify(serieskey = jsonkey, results = jsondata)
          response = make_response(json.dumps(gpsdata))
          response.headers['Content-Type'] = "application/json"
          response.headers["Content-Disposition"] = "attachment; filename=HelmSmart.json"
          return response

        except NameError as e:
          log.info('inFluxDB_GPS: NameError in convert_influxdb_gpsjson %s:  ', gpsdata)
          log.info('inFluxDB_GPS: NameError in convert_influxdb_gpsjson %s:  ' % str(e))
          
        except:
          #log.info('Telemetrypost: Error in geting Telemetry parameters %s:  ', posttype)
          e = sys.exc_info()[0]
          log.info('inFluxDB_GPS: Error in geting inFluxDB JSONF data %s:  ' % e)
      
          return jsonify( message='Error in inFluxDB_GPS JSONF parsing', status='error')
        

      
      elif dataformat == 'json':
        try:


         
          gpsdata=[]
          jsondata=[]
          #for jsondata in jsondataarray:


          jsondata = jsondataarray
          #log.info("freeboard  jsondata  %s:  %s",len(jsondata),  jsondata)
          
          list_length = len(jsondata)
          for i in range(list_length-1):
            oldvector = (jsondata[i]['lat'], jsondata[i]['lng'])
            oldsource = jsondata[i]['source']
            newvector = (jsondata[i+1]['lat'], jsondata[i+1]['lng'])
            newsource = jsondata[i+1]['source']
            
            if (newsource == oldsource) and (newvector != oldvector):

              oldtime = jsondata[i]['epoch']
              newtime = jsondata[i+1]['epoch']

              deltatime = abs(newtime - oldtime)
              
              delta = geodesic(oldvector, newvector).miles
              #print 'GetGPSJSON processing dalta points:', delta

              #speed = {'speed':float(delta/(float(deltatime)*60*60))} 
              if deltatime == 0:
                speed = float(0)
   
              else:
                speed = float((delta/(float(deltatime)))*60*60)
              #distance = {'distance':delta}

              if SERIES_KEY2 == "":
                gpsjson = {'epoch': jsondata[i]['epoch'], 'source':jsondata[i]['source'], 'lat':jsondata[i]['lat'], 'lng': jsondata[i]['lng'], 'distance':delta, 'speed':speed, 'interval':deltatime}
              else:
                gpsjson = {'epoch': jsondata[i]['epoch'], 'source':jsondata[i]['source'], 'lat':jsondata[i]['lat'], 'lng': jsondata[i]['lng'], 'distance':delta, 'speed':speed, 'overlay': jsondata[i]['overlay']}
              
              #if delta < float(maxthreshold)/1000:
              if deltatime <  float(maxinterval) * 60:
                if speed < float(maxthreshold)/100:
                  gpsdata.append(gpsjson)
                
          #except:
          #  e = sys.exc_info()[0]
          #  log.info('inFluxDB_GPS: Error in geting inFluxDB JSON data %s:  ' % e)

          gpsdata = sorted(gpsdata,key=itemgetter('epoch'))
          #print('GetGPSJSON returning data points:')
          log.info('GetGPSJSON: returning JSON data:  ' )

          
          return jsonify(serieskey = jsonkey, results = gpsdata)
        
        except AttributeError as e:
          log.info('inFluxDB_GPS: AttributeError in convert_influxdb_gpsjson %s:  ', data)
          #e = sys.exc_info()[0]

          log.info('inFluxDB_GPS: AttributeError in convert_influxdb_gpsjson %s:  ' % str(e))
          
        except TypeError as e:
          log.info('inFluxDB_GPS: TypeError in convert_influxdb_gpsjson %s:  ', data)
          #e = sys.exc_info()[0]

          log.info('inFluxDB_GPS: TypeError in convert_influxdb_gpsjson %s:  ' % str(e))
          
        except ValueError as e:
          log.info('inFluxDB_GPS: ValueError in convert_influxdb_gpsjson %s:  ', data)
          #e = sys.exc_info()[0]

          log.info('inFluxDB_GPS: ValueError in convert_influxdb_gpsjson %s:  ' % str(e))            
          
        except NameError as e:
          log.info('inFluxDB_GPS: NameError in convert_influxdb_gpsjson %s:  ', data)
          #e = sys.exc_info()[0]

          log.info('Sync: NameError in convert_influxdb_gpsjson %s:  ' % str(e))          
        except:
          e = sys.exc_info()[0]
          log.info('inFluxDB_GPS: Error in geting inFluxDB JSON data %s:  ' % e)
      
          return jsonify( message='Error in inFluxDB_GPS JSON parsing', status='error')
        
      else:
        result = json.dumps(data.data, cls=DateEncoder)
  
        response = make_response(result) 
    
        response.headers['content-type'] = "application/json"
        return response
  
  except AttributeError as e:
    log.info('inFluxDB_GPS: AttributeError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
    #e = sys.exc_info()[0]

    log.info('inFluxDB_GPS: AttributeError in convert_influxdb_gpsjson %s:  ' % str(e))
    
  except TypeError as e:
    log.info('inFluxDB_GPS: TypeError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
    #e = sys.exc_info()[0]

    log.info('inFluxDB_GPS: TypeError in convert_influxdb_gpsjson %s:  ' % str(e))
    
  except ValueError as e:
    log.info('inFluxDB_GPS: ValueError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
    #e = sys.exc_info()[0]

    log.info('inFluxDB_GPS: ValueError in convert_influxdb_gpsjson %s:  ' % str(e))            
    
  except NameError as e:
    log.info('inFluxDB_GPS: NameError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
    #e = sys.exc_info()[0]

  except IndexError as e:
    log.info('inFluxDB_GPS: IndexError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
    log.info('inFluxDB_GPS: IndexError in convert_influxdb_gpsjson %s:  ' % str(e)) 
    #e = sys.exc_info()[0]


  except:
    e = sys.exc_info()[0]
    log.info('inFluxDB_GPS: Error read_data exception data.points %s:  ' % e)
    return jsonify( message='gps_influxdb read_data exception data.points', status='error')
  

  finally:
    db_pool.putconn(conn)





# Gets GPS lat and lng with data overlay
@app.route('/getgpsseriesbydeviceid_dbc')
def getgpsseriesbydeviceid_dbc():
  conn = db_pool.getconn()

  devicekey = request.args.get('devicekey', '4d231fb3a164c5eeb1a8634d34c578eb')
  deviceid = request.args.get('deviceid', '')
  startepoch = request.args.get('startepoch', 0)
  endepoch = request.args.get('endepoch', 0)
  resolution = request.args.get('resolution', 60)
  SERIES_KEY1 = request.args.get('serieskey1', '')
  SERIES_KEY2 = request.args.get('serieskey2', '')

  dataformat = request.args.get('format', 'json')
  minthreshold = request.args.get('min', '0')
  maxthreshold = request.args.get('max', '1000000')
  maxinterval = request.args.get('maxinterval', '1440')
  gpsmethod = request.args.get('fix', 15)

  
  query = "select deviceid from user_devices where deviceapikey = %s"

  response = None
  


  try:
  #if dataformat == 'json':
      # first check db to see if deviceapikey is matched to device id
      if deviceid == "":
        cursor = conn.cursor()
        cursor.execute(query, (devicekey,))
        i = cursor.fetchone()
        # if not then just exit
        if cursor.rowcount == 0:
            return jsonify( message='No device key found', status='error')
        else:
            deviceid = str(i[0]) 
  
      measurement = "HelmSmart"
      measurement = "HS_" + str(deviceid)
      # Modify these with your settings found at: http://tempo-db.com/manage/
      API_KEY = '7be1d82569414dceaa82fd93fadd7940'
      API_SECRET = '0447ec319c3148cb98d96bfc96c787e1'

      host = 'hilldale-670d9ee3.influxcloud.net' 
      port = 8086
      username = 'helmsmart'
      password = 'Salm0n16'
      database = 'pushsmart-cloud'


      db = InfluxDBCloud(host, port, username, password, database,  ssl=True)    


      #rollup = "mean"
      rollup = "median"

      #print 'TempoDB Series Key:', SERIES_KEY

      if SERIES_KEY1.find(".*.") > 0:  
        SERIES_KEY1 = SERIES_KEY1.replace(".*.","*.")

      if SERIES_KEY2.find(".*.") > 0:  
        SERIES_KEY2 = SERIES_KEY2.replace(".*.","*.")        
      
      gpskey =SERIES_KEY1
      log.info("inFlux-cloud serieskeys %s", gpskey)
      
      overlaykey =SERIES_KEY2
      log.info("inFlux-cloud serieskeys %s", overlaykey)



      seriesname = SERIES_KEY1
      seriestags = seriesname.split(".")

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
      log.info("inFlux-cloud parameter %s", parameter)

      if int(gpsmethod) == 0:
        fixtype = 'no GPS'
      elif int(gpsmethod) == 1:        
        fixtype = 'GNSS fix'
      elif int(gpsmethod) == 2:            
        fixtype = 'DGNSS fix'
      elif int(gpsmethod) == 3:            
        fixtype = 'Precise GNSS'
      elif int(gpsmethod) == 4:            
        fixtype = 'RTK Fixed Integer'
      elif int(gpsmethod) == 5:            
        fixtype = 'RTK Float'
      elif int(gpsmethod) == 6:            
        fixtype = 'Estimated mode'
      elif int(gpsmethod) == 7:            
        fixtype = 'Manual Input'
      elif int(gpsmethod) == 8:            
        fixtype = 'Simulate mode'
      else:            
        fixtype = 'NULL'      

      log.info("inFlux-cloud fixtype %s", fixtype)

      sourcekey = ""

      if parameter == 'latlng':
        serieskeys="( deviceid='"
        serieskeys= serieskeys + seriesdeviceid[1] 
        serieskeys= serieskeys +  "' AND sensor='" +  seriessensor[1]
        if seriessource[1] != "*":
          serieskeys= serieskeys +  "' AND source='" +  seriessource[1] 
        serieskeys= serieskeys +  "' AND instance='" +  seriesinstance[1] 
        serieskeys= serieskeys +  "' AND type='" +  fixtype
        serieskeys= serieskeys +  "'  ) " 


                
      else:
        serieskeys="( deviceid='"
        serieskeys= serieskeys + seriesdeviceid[1] 
        serieskeys= serieskeys +  "' AND sensor='" +  seriessensor[1]
        if seriessource[1] != "*":
          serieskeys= serieskeys +  "' AND source='" +  seriessource[1] 
        serieskeys= serieskeys +  "' AND instance='" +  seriesinstance[1] 
        serieskeys= serieskeys +  "' AND type='" +  fixtype
        serieskeys= serieskeys +  "' AND parameter='" +  seriesparameter[1] + "'   )"

        
      if seriessource[1] != "*":
        sourcekey = " AND source = '"  +  seriessource[1] 

      log.info("inFlux-cloud serieskeys %s", serieskeys)


 

      

      if SERIES_KEY2 == "":
      # Just get lat/lng

        query = ('select median(lat) as lat, median(lng) as lng , last(source) as source from {} '
                        'where {}  AND time > {}s and time < {}s '
                       'group by *, time({}s)') \
                  .format( measurement, serieskeys, 
                          startepoch, endepoch,
                          resolution)

        """
        query = ('select median(lat) as lat, median(lng) as lng from {} '
                        'where {} AND time > {}s and time < {}s '
                       'group by time({}s)') \
                  .format( measurement, serieskeys,
                          startepoch, endepoch,
                          resolution)
        """
        
        log.info("inFlux-cloud gps: Position Query %s", query)
        
      else:
      # get lat/lng plus overlay series

        overlayname = SERIES_KEY2
        log.info("inFlux-cloud gps: overlayname Query %s", overlayname)
        
        overlaytags = overlayname.split(".")
        log.info("inFlux-cloud gps: overlaytags Query %s", overlaytags)
        
        overlaydeviceidtag = overlaytags[0]
        overlaydeviceid = overlaydeviceidtag.split(":")

        overlaysensortag = overlaytags[1]
        overlaysensor =overlaysensortag.split(":")

        overlaysourcetag = overlaytags[2]
        overlaysource = overlaysourcetag.split(":")

        overlayinstancetag = overlaytags[3]
        overlayinstance = overlayinstancetag.split(":")

        overlaytypetag = overlaytags[4]
        overlaytype = overlaytypetag.split(":")

        overlayparametertag = overlaytags[5]
        overlayparameter = overlayparametertag.split(":")    

        log.info("inFlux-cloud gps: overlayparameter Query %s", overlayparameter)
        
        overlaykey="( deviceid='"
        overlaykey= overlaykey + overlaydeviceid[1] 
        overlaykey= overlaykey +  "' AND sensor='" +  overlaysensor[1]
        #if overlaysource[1] != "*":
        #  overlaykey= overlaykey +  "' AND source='" +  overlaysource[1] 
        overlaykey= overlaykey +  "' AND instance='" +  overlayinstance[1] 
        overlaykey= overlaykey +  "' AND type='" +  overlaytype[1] 
        overlaykey= overlaykey +  "' AND parameter='" +  overlayparameter[1] + "'   )"

        log.info("inFlux-cloud gps: overlaykey Query %s", overlaykey)

        serieskeys   =    serieskeys  + " OR " +   overlaykey
        log.info("inFlux-cloud gps: serieskeys Query %s", serieskeys)

  
        query = ('select median(lat) as lat, median(lng) as lng, mean({}) as {}, last(source) as source from {} '
                        'where {} AND time > {}s and time < {}s '
                       'group by *, time({}s)') \
                  .format( overlayparameter[1], overlayparameter[1], measurement, serieskeys,
                          startepoch, endepoch,
                          resolution)

        """
        query = ('select median(lat) as lat, median(lng) as lng, mean({}) as overlay, last(source) as source from {} '
                        'where {} AND time > {}s and time < {}s '
                       'group by *, time({}s)') \
                  .format( overlayparameter[1], measurement, serieskeys,
                          startepoch, endepoch,
                          resolution)
        """    

   
        log.info("inFlux gps: Overlay Query %s", query)

        

      try:
        data= db.query(query)
        
      except TypeError as e:
        log.info('get_influxdbcloud_data: Type Error in InfluxDB mydata append %s:  ', query)
        log.info('get_influxdbcloud_data: Type Error in InfluxDB mydata append %s:  ' % str(e))
              
      except KeyError as e:
        log.info('get_influxdbcloud_data: Key Error in InfluxDB mydata append %s:  ', query)
        log.info('get_influxdbcloud_data: Key Error in InfluxDB mydata append %s:  ' % str(e))

      except NameError as e:
        log.info('get_influxdbcloud_data: Name Error in InfluxDB mydata append %s:  ', query)
        log.info('get_influxdbcloud_data: Name Error in InfluxDB mydata append %s:  ' % str(e))
              
      except IndexError as e:
        log.info('get_influxdbcloud_data: Index error in InfluxDB mydata append %s:  ', query)
        log.info('get_influxdbcloud_data: Index Error in InfluxDB mydata append %s:  ' % str(e))  

      except ValueError as e:
        log.info('get_influxdbcloud_data: Index error in InfluxDB mydata append %s:  ', query)
        log.info('get_influxdbcloud_data: Value Error in InfluxDB  %s:  ' % str(e))

      except AttributeError as e:
        log.info('get_influxdbcloud_data: Index error in InfluxDB mydata append %s:  ', query)
        log.info('get_influxdbcloud_data: AttributeError in InfluxDB  %s:  ' % str(e))     

      except InfluxDBClientError as e:
        log.info('get_influxdbcloud_data: Exception Error in InfluxDB  %s:  ' % str(e))     
        
      except:
        #log.info('Telemetrypost: Error in geting Telemetry parameters %s:  ', posttype)
        e = sys.exc_info()[0]
        log.info('inFluxDB gps: Error in geting inFluxDB data %s:  ' % e)
        
        return jsonify( message='Error in inFluxDB query 2', status='error')
        #raise
      
      #return jsonify(results=data)
      #log.info('getgpsseriesbydeviceid: data %s:  ', data)  
      log.info('***************************************************************************************************  ')
      
      if not data:
        return jsonify( message='No data object to return 1', status='error')

      #return jsonify( message='data object to return 1', status='success')
      # return csv formated data
      try:
        jsondata=[]
        jsonkey=[]
        strvaluekey = {'Series1': SERIES_KEY1, 'Series2': SERIES_KEY2,'start': startepoch,  'end': endepoch, 'resolution': resolution}
        jsonkey.append(strvaluekey)
        jsondataarray=[]

        #if overlaykey == "":
        # Just get lat/lng
        keys = data.raw.get('series',[])
        jsondata=[]
        for series in keys:
          #log.info("influxdb results..%s", series )
          #log.info("influxdb results..%s", series )
          strvalue ={}


          #name = series['name']
          name = series['tags']            
          #log.info("inFluxDB_GPS_JSON name %s", name )
          seriesname = series['tags'] 
          #seriestags = seriesname.split(".")
          #seriessourcetag = seriestags[2]
          #seriessource = seriessourcetag.split(":")
          #source= seriesname['source']
          source='FF'
          parameter = seriesname['parameter']
          #log.info("inFluxDB_GPS_JSON values %s", series['values'] )
          
          for point in  series['values']:
            fields = {}
            fields[parameter] = None
            for key, val in zip(series['columns'], point):
              fields[key] = val
            source = fields.get('source', '.*') 
            #strvalue = {'epoch': fields['time'], 'tag':seriesname, 'lat': fields['lat'], 'lng': fields['lng']}
            #log.info("freeboard Get InfluxDB series points %s , %s", fields['time'], fields[parameter])

            mydatetimestr = str(fields['time'])

            #mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')
            mydatetime =  int(time.mktime(time.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')))
            
            #strvalue = {'epoch': fields['time'], 'source':tag['source'], 'value': fields[parameter]}
            if fields[parameter] != None:
              #strvalues = []
              strvalue = {'epoch': mydatetime, 'tag':seriesname, 'value': fields[parameter]}
              strvalues = (mydatetime, source,  parameter, fields[parameter] )

              
              jsondata.append(strvalues)


            
        # here we have an array of seperated lat and lng values taged with epoch times and series tags
        # Like 
        #'(u'HelmSmart', {u'instance': u'0', u'parameter': u'lat', u'deviceid': u'001EC010AD69', u'source': u'06', u'sensor': u'position_rapid', u'type': u'NULL'})':
        # [{u'time': u'2016-08-18T11:00:00Z', u'lng': None, u'lat': 42.012865}],
        # '(u'HelmSmart', {u'instance': u'0', u'parameter': u'lng', u'deviceid': u'001EC010AD69', u'source': u'06', u'sensor': u'position_rapid', u'type': u'NULL'})':
        # [{u'time': u'2016-08-18T11:00:00Z', u'lng': -124.13088, u'lat': None}],
        #
        # We need to reorder this into joined lat and lng based on same epoch times

        #jsondata = sorted(jsondata,key=itemgetter('epoch'))
        log.info('--------------------------------------------------------------------------------------------------  ')
        
        # sort based on epoch times
        jsondata = sorted(jsondata, key=lambda latlng: latlng[0])
        #log.info("getgpsseriesbydeviceid_dbc  jsondata   %s",jsondata)
        #return jsonify( message=jsondata, status='success')

        log.info("getgpsseriesbydeviceid_dbc  jsondata result length  %s: ",len(jsondata))

        # group lat and lng values based on epoch times and get rid of repeated epoch times
        for key, latlnggroup in groupby(jsondata, lambda x: x[0]):

          valuelat = None
          valuelng = None
          valueoverlay = None
          
          for latlng_values in latlnggroup:
            if latlng_values[2] == 'lat':
              valuelat = latlng_values[3]
              valuesource = latlng_values[1]
              
              
            elif latlng_values[2] == 'lng':
              valuelng = latlng_values[3]

            elif latlng_values[2] != None:
              valueoverlay = latlng_values[3]              
              

            
          #strvalues=  {'epoch': key, 'source':thing[1], 'value': thing[3]}

          # if we have valid lat and lng - make a json array
          if  valuelat != None and valuelng != None and valueoverlay != None:
            strvalues=  {'epoch': key, 'source':valuesource, 'lat': valuelat, 'lng': valuelng,  'overlay':valueoverlay}
            jsondataarray.append(strvalues)
            
          elif  valuelat != None and valuelng != None:
            strvalues=  {'epoch': key, 'source':valuesource, 'lat': valuelat, 'lng': valuelng}
            jsondataarray.append(strvalues)
            
            #log.info("freeboard  jsondata group   %s",strvalues)

      except KeyError as e:
        log.info('getgpsseriesbydeviceid_dbc: KeyError in geting gps data parsing  %s:  ', jsondataarray)
        log.info('getgpsseriesbydeviceid_dbc: KeyError in geting gps data parsing  %s:  ' % str(e))
          
      except NameError as e:
        log.info('getgpsseriesbydeviceid_dbc: NameError in geting gps data parsing  %s:  ', jsondataarray)
        log.info('getgpsseriesbydeviceid_dbc: NameError in geting gps data parsing  %s:  ' % str(e))
        
      except:
        #log.info('Telemetrypost: Error in geting Telemetry parameters %s:  ', posttype)
        e = sys.exc_info()[0]
        log.info('getgpsseriesbydeviceid_dbc: Error in geting gps data parsing %s:  ' % e)
      
        return jsonify( message='Error in inFluxDB_GPS  parsing', status='error')

      log.info("getgpsseriesbydeviceid_dbc  jsondataarray result length  %s:",len(jsondataarray))      
      
      if dataformat == 'csv':
        try:
          #def generate():
          #if overlaykey == "":
          # Just get lat/lng
          # create header row
          strvalue ='TimeStamp, serieskey1: ' + SERIES_KEY1 + ', serieskey2: ' + SERIES_KEY2 +', start: ' + startepoch + ', end: ' + endepoch +  ', resolution: ' + resolution  + ' \r\n'

          # create header row
          if SERIES_KEY2 != "":      
            strvalue = strvalue + 'epoch, time, source, lat, lng, seg distance, speed, delta time, ' + overlayparameter[1] + ' \r\n'
          else:
            strvalue = strvalue + 'epoch, time, source, lat, lng, seg distance, speed, delta time \r\n'

       
          #get all other rows
          #for dataset in data:
          jsondata = jsondataarray

          list_length = len(jsondata)
          for i in range(list_length-1):
            oldvector = (jsondata[i]['lat'], jsondata[i]['lng'])
            oldsource = jsondata[i]['source']
            newvector = (jsondata[i+1]['lat'], jsondata[i+1]['lng'])
            newsource = jsondata[i+1]['source']
            
            if (newsource == oldsource) and (newvector != oldvector):
              oldtime = jsondata[i]['epoch']
              newtime = jsondata[i+1]['epoch']

              deltatime = abs(newtime - oldtime)
              
              delta = geodesic(oldvector, newvector).miles
              if deltatime == 0:
                speed = float(0)
              else:
                speed = float((delta/(float(deltatime)))*60*60)

              mytime = datetime.datetime.fromtimestamp(float(jsondata[i]['epoch'])).strftime('%Y-%m-%d %H:%M:%SZ')
                
              if SERIES_KEY2 == "":                
                strvalue = strvalue + str(jsondata[i]['epoch'])+ ', ' + str(mytime) + ', ' + str(jsondata[i]['source']) + ', ' + str(jsondata[i]['lat']) + ', ' + str(jsondata[i]['lng']) + ', ' + str(delta)+ ', ' + str(speed)+ ', ' + str(deltatime) + ' \r\n'
              else:
                strvalue = strvalue + str(jsondata[i]['epoch'])+ ', ' + str(mytime) + ', ' + str(jsondata[i]['source']) + ', ' + str(jsondata[i]['lat']) + ', ' + str(jsondata[i]['lng']) + ', ' + str(delta)+ ', ' + str(speed)+ ', ' + str(deltatime) + ', ' + str(jsondata[i].get('overlay',""))+ ' \r\n'

          response = make_response(strvalue)
          response.headers['Content-Type'] = 'text/csv'
          response.headers["Content-Disposition"] = "attachment; filename=HelmSmart.csv"
          return response
        
        except KeyError as e:
          log.info('inFluxDB_GPS: KeyError in parsing  CSV data  %s:  ', strvalue)
          log.info('inFluxDB_GPS: KeyError in  parsing  CSV data  %s:  ' % str(e))  

        except NameError as e:
          log.info('inFluxDB_GPS: NameError in parsing  CSV data  %s:  ', strvalue)
          log.info('inFluxDB_GPS: NameError in  parsing  CSV data  %s:  ' % str(e))  
        
        except:
          #log.info('Telemetrypost: Error in geting Telemetry parameters %s:  ', posttype)
          e = sys.exc_info()[0]
          log.info('inFluxDB_GPS: Error in geting inFluxDB CSV data %s:  ' % e)
      
          return jsonify( message='Error in inFluxDB_GPS CSV parsing', status='error')

      elif dataformat == 'gpx':
        try:
          #def generate():
          # create header row
          #strvalue ='TimeStamp, serieskey1: ' + SERIES_KEY1 + ', serieskey2: ' + SERIES_KEY2 +', start: ' + startepoch + ', end: ' + endepoch +  ', resolution: ' + resolution  + ' \r\n'
          gpxpoints=[]
          # create header row
          #strvalue = strvalue + 'time, value1, value2, value3, value4 \r\n'
          strvalue = ""
          strvalue = '<?xml version="1.0" encoding="UTF-8"?>' + '\r\n'
          strvalue = strvalue + '<gpx creator="HelmSmart Visualizer http://www.helmsmart.com/" '
          strvalue = strvalue + 'version="1.1" xmlns="http://www.topografix.com/GPX/1/1" '
          strvalue = strvalue + 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
          strvalue = strvalue + 'xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">' + '\r\n'
          strvalue = strvalue + '<trk>' + '\r\n'
          strvalue = strvalue + '<name>Track001</name>' + '\r\n'
          strvalue = strvalue + '<trkseg>' + '\r\n'
          #get all other rows
          gpxpoints = jsondataarray


          #Next go through array and calculate the distance and speed vectors.
          list_length = len(gpxpoints)
          for i in range(list_length-1):
            
              oldvector = (gpxpoints[i]['lat'], gpxpoints[i]['lng'])
              newvector = (gpxpoints[i+1]['lat'], gpxpoints[i+1]['lng'])

              if newvector != oldvector:

                oldtime = gpxpoints[i]['epoch']
                newtime = gpxpoints[i+1]['epoch']

                deltatime = abs(newtime - oldtime)
                
                delta = geodesic(oldvector, newvector).miles

                if deltatime == 0:
                  speed = float(0)
     
                else:
                  speed = float((delta/(float(deltatime)))*60*60)

                # if speed vector less then threshold add to GPX file
                if speed < float(maxthreshold)/100:
                  mytime = datetime.datetime.fromtimestamp(float(gpxpoints[i]['epoch'])).strftime('%Y-%m-%dT%H:%M:%SZ')
                  strvalue = strvalue + '<trkpt lat="' + str(gpxpoints[i]['lat']) + '" lon="' + str(gpxpoints[i]['lng']) + '"> \r\n'
                  strvalue = strvalue + '<time>' + str(mytime) + '</time> \r\n'
                  strvalue = strvalue + '</trkpt> \r\n'

          #close out GPX file with footer
          strvalue = strvalue + '</trkseg> \r\n'
          strvalue = strvalue + '</trk> \r\n'
          strvalue = strvalue + '<extensions> \r\n'
          strvalue = strvalue + '</extensions> \r\n'
          strvalue = strvalue + '</gpx> \r\n'
          
          response = make_response(strvalue)
          response.headers['Content-Type'] = 'text/plain'
          response.headers["Content-Disposition"] = "attachment; filename=HelmSmart.gpx"
          return response
        except:
          #log.info('Telemetrypost: Error in geting Telemetry parameters %s:  ', posttype)
          e = sys.exc_info()[0]
          log.info('inFluxDB_GPS: Error in geting inFluxDB GPX data %s:  ' % e)
      
          return jsonify( message='Error in inFluxDB_GPS GPX parsing', status='error')

      elif dataformat == 'jsonf':
        try:
          jsondata=[]
          jsonkey=[]
          strvaluekey = {'Series1': SERIES_KEY1, 'Series2': SERIES_KEY2,'start': startepoch,  'end': endepoch, 'resolution': resolution}
          jsonkey.append(strvaluekey)

          gpsdata=[]
          jsondata=[]
          #for jsondata in jsondataarray:


          jsondata = jsondataarray


          list_length = len(jsondata)
          for i in range(list_length-1):
            oldvector = (jsondata[i]['lat'], jsondata[i]['lng'])
            oldsource = jsondata[i]['source']
            newvector = (jsondata[i+1]['lat'], jsondata[i+1]['lng'])
            newsource = jsondata[i+1]['source']
            
            if (newsource == oldsource) and (newvector != oldvector):
              oldtime = jsondata[i]['epoch']
              newtime = jsondata[i+1]['epoch']

              deltatime = abs(newtime - oldtime)
              
              delta = geodesic(oldvector, newvector).miles
              if deltatime == 0:
                speed = float(0)
              else:
                speed = float((delta/(float(deltatime)))*60*60)

              if SERIES_KEY2 == "":
                gpsjson = {'epoch': jsondata[i]['epoch'], 'source':jsondata[i]['source'], 'lat':jsondata[i]['lat'], 'lng': jsondata[i]['lng'], 'distance':delta, 'speed':speed, 'interval':deltatime}
              else:
                gpsjson = {'epoch': jsondata[i]['epoch'],  'source':jsondata[i]['source'],'lat':jsondata[i]['lat'], 'lng': jsondata[i]['lng'], 'distance':delta, 'speed':speed, 'overlay': jsondata[i].get('overlay',"")}

              #mininterval
              if deltatime <  float(maxinterval) * 60:
                if speed < float(maxthreshold)/100:
                  gpsdata.append(gpsjson)
          
          #print 'inFluxDB_GPS JSONF returning data points:'

          #return jsonify(serieskey = jsonkey, results = jsondata)
          response = make_response(json.dumps(gpsdata))
          response.headers['Content-Type'] = "application/json"
          response.headers["Content-Disposition"] = "attachment; filename=HelmSmart.json"
          return response

        
        except:
          #log.info('Telemetrypost: Error in geting Telemetry parameters %s:  ', posttype)
          e = sys.exc_info()[0]
          log.info('inFluxDB_GPS: Error in geting inFluxDB JSONF data %s:  ' % e)
      
          return jsonify( message='Error in inFluxDB_GPS JSONF parsing', status='error')
        

      
      elif dataformat == 'json':
        try:


         
          gpsdata=[]
          jsondata=[]
          #for jsondata in jsondataarray:


          jsondata = jsondataarray
          log.info("freeboard  jsondata  %s:  %s",len(jsondata),  jsondata)
          
          list_length = len(jsondata)
          for i in range(list_length-1):
            oldvector = (jsondata[i]['lat'], jsondata[i]['lng'])
            oldsource = jsondata[i]['source']
            newvector = (jsondata[i+1]['lat'], jsondata[i+1]['lng'])
            newsource = jsondata[i+1]['source']
            
            #if (newsource == oldsource) and (newvector != oldvector):
            if  (newvector != oldvector):
              oldtime = jsondata[i]['epoch']
              newtime = jsondata[i+1]['epoch']

              deltatime = abs(newtime - oldtime)
              
              #delta = vincenty(oldvector, newvector).miles
              delta = geodesic(oldvector, newvector).miles
              
              #print 'GetGPSJSON processing dalta points:', delta

              #speed = {'speed':float(delta/(float(deltatime)*60*60))} 
              if deltatime == 0:
                speed = float(0)
   
              else:
                speed = float((delta/(float(deltatime)))*60*60)
              #distance = {'distance':delta}

              if SERIES_KEY2 == "":
                gpsjson = {'epoch': jsondata[i]['epoch'], 'source':jsondata[i]['source'], 'lat':jsondata[i]['lat'], 'lng': jsondata[i]['lng'], 'distance':delta, 'speed':speed, 'interval':deltatime}
              else:
                gpsjson = {'epoch': jsondata[i]['epoch'], 'source':jsondata[i]['source'], 'lat':jsondata[i]['lat'], 'lng': jsondata[i]['lng'], 'distance':delta, 'speed':speed, 'overlay': jsondata[i].get('overlay',"")}
              
              #if delta < float(maxthreshold)/1000:
              if deltatime <  float(maxinterval) * 60:
                if speed < float(maxthreshold)/100:
                  gpsdata.append(gpsjson)

          log.info('getgpsseriesbydeviceid_dbc: gpsdata_len  %s:  ', len(gpsdata) )   
          log.info('getgpsseriesbydeviceid_dbc: gpsdata  %s:  ', gpsdata)      
          #except:
          #  e = sys.exc_info()[0]
          #  log.info('inFluxDB_GPS: Error in geting inFluxDB JSON data %s:  ' % e)

          gpsdata = sorted(gpsdata,key=itemgetter('epoch'))
          #print 'GetGPSJSON returning data points:'
          log.info('getgpsseriesbydeviceid_dbc: returning JSON data:  ' )

          
          return jsonify(serieskey = jsonkey, results = gpsdata)
        
        except AttributeError as e:
          #log.info('inFluxDB_GPS: AttributeError in convert_influxdb_gpsjson %s:  ', data)
          #e = sys.exc_info()[0]

          log.info('getgpsseriesbydeviceid_dbc: AttributeError in parsing json output %s:  ' % str(e))
          
        except TypeError as e:
          #log.info('inFluxDB_GPS: TypeError in convert_influxdb_gpsjson %s:  ', data)
          #e = sys.exc_info()[0]

          log.info('getgpsseriesbydeviceid_dbc: TypeError in  parsing json output  %s:  ' % str(e))

        except KeyError as e:
          #log.info('inFluxDB_GPS: TypeError in convert_influxdb_gpsjson %s:  ', data)
          #e = sys.exc_info()[0]

          log.info('inFluxDB_GPS: KeyError in  parsing json output  %s:  ' % str(e))
          
        except ValueError as e:
          #log.info('inFluxDB_GPS: ValueError in convert_influxdb_gpsjson %s:  ', data)
          #e = sys.exc_info()[0]

          log.info('inFluxDB_GPS: ValueError in  parsing json output  %s:  ' % str(e))            
          
        except NameError as e:
          #log.info('inFluxDB_GPS: NameError in convert_influxdb_gpsjson %s:  ', data)
          #e = sys.exc_info()[0]

          log.info('Sync: NameError in  parsing json output  %s:  ' % str(e))          
        except:
          e = sys.exc_info()[0]
          log.info('getgpsseriesbydeviceid_dbc: Error in  parsing json output  %s:  ' % e)
      
          return jsonify( message='Error in inFluxDB_GPS JSON parsing', status='error')
        
      else:
        result = json.dumps(data.data, cls=DateEncoder)
  
        response = make_response(result) 
    
        response.headers['content-type'] = "application/json"
        return response
  
  except AttributeError as e:
    log.info('getgpsseriesbydeviceid_dbc: AttributeError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
    #e = sys.exc_info()[0]

    log.info('getgpsseriesbydeviceid_dbc: AttributeError in convert_influxdb_gpsjson %s:  ' % str(e))
    
  except TypeError as e:
    log.info('getgpsseriesbydeviceid_dbc: TypeError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
    #e = sys.exc_info()[0]

    log.info('getgpsseriesbydeviceid_dbc: TypeError in convert_influxdb_gpsjson %s:  ' % str(e))
    
  except ValueError as e:
    log.info('getgpsseriesbydeviceid_dbc: ValueError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
    #e = sys.exc_info()[0]

    log.info('getgpsseriesbydeviceid_dbc: ValueError in convert_influxdb_gpsjson %s:  ' % str(e))            
    
  except NameError as e:
    log.info('getgpsseriesbydeviceid_dbc: NameError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
    #e = sys.exc_info()[0]

  except IndexError as e:
    log.info('getgpsseriesbydeviceid_dbc: IndexError in convert_influxdb_gpsjson %s:  ', SERIES_KEY1)
    log.info('getgpsseriesbydeviceid_dbc: IndexError in convert_influxdb_gpsjson %s:  ' % str(e))     
    #e = sys.exc_info()[0]


  except:
    e = sys.exc_info()[0]
    log.info('getgpsseriesbydeviceid_dbc: Error read_data exception data.points %s:  ' % e)
    return jsonify( message='gps_influxdb read_data exception data.points', status='error')
  

  finally:
    db_pool.putconn(conn)



def make_switchpgn(statusvalues, switchinstance, switchid, switchvalue):

  #update new switch value
  statusvalues[int(switchid)]=switchvalue

  #construct switchpgn
  switchpgn = "$PCDIN,01F20E,00000000,00,"
  switchpgn = switchpgn +  "{:02X}".format(int(switchinstance))
  
  swbyte = int(statusvalues[3]) << 2 | int(statusvalues[2])
  switchpgn = switchpgn  +  "{:01X}".format(int(swbyte))  

  
  swbyte = int(statusvalues[1]) << 2 | int(statusvalues[0])
  switchpgn = switchpgn  +  "{:01X}".format(int(swbyte))  

  
  swbyte = int(statusvalues[7]) << 2 | int(statusvalues[6])
  switchpgn = switchpgn  +  "{:01X}".format(int(swbyte))  

  
  swbyte = int(statusvalues[5]) << 2 | int(statusvalues[4])
  switchpgn = switchpgn  +  "{:01X}".format(int(swbyte))  

  
  swbyte = int(statusvalues[11]) << 2 | int(statusvalues[10])
  switchpgn = switchpgn  +  "{:01X}".format(int(swbyte))  

  
  swbyte = int(statusvalues[9]) << 2 | int(statusvalues[8])
  switchpgn = switchpgn  +  "{:01X}".format(int(swbyte))  

  
  swbyte = int(statusvalues[15]) << 2 | int(statusvalues[14])
  switchpgn = switchpgn  +  "{:01X}".format(int(swbyte))  

  
  swbyte = int(statusvalues[13]) << 2 | int(statusvalues[12])
  switchpgn = switchpgn  +  "{:01X}".format(int(swbyte))  


  switchpgn = switchpgn + "FFFFFF*24"

  return switchpgn


def make_dimmerpgn(statusvalues, dimmerinstance, dimmerid, dimmervalue, dimmeroverride):

  #update new dimmer value
  statusvalues[int(dimmerid)]=dimmervalue

  #update new dimmer control value
  statusvalues[4]=dimmeroverride << 4

  #construct dimmerpgn
  #dimmerpgn = "$PCDIN,00FF06,00000000,00,99E1"
  dimmerpgn = "$00FF06#"
  dimmerpgn = dimmerpgn +  "{:02X}".format(int(dimmerinstance))
  dimmerpgn = dimmerpgn  +   "{:02X}".format(int(statusvalues[0]))  
  dimmerpgn = dimmerpgn  +   "{:02X}".format(int(statusvalues[1]))  
  dimmerpgn = dimmerpgn  +   "{:02X}".format(int(statusvalues[2]))
  dimmerpgn = dimmerpgn  +   "{:02X}".format(int(statusvalues[3]))  
  dimmerpgn = dimmerpgn  +   "{:02X}".format(int(statusvalues[4]))
  dimmerpgn = dimmerpgn + "*24"

  return dimmerpgn

def make_timmerpgn_array(timmerArrays, timmerinstance, timmerid, timmervalues):

  #update new timmer value
  timmervalues.replace("[","")
  #log.info("make_timmerpgn   timmervalues length = %s", len(timmervalues))  
  timmervalues.replace("]","")
  #log.info("make_timmerpgn   timmervalues = %s", timmervalues)  
  timmervaluesarray = timmervalues.split(",")
  log.info("make_timmerpgn_array   timmervalues length %s", len(timmerArrays))  
  valueArray = []
  #int(timmerinstance)
  for x in range(0,144):
    #valueArray.append( int(filter(str.isdigit, timmervaluesarray[x])))
    valueArray.append( getIndexFromValue(timmervaluesarray[x]))

  try:
    
    timmerValues =  timmerArrays[int(timmerinstance)]

    log.info("make_timmerpgn_array   timmervalues exists ")  
    for x in range(0,144):
      if int(valueArray[x]) != int(255):
        timmerArrays[int(timmerinstance)][x] = int(valueArray[x])

  except IndexError:
    log.info("make_timmerpgn_array   inserting ")  
    timmerArrays.insert(int(timmerinstance), valueArray)
    
  return
  
def make_timmerpgn(timmerArrays, timmerinstance, timmerid, timmervalues):

  #update new timmer value
  timmervalues.replace("[","")
  #log.info("make_timmerpgn   timmervalues length = %s", len(timmervalues))  
  timmervalues.replace("]","")
  #log.info("make_timmerpgn   timmervalues = %s", timmervalues)  
  timmervaluesarray = timmervalues.split(",")
  
  #log.info("make_timmerpgn   timmervaluesarray length = %s", len(timmervaluesarray))  
  #log.info("make_timmerpgn   timmervaluesarray = %s", timmervaluesarray)  
  #log.info("make_timmerpgn   timmerArray = %s", timmerArray)  
  #construct dimmerpgn
  #dimmerpgn = "$PCDIN,00FF06,00000000,00,99E1"
  timmerpgn = "$00FF07#"
  timmerpgn = timmerpgn +  "{:02X}".format(int(timmerinstance))
  
  log.info("make_timmerpgn   length timmerArray = %s", len(timmerArrays[int(timmerinstance)]))
  
  valueArray = []

  if len(timmerArrays[int(timmerinstance)]) < 144:
  
    for x in range(0,144):
      #valueArray.append( int(filter(str.isdigit, timmervaluesarray[x])))
      valueArray.append( getIndexFromValue(timmervaluesarray[x]))
      
    log.info("make_timmerpgn   valueArray = %s", valueArray)
      
    timmerArrays[int(timmerinstance)].append(valueArray)
      #timmerArrays[int(timmerinstance)].append( int(filter(str.isdigit, timmervaluesarray[x])))
      
  else:
    for x in range(0,144):
      if getIndexFromValue(timmervaluesarray[x])  != int(255):
        #temp = int(filter(str.isdigit, timmervaluesarray[x]))
        temp =getIndexFromValue(timmervaluesarray[x]) 
        

    #if int(timmervaluesarray[x]) != int(255):
     #   timmerArray[x] = int(timmervaluesarray[x])       
        
    timmerpgn = timmerpgn  +   "{:02X}".format(int( timmerArrays[int(timmerinstance)][x]))  

  
  timmerpgn = timmerpgn + "*24"

  return timmerpgn


def getIndexFromValue(valueStr):

  try:
    index = int(re.search("\d+", valueStr)[0])
    
    return index
    
  except:
    e = sys.exc_info()[0]
    log.info('getIndexFromValue: Error  %s:  ' % e)
    return ""

@app.route('/addnewdevice')
def addnewdevice_endpoint():
  
  conn = db_pool.getconn()

  useremail = request.args.get('useremail', '')
  deviceid = request.args.get('deviceid', '000000000000')
  devicename = request.args.get('name', 'SeaSmart')
  status = 1

  userid=hash_string(useremail)
  log.info("addnewdevice- userid %s", userid)
  #deviceapikey=hash_string(userid+deviceid+"083019")
  deviceapikey=hash_string(userid+deviceid+"013024")
  log.info("addnewdevice - deviceapikey %s", deviceapikey)
  
  try:
    
    query  = "select userid from user_devices where useremail = %s"
    cursor = conn.cursor()

    cursor = conn.cursor()
    cursor.execute(query, ( useremail,))
    i = cursor.fetchone()       

    #no existing userid so need to use hashed email for userid and hashed deviceid for combined deviceapikey      
    if cursor.rowcount == 0:
      log.info("addnewdevice - userid does not exist so adding userid and deviceapikey", deviceapikey)
      userstatus = "user does not exist - adding"
      
      query  = "insert into user_devices ( deviceapikey, userid, useremail, deviceid, devicestatus, devicename) Values (%s, %s, %s, %s, %s, %s)"

      # add new device record to DB
      cursor = conn.cursor()
      cursor.execute(query, (deviceapikey, userid, useremail, deviceid, status,  devicename))

      conn.commit()
        
      if cursor.rowcount == 0:
        userstatus = " Could not add user deviceid " + str(deviceid)
        return jsonify( message='Could not add device', status='error')
      
      userstatus = "new userid and deviceapikey added"
      return jsonify( message='Added user deviceid' , deviceapikey=deviceapikey, userstatus = userstatus )

    #userid exists so look up if deviceapikey has already been added
    else:
      userid= str(i[0])
      log.info("Add Device status userid  %s  exists", userid )

      query  = "select deviceapikey from user_devices where userid = %s and deviceid = %s"
      cursor = conn.cursor()

      cursor = conn.cursor()
      cursor.execute(query, ( userid, deviceid))
      i = cursor.fetchone()       

      #no existing deviceapikey so add new one 
      if cursor.rowcount == 0:
      
        log.info("addnewdevice - udeviceapikey does not exist so adding  deviceapikey %s", deviceapikey)
        userstatus = "deviceapikey does not exist - adding"
        
        query  = "insert into user_devices ( deviceapikey, userid, useremail, deviceid, devicestatus, devicename) Values (%s, %s, %s, %s, %s, %s)"

        # add new device record to DB
        cursor = conn.cursor()
        cursor.execute(query, (deviceapikey, userid, useremail, deviceid, status,  devicename))

        conn.commit()
          
        if cursor.rowcount == 0:
          userstatus = " Could not add user deviceid " + str(deviceid)
          return jsonify( message='Could not add device', status='error')
        
        userstatus = "deviceapikey new deviceapikey added"
        return jsonify( message='Added user deviceid' , deviceapikey=deviceapikey, userstatus = userstatus )     

      #deviceapikey already exists so just return it
      else:
        deviceapikey= str(i[0])
        log.info("Add Device status - deviceapikey already exixts %s", deviceapikey)
        userstatus = "user deviceid " + str(deviceid) + " already exists"
        
        return jsonify( message='user deviceidapikey already exists' , deviceapikey=deviceapikey, userstatus = userstatus )

  except TypeError as e:
    log.info("Add Device error -:TypeError deviceid %s ", deviceid)
    log.info('Add Device error -:TypeError  Error %s:  ' % e)
    return jsonify( message='Add user deviceid error - failed' , deviceapikey=deviceapikey, userstatus = "could not add deviceapikey" )

  except:
    e = sys.exc_info()[0]
    log.info("Add Device error - Error in adding device %s", deviceid)
    log.info('Add Device error: Error in adding device %s:  ' % e)
    return jsonify( message='Add user deviceid error - failed' , deviceapikey=deviceapikey, userstatus = "could not add deviceapikey" )
  
  finally:
    db_pool.putconn(conn)    

@app.route('/updatedevice')
def updatedevice_endpoint():
  
  conn = db_pool.getconn()
  
  deviceapikey = request.args.get('deviceapikey', '')
  alertemail = request.args.get('alertemail', '')
  alertsms = request.args.get('alertsms', '')
  devicename = request.args.get('devicename', 'SeaSmart')

  log.info("Update Device  - update user_devices SET devicename = %s, alertemail = %s, smsnumber = %s WHERE deviceapikey =  %s", devicename, alertemail, alertsms, deviceapikey)
 
  query  = "update user_devices SET devicename = %s, alertemail = %s, smsnumber = %s WHERE deviceapikey =  %s"
  
  try:
    # add new device record to DB
    cursor = conn.cursor()
    cursor.execute(query, (devicename, alertemail, alertsms, deviceapikey))

    conn.commit()
    #i = cursor.fetchone()
    # if not then just exit
    #if cursor.rowcount == 0:
      
    if cursor.rowcount == 0:
          return jsonify( message='Could not update device', status='error')      
    else:
          return jsonify( message='device updated', status='success') 
  
    

  finally:
    db_pool.putconn(conn)   

@app.route('/deletedevice')
def deletedevice_endpoint():
  
  conn = db_pool.getconn()
  
  deviceapikey = request.args.get('deviceapikey', '')
  useremail = request.args.get('useremail', '')
  deviceid = request.args.get('deviceid', '000000000000')
  devicename = request.args.get('name', '')


 
  query  = "delete from user_devices where deviceapikey = %s AND deviceid = %s AND useremail = %s "
  
  try:
    # add new device record to DB
    cursor = conn.cursor()
    cursor.execute(query, (deviceapikey, deviceid, useremail))

    conn.commit()
    #i = cursor.fetchone()
    # if not then just exit
    #if cursor.rowcount == 0:
      
    if cursor.rowcount == 0:
          return jsonify( message='Could not delete device', status='error')      
    else:
          return jsonify( message='device deleted', status='success') 
  
    

  finally:
    db_pool.putconn(conn)


def check_device_subscription_active(device_id):

  log.info("check_device_subscription_active device_id %s:  ", device_id)

  conn = db_pool.getconn()
  
  #query  = "select  subscriptionenddate, devicestatus from user_devices where  deviceid = %s "
  #query  = "select  COALESCE(subscriptionenddate, None), devicestatus from user_devices where  deviceid = %s "
  query  = "select  COALESCE(subscriptionenddate, '2026-01-01'), devicestatus from user_devices where  deviceid = %s "
  
  try:
    # add new device record to DB
    cursor = conn.cursor()
    cursor.execute(query, (device_id, ))

    conn.commit()

    i = cursor.fetchone()
    # if not then just exit
    #if cursor.rowcount == 0:
      
    if cursor.rowcount == 0:
      log.info("check_device_subscription_active device not found device_id %s:  ", device_id)
      return False
    
    else:
      
      # Get subscription end date
      subscription_end_date= str(i[0])
      devicestatus= str(i[1])
      
      log.info("check_device_subscription_active device found device_id %s: enddate %s devicestatus %s", device_id, subscription_end_date, devicestatus)

      #if subscription_end_date != "" and subscription_end_date != None and subscription_end_date is not None:
      if subscription_end_date:      

        date_object = datetime.datetime.strptime(subscription_end_date, "%Y-%m-%d").date()
        log.info("check_device_subscription_active device found device_id %s: date_object %s ", device_id, date_object)
        
        nowday = date.today()
        log.info("check_device_subscription_active device found device_id %s: todaydate %s ", device_id, nowday)

        if nowday < date_object:
          log.info("check_device_subscription_active device found device_id subscription active")


          try:
            query  = "update user_devices SET devicestatus=1 where deviceid=%s"
            cursor = conn.cursor()
            cursor.execute(query, (device_id, ))

            conn.commit()
            
          except:
            e = sys.exc_info()[0]
            log.info("check_device_subscription_active: DB update error device_id %s ", device_id)
            log.info('check_device_subscription_active: DB update error %s:  ' % e)
          
          return True

        else:
          log.info("check_device_subscription_active device found device_id subscription inactive")

          try:
            query  = "update user_devices SET devicestatus=0 where deviceid=%s"
            cursor = conn.cursor()
            cursor.execute(query, (device_id, ))

            conn.commit()
            
          except:
            e = sys.exc_info()[0]
            log.info("check_device_subscription_active: DB update error device_id %s ", device_id)
            log.info('check_device_subscription_active: DB update error %s:  ' % e)
          
          return False

      else:
        log.info("check_device_subscription_active device found device_id subscription unknown")          
      
        return False
  
    

  finally:
    db_pool.putconn(conn)  



# **********************************************************************
#
# MAin SeaSmart/SeaGauge HTTP POST
# takes data from POST and adds to SQS que for workers to process
#
# **********************************************************************

@app.route('/devices/<device_id>/PushCache/<partition>', methods=['POST'])
@cross_origin()
def events_endpoint(device_id, partition):



  try:

    log.info("Que SQS:Parse JSON request.data %s:  ", request.data)

    # ######################################################
    # First lets package the seasmart gateway payload into a json so we can place in SQS queue
    # #######################################################

    device_json = json.dumps(
      dict(
              device_id = device_id,
              partition = partition,
              payload =  request.data,
              content_type = request.content_type,
              dyno_id = os.environ['DYNO']
            ),
      cls=DateEncoder)

    #log.info("Que SQS:Parse JSON device_id %s: partition: %s data: %s ", device_id, partition, device_json)
    log.info("Que SQS:Parse JSON device_id %s:  ", device_id)
    log.info("Que SQS:Parse JSON device_json %s:  ", device_json)

  except SystemExit as e:
    log.info("Que SQS:SystemExitError device_id %s: partition: %s data: %s ", device_id, partition, request.data)
    log.info('Que SQS:SystemExitError  Error in que SQS %s:  ' % e)

  except NameError as e:
    log.info("Que SQS:NameError device_id %s: %s ", device_id, request.data)
    log.info('Que SQS:NameError  Error in que SQS %s:  ' % e)

  except TypeError as e:
    log.info("Que SQS:TypeError device_id %s: %s ", device_id, request.data)
    log.info('Que SQS:TypeError  Error in que SQS %s:  ' % e)
    
  except UnicodeDecodeError as e:
    log.info("Que SQS:UnicodeDecodeError device_id %s: %s ", device_id, request.data)
    log.info('Que SQS:UnicodeDecodeError  Error in que SQS %s:  ' % e)
    
  except:
    e = sys.exc_info()[0]
    log.info("Que SQS:device_id %s: partition: %s data: %s ", device_id, partition, request.data)
    log.info('Que SQS: Error in que SQS %s:  ' % e)


  ##################################################################
  ## use deviceid to see if its in the database and enabled
  ##################################################################
  deviceid_enabled = mc.get(device_id + '_enabled' )
  log.info('events_endpoint - start subscription check device_id %s deviceid_enabled %s :  ', device_id, deviceid_enabled)
  
  if deviceid_enabled != "" and deviceid_enabled != None and deviceid_enabled is not None:
    
    device_subscription_active = deviceid_enabled
    log.info('events_endpoint - subscription check device_id %s device_subscription_active %s :  ', device_id, device_subscription_active)
    
  else:
  
    device_subscription_active = check_device_subscription_active(device_id)
    log.info('events_endpoint - subscription check device_id %s device_subscription_active %s :  ', device_id, device_subscription_active)

    mc.set(device_id + '_enabled' , device_subscription_active, time=120)
    
  ##################################################################
  # if subcription is inactive - just exit and do not process any data
  ##################################################################
  if device_subscription_active == False:
    epochtime =  int(time.time())

    log.info('events_endpoint device_id %s is subscription_inactive : exiting ', device_id)
    
    return jsonify(result="OK", epochtime=epochtime)
    
  ##################################################################

    
  try:
    # ######################################################
    # now place in PUSHSMART SQS queue
    # #######################################################
    # Send message to SQS queue
    response = sqs_queue.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        #MessageAttributes={ 'Device': {  'deviceid':device_id} },
        MessageBody=(device_json)
    )

    #print(response['MessageId'])

    log.info("Send SQS he:helmsmart-pushsmart  %s:  response %s: ", device_id,response['MessageId'])


    # Send message to SQS queue
    response = sqs_queue.send_message(
        QueueUrl="https://sqs.us-west-2.amazonaws.com/291312677175/helmsmart-cloud",
        DelaySeconds=10,
        #MessageAttributes={ 'Device': {  'deviceid':device_id} },
        MessageBody=(device_json)
    )

    #print(response['MessageId'])

    log.info("Send SQS helmsmart-cloud :device_id %s:  response %s: ", device_id,response['MessageId'])


    

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



  try:
    # ######################################################
    # now place in PUSHSMART RAW SQS queue
    # #######################################################
    # Send message to SQS queue

    response = sqs_queue.send_message(
        QueueUrl=psraw_queue_url,
        DelaySeconds=10,
        #MessageAttributes={ 'Device': {  'deviceid':device_id} },
        MessageBody=(device_json)
    )

    #print(response['MessageId'])

    log.info("Send SQS PSRAW:device_id %s:  response %s: ", device_id,response['MessageId'])


    
  except botocore.exceptions.ClientError as e:
    log.info("Send SQS PSRAW:ClientError device_id %s:  ", device_id)
    log.info('Send SQS PSRAW:ClientError  Error in que SQS %s:  ' % e)

  except botocore.exceptions.ParamValidationError as e:
    log.info("Send SQS PSRAW:ParamValidationError device_id %s:  ", device_id)
    log.info('Send SQS PSRAW:ParamValidationError  Error in que SQS %s:  ' % e)

  except NameError as e:
    log.info("Send SQS PSRAW:NameError device_id %s:  ", device_id)
    log.info('Send SQS PSRAW:NameError  Error in que SQS %s:  ' % e)    
    
  except:
    e = sys.exc_info()[0]
    log.info("Send SQS PSRAW:device_id %s:  ", device_id)
    log.info('Send SQS PSRAW: Error in que SQS %s:  ' % e)


  # ######################################################
  # Next we will check MCACHER for any Switch keys
  # #######################################################
  switchitem = ""
  switchpgn=""
  # Memcacher get
  try:
    switchitem = mc.get(device_id + '_switch' )
    log.info('events_endpoint - MemCache switch get  deviceid %s payload %s:  ', device_id, switchitem)

  except:
    switchitem = ""
    log.info('events_endpoint - MemCache switch error  deviceid %s payload %s:  ', device_id, switchitem)
    e = sys.exc_info()[0]
    log.info('events_endpoint - MemCache switch error %s:  ' % e)

  if switchitem != "" and switchitem != None and switchitem is not None:
    switchpgn=""
    statusvalues=[]
    statusvalues.append(int(3))    
    statusvalues.append(int(3))
    statusvalues.append(int(3))
    statusvalues.append(int(3))
    statusvalues.append(int(3))
    statusvalues.append(int(3))
    statusvalues.append(int(3))
    statusvalues.append(int(3))
    statusvalues.append(int(3))
    statusvalues.append(int(3))
    statusvalues.append(int(3))
    statusvalues.append(int(3))
    statusvalues.append(int(3))
    statusvalues.append(int(3))
    statusvalues.append(int(3))
    statusvalues.append(int(3))

    log.info("events_endpoint get switch key %s", switchitem )

    #for each event make a new Switch PGN that adds in the previous events
    for data in switchitem:
      log.info("events_endpoint get switch data %s ", data)
      #json_data = json.loads(data)
      #log.info("events_endpoint get switch jsondata %s %s %s", json_data.instance,  json_data.switchid, json_data.switchvalue)
      switchinstance = int(data['instance'])
      switchid = int(data['switchid'])
      switchvalue = int(data['switchvalue'])
      # append switch events so we write them once
      switchpgn = make_switchpgn(statusvalues, switchinstance,switchid,switchvalue)
      log.info("events_endpoint get make switchpgn %s", switchpgn )
      

    # Memcacher delete
    try:
      mc.delete(device_id + '_switch' )
      log.info('events_endpoint - MemCache switch delete  deviceid %s payload %s:  ', device_id, switchpgn)
      
    except:
      log.info('events_endpoint - MemCache switch error  deviceid %s payload %s:  ', device_id, switchpgn)
      e = sys.exc_info()[0]
      log.info('events_endpoint - MemCache switch error %s:  ' % e)
    #break

  else:
    switchpgn="" 
    log.info("events_endpoint no values in switch cache %s", switchpgn )

  # ######################################################
  # Next we will check MCACHER for any dimmer keys
  # #######################################################
  dimmeritem = ""
  dimmerpgn=""
  dimmerpgns=[]
# Memcacher get
  try:

    dimmeritem = mc.get(device_id + '_dimmer' )

    log.info('events_endpoint - MemCache dimmer get  deviceid %s payload %s:  ', device_id, dimmeritem)


  except:
    dimmeritem = ""
    log.info('events_endpoint - MemCache dimmer error  deviceid %s payload %s:  ', device_id, dimmeritem)
    e = sys.exc_info()[0]
    log.info('events_endpoint - MemCache dimmer error %s:  ' % e)    

  if dimmeritem != ""  and dimmeritem != None and dimmeritem is not None:
    dimmerpgn=""
    statusvalues=[]

    for x in range(0,256):
      statusvalues.append(int(255))    

    
    # sort list so higher overrides are last to be sure they take effect
    # 0 = No Override and will be deleted from MemCache on next HTTP Post from Gateway
    # 1 = Remove Override - sent from WebPage to trun override Off
    # 2-4 = Enabel override whihc is not removed from MemCache untill a override=1 is recieved.
    dimmeritem = sorted(dimmeritem, key = lambda i: ( i['dimmeroverride'],i['instance'])) 

    log.info("events_endpoint get dimmer key %s", dimmeritem )

    dimmerpgns=[]
    savedimmeritems = []
    
    for data in dimmeritem:
      log.info("events_endpoint get dimmer data %s", data )
      dimmerinstance = int(data['instance'])
      dimmerid = int(data['dimmerid'])
      dimmervalue = int(data['dimmervalue'])
      dimmeroverride = int(data['dimmeroverride'])
      log.info("events_endpoint get make dimmerpgn dimmeroverride %s", dimmeroverride )
    
      # Make up Responce dimmer PGN to send back to gateway if valid dimmervalue only if override is not false
      if dimmeroverride != 1 and dimmervalue != 255:
        dimmerpgn = make_dimmerpgn(statusvalues, dimmerinstance,dimmerid,dimmervalue,dimmeroverride)
        log.info("events_endpoint get make dimmerpgn %s", dimmerpgn )
        dimmerpgns.append(dimmerpgn)
        log.info("events_endpoint get make dimmerpgns %s", dimmerpgns )
        
      else:
        log.info("events_endpoint NULL dimmervalue so ignore " )
      

    # Memcacher delete
    try:

      # dont delete any active overides  - they expire in 10 minutes if not renewed
      mc.delete(device_id + '_dimmer' )
      log.info('events_endpoint - MemCache dimmer delete  deviceid %s payload %s:  ', device_id, dimmerpgns)

        
    except:
      log.info('events_endpoint - MemCache dimmer error  deviceid %s payload %s:  ', device_id, dimmerpgns)
      e = sys.exc_info()[0]
      log.info('events_endpoint - MemCache dimmer error %s:  ' % e)

  # ######################################################
  # Next we will check MCACHER for any timmer keys
  # #######################################################
  timmeritem = ""
  timmerpgn=""
  timmerpgns=[]
 # Memcacher get
  # first get global instance counter for device id
  # global variable for timmer instances used in memcache ids
  #variable is incremented in each device push from 0 to 31 so
  #that we only pick one instance at a time.
  #This prevents pushing too many timmer updates at once to each gateway.
  #Thus we only push one timmer instance at a time but cycle though all of them eventually
  global_t_instance=0
  try:
    #global_t_instance  is a counter  that modo 32   
    global_t_instance = mc.get(device_id + '_timmerid' )
    
    #global_t_instance  is a counter  that modo 32
    if not (0 <= global_t_instance <= 31):
      global_t_instance=0
    #  mc.incr((device_id + '_timmerid' ))      

    #else:
    #  global_t_instance=0
    #  mc.set((device_id + '_timmerid' ), global_t_instance)
      
    log.info('events_endpoint - MemCache get timmerid  deviceid %s global_t_instance %s:  ', device_id, global_t_instance)
    
  except:
    global_t_instance = 0
    #mc.set((device_id + '_timmerid' ), global_t_instance)
    #log.info('events_endpoint - MemCache timmer error  deviceid %s global_t_instance %s:  ', device_id, global_t_instance)
    e = sys.exc_info()[0]
    #log.info('events_endpoint - MemCache timmer error %s:  ' % e)

  timmeritem = ""

  cache_instance = global_t_instance

  for x in range(0, 32):

  
    try:
      #global_t_instance  is a counter  that modo 32

      timmerid =str(device_id) + '_timmer_' +  str(cache_instance)
      #log.info('events_endpoint - MemCache timmer get  deviceid %s timmerid %s:  ', device_id, timmerid)
      
      timmeritem = mc.get(timmerid )

      #log.info('events_endpoint - MemCache timmer get  timmerid %s payload %s:  ', timmerid, timmeritem)

      if timmeritem != ""  and timmeritem != None and timmeritem is not None:
        global_t_instance = cache_instance
        break
      
      else:
        global_t_instance =  cache_instance
        cache_instance  = ((cache_instance+1) % 32)
      
    except:
      timmeritem = ""
      #log.info('events_endpoint - MemCache read timmer error  timmerid %s :  ', timmerid)
      e = sys.exc_info()[0]
      #log.info('events_endpoint - MemCache timmer error %s:  ' % e)

  #update instance index to point to next one
  mc.set((device_id + '_timmerid' ), ((global_t_instance+1) % 32))      
  log.info('events_endpoint - MemCache read timmer loop completed  timmerid %s instance %s :  ', device_id, global_t_instance)
 
  
  if timmeritem != ""  and timmeritem != None and timmeritem is not None:
    timmerpgn=""
    timmerArrays=[]
    timmerArray=[]

        
    for t_instance in range(0,16):
      timmerArrays.append(timmerArray)
         
    #for each event make a new Switch PGN that adds in the previous events
    timmerpgns=[]
    for data in timmeritem:
      #log.info("events_endpoint get timmer data %s", data )
      timmerinstance = int(data['instance'])
      timmertype = data['timmerid']
      timmerparameter = str(data.get('timmerparameter', 'value0'))
      timmervalues = str(data['timmervalues'])
      # append switch events so we write them once
      #timmerpgn = make_timmerpgn_array(timmerArrays, timmerinstance,timmerid,str(timmervalues))


      #update new timmer value
      timmervalues.replace("[","")
      #log.info("make_timmerpgn   timmervalues length = %s", len(timmervalues))  
      timmervalues.replace("]","")
      #log.info("make_timmerpgn   timmervalues = %s", timmervalues)  
      timmervaluesarray = timmervalues.split(",")
      log.info("make_timmerpgn_array   timmervalues length %s", len(timmerArrays))
      log.info("make_timmerpgn_array   timmerinstance %s", timmerinstance)
      log.info("make_timmerpgn_array   timmertype %s", timmertype)
      log.info("make_timmerpgn_array   timmerparameter %s", timmerparameter)

      
      #timmerparameterindex =  int(filter(str.isdigit, timmerparameter))
      timmerparameterindex = getIndexFromValue( timmerparameter)

      
      log.info("make_timmerpgn_array   timmerparameterindex %s", timmerparameterindex)
      valueArray = []
      #int(timmerinstance)
      for x in range(0,144):
        valueArray.append( getIndexFromValue(timmervaluesarray[x]))
        
      log.info("events_endpoint get make_timmerpgn_array valueArray %s", valueArray )
      
      try:
        
        timmerValues =  timmerArrays[int(timmerinstance)]

        log.info("make_timmerpgn_array   timmervalues exists %s", len(timmerValues))

        if len(timmerValues) == 144:
          log.info("make_timmerpgn_array   old timmervalues exists ")
          for x in range(0,144):
            if int(valueArray[x]) != int(255):
              timmerArrays[int(timmerinstance)][x] = int(valueArray[x])
        else:
          log.info("make_timmerpgn_array   adding new timmervalues  ")
          #for x in range(0,144):
          timmerArrays[int(timmerinstance)]=( valueArray)
              
      except IndexError:
        log.info("make_timmerpgn_array   IndexError %s " , int(timmerinstance))  
        #timmerArrays.insert(int(timmerinstance), valueArray)



    #log.info("events_endpoint get make timmerArrays %s", timmerArrays )  

    for t_instance in range(0,16):
      if len(timmerArrays[t_instance]) !=0:
        if str(timmertype) == "LED 1 Channel":
          timmerpgn = "$00FF07#"
        elif str(timmertype) == "RGB 1 Channel":
          timmerpgn = "$00FF08#"
        elif str(timmertype) == "LED 4 Channel":
          timmerpgn = "$00FF09#"
        else :
          timmerpgn = "$00FF0A#"
          
        timmerpgn = timmerpgn +  "{:02X}".format(t_instance)        
        for x in range(0,144):               
          timmerpgn = timmerpgn  +   "{:02X}".format(int( timmerArrays[t_instance][x]))  
        timmerpgn = timmerpgn + "*24"
        #log.info("events_endpoint get make timmerpgn %s", timmerpgn )
             
        timmerpgns.append(timmerpgn)
    

    log.info("events_endpoint created timmerpgns %s -> %s", device_id, timmerpgns )
    # Memcacher delete
    try:
      #mc.delete(device_id + '_timmer_' + str(global_t_instance))
      log.info('events_endpoint - MemCache timmer delete  deviceid %s payload %s:  ', device_id, timmerpgns)
      
    except:
      log.info('events_endpoint - MemCache timmer error  deviceid %s payload %s:  ', device_id, timmerpgns)
      e = sys.exc_info()[0]
      log.info('events_endpoint - MemCache timmer error %s:  ' % e)
    #break

  else:
    timmeritem = ""
    timmerpgns=[]
    log.info("events_endpoint no values in timmer cache %s", timmerpgns )



  # ######################################################
  # Now return response based on any cached switch/dimmer/timmer keys
  # #######################################################
  epochtime =  int(time.time())

  log.info("events_endpoint memc keys switchpgn %s dimmerpgns %s timmerpgns %s",switchpgn, dimmerpgns, timmerpgns )
  
  if switchpgn == "" and len(dimmerpgns) == 0 and len(timmerpgns) == 0:
    log.info("events_endpoint sending empty post response %s", device_id ) 
    return jsonify(result="OK", epochtime=epochtime)

  elif switchpgn != "" and len(dimmerpgns) == 0 and len(timmerpgns) == 0:
    log.info("events_endpoint sending switchpgn %s", switchpgn )  
    #cache.delete(cache=device_id, key="switch_0")
    return jsonify(result="OK", switch=switchpgn, epochtime=epochtime)

  elif switchpgn == "" and len(dimmerpgns) != 0 and len(timmerpgns) == 0:
    log.info("events_endpoint sending dimmer key %s", dimmeritem )
    #cache.delete(cache=device_id, key="dimmer")
    return jsonify(result="OK", dimmer=dimmerpgns, epochtime=epochtime)

  elif switchpgn == "" and len(dimmerpgns) != 0 and len(timmerpgns) != 0:
    log.info("events_endpoint sending dimmer key %s", dimmeritem )
    #cache.delete(cache=device_id, key="dimmer")
    return jsonify(result="OK", dimmer=dimmerpgns, timmer=timmerpgns,  epochtime=epochtime)  


  elif switchpgn == "" and len(dimmerpgns) == 0 and len(timmerpgns) != 0:
    log.info("events_endpoint sending timmer key %s", timmerpgns )
    #cache.delete(cache=device_id, key="dimmer")
    return jsonify(result="OK", timmer=timmerpgns, epochtime=epochtime)

  # ######################################################
  # finally we always return the current time in the responce
  # #######################################################


  #epochtime =  int(time.time())
  #return jsonify(result="OK", epochtime=epochtime)   

# End of main POST routine


@app.route('/freeboard_tcp/<apikey>', methods=['GET','POST'])
@cross_origin()
def freeboard_tcp(apikey):

    deviceapikey =apikey
    Interval = "1min"
     
    #deviceapikey = request.args.get('apikey','')
    #serieskey = request.args.get('datakey','')
    #Interval = request.args.get('Interval',"1min")

    #return jsonify(result="OK")
    
    response = None

    starttime = 0

    epochtimes = getepochtimes(Interval)
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    resolution = epochtimes[2]


    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        #callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })
      return "invalid deviceid"


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)




    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    serieskeys= serieskeys +  " sensor='tcp'  "
    #serieskeys= serieskeys +  " (type='True') " 

    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)



      
    query = ('select  DISTINCT(raw) AS raw  from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by *, time({}s) LIMIT 1') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution) 
 


    log.info("freeboard data Query %s", query)
    #return jsonify(result="OK")

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))


            
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', response)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        pass

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        #callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return 'error - no data'


    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        #callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return 'error - no data'
      
    #return jsonify(result="OK")
    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)

    keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    PGNValues=""
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'

      for series in keys:
        #log.info("influxdb results..%s", series )
        #log.info("influxdb results..%s", series )
        strvalue ={}
 
        #points = list(response.get_points())

        #log.info('freeboard:  InfluxDB-Cloud points%s:', points)

        #name = series['name']
        name = series['tags']            
        #log.info("inFluxDB_GPS_JSON name %s", name )
        seriesname = series['tags'] 
        #seriestags = seriesname.split(".")
        #seriessourcetag = seriestags[2]
        #seriessource = seriessourcetag.split(":")
        source= seriesname['source']
        PGN= seriesname['type']
        parameter = seriesname['parameter']
        #log.info("inFluxDB_GPS_JSON values %s", series['values'] )
        #pgnpoints = series['values']
        for point in  series['values']:
          #pgnpoints = point['raw']
          fields = {}
          for key, val in zip(series['columns'], point):
            fields[key] = val
            
        PGNValues= PGNValues + fields['raw'] + '\r\n'        
        """
        for point in  series['values']:
          fields = {}
          fields[parameter] = None
          for key, val in zip(series['columns'], point):
            fields[key] = val
            
          #strvalue = {'epoch': fields['time'], 'tag':seriesname, 'lat': fields['lat'], 'lng': fields['lng']}
          #log.info("freeboard Get InfluxDB series points %s , %s", fields['time'], fields[parameter])

          mydatetimestr = str(fields['time'])

          #mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')
          mydatetime =  int(time.mktime(time.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')))
          
          #strvalue = {'epoch': fields['time'], 'source':tag['source'], 'value': fields[parameter]}
          if fields[parameter] != None:
            #strvalues = []
            strvalue = {'epoch': mydatetime, 'tag':seriesname, 'PGN':PGN, 'value': fields[parameter]}
            strvalues = (mydatetime, PGN,  parameter, fields[parameter] )

            
        jsondata.append(strvalues)
        """
        #PGNValues= PGNValues + pgnpoints['raw'] + "\r\n"

        """
        for point in points:
          log.info('freeboard:  InfluxDB-Cloud point%s:', point)
          if point['raw'] is not None: 
            value1 = point['raw']
            

         
          mydatetimestr = str(point['time'])

          mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')

        log.info('freeboard: freeboard returning data values tcp:%s,   ', value1)            
        """
      #callback = request.args.get('callback')
      #myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")


      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','lat':value1, 'lng':value2,})
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','raw':value1})
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True','raw':jsondata})
      #response = make_response(PGNValues)
      #response.headers['Content-Type'] = 'text/txt'
      #return response
      #return jsonify(result="OK", PGNValues='$PCDIN,01F010,69BEO231,06,C6F09D42309D3926*5F\r\n$PCDIN,01F112,69BEO22M,06,EAE2090000390AFD*2A\r\n$PCDIN,01F119,69BEO23E,06,C1FF7FE9FE3BFEFF*25\r\n$PCDIN,01F11A,69BEO23D,06,C1F59D42390AFFFF*53\r\n$PCDIN,01F801,69BEO22K,06,20A80A191C2103B6*20\r\n$PCDIN,01F802,69BEO22L,06,C6FCD8BC0A00FFFF*5C\r\n')
      #return jsonify(result="OK", PGNValues=PGNValues[0:1024])
      return PGNValues[0:3072]
      #return jsonify(results = PGNValues)

    except TypeError as e:
      #log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
      #log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
      #log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))          
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        #callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })
        return 'error'

  
    #return jsonify(status='error', update=False )
    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })
    return 'error'

@app.route('/websockettest')
def main():
        return render_template('websockettest.html')

@socketio.on('connect')
def handle_connect(auth):
  log.info('socketio handle_connect: message %s:  ' , auth)
  hello_message = {
      "name": "HelmSmart Signal K Server",
      "version": "0.1.0",
      "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
      "self": "vessels.urn:mrn:signalk:uuid:c0d79334-4e25-4245-8892-54e8ccc8021d",
      "roles": ["master"]
  }
  #send(message)
  sid = request.sid
  emit(hello_message, room=sid)


@socketio.on('message')
def handle_message(message):
  log.info('socketio handle_message: message %s:  ', message)
  hello_message = {
      "name": "HelmSmart Signal K Server",
      "version": "0.1.0",
      "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
      "self": "vessels.urn:mrn:signalk:uuid:c0d79334-4e25-4245-8892-54e8ccc8021d",
      "roles": ["master"]
  }
  #send(message)
  sid = request.sid
  emit(hello_message, room=sid)

"""
@app.route('/signalk')
@cross_origin()
def signalk_hello():

  hello_message = {
      "name": "HelmSmart Signal K Server",
      "version": "0.1.0",
      "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
      "self": "vessels.urn:mrn:signalk:uuid:c0d79334-4e25-4245-8892-54e8ccc8021d",
      "roles": ["master"]
  }

  return json.dumps(hello_message)
"""


@app.route('/signalk')
@cross_origin()
def signalk_hello():

  hello_message = {
      "endpoints": {
          "v1": {
              "version": "1.1.2",
              #"signalk-http": "http://www.helmsmart-cloud.com/signalk/v1/api/"
              "signalk-ws": "ws://www.helmsmart-cloud.com/signalk/v1/stream"
          }
      }
  }
  return json.dumps(hello_message)








@app.route('/signalk/v1/api/self')
@cross_origin()
def signalk_api_self():

  hello_message = {
      "name": "HelmSmart Signal K Server",
      "version": "0.1.0",
      "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
      #"self": "vessels.urn:mrn:signalk:uuid:c0d79334-4e25-4245-8892-54e8ccc8021d",
      "self": "urn:mrn:imo:mmsi:338184312",
      "mmsi": "338184312",
      "roles": ["master"]
  }
  return json.dumps(hello_message)






@app.route('/signalk/v1/api/vessels/self/')
@cross_origin()
def signalk_api_vessels_self():

  hello_message = {
    "version": "1.0.0",
    "self": "urn:mrn:signalk:uuid:705f5f1a-efaf-44aa-9cb8-a0fd6305567c",
    "vessels": {
      "urn:mrn:signalk:uuid:705f5f1a-efaf-44aa-9cb8-a0fd6305567c": {
        "navigation": {
          "speedOverGround": {
            "value": 4.32693662,
            "$source": "ttyUSB0.GP",
            "sentence": "RMC",
            "timestamp": "2017-05-16T05:15:50.007Z"
          },
          "position": {
            "value": {
              "altitude": 0.0,
              "latitude": 37.81479,
              "longitude": -122.44880152
            },
            "$source": "ttyUSB0.GP",
            "sentence": "RMC",
            "timestamp": "2017-05-16T05:15:50.007Z"
          },
          "headingMagnetic": {
            "value": 5.55014702,
            "$source": "ttyUSB0.II",
            "sentence": "HDM",
            "timestamp": "2017-05-16T05:15:54.006Z"
          }
        },
        "name": "Motu",
        "uuid": "urn:mrn:signalk:uuid:705f5f1a-efaf-44aa-9cb8-a0fd6305567c"
      }
    },
    "sources": {
      "ttyUSB0": {
        "label": "ttyUSB0",
        "type": "NMEA0183",
        "GP": {
          "talker": "GP",
          "sentences": {
            "RMC": "2017-04-03T06:14:04.451Z"
          }
        },
        "II": {
          "talker": "II",
          "sentences": {
            "HDM": "2017-05-16T05:15:54.006Z"
          }
        }
      }
    }
  }

  return json.dumps(hello_message)     




@app.route('/signalk/v1/stream')
@cross_origin()
def signalk_api_vessels_self_navigation():

  hello_message = {
    "context": "vessels",
     "updates": [{
        "source": {
          "pgn": "128275",
          "device": "/dev/actisense",
          "timestamp": "2014-08-15-16:00:05.538",
          "src": "115"
        },
        "values": [
          {
            "path": "navigation.logTrip",
            "value": 43374
          },
          {
            "path": "navigation.log",
            "value": 17404540
          }]
       }
       ]
  }

  return json.dumps(hello_message)     



@app.route('/nmearemote_watch')
@cross_origin()
def nmearemote_watch():


  devicekey = request.args.get('devicekey', 'cd7ade4354448b169463652859657cd7')
  #deviceid = request.args.get('deviceid', '')
  #startepoch = request.args.get('startepoch', 0)
  #endepoch = request.args.get('endepoch', 0)

  interval = request.args.get('interval',"1min")
  #Instance = request.args.get('instance','0')
  #resolution = request.args.get('resolution',"")
  keys = request.args.get('id',"")

  response = None

  jsonresults=[]
  
  deviceid = getedeviceid(devicekey)

  log.info("freeboard_raw deviceid %s", deviceid)

  if deviceid == "":
    return "invalid deviceid"

  host = 'hilldale-670d9ee3.influxcloud.net' 
  port = 8086
  username = 'helmsmart'
  password = 'Salm0n16'
  database = 'pushsmart-cloud'


  serieskeys = keys.split(",")

  for idkey in serieskeys:
    log.info("nmearemote_watch  idkey %s", idkey)

    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)
    
    query, units = nmearemote_functions.idkey_query(deviceid, idkey, interval)

    log.info("nmearemote_watch query %s", query)

    if query == "":
      #jsonresult = {"id":idkey, "value":value, "unit":"rpm"}
      jsonresults.append({"id":idkey, "value":"", "unit":""})

    else:

      try:
          response= dbc.query(query)

      #except InfluxDBServerError as e:
      except InfluxDBClientError as e:
        log.info('nmearemote_watch: Exception Client Error in InfluxDB  %s:  ' % str(e))

        
      except:
          log.info('nmearemote_watch: Error in InfluxDB mydata append %s:', query)
          e = sys.exc_info()[0]
          log.info("nmearemote_watch: Error: %s" % e)
          return jsonify(result="error")

      if response is None:
          log.info('nmearemote_watch: InfluxDB Query has no data ')
          return jsonify(result="error")

        
      if not response:
          log.info('nmearemote_watch: InfluxDB Query has no data ')
          return jsonify(result="error")

      points = list(response.get_points())

      for point in points:

        log.info('nmearemote_watch: InfluxDB Query point %s', point)

        #idkey Engine.0.RPM
        #jsonresult = {"id":"Engine.0.RPM","value":1200,"unit":"rpm"}
        value = point['value']
        jsonresult = {"id":idkey, "value":value, "unit":units}

        log.info('nmearemote_watch: InfluxDB Query jsonresult %s', jsonresult)
        
        jsonresults.append(jsonresult)

        log.info('nmearemote_watch: InfluxDB Query jsonresults %s ', jsonresults)

  """
  jsonresults=[]
  
  jsonresult = {"id":"Engine.0.RPM","value":1200,"unit":"rpm"}
  jsonresults.append(jsonresult)

  jsonresult = {"id":"Engine.0.engineTemperature","value":185,"unit":"rpm"}
  jsonresults.append(jsonresult)

  jsonresult = {"id":"Engine.0.oilPressure","value":45,"unit":"psi"}
  jsonresults.append(jsonresult)

  jsonresult = {"id":"Engine.0.FuelRate","value":10.2,"unit":"gpm"}
  jsonresults.append(jsonresult)
  """
  

  return json.dumps(jsonresults, ensure_ascii=False).encode('utf8')


@app.route('/pushsmart')
@app.route('/freeboard_raw')
@cross_origin()
def freeboard_raw():

    #deviceapikey =apikey
    #Interval = "1min"
     
    devicekey = request.args.get('devicekey', 'cd7ade4354448b169463652859657cd7')
    #deviceid = request.args.get('deviceid', '')
    startepoch = request.args.get('startepoch', 0)
    endepoch = request.args.get('endepoch', 0)

    Interval = request.args.get('interval',"5 minutes")
    Instance = request.args.get('instance','0')
    resolution = request.args.get('resolution',"")
    psformat = request.args.get('format',"")

    
    """    
    starttime = 0

    if startepoch == 0:
      epochtimes = getepochtimes(Interval)
      startepoch = epochtimes[0]
      endepoch = epochtimes[1]
      if resolution == "":
        resolution = epochtimes[2]
    """        
    response = None



    deviceid = getedeviceid(devicekey)
    
    log.info("freeboard_raw deviceid %s", deviceid)

    if deviceid == "":
        #callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })
      return "invalid deviceid"



    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid) + '_psraw'


    database="PushSmart_TCP"

    #serieskeys=" deviceid='"
    #serieskeys= serieskeys + deviceid + "' AND "
    #serieskeys= serieskeys +  " sensor='tcp'  "


    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid 

    log.info("freeboard_raw Query InfluxDB-Cloud:%s", serieskeys)
    log.info("freeboard_raw Create InfluxDB %s", database)

    IFDBCToken = os.environ.get('InfluxDBCloudToken')
    IFDBCOrg = os.environ.get('InfluxDBCloudOrg')
    IFDBCBucket = os.environ.get('InfluxDBCloudBucket')
    IFDBCURL = os.environ.get('InfluxDBCloudURL')




    #dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)
    #client = InfluxDBClient3(host=IFDBCURL, token=IFDBCToken, org=IFDBCOrg)
    client = InfluxDBClient3(host=IFDBCURL, token=IFDBCToken, org=IFDBCOrg, database=IFDBCBucket)



    """      
    query = ('select  DISTINCT(raw) AS raw  from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by *, time({}s) LIMIT 1') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution) 
    """     
    """  
    SELECT *
    FROM "HS_AC1518EFEBF8_psraw"
    WHERE
    time >= now() - interval '1 hour'
    """  

      
    query = ('select  DISTINCT(psraw) AS psraw  from {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s) ') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution) 
 
    query = ('select *  from "{}" where  time > {}s and time < {}s  LIMIT 100').format( measurement, startepoch, endepoch)

    query = ('''select *  from "{}" where  time >= now() - interval '{}' LIMIT 250''').format(measurement, Interval)
    query = ('''select *  from "{}" where  time >= now() - interval '{}' order by time desc LIMIT 250''').format(measurement, Interval)


    #query = ('select *  from "{}" LIMIT 10').format( measurement)
    #query = 'SELECT * FROM PushSmart_TCP LIMIT 10'
    #query = 'SELECT * FROM "HS_AC1518EFEBF8_psraw" LIMIT 10'

    log.info("freeboard_raw Query %s", query)
    #return jsonify(result="OK")

    #query = "SELECT * from home WHERE time >= -90d"
    #table = client.query(query=query, language="influxql")

    try:
        response= client.query(query=query, language="sql")
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))


            
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', response)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        pass

    #close the connection
    client.close()
    
    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        #callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return ("no data available - interval = {}").format(Interval)


    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        #callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })
        return ("no data available - interval = {}").format(Interval)
      
    #return jsonify(result="OK")
    #log.info('freeboard:  InfluxDB-Cloud response  %s:', response)

    #values = response.select(['psraw'])
    values = response.column('psraw')
    #log.info("freeboard_raw Get InfluxDB psraw values %s", values)
    #log.info("freeboard_raw Get InfluxDB psraw json.dumps(values) %s", json.dumps(values))

    
    jsondata=[]


    if psformat == "csv":
      PGNValues= measurement + ',\r\n'
    else:
      PGNValues=""

    try:
    
      for series in values:
        #log.info("influxdb psraw..%s", series.as_py() )

        if psformat == "csv":
          PGNValues= PGNValues + '"' + series.as_py()  + '"' + ',\r\n'
        elif psformat == "psd":
          PGNValues= PGNValues + series.as_py() + '\\r\\n'
        elif psformat == "sgk":
          PGNValues= PGNValues + series.as_py() + '\\r\\n'
        else:
          PGNValues= PGNValues + series.as_py() + '\r\n'


      if psformat == "json":
        return jsonify(result="OK", PGNValues=PGNValues[0:5072], measurement=measurement, interval=Interval  )

      elif psformat == "csv":
        response = make_response(PGNValues[0:5072])
        response.headers['Content-Type'] = 'text/csv'
        response.headers["Content-Disposition"] = "attachment; filename=PushSmart_" + measurement + ".csv"
        return response
        
      elif psformat == "psd":
        schema = SCHEMA
        nmea_records = nmea.loads(PGNValues)
        mysortedrecords = sorted(nmea_records, key=lambda t:t[1])

        #log.info("freeboard_raw Get InfluxDB psraw nmea_records %s", dump_json(schema, mysortedrecords))
        return dump_json(schema, mysortedrecords)    

      elif psformat == "sgk":
        schema = SCHEMA
        nmea_records = nmea.loads(PGNValues)
        mysortedrecords = sorted(nmea_records, key=lambda t:t[1])
        #log.info("freeboard_raw Get InfluxDB psraw nmea_records %s", dump_json(schema, mysortedrecords))


        skdata = signalk.parseSIGK(deviceid, dump_json(schema, mysortedrecords))
        #log.info("freeboard_raw Get InfluxDB psraw sigk_records %s", skdata)
        return skdata
              
      else:    
        return PGNValues[0:5072]

    
      #return jsonify(results = PGNValues)

    except TypeError as e:
      #log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
      #log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
      #log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))          
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        #callback = request.args.get('callback')
        #return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })
        return 'error'

  
    #return jsonify(status='error', update=False )
    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })
    return 'error'


@app.route('/freeboard_chart_test')
@cross_origin()
def freeboard_chart_test():

  values=[]
  
  value = 1.1
  values.append({"thing": "SEASWITCH_ENETG2_A17",
      "created": "2016-11-25T19:56:20.796Z",
      "content": {"amps":1.0, "volts":value}})
  
  value = 2.3
  values.append({"thing": "SEASWITCH_ENETG2_A17",
      "created": "2016-11-25T19:56:20.796Z",
      "content": {"amps":1.0, "volts":value}})
  
  value = 3.4
  values.append({"thing": "SEASWITCH_ENETG2_A17",
      "created": "2016-11-25T19:56:20.796Z",
      "content": {"amps":1.0, "volts":value}})
  
  value = 2.8
  values.append({"thing": "SEASWITCH_ENETG2_A17",
      "created": "2016-11-25T19:56:20.796Z",
      "content": {"amps":1.0, "volts":value}})
  
  value = 3.8
  values.append({"thing": "SEASWITCH_ENETG2_A17",
      "created": "2016-11-25T19:56:20.796Z",
      "content": {"amps":1.0, "volts":value}})
  
  value = 1.6
  values.append({"thing": "SEASWITCH_ENETG2_A17",
      "created": "2016-11-25T19:56:20.796Z",
      "content": {"amps":1.0, "volts":value}})
  
  value = 1.1
  values.append({"thing": "SEASWITCH_ENETG2_A17",
      "created": "2016-11-25T19:56:20.796Z",
      "content": {"amps":1.0, "volts":value}})
  

  #log.info('freeboard: freeboard_chart_test returning data values %s:%s  ', value1, point['volts'])    
  #return jsonify(date_time=mydatetime, update=True, rpm=value1, eng_temp=value2, oil_pressure=value3, alternator=value4, boost=value5, fuel_rate=value6, fuel_level=value7, eng_hours=value8)
  callback = request.args.get('callback')
  #myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")
  #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'volts':value1, 'amps':value2, 'power':value3, 'energy':value4})
  #return '{0}({1})'.format(callback, {'values':values})
  #return '{0}({1})'.format(callback, values)
  #return jsonify({  "this": "succeeded", "by": "getting", "the": "dweets","with":values})
  #return jsonify({"values":[{"volt":1},{"volt":2},{"volt":3},{"volt":4},{"volt":5},{"volt":6}]})
  return jsonify({  "values":values})



@app.route('/freeboard_ac_status_array')
@cross_origin()
def freeboard_ac_status_array():

    deviceapikey = request.args.get('apikey','')
    serieskey = request.args.get('datakey','')
    Interval = request.args.get('Interval',"1hour")
    Instance = request.args.get('instance','0')
    actype = request.args.get('type','GEN')
    mytimezone = request.args.get('timezone',"UTC")

    
    response = None
    
    starttime = 0

    epochtimes = getepochtimes(Interval)
    startepoch = epochtimes[0]
    endepoch = epochtimes[1]
    resolution = epochtimes[2]
    resolution = 60

    deviceid = getedeviceid(deviceapikey)
    
    log.info("freeboard deviceid %s", deviceid)

    if deviceid == "":
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'deviceid error' })


    host = 'hilldale-670d9ee3.influxcloud.net' 
    port = 8086
    username = 'helmsmart'
    password = 'Salm0n16'
    database = 'pushsmart-cloud'

    measurement = "HelmSmart"
    measurement = 'HS_' + str(deviceid)




    serieskeys=" deviceid='"
    serieskeys= serieskeys + deviceid + "' AND "
    #serieskeys= serieskeys +  " (sensor='engine_parameters_rapid_update' OR sensor='engine_parameters_dynamic'  OR  sensor='fluid_level') AND "
    serieskeys= serieskeys +  " (sensor='ac_basic' OR sensor='ac_watthours'  ) "
    serieskeys= serieskeys +  "  AND type = '" + actype + "' AND "
    serieskeys= serieskeys +  " (instance='" + Instance + "') "





    log.info("freeboard Query InfluxDB-Cloud:%s", serieskeys)
    log.info("freeboard Create InfluxDB %s", database)


    dbc = InfluxDBCloud(host, port, username, password, database,  ssl=True)

      
    query = ('select  mean(ac_line_neutral_volts) AS volts, mean(ac_amps) AS  amps, mean(ac_watts) AS power, mean(ac_kwatthours) AS energy FROM {} '
                     'where {} AND time > {}s and time < {}s '
                     'group by time({}s)') \
                .format( measurement, serieskeys,
                        startepoch, endepoch,
                        resolution) 
 


    log.info("freeboard data Query %s", query)

    try:
        response= dbc.query(query)
        
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', query)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))

    except UnboundLocalError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))  

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))


    except InfluxDBServerError as e:
      log.info('freeboard_createInfluxDB: Exception Client Error in InfluxDB  %s:  ' % str(e))

      
    except:
        log.info('freeboard: Error in InfluxDB mydata append %s:', query)
        e = sys.exc_info()[0]
        log.info("freeboard: Error: %s" % e)
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })

    if response is None:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })

    if not response:
        log.info('freeboard: InfluxDB Query has no data ')
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'missing' })

    log.info('freeboard:  InfluxDB-Cloud response  %s:', response)

    keys = response.raw.get('series',[])
    #keys = result.keys()
    #log.info("freeboard Get InfluxDB series keys %s", keys)


    #callback = request.args.get('callback')
    #return '{0}({1})'.format(callback, {'update':'False', 'status':'success' })
     
    jsondata=[]
    #jsonkey=[]
    #strvaluekey = {'Series': SERIES_KEY, 'start': start,  'end': end, 'resolution': resolution}
    #jsonkey.append(strvaluekey)
    #print 'freeboard start processing data points:'
    
    #log.info("freeboard jsonkey..%s", jsonkey )
    try:
    
      strvalue = ""
      value1 = '---'
      value2 = '---'
      value3 = '---'
      value4 = '---'
      value5 = '---'
      value6 = '---'
      value7 = '---'
      value8 = '---'

      ac_points = []
      volts=[]
      amps=[]
      power=[]
      energy=[]
      
      points = list(response.get_points())

      log.info('freeboard:  InfluxDB-Cloud points%s:', points)

      for point in points:
        log.info('freeboard:  InfluxDB-Cloud point%s:', point)

        if point['time'] is not None:
            mydatetimestr = str(point['time'])
            ##log.info('freeboard_environmental:: mydatetimestr %s:  ' % mydatetimestr)
            
            # convert string to datetime opject
            mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%S%z')
            ##log.info('freeboard_environmental:: mydatetime %s:  ' % mydatetime)

            # set timezone of new datetime opbect
            mydatetimetz = mydatetime.replace(tzinfo=ZoneInfo(mytimezone))
            ##log.info('freeboard_environmental:: mydatetimetz %s:  ' % mydatetimetz)    

            ## This dosnt work for python 3.11 anymore
            ## throws an OverFlow error
            ##dtt = mydatetimetz.timetuple()
            ##ts = int(mktime(dtt)*1000)
            ## So we need to convert datetime directly to seconds and add in timezone offesets

            # get seconds offset for selected timezone
            tzoffset = mydatetimetz.utcoffset().total_seconds()
            ##log.info('freeboard_environmental:: tzoffset %s:  ' % tzoffset)           

            # adjust GMT time for slected timezone for display purposes
            ts = int((mydatetime.timestamp() + tzoffset) * 1000 )
            ##log.info('freeboard_environmental:: ts %s:  ' % ts)

          

        if point['volts'] is not None:
          value = convertfbunits( point['volts'], 40)
          volts.append({'epoch':ts, 'value':value})
        
        if point['amps'] is not None:
          value = convertfbunits( point['amps'], 40)
          amps.append({'epoch':ts, 'value':value})
        
        if point['power'] is not None:
          value = convertfbunits( point['power'], 40)
          power.append({'epoch':ts, 'value':value})
        
        if point['energy'] is not None:
          value = convertfbunits( point['energy'], 40)
          energy.append({'epoch':ts, 'value':value})






        


        
      #myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")
      #ac_points.append({'epoch':ts, 'date_time':myjsondate, 'update':'True', 'volts':value1, 'amps':value2, 'power':value3, 'energy':value4})
      #ac_points.append({'epoch':ts, 'date_time':myjsondate, 'update':'True', 'volts':value1, 'amps':value2, 'power':value3, 'energy':value4})
        
      #log.info('freeboard: freeboard_engine returning data values %s:%s  ', value1, point['volts'])    
      #return jsonify(date_time=mydatetime, update=True, rpm=value1, eng_temp=value2, oil_pressure=value3, alternator=value4, boost=value5, fuel_rate=value6, fuel_level=value7, eng_hours=value8)
      callback = request.args.get('callback')
      #myjsondate = mydatetime.strftime("%B %d, %Y %H:%M:%S")
      #return '{0}({1})'.format(callback, {'date_time':myjsondate, 'update':'True', 'volts':value1, 'amps':value2, 'power':value3, 'energy':value4})
      #return '{0}({1})'.format(callback, {'ac_points':ac_points})
      return '{0}({1})'.format(callback, {'volts':volts, 'amps':amps, 'power':power, 'energy':energy})
    
    except TypeError as e:
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Type Error in InfluxDB mydata append %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Key Error in InfluxDB mydata append %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Name Error in InfluxDB mydata append %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
        log.info('freeboard: Index Error in InfluxDB mydata append %s:  ' % str(e))  

    except ValueError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: Value Error in InfluxDB  %s:  ' % str(e))

    except AttributeError as e:
      #log.info('freeboard: Index error in InfluxDB mydata append %s:  ', response)
      log.info('freeboard_createInfluxDB: AttributeError in InfluxDB  %s:  ' % str(e))     

    except InfluxDBClientError as e:
      log.info('freeboard_createInfluxDB: Exception Error in InfluxDB  %s:  ' % str(e))     
    
    except:
        log.info('freeboard: Error in geting freeboard response %s:  ', strvalue)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting freeboard ststs %s:  ' % e)
        #return jsonify(update=False, status='missing' )
        callback = request.args.get('callback')
        return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })

  
    #return jsonify(status='error', update=False )
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, {'update':'False', 'status':'error' })


# ######################################################
# called from sqs_poller when it ques a set switch command via timmer task list
# #####################################################

@app.route('/setswitchapi')
@cross_origin()
def setswitchapi():
  deviceapikey = request.args.get('deviceapikey', "")
  deviceid = request.args.get('deviceid', "")
  switchid = request.args.get('switchid', "0")
  switchvalue = request.args.get('switchvalue', "3")
  instance = request.args.get('instance', "0")

  if deviceapikey != "":
    deviceid = getedeviceid(deviceapikey)

  elif deviceid == "":
    return jsonify(result="Error", switch=switchid)
    
  log.info("setswitchapi deviceid %s", deviceid)
  #log.info("sendswitchapi switchpgn %s", switchpgn)
  
  if deviceid == "":
    return jsonify(result="Error", switch=switchid)

  # Create an client object
  #cache = IronCache()
  switchitem=""
  """
  try:
    log.info("setswitchapi - IronCache  get key %s", "switch_"+str(instance))
    switchitem = cache.get(cache=deviceid, key="switch_"+str(instance))

  except NameError as e:
      log.info('setswitchapi - IronCache NameError %s:  ' % str(e))

    
  except:
    switchitem = ""
    log.info('setswitchapi - IronCache error  %s:  ', switchitem)
    e = sys.exc_info()[0]
    log.info('setswitchapi - IronCache error %s:  ' % e)
  """

  try:
    #switchitem = mc.get(deviceid + '_switch_'+str(instance))
    switchitem = mc.get(deviceid + '_switch')

    log.info('setswitchapi - MemCache   deviceid %s payload %s:  ', deviceid, switchitem)

  except NameError as e:
    log.info('setswitchapi - MemCache NameError %s:  ' % str(e))

    
  except:
    switchitem = ""
    log.info('setswitchapi - MemCache error  deviceid %s payload %s:  ', deviceid, switchitem)
    e = sys.exc_info()[0]
    log.info('setswitchapi - MemCache error %s:  ' % e)


  newswitchitem=[]      
  if switchitem != "" and switchitem != "" and switchitem is not None:
    log.info("setswitchapi - IronCache  key exists %s", switchitem)
    #jsondata = json.loads(switchitem)
    jsondata = switchitem
    for item in jsondata:
      newswitchitem.append(item)
    
  switchpgn = {'instance':instance, 'switchid':switchid, 'switchvalue':switchvalue}
  newswitchitem.append(switchpgn)
  log.info("setswitchapi - IronCache  new key  %s",json.dumps(newswitchitem))

   
  # Put an item
  #cache.put(cache="001EC0B415BF", key="switch", value="$PCDIN,01F20E,00000000,00,0055000000FFFFFF*23")
  #cache.put(cache="001EC0B415BF", key="switch", value=switchpgn )
  #switchpgn = {'instance':instance, 'switchid':switchid, 'switchvalue':switchvalue}
  log.info("Cache put switch key %s", newswitchitem)
  log.info("setswitchapi - Cache  put key %s", "switch_"+str(instance))
  #item=cache.put(cache=deviceid, key="switch_"+str(instance), value=newswitchitem )
  #log.info("IronCache response key %s", item)

  try:
    #mc.set(deviceid + "_switch_"+str(instance) , newswitchitem, time=600)
    mc.set(deviceid + "_switch" , newswitchitem, time=600)
    log.info('setswitchapi - MemCache  set deviceid %s payload %s:  ', deviceid, newswitchitem)

  except NameError as e:
    log.info('setswitchapi - MemCache set NameError %s:  ' % str(e))

    
  except:
    newswitchitem = ""
    log.info('setswitchapi - MemCache set error  deviceid %s payload %s:  ', deviceid, newswitchitem)
    e = sys.exc_info()[0]
    log.info('setswitchapi - MemCache set error %s:  ' % e)


  
  return jsonify(result="OK", switch=newswitchitem)


# ######################################################
# called from sqs_poller when it ques a set switch command via timmer task list
# #####################################################

@app.route('/setdimmerapi')
@cross_origin()
def setdimmerapi():
  deviceapikey = request.args.get('deviceapikey', "")
  deviceid = request.args.get('deviceid', "")
  dimmerid = request.args.get('dimmerid', "0")
  dimmervalue = request.args.get('dimmervalue', "3")
  dimmeroverride = request.args.get('dimmeroverride', "0")
  instance = request.args.get('instance', "0")


  if deviceapikey != "":
    deviceid = getedeviceid(deviceapikey)

  elif deviceid == "":
    return jsonify(result="Error", switch=dimmerid)
    
  log.info("setdimmerapi deviceid %s", deviceid)
  #log.info("sendswitchapi dimmerpgn %s", dimmerpgn)
  
  if deviceid == "":
    return jsonify(result="Error", switch=dimmerid)

  # Create an client object
  #cache = IronCache()
  dimmeritem=""


  try:
    dimmeritem = mc.get(deviceid + '_dimmer')

    log.info('setdimmerapi - MemCache   deviceid %s payload %s:  ', deviceid, dimmeritem)

  except NameError as e:
    log.info('setdimmerapi - MemCache NameError %s:  ' % str(e))

    
  except:
    dimmeritem = ""
    log.info('setdimmerapi - MemCache error  deviceid %s payload %s:  ', deviceid, dimmeritem)
    e = sys.exc_info()[0]
    log.info('setdimmerapi - MemCache error %s:  ' % e)


  # if we have old keys we need to delete redundent keys with same switch id's and values
  # since these will all be set at one time

  #create new dimmerpgn
  dimmerpgn = {'instance':instance, 'dimmerid':dimmerid, 'dimmervalue':dimmervalue, 'dimmeroverride':dimmeroverride}
  log.info("setdimmerapi - MemCache  new dimmerpgn %s", dimmerpgn)

  newdimmeritem=[]      
  if dimmeritem != "" and dimmeritem != None and dimmeritem is not None:
    log.info("setdimmerMemCache - MemCache  key exists %s", dimmeritem)
    #jsondata = json.loads(dimmeritem)
    jsondata = dimmeritem
    #log.info("setdimmerapi - IronCache  key exists %s", dimmeritem.value)
    #jsondata = json.loads(dimmeritem.value)
    for item in jsondata:
      #do not append old item if it matches the new one
      # need to checkif both old dimmerid and dimmerinstance match new one
      # If they match, dont add old one - we do this so we can update if we get a change in dimmeroverride value
      # Overrides (!=0) are always appended
      #if item != dimmerpgn:
      if (int(item['instance']) != int(dimmerpgn['instance'])) or (int(item['dimmerid']) != int(dimmerpgn['dimmerid'])) :
        
        # not all items have all keys so we need to rebuild them
        itemInstance = item.get('instance', '0')
        itemDimmerid = item.get('dimmerid', '0')
        itemDimmervalue = item.get('dimmervalue', '0')
        itemDimmeroverride = item.get('dimmeroverride', '0')
        
        newItem = {'instance':itemInstance, 'dimmerid':itemDimmerid, 'dimmervalue':itemDimmervalue, 'dimmeroverride':itemDimmeroverride}
        
        newdimmeritem.append(newItem)
        log.info("setdimmerMemCache - old  keys are different %s", newdimmeritem)

      # if instance and ID are equal but old override value is 2 (override enabled) and new value is 0 (NULL from Alert)
      # Keep override active
      elif (int(item['instance'])  == int(dimmerpgn['instance'])) and (int(item['dimmerid']) == int(dimmerpgn['dimmerid'])):
        #if we are disable override mode - new value =1 comes from web page api
        #
        # Not all ITEMs have a dimmeroverride so we need to check if one exists first
        # itemDimmeroverride =  item['dimmeroverride']
        itemDimmeroverride = item.get('dimmeroverride', '0')
        
        if int(dimmerpgn['dimmeroverride']) == 1 and int(itemDimmeroverride) >= 2:
          #dimmerpgn = {'instance':instance, 'dimmerid':dimmerid, 'dimmervalue':dimmervalue, 'dimmeroverride':'0'}
          dimmerpgn = {'instance':instance, 'dimmerid':dimmerid, 'dimmervalue':dimmervalue, 'dimmeroverride':'1'}
          log.info("setdimmerMemCache - old  keys are same with new override = 1 and old >=2 %s", dimmerpgn)
          
        #If wee are in override mode  - replace values with override  
        elif int(dimmerpgn['dimmeroverride'] )  == 0 and int(itemDimmeroverride) >= 2:
          dimmerpgn['dimmervalue'] = item['dimmervalue'] 
          dimmerpgn['dimmeroverride'] = itemDimmeroverride
          log.info("setdimmerMemCache - old  keys are same with new override =0 old >=2 %s", dimmerpgn)

          

          
  #dimmerpgn = {'instance':instance, 'dimmerid':dimmerid, 'dimmervalue':dimmervalue}
  #now add new dimmerpgn
  log.info("setdimmerMemCache - Cache  adding new key  %s",dimmerpgn)
  
  newdimmeritem.append(dimmerpgn)
  log.info("setdimmerMemCache - Cache  new keys  %s",json.dumps(newdimmeritem))

   

  log.info("setdimmerMemCache put dimmer device= %s keys = %s", deviceid, newdimmeritem)
  #log.info("setdimmerapi - IronCache  put key %s", "dimmer_"+str(instance))
  #log.info("setdimmerapi - IronCache  put key %s", "dimmer")
  #item=cache.put(cache=deviceid, key="dimmer", value=newdimmeritem )
  #log.info("IronCache response key %s", item)


  try:
    #log.info("setdimmerapi - IronCache  get key %s", "dimmer_"+str(instance))
    #dimmeritem = cache.get(cache=deviceid, key="dimmer_"+str(instance))
    #dimmeritem = cache.get(cache=deviceid, key="dimmer")
    mc.set(deviceid + '_dimmer' , newdimmeritem, time=600)

    log.info('setdimmerMemCache - MemCache  set deviceid %s payload %s:  ', deviceid, newdimmeritem)

  except NameError as e:
    log.info('setdimmerMemCache - MemCache set NameError %s:  ' % str(e))

    
  except:
    dimmeritem = ""
    log.info('setdimmerMemCache - MemCache set error  deviceid %s payload %s:  ', deviceid, newdimmeritem)
    e = sys.exc_info()[0]
    log.info('setdimmerMemCache - MemCache set error %s:  ' % e)

  
  return jsonify(result="OK", dimmer=newdimmeritem)




# ######################################################
# called from web page to directly set a dimmer value
# #####################################################
#Updates MemCache with new Dimmer records
def setdimmerMemCache(deviceid, new_instance, new_dimmerid, new_dimmeroverride, new_dimmervalue ):
    
  log.info("setdimmerMemCache deviceid:%s  instance:%s dimmerid:%s dimmeroverride:%s dimmervalue:%s ", deviceid, new_instance, new_dimmerid, new_dimmeroverride, new_dimmervalue )
  #log.info("sendswitchapi switchpgn %s", switchpgn)
  
  if deviceid == "":
    return jsonify(result="Error", dimmer=dimmerid)

  old_dimmeritem=""
  old_dimmerOVRDitem=""
  
  try:
    #log.info("setdimmerapi - IronCache  get key %s", "dimmer_"+str(instance))
    #dimmeritem = cache.get(cache=deviceid, key="dimmer_"+str(instance))
    #dimmeritem = cache.get(cache=deviceid, key="dimmer")
    old_dimmeritem = mc.get(deviceid + '_dimmer' )

    log.info('setdimmerMemCache - MemCache  get old key deviceid %s payload %s:  ', deviceid, old_dimmeritem)

  except NameError as e:
    log.info('setdimmerMemCache - MemCache  get NameError %s:  ' % str(e))

    
  except:
    old_dimmeritem = ""
    log.info('setdimmerMemCache - MemCache   get error  deviceid %s payload %s:  ', deviceid, old_dimmeritem)
    e = sys.exc_info()[0]
    log.info('setdimmerMemCache - MemCache  get error %s:  ' % e)

  # see if there is an override key
  try:
    old_dimmerOVRDitem = mc.get(deviceid + '_dimmerOVRD' )

    log.info('setdimmerMemCache - MemCache  get old key deviceid %s OVRD payload %s:  ', deviceid, old_dimmerOVRDitem)

    if old_dimmerOVRDitem != "" and old_dimmerOVRDitem != None and old_dimmerOVRDitem is not None:
      old_itemOVRDInstance = old_dimmerOVRDitem.get('instance', '255')
      old_itemOVRDDimmerid = old_dimmerOVRDitem.get('dimmerid', '255')
      old_itemOVRDDimmervalue = old_dimmerOVRDitem.get('dimmervalue', '255')
      old_itemOVRDDimmeroverride = old_dimmerOVRDitem.get('dimmeroverride', '255')
      
    else:
      old_itemOVRDInstance = 255
      old_itemOVRDDimmerid = 255
      old_itemOVRDDimmervalue = 255
      old_itemOVRDDimmeroverride = 255  

    log.info("setdimmerMemCache - MemCache  old OVRD dimmerpgn %s: %s: %s : %s", old_itemOVRDInstance, old_itemOVRDDimmerid, old_itemOVRDDimmervalue, old_itemOVRDDimmeroverride)

  except NameError as e:
    log.info('setdimmerMemCache - MemCache  OVRD get NameError %s:  ' % str(e))

    
  except:
    old_dimmerOVRDitem = ""
    log.info('setdimmerMemCache - MemCache   get error  deviceid %s OVRD payload %s:  ', deviceid, old_dimmerOVRDitem)
    e = sys.exc_info()[0]
    log.info('setdimmerMemCache - MemCache  get error %s:  ' % e)

  # Create an client object
  #cache = IronCache()


  # Get existing keys that match instance
  # will include all switchid's in single instance and possible commands for each dimmer id
  # if unit is off-line these will stach up into long list of commands
  """  
  try:
    #log.info("setdimmerapi - IronCache  get key %s", "dimmer_"+str(instance))
    #dimmeritem = cache.get(cache=deviceid, key="dimmer_"+str(instance))
    dimmeritem = cache.get(cache=deviceid, key="dimmer")

  except NameError, e:
      log.info('setdimmerapi - IronCache NameError %s:  ' % str(e))

    
  except:
    dimmeritem = ""
    log.info('setdimmerapi - IronCache error  %s:  ', dimmeritem)
    e = sys.exc_info()[0]
    log.info('setdimmerapi - IronCache error %s:  ' % e)
  """

  
  # if we have old keys we need to delete redundent keys with same switch id's and values
  # since these will all be set at one time

  #create new dimmerpgn
  new_dimmerpgn = {'instance':new_instance, 'dimmerid':new_dimmerid, 'dimmervalue':new_dimmervalue, 'dimmeroverride':new_dimmeroverride}
  log.info("setdimmerMemCache - MemCache  new dimmerpgn %s", new_dimmerpgn)


  #create new OVERRIDE dimmerpgn
  if int(new_dimmeroverride) == 2:
    new_OVRDdimmerpgn = {'instance':new_instance, 'dimmerid':new_dimmerid, 'dimmervalue':new_dimmervalue, 'dimmeroverride':new_dimmeroverride}
    log.info("setdimmerMemCache - MemCache  new dimmerpgn %s", new_OVRDdimmerpgn)
    
  else:
    new_OVRDdimmerpgn = {}


  
  newdimmeritem=[]

  # check if there was a valid old/existig key
  if old_dimmeritem != "" and old_dimmeritem != None and old_dimmeritem is not None:
    log.info("setdimmerMemCache - MemCache  old key exists %s", old_dimmeritem)
    #jsondata = json.loads(dimmeritem)
    jsondata = old_dimmeritem
    #log.info("setdimmerapi - IronCache  key exists %s", dimmeritem.value)
    #jsondata = json.loads(dimmeritem.value)
    for old_item in jsondata:
      # not all items have all keys so we need to rebuild them
      old_itemInstance = old_item.get('instance', '0')
      old_itemDimmerid = old_item.get('dimmerid', '0')
      old_itemDimmervalue = old_item.get('dimmervalue', '0')
      old_itemDimmeroverride = old_item.get('dimmeroverride', '0')
      
      # do not append old item if it matches the new one
      # need to checkif both old dimmerid and dimmerinstance match new one
      # If they match, dont add old one - we do this so we can update if we get a change in dimmeroverride value
      # Overrides (!=0) are always appended
      if ((int(old_itemInstance) != int(new_instance)) or (int(old_itemDimmerid) != int(new_dimmerid))) :
        
        #keys dont match so add back in the old key
        oldItem = {'instance':old_itemInstance, 'dimmerid':old_itemDimmerid, 'dimmervalue':old_itemDimmervalue, 'dimmeroverride':old_itemDimmeroverride}

        # add copy of old key to set of new keys because they dont match the new ones
        newdimmeritem.append(oldItem)
        log.info("setdimmerMemCache - old  keys are different %s", newdimmeritem)

  # no old keys in memcache
  else:
    log.info("setdimmerMemCache - MemCache is empty")

  # if new override is false ( ==1) - we wont do anything with new values
  if int(new_dimmeroverride) == 1:
    #clear out the new key so we dont set it later
    new_dimmerpgn.clear()
    log.info("setdimmerMemCache -clearing out new key  %s",new_dimmerpgn)


  #create new OVERRIDE dimmerpgn if instance and id matches and override == 2
  if (int(old_itemOVRDDimmeroverride) == 2) and (int(old_itemOVRDInstance)  == int(new_instance)) and (int(old_itemOVRDDimmerid) == int(new_dimmerid)):
    #construct a new dimmerpgn using override values
    new_dimmerpgn = {'instance':int(new_instance), 'dimmerid':int(new_dimmerid), 'dimmervalue':int(old_itemOVRDDimmervalue), 'dimmeroverride':'2'}
    log.info("setdimmerMemCache - old  keys are same with old override = 2  %s", new_dimmerpgn)
    

  #now add new dimmerpgn which may have been modified by a old override key
  log.info("setdimmerMemCache - Cache  adding new key  %s",new_dimmerpgn)

  # append new dimmerpgn to list of old ones from memcache if they exist
  if len(new_dimmerpgn) !=0:
    newdimmeritem.append(new_dimmerpgn)
    log.info("setdimmerMemCache - Cache  new keys  %s",json.dumps(newdimmeritem))


  log.info("setdimmerMemCache put dimmer device= %s keys = %s", deviceid, newdimmeritem)

  # now set all values back to memcache so they be used later when gateway posts new data
  try:
    
    if len(newdimmeritem) != 0:
      mc.set(deviceid + '_dimmer' , newdimmeritem, time=600)
      log.info('setdimmerMemCache - MemCache  set deviceid %s len %s payload %s:  ', deviceid, len(newdimmeritem), newdimmeritem)

    # we set any overrides to a seperate key that expires on its own after 10 minutes
    if len(new_OVRDdimmerpgn) !=0:
      mc.set(deviceid + '_dimmerOVRD' , new_OVRDdimmerpgn, time=600)
      log.info('setdimmerMemCache - MemCache  set OVRD deviceid %s len %s payload %s:  ', deviceid, len(new_OVRDdimmerpgn), new_OVRDdimmerpgn)

      
  except NameError as e:
    log.info('setdimmerMemCache - MemCache set NameError %s:  ' % str(e))

    
  except:
    dimmeritem = ""
    log.info('setdimmerMemCache - MemCache set error  deviceid %s payload %s:  ', deviceid, newdimmeritem)
    e = sys.exc_info()[0]
    log.info('setdimmerMemCache - MemCache set error %s:  ' % e)

  
  return newdimmeritem






@app.route('/setdimmerbankapi')
def setdimmerbankapi():
  deviceid = request.args.get('deviceid', '000000000000')
  dimmerid = request.args.get('dimmerid', "0")
  dimmeroverride = request.args.get('dimmeroverrides', "0")
  dimmervalue = request.args.get('dimmervalues', "255")
  #instance = request.args.get('instance', "0")
  newdimmeritem = {}
  
  log.info("setdimmerbankapi deviceid %s", deviceid)

  dimmervalues = dimmervalue.split(',')
  log.info("setdimmerbankapi dimmervalues %s", dimmervalues)
  dimmeroverrides = dimmeroverride.split(',')
  log.info("setdimmerbankapi dimmeroverrides %s", dimmeroverrides)

  valuesLen = len(dimmervalues)
  log.info("setdimmerbankapi valuesLen %s", valuesLen)

  if int(dimmervalues[0]) < 101:
      log.info("setdimmerbankapi MASTER setdimmerMemCache %s, %s, %s, %s, %s", deviceid, 0, dimmerid, dimmeroverrides[0], dimmervalues[0] )
      newdimmeritem = setdimmerMemCache(deviceid, 0, dimmerid, dimmeroverrides[0], dimmervalues[0])

  else:

    for instance  in  range(0, 16):

      log.info("setdimmerbankapi setdimmerMemCache %s, %s, %s, %s, %s", deviceid, instance, dimmerid, dimmeroverrides[instance], dimmervalues[instance] )
      newdimmeritem = setdimmerMemCache(deviceid, instance, dimmerid, dimmeroverrides[instance], dimmervalues[instance])


  return jsonify(result="OK", dimmer=newdimmeritem)





  
# ######################################################
# called from sqs_poller when it ques a set timmer command via timmer task list
# #####################################################
@app.route('/settimmerapi')
def settimmerapi():
  deviceid = request.args.get('deviceid', '000000000000')
  timmertype = request.args.get('type', "")
  timmerparameter = request.args.get('parameter', "")
  timmervalues = request.args.get('array', "")
  instance = request.args.get('instance', "0")


  
    
  log.info("settimmerapi deviceid %s", deviceid)
  log.info("settimmerapi timmertype %s", timmertype)
  log.info("settimmerapi instance %s", instance)
  log.info("settimmerapi parameter %s", timmerparameter)

  # timmertype, timmerparameter, instance could all be empty strings which will cause problems

  if timmertype == "":
    return jsonify(result="Error", timmer=deviceid)

  if instance == "":
    return jsonify(result="Error", timmer=deviceid)

  if timmerparameter == "":
    return jsonify(result="Error", timmer=deviceid)

  if deviceid == "":
    return jsonify(result="Error", timmer=deviceid)

  # this creates an error if the value is empty string ""
  #timmerparameterindex =  int(filter(str.isdigit, str(timmerparameter)))
  timmerparameterindex = getIndexFromValue(timmerparameter)
  
  log.info("settimmerapi    timmerparameterindex %s", timmerparameterindex)
  #log.info("settimmerapi values %s", timmervalues)
  #log.info("sendswitchapi switchpgn %s", switchpgn)


  if str(timmertype) == "RGB 1 Channel":
    instance = timmerparameterindex
  elif str(timmertype) == "LED 4 Channel":
    instance = timmerparameterindex

  


  timmeritem=""
  try:
    #log.info("setdimmerapi - IronCache  get key %s", "dimmer_"+str(instance))
    #dimmeritem = cache.get(cache=deviceid, key="dimmer_"+str(instance))
    #dimmeritem = cache.get(cache=deviceid, key="dimmer")
   
    timmerid =str(deviceid) + '_timmer_' +  str(instance )
    log.info('settimmerapi - MemCache  get deviceid %s timmerid %s:  ', deviceid, timmerid)

    #timmeritem = mc.get(deviceid + '_timmer' )
    timmeritem = mc.get(timmerid)
    log.info('settimmerapi - MemCache  get deviceid %s payload %s:  ', deviceid, timmeritem)

  except NameError as e:
    log.info('settimmerapi - MemCache  get NameError %s:  ' % str(e))

    
  except:
    timmeritem = ""
    log.info('settimmerapi - MemCache   get error  deviceid %s payload %s:  ', deviceid, timmeritem)
    e = sys.exc_info()[0]
    log.info('settimmerapi - MemCache  get error %s:  ' % e)



  # Create an client object
  #cache = IronCache()


  # Get existing keys that match instance
  # will include all switchid's in single instance and possible commands for each dimmer id
  # if unit is off-line these will stach up into long list of commands
  """  
  try:
    #log.info("setdimmerapi - IronCache  get key %s", "dimmer_"+str(instance))
    #dimmeritem = cache.get(cache=deviceid, key="dimmer_"+str(instance))
    dimmeritem = cache.get(cache=deviceid, key="dimmer")

  except NameError, e:
      log.info('setdimmerapi - IronCache NameError %s:  ' % str(e))

    
  except:
    dimmeritem = ""
    log.info('setdimmerapi - IronCache error  %s:  ', dimmeritem)
    e = sys.exc_info()[0]
    log.info('setdimmerapi - IronCache error %s:  ' % e)
  """

  
  # if we have old keys we need to delete redundent keys with same switch id's and values
  # since these will all be set at one time

  #create new timmerpgn
  timmerpgn = {'instance':instance, 'timmerid':timmertype, 'timmerparameter':timmerparameter, 'timmervalues':timmervalues}
  
  newtimmeritem=[]      
  if timmeritem != "" and timmeritem != None and timmeritem is not None:
    log.info("settimmerapi - MemCache  key exists %s", timmeritem)
    #jsondata = json.loads(dimmeritem)
    jsondata = timmeritem
    #log.info("setdimmerapi - IronCache  key exists %s", dimmeritem.value)
    #jsondata = json.loads(dimmeritem.value)
    for item in jsondata:
      #do not append old item if it matches the new one
      if item != timmerpgn:
        newtimmeritem.append(item)
      

    
  #dimmerpgn = {'instance':instance, 'dimmerid':dimmerid, 'dimmervalue':dimmervalue}
  #now add new dimmerpgn
  newtimmeritem.append(timmerpgn)
  log.info("settimmerapi - Cache  new key  %s",json.dumps(newtimmeritem))

   

  log.info("settimmerapi put timmer device= %s key = %s", deviceid, newtimmeritem)
  #log.info("setdimmerapi - IronCache  put key %s", "dimmer_"+str(instance))
  #log.info("setdimmerapi - IronCache  put key %s", "dimmer")
  #item=cache.put(cache=deviceid, key="dimmer", value=newdimmeritem )
  #log.info("IronCache response key %s", item)


  try:
    #log.info("setdimmerapi - IronCache  get key %s", "dimmer_"+str(instance))
    #dimmeritem = cache.get(cache=deviceid, key="dimmer_"+str(instance))
    #dimmeritem = cache.get(cache=deviceid, key="dimmer")
    #mc.set(deviceid + '_timmer' , newtimmeritem, time=600)
    mc.set(timmerid, newtimmeritem, time=600)
   

    log.info('settimmerapi - MemCache  set deviceid %s payload %s:  ', deviceid, newtimmeritem)

  except NameError as e:
    log.info('settimmerapi - MemCache set NameError %s:  ' % str(e))

    
  except:
    timmeritem = ""
    log.info('settimmerapi - MemCache set error  deviceid %s payload %s:  ', deviceid, newtimmeritem)
    e = sys.exc_info()[0]
    log.info('settimmerapi - MemCache set error %s:  ' % e)

    
  return jsonify(result="OK", timmer=timmeritem)

def getdevicekeys(deviceapikey):

    conn = db_pool.getconn()

  
    query = "select deviceid, userid from user_devices where deviceapikey = %s"

    try:
    # first check db to see if deviceapikey is matched to device id

        cursor = conn.cursor()
        cursor.execute(query, (deviceapikey,))
        i = cursor.fetchone()
            
        # see we got any matches
        if cursor.rowcount == 0:
            # cursor.close
            db_pool.putconn(conn) 
            return ""
        
        else:
            deviceid = str(i[0])
            userid = str(i[1])
            db_pool.putconn(conn) 
            return deviceid, userid


    except TypeError as e:
        log.info('freeboard: TypeError in geting deviceid  %s:  ', deviceapikey)
        log.info('freeboard: TypeError in geting deviceid  %s:  ' % str(e))
            
    except KeyError as e:
        log.info('freeboard: KeyError in geting deviceid  %s:  ', deviceapikey)
        log.info('freeboard: KeyError in geting deviceid  %s:  ' % str(e))

    except NameError as e:
        log.info('freeboard: NameError in geting deviceid  %s:  ', deviceapikey)
        log.info('freeboard: NameError in geting deviceid  %s:  ' % str(e))
            
    except IndexError as e:
        log.info('freeboard: IndexError in geting deviceid  %s:  ', deviceapikey)
        log.info('freeboard: IndexError in geting deviceid  %s:  ' % str(e))  


    except:
        log.info('freeboard: Error in geting  deviceid %s:  ', deviceapikey)
        e = sys.exc_info()[0]
        log.info('freeboard: Error in geting deviceid  %s:  ' % str(e))

    # cursor.close
    db_pool.putconn(conn)                       

    return ""
     
