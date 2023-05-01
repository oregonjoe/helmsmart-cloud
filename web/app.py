import os
from os import environ
from os import environ as env, path
import pylibmc  
import sys
import json

#import md5
import hashlib
import base64

import requests
from requests.exceptions import HTTPError

import urllib
#from urlparse import urlparse
from urllib.parse import urlparse,urlencode, quote_plus
import psycopg


from influxdb.influxdb08 import InfluxDBClient

from influxdb import InfluxDBClient as InfluxDBCloud
from influxdb.client import InfluxDBClientError

import logging
# *******************************************************************
# Debug Output defines
# Comment to enable/disable
# ********************************************************************
#debug_all = False
debug_all = True

   

requests_log = logging.getLogger("requests")
#requests_log.setLevel(logging.WARNING)
#requests_log.setLevel(logging.INFO)
requests_log.setLevel(logging.DEBUG)
#logging.disable(logging.DEBUG)

#logging.basicConfig(level=logging.INFO)  
logging.basicConfig(level=logging.DEBUG)
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

#app.secret_key = 'super secret key'
app.secret_key = 'J0Zr27j/3yX L~SMP!jmN]CDI/,?RB'
app.config['SESSION_TYPE'] = 'filesystem'

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




# Application routes for web server


#@app.route("/")
#def hello_world():
#    return "<p>Hello, Joe World 4!</p>"



@app.route('/')
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
            myusername = mydata['name']
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
                #session['adminid'] = verificationdata['email']
            else:
                session['userid'] = hash_string('helmsmart@mockmyid.com')
                
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
          
    except:
      e = sys.exc_info()[0]
      log.info('dashboard.html: Error in geting user  %s:  ' % str(e))
      pass


    return render_template('dashboards_list.html', user=session['profile'], env=env) 

@app.route('/freeboard_getdashboardjson')
@cross_origin()
def freeboard_getdashboardjson():

  prefuid = request.args.get('prefuid',1)


  dashboardjson = getdashboardjson(prefuid)
  
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


    dashboardlists = getdashboardlists(userid)

    
    log.info("freeboard_GetDashboardJSON prefuid %s ", userid)
    log.info("freeboard_GetDashboardJSON dashboardlists %s ",  jsonify(dashboardlists))


    return jsonify({'preferences':dashboardlists})
  #  result = json.dumps(r, cls=DateEncoder)

  #response = make_response(dashboardlists)
  #response.headers['Cache-Control'] = 'public, max-age=0'
  #response.headers['content-type'] = "application/json"
  #return response




@app.route('/help')
@cross_origin()
def help():

    response = make_response(render_template('index.html', features = []))
    #response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response



### dashboard functions ####
    
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


  #except psycopg2.ProgrammingError as e:
  #  log.info('freeboard_addnewdashboard: ProgrammingError in  update pref %s:  ', userid)
  #  log.info('freeboard_addnewdashboard: ProgrammingError in  update pref  %s:  ' % str(e))
  #  return jsonify(result="ProgrammingError error")
  
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
    return float("{0:.2f}".format(value * 1.0 ) )

  #//   case 17: //="17">Radians</option>
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
                oldtime = datetime.datetime.now() - datetime.timedelta(months=1)
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
          mydatetime = datetime.datetime.strptime(mydatetimestr, '%Y-%m-%dT%H:%M:%SZ')

          mydatetime_utctz = mydatetime.replace(tzinfo=timezone('UTC'))
          mydatetimetz = mydatetime_utctz.astimezone(timezone(mytimezone))

          #dtt = mydatetime.timetuple()       
          dtt = mydatetimetz.timetuple()
          ts = int(mktime(dtt)*1000)
          
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
      
    #except pyonep.exceptions.JsonRPCRequestException as ex:
    #    print('JsonRPCRequestException: {0}'.format(ex))
        
    #except pyonep.exceptions.JsonRPCResponseException as ex:
    #    print('JsonRPCResponseException: {0}'.format(ex))
        
    #except pyonep.exceptions.OnePlatformException as ex:
    #    print('OnePlatformException: {0}'.format(ex))
       
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


