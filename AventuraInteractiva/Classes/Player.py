# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe titles.

import os
import PrepararCridar as Call
from Classes import Objectes

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
            self.objectes[afegit] += quantitat
        else:
            self.objectes[afegit]=quantitat
    
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

    def ObjectesMochila(self, team, target = None, combat = bool(False)):
            res = 0
            if combat == True:
                used = False
            while res != 3:
                res = 0
                while res not in [1, 2, 3]:
                    os.system("cls")
                    print("1 -> Veure")
                    print("2 -> Utilitzar")
                    print("3 -> Sortir")
                    try:
                        res = int(input("\nQue vols fer: "))
                        if res not in [1, 2, 3]:
                            print("Has de dir un dels 3 numeros...")
                    except ValueError:
                        print("Ha ocurregut un error...")
                if res == 1:
                    os.system("cls")
                    self.MostrarObjectes()
                    input("Presiona per a continuar...")
                if res == 2:
                    obj = -2
                    objectNames = list(self.objectes.keys())
                    while obj not in range(1, len(objectNames) + 1) and obj != 0:
                        try:
                            os.system("cls")
                            ind = 1
                            for i in objectNames:
                                print(f"{ind} - > {i.ObjectName}")
                                ind += 1
                            print("Per a sortir de la seleccio escriu 0.")
                            obj = int(input("\nQuin objecte vols utilitzar: "))
                            if obj not in range(1, len(objectNames) + 1) and obj != 0:
                                print("\nHas de dir un dels objectes... o escriure 0")
                        except ValueError:
                            print("\nHa ocurregut un error...")
                            input("\nPresiona per a continuar...")
                    if obj != 0:
                        if type(objectNames[obj - 1]) != Objectes.ObjecteClau:
                            if objectNames[obj - 1].OutCombat == False and combat == False:
                                print("Aquest objecte només es pot utilitzar en combat...")
                                input("Presiona per a continuar...")
                            else:
                                utilitzat = True
                                if target == None:
                                    res = 0
                                    while res not in range(1, len(team) + 2):
                                        os.system("cls" if os.name == "nt" else "clear")
                                        targetable = []
                                        for i in team.values():
                                            if i.StatsCombat["CurHP"] > 0:
                                                targetable.append(i)
                                        count = 1
                                        for i in targetable:
                                            print(f"{count} -> {i.nom}, Lv: {i.Lv}")
                                            count += 1
                                        print(f"{count} -> Sortir")
                                        try:
                                            res = int(input("Digues de a qui vols atacar: "))
                                            if res not in range(1, count + 1):
                                                print("Has de dir un dels numeros corresponents...")
                                        except ValueError:
                                            print("Ha ocurregut un error...")
                                            input("Presiona per a continuar...")
                                    if res in range(1, count):
                                        target = targetable[res - 1]
                                    if res == count:
                                        print("Has deixat d'utilitzar aquest objecte...")
                                        utilitzat = False
                                if utilitzat == True:
                                    objectNames[obj - 1].Utilitzar(target)
                                    self.objectes[objectNames[obj - 1]]-= 1
                                    print(f"Has utilitzat: {objectNames[obj - 1].ObjectName}")
                                    if combat == True:
                                        used = True
                                        res = 3
                                    if self.objectes[objectNames[obj - 1]] <= 0:
                                        self.objectes.pop(objectNames[obj - 1])
                        else:
                            print("Els objectes clau no es poden utilitzar, son objectes de missio o amb altres finalitats...")
                            input("Presiona per a continuar")
                    else:
                        print("Has sortit del menu d'utilització.")
            if combat == True:
                return used
            
                
        
