from flask import Flask, jsonify, redirect, request, render_template, url_for
from calculate import *

app = Flask(__name__)

f = open('names.txt', 'r')
allPokemonNames = [line.strip() for line in f]
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pokemonName = request.form['homeSearch']
        if not pokemonName:
            return redirect(url_for('error', pokemonName = "null"))
        return redirect(url_for('result', pokemonName = pokemonName))
    return render_template('index.html', isIndex = True)

@app.route('/result/<pokemonName>', methods = ['GET', 'POST'])
def result(pokemonName):
    varietyList = getEverything(pokemonName)
    if not varietyList:
        return redirect(url_for('error', pokemonName = pokemonName))
    if request.method == 'POST':
        return redirect(url_for('result', pokemonName = request.form['navSearch']))
    return render_template('result.html', pokemonName = pokemonName, varietyList = varietyList, index = 0)

@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        return redirect(url_for('result', pokemonName = request.form['navSearch']))
    return render_template("about.html")

@app.route('/error/<pokemonName>', methods=['GET', 'POST'])
def error(pokemonName):
    if request.method == 'POST':
        return redirect(url_for('result', pokemonName = request.form['navSearch']))
    return render_template('error.html')

@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('query', '').lower()
    matches = [name for name in allPokemonNames if name.lower().startswith(query)]
    return jsonify(matches[:5])


if __name__ == '__main__':
    app.run(debug=True)
