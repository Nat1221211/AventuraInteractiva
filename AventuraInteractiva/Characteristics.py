# Arxiu: Moves.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe Moves.

import random

class Moves():
    
    Name = ""
    Description = ""
    Power = int()
    Precision = int()
    Type = False
    Cost = int()
    StatusEffect = ()
    
    # Metodes
    def __init__(self, name, description, power, precision, tipo, cost, efect):
        self.Name = name
        self.Description = description
        self.Power = power
        self.Precision = precision
        self.Type = tipo
        self.Cost = cost
        self.StatusEffect = efect

class Skills():
    Name = ""
    Description = ""
    Power = int()
    Precision = int()
    Type = False
    Cost = int()

    
    # Metodes
    def __init__(self, name, description, power, precision):
        self.Name = name
        self.Description = description
        self.Power = power
        self.Precision = precision