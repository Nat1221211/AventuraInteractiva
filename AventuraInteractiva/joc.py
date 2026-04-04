# Arxiu: joc.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem el programa principal del joc d'aventures per terminal.

# Llibreries
import os

import AppWindow

# Creem la funcio per a generar els grups d'entitats algo aixi com els tipus.
entityGroups = {""}

# Definit finestra del joc principal...
App = AppWindow.App()

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