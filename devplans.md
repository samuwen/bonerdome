README:

Combat System
	Design damage / defense mechanisms

Abilities
	create and build lots of abilities

Professions
	Flesh out profession system. create multiple professions and give them varied skillsets

Look system
	Need to adjust the menu so that more useful information is written about the given object and remove the a) b) c) prompts.
	Need to write all the info for any given object

Escape menu (to handle quitting the app, settings menu, other shit like that)

File reorg
	Lots of stuff is still in settings.py where it should not be

Multiple mapping methods (Standard is boring)

Look past current player's location / map bounds (scrolling, X command in stone soup)

running

splash targetting

build keymapping menu and move handle_keys to read the instance of the map. split all those functions out into their own little functions
	so that handle_keys just acts as a traffic cop

monsters wake up and wander around the map

monsters pathfind the player if they know he's around / just off screen

monsters respawn if enemy population drops too low

redesign the entire way enemies and items are populated in the game. the current way it works is that it determines a max number of potential things that can spawn in a room and then tries to select them based on a set of percentages. its a neat system for something with a tiered set of percentages that all need to be held to (ie: orcs can spawn 80% of the time, and if that's the only choice, (this is only invoked if the tiles aren't blocked. its an ass-backwards way of handling it) then the orc will always spawn. if there's additional possibilities that can spawn, it'll check if the orc spawns, then the next thing, and such and so forth.). This will block the entire process of monster respawn and stuff like that.

fuck one thing leads to 2 others. gotta revamp the equipment system. things are equipped and handled directly on the object class? instead of the combatant class? also the inventory is kept independent of the object class for no good fucking reason. everything is garbage and i hate it. :D