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
        objecte = aliat.Objecte
        for k, v in self.Effects.items():
            if k in ["HP", "Mana"]:
                cur = k
                if k == "HP":
                    cur = "Cur" + k
                max = "Max" + k
                if isinstance(v, str) and v.endswith("%"):
                    rec = v.replace("%", "")
                    rec = int(rec)
                    recup = ((objecte.StatsCombat[max] * rec) / 100)
                else:
                    recup = float(v)

                if objecte.StatsCombat[cur] + recup > objecte.StatsCombat[max]:
                    recup = objecte.StatsCombat[max] - objecte.StatsCombat[cur]
                
                app.RecuperantVida = True
                app.Motxila = False
                app.Menu.ActualitzarEstatMenuEquip(objecte, recup, cur, max)
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
