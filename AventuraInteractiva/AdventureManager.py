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

def Mapa(App):
    
    UIManager.CrearMenu(App.jugador.Ubicacio.Connections, "Mapa", "Zones", App.jugador, App.Zones)
    App.CanviarMenu(UIManager.Menus["Mapa"])
    App.MostrarMenu()

def CanviarZona(App, seleccio):
    App.jugador.Ubicacio = App.Zones[seleccio.id]    # Canviem la zona i la retornem
    App.jugador.ActualitzarUltimPobleVisitat()
    App.event.CridarEvent("Lloc Visitat", App.jugador.Ubicacio.id, App.jugador, App.Missions)
    
    UIManager.MostrarMenuPrincipal(App)
    

def OcurrenciaMisio(misio, jugador, missions, event, objectes, exits):
    if type(misio) == Missions.KillMission:        
        CombatManager.Lluitar(jugador, misio.Enemic, event, missions, objectes, exits)
    elif type(misio) == Missions.FindMission:
        print(f"Has trobat en/la {misio.Objective["find"]}")
        event.CridarEvent("Persona Missio Trobada", misio.Objective["find"], jugador, missions)
    elif type(misio) == Missions.ObjectMission:
        print(f"Has trobat l'objecte {misio.Objective["ObjName"]}")
        event.CridarEvent("Objecte Missio Trobat", misio.Objective["object"], jugador, missions)
    if type(misio) != Missions.KillMission:
        input("Presiona per a Continuar...")

def ExplorarTrobaroNo(jugador, objects):
    
    perTrobar = len(jugador.Ubicacio.Objectes.keys())
    if perTrobar >= 1:
        choice = random.choices(["res", "objecte"], [10, 90])
        if choice == ["objecte"]:
            objectes = [j[1]["id"] for j in jugador.Ubicacio.Objectes.items()]
            probabilitat = [j[1]["prob"] for j in jugador.Ubicacio.Objectes.items()]
            trobat = random.choices(objectes, probabilitat)

            tipus = jugador.Ubicacio.Objectes[trobat[0]]["type"]
            identif = trobat[0]

            print(f"Has trobat un/a {objects[tipus][identif].ObjectName}.")
            jugador.AfegirObjecte(objects[tipus][identif], 1)
            jugador.Ubicacio.ObjecteTrobat(trobat[0])

    if perTrobar == 0 or choice == ["res"]:
        print("No has trobat res...")

def Explorar(jugador, missions, Entities, event, zones, objects, achievements):

    print("Has començar a explorar...")
    prob = random.randrange(1, 100)
    choice = [""]
    if prob <= 20:  # Or
        TrobarOr(jugador)
    elif prob > 20 and prob <= 70:  # Res / Missions / Ocurrencies
        llista = []
        for id in jugador.MisionsAcceptades:
            for i in missions.items():
                if id in i[1]:
                    if i[1][id].Objective["place"] == jugador.Ubicacio.id:
                        if i[0] == "Kill":
                            if i[1][id].Generic == False:
                                llista.append(i[1][id])
                        else:
                            llista.append(i[1][id])
        if len(llista) > 0:
            choice = random.choices(["res", "missio"], [10, 90])
            if choice[0] == "missio":
                misio = random.choice(llista)
                OcurrenciaMisio(misio, jugador, missions, event, objects, achievements)
        if len(llista) == 0 or choice == ["res"]:
            ExplorarTrobaroNo(jugador, objects)
    elif prob > 70 and prob <= 95:  # Lluitar
        CombatManager.GenerarEnemic(Entities, jugador, event, missions, objects, achievements)
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
