#!/usr/bin/env python3

import sys, logging, os, json

version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


print("\nWelcome to 'Magellan'. You awake on the ship 'Magellan' and seek to figure out what transpired and possibly how to even leave. \nExplore, uncover, and escape. Happy hunting. Oh and always assume the character is facing north to help with navigating :)")

global player_inventory
player_inventory = []

#global count
#count = 0

# Game loop functions
def render(game,current,moves,points):
    ''' Displays the current room, moves, and points '''
    r = game['rooms']
    c = r[current]
    
    print('\n\nMoves: {moves}, Points: {points}'.format(moves=moves, points=points))
    print('\n\nYou are {name}'.format(name=c['name']))
    print(c['desc'])
    if len(c['inventory']):
        print('You see the following items:')
        for i in c['inventory']:
            print('\t{i}'.format(i=i))

def getInput(game,current,verbs):
    ''' Asks the user for input and normalizes the inputted value. Returns a list of commands '''

    toReturn = input('\nWhat would you like to do? ').strip().upper().split()
    if (len(toReturn)):
        #assume the first word is the verb
        toReturn[0] = normalizeVerb(toReturn[0],verbs)
    return toReturn


def update(selection,game,current,inventory):
    ''' Process the input and update the state of the world '''
    s = list(selection)[0]  #We assume the verb is the first thing typed
    r = game['rooms']
    c = r[current]

    if s == "":
        print("\nSorry, I don't understand.")
        return current
    elif s == 'EXITS':
        printExits(game,current)
        return current
    elif s == 'GET' and c == 'INSPECT MED BAY':
        add_inventory("keycard") 
        c['inventory'].remove("keycard")
        print('You got the keycard.')
        return current
    elif s == 'USE':
        if len(player_inventory):
            for e in game['rooms'][current]['exits']:
                if s == e['verb'] and e['target'] != 'NoExit':
                    return e['target']
        else:
            print("\nYou don't have the keycard yet.")            
    else:
        for e in game['rooms'][current]['exits']:
            if s == e['verb'] and e['target'] != 'NoExit':
                return e['target']
    print("\nType something else.")
    return current


# Helper functions

def printExits(game,current):
    e = ", ".join(str(x['verb']) for x in game['rooms'][current]['exits'])
    print('\nYou can do the following: {directions}'.format(directions = e))

def normalizeVerb(selection,verbs):
    for v in verbs:
        if selection == v['v']:
            return v['map']
    return ""

def end_game(winning,points,moves):
    if winning:
        print('You step into the Escape Pod and close the hatch. With a sudden jolt the pod fires into the void, the Magellan getting smaller and smaller and the only thing you do is clutch the bear to your chest. All you can do now is wait. \nYou have escaped, congrats! I hope you enjoyed.')
       # print('You scored {points} points in {moves} moves! Nicely done!'.format(moves=moves, points=points))
    else:
        print('Thanks for playing!')
        print('You scored {points} points in {moves} moves. See you next time!'.format(moves=moves, points=points))

def add_inventory(item):
    # This is an interesting addition to the game
    player_inventory.append(item)
    print("\nYou picked up the keycard.")

    #r = game['rooms']
    #c = r[current]

    #if len(c['inventory']):

       # c['inventory']) = []

  #  else:
   #     print('There is nothing here.')    

#def counter():
 #   count = 1
  #  return True




def main():
    gameFile = 'game.json'

    game = {}
    with open(gameFile) as json_file:
        game = json.load(json_file)

    #player_inventory = {"keycard":0}
    current = 'START'
    win = ['END']
    lose = []
    moves = 0
    points = 0
    inventory = []
   # count = 0
   # r = game['rooms']
    #c = r[current]
    while True:

        render(game,current,moves,points)

        selection = getInput(game,current,game['verbs'])

        if selection[0] == 'QUIT':
            end_game(False,points,moves)
            break


#if player enters the med bay put a counter at 1  then if they do 'use' and counter is 1 then they can enter the capt quarters

       # if selection[0] == 'GET':
        #    r = game['rooms']
         #   c = r[current]

          #  add_inventory()

        current = update(selection,game,current,inventory)

        #if current[game['rooms']] == 'INSPECT MED BAY':
         #   count = count + 1
          #  print("\nYou got the keycard.")
           # continue

        if current in win:
            end_game(True,points,moves)
            break
        if current in lose:
            end_game(False,points,moves)
            break

        moves += 1





if __name__ == '__main__':
	main()