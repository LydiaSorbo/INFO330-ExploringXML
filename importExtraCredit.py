import sqlite3
import xml.etree.ElementTree as ET
import sys

conn = sqlite3.connect('pokemon.sqlite')
curr = conn.cursor()

tree = ET.parse(sys.argv[1])
root = tree.getroot()

for pokemon in root.findall('pokemon'):
    pokedex_number = int(pokemon.get('pokedexNumber'))
    name = pokemon.find('name').text
    classification = pokemon.get('classification')
    generation = pokemon.get('generation')
    types = [t.text for t in pokemon.findall('type')]
    hp = int(pokemon.find('hp').text)
    attack = int(pokemon.find('attack').text)
    defense = int(pokemon.find('defense').text)
    speed = int(pokemon.find('speed').text)
    sp_attack = int(pokemon.find('sp_attack').text)
    sp_defense = int(pokemon.find('sp_defense').text)
    height = float(pokemon.find('height/m').text)
    weight = float(pokemon.find('weight/kg').text)
    abilities = [a.text for a in pokemon.findall('abilities/ability')]

    curr.execute("INSERT INTO pokemon (pokedex_number, name, classification, generation, hp, attack, defense, speed, "
                 "sp_attack, sp_defense, height, weight) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                 (pokedex_number, name, classification, generation, hp, attack, defense, speed, sp_attack,
                  sp_defense, height, weight))

    pokemon_id = curr.lastrowid

    for t in types:
        curr.execute("INSERT INTO pokemon_types (pokemon_id, type) VALUES (?, ?)", (pokemon_id, t))

    for a in abilities:
        curr.execute("INSERT INTO pokemon_abilities (pokemon_id, ability) VALUES (?, ?)", (pokemon_id, a))

conn.commit()
conn.close()