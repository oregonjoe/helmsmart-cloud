import os
from os import environ
from os import environ as env, path
import pylibmc  
import sys


import json

#import md5
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

#from flask import render_template
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



from flask_cors import CORS, cross_origin

import logging
requests_log = logging.getLogger("requests")
#requests_log.setLevel(logging.WARNING)
#requests_log.setLevel(logging.INFO)
requests_log.setLevel(logging.DEBUG)
#logging.disable(logging.DEBUG)

#logging.basicConfig(level=logging.INFO)  
logging.basicConfig(level=logging.DEBUG)
log = logging




 
#@app.route('/dashboard')
#@cross_origin()
def dashboard():

    log.info("dashboard.html: START ****" )
    
    try:
      
      if session['profile'] is not None:
        
        try:
          mydata = session['profile']
          log.info("dashboard: customdata:%s", mydata)
          
        
          if mydata is not None:
            user_email = mydata['name']
            log.info("dashboard.html: user exists:%s", user_email)
           
        except:
          e = sys.exc_info()[0]
          log.info('dashboard.html: Error in geting user.custom_data  %s:  ' % str(e))
          return render_template('dashboards_list.html', user=session['profile'], env=env) 

        try:
          if user_email is not None:

            conn = db_pool.getconn()
            session['username'] = user_email
            
            log.info("dashboard.html: email:%s", user_email )

            query = "select userid from user_devices where useremail = %s group by userid"
            
            cursor = conn.cursor()
            cursor.execute(query, [user_email])
            i = cursor.fetchone()       
            if cursor.rowcount > 0:

                session['userid'] = str(i[0])
                #session['adminid'] = verificationdata['email']
            else:
                session['userid'] = hash_string('helmsmart@mockmyid.com')

            # cursor.close
            db_pool.putconn(conn)

            log.info("dashboard.html: userid:%s", session['userid'])

            response = make_response(render_template('dashboard.html', features = []))
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, post-check=0, pre-check=0, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '-1'
            return response
  
        except:
          e = sys.exc_info()[0]
          log.info('dashboard.html: Error in geting user_email  %s:  ' % str(e))
          pass


    except KeyError as e:
        log.info('freeboard_addnewdashboard: KeyError in  update pref  %s:  ', session['profile'])
        log.info('freeboard_addnewdashboard: KeyError in  update pref  %s:  ' % str(e))
    
    except:
      e = sys.exc_info()[0]
      log.info('dashboard.html: Error in geting user  %s:  ' % str(e))
      pass


    return render_template('dashboards_list.html', user=session['profile'], env=env) 

