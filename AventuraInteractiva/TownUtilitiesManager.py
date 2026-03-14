# Arxiu: TownUtilitiesManager.py
# Autor: Bernat Puig Casals
# Data: 14 de Març de 2026
# Descripcio:
# Creem el modul d'utilitats dels pobles del joc d'aventures per terminal.

# Import i Moduls
import random

import UIManager
from Classes import Missions

def Botiga(jugador, objectes):
    botigues = jugador.Ubicacio.Shops
    UIManager.CrearMenu(botigues.items(), "Botigues")
    sel = UIManager.MostrarMenus(UIManager.Menus["Botigues"])
    if sel != None:
        UIManager.CrearMenuProductes(botigues[sel]["Venta"].items(), "Productes")
        prod = ""
        while prod == "":
            prod = UIManager.MostrarMenus(UIManager.Menus["Productes"])
            if prod != None:
                product = objectes[botigues[sel]["Venta"][prod]["type"]][prod]
                jugador.AfegirObjecte(product, 1)
                jugador.Gold -= botigues[sel]["Venta"][prod]["price"]


def Posada(jugador, free = False):

    if free == False:
        res = UIManager.MostrarMenus(UIManager.Menus["Posada"], False)
    if free == True or res == "si":
        if jugador.Gold >= 100 or free == True:
            print("Has descansat comodament, t'has recuperat completament...")
            if free == False:
                jugador.Gold -= 100
            for i in jugador.Team.values():
                i.Recuperacio()
        else:
            print("No tens suficient gold per pagar la posada, has marxat sense poder descansar...")
    else:
        print("Has marxat...")  
