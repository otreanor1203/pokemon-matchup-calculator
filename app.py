from flask import Flask, redirect, request, render_template, jsonify, url_for
from calculate import *

app = Flask(__name__)

pokemonName = ""
varietyList = []

@app.route('/result/<pokemonName>', methods = ['GET', 'POST'])
def result(pokemonName):
        return render_template('result.html', styleSheet = "resultStyles.css", varietyList = varietyList, index = 0)

@app.route('/', methods=['GET', 'POST'])
def index():
    global pokemonName, varietyList
    if request.method == 'POST':
        pokemonName = request.form['pokemonName']
        varietyList = getEverything(pokemonName)
        if varietyList:
            return redirect(url_for('result', pokemonName = pokemonName))
        else:
            return render_template('index.html', styleSheet = "indexStyles.css", error="Pokemon not found!")
    return render_template('index.html', styleSheet = "indexStyles.css")

# NEXT TASK -- MAKE AN ERROR PAGE OR SESSION

@app.route('/about', methods=['GET'])
def about():
    return render_template("about.html", styleSheet = "aboutStyles.css")


if __name__ == '__main__':
    app.run(debug=True)
