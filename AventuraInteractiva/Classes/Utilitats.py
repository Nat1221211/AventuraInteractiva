# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe titles.

import random
import tkinter as tk

class Menu():
    def __init__(self, app, canvas, opcions):
        self.app = app
        self.canvas = canvas
        self.opcions = opcions
        self.index = 0
        self.labels = []
        self.seleccionat = None
    
    def dibuixar(self, x = 100, y = 100):
        self.canvas.delete("menu_interactiu")
        self.labels = []

        for i, opcio in enumerate(self.opcions):
            color = "blue" if self.index == i else "black"
            text = opcio.Nom

            label = self.canvas.create_text(
                x, y + (i*40),
                text=text, fill=color,
                font=("Courier", 18, "bold"),
                anchor="w", tags="menu_interactiu"
            )
            self.labels.append(label)

    def Moviment(self, direccio):
        if direccio == "w":
            self.index = (self.index -1) % len(self.opcions)
        elif direccio == "s":
            self.index = (self.index +1) % len(self.opcions)
        
        self.dibuixar()
        


class OpcioMenu():
    def __init__(self,iden, nom, habilitat, descripcio, condicio_habilitat = False):
        self.id = iden
        self.Nom = nom
        self.Descripcio = descripcio
        self.Habilitat = habilitat
        if condicio_habilitat == True:
            self.Habilitat = True
