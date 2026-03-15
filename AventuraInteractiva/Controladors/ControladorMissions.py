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

def sistemaMissionsDerrota(dada, jugador, missions):
    for id in jugador.MisionsAcceptades:
        if id in missions["Kill"].keys():
            if missions["Kill"][id].Status not in ["Pendent Reclamar"]:
                if missions["Kill"][id].Generic == True:
                    if dada.base.id in missions["Kill"][id].Objective["enemy"]:
                        missions["Kill"][id].Count += 1
                else:
                    for obj in missions["Kill"][id].Objective["enemy"]:
                        if obj["entity"] == dada.base.id:
                            if obj["name"] == dada.nom:
                                if obj["level"] == dada.Lv:
                                    missions["Kill"][id].Count += 1

                if missions["Kill"][id].Count >= missions["Kill"][id].Objective["Amount"]:
                    ReclamarMissio(missions["Kill"][id])

def sistemaMissionsVisita(dada, jugador, missions):
    for id in jugador.MisionsAcceptades:
        if id in missions["Place"].keys():
            if dada == missions["Place"][id].Objective["place"]:
                ReclamarMissio(missions["Place"][id])

def sistemaMissionsObject(dada, jugador, missions):
    for id in jugador.MisionsAcceptades:
        if id in missions["Object"].keys():
            if dada == missions["Object"][id].Objective["object"]:
                ReclamarMissio(missions["Object"][id])

def sistemaMissionsFind(dada, jugador, missions):
    for id in jugador.MisionsAcceptades:
        if id in missions["Find"].keys():
            if dada == missions["Find"][id].Objective["find"]:
                ReclamarMissio(missions["Find"][id])


def ReclamarMissio(missio):
    missio.Status = "Pendent Reclamar"
    input(f"Has completat la missio {missio.Name}.\nPensa a Reclamar-la...")


def DesbloquejarMissio(dada, jugador, missions):
    for id, misions in missions.items():    # Aquest fa referencia a Kill Place, etc. els tipus de missions
        for id2, misio in misions.items():  # Aquest a cada mission en si.
            if "Mission" in misio.Requisite.keys() and dada in misio.Requisite["Mission"]:
                res = misio.MissioDesbloquejable(jugador)
                if res == True:
                    misio.Status = "Disponible"
                    jugador.MissionsDisponibles.append(id2)