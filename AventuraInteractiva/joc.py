# Arxiu: joc.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem el programa principal del joc d'aventures per terminal.

# Llibreries
import os

from Classes import Entitat
from Classes import Player
from Classes import Events
import PrepararCridar as Call
import SaveGame
import UIManager
import CombatManager
import AdventureManager
import TownUtilitiesManager as TUtManager

from Controladors import ControladorMissions
from Controladors import ControladorExits

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

achievements = Call.CallAchievements()

missions = Call.CallMissions(Entities)

missions["Place"]["first_adventure"].Status = "Disponible"

event = Events.ControladorEvents()

event.NouEvent("Derrotar Enemic", ControladorMissions.sistemaMissionsDerrota)
event.NouEvent("Lloc Visitat", ControladorMissions.sistemaMissionsVisita)
event.NouEvent("Objecte Missio Trobat", ControladorMissions.sistemaMissionsObject)
event.NouEvent("Persona Missio Trobada", ControladorMissions.sistemaMissionsFind)
event.NouEvent("Missio Finalitzada", ControladorMissions.DesbloquejarMissio)
event.NouEvent("Nivell Incrementat",  ControladorExits.sistemaExitsStatChange)

def CrearJugador(first = False):
    nom = ""
    while nom == "":
        try:
            nom = input("Digues el nom del personatge: ")
        except ValueError:
            print("Ha ocurregut un error...")
    
    UIManager.CrearMenu(Entities.items(), "Menu Seleccio Inicial", ("Tipus Entitat", "Playable"))
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
        AdventureManager.Mapa(jugador, zones, missions, event)
    elif accio == "explorar":
        AdventureManager.Explorar(jugador, missions, Entities, event, zones, Objects, achievements)
    elif accio == "hostal":
        TUtManager.Posada(jugador)
    elif accio == "botiga":
        TUtManager.Botiga(jugador, Objects)
    elif accio == "estat":
        UIManager.VeureEstatus(jugador)
    elif accio == "missions":
        UIManager.MenuMisions(jugador, missions, event, Objects, achievements)
    elif accio == "lluitar":
        CombatManager.GenerarEnemic(Entities, jugador, event, missions, Objects, achievements)
    elif accio == "guardar":
        SaveGame.GuardarPartida(jugador, missions)
    elif accio == "exits":
        UIManager.MostrarExits(achievements, jugador)
    elif accio == "motxila":
        jugador.ObjectesMochila(Objects, False)
    elif accio == "gremi":
        # Gremi()
        print("Desactivat")

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
        TUtManager.Posada(jugador, True)
        input("Presiona per a continuar...")
        # if PostGame == False and objectes[15] in jugador.objectes.keys(): # Es pot eliminar aquest easter egg eliminant la funcio EasterEgg() i les 3 linies baix aquesta.
        #     PostGame = True   # Faria falta eliminar també el bool Easter dins el main()
        #     EasterEgg()

if __name__ == "__main__":
    main()