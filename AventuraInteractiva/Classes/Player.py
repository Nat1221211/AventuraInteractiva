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
        for k, v in self.Team.items():
            for stat, value in self.StatIncrement.items():
                v.StatsPermanents[stat]["%"] = value["%"]
                v.StatsPermanents[stat]["Flat"] = value["Flat"]

    def AfegirObjecte(self, afegit, quantitat):
        if afegit.id in self.objectes.keys():
            self.objectes[afegit.id]["amount"] += quantitat
        else:
            self.objectes.update({afegit.id: {"objecte": afegit, "amount": quantitat}})
        UIManager.CrearMenu(self.objectes.items(), "Motxila", "Objectes")
    
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
                    if combat == True:
                        return None

            
                
        
