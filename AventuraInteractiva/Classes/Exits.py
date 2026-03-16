# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe Tipus d'entitat.

import random
from Classes import Objectes

class Exits():
    
    Obtained = False

    # Metodes
    def __init__(self, iden, name, description, hiden, rewards, unlock):
        self.id = iden
        self.Name = name
        self.Description = description
        self.Hiden = hiden
        self.Obtained = False
        self.Rewards = rewards
        self.UnlockRequirements = unlock

        
