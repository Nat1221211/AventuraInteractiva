# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe titles.

import random

class Menu():
    def __init__(self, titol, opcions, op_per_pag):
        self.Titol = titol
        self.Opcions = opcions
        self.Cursor = 0
        self.OpcionsPagina = op_per_pag
    
    
    def MoureCursor(self, direccio):
        total = len(self.Opcions)
        self.Cursor = (self.Cursor + direccio) % total

    def SeleccionarOpcio(self):
        opcio = self.Opcions[self.Cursor]
        if opcio.Habilitat == True:
            return opcio.Nom
        return None

    def OpcionsVisible(self):
        pagina = self.Cursor // self.OpcionsPagina
        inici = pagina * self.OpcionsPagina
        fi = inici + self.OpcionsPagina
        return self.Opcions[inici:fi], inici

class OpcioMenu():
    def __init__(self, nom, habilitat, descripcio):
        self.Nom = nom
        self.Descripcio = descripcio
        self.Habilitat = habilitat

class MostrarMenu():
    def Mostrar(Menu):
        print("\n" + Menu.Titol)
        opcions, inici = Menu.OpcionsVisible()

        for i, opcio in enumerate(opcions):
            index = inici + i
            cursor = "->" if index == Menu.Cursor else "  "
            estat = "" if opcio.Habilitat == True else "(Bloquejat)"

            print(f"{cursor} {opcio.Nom} {estat}")
        
        print(f"\nDescripció: {opcions[Menu.Cursor].Descripcio}")

    