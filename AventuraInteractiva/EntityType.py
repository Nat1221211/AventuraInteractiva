# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe Tipus d'entitat.

import random

class EntityType():
    
    EntityName = ""
    EntityDescription = ""
    Health = int()
    Attack = int()
    Defense = int()
    Speed = int()
    isPlayable = bool()
    baseXP = int()

    # Metodes
    def __init__(self, name, playable, hp, atk, defs, spd, xp, description):
        self.EntityName = name
        self.Health = hp
        self.Attack = atk
        self.Defense = defs
        self.Speed = spd
        self.isPlayable = playable
        self.baseXP = xp
        self.EntityDescription = description