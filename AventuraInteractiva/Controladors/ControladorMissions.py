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

def sistemaMissionsDerrota(dada, app):
    for id in app.jugador.MisionsAcceptades:
        if id in app.missions["Kill"].keys():
            if app.missions["Kill"][id].Status not in ["Pendent Reclamar"]:
                if app.missions["Kill"][id].Generic == True:
                    if dada.base.id in app.missions["Kill"][id].Objective["enemy"]:
                        app.missions["Kill"][id].Count += 1
                else:
                    for obj in app.missions["Kill"][id].Objective["enemy"]:
                        if obj["entity"] == dada.base.id:
                            if obj["name"] == dada.nom:
                                if obj["level"] == dada.Lv:
                                    app.missions["Kill"][id].Count += 1

                if app.missions["Kill"][id].Count >= app.missions["Kill"][id].Objective["Amount"]:
                    ReclamarMissio(app.missions["Kill"][id])

def sistemaMissionsVisita(dada, app):
    for id in app.jugador.MisionsAcceptades:
        if id in app.missions["Place"].keys():
            if dada == app.missions["Place"][id].Objective["place"]:
                ReclamarMissio(app.missions["Place"][id])

def sistemaMissionsObject(dada, app):
    for id in app.jugador.MisionsAcceptades:
        if id in app.missions["Object"].keys():
            if dada == app.missions["Object"][id].Objective["object"]:
                ReclamarMissio(app.missions["Object"][id])

def sistemaMissionsFind(dada, app):
    for id in app.jugador.MisionsAcceptades:
        if id in app.missions["Find"].keys():
            if dada == app.missions["Find"][id].Objective["find"]:
                ReclamarMissio(app.missions["Find"][id])


def ReclamarMissio(missio):
    missio.Status = "Pendent Reclamar"
    input(f"Has completat la missio {missio.Name}.\nPensa a Reclamar-la...")


def DesbloquejarMissio(dada, app):
    for id, misions in app.missions.items():    # Aquest fa referencia a Kill Place, etc. els tipus de missions
        for id2, misio in misions.items():  # Aquest a cada mission en si.
            if "Mission" in misio.Requisite.keys() and dada in misio.Requisite["Mission"]:
                res = misio.MissioDesbloquejable(app.jugador)
                if res == True:
                    misio.Status = "Disponible"
                    app.jugador.MissionsDisponibles.append(id2)