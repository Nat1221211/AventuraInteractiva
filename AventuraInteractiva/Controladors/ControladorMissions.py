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
        if id in app.Missions["Kill"].keys():
            if app.Missions["Kill"][id].Status not in ["Pendent Reclamar"]:
                if app.Missions["Kill"][id].Generic == True:
                    if dada.base.id in app.Missions["Kill"][id].Objective["enemy"]:
                        app.Missions["Kill"][id].Count += 1
                else:
                    for obj in app.Missions["Kill"][id].Objective["enemy"]:
                        if obj["entity"] == dada.base.id:
                            if obj["name"] == dada.nom:
                                if obj["level"] == dada.Lv:
                                    app.Missions["Kill"][id].Count += 1

                if app.Missions["Kill"][id].Count >= app.Missions["Kill"][id].Objective["Amount"]:
                    ReclamarMissio(app.Missions["Kill"][id], app)

def sistemaMissionsVisita(dada, app):
    for id in app.jugador.MisionsAcceptades:
        if id in app.Missions["Place"].keys():
            if dada == app.Missions["Place"][id].Objective["place"]:
                ReclamarMissio(app.Missions["Place"][id], app)

def sistemaMissionsObject(dada, app):
    for id in app.jugador.MisionsAcceptades:
        if id in app.Missions["Object"].keys():
            if dada == app.Missions["Object"][id].Objective["object"]:
                ReclamarMissio(app.Missions["Object"][id], app)

def sistemaMissionsFind(dada, app):
    for id in app.jugador.MisionsAcceptades:
        if id in app.Missions["Find"].keys():
            if dada == app.Missions["Find"][id].Objective["find"]:
                ReclamarMissio(app.Missions["Find"][id], app)


def ReclamarMissio(missio, app):
    missio.Status = "Pendent Reclamar"
    app.Menu.CrearDialeg(f"Has completat la missio {missio.Name}.\nPensa a Reclamar-la...")


def DesbloquejarMissio(dada, app):
    for id, misions in app.Missions.items():    # Aquest fa referencia a Kill Place, etc. els tipus de missions
        for id2, misio in misions.items():  # Aquest a cada mission en si.
            if "Mission" in misio.Requisite.keys() and dada.id in misio.Requisite["Mission"]:
                res = misio.MissioDesbloquejable(app.jugador)
                if res == True:
                    misio.Status = "Disponible"
                    app.jugador.MissionsDisponibles.append(id2)