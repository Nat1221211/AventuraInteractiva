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
    Magic = int()
    Attack = int()
    Intel = int()
    Defense = int()
    Speed = int()
    isPlayable = bool()
    baseXP = int()
    EntityGroup = []
    EntityMoves = {}

    # Metodes
    def __init__(self, name, playable, hp, magi, atk, intel, defs, spd, xp, group, description, moves):
        self.EntityName = name
        self.Health = hp
        self.Magic = magi
        self.Attack = atk
        self.Intel = intel
        self.Defense = defs
        self.Speed = spd
        self.isPlayable = playable
        self.baseXP = xp
        self.EntityGroup = group
        self.EntityDescription = description
        self.EntityMoves = moves