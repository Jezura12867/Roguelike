import pygame
from random import randint

class Rooms:

    def __init__(self) -> None:

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
                ]
        }


        self.room = 0, 0


    def new_room(self, x, y, rooms_dict):
        rooms_dict.update({f"{self.room}": self.types[str(randint(0, len(self.types) - 1))]})
        return rooms_dict


    def main(self, rooms_dict):

        if rooms_dict.get(f"{self.room[0], self.room[1]}") == None:
            rooms_dict = (Rooms().new_room(self.room[0], self.room[1], rooms_dict))
        
        return rooms_dict.get(f"{self.room[0], self.room[1]}"), rooms_dict
