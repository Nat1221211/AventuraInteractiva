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

    App.root.mainloop()
        

if __name__ == "__main__":
    main()