from flask import Flask, request, render_template, jsonify
from calculate import *

app = Flask(__name__)

onResult = False
pokemon_name = ""
variety_list = []
variety = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    global onResult, pokemon_name, variety_list, variety
    if request.method == 'POST':
        if not onResult:
            onResult = True
            pokemon_name = request.form['pokemon_name']
            variety_list = getEverything(pokemon_name)
            if variety_list:
                return render_template('result.html', list = variety_list, index = 0)
            else:
                return render_template('index.html', error="Pokemon not found!")
        else:
            variety = int(request.form['variety_select'])
            return render_template('result.html', list = variety_list, index = variety)

    onResult = False        
    return render_template('index.html')

@app.route('/api/options', methods=['GET'])
def get_options():
    pokemon_list = [{'value': i, 'name': pokemon.name} for i, pokemon in enumerate(variety_list)]
    return jsonify(pokemon_list)


if __name__ == '__main__':
    app.run(debug=True)
