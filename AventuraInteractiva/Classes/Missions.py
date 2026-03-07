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
    Status = "Bloquejada"
    Rewards = {}
    Requisite = []
    Place = Zones.Zona
    Finished = False
    Categoria = ""


    # Metodes
    def __init__(self, iden, name, description, rewards, cat):
        self.id = iden
        self.Name = name
        self.Description = description
        self.Rewards = rewards
        self.Categoria = cat

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

    def MissioDesbloquejable(self, jugador):
        resultat = True
        for key, value in self.Requisite.items():
            if key == "Lv":
                if jugador.Team["Player"].Lv < value:
                    resultat = False
            elif key == "Mission":
                for id in jugador.MissionsFinalitzades:
                    if id not in self.Requisite["Mission"]:
                        resultat = False
        
        return resultat

    def Aceptar(self, jugador):
        self.RequisitesCompleted(jugador)
        if self.Status == "Requisites":
            self.Status = "Accepted"
            print(f"Has aceptat {self.Name}.\n")
        else:
            print("No compleixes amb els requisits per a la missio...")
    
    def Reclamar(self, jugador):
        if self.Status == "Pendent Reclamar":
            for id, value in self.Rewards.items():
                if id == "XP":
                    for id, ent in jugador.Team.items():
                        ent.LvlUp(None, value)
                elif id == "Gold":
                    jugador.Gold += value
                elif id == "Objects":
                    for obj in value:
                        jugador.AfegirObjecte(obj["id"], obj["Amount"])
                elif id == "Title":
                    jugador.Titles.append(value)
            self.Status = "Completada"
            jugador.MissionsFinalitzades.append(self.id)
            jugador.MisionsAcceptades.remove(self.id)

class FindMission(Mission):
    
    Objective = ""
    
    # Metodes
    def __init__(self, iden, name, description, cat, rewards, objective, requisite):
        self.id = iden
        self.Name = name
        self.Description = description
        self.Categoria = cat
        self.Rewards = rewards
        self.Objective = objective
        self.Requisite = requisite
        
    
    def Completed(self):
        self.Status = "Rewards Unclaimed"
        print(f"Has completat la missio {self.Name}.")

class ObjectMission(Mission):
    
    Objective = Objectes.ObjecteClau
    
    # Metodes
    def __init__(self, iden, name, description, cat, rewards, objective, requisite):
        self.id = iden
        self.Name = name
        self.Description = description
        self.Categoria = cat
        self.Rewards = rewards
        self.Objective = objective
        self.Requisite = requisite
   
    def Completed(self):
        print(f"Has completat la missio {self.Name}.")
        self.Status = "Rewards Unclaimed"

class PlaceMission(Mission):
    
    Objective = Zones.Zona
    
    # Metodes
    def __init__(self, iden, name, description, cat, rewards, objective, requisite):
        self.id = iden
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
    Count = 0
    
    # Metodes
    def __init__(self, iden, name, description, cat, rewards, objective, requisite, generic = True):
        self.id = iden
        self.Name = name
        self.Description = description
        self.Categoria = cat
        self.Rewards = rewards
        self.Objective = objective
        self.Requisite = requisite
        self.Generic = generic
        self.Count = 0
        if self.Generic == False:
            for i in self.Objective:
                self.Enemic = Entitat.Entity("missions_enemy", self.Objective["entity"], self.Objective["name"],
                                             False, self.Objective["level"])

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


