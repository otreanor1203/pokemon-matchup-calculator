from flask import Flask, redirect, request, render_template, jsonify, url_for
from calculate import *

app = Flask(__name__)

onResult = False
pokemon_name = ""
variety_list = []
variety = 0
fromPost = False

# typeImages = {
#         'normal': 'normal.png',
#         'fire': 'fire.png',
#         'water': 'water.png',
#         'electric': 'electric.png',
#         'grass': 'grass.png',
#         'ice': 'ice.png',
#         'fighting': 'fighting.png',
#         'poison': 'poison.png',
#         'ground': 'ground.png',
#         'flying': 'flying.png',
#         'psychic': 'psychic.png',
#         'bug': 'bug.png',
#         'rock': 'rock.png',
#         'ghost': 'ghost.png',
#         'dragon': 'dragon.png',
#         'dark': 'dark.png',
#         'steel': 'steel.png',
#         'fairy': 'fairy.png'
# }

@app.route('/result/<pokemon_name>', methods = ['GET', 'POST'])
def result(pokemon_name):
    global fromPost
    if fromPost:
        fromPost = False
        return render_template('result.html', varietyList = variety_list, index = 0)
    else:
        return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    global onResult, pokemon_name, variety_list, variety, fromPost
    if request.method == 'POST':
        if not onResult:
            onResult = True
            pokemon_name = request.form['pokemon_name']
            variety_list = getEverything(pokemon_name)
            if variety_list:
                fromPost = True
                return redirect(url_for('result', pokemon_name = pokemon_name))
            else:
                onResult = False
                return render_template('index.html', error="Pokemon not found!")

    onResult = False        
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
