import os
from os import environ
from os import environ as env, path
import pylibmc  
import sys


import json

import logging



logging.basicConfig(level=logging.DEBUG)
log = logging

from psycopg_pool import ConnectionPool
db_pool = ConnectionPool(os.environ.get('DATABASE_URL'))

#import helmsmartmodules.user_db_functions

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


def getuserid(user_email):

    log.info("getuserid: email:%s", user_email )
    
    try:
      
        conn = db_pool.getconn()


        query = "select userid from user_devices where useremail = %s group by userid"
        
        cursor = conn.cursor()
        cursor.execute(query, [user_email])
        i = cursor.fetchone()       
        if cursor.rowcount > 0:

            userid = str(i[0])
            
        else:
            #session['userid'] = hash_string('helmsmart@mockmyid.com')
            userid = "0"
            
        # cursor.close
        db_pool.putconn(conn)

        log.info("getuserid: userid:%s", userid)

        return userid
  


    except KeyError as e:
        log.info('getuserid: KeyError in  getuserid   %s:  ', user_email)
        log.info('getuserid: KeyError in  getuserid   %s:  ' % str(e))
    
    except:
      e = sys.exc_info()[0]
      log.info('getuserid.html: Error in geting user  %s:  ' % str(e))
      pass


    return "0"



