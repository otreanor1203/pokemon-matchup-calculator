

# user_pokemon = input("Enter a pokemon: ")

# user_type = getType(user_pokemon)

# if user_type:
#     weakness = getWeaknesses(user_type)
#     printEffectiveness(weakness)


















from flask import Flask, request, render_template
from calculate import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pokemon_name = request.form['pokemon_name']
        pokemon_data = getPokemonData(pokemon_name)
        if pokemon_data:
            user_type = getType(pokemon_data)
            weakness = getWeaknesses(user_type)
            effectiveness = printEffectiveness(weakness)
            return render_template('result.html', effectiveness=effectiveness)
        else:
            return render_template('index.html', error="Pokemon not found!")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
