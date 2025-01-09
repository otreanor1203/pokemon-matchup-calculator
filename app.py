from flask import Flask, jsonify, redirect, request, render_template, url_for, session
import pickle
from flask_sqlalchemy import SQLAlchemy
from setup.calculate import *

app = Flask(__name__)
app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokemon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Class to manage the pokemon family database, which stores each pokemon's info
class PokemonFamily(db.Model):
    __tablename__ = 'pokemon_family'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    varieties = db.relationship("PokemonIndividual", back_populates="family")

# Class to manage each pokemon variety as its own entry
class PokemonIndividual(db.Model):
    __tablename__ = 'pokemon_individual'
    id = db.Column(db.Integer, primary_key=True)
    family_id = db.Column(db.Integer, db.ForeignKey('pokemon_family.id'))
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), default = "")
    type = db.Column(db.JSON)
    weaknesses = db.Column(db.JSON)

    family = db.relationship("PokemonFamily", back_populates="varieties")


# Home page. Checks to see if a pokemon was entered and then redirects to the result page.
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pokemonName = request.form['homeSearch']
        if not pokemonName:
            return redirect(url_for('error', pokemonName = "null"))
        session["first"] = True
        return redirect(url_for('result', pokemonName = pokemonName))
    return render_template('index.html', isIndex = True)

# Result page. Checks the database to see if the pokemon that was entered is valid, and then gathers the info on the variety
# and puts each variety into a list. If the pokemon does not exist then it redirects into the error page, otherwise it displays the info.
# If this someone searches for another pokemon on this page, then it will redirect to itself with that pokemon.
# Session is used to store the pokemon name and current variety list
@app.route('/result/<pokemonName>', methods = ['GET', 'POST'])
def result(pokemonName):
    if request.method == 'POST':
        return redirect(url_for('result', pokemonName = request.form['navSearch']))
    pokemonName = pokemonName.capitalize()
    family = PokemonFamily.query.filter_by(name=pokemonName).first()
    if not family:
        return redirect(url_for('error', pokemonName = pokemonName))
    sqlVarieties = family.varieties
    varietyList = []
    for variety in sqlVarieties:
        varietyList.append(Pokemon(name = variety.name, url = variety.url, data = None, image = variety.image, type = variety.type, weaknesses = variety.weaknesses))
    if not varietyList:
        return redirect(url_for('error', pokemonName = pokemonName))
    session["currentPokemonName"] = pokemonName
    session["varietyList"] = pickle.dumps(varietyList)
    return render_template('result.html', pokemonName = pokemonName, varietyList = [variety.toDict() for variety in varietyList], index = 0)

# About page
@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        session["first"] = True
        return redirect(url_for('result', pokemonName = request.form['navSearch']))
    return render_template("about.html")

# Error page.
@app.route('/error/<pokemonName>', methods=['GET', 'POST'])
def error(pokemonName):
    if request.method == 'POST':
        session["first"] = True
        return redirect(url_for('result', pokemonName = request.form['navSearch']))
    return render_template('error.html')

# Route used when autocompleting a search. Grabs the query from JS and determines if any pokemon can autocomplete the
# search, and then sends over the first 5 pokemon name and image pairs.
@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('query', '').capitalize()
    matches = PokemonFamily.query.filter(PokemonFamily.name.like(f'{query}%')).limit(5).all()
    suggestions = []
    for match in matches:
        name = match.name
        firstVariety = match.varieties[0]
        image = firstVariety.image
        pair = [name, image]
        suggestions.append(pair)

    return jsonify(suggestions)


if __name__ == '__main__':
    app.run(debug=False)
