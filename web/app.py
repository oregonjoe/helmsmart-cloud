import os
from os import environ
import sys
import json
import urllib
#from urlparse import urlparse
from urllib.parse import urlparse
import psycopg  

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
db_pool = ConnectionPool(os.environ.get('DATABASE_URL'))

#app = Flask(__name__)


app = Flask(__name__)
CORS(app) 
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['DEBUG'] = True
app.debug = True


#Adding auth0
from auth0.v3.authentication import GetToken
from auth0.v3.authentication import Users

AUTH0_CALLBACK_URL = environ.get('AUTH0_CALLBACK_URL')
AUTH0_CLIENT_ID = environ.get('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = environ.get('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = environ.get('AUTH0_DOMAIN')



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







@app.route("/")
def hello_world():
    return "<p>Hello, Joe World 4!</p>"

#app.run(debug=True)
