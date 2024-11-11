from flask import Flask, jsonify, redirect, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from calculate import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokemon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class PokemonFamily(db.Model):
    __tablename__ = 'pokemon_family'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    varieties = db.relationship("PokemonIndividual", back_populates="family")

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


# f = open('names.txt', 'r')
# allPokemonNames = [line.strip() for line in f]
    
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
    query = request.args.get('query', '').capitalize()
    matches = PokemonFamily.query.filter(PokemonFamily.name.like(f'{query}%')).all()
    matches = matches[:5]
    suggestions = []
    for match in matches:
        name = match.name
        firstVariety = match.varieties[0]
        image = firstVariety.image
        pair = [name, image]
        suggestions.append(pair)

    return jsonify(suggestions)


if __name__ == '__main__':
    app.run(debug=True)
