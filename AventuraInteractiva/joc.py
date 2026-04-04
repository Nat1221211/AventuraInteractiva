# Arxiu: joc.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem el programa principal del joc d'aventures per terminal.

# Llibreries
import os

import AppWindow
import SaveGame
import UIManager
import CombatManager
import AdventureManager
import TownUtilitiesManager as TUtManager


# Creem la funcio per a generar els grups d'entitats algo aixi com els tipus.
entityGroups = {""}



# Definit finestra del joc principal...
App = AppWindow.App()

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
        AdventureManager.Mapa(jugador, zones, missions, event, achievements)
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


def main():
    print("!! - Joc Interactiu - !!")

    PostGame = False
    while True:
        App.root.mainloop()
        # alive = 1
        # while alive > 0:
        #     UIManager.ClearScreen()
        #     AccioMenuPrincipal()
        #     alive = 0
        #     for i in jugador.Team.values():
        #         if i.StatsCombat["CurHP"] > 0:
        #             alive += 1
        # print(f"Has estat derrotat, t'han trobat i ara estas en la posada del ultim poble per el que has passat...")
        # jugador.Ubicacio = jugador.UltimPobleVisitat
        # TUtManager.Posada(jugador, True)
        # input("Presiona per a continuar...")
        # if PostGame == False and objectes[15] in jugador.objectes.keys(): # Es pot eliminar aquest easter egg eliminant la funcio EasterEgg() i les 3 linies baix aquesta.
        #     PostGame = True   # Faria falta eliminar també el bool Easter dins el main()
        #     EasterEgg()

if __name__ == "__main__":
    main()