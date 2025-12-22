# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe Tipus d'entitat.

import random

class Mission():
    
    Name = ""
    Description = ""
    Status = "Unaccepted"
    Rewards = {}
    Objective = ""


    # Metodes
    def __init__(self, name, description, rewards):
        self.Name = name
        self.Description = description
        self.Rewards = rewards
    
    def Aceptar(self):
        self.Status = "Acepted"

    def Completed(self):
        self.Status = "Completed"



# class StoryMission(Mission):
    
#     Name = ""
#     Description = ""

#     # Metodes
#     def __init__(self, name, description):
#         self.Name = name
#         self.Description = description

# class SubMission(Mission):
    
#     Name = ""
#     Description = ""

#     # Metodes
#     def __init__(self, name, description):
#         self.Name = name
#         self.Description = description