import os
from os import environ
from os import environ as env, path
import pylibmc  
import sys
import json

import requests
from requests.exceptions import HTTPError

import urllib
#from urlparse import urlparse
from urllib.parse import urlparse,urlencode, quote_plus
import psycopg

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

@app.route('/freeboard_getdashboardlist')
@cross_origin()
def freeboard_getdashboardlist():

  userid = request.args.get('userid',1)


  dashboardlists = getdashboardlists(userid)
  
  log.info("freeboard_GetDashboardJSON prefuid %s -> %s", userid, dashboardlists)


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
            return jsonify( message='Could not get prefuids', status='error')
            db_pool.putconn(conn) 
            return ""
        
        else:
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



#app.run(debug=True)
