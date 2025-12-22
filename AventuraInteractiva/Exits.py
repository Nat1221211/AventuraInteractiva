# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe Tipus d'entitat.

import random
import Objectes

class Exits():
    
    Name = ""
    Description = ""
    Obtained = False


    # Metodes
    def __init__(self, name, description):
        self.Name = name
        self.Description = description
    
    def Obtain(self, jugador, reward, rewtype):
        self.Obtained = True
        if rewtype == "AllStats":
            jugador.MaxHP += reward
            jugador.ATK += reward
            jugador.DEF += reward
            jugador.SPD += reward
        elif rewtype == "HP":
            jugador.MaxHP += reward
        elif rewtype == "ATK":
            jugador.ATK += reward
        elif rewtype == "DEF":
            jugador.DEF += reward
        elif rewtype == "SPD":
            jugador.SPD += reward
        elif rewtype == "ExitBuff":
            jugador.Tituls.append(reward)
            print("")

class StatusExit(Exits):

    RequisitStat = ""
    RequisitNumber = int()
    Rewards = None
    RewType = ""


    def __init__(self, name, description, RequisitStat, reqnumber, reward, rewardtype):
        self.Name = name
        self.Description = description
        self.RequisitStat = RequisitStat
        self.RequisitNumber = reqnumber
        self.Rewards = reward
        self.RewType = rewardtype

    def Completed(self, jugador):
        if self.RequisitType == "Lv":
            if jugador.Lv >= self.RequisitNumber:
                self.Obtain(jugador, self.Rewards, self.RewType)
        elif self.RequisitType == "ATK Stat":
            if jugador.ATK >= self.RequisitNumber:
                self.Obtain(jugador, self.Rewards, self.RewType)
        elif self.RequisitType == "HP Stat":
            if jugador.MaxHP >= self.RequisitNumber:
                self.Obtain(jugador, self.Rewards, self.RewType)
        elif self.RequisitType == "DEF Stat":
            if jugador.DEF >= self.RequisitNumber:
                self.Obtain(jugador, self.Rewards, self.RewType)
        elif self.RequisitType == "SPD Stat":
            if jugador.SPD >= self.RequisitNumber:
                self.Obtain(jugador, self.Rewards, self.RewType)

class ObjectExit(Exits):

    ObjectRequired = []
    Quantity = int()
    Rewards = None
    RewType = ""

    def __init__(self, name, description, ObjectRequired, Quantity, reward, rewardtype):
        self.Name = name
        self.Description = description
        self.ObjectRequired = ObjectRequired
        self.Quantity = Quantity
        self.Rewards = reward
        self.RewType = rewardtype
    
    def Completed(self, jugador):
        print("")

class KillExit(Exits):

    Entities = []
    Quantity = int()
    Count = int()
    Rewards = None
    RewType = ""

    def __init__(self, name, description, entities, quantity, reward, rewardtype):
        self.Name = name
        self.Description = description
        self.Entities = entities
        self.Quantity = quantity
        self.Rewards = reward
        self.RewType = rewardtype

    def IncrementCount(self, enemy):
        if enemy.base in self.Entities:
            self.count += 1
    
    def Completed(self, jugador):
        if self.count >= self.Quantity:
            self.Obtain(jugador, self.Rewards, self.RewType)