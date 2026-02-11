import pygame
from random import randint

class Rooms:

    def __init__(self) -> None:


        # Stores every possible room
        self.types = {
            "0": [  "XXXXXXXXXXXXXEEEXXXXXXXXXXXXXXX",
                    "X                             X",
                    "X     X                       X",
                    "X                             X",
                    "X                             X",
                    "X                             X",
                    "X                             X",
                    "E                             E",
                    "E                XX           E",
                    "E                XX           E",
                    "X                             X",
                    "X                             X",
                    "X                             X",
                    "X                             X",
                    "X                             X",
                    "X                             X",
                    "X                             X",
                    "XXXXXXXXXXXXXEEEXXXXXXXXXXXXXXX",
                ],
            "1": [  "XXXXXXXXXXXXXEEEXXXXXXXXXXXXXXX",
                    "X                             X",
                    "X     X                       X",
                    "X                             X",
                    "X                             X",
                    "X                             X",
                    "X                             X",
                    "E                             E",
                    "E                             E",
                    "E                             E",
                    "X                             X",
                    "X                             X",
                    "X                             X",
                    "X                             X",
                    "X                             X",
                    "X                             X",
                    "X                             X",
                    "XXXXXXXXXXXXXEEEXXXXXXXXXXXXXXX",
                ],
            "2": [  "XXXXXXXXXXXXXEEEXXXXXXXXXXXXXXX",
                    "X                             X",
                    "X                             X",
                    "X     XXXXXXXXXXXXXXXXXXX     X",
                    "X                             X",
                    "X                             X",
                    "X                             X",
                    "E                             E",
                    "E                             E",
                    "E                             E",
                    "X                             X",
                    "X                             X",
                    "X                             X",
                    "X                             X",
                    "X                             X",
                    "X                             X",
                    "X                             X",
                    "XXXXXXXXXXXXXEEEXXXXXXXXXXXXXXX",
                ],
            "3": [  "XXXXXXXXXXXXXEEEXXXXXXXXXXXXXXX",
                    "X                     X       X",
                    "X     X                       X",
                    "X                             X",
                    "X                   XX        X",
                    "X                             X",
                    "X                             X",
                    "E                             E",
                    "E                             E",
                    "E              X              E",
                    "X                    X        X",
                    "X                             X",
                    "X                     X       X",
                    "X       X                     X",
                    "X       XX                    X",
                    "X                             X",
                    "X                             X",
                    "XXXXXXXXXXXXXEEEXXXXXXXXXXXXXXX",
                ]
        }


    # Adds new room to rooms_dict; name is determined by the coordinates of the room on the map
    def new_room(self, rooms_dict, room):
        rooms_dict.update({f"{room}": self.types[str(randint(0, len(self.types) - 1))]})
        return rooms_dict


    def main(self, rooms_dict, room):

        # If current room is in the list of rooms generated
        if rooms_dict.get(f"{room[0], room[1]}") == None:
            rooms_dict = (Rooms().new_room(rooms_dict, room))
        
        return rooms_dict.get(f"{room[0], room[1]}"), rooms_dict, room
