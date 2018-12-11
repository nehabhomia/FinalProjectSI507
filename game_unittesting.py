#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 23:35:10 2018

@author: nehabhomia
"""

import unittest
import poke_game as game
#import poke_db as database
import sqlite3

class TestTrainer(unittest.TestCase):

    def testConstructor(self):
        trainer1 = game.Trainer('Neha', 'Kanto')
        trainer2 = game.Trainer('Danny', 'Johto')
        trainer3 = game.Trainer('Bryan', 'Hoenn')
        
        self.assertEqual(trainer1.name, 'Neha')
        self.assertEqual(trainer1.region, 'Kanto')
        self.assertEqual(trainer1.__str__(), 'Welcome to Kanto, Neha!')

        self.assertEqual(trainer2.name, 'Danny')
        self.assertEqual(trainer2.region, 'Johto')
        self.assertEqual(trainer2.__str__(), 'Welcome to Johto, Danny!')

        self.assertEqual(trainer3.name, 'Bryan')
        self.assertEqual(trainer3.region, 'Hoenn')
        self.assertEqual(trainer3.__str__(), 'Welcome to Hoenn, Bryan!')
    
class TestPokemon(unittest.TestCase):
    
    def testConstructor(self):
        pokemon1 = game.Pokemon('Bulbasaur', 'Grass', 'Kanto', ['Solar Beam', 'Whip', 'Slash'])
        pokemon2 = game.Pokemon('Totodile', 'Water', 'Johto', ['Ice-Punch', 'Swords Dance', 'Cut'])
        
        self.assertEqual(pokemon1.name, 'Bulbasaur')
        self.assertEqual(pokemon1.type, 'Grass')
        self.assertEqual(pokemon1.region, 'Kanto')
        self.assertEqual(pokemon1.moves, ['Solar Beam', 'Whip', 'Slash'])
        self.assertEqual(pokemon1.__str__(), 'The Pokemon assigned to you is Bulbasaur. It is a Grass Pokemon from Kanto. It can play several moves like Solar Beam, Whip, etc..')

        self.assertEqual(pokemon2.name, 'Totodile')
        self.assertEqual(pokemon2.type, 'Water')
        self.assertEqual(pokemon2.region, 'Johto')
        self.assertEqual(pokemon2.moves, ['Ice-Punch', 'Swords Dance', 'Cut'])
        self.assertEqual(pokemon2.__str__(), 'The Pokemon assigned to you is Totodile. It is a Water Pokemon from Johto. It can play several moves like Ice-Punch, Swords Dance, etc..')
        
class TestDatabase(unittest.TestCase):
    
    def testScraping(self):
        pass
    
    def testApi(self):
        pass
    
    def testTableCreation(self):
        conn = sqlite3.connect('pokemon_database')
        cur = conn.cursor()
        
        statement = "SELECT count(*) FROM sqlite_sequence WHERE name = 'Regions'"
        cur.execute(statement)
        test = cur.fetchone()
        self.assertEqual(test, (1,))
        conn.commit()
        
        statement = "SELECT count(*) FROM sqlite_sequence WHERE name = 'Junk'"
        cur.execute(statement)
        test = cur.fetchone()
        self.assertEqual(test, (0,))
        conn.commit()
        
        conn.close()
        pass
    
    def testTablePopulation(self):
        conn = sqlite3.connect('pokemon_database')
        cur = conn.cursor()
        
        statement = "SELECT count(*) FROM Moves WHERE TypeId = 15"
        cur.execute(statement)
        test = cur.fetchone()
        self.assertEqual(test, (2,))
        conn.commit()
        
        statement = "SELECT count(*) FROM TypeStrength"
        cur.execute(statement)
        test = cur.fetchone()
        self.assertEqual(test, (3,))
        conn.commit()
        
        conn.close()
        pass

#class TestBattle(unittest.TestCase):
#    
#    def testRandomAssignment(self):
#        pass

unittest.main()