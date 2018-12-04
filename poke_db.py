#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 19:35:26 2018

@author: nehabhomia
"""

import sqlite3
import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect('pokemon_database')
cur = conn.cursor()

#Creating 5 tables - Regions (Kanto, Johto, Hoenn)
#Pokemon (9 starter pokemon, 3 from each region)
#Types (the 3 starter types - plant, fire, water)
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
    DROP TABLE IF EXISTS 'Pokemon';
'''
cur.execute(statement)

statement = '''
    DROP TABLE IF EXISTS 'Type';
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
    CREATE TABLE 'Type' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Type' TEXT NOT NULL,
        'Strong Against' TEXT NOT NULL,
        'Weak Against' TEXT NOT NULL
    );
'''
cur.execute(statement)
conn.commit()

#creating the table 'Pokemon', column names id, Pokemon name, region id, type id
statement = '''
    CREATE TABLE 'Pokemon' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Pokemon' TEXT NOT NULL,
        'Type Id' INTEGER NOT NULL,
        'Region Id' INTEGER NOT NULL
    );
'''
cur.execute(statement)
conn.commit()

#creating the table 'Moves', column names id, Move name, type id
statement = '''
    CREATE TABLE 'Moves' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Move name' TEXT NOT NULL,
        'Type Id' INTEGER NOT NULL
    );
'''
cur.execute(statement)
conn.commit()

#creating the table 'Poke-Move', column names id, Pokemon id, move id
statement = '''
    CREATE TABLE 'Poke-Move' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Pokemon Id' INTEGER NOT NULL,
        'Move Id' INTEGER NOT NULL
    );
'''
cur.execute(statement)
conn.commit()

# =============================================================================
# Populating the tables
# =============================================================================

baseurl = 'http://pokemon.wikia.com'

def get_regions_data():
    regions_extension = '/wiki/Category:Region_Starters'
    main_regions_page = requests.get(baseurl+regions_extension).text
    main_regions_soup = BeautifulSoup(main_regions_page, 'html.parser')
    names_list = []
    urls_list = []    
    regions_section = main_regions_soup.find_all("li", {"class": "category-page__trending-page"})
    for region in regions_section:
        regions_url = region.find('a')['href'] #gets extensions for individual region's url
        regions_title = region.find("figcaption", {"class": "category-page__trending-page-title"}).text
        #gets the text of each section, but it includes "starter pokemon"
        regions_name = regions_title.split(' ')[0] #split string by space and display just first element i.e. the name
       
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
            hoenn_names = []
            hoenn_urls = []
            for pokemon in pokemon_names:
                hoenn_names.append(pokemon.text)
            hoenn_names.remove('Hoenn Region')
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
    johto_names = names_list[:3]
    johto_urls = urls_list[:3]
    kanto_names = names_list[3:]
    kanto_urls = urls_list[3:]

get_regions_data()

conn.close()