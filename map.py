import pygame
from random import randint

class Rooms:

    def __init__(self) -> None:


        # Stores every possible room
        # X -- Wall
        # E -- Entrance/exit
        # S -- Enemy spawn locations
        # [blank] -- Air
        self.types = {
            "0": [  "XXXXXXXXXEEXXXXXXXXXXXXX",
                    "X                      X",
                    "X         S      S     X",
                    "X   S                  X",
                    "X                      X",
                    "E                      E",
                    "E   S    XX            E",
                    "E        XX      S     E",
                    "X         S            X",
                    "X                      X",
                    "X                   S  X",
                    "X                      X",
                    "X    S                 X",
                    "XXXXXXXXXEEXXXXXXXXXXXXX",
                ],
            "1": [  "XXXXXXXXXEEXXXXXXXXXXXXX",
                    "X                      X",
                    "X    S                 X",
                    "X                S     X",
                    "X                      X",
                    "E                      E",
                    "E          S           E",
                    "E                      E",
                    "X                 S    X",
                    "X   S                  X",
                    "X              S       X",
                    "X                      X",
                    "X                      X",
                    "XXXXXXXXXEEXXXXXXXXXXXXX",
                ],
            "2": [  "XXXXXXXXXEEXXXXXXXXXXXXX",
                    "X                 S    X",
                    "X   S                  X",
                    "X      XXXXXX  XXXX    X",
                    "X      X          X    X",
                    "E           S          E",
                    "E       S              E",
                    "E                      E",
                    "X      X          X    X",
                    "X      XXXXXX  XXXX    X",
                    "X                S     X",
                    "X   S                  X",
                    "X                      X",
                    "XXXXXXXXXEEXXXXXXXXXXXXX",
                ],
            "3": [  "XXXXXXXXXEEXXXXXXXXXXXXX",
                    "X   S   X              X",
                    "X       X         S    X",
                    "X                      X",
                    "X                      X",
                    "E         XXXXXX       E",
                    "E   S     XXXXXX       E",
                    "E         XXXXXX       E",
                    "X            X         X",
                    "X            X    S    X",
                    "X       S    X         X",
                    "X                      X",
                    "X              S       X",
                    "XXXXXXXXXEEXXXXXXXXXXXXX",
                ]
        }


    # Adds new room to rooms_dict; name is determined by the coordinates of the room on the map
    def new_room(self, rooms_dict, room):
        rooms_dict.update({f"{room}": (self.types[str(randint(0, len(self.types) - 1))], randint(1, 5))})
        return rooms_dict


    def main(self, rooms_dict, room):

        # If current room is in the list of rooms generated
        if rooms_dict.get(f"{room[0], room[1]}") == None:
            rooms_dict = (Rooms().new_room(rooms_dict, room))
        
        return rooms_dict.get(f"{room[0], room[1]}"), rooms_dict, room
