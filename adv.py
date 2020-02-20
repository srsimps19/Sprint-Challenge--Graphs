from room import Room
from player import Player
from world import World
from stack import Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

bestPath = []
traversal_path = []

def explore(player, world, traversal_path, visited):
    trackBack = Stack()
    while len(visited) < len(room_graph):
        thisRoom = player.current_room
        visited.add(thisRoom.id)
        roomExits = thisRoom.get_exits()
        print(f"Room Exits: {roomExits}")
        roomNumbers = []

        for direction in roomExits:
            roomNumbers.append(thisRoom.get_room_in_direction(direction))
        
        unexploredDirections = []

        for room in roomNumbers:
            if room.id not in visited:
                unexploredDirections.append(roomExits[roomNumbers.index(room)])
        
        if len(unexploredDirections) > 0:
            direction = random.randint(0, len(unexploredDirections)-1)
            moveDir = unexploredDirections[direction][0]
            trackBackDir = ''
            if moveDir == 'n':
                trackBackDir = 's'
            elif moveDir == 's':
                trackBackDir = 'n'
            elif moveDir == 'e':
                trackBackDir = 'w'
            else:
                trackBackDir = 'e'

        if len(unexploredDirections) >= 1:
            pathBack = []
            trackBack.push(pathBack)

        pathBack.append(trackBackDir)
        player.travel(moveDir, False)
        traversal_path.append(moveDir)

    if len(unexploredDirections) == 0:
        if trackBack.size()>0:
            pathBack = trackBack.pop()
            while len(pathBack) >0:
                move = pathBack[-1]
                del pathBack[-1]
                player.travel(move, False)
                traversal_path.append(move)
        else:
            return traversal_path

    return traversal_path

def mainLoop(attempts, world):
    bestPath = [None] * 100000
    traversal_path = []

    for a in range(attempts):
        print(f"attempt: {a+1}")
        player = Player(world.starting_room)
        visited = set()
        trackBack = Stack()
        traversal_path = []
        explore(player, world, traversal_path, visited)
        if len(traversal_path) < len(bestPath):
            bestPath = traversal_path

    traversal_path = bestPath

    return traversal_path

traversal_path = mainLoop(1, world)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
