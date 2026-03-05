# Arxiu: PrepararCridar.py
# Autor: Bernat Puig Casals
# Data: 5 de Març de 2026
# Descripcio:
# Creem el modul per a fer accions relacionades amb les missions.

import os
import random
import tkinter

from Classes import Entitat
from Classes import EntityType
from Classes import Missions
from Classes import Titles
from Classes import Zones
from Classes import Player
from Classes import Utilitats
from Classes import Characteristics
import PrepararCridar as Call

achievements = Call.CallAchievements()

def sistemaExits(enemic, jugador):
    for id, value in achievements.items():
        if id in missions["Kill"].keys():
            if enemic.base.id in missions["Kill"][id].Objective:
                missions["Kill"][id].Count += 1

