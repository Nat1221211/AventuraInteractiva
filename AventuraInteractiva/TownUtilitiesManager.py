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
    UIManager.CrearMenu(botigues.items(), "Botigues", "Botigues")
    sel = UIManager.MostrarMenus(UIManager.Menus["Botigues"])
    if sel != None:
        UIManager.CrearMenuProductes(botigues[sel]["Venta"].items(), "Productes")
        prod = ""
        while prod != None:
            prod = UIManager.MostrarMenus(UIManager.Menus["Productes"])
            if prod != None:
                product = objectes[botigues[sel]["Venta"][prod]["type"]][prod]
                amt = -1
                while amt != None and int(amt) < 0:
                    try:
                        amt = input("Digues quans en vols: (Enter per a sortir o enviar el numero..., 0 per a sortir)")
                        if int(amt) < 0:
                            print("Ha ocurregut un error amb el numero introduit...")
                        elif int(amt) == 0:
                            print("Has sortit del menu de compra")
                    except ValueError:
                        print("Ha ocurregut un error amb el numero introduit...")
                        if amt == "":
                            amt = None
                if amt != None:
                    amt = int(amt)
                    if amt > 0:
                        if jugador.Gold > botigues[sel]["Venta"][prod]["price"] * amt:
                            jugador.AfegirObjecte(product, amt)
                            jugador.Gold -= botigues[sel]["Venta"][prod]["price"] * amt
                            input(f"Has comprat {amt} {botigues[sel]["Venta"][prod]["name"]}.")
                        else:
                            input("No tens suficients diners per a comprar-ho...")


def CridarPosada(App):
    App.QuinaConfirmacio = "Hostal"
    App.MenuConfirmacio("Vols quedar-te a l'hostal?\nFer-ho costara 100 d'or...")

def Posada(App, free = False):
    if App.jugador.Gold >= 100 or free == True:
        App.Menu.CrearDialeg("Has descansat comodament, t'has recuperat completament...")
        if free == False:
            App.jugador.Gold -= 100
        for i in App.jugador.Team.values():
            i.Recuperacio()
    else:
         App.Menu.CrearDialeg("No tens suficient or per pagar la posada, has marxat sense poder descansar...")
