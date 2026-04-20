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
    
    def Utilitzar(self, app, aliat):
        aliat = aliat.Objecte
        for k, v in self.Effects.items():
            if k in ["HP", "Mana"]:
                cur = k
                if k == "HP":
                    cur = "Cur" + k
                max = "Max" + k
                if isinstance(v, str) and v.endswith("%"):
                    rec = v.replace("%", "")
                    rec = int(rec)
                    if aliat.StatsCombat[cur] + ((aliat.StatsCombat[max] * rec) / 100) > aliat.StatsCombat[max]:
                        aliat.StatsCombat[cur] = aliat.StatsCombat[max]
                    else:
                        recup = ((aliat.StatsCombat[max] * rec) / 100)
                        aliat.StatsCombat[cur] += recup
                else:
                    v = float(v)
                    if aliat.StatsCombat[cur] + v > aliat.StatsCombat[max]:
                        aliat.StatsCombat[cur] = aliat.StatsCombat[max]
                    else:
                        aliat.StatsCombat[cur] += v
            if k == "Flee":
                print("")
            if k in ["ATK","SPD","DEF","INT"]:
                print()
        app.MenuMotxila()

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
