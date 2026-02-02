import os
from os import environ
from os import environ as env, path
#import pylibmc
import bmemcached
import sys
import re
#import pyarrow as pa
import json
from threading import Thread

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

import logging
# *******************************************************************
# Debug Output defines
# Comment to enable/disable
# ********************************************************************
#debug_all = False
debug_all = True
debug_info = True
debug_memcachier = False



logging.basicConfig(level=logging.DEBUG)
log = logging

from psycopg_pool import ConnectionPool
db_pool = ConnectionPool(os.environ.get('DATABASE_URL'))

from flask_cognito_lib import CognitoAuth
from flask_cognito_lib.decorators import (
    auth_required,
    cognito_login,
    cognito_login_callback,
    cognito_logout,
)


from flask_awscognito import AWSCognitoAuthentication

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

#import dashboard_routes
import botocore
import boto3
from botocore.exceptions import ClientError
