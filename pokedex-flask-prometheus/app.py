from flask import Flask, render_template, url_for, request, redirect
import requests
import os
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
import json
from prometheus_client import start_http_server, Summary, Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)
Bootstrap(app)
fa = FontAwesome(app)

# Definir métricas prometheus
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
##########

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
		return render_template('pokemon.html', stats=stats, types=types, sprites=sprites, name = name, weight = weight)
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

### AGREGAR METRICAS PARA SCRAPEAR APP
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
#######

port = int(os.environ.get('PORT', 5000)) 
if __name__ == '__main__':
	start_http_server(8000)  # Exponer métricas en el puerto 8000
	app.run(thre=True, port=port, debug=True)
