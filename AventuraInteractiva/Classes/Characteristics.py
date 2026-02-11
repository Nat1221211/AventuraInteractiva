# Arxiu: Moves.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe Moves.

import random
import os

class Moves():
    
    Name = ""
    Description = ""
    Power = int()
    Precision = int()
    Type = False
    Cost = int()
    Buff = {}
    Debuff = {}
    MultiTarget = False
    Healing = False
    Protective = False
    AutoDamaging = 0

    # Metodes
    def __init__(self, name, description, power, precision, tipo, cost, buff, debuff, multitarget = False, healing = False, protective = False, autodamage = 0):
        self.Name = name
        self.Description = description
        self.Power = power
        self.Precision = precision
        self.Type = tipo
        self.Cost = cost
        self.Buff = buff
        self.Debuff = debuff
        self.MultiTarget = multitarget
        self.Healing = healing
        self.Protective = protective
        self.AutoDamaging = autodamage
    
    

class Effects():
    
    Name = ""
    Description = ""
    Blocking = tuple() # Si impedeix el moviment
    Turns = int() # If = 0 es permanent (posada o objecte per eliminar)
    Damage = int()  # Dany percentual num baix...
    StatEffects = tuple()   # Reduccions d'estadistiques i altres...
    RemainingTurns = 0
    
    
    # Metodes
    def __init__(self, name, description, blocking, turns, damage, statuschanges = "None"):
        self.Name = name
        self.Description = description
        self.Blocking = blocking
        self.Turns = turns
        self.Damage = damage
        self.StatEffects = statuschanges     