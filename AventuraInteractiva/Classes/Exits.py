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
    

    def UnlockExit(self, jugador):
        self.Obtained = True
        jugador.AcquiredAchievements.append(self.id)
        self.ClaimRewards(jugador)

    def ComprovarExit(self, jugador):
        print()

    def ClaimRewards(self, jugador):
        for key, value in self.rewards.items():
            if self.unlock["Type"] == "Stat":
                tipus = "Flat"
                if isinstance(value, str):
                    if value.endswith("%"):
                        tipus = "%"
                        value.replace("%", "")
                jugador.StatIncrement[key][tipus]+=value

        
