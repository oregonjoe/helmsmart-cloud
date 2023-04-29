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


#from psycopg.pool import ThreadedConnectionPool
from psycopg.pool import ConnectionPool
#db_pool = ThreadedConnectionPool( 1,  **connection_from(os.environ['DATABASE_URL']))
db_pool = ConnectionPool( 1,  **connection_from(os.environ['DATABASE_URL']))


#app = Flask(__name__)


app = Flask(__name__)
CORS(app) 
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['DEBUG'] = True
app.debug = True


@app.route("/")
def hello_world():
    return "<p>Hello, Joe World 2!</p>"

#app.run(debug=True)
