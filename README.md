# FinalProjectSI507
Final Project for SI 507

Project title and description:
Live Pokémon Battle Game – Multiplayer
Pokémon battle on the command line, with a choice from 9 starter Pokémon (3 each from 3 regions.) Pokémon start with a health score of 1000, score decreases based on moves played by the other player. First player’s Pokémon to reach a health score of 0 (zero) loses.

Data Sources:
●	http://pokemon.wikia.com/wiki/List_of_Pokémon#Generation%20II
○	Crawling [and scraping] multiple pages in a site you haven’t used before
○	Challenge score = 8
●	https://pokeapi.co
○	Web API you haven’t used before that requires no authorization
○	Challenge score = 3
●	Total challenge score = 11

Data Source 1 - Pokémon Fan Wikipedia:
●	Pokémon Wikipedia site to be used (URL link for the list of all Pokémon) to identify the regions, a list of all types and get the starter Pokémon from the 3 regions of our choice (Johto, Kanto and Hoenn)
●	From this webpage, go to each Pokémon’s individual page and get its information(type).
●	All of this information is then stored in various tables (as described below) in a database.

Data Source 2 - Pokémon API:
●	Using Pokémon names, get moves from the poke api.
●	Populate the moves table in the database using this information.
●	Populate the PokeMoves tables using the Pokemon and the Moves tables. 

Caching:
●	All the Pokémon stats are being stored in a database, and this database will be used during the battle.
●	API requests and requests for BeautifulSoup being cached using the requests-cache library.
●	Requirements.text file added, libraries used =
○	Bs4
○	Requests
○	Requests-Cache
●	Did not need to install sqlite as it is an inbuilt python library.

Database:
●	All the Pokémon stats are being stored in a database, and this database will be used during the battle.
●	The database has 6 tables
○	Regions - (Kanto, Johto, Hoenn)
○	Pokemon
■	9 starter Pokémon
■	3 from each region
■	Johto
●	Chikorita
●	Cyndaquil
●	Totodile
■	Kanto
●	Bulbasaur
●	Charmander
●	Squirtle
■	Hoenn
●	Treecko
●	Torchic
●	Mudkip
○	Types
■	all the types that exist
■	scraped from a list of types on the wiki page
○	TypeStrength
■	Hand-coded
■	Used to amplify moves based on Pokémon type
○	Moves
■	Stores 10 moves for each Pokémon
■	Also stores the type of the move
■	And the power/score of that move
○	PokeMove
■	This table is used as a bridge to track al the moves of a particular Pokémon.

Presentation Option:
●	Presentation would be a live battle on the command line.
●	Player 1 will be asked to enter their name (they’re a trainer) and their choice of starter region (out of 3 region options - Kanto, Johto, Hoenn)
●	A starter Pokémon (from 3 options) will be randomly assigned to the trainer based on their choice of region.
●	Repeat process for Player 2.
●	Battle will begin.
●	Each Pokémon starts with a health score of 1000.
●	Player 1 is asked to choose a move from a list of 10 moves.
●	Player 2 is asked to choose a move from a list of 10 moves.
●	Health scores deduct for the Pokémon based on the move played by the opposite player.
●	The first player’s Pokémon to reach a health score of 0 loses.
●	The move scores/effect vary based on the Pokémon and the move type, which will all be stored in the database.

Presentation Tool:

Command Line/Terminal.
