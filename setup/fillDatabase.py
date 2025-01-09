# This file generated the database that I use for this website. It has two classes, PokemonFamily which stores
# each pokemon, and PokemonIndividual, which stores each pokemon variety as a separate entry.
# This uses the calculate.py file heavily to fill in the info.
# Must run this file from the testingandsetup directory.


from sqlalchemy import JSON, ForeignKey, create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from calculate import *

engine = create_engine('sqlite:///pokemon.db')
Base = declarative_base()


class PokemonFamily(Base):
    __tablename__ = 'pokemon_family'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    varieties = relationship("PokemonIndividual", back_populates="family")

class PokemonIndividual(Base):
    __tablename__ = 'pokemon_individual'
    id = Column(Integer, primary_key=True)
    family_id = Column(Integer, ForeignKey('pokemon_family.id'))
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    image = Column(String, default = "")
    type = Column(JSON)
    weaknesses = Column(JSON)

    family = relationship("PokemonFamily", back_populates="varieties")
    
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

namesFile = open('names.txt', 'r')

namesList = namesFile.readlines()

namesFile.close()


for pokemonName in namesList:
    pokemonName = pokemonName[:-1]
    fam = PokemonFamily(name = pokemonName)
    varietyList = getEverything(pokemonName)
    link = []
    for variety in varietyList:
        nextVariety = PokemonIndividual(
            name = variety.name,
            url = variety.url,
            image = variety.image,
            type = variety.type,
            weaknesses = variety.weaknesses
        )
        link.append(nextVariety)
    fam.varieties = link
    session.add(fam)
    print(f"added {pokemonName}")
    
session.commit()

