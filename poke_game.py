#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 11:07:45 2018

@author: nehabhomia
"""

from poke_db import *

# =============================================================================
# Classes
# =============================================================================

class Trainer:
    '''
    Will create the instance of a trainer.
    input = trainer name, choice of region
    attributes = name, region
    '''
    
class Pokemon:
    '''
    Will create the instance of a pokemon.
    input = trainer's choice of region
    attributes = pokemon name, type, region, moves, health (base health of 1000)
    '''

# =============================================================================
# Functions
# =============================================================================

def get_trainer_input():
    '''
    This function will take in players inputs (both player 1 and player 2) and
    create 2 instances of trainers from them.
    inputs asked within function = player name and player region.
    choice of region from 3 regions - Johto, Kanto and Hoenn
    Will return the region of choice.
    '''
    pass

def assign_pokemon(region):
    '''
    Will take the region returned in the previous function and will then randomly
    assign a pokemon to each player based on the region of their choice.
    Will return two instaces of the Pokemon class, assigned to each player.
    '''
    pass

def health_progress_bar():
    '''
    This function will help us create the reverse progress bar to denote the
    health score of the pokemon of each player. Bar will decrease as moves are
    played.
    '''
    ### https://github.com/WoLpH/python-progressbar
    ### https://progressbar-2.readthedocs.io/en/latest/progressbar.widgets.html#progressbar.widgets.ReverseBar
    pass

def pokemon_battle(pokemon):
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
    pass