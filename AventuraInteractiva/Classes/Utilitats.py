# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe titles.

import random
import tkinter as tk

class Menu():
    def __init__(self, app, canvas, ident, opcions):
        self.app = app
        self.canvas = canvas
        self.id = ident
        self.opcions = opcions
        self.index = 0
        self.columnes = 0
        self.espaiat_x = 250
        self.espaiat_y = 40
        self.x_inicial = 250
        self.y_inicial = 250
    
    def dibuixar(self, x = None, y = None):
        self.canvas.delete("menu_interactiu")
        self.labels = []

        for i, opcio in enumerate(self.opcions):
            colum = i % self.columnes
            fila = i // self.columnes

            if x == None or y == None:
                x = self.x_inicial + (colum * self.espaiat_x)
                y = self.y_inicial + (fila * self.espaiat_y)

            color = "blue" if self.index == i else "black"

            label = self.canvas.create_text(
                x, y + (i*40),
                text=opcio.Nom, fill=color,
                font=("Courier", 18, "bold"),
                anchor="w", tags="menu_interactiu"
            )
            self.labels.append(label)

    def Moviment(self, direccio):
        if direccio == "w":
            self.index = (self.index -1) % len(self.opcions)
        elif direccio == "s":
            self.index = (self.index +1) % len(self.opcions)
        elif direccio == "a" and self.index % self.columnes != 0:
            self.index -= 1
        elif direccio == "a" and (self.index + 1) % self.columnes != 0 and self.index + 1 < len(self.opcions):
            self.index -= 1

        self.dibuixar()
        


class OpcioMenu():
    def __init__(self,iden, nom, habilitat, descripcio, condicio_habilitat = False):
        self.id = iden
        self.Nom = nom
        self.Descripcio = descripcio
        self.Habilitat = habilitat
        if condicio_habilitat == True:
            self.Habilitat = True
