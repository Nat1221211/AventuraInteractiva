# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe Tipus d'entitat.

import random
from Classes import Objectes

class Exits():
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

    def ComprovarExit(self, entitat, jugador):
        unlock = True
        if self.Obtained == False:
            if self.UnlockRequirements["Type"] == "Stat":
                if self.UnlockRequirements["Objective"] == "Lv":
                    if entitat.Lv < self.UnlockRequirements["Amount"]:
                        unlock = False
                elif self.UnlockRequirements["Objective"] in []:
                    print("")
                else:
                    if entitat.StatsCombat[self.UnlockRequirements["Objective"]] < self.UnlockRequirements["Amount"]:
                        unlock = False            
            else:
                unlock = False
            if unlock == True:
                self.Obtained = True
                jugador.AcquiredAchievements.append(self.id)
                self.ClaimRewards(jugador)


    def ClaimRewards(self, jugador):
        for key, value in self.Rewards.items():
            if self.UnlockRequirements["Type"] == "Stat":
                tipus = "Flat"
                if isinstance(value, str):
                    if value.endswith("%"):
                        tipus = "%"
                        value.replace("%", "")
                jugador.StatIncrement[key][tipus]+=value

class KillExit(Exits):

    def __init__(self, iden, name, description, hiden, rewards, unlock, count):
        super().__init__(iden, name, description, hiden, rewards, unlock)
        self.Count = count

        
