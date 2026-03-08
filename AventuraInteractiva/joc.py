# Arxiu: joc.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem el programa principal del joc d'aventures per terminal.

# Llibreries
import os
import random
import tkinter

from Classes import Objectes
from Classes import Exits
from Classes import Entitat
from Classes import EntityType
from Classes import Missions
from Classes import Titles
from Classes import Zones
from Classes import Player
from Classes import Utilitats
from Classes import Characteristics
from Classes import Events
import PrepararCridar as Call
import SaveGame
import UIManager
import CombatManager

from Controladors import ControladorMissions

Objects = Call.CallObject()
Effects = Call.CallEfect()
Movements = Call.CallMovement(Effects)
Entities = Call.CallEntity(Movements)


# Creem la funcio per a generar els grups d'entitats algo aixi com els tipus.
entityGroups = {""}

        # Zones
zones = Call.CallZones()

# # Botiga
botiga = [Objects["Combat"]["inferior_potion"],
          Objects["Combat"]["potion"],
          Objects["Combat"]["intermediate_potion"]
          ]

achievements = []

missions = Call.CallMissions()

missions["Place"]["first_adventure"].Status = "Disponible"

event = Events.ControladorEvents()

event.NouEvent("Derrotar Enemic", ControladorMissions.sistemaMissionsDerrota)
event.NouEvent("Lloc Visitat", ControladorMissions.sistemaMissionsVisita)
event.NouEvent("Missio Finalitzada", ControladorMissions.DesbloquejarMissio)





def CrearJugador(first = False):
    nom = ""
    while nom == "":
        try:
            nom = input("Digues el nom del personatge: ")
        except ValueError:
            print("Ha ocurregut un error...")
    
    UIManager.CrearMenu(Entities.items(), "Menu Seleccio Inicial")
    identifier = None
    while identifier == None:
        identifier = UIManager.MostrarMenus(UIManager.Menus["Menu Seleccio Inicial"], False)
        if identifier == None:
            print("Has de seleccionar una de les opcions")
    if first == True:
        id = "Player"
    else:
        id = f"ally_{len(jugador.Team)}"
    playableentity = Entitat.Entity(id, nom, 5, True, Entities[identifier])

    return playableentity

jugador = Player.Player

def AccioMenuPrincipal():
    global jugador
    
    print()

    # Seleccionem la accio
    if jugador.Ubicacio.ZoneType == "Poble":
        accio = UIManager.MostrarMenus(UIManager.Menus["Menu Poble"], False, False, None, None, f"Vostè es troba a {jugador.Ubicacio.NameZone}")
    elif jugador.Ubicacio.ZoneType != "Poble":
        accio = UIManager.MostrarMenus(UIManager.Menus["Menu Wild"], False, False, None, None, f"Vostè es troba a {jugador.Ubicacio.NameZone}")

    UIManager.ClearScreen()
    # Executem acció seleccionada
    if accio == "mapa":
        Mapa()
    elif accio == "explorar":
        Explorar()
    elif accio == "hostal":
        Posada()
    elif accio == "botiga":
        Botiga()
    elif accio == "estat":
        UIManager.VeureEstatus(jugador)
    elif accio == "missions":
        UIManager.MenuMisions(jugador, missions, event)
    elif accio == "lluitar":
        CombatManager.GenerarEnemic(Entities, jugador, event, missions)
    elif accio == "guardar":
        SaveGame.GuardarPartida(jugador, missions)
    elif accio == "exits":
        #MostrarExits()
        print("No actualitxat")
    elif accio == "motxila":
        jugador.ObjectesMochila(jugador.Team)
    elif accio == "gremi":
        # Gremi()
        print("Desactivat")



def PrepararBotiga(): # Afegir objectes segons nivell
    global jugador
    if jugador.Team.get(jugador.Name).Lv > 35:
        print()
    elif jugador.Team.get(jugador.Name).Lv > 20:
        print()
    elif jugador.Team.get(jugador.Name).Lv > 10:
        print()

def Botiga():
    res = -1
    while res not in (range(0, len(botiga) + 2)):
        temp = 0
        for i in botiga:
            print(f"{temp + 1} -> {i.ObjectName}")
            print(f"Preu: {i.Preu} gold\n")
            temp += 1
            if temp == len(botiga):
                print(f"{temp + 1} -> Sortir")
        res = int(input("Que vols comprar: "))
        if res not in (range(0, len(botiga) + 2)):
            print("Has de dir un dels objectes o el numero equivalent a sortir.")
    if res == len(botiga) + 1:
        print("Has sortit de la botiga...")
    else:
        qty = 0
        res = res -1
        while qty < 1:
            qty = int(input(f"\nQuants/es {botiga[res].ObjectName} vols comprar: "))
        jugador.AfegirObjecte(botiga[res], qty)
        jugador.Gold -= botiga[res].Preu * qty
        print(f"Has comprat {qty} {botiga[res].ObjectName} per {botiga[res].Preu * qty} gold !")

