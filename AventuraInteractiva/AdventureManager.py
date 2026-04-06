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
    

def OcurrenciaMisio(misio, app):
    if type(misio) == Missions.KillMission:        
        CombatManager.Lluitar(app.jugador, misio.Enemic, app)
    elif type(misio) == Missions.FindMission:
        app.Menu.CrearDialeg(f"Has trobat en/la {misio.Objective["find"]}")
        app.event.CridarEvent("Persona Missio Trobada", misio.Objective["find"], app.jugador, app.missions)
    elif type(misio) == Missions.ObjectMission:
        app.Menu.CrearDialeg(f"Has trobat l'objecte {misio.Objective["ObjName"]}")
        app.event.CridarEvent("Objecte Missio Trobat", misio.Objective["object"], app.jugador, app.missions)
    if type(misio) != Missions.KillMission:
        input("Presiona per a Continuar...")

def ExplorarTrobaroNo(app):
    
    perTrobar = len(app.jugador.Ubicacio.Objectes.keys())
    if perTrobar >= 1:
        choice = random.choices(["res", "objecte"], [10, 90])
        if choice == ["objecte"]:
            objectes = [j[1]["id"] for j in app.jugador.Ubicacio.Objectes.items()]
            probabilitat = [j[1]["prob"] for j in app.jugador.Ubicacio.Objectes.items()]
            trobat = random.choices(objectes, probabilitat)

            tipus = app.jugador.Ubicacio.Objectes[trobat[0]]["type"]
            identif = trobat[0]

            app.jugador.AfegirObjecte(app.Objects[tipus][identif], 1)
            app.jugador.Ubicacio.ObjecteTrobat(trobat[0])
            app.Menu.CrearDialeg(f"Has trobat {app.Objects[tipus][identif].ObjectName}.")


    if perTrobar == 0 or choice == ["res"]:
        app.Menu.CrearDialeg(f"No has trobat res...")


def Explorar(app):

    app.Menu.CrearDialeg(f"Has començat a explorar la zona...") 
    prob = random.randrange(1, 100)
    choice = [""]
    if prob <= 20:  # Or
        TrobarOr(app)
    elif prob > 20 and prob <= 70:  # Res / Missions / Ocurrencies
        llista = []
        for id in app.jugador.MisionsAcceptades:
            for i in app.missions.items():
                if id in i[1]:
                    if i[1][id].Objective["place"] == app.jugador.Ubicacio.id:
                        if i[0] == "Kill":
                            if i[1][id].Generic == False:
                                llista.append(i[1][id])
                        else:
                            llista.append(i[1][id])
        if len(llista) > 0:
            choice = random.choices(["res", "missio"], [10, 90])
            if choice[0] == "missio":
                misio = random.choice(llista)
                OcurrenciaMisio(misio, app)
        if len(llista) == 0 or choice == ["res"]:
            app.Menu.CrearDialeg(f"Has començat a buscar objectes")
            ExplorarTrobaroNo(app)
    elif prob > 70 and prob <= 95:  # Lluitar
        CombatManager.GenerarEnemic(app)
    elif prob > 95 and prob <= 100: # Seguent ruta
        TrobarSeguentZona(app)
        
    app.jugador.Ubicacio.ExplorarCount += 1
    DesbloquejarRutaPerExploracions(app)

def DesbloquejarRutaPerExploracions(app):
    rutaTrobada = False
    rutes = []
    for i in app.jugador.Ubicacio.Connections:
        if app.Zones[i].ZoneType == "Poble":
            if i not in app.jugador.LlocsTrobats:
                app.jugador.LlocsTrobats.append(i)
                rutaTrobada = True
                rutes.append(i)
        else:
            if app.jugador.Ubicacio.ExplorarCount >= app.Zones[i].IntentsPerTrobar and i not in app.jugador.LlocsTrobats:
                app.jugador.LlocsTrobats.append(i)
                rutaTrobada = True
                rutes.append(i)
        
        if rutaTrobada == True:
            if len(rutes) > 1:
                app.Menu.CrearDialeg(f"Has trobat un cami a {app.Zones[i].NameZone}.")
            else:
                app.Menu.CrearDialeg(f"Has trobat un cami a {app.Zones[i].NameZone}.")
            
def TrobarSeguentZona(app):
    posiblesRutesATrobar = []
    rutesTrobades = []
    for i in app.jugador.Ubicacio.Connections:
        complert = app.Zones[i].ComprobarCondicio(app.jugador)
        if complert == True and i not in app.jugador.LlocsTrobats:
            posiblesRutesATrobar.append(i)
        if i in app.jugador.LlocsTrobats:
            rutesTrobades.append(i)
    if len(posiblesRutesATrobar) == 0:
        app.Menu.CrearDialeg(f"No sembla haver-hi cap altre ruta per trobar...")
    else:
        trobat = random.choice(posiblesRutesATrobar)
        app.jugador.LlocsTrobats.append(trobat)
        app.Menu.CrearDialeg(f"Has trobat una ruta a {app.Zones[trobat].NameZone}")
        

    

def TrobarOr(app):

    mult = {"Bronze": 10, "Plata": 100, "Or": 1000, "Or Platejat": 10000}
    
    monedaTrobada = []
    
    claus = []
    weight = []
    for i in app.jugador.Ubicacio.Or.values():
        weight.append(i["prob"])
        claus.append(i["type"])
    if len(app.jugador.Ubicacio.Or.keys()) > 1:
        monedaTrobada = random.choices(claus, weights=weight)
    else:
        monedaTrobada = [claus[0]]

    found = random.randint(app.jugador.Ubicacio.Or[monedaTrobada[0]]["amount_range"][0], 
                           app.jugador.Ubicacio.Or[monedaTrobada[0]]["amount_range"][1])
    
    app.jugador.Gold += found * mult[monedaTrobada[0]]
    if monedaTrobada[0] in ["Bronze", "Plata"]:
        app.Menu.CrearDialeg(f"Has trobat {found} monedes de {monedaTrobada[0]}")
    else:
        app.Menu.CrearDialeg(f"Has trobat {found} monedes d'{monedaTrobada[0]}")
