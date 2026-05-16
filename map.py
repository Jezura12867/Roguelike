# Importing
from random import randint

class Map:

    def __init__(self):

        ## Stores every possible room
        # X -- Wall
        # E -- Entrance/exit
        # S -- Enemy spawn locations
        # [blank] -- Air
        self.types = {
            "0": [  "XXXXXXXXXXXXXXXXXXXXXEEEEEXXXXXXXXXXXXXXXXXXXXXX",
                    "X                                              X",
                    "X         S                              S     X",
                    "X   S                                          X",
                    "X                                  XX          X",
                    "X                                  XX          X",
                    "X   S    XXX           XXX                     X",
                    "X        XXX     S     XXX                     X",
                    "X        XXX           XXX        S            X",
                    "X                                              X",
                    "X                                           S  X",
                    "E                                              E",
                    "E    S                                         E",
                    "E                   XXX                        E",
                    "E         S         XXX                  S     E",
                    "E   S               XXX                        E",
                    "E                                              E",
                    "X                                    XXX       X",
                    "X   S                                XXX       X",
                    "X                S                   XXX       X",
                    "X                                 S            X",
                    "X           XXX                                X",
                    "X           XXX                   S            X",
                    "X           XXX                                X",
                    "X                                           S  X",
                    "X    S                                         X",
                    "X                                              X",
                    "XXXXXXXXXXXXXXXXXXXXXEEEEEXXXXXXXXXXXXXXXXXXXXXX",
                ],
            "1": [  "XXXXXXXXXXXXXXXXXXXXXEEEEEXXXXXXXXXXXXXXXXXXXXXX",
                    "X                                              X",
                    "X           S                            S     X",
                    "X   S                                          X",
                    "X                                              X",
                    "X                                              X",
                    "X   S                                          X",
                    "X                 S                            X",
                    "X                                 S            X",
                    "X                                              X",
                    "X                                         S    X",
                    "E                                              E",
                    "E    S                                         E",
                    "E                                              E",
                    "E         S                              S     E",
                    "E   S                                          E",
                    "E                                              E",
                    "X                                              X",
                    "X   S                                          X",
                    "X                S                             X",
                    "X                                S             X",
                    "X                                              X",
                    "X                                 S            X",
                    "X                                              X",
                    "X                                           S  X",
                    "X    S                                         X",
                    "X                                              X",
                    "XXXXXXXXXXXXXXXXXXXXXEEEEEXXXXXXXXXXXXXXXXXXXXXX",
                ],
            "2": [  "XXXXXXXXXXXXXXXXXXXXXEEEEEXXXXXXXXXXXXXXXXXXXXXX",
                    "X                                              X",
                    "X    S                                 S       X",
                    "X   S                                          X",
                    "X                                              X",
                    "X                                              X",
                    "X   S                                          X",
                    "X                S                             X",
                    "X                                 S            X",
                    "X                                              X",
                    "X                                           S  X",
                    "E        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX        E",
                    "E    S                                         E",
                    "E                                              E",
                    "E         S                              S     E",
                    "E   S                                          E",
                    "E                                              E",
                    "X                                              X",
                    "X   S                                          X",
                    "X                S                             X",
                    "X                                 S            X",
                    "X                                              X",
                    "X                                 S            X",
                    "X                                              X",
                    "X                                           S  X",
                    "X    S                                         X",
                    "X                                              X",
                    "XXXXXXXXXXXXXXXXXXXXXEEEEEXXXXXXXXXXXXXXXXXXXXXX",
                ],
            "3": [  "XXXXXXXXXXXXXXXXXXXXXEEEEEXXXXXXXXXXXXXXXXXXXXXX",
                    "X                                              X",
                    "X         S                              S     X",
                    "X                                              X",
                    "X                                              X",
                    "X               S                              X",
                    "X                                              X",
                    "X        XX                            XX      X",
                    "X        XX                            XX      X",
                    "X        XX                            XX      X",
                    "X        XX  S                         XX   S  X",
                    "E        XX                            XX      E",
                    "E        XX                            XX      E",
                    "E        XX                            XX      E",
                    "E        XX S                          XX      E",
                    "E        XX                            XX      E",
                    "E        XX                            XX      E",
                    "X        XX                            XX      X",
                    "X   S                  XX                      X",
                    "X                S     XX                      X",
                    "X                      XX         S            X",
                    "X                      XX                      X",
                    "X                      XX         S            X",
                    "X                                              X",
                    "X                                           S  X",
                    "X    S                                         X",
                    "X                                              X",
                    "XXXXXXXXXXXXXXXXXXXXXEEEEEXXXXXXXXXXXXXXXXXXXXXX",
                ],
        }


    # Adds new room to rooms_dict; name is determined by the coordinates of the room on the map
    def new_room(self, rooms_dict, room):
        rooms_dict.update({f"{room}": (self.types[str(randint(0, len(self.types) - 1))], randint(1, 5))})
        return rooms_dict


    def main(self, rooms_dict, room):

        # If current room is in the list of rooms generated
        if rooms_dict.get(f"{room[0], room[1]}") == None:
            rooms_dict = (Map().new_room(rooms_dict, room))
        
        return rooms_dict.get(f"{room[0], room[1]}"), rooms_dict, room
