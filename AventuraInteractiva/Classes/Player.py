# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe titles.

import os
import PrepararCridar as Call
from Classes import Objectes
import UIManager
import CombatManager

class Player():
        
    # Metodes
    def __init__(self, name, team, place):
        self.Name = name
        self.Team = team
        self.Ubicacio = place 
        self.Gold = 2000

        # Seguiment
        self.AcquiredAchievements = []  # En aquests tres s'indicara l'id o nom de la misio dins del csv corresponent.
        self.MisionsAcceptades = []
        self.MissionsFinalitzades = []
        self.MissionsDisponibles = ["first_adventure"]
        self.LlocsTrobats = ["dawn_village", "south_forest"]
        self.LlocsVisitats = ["dawn_village"]

        # Objectes i Altres
        self.objectes = {} # Diccionari, objecte(nom/id en csv) = clau i quantitat = valor
        self.UltimPobleVisitat = self.Ubicacio
        self.PostGame = False
        self.Companys = {}
        self.Titles = []

        self.Estadistiques = {  # Estadistiques Generiques, hem refereixio a missionsCompletades, enemics derrotats etc...
            "": 0,

        }

        self.StatIncrement = {
            "MaxHP": {"%": int(), "Flat": int()},
            "MaxMana": {"%": int(), "Flat": int()},
            "ATK": {"%": int(), "Flat": int()},
            "INT": {"%": int(), "Flat": int()},
            "DEF": {"%": int(), "Flat": int()},
            "SPD": {"%": int(), "Flat": int()},
        }

        self.fleeProb = 75
    
    def AplicarStatsGenerals(self):
        for i in self.Team:
            for j in self.StatIncrement.items():
                i.StatPermanent[j[0]]["%"] = j[1]["%"]
                i.StatPermanent[j[0]]["Flat"] = j[1]["Flat"]
            i.DefinirPermanentStats()

    def AfegirObjecte(self, afegit, quantitat):
        if afegit in self.objectes:
            self.objectes[afegit.id]["amount"] += quantitat
        else:
            self.objectes[afegit.id].update({"objecte": afegit, "amount": quantitat})
        UIManager.CrearMenu(self.objectes.items(), "Motxila", "Objectes",opcionsvisibles=6)
    
    def ActualitzarUltimPobleVisitat(self):
        if self.Ubicacio.ZoneType == "Poble":
            self.UltimPobleVisitat = self.Ubicacio
        self.LlocsVisitats.append(self.Ubicacio.NameZone)

    def MostrarObjectes(self):
        os.system("cls")
        for i in self.objectes.items():
            print(f"{i[0].ObjectName}, Qty: {i[1]}")
            print(f"{i[0].ObjectDescription}")
            print("\n")

    def ObjectesMochila(self, objectes, combat = False):
            obj = ""
            while obj != None:
                obj = UIManager.MostrarMenus(UIManager.Menus["Motxila"])
                if obj != None:
                    objecte = objectes[obj["type"]][obj["id"]]
                    if combat == False:
                        obj = CombatManager.UseObject(self, self.Team, objecte)
                    else:
                        return objecte
                else:
                    input("Has sortit de la motxila...")

            
                
        
