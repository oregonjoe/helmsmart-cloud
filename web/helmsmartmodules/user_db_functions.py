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
