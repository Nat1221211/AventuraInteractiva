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
    def __init__(self, name, description):
        self.ObjectName = name
        self.ObjectDescription = description
    
    def Utilitzar():
        print("")

class ObjecteCombat(Objecte):

    Effects = {}    # Efectes i increment d'aquests...
    Preu = int()
    OutCombat = False

    # Metodes
    def __init__(self, name, description, effects, price, usableoutcombat = False):
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
                    else:
                        jugador.StatsCombat[k] += ((jugador.StatsCombat[k] * rec) / 100)
                else:
                    cur = k
                    if k == "HP":
                        cur = "Cur" + k
                    max = "Max" + k
                    if jugador.StatsCombat[cur] + v > jugador.StatsCombat[max]:
                        jugador.StatsCombat[cur] = jugador.StatsCombat[max]
                    else:
                        jugador.StatsCombat[cur] += v
            if k == "Flee":
                print("")
            if k in ["ATK","SPD","DEF","INT"]:
                print()