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
    
    def MostrarRecompenses(self, app):
        text = f"Recompenses: "
        if "XP" in self.Rewards.keys():
            text += f"\n  - XP: {self.Rewards["XP"]}"
        if "Gold" in self.Rewards.keys():
            text += f"\n  - Or: {self.Rewards["Gold"]}"
        if "Objects" in self.Rewards.keys():
            text += f"\n  - Objects: "
            for object in self.Rewards["Objects"]:
                text += f"\n    + {app.Objects[object["type"]][object["id"]].ObjectName} x{object["Amount"]}"
        
        return text

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
                for id in self.Requisite["Mission"]:
                    if id not in jugador.MissionsFinalitzades:
                        resultat = False
        
        return resultat

    def Aceptar(self, jugador):
        self.RequisitesCompleted(jugador)
        if self.Status == "Requisites":
            self.Status = "Accepted"
            print(f"Has aceptat {self.Name}.\n")
        else:
            print("No compleixes amb els requisits per a la missio...")
    
    def Reclamar(self, jugador, Objectes, events, exits):
        if self.Status == "Pendent Reclamar":
            for id, value in self.Rewards.items():
                if id == "XP":
                    for id, ent in jugador.Team.items():
                        ent.LvlUp(events, jugador, exits, None, value)
                elif id == "Gold":
                    jugador.Gold += value
                elif id == "Objects":
                    for obj in value:
                        jugador.AfegirObjecte(Objectes[obj["type"]][obj["id"]], obj["Amount"])
                elif id == "Title":
                    jugador.Titles.append(value)
            self.Status = "Completada"
            jugador.MissionsFinalitzades.append(self.id)
            jugador.MisionsAcceptades.remove(self.id)
    
class FindMission(Mission):
    
    Objective = {}
    
    # Metodes
    def __init__(self, iden, name, description, cat, rewards, objective, requisite):
        self.id = iden
        self.Name = name
        self.Description = description
        self.Categoria = cat
        self.Rewards = rewards
        self.Objective = objective
        self.Requisite = requisite
    
    def TextProgres(self):

        text = f"Visitat {self.Objective["place"]}: "

        if self.Status == "Pendent Reclamar":
            text += "1 / 1"
        else:
            text += "0 / 1"

        return text


class ObjectMission(Mission):
    
    Objective = {}
    
    # Metodes
    def __init__(self, iden, name, description, cat, rewards, objective, requisite):
        self.id = iden
        self.Name = name
        self.Description = description
        self.Categoria = cat
        self.Rewards = rewards
        self.Objective = objective
        self.Requisite = requisite
    
    def TextProgres(self):

        text = f"Trobar en/la {self.Objective["place"]}: "

        if self.Status == "Pendent Reclamar":
            text += "1 / 1"
        else:
            text += "0 / 1"

        return text
  
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
    
    def TextProgres(self, app):

        text = f"Trobar {app.Zones[self.Objective["place"]].NameZone}: "

        if self.Status == "Pendent Reclamar":
            text += "1 / 1"
        else:
            text += "0 / 1"
        
        return text


class KillMission(Mission):
    
    Objective = []
    Count = 0
    
    # Metodes
    def __init__(self, iden, name, description, cat, rewards, objective, requisite, generic = True, entitats = None):
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
            self.Enemic = {}
            count = 0
            for j in self.Objective["enemy"]:
                self.Enemic.update({
                    f"missions_enemy_{count}":
                    Entitat.Entity(f"missions_enemy_{count}", j["name"],
                                    j["level"], False, entitats[j["entity"]])
                })
                count += 1

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
        
    def TextProgres(self, app):

        if self.Generic == True:
            nom_entitat = app.Enemies[self.Objective["enemy"][0]].EntityName
        else:
            nom_entitat = app.Enemies[self.Objective["enemy"][0]["name"]]

        text = f"Derrotar {nom_entitat}: "

        text += f"{self.Count} / {self.Objectiu["Amount"]}"

        return text