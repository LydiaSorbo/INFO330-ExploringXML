import sqlite3
import xml.etree.ElementTree as ET
import sys

try:
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
        height_m = float(pokemon.find('height/m').text)
        weight_kg = float(pokemon.find('weight/kg').text)
        abilities = [a.text for a in pokemon.findall('abilities/ability')]

        curr.execute('SELECT id FROM classification WHERE text = ?', (classification,))
        classification_id = curr.fetchone()
        if classification_id is None:
            curr.execute('INSERT INTO classification (text) VALUES (?)', (classification,))
            classification_id = curr.lastrowid
        else:
            classification_id = classification_id[0]

        curr.execute(
            "INSERT INTO pokemon (pokedex_number, name, classification_id, generation, hp, attack, defense, speed, "
            "sp_attack, sp_defense, height_m, weight_kg) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (pokedex_number, name, classification_id, generation, hp, attack, defense, speed, sp_attack,
             sp_defense, height_m, weight_kg))

        pokemon_id = curr.lastrowid

        for type_elem in pokemon.findall('type'):
            type_name = type_elem.text
            curr.execute('SELECT id FROM type WHERE name = ?', (type_name,))
            type_id = curr.fetchone()
            if type_id is None:
                curr.execute('INSERT INTO type (name) VALUES (?)', (type_name,))
                type_id = curr.lastrowid
            else:
                type_id = type_id[0]
            curr.execute('INSERT INTO pokemon_type (pokemon_id, type_id) VALUES (?, ?)', (pokemon_id, type_id))

        for ability_elem in pokemon.findall('abilities/ability'):
            ability_name = ability_elem.text
            curr.execute('SELECT id FROM ability WHERE name = ?', (ability_name,))
            ability_id = curr.fetchone()
            if ability_id is None:
                curr.execute('INSERT INTO ability (name) VALUES (?)', (ability_name,))
                ability_id = curr.lastrowid
            else:
                ability_id = ability_id[0]
            curr.execute('INSERT INTO pokemon_abilities (pokemon_id, ability_id) VALUES (?, ?)',
                        (pokemon_id, ability_id))

    conn.commit()
except sqlite3.Error as error:
    print("SQLite error:", error)
finally:
    conn.close()