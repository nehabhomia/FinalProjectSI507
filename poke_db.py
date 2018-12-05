#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 19:35:26 2018

@author: nehabhomia
"""

import sqlite3
import requests
from bs4 import BeautifulSoup
import json
import requests_cache
requests_cache.install_cache('pokemon_cache')

conn = sqlite3.connect('pokemon_database')
cur = conn.cursor()

#Creating 6 tables - Regions (Kanto, Johto, Hoenn)
#Pokemon (9 starter pokemon, 3 from each region)
#Types (the 3 starter types - plant, fire, water)
#TypeStrength
#Moves (id, move, attack/defense, type, score)
#Poke-Move (Id, pokemon id, move id)

# =============================================================================
# Dropping the tables
# =============================================================================

statement = '''
    DROP TABLE IF EXISTS 'Regions';
'''
cur.execute(statement)

statement = '''
    DROP TABLE IF EXISTS 'Pokemons';
'''
cur.execute(statement)

statement = '''
    DROP TABLE IF EXISTS 'Types';
'''
cur.execute(statement)

statement = '''
    DROP TABLE IF EXISTS 'TypeStrength';
'''
cur.execute(statement)

statement = '''
    DROP TABLE IF EXISTS 'Moves';
'''
cur.execute(statement)

statement = '''
    DROP TABLE IF EXISTS 'Poke-Move';
'''
cur.execute(statement)

# =============================================================================
# Creating the tables
# =============================================================================

#creating the table 'Regions', column names should be a primary key id and region name
statement = '''
    CREATE TABLE 'Regions' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Region' TEXT NOT NULL
    );
'''
cur.execute(statement)
conn.commit()

#creating the table 'Type', column names type id, type, strong against, weak against
statement = '''
    CREATE TABLE 'Types' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Type' TEXT NOT NULL
    );
'''
cur.execute(statement)
conn.commit()

#creating the table 'TypeStrength', column names id, type, strong against, weak against
statement = '''
    CREATE TABLE 'TypeStrength' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Type' TEXT NOT NULL,
        'StrongAgainst' INTEGER,
        'WeakAgainst' INTEGER
    );
'''
cur.execute(statement)
conn.commit()

#creating the table 'Pokemon', column names id, Pokemon name, region id, type id
statement = '''
    CREATE TABLE 'Pokemons' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Pokemon' TEXT NOT NULL,
        'TypeId' INTEGER,
        'RegionId' INTEGER NOT NULL
    );
'''
cur.execute(statement)
conn.commit()

#creating the table 'Moves', column names id, Move name, type id
statement = '''
    CREATE TABLE 'Moves' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'MoveName' TEXT NOT NULL,
        'TypeId' INTEGER,
        'Power' INTEGER
    );
'''
cur.execute(statement)
conn.commit()

#creating the table 'Poke-Move', column names id, Pokemon id, move id
statement = '''
    CREATE TABLE 'Poke-Move' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'PokemonId' INTEGER NOT NULL,
        'MoveId' INTEGER NOT NULL
    );
'''
cur.execute(statement)
conn.commit()

# =============================================================================
# Scraping the data
# =============================================================================

baseurl = 'http://pokemon.wikia.com'
names_list = []
urls_list = [] 
hoenn_names = []
hoenn_urls = []
name_regions = []

def get_regions_data():
    regions_extension = '/wiki/Category:Region_Starters'
    main_regions_page = requests.get(baseurl+regions_extension).text
    main_regions_soup = BeautifulSoup(main_regions_page, 'html.parser')   
    regions_section = main_regions_soup.find_all("li", {"class": "category-page__trending-page"})
    for region in regions_section:
        regions_url = region.find('a')['href'] #gets extensions for individual region's url
        regions_title = region.find("figcaption", {"class": "category-page__trending-page-title"}).text
        #gets the text of each section, but it includes "starter pokemon"
        regions_name = regions_title.split(' ')[0] #split string by space and display just first element i.e. the name
        name_regions.append(regions_name)
        if regions_name == 'Johto' or regions_name == 'Kanto': #these 2 regions have pokemons in tables
            regions_page = requests.get(baseurl+regions_url).text
            regions_soup = BeautifulSoup(regions_page, 'html.parser')
            pokemon_table = regions_soup.find("table", {"class":"article-table"})
            for pokemon in pokemon_table:
                if pokemon.find('a') != None and pokemon.find('a') != -1: #takes only columns with pokemon names and urls
                    regions_pokemon = pokemon.find('a')['title']
                    names_list.append(regions_pokemon)
                    pokemon_url = pokemon.find('a')['href']
                    urls_list.append(pokemon_url)
                else: #other columns of no use to us
                    pass
        elif regions_name == 'Hoenn':
            regions_page = requests.get(baseurl+regions_url).text
            regions_soup = BeautifulSoup(regions_page, 'html.parser')
            pokemon_para = regions_soup.find("div", {"id":"mw-content-text"}).find_all('p')[1]
            pokemon_names = pokemon_para.find_all('a')
            for pokemon in pokemon_names:
                hoenn_names.append(pokemon.text)
                hoenn_urls.append(pokemon['href'])
            hoenn_names.remove('Hoenn Region')
            hoenn_urls.remove('/wiki/Hoenn')
        else: #coding just for Hoenn region as per the proposal, rather than for all other regions.
            #all other regions have it in text paragraph
            #how to get regions from those?
            #first text for url is region, next three are pokemon names and urls, can ignore the ones after that.
#            pokemon_para = regions_soup.find("div", {"id":"mw-content-text"})
#            if pokemon_para.find('p').find('a') != None:
#                pokemon_names = pokemon_para.find('p').find_all('a')
#                names_list = []
#                for pokemon in pokemon_names:
#                    names_list.append(pokemon.text)
#                print (names_list[1], names_list[4], names_list[6])
            pass
        
        
get_regions_data()        
johto_names = names_list[:3]
johto_urls = urls_list[:3]
kanto_names = names_list[3:]
kanto_urls = urls_list[3:]
urls_list.extend(hoenn_urls)

types_list = []
def get_types():
    types_page = requests.get(baseurl+'/Types').text
    types_soup = BeautifulSoup(types_page, 'html.parser')
    if types_soup.find("table", {"class":"article-table"}).find_all("span", {"class":"t-type2"}) != None:
        all_types_list = types_soup.find("table", {"class":"article-table"}).find_all("span", {"class":"t-type2"})

    for row in all_types_list:
        types_list.append(row.text)

get_types()
#print(types_list)

pokemon_name_type_dict = {}
def get_pokemons_data():
    for url in urls_list:
        pokemon_page = requests.get(baseurl+url).text
        pokemon_soup = BeautifulSoup(pokemon_page, 'html.parser')
        pokemon_type = pokemon_soup.find("span", {"class":"t-type2"}).text
        pokemon_name = url.split('/')[-1]
        pokemon_name_type_dict[pokemon_name] = pokemon_type
get_pokemons_data()

move_names = []
def get_moves_data():
    moves_page = requests.get(baseurl+'/List_of_moves').text
    moves_soup = BeautifulSoup(moves_page, 'html.parser')
    moves_table = moves_soup.find("div", {"id":"mw-content-text"})
    tester = moves_table.find_all('td')
    for row in tester:
        if row.find('a') != None:
            name = row.find('a').text
            if len(name) != 1 and name != '':
                move_names.append(name)
get_moves_data()

base_url = 'https://pokeapi.co/api/v2/pokemon/'

def get_pokemon_moves():
    my_pokemons = [152, 155, 158, 1, 4, 7, 252, 255, 258]
    pokemon_moves = {}
    for pokemon in my_pokemons:
        pokemon_page = requests.get(base_url+str(pokemon)+'/').text
        pokemon_dict = json.loads(pokemon_page)
        pokemon_name = pokemon_dict['name']
        moves_list = []
        dict_moves_list = pokemon_dict['moves'][:10] #taking first 10 moves
        for move in dict_moves_list:
            move_name = move['move']['name']
            move_url = move['move']['url']
            move_page = requests.get(move_url).text
            move_dict = json.loads(move_page)
            move_type = move_dict["type"]["name"]
            move_power = move_dict["power"]
            if move_power == None:
                move_power = 0
            move_complete_dict = {"name": move_name, "type": move_type, "power": move_power}
            moves_list.append(move_complete_dict)
        pokemon_moves[pokemon_name] = moves_list
        moves_list = []
    return pokemon_moves

pokemon_move_dict = get_pokemon_moves()

# =============================================================================
# Populating the tables
# =============================================================================

#Populating 'Regions' Table
for name in name_regions:
    name = (name,)
    statement = "INSERT INTO \"Regions\" (Region) VALUES (?)"
    cur.execute(statement, name)
    conn.commit()

#Populating 'Pokemons' Table
for name in johto_names:
    Id = 2
    statement = "INSERT INTO \"Pokemons\" (Pokemon, RegionId) VALUES (?, ?)"
    cur.execute(statement, (name, Id))
    conn.commit()

for name in kanto_names:
    Id = 4
    statement = "INSERT INTO \"Pokemons\" (Pokemon, RegionId) VALUES (?, ?)"
    cur.execute(statement, (name, Id))
    conn.commit()

for name in hoenn_names:
    Id = 6
    statement = "INSERT INTO \"Pokemons\" (Pokemon, RegionId) VALUES (?, ?)"
    cur.execute(statement, (name, Id))
    conn.commit()

#Populating 'Types' Table
for poke_type in types_list:
    statement = "INSERT INTO \"Types\" (Type) VALUES (?)"
    poke_type = (poke_type,)
    cur.execute(statement, poke_type)
    conn.commit()
    
for key in pokemon_name_type_dict: #populate TypeId in Pokemons table
    type_name = pokemon_name_type_dict[key]
    statement = "SELECT Id FROM Types WHERE Type = ?"
    cur.execute(statement, (type_name,))
    type_id = cur.fetchone()
    conn.commit()
    #insert into table
    statement = "UPDATE \"Pokemons\" SET TypeId = ? WHERE Pokemon = ?"
    cur.execute(statement, (type_id[0], key,))
    conn.commit()

#Populating table 'TypeStrength'
pairs = [('Fire', 'Grass', 'Water'), ('Grass', 'Water', 'Fire'), ('Water', 'Fire', 'Grass')]
for pair in pairs:
    statement = "INSERT INTO \"TypeStrength\" (Type, StrongAgainst, WeakAgainst) VALUES (?, ?, ?)"
    cur.execute(statement, pair)
    conn.commit()
    
#Populating table 'Moves'
for pokemon in pokemon_move_dict:
    pokemon_moves_list = pokemon_move_dict[pokemon]
    for move in pokemon_moves_list:
        # first get id of type
        type_name = move["type"].capitalize()
        statement = "SELECT Id FROM Types WHERE Type = ?"
        cur.execute(statement, (type_name,))
        type_id = cur.fetchone()
        conn.commit()
        # insert into table
        move_name = move["name"]
        move_power = move["power"]
        statement = "INSERT INTO Moves (MoveName, TypeId, Power) VALUES (?,?,?)"
        cur.execute(statement, (move_name, type_id[0], move_power,))
        conn.commit()

conn.close()