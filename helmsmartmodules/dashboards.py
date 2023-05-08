from __main__ import app

@app.route('/dashboard')
#@login_required
@cross_origin()
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

