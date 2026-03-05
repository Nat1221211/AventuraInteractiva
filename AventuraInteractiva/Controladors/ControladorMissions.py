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
import joc as Joc

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

def MenuMisions():
    sel = Joc.MostrarMenus(Joc.Menus["Missions"])

    if sel == "aceptar":
        Joc.CrearMenuMissions(missions, "Aceptar Missions", Joc.jugador.MissionsDisponibles, None, 4)
        res = Joc.MostrarMenus(Joc.Menus["Aceptar Missions"])
        if res != None:
            Joc.jugador.MisionsAcceptades.append(res)
        else:
            print("Has sortit del Menu")
            input("Presiona per a continuar...")
    elif sel == "veure":
        res = Joc.MostrarMenus(Joc.Menus["Veure Missions"])
        if res == "disponibles":
            Joc.CrearMenuMissions(missions, "Missions Disponibles", Joc.jugador.MissionsDisponibles, None, 6)
            res = Joc.MostrarMenus(Joc.Menus["Missions Disponibles"], True, False, None, "", False)
        elif res == "completades":
            Joc.CrearMenuMissions(missions, "Missions Completades", Joc.jugador.MissionsFinalitzades, None, 6)
            res = Joc.MostrarMenus(Joc.Menus["Missions Completades"], True, False, None, "", False)
        elif res == "acceptades":
            Joc.CrearMenuMissions(missions, "Missions Acceptades", Joc.jugador.MisionsAcceptades, None, 6)
            res = Joc.MostrarMenus(Joc.Menus["Missions Acceptades"], True, False, None, "", False)
    
    elif sel == "reclamar":
        Joc.CrearMenuMissions(missions, "Reclamar Missions", Joc.jugador.MisionsAcceptades, "Completed", 4)
        res = Joc.MostrarMenus(Joc.Menus["Reclamar Missions"])