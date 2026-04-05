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
    paths = dict()
    Companions = dict()
    
    # Metodes
    def __init__(self, iden, name, playable, hp, magi, atk, intel, defs, spd, xp, group, description, moves):
        self.id = iden
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
        self.Companions = {}
        self.Images = {
            "Frontal": ""
        }
    
    def AddImages(self, images):
        self.Images = images
    
    def AddPaths(self, paths):
        self.paths = paths
    
    def AddCompanions(self, companions):
        for i in companions.items():
            self.Companions.update({i[0]: i[1]})
