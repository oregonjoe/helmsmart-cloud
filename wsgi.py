
#from app.main import app
from web.app import app
from web.app import socketio

#if __name__ == "__main__":
if __name__ == "__app__":
        #app.run()
        socketio.run(app)
