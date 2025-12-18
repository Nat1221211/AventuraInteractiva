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


    # Metodes
    def __init__(self, name, description, tipus, enemies, lvlrange):
        self.NameZone = name
        self.Description = description
        self.ZoneType = tipus
        self.Enemies = enemies
        self.LevelRange = lvlrange
    
    def AddConnections(self, connections):
        self.Connections = connections