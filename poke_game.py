#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 11:07:45 2018

@author: nehabhomia
"""

#from poke_db import *
import progressbar
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
        self.health = 250
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
    pass

'''
In this game section we will take in the two Players' inputs and create two
pokemon instances using our game file and will create an interactive prompt.
Each player will be asked to choose a move form a list of 10 moves that their
pokemon can make.
After both players have input their choice of move, the moves will be played.
This move MIGHT be displayed using progress bar, and each pokemon's progress
bar will decrease by the power of the move played by the opposing player.
As soon as one pokemon's progress bar/health score reaches zero, that pokemon
loses and the other player is declared as winner.
Game over.
'''

if __name__ == "__main__":
    regions = ['Kanto', 'Johto', 'Hoenn']
    error_message = "\nInvalid input ¯\_(ツ)_/¯. Please Try Again.\n"
    
    user1_name = input("\nPlayer 1 Enter Name: ")
    user1_region = input("Welcome, {}! Enter your choice of Region. You can choose a region from Kanto, Johto or Hoenn: ".format(user1_name))
    while user1_region not in regions:
        print (error_message)
        user1_region = input("Welcome, {}! Enter your choice of Region. You can choose a region from Kanto, Johto or Hoenn: ".format(user1_name))
    trainer1 = Trainer(user1_name, user1_region)
    pokemon_assigned1 = assign_pokemon(trainer1.region)
    print('\n', pokemon_assigned1)
    
    user2_name = input("\nPlayer 2 Enter Name: ")
    user2_region = input("Welcome, {}! Enter your choice of Region. You can choose a region from Kanto, Johto or Hoenn: ".format(user2_name))
    while user2_region not in regions:
        print (error_message)
        user2_region = input("Welcome, {}! Enter your choice of Region. You can choose a region from Kanto, Johto or Hoenn: ".format(user2_name))
    trainer2 = Trainer(user2_name, user2_region)
    pokemon_assigned2 = assign_pokemon(trainer2.region)
    print('\n', pokemon_assigned2)
    
    print("\n" + '-'*15 + " Let the battle begin.. " + '-'*15 + "\n")
    
    widgets1 = [
        progressbar.AnimatedMarker(),
        progressbar.DynamicMessage('health'),
        progressbar.AnimatedMarker(),
        " ",
        progressbar.ReverseBar(' ',fill= ":", left="[", right = "] 250")
    ]
    
    widgets2 = [
        progressbar.AnimatedMarker(),
        progressbar.DynamicMessage('health'),
        progressbar.AnimatedMarker(),
        " ",
        progressbar.ReverseBar(' ',fill= ":", left="[", right = "] 250")
    ]
    
    player2Health = progressbar.ProgressBar(widgets=widgets2, min_value=0, max_value=250, prefix=pokemon_assigned2.name)
    player1Health = progressbar.ProgressBar(widgets=widgets1, min_value=0, max_value=250, prefix=pokemon_assigned1.name)
    max_health = 250
    
    currentPlayer1 = True
    initial_statement = "Enter 'Quit' to exit the game at any time. Enter 'Help' for instructions.\n\n"
    help_statement = """\nEnter 'List moves' to get a list of possible moves.\n
    Enter 'Make move' followed by list index number (or chose a random number from 1-10) to make that move against the opposite Trainer's Pokemon.\n
    Enter 'Surrender' to surrender the battle.\n"""
    user_input = input(initial_statement)
    while user_input != 'Quit':
        if user_input == 'Help':
            print (help_statement)
            user_input = input(initial_statement)
        elif user_input == 'List moves':
            if currentPlayer1 == True:
                print ("\n{}'s {}'s moves ".format(trainer1.name, pokemon_assigned1.name))
                move_names = pokemon_assigned1.moves
            else:
                print ("\n{}'s {}'s moves ".format(trainer2.name, pokemon_assigned2.name))
                move_names = pokemon_assigned2.moves
            for move in move_names:
                print('\n', move_names.index(move) + 1, ' ', str(move))
            user_input = input("\n'Make move' or " + initial_statement)
        elif user_input == 'Make move':
            if currentPlayer1 == True:
                my_statement = ("Which of {}'s move do you want to make, {}? ".format(pokemon_assigned1.name, trainer1.name))
                move_power = pokemon_assigned1.power
            else:
                my_statement = ("Which of {}'s move do you want to make, {}? ".format(pokemon_assigned2.name, trainer2.name))
                move_power = pokemon_assigned2.power
            move_number = input(my_statement)
            moves_indices = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
            if move_number in moves_indices:
                attack_power = move_power[int(move_number)-1]
                if currentPlayer1 == True:
                    pokemon_assigned2.health = pokemon_assigned2.health - attack_power
                    show_health2 = max_health - pokemon_assigned2.health
                    if pokemon_assigned2.health <= 0:
                        show_health2 = max_health
                        player2Health.update(show_health2, health = 0)
                        print('\n{} wins!'.format(trainer1.name))
                        break
                    player2Health.update(show_health2, health = pokemon_assigned2.health)
                    currentPlayer1 = False
                    print("\n\n{}'s turn.".format(trainer2.name))
                else:
                    pokemon_assigned1.health = pokemon_assigned1.health - attack_power
                    show_health1 = max_health - pokemon_assigned1.health
                    if pokemon_assigned1.health <= 0:
                        show_health1 = max_health
                        player1Health.update(show_health1, health = 0)
                        print ('\n{} wins!'.format(trainer2.name))
                        break
                    player1Health.update(show_health1, health = pokemon_assigned1.health)
                    currentPlayer1 = True
                    print("\n\n{}'s turn.".format(trainer1.name))
                user_input = input(initial_statement)
            else:
                print(error_message)
                user_input = input("\n'Make move' or " + initial_statement)
        elif user_input == 'Surrender':
            if currentPlayer1 == True:
                print ("\n{} has surrendered. {}'s {} wins!".format(trainer1.name, trainer2.name, pokemon_assigned2.name))
            else:
                print ("\n{} has surrendered. {}'s {} wins!".format(trainer2.name, trainer1.name, pokemon_assigned1.name))
            break
        else:
            print (error_message)
            user_input = input(initial_statement)
            
    print("\n" + '-'*20 + " Game Over " + '-'*20)