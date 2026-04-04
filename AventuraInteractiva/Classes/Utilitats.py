# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe titles.

import random
import tkinter as tk
from tkinter import font as tkfont
import os

filepath = os.path.dirname(__file__)

class Menu():
    def __init__(self, app, canvas, ident, opcions, imatge = None, limitfila = 10):
        self.app = app
        self.canvas = canvas
        self.id = ident
        self.opcions = opcions
        self.imatge = imatge
        self.limitopcfila = limitfila
        self.index = 0
        self.columnes = len(self.opcions) // limitfila if len(self.opcions) > limitfila else 1
        self.espaiat_x = 250
        self.espaiat_y = 40
        self.x_inicial = self.app.Ancho - 300
        self.y_inicial = 50
    
    def dibuixar(self, x = None, y = None):
        self.canvas.delete("menu_interactiu")
        self.labels = []

        if self.imatge != None:
            ruta = os.path.join(filepath, self.imatge)
            self.app.RedimensionarFons(ruta)


        font = tkfont.Font(family="Courier", size=18, weight="bold")

        mides_opcions = [font.measure(opc.Nom) for i, opc in enumerate(self.opcions)]
        ample_max = max(mides_opcions) if mides_opcions else 0

        self.x_inicial = (self.app.Ancho - 40) - ample_max

        for i, opcio in enumerate(self.opcions):
            if self.columnes > 0:
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
        
        self.dibuixar_fons_menus()
    
    def dibuixar_sense_borrar(self, dialeg, index = 0):

        font = tkfont.Font(family="Courier", size=16, weight="bold")
        if index == 0:
            self.mostrat = ""

        if index < len(dialeg):  
            self.mostrat += dialeg[index]
        
        self.canvas.delete("dialeg")
        self.canvas.create_text(
            30, 450,
            text=self.mostrat, fill="black",
            font=("Courier", 16, "bold"),
            anchor="w", tags="dialeg"
        )

        if index > len(dialeg) -1 and index % 2 == 0:
            self.canvas.create_text(
            self.app.Ancho - 50, 550,
            text="<>", fill="black",
            font=("Courier", 16, "bold"),
            anchor="w", tags="dialeg"
        )

        rect2 = self.canvas.create_rectangle(
            5, 420,
            self.app.Ancho - 5,
            self.app.Alto - 5,
            fill="white", outline="black",
            width=4, tags="dialeg"
        )

        # Ordenem les coses
            # Enviem fons al final
        self.canvas.tag_lower("fons")

            # Enviem a davant del tot el tag
        self.canvas.tag_raise("dialeg")

            # Enviem rectangle sota el tag 
        self.canvas.tag_lower(rect2, "dialeg")

        # Escriure pas a pas cridant la mateixa funcio un mica mes tard
    
        self.app.root.after(50, lambda: self.dibuixar_sense_borrar(dialeg, index+1))

    
    def dibuixar_fons_menus(self):
        
        bbox = self.canvas.bbox("menu_interactiu")

        if bbox:
            margin = 25

            rect = self.canvas.create_rectangle(
                bbox[0] - margin, 
                bbox[1] - margin, 
                bbox[2] + margin, 
                bbox[3] + margin,
                fill="white", outline="black",
                width=4, tags="menu_interactiu"
            )

        # Ordenem les coses
            # Enviem fons al final
            self.canvas.tag_lower("fons")

            # Enviem a davant del tot el tag menu interactiu
            self.canvas.tag_raise("menu_interactiu")

            # Enviem rectangle sota el tag menu inetractiu
            self.canvas.tag_lower(rect, "menu_interactiu")

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
