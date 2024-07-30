from flask import Flask, render_template, url_for, request, redirect
import requests
import os
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST, start_http_server
import threading

app = Flask(__name__)
Bootstrap(app)
fa = FontAwesome(app)

# Define a counter metric
REQUEST_COUNT = Counter('app_requests_total', 'Total number of requests')

@app.route('/')
def index():
    REQUEST_COUNT.inc()
    pokemon = [" ".join(i["name"].split("-")).title() for i in requests.get('https://pokeapi.co/api/v2/pokemon/?limit=-1').json()["results"]]
    return render_template('index.html', pokemon=pokemon)

@app.route('/<pokemon>')
def pokemon(pokemon):
    REQUEST_COUNT.inc()
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
    REQUEST_COUNT.inc()
    try:
        pokemon = request.form['pokemon']
        pk = "-".join(pokemon.split(" ")).lower()
        return redirect(url_for('pokemon', pokemon=pk))
    except:
        return redirect(url_for('index'))

def start_metrics_server():
    try:
        start_http_server(8000)
    except OSError as e:
        if e.errno == 98:
            print("Port 8000 is already in use")
        else:
            raise

if __name__ == '__main__':
    # Start metrics server in a new thread
    threading.Thread(target=start_metrics_server).start()
    # Start the Flask app server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
