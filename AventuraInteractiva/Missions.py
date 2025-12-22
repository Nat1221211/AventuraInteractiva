# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe Mission.

import random
import Entitat
import Objectes

class Mission():
    
    Name = ""
    Description = ""
    Status = "Unacceped"
    Rewards = {}


    # Metodes
    def __init__(self, name, description, rewards):
        self.Name = name
        self.Description = description
        self.Rewards = rewards
    
    def Aceptar(self):
        self.Status = "Acepted"
    
    def Completed(self):
        self.Status = "Rewards Unclaimed"

    def ClaimedRewards(self, jugador):
        self.Status = "Completed"
        for i in self.Rewards:
            if type(i) == str:
                jugador.Tituls.append(i)
            elif type(i) == tuple:
                if type(i[0]) == Objectes.ObjecteCombat:
                    jugador.AfegirObjecte(i[0], i[1])
                    print(f"Has obtingut {i[1]} {i[0].ObjectName}")
                elif i[0] == "Gold":
                    jugador.gold += i[1]
                    print(f"Has obtingut {i[1]} gold.")
                elif i[0] == "XP":
                    jugador.AddXP(i[1])

class FindMission(Mission):
    
    Objective = ""
    
    # Metodes
    def __init__(self, name, description, rewards, objective):
        self.Name = name
        self.Description = description
        self.Rewards = rewards
        self.Objective = objective
    
    def Completed(self):
        self.Status = "Rewards Unclaimed"

class ObjectMission(Mission):
    
    Objective = Objectes.ObjecteClau
    
    # Metodes
    def __init__(self, name, description, rewards, objective):
        self.Name = name
        self.Description = description
        self.Rewards = rewards
        self.Objective = objective
    
    def Completed(self):
        self.Status = "Rewards Unclaimed"

class KillMission(Mission):
    
    Objective = Entitat.Entity
    Quantity = int()
    Count = int()
    
    # Metodes
    def __init__(self, name, description, rewards, qty, objective):
        self.Name = name
        self.Description = description
        self.Rewards = rewards
        self.Quantity = qty
        self.Objective = objective

    def IncrementCount(self, enemy):
        if enemy.base == self.Objective:
            self.Count += 1
    
    def Completed(self, jugador):
        if self.Count >= self.Quantity:
            self.Status = "Rewards Unclaimed"
            self.ClaimedRewards(jugador)


