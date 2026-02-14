# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe Tipus d'entitat.

import random
from Classes import Objectes

class Exits():
    
    Name = ""
    Description = ""
    Obtained = False


    # Metodes
    def __init__(self, name, description):
        self.Name = name
        self.Description = description
    
    def Obtain(self, jugador):
        self.Obtained = True
        for i in jugador.Team:
            for k in self.rewtype:
                i.DefinirPermanentStats(())
                
        if self.rewtype == "Title":
            jugador.Tituls.append(self.reward)
            print(f"Has obtingut el titol {self.reward.TitleName}.")
        

class StatusExit(Exits):

    RequisitStat = ""
    RequisitNumber = int()
    Rewards = None
    RewType = ""


    def __init__(self, name, description, RequisitStat, reqnumber, reward):
        self.Name = name
        self.Description = description
        self.RequisitStat = RequisitStat
        self.RequisitNumber = reqnumber
        self.Rewards = reward

    def Completed(self, jugador):
        for i in jugador.Team:
            if self.RequisitStat == "Lv":
                if jugador.Lv >= self.RequisitNumber:
                    self.Obtain(jugador, self.Rewards)
            elif jugador.CombatStats[self.RequisitStat] >= self.RequisitNumber:
                    self.Obtain(jugador, self.Rewards)

class ObjectExit(Exits):

    ObjectRequired = []
    Quantity = int()
    Rewards = {}

    def __init__(self, name, description, ObjectRequired, Quantity, reward):
        self.Name = name
        self.Description = description
        self.ObjectRequired = ObjectRequired
        self.Quantity = Quantity
        self.Rewards = reward
    
    def Completed(self, jugador):
        print("")

class KillExit(Exits):

    Entities = []
    Quantity = int()
    Count = int()
    Rewards = None
    RewType = ""

    def __init__(self, name, description, entities, quantity, reward):
        self.Name = name
        self.Description = description
        self.Entities = entities
        self.Quantity = quantity
        self.Rewards = reward

    def IncrementCount(self, enemy):
        if enemy.base.EntityName in self.Entities:
            self.Count += 1
    
    def Completed(self, team):
        if self.Count >= self.Quantity:
            self.Obtain(team, self.Rewards, self.RewType)