def Posada(free = False):
    global jugador
    res = ""
    if free == False:
        while res not in ["S", "N"]:
            UIManager.ClearScreen()
            try:
                res = input("\nVols descansar? Costa 100 gold (S / N): ").capitalize()
            except ValueError:
                print("Ha ocurregut un error...")
    if res == "S" or free == True:
        if jugador.Gold >= 100 or free == True:
            print("Has descansat comodament, t'has recuperat completament...")
            if free == False:
                jugador.Gold -= 100
            for i in jugador.Team.values():
                i.StatsCombat["CurHP"] = i.StatsCombat["MaxHP"]
                i.StatsCombat["Mana"] = i.StatsCombat["MaxMana"]
                i.afected = []
        else:
            print("No tens suficient gold per pagar la posada, has marxat sense poder descansar...")
    else:
        print("Has marxat...")

def Mapa():
    global jugador    
    
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

def OcurrenciaMisio(misio):
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

def ExplorarTrobaroNo():
    global jugador
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

def Explorar():
    global jugador
    print("Has començar a explorar...")
    prob = random.randrange(1, 100)
    choice = [""]
    if prob <= 20:  # Or
        TrobarOr(jugador.Ubicacio.Or)
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
                OcurrenciaMisio(misio)
        if len(llista) == 0 or choice == ["res"]:
            ExplorarTrobaroNo()
    elif prob > 70 and prob <= 95:  # Lluitar
        CombatManager.GenerarEnemic(Entities, jugador, event, missions)
    elif prob > 95 and prob <= 100: # Seguent ruta
        TrobarSeguentZona()
        
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
    
def TrobarSeguentZona():
    global jugador
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

    

def TrobarOr(moneda):
    global jugador
    mult = {"Bronze": 10, "Plata": 100, "Or": 1000, "Or Platejat": 10000}
    
    monedaTrobada = []
    
    claus = []
    weight = []
    for i in jugador.Ubicacio.Or.values():
        weight.append(i["prob"])
        claus.append(i["type"])
    if len(moneda.keys()) > 1:
        monedaTrobada = random.choices(claus, weights=weight)
    else:
        monedaTrobada = [claus[0]]

    found = random.randint(jugador.Ubicacio.Or[monedaTrobada[0]]["amount_range"][0], jugador.Ubicacio.Or[monedaTrobada[0]]["amount_range"][1])
    
    jugador.Gold += found * mult[monedaTrobada[0]]
    if monedaTrobada[0] in ["Bronze", "Plata"]:
        print(f"Has trobat {found} monedes de {monedaTrobada[0]}")
    else:
        print(f"Has trobat {found} monedes d'{monedaTrobada[0]}")    

def SeleccioPartida():
    global jugador
    ruta_base = os.path.dirname(__file__)
    ruta = os.path.join(ruta_base, "Saves/save.json")
    if os.path.isfile(ruta):
        res = UIManager.MostrarMenus(UIManager.Menus["Pantalla de Titol"], False)
        if res != None:
            if res == "carregar":
                ruta_partida = os.path.join(ruta_base, "Saves/save.json")
                jugador = SaveGame.CarregarPartida(ruta_partida, missions, Objects, zones, Entities)
            elif res == "nova":
                NovaPartida()
        else:
            print("Ha ocurregut un error...")
    else:
        NovaPartida()

def NovaPartida():
    # Cridem la funcio per crear el jugador, la variable ubicacio, i la variable de diccionari amb els grups i les seves entitats
    global jugador
    personatge = CrearJugador(True)
    ubicacio = zones["dawn_village"]
    team = {}
    team.update({"Player": personatge})

    jugador = Player.Player(personatge.nom, team, ubicacio)

    # # Afegim algun objecte al jugador de base
    jugador.AfegirObjecte(Objects["Combat"]["inferior_potion"], 2)

def main():
    print("!! - Joc Interactiu - !!")

    SeleccioPartida()

    PostGame = False
    while True:
        alive = 1
        while alive > 0:
            UIManager.ClearScreen()
            AccioMenuPrincipal()
            alive = 0
            for i in jugador.Team.values():
                if i.StatsCombat["CurHP"] > 0:
                    alive += 1
        print(f"Has estat derrotat, t'han trobat i ara estas en la posada del ultim poble per el que has passat...")
        jugador.Ubicacio = jugador.UltimPobleVisitat
        Posada(True)
        input("Presiona per a continuar...")
        # if PostGame == False and objectes[15] in jugador.objectes.keys(): # Es pot eliminar aquest easter egg eliminant la funcio EasterEgg() i les 3 linies baix aquesta.
        #     PostGame = True   # Faria falta eliminar també el bool Easter dins el main()
        #     EasterEgg()

if __name__ == "__main__":
    main()