from flask import Flask, request, render_template, redirect, url_for, Response
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from prometheus_client import start_http_server, Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import os
import requests
import time
import logging
import multiprocessing

# Configuración de logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
Bootstrap(app)
fa = FontAwesome(app)

# Definir métricas
REQUEST_TIME = Histogram('flask_request_duration_seconds', 'Request duration', ['method', 'endpoint'])
REQUEST_COUNT = Counter('flask_request_count', 'Total number of requests', ['method', 'endpoint', 'status_code'])

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    request_latency = time.time() - request.start_time
    endpoint = request.endpoint if request.endpoint else 'unknown'
    REQUEST_TIME.labels(request.method, endpoint).observe(request_latency)
    REQUEST_COUNT.labels(request.method, endpoint, response.status_code).inc()
    return response

@app.route('/')
def index():
    pokemon = [" ".join(i["name"].split("-")).title() for i in requests.get(f'https://pokeapi.co/api/v2/pokemon/?limit=-1').json()["results"]]
    return render_template('index.html', pokemon=pokemon)

@app.route('/<pokemon>')
def pokemon(pokemon):
    try:
        req = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}').json()
        print(req["id"])
        stats = req['stats']
        types = req['types']
        sprites = [req['sprites'][i] for i in req['sprites']]
        name = " ".join(req['name'].split("-")).title()
        weight = req['weight']
        sprites[0], sprites[1], sprites[2], sprites[3], sprites[4], sprites[5], sprites[6], sprites[7] = sprites[4], sprites[0], sprites[5], sprites[1], sprites[6], sprites[2], sprites[7], sprites[3]
        sprites = [i if i != None else "" for i in sprites]
        return render_template('pokemon.html', stats=stats, types=types, sprites=sprites, name=name, weight=weight)
    except:
        return redirect(url_for('index'))

@app.route('/get_pokemon', methods=['POST'])
def get_pokemon():
    try:
        pokemon = request.form['pokemon']
        pk = "-".join(pokemon.split(" ")).lower()
        return redirect(url_for('pokemon', pokemon=pk))
    except:
        return redirect(url_for('index'))

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

def start_prometheus():
    logging.info('Attempting to start Prometheus metrics server on port 8000')
    try:
        start_http_server(8000)
        logging.info('Prometheus metrics server successfully started on port 8000')
    except Exception as e:
        logging.error(f'Failed to start Prometheus metrics server: {e}')

port = int(os.environ.get('PORT', 5000))
if __name__ == '__main__':
    # Iniciar el servidor de Prometheus en un proceso separado
    prometheus_process = multiprocessing.Process(target=start_prometheus)
    prometheus_process.start()
    logging.info('Prometheus process started')
    
    logging.info(f'Starting Flask app on port {port}')
    app.run(threaded=True, host='0.0.0.0', port=port)

    # Asegurarse de que el proceso de Prometheus se cierre correctamente al finalizar
    prometheus_process.join()
