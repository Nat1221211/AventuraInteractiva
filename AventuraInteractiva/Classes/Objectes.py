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
    
    def Utilitzar(self, jugador):
        for k, v in self.Effects.items():
            if k in ["HP", "Mana"]:
                if v == str and v.endswith("%"):
                    rec = int(v.replace("%", ""))
                    if jugador.StatsCombat[k] + ((jugador.StatsCombat[k] * rec) / 100) > jugador.StatsCombat[max]:
                        jugador.StatsCombat[k] = jugador.StatsCombat[max]
                        input("Has recuperat tota la vida...")
                    else:
                        recup = ((jugador.StatsCombat[k] * rec) / 100)
                        jugador.StatsCombat[k] += recup
                        input(f"Has recuperat {recup} punts de vida...")
                else:
                    cur = k
                    if k == "HP":
                        cur = "Cur" + k
                    max = "Max" + k
                    v = float(v)
                    if jugador.StatsCombat[cur] + v > jugador.StatsCombat[max]:
                        jugador.StatsCombat[cur] = jugador.StatsCombat[max]
                        input("Has recuperat tota la vida...")
                    else:
                        jugador.StatsCombat[cur] += v
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
