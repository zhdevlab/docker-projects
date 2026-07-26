import os
from flask import Flask
import redis


app = Flask(__name__)
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = int(os.getenv('REDIS_PORT', 6379))
r = redis.Redis(host=redis_host, port=redis_port)

# The welcome page
@app.route('/')
def welcome_page():
    return 'Welcome to my counter app!'

# The visitor count page
@app.route('/count')
def count():
    count = r.incr('visitor_count_hits')
    return f'You are Visitor number: {count}'

if  __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
