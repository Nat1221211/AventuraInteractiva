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

    TypeEffect = [] # Si afecta a curar, augment d'estadistiques, fugida, etc...
    EffectQuantity = int()  # Quantitat del efecte (curació, augment d'estadistiques, etc. La quantitat)
    Preu = int()

    # Metodes
    def __init__(self, name, description, TypeEffect, effectquantity, price):
        self.ObjectName = name
        self.ObjectDescription = description
        self.TypeEffect = TypeEffect
        self.EffectQuantity = effectquantity
        self.Preu = price
    
    def Utilitzar(self, jugador):
        for i in self.TypeEffect:
            if i == "Health":
                if jugador.CurHP + self.EffectQuantity > jugador.MaxHP:
                    jugador.CurHP = jugador.MaxHP
                else:
                    jugador.CurHP += self.EffectQuantity
            if i == "Mana":
                if jugador.Mana + self.EffectQuantity > jugador.MaxMana:
                    jugador.Mana = jugador.MaxMana
                else:
                    jugador.Mana += self.EffectQuantity
            elif i == "Flee":
                print("")
            else:
                jugador.BuffTempStats(self.EffectQuantity, [i])