# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe Mission.

import random
import Entitat
import Objectes
import Zones

class Mission():
    
    Name = ""
    Description = ""
    Status = "Unacceped"
    Rewards = {}
    Requisite = []
    Place = Zones.Zona


    # Metodes
    def __init__(self, name, description, rewards):
        self.Name = name
        self.Description = description
        self.Rewards = rewards
    
    def Aceptar(self, jugador):
        reqcompleted = True
        if len(self.Requisite) > 0:
            for i in self.Requisite:
                if type(i) == tuple:
                    if i[0] == "Lv":
                        if jugador.Lv <= i[1]:
                            reqcompleted = False
                elif type(i) in [Mission, FindMission, ObjectMission, KillMission]:
                    if i.Status != "Completed":
                        reqcompleted = False
        if reqcompleted == True:
            self.Status = "Acepted"
            print(f"Has aceptat {self.Name}.\n")
        else:
            print("No compleixes amb els requisits per a la missio...")
        input("Presiona per a continuar...")
    
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
    def __init__(self, name, description, rewards, objective, requisite, place):
        self.Name = name
        self.Description = description
        self.Rewards = rewards
        self.Objective = objective
        self.Requisite = requisite
        self.Place = place
    
    def Completed(self):
        self.Status = "Rewards Unclaimed"

class ObjectMission(Mission):
    
    Objective = Objectes.ObjecteClau
    
    # Metodes
    def __init__(self, name, description, rewards, objective, requisite, place):
        self.Name = name
        self.Description = description
        self.Rewards = rewards
        self.Objective = objective
        self.Requisite = requisite
        self.Place = place
   
    def Completed(self):
        self.Status = "Rewards Unclaimed"

class KillMission(Mission):
    
    Objective = Entitat.Entity
    Quantity = int()
    Count = int()
    
    # Metodes
    def __init__(self, name, description, rewards, qty, objective, requisite, place):
        self.Name = name
        self.Description = description
        self.Rewards = rewards
        self.Quantity = qty
        self.Objective = objective
        self.Requisite = requisite
        self.Place = place

    def IncrementCount(self, enemy):
        if enemy.base == self.Objective:
            self.Count += 1
    
    def Completed(self):
        if self.Count >= self.Quantity:
            self.Status = "Rewards Unclaimed"


