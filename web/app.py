import urllib
from urlparse import urlparse
import psycopg2  

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



from psycopg2.pool import ThreadedConnectionPool
db_pool = ThreadedConnectionPool(
  1, # min connections,
  int(os.environ.get('MAX_DB_CONNECTIONS',3)),
  **connection_from(os.environ['DATABASE_URL'])
)



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
