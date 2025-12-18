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

    TypeEffect = "" # Si afecta a curar, augment d'estadistiques, fugida, etc...
    EffectQuantity = int()  # Quantitat del efecte (curació, augment d'estadistiques, etc. La quantitat)

    # Metodes
    def __init__(self, name, description, TypeEffect, effectquantity):
        self.ObjectName = name
        self.ObjectDescription = description
        self.TypeEffect = TypeEffect
        self.EffectQuantity = effectquantity
    
    def Utilitzar(self, jugador):
        if self.TypeEffect == "Health":
            if jugador.CurHP + self.EffectQuantity > jugador.MaxHP:
                jugador.CurHP = jugador.MaxHP
            else:
                jugador.CurHP += self.EffectQuantity
        elif self.TypeEffect == "ATK":
            jugador.tempATK *= self.EffectQuantity
        elif self.TypeEffect == "SPD":
            jugador.tempSPD *= self.EffectQuantity
        elif self.TypeEffect == "DEF":
            jugador.tempDEF *= self.EffectQuantity
        elif self.TypeEffect == "Flee":
            print("")