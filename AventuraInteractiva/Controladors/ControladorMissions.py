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

missions = Call.CallMissions()

def sistemaMissionsDerrota(dada, jugador):
    for id in jugador.self.MisionsAcceptades:
        if id in missions["Kill"].keys() and isinstance(dada, Entitat):
            if dada.base.id in missions["Kill"][id].Objective:
                missions["Kill"][id].Count += 1

                if missions["Kill"][id].Count >= missions["Kill"][id].Quantity:
                    ReclamarMissio(missions["Kill"][id])

def sistemaMissionsVisita(dada, jugador):
    for id in jugador.self.MisionsAcceptades:
        if id in missions["Place"].keys() and isinstance(dada, str):
            if dada in missions["Place"][id].Objective:
                ReclamarMissio(missions["Place"][id])


def ReclamarMissio(missio):
    missio.Status = "Pendent Reclamar"

