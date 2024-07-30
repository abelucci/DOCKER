# app.py
from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST, start_http_server
import threading

app = Flask(__name__)

# Define a counter metric
REQUEST_COUNT = Counter('app_requests_total', 'Total number of requests')

@app.route('/')
def hello_world():
    REQUEST_COUNT.inc()
    return 'Hello, World!'

def start_metrics_server():
    start_http_server(8000)

if __name__ == '__main__':
    # Start metrics server in a new thread
    threading.Thread(target=start_metrics_server).start()
    # Start the Flask app server
    app.run(host='0.0.0.0', port=5000)

