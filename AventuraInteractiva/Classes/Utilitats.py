# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe titles.

import random
import tkinter as tk

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
            return opcio.id
        return None

    def OpcionsVisible(self):
        pagina = self.Cursor // self.OpcionsPagina
        inici = pagina * self.OpcionsPagina
        fi = inici + self.OpcionsPagina
        totalpag = len(self.Opcions) // self.OpcionsPagina
        if (len(self.Opcions) % self.OpcionsPagina) > 0:
            totalpag += 1
        return self.Opcions[inici:fi], inici, pagina, totalpag

class OpcioMenu():
    def __init__(self,iden, nom, posicio, habilitat, descripcio, condicio_habilitat = False):
        self.id = iden
        self.Nom = nom
        self.Posicio = posicio
        self.Descripcio = descripcio
        self.Habilitat = habilitat
        if condicio_habilitat == True:
            self.Habilitat = True

class MostrarMenu():
    def Mostrar(App, Menu, textextra = ""):
        if textextra != "":
            print(f"\n{textextra}")
        print("\n" + Menu.Titol)
        opcions, inici, pagina, total = Menu.OpcionsVisible()

        App.NetejarPantalla()

        for i, opcio in enumerate(opcions):
            index = inici + i
            cursor = "->" if index == Menu.Cursor else ""
            estat = "" if opcio.Habilitat == True else "(Bloquejat)"
            objecte = tk.Button(App.root, text=opcio.Nom, 
                                    font=("Helvetica", 18), command=Menu.SeleccionarOpcio,
                                    fg="black", bg = "white"
                                    )
            posicio = opcio.Posicio
            App.canvas.create_window(App.Ancho * posicio[0], posicio[1], window=objecte)
        
        if total > 1:
            print(f"\nPagina: {pagina + 1} de {total}")

        posicio = Menu.Cursor % len(opcions)
    