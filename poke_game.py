#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 11:07:45 2018

@author: nehabhomia
"""

#from poke_db import *
import progressbar
import time
import sqlite3

conn = sqlite3.connect('pokemon_database')
cur = conn.cursor()

# =============================================================================
# Classes
# =============================================================================

class Trainer:
    '''
    Will create the instance of a trainer.
    input = trainer name, choice of region
    attributes = name, region
    '''
    def __init__(self, name, region):
        self.name = name
        self.region = region
    
    def __str__(self):
        return ('Welcome to {}, {}!'.format(self.region, self.name))
    
class Pokemon:
    '''
    Will create the instance of a pokemon.
    input = trainer's choice of region
    attributes = pokemon name, type, region, moves, health (base health of 1000)
    '''
    def __init__(self, name, poke_id, poke_type, region, moves, power):
        self.name = name
        self.type = poke_type
        self.region = region
        self.moves = moves
        self.health = 1000
        self.id = poke_id
        self.power = power
    
    def __str__(self):
        moves = self.moves[0] + ', ' + self.moves[1] + ', etc.'
        return ('The Pokemon assigned to you is {}. It is a {} Pokemon from {}. It can play several moves like {}.'.format(self.name, self.type, self.region, moves))

# =============================================================================
# Functions
# =============================================================================

def get_trainer_input(trainer_number):
    '''
    This function will take in players inputs (both player 1 and player 2) and
    create 2 instances of trainers from them.
    inputs asked within function = player name and player region.
    choice of region from 3 regions - Johto, Kanto and Hoenn
    Will return the region of choice.
    '''
    # Display help text to start the battle
    help_statement = """Enter trainer%s name and choice of Pokemon region in space separated format <name> <region>\nYou can choose a region from Kanto, Johto, Hoenn"""
    user_resp = input(help_statement%trainer_number + ": ")
    trainer1_input = user_resp.split(' ')
    trainer1 = Trainer(trainer1_input[0], trainer1_input[1])
    return trainer1

def assign_pokemon(region):
    '''
    Will take the region returned in the previous function and will then randomly
    assign a pokemon to each player based on the region of their choice.
    Will return two instaces of the Pokemon class, assigned to each player.
    '''
    # get region id
    statement = "SELECT Id FROM Regions WHERE Region = ?"
    cur.execute(statement, (region,))
    region_id = cur.fetchone()[0]

    # get one Pokemon from this region_id randomly
    statement = "SELECT * FROM Pokemons WHERE RegionId = ? ORDER BY RANDOM()"
    cur.execute(statement, (region_id,))
    pokemon = cur.fetchone()
    pokemon_id = pokemon[0]
    pokemon_name = pokemon[1]
    type_id = pokemon[2]

    # get type name for this Pokemon
    statement = "SELECT Type FROM Types WHERE Id = ?"
    cur.execute(statement, (type_id,))
    type_name = cur.fetchone()[0]

    # get all moves name for this pokemon
    statement = """SELECT MoveName, Power FROM Moves
JOIN PokeMove ON Moves.Id = PokeMove.MoveId
JOIN Pokemons ON PokeMove.PokemonId = Pokemons.Id
WHERE Pokemons.Id = ?
        """
    cur.execute(statement, (pokemon_id,))
    pokemon_moves = cur.fetchall()
    pokemon_moves_list = []
    pokemon_power_list = []
    for move in pokemon_moves:
        pokemon_moves_list.append(move[0])
        pokemon_power_list.append(move[1])
    pokemon_object = Pokemon(pokemon_name, pokemon_id, type_name, region, pokemon_moves_list, pokemon_power_list)
    return pokemon_object

def health_progress_bar():
    '''
    This function will help us create the reverse progress bar to denote the
    health score of the pokemon of each player. Bar will decrease as moves are
    played.
    '''
    ### https://github.com/WoLpH/python-progressbar
    ### https://progressbar-2.readthedocs.io/en/latest/progressbar.widgets.html#progressbar.widgets.ReverseBar
    widgets = [
        progressbar.AnimatedMarker(),
        progressbar.DynamicMessage('health'),
        progressbar.AnimatedMarker(),
        " ",
        progressbar.ReverseBar(' ',fill= "#", left="[", right = "]")
    ]
    player1Health = progressbar.ProgressBar(widgets=widgets, min_value=0, max_value=1000, prefix="player1 ").start()
    max_health = 1000
    current_health = max_health
    # let us assume player 1 got these power shots on him, total = 1000
    power = [50, 100, 200, 50, 300, 25, 50, 25, 100, 100]
    for i in range(10):
        current_health = current_health - power[i]
        show_health = max_health - current_health
        player1Health.update(show_health, health = current_health)
        time.sleep(0.5)
    player1Health.finish()

#health_progress_bar()

def pokemon_battle():
    '''
    This function will take in the two Pokemon instances and will create an
    interactive prompt.
    Each player will be asked to choose a move form a list of 10 moves that their
    pokemon can make.
    After both players have input their choice of move, the moves will be played.
    This move MIGHT be displayed using progress bar, and each pokemon's progress
    bar will decrease by the power of the move played by the opposing player.
    As soon as one pokemon's progress bar/health score reaches zero, that pokemon
    loses and the other player is declared as winner.
    Game over.
    '''
    ### don't forget to code for the players to be able to quit the game at any
    ### point of time.
    
    #get first trainer
    trainer1 = get_trainer_input(1)
    print("#############")
    print(trainer1)
    print("#############")
    # get random pokemon for this trainer from selected region
    pokemon_assigned1 = assign_pokemon(trainer1.region)
    print()
    print(pokemon_assigned1)
    print()

    # get second trainer
    trainer2 = get_trainer_input(2)
    print("#############")
    print(trainer2)
    print("#############")
    # get random pokemon for this trainer from selected region
    pokemon_assigned2 = assign_pokemon(trainer2.region)
    print()
    print(pokemon_assigned2)

#pokemon_battle()

conn.close()