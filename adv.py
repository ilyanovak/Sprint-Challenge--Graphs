from room import Room
from player import Player
from world import World
from collections import deque

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

traversal_path = []
traversal_graph = {}

def traverse_helper(prevDirection, prevRoom):

    if player.current_room.id not in traversal_graph:
        traversal_graph[player.current_room.id] = dict.fromkeys(
            player.current_room.get_exits(), "?")

    if prevDirection is not None:
        traversal_graph[prevRoom.id][prevDirection] = player.current_room.id
    if prevDirection == "n":
        traversal_graph[player.current_room.id]['s'] = prevRoom.id
    elif prevDirection == "s":
        traversal_graph[player.current_room.id]['n'] = prevRoom.id
    elif prevDirection == "e":
        traversal_graph[player.current_room.id]['w'] = prevRoom.id
    elif prevDirection == "w":
        traversal_graph[player.current_room.id]['e'] = prevRoom.id

    emptyDirections = [
        prevDirection for prevDirection in traversal_graph[player.current_room.id]
        if traversal_graph[player.current_room.id][prevDirection] == '?']

    if emptyDirections == []:
        if prevDirection == "n":
            player.travel('s')
            traversal_path.append('s')
        elif prevDirection == "s":
            player.travel('n')
            traversal_path.append('n')
        elif prevDirection == "e":
            player.travel('w')
            traversal_path.append('w')
        elif prevDirection == "w":
            player.travel('e')
            traversal_path.append('e')
        return

    for direction in emptyDirections:
        prevRoom = player.current_room
        player.travel(direction)
        traversal_path.append(direction)

        traverse_helper(direction, prevRoom)

    if prevDirection == "n":
        player.travel('s')
        traversal_path.append('s')
    elif prevDirection == "s":
        player.travel('n')
        traversal_path.append('n')
    elif prevDirection == "e":
        player.travel('w')
        traversal_path.append('w')
    elif prevDirection == "w":
        player.travel('e')
        traversal_path.append('e')

traverse_helper(None, None)

# print(traversal_path)
# print(traversal_graph)

# # TRAVERSAL TEST - DO NOT MODIFY
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



# #######
# # UNCOMMENT TO WALK AROUND
# #######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
