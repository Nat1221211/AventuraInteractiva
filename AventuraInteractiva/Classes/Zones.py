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
    Or = {}
    Objectes = {}
    ExplorarCount = 0
    CondicioPerTrobarRuta = {}
    IntentsPerTrobar = 10


    # Metodes
    def __init__(self, id, name, description, tipus, enemies, gol, intents = 5):
        self.id = id
        self.NameZone = name
        self.Description = description
        self.ZoneType = tipus
        self.Enemies = enemies
        self.Or = gol
        self.CondicioPerTrobarRuta = {}
        self.IntentsPerTrobar = intents
        self.Connections = None
    
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
    
    def ComprobarCondicio(self, player):
        if self.CondicioPerTrobarRuta != None:
            trobada = True
            for j in self.CondicioPerTrobarRuta:
                if j[0] == "Ubicacio":
                    for k in j[1]:
                        if k.Trobada != True:
                            trobada = False
                if j[0] == "Objecte":
                    for v in j[1]:
                        if v not in player.objectes.keys():
                            trobada = False
                if j[0] == "Missio":
                    for m in j[1]:
                        if m.Finished != True:
                            trobada = False
            return trobada
        else:
            return True
    
    def AfegirCondicio(self, condicio):
        self.CondicioPerTrobarRuta = condicio