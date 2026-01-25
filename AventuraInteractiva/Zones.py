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
    ProbOfMultiple = []
    # Enemics disponibles en aquesta zona
    Connections = []
    # Zones accessibles des d'aquesta
    LevelRange = tuple()
    Trobada = False
    Or = {"": [tuple(), 100]}
    ObjectesPerTrobar = {}
    ExplorarCount = 0
    CondicioPerTrobarRuta = tuple()
    IntentsPerTrobar = 5


    # Metodes
    def __init__(self, name, description, tipus, enemies, probmultiple, lvlrange, gol = {"Bronze": [(1, 7), 100]}, trobada = False, condicio = None, intents = 5):
        self.NameZone = name
        self.Description = description
        self.ZoneType = tipus
        self.Enemies = enemies
        self.ProbOfMultiple = probmultiple
        self.LevelRange = lvlrange
        self.Or = gol
        self.Trobada = trobada
        self.CondicioPerTrobarRuta = condicio
        self.IntentsPerTrobar = intents
    
    def AddConnections(self, connections):
        self.Connections = connections
    
    def Trobar(self):
        self.Trobada = True
    
    def AfegirObjectePerTrobar(self, objectes):
        for i in objectes:  
            self.ObjectesPerTrobar[i[0]] = i[1]
            # i[0] = Objecte i[1] = llista amb prob i quantitat per trobar.
    
    def ObjecteTrobat(self, trobat):
        if self.ObjectesPerTrobar[trobat][1] >= 1:
            self.ObjectesPerTrobar[trobat][1] -= 1
            if self.ObjectesPerTrobar[trobat][1] <= 0:
                self.ObjectesPerTrobar.pop(trobat)
    
    def ComprobarCondicio(self, zones):
        print()