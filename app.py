from flask import Flask, redirect, request, render_template, url_for
from calculate import *

app = Flask(__name__)
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('result', pokemonName = request.form['homeSearch']))
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


if __name__ == '__main__':
    app.run(debug=True)
