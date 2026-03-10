# Arxiu: AdventureManager.py
# Autor: Bernat Puig Casals
# Data: 10 de Març de 2026
# Descripcio:
# Creem el modul d'aventures del joc d'aventures per terminal.

# Import i Moduls
import random

import UIManager
from Classes import Missions
import CombatManager

def Mapa(jugador, zones, missions, event):
    
    UIManager.CrearMenu(jugador.Ubicacio.Connections, "Mapa", jugador, zones, None, 4)

    seleccio = UIManager.MostrarMenus(UIManager.Menus["Mapa"], True, False, None, None, f"Ubicació: {jugador.Ubicacio.NameZone}")

    if seleccio == "bloquejat":
        print("Opcio Bloquejada!")
        input("Presiona per a continuar...")
    elif seleccio != None:
        jugador.Ubicacio = zones[seleccio]    # Canviem la zona i la retornem
        jugador.ActualitzarUltimPobleVisitat()
        event.CridarEvent("Lloc Visitat", jugador.Ubicacio.id, jugador, missions)
    elif seleccio == None:
        input("Has sortit del mapa... (Presiona per a continuar)")

def OcurrenciaMisio(misio, jugador, missions, event):
    if type(misio) == Missions.KillMission:
        if misio.Enemic == 1:
            aLluitar = [misio.Enemic]
        CombatManager.Lluitar(jugador, aLluitar, event, missions)
    elif type(misio) == Missions.FindMission:
        print(f"Has trobat en/la {misio.Objective}")
        misio.Completed()
    elif type(misio) == Missions.ObjectMission:
        print(f"Has trobat l'objecte {misio.Objective.ObjectName}")
        misio.Completed()
    if type(misio) != Missions.KillMission:
        input("Presiona per a Continuar...")

def ExplorarTrobaroNo(jugador):
    
    perTrobar = len(jugador.Ubicacio.Objectes)
    if perTrobar >= 1:
        choice = random.choices(["res", "objecte"], [10, 90])
        if choice == ["objecte"]:
            objectes = list(jugador.Ubicacio.Objectes.keys())
            probabilitat = [j[0] for j in jugador.Ubicacio.Objectes.values()]
            trobat = random.choices(objectes, probabilitat)
            jugador.Ubicacio.ObjecteTrobat(trobat[0])
            print(f"Has trobat un/a {trobat[0].ObjectName}.")
            jugador.AfegirObjecte(trobat[0], 1)

    if perTrobar == 0 or choice == ["res"]:
        print("No has trobat res...")

def Explorar(jugador, missions, Entities, event, zones):

    print("Has començar a explorar...")
    prob = random.randrange(1, 100)
    choice = [""]
    if prob <= 20:  # Or
        TrobarOr(jugador)
    elif prob > 20 and prob <= 70:  # Res / Missions / Ocurrencies
        llista = []
        for i, v in missions.items():
            for id, value in v.items():
                if value.Status == "Accepted" and value.Place == jugador.Ubicacio:
                    if type(i) == Missions.KillMission:
                        if value.Generic == False:
                            llista.append(id)
                    else:
                        llista.append(id)
        if len(llista) > 0:
            choice = random.choices(["res", "missio"], [80, 20])
            if choice[0] == "missio":
                misio = random.choice(llista)
                OcurrenciaMisio(misio, jugador, missions, event)
        if len(llista) == 0 or choice == ["res"]:
            ExplorarTrobaroNo(jugador)
    elif prob > 70 and prob <= 95:  # Lluitar
        CombatManager.GenerarEnemic(Entities, jugador, event, missions)
    elif prob > 95 and prob <= 100: # Seguent ruta
        TrobarSeguentZona(jugador, zones)
        
    jugador.Ubicacio.ExplorarCount += 1
    rutaTrobada = False
    for i in jugador.Ubicacio.Connections:
        if zones[i].ZoneType == "Poble":
            if i not in jugador.LlocsTrobats:
                jugador.LlocsTrobats.append(i)
                print(f"Has trobat un cami a {zones[i].NameZone}")
                rutaTrobada = True
        else:
            if jugador.Ubicacio.ExplorarCount >= zones[i].IntentsPerTrobar and i not in jugador.LlocsTrobats:
                jugador.LlocsTrobats.append(i)
                print(f"Has trobat un cami a {zones[i].NameZone}")
                rutaTrobada = True
    if choice[0] != "missio" and prob < 70 or rutaTrobada == True:
        input("Presiona per a continuar...")
    
def TrobarSeguentZona(jugador, zones):

    posiblesRutesATrobar = []
    rutesTrobades = []
    for i in jugador.Ubicacio.Connections:
        complert = zones[i].ComprobarCondicio(jugador)
        if complert == True and i not in jugador.LlocsTrobats:
            posiblesRutesATrobar.append(i)
        if i in jugador.LlocsTrobats:
            rutesTrobades.append(i)
    if len(posiblesRutesATrobar) == 0:
        if len(rutesTrobades) == len(jugador.Ubicacio.Connections):
            print("Ja has trobat totes les rutes en aquesta zona...")
        else:
            print("No sembla haber-hi cap altre ruta...")
    else:
        trobat = random.choice(jugador.Ubicacio.Connections)
        print(f"Has trobat una ruta a {zones[trobat].NameZone}.")
        jugador.LlocsTrobats.append(trobat)
    input("Presiona per a continuar...")

    

def TrobarOr(jugador):

    mult = {"Bronze": 10, "Plata": 100, "Or": 1000, "Or Platejat": 10000}
    
    monedaTrobada = []
    
    claus = []
    weight = []
    for i in jugador.Ubicacio.Or.values():
        weight.append(i["prob"])
        claus.append(i["type"])
    if len(jugador.Ubicacio.Or.keys()) > 1:
        monedaTrobada = random.choices(claus, weights=weight)
    else:
        monedaTrobada = [claus[0]]

    found = random.randint(jugador.Ubicacio.Or[monedaTrobada[0]]["amount_range"][0], jugador.Ubicacio.Or[monedaTrobada[0]]["amount_range"][1])
    
    jugador.Gold += found * mult[monedaTrobada[0]]
    if monedaTrobada[0] in ["Bronze", "Plata"]:
        print(f"Has trobat {found} monedes de {monedaTrobada[0]}")
    else:
        print(f"Has trobat {found} monedes d'{monedaTrobada[0]}")    
