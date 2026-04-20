# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe Tipus d'entitat.

import random

class Objecte():
    
    ObjectName = ""
    ObjectDescription = ""

    # Metodes
    def __init__(self, name, description):
        self.ObjectName = name
        self.ObjectDescription = description
    
    def Utilitzar():
        print("")

class ObjecteClau(Objecte):

    # Metodes
    def __init__(self, iden, name, description):
        self.id = iden
        self.ObjectName = name
        self.ObjectDescription = description
    
    def Utilitzar():
        print("")

class ObjecteCombat(Objecte):

    Effects = {}    # Efectes i increment d'aquests...
    Preu = int()
    OutCombat = False

    # Metodes
    def __init__(self, iden, name, description, effects, price, usableoutcombat = False):
        self.id = iden
        self.ObjectName = name
        self.ObjectDescription = description
        self.Effects = effects
        self.Preu = price
        self.OutCombat = usableoutcombat
    
    def Utilitzar(self, aliat):
        for k, v in self.Effects.items():
            if k in ["HP", "Mana"]:
                if v == str and v.endswith("%"):
                    rec = int(v.replace("%", ""))
                    if aliat.StatsCombat[k] + ((aliat.StatsCombat[k] * rec) / 100) > aliat.StatsCombat[max]:
                        aliat.StatsCombat[k] = aliat.StatsCombat[max]
                        input("Has recuperat tota la vida...")
                    else:
                        recup = ((aliat.StatsCombat[k] * rec) / 100)
                        aliat.StatsCombat[k] += recup
                        input(f"Has recuperat {recup} punts de vida...")
                else:
                    cur = k
                    if k == "HP":
                        cur = "Cur" + k
                    max = "Max" + k
                    v = float(v)
                    if aliat.StatsCombat[cur] + v > aliat.StatsCombat[max]:
                        aliat.StatsCombat[cur] = aliat.StatsCombat[max]
                        input("Has recuperat tota la vida...")
                    else:
                        aliat.StatsCombat[cur] += v
                        input(f"Has recuperat {v} punts de vida...")
            if k == "Flee":
                print("")
            if k in ["ATK","SPD","DEF","INT"]:
                print()

class ObjecteEquipment(Objecte):

    # Metodes
    def __init__(self, name, description, price, stats, effects):
        self.ObjectName = name
        self.ObjectDescription = description
        self.Preu = price
        self.Stats = {

        }
        self.Effects = {

        }
