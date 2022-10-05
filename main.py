from app import app
from decouple import config

if __name__ == '__main__':
    app.run(debug=True, host=config('host', default='0.0.0.0'), port=config('port', default=5000))
    # app.run(debug=True, host='192.168.1.154')