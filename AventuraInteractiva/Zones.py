# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe zones.

import random

class Zona():
    
    NameZone = ""
    Description = ""
    ZoneType = ""
    Enemies = {}
    # Enemics disponibles en aquesta zona
    Connections = []
    # Zones accessibles des d'aquesta
    LevelRange = tuple()
    Trobada = False
    Or = {"": [tuple(), 100]}


    # Metodes
    def __init__(self, name, description, tipus, enemies, lvlrange, gol = {"Bronze": [(1, 7), 100]}, trobada = False):
        self.NameZone = name
        self.Description = description
        self.ZoneType = tipus
        self.Enemies = enemies
        self.LevelRange = lvlrange
        self.Or = gol
        self.Trobada = trobada
    
    def AddConnections(self, connections):
        self.Connections = connections
    
    def Trobar(self):
        self.Trobada = True