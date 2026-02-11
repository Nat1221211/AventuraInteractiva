# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe Mission.

import random
from Classes import Entitat
from Classes import Objectes
from Classes import Zones
from Classes import EntityType

import os

class Mission():
    
    Name = ""
    Description = ""
    Status = "Unacceped"
    Rewards = {}
    Requisite = []
    Place = Zones.Zona
    Finished = False
    Categoria = ""


    # Metodes
    def __init__(self, name, description, rewards, cat):
        self.Name = name
        self.Description = description
        self.Rewards = rewards
        self.Categoria = cat
    
    def RequisitesCompleted(self, jugador):
        if self.Status not in ["Accepted", "Requisites", "Completed", "Rewards Unclaimed"]:
            reqcompleted = True
            if len(self.Requisite) > 0:
                for i in self.Requisite:
                    if type(i) == tuple:
                        if i[0] == "Lv":
                            if jugador.team[0].Lv < i[1]:
                                reqcompleted = False
                    elif type(i) in [Mission, FindMission, ObjectMission, KillMission, PlaceMission]:
                        if i.Status != "Completed":
                            reqcompleted = False
            if reqcompleted == True:
                self.Status = "Requisites"

    def ShowRequisites(self):
        if len(self.Requisite) > 0:
            print("-- Requisites:")
            for i in self.Requisite:
                if type(i) == tuple:
                    if i[0] == "Lv":
                        print(f"    Player Level >= {i[1]}")
                elif type(i) in [Mission, FindMission, ObjectMission, KillMission]:
                    print(f"    {i.Name} Completed")
            print("\n")


    def Aceptar(self, jugador):
        self.RequisitesCompleted(jugador)
        if self.Status == "Requisites":
            self.Status = "Accepted"
            print(f"Has aceptat {self.Name}.\n")
        else:
            print("No compleixes amb els requisits per a la missio...")
    
    def Completed(self):
        self.Status = "Rewards Unclaimed"

    def ClaimedRewards(self, jugador):
        if self.Status == "Rewards Unclaimed":
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
                        for t in jugador.team:
                            t.LvlUp(None, i[1])
            self.Finished = True
            jugador.MissionsFinalitzades.append(self)
        else:
            print("Encara no has complert la missio...")

class FindMission(Mission):
    
    Objective = ""
    
    # Metodes
    def __init__(self, name, description, cat, rewards, objective, requisite, place):
        self.Name = name
        self.Description = description
        self.Categoria = cat
        self.Rewards = rewards
        self.Objective = objective
        self.Requisite = requisite
        self.Place = place
        
    
    def Completed(self):
        self.Status = "Rewards Unclaimed"
        print(f"Has completat la missio {self.Name}.")

class ObjectMission(Mission):
    
    Objective = Objectes.ObjecteClau
    
    # Metodes
    def __init__(self, name, description, cat, rewards, objective, requisite, place):
        self.Name = name
        self.Description = description
        self.Categoria = cat
        self.Rewards = rewards
        self.Objective = objective
        self.Requisite = requisite
        self.Place = place
   
    def Completed(self):
        print(f"Has completat la missio {self.Name}.")
        self.Status = "Rewards Unclaimed"

class PlaceMission(Mission):
    
    Objective = Zones.Zona
    
    # Metodes
    def __init__(self, name, description, cat, rewards, objective, requisite):
        self.Name = name
        self.Description = description
        self.Categoria = cat
        self.Rewards = rewards
        self.Objective = objective
        self.Requisite = requisite
   
    def Completed(self):
        if self.Status == "Accepted":
            self.Status = "Rewards Unclaimed"
            print(f"\nHas completat la missio {self.Name}.")
            input("\nPresiona per a continuar...")

class KillMission(Mission):
    
    Objective = []
    Quantity = int()
    Count = 0
    Generic = True 
    # En referencia a si un enemic generat aleatori compta, en aquest acs seria si
    # si el cas es per exemple un unic enemic, que apareix no com els altres sino per que hauria d'estar alla
    # seria False i el generaria segons el que compte la clase.
    Enemic = None

    
    # Metodes
    def __init__(self, name, description, cat, rewards, qty, objective, requisite, place, generic = True, enemy = None):
        self.Name = name
        self.Description = description
        self.Categoria = cat
        self.Rewards = rewards
        self.Quantity = qty
        self.Objective = objective
        self.Requisite = requisite
        self.Place = place
        self.Generic = generic
        if self.Generic == False:
            self.Enemic = enemy

    def IncrementCount(self, enemy):
        if self.Generic == True:
            if enemy.base in self.Objective:
                self.Count += 1
            if self.Count >= self.Quantity:
                os.system("cls" if os.name == "nt" else "clear")
                self.Status = "Rewards Unclaimed"
                print(f"\nHas completat la missió {self.Name}.\n")
                input("Presiona per a continuar...")
        else:
            if enemy == self.Enemic:
                self.Status = "Rewards Unclaimed"


