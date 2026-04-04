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
            text = opcio.nom


class OpcioMenu():
    def __init__(self,iden, nom, posicio, habilitat, descripcio, condicio_habilitat = False):
        self.id = iden
        self.Nom = nom
        self.Posicio = posicio
        self.Descripcio = descripcio
        self.Habilitat = habilitat
        if condicio_habilitat == True:
            self.Habilitat = True
