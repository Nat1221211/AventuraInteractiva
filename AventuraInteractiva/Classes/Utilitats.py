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
    def __init__(self, app, canvas, ident, opcions, imatgeFons = None, limitfila = 10):
        self.app = app
        self.canvas = canvas
        self.id = ident
        self.opcions = opcions
        self.imatge = imatgeFons
        self.limitopcfila = limitfila
        self.index = 0
        self.columnes = len(self.opcions) // limitfila if len(self.opcions) > limitfila else 1
        self.espaiat_x = 250
        self.espaiat_y = 40
        self.x_inicial = self.app.Ancho - 300
        self.y_inicial = 50

        # Estats Dialeg
        self.Esciribint = False
        self.Parpadeig = None
        self.SeleccioEntitats = False
    
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
    
    def dibuixar_sense_borrar(self, dialeg):
        self.textdialeg = dialeg
        self.mostrat = ""
        self.canvas.delete("dialeg")
        self.Escribint = True
        self.app.DialegActiu = True
        
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

        self.TextAnimat(0)

    def TextAnimat(self, index):
        if not self.Escribint == True:
            return
        
        if index <= len(self.textdialeg):  
            mostrat = self.textdialeg[:index]

            self.canvas.delete("text_animat")
            self.canvas.create_text(
                30, 450,
                text=mostrat, fill="black",
                font=("Courier", 16, "bold"),
                anchor="nw", tags=("dialeg", "text_animat")
            )

            self.after_id = self.app.root.after(75, lambda: self.TextAnimat(index+1))
        else:
            self.Escribint = False
            self.ComencarParpadeig()
        
    def ComencarParpadeig(self, visible = True):
        self.canvas.delete("simbol_continuar")
        if visible:
            self.canvas.create_text(
                self.app.Ancho - 50, 550,
                text="<>", fill="blue",
                font=("Courier", 14, "bold"),
                anchor="w", tags=("dialeg", "simbol_continuar")
            )
        self.parpadeig_id = self.app.root.after(150, lambda: self.ComencarParpadeig(not visible))

    def PulsarEnter(self):  # Funcio per a determinar que ocurreix si estem en un menu i es presiona enter...
        if self.Escribint:
            self.app.root.after_cancel(self.after_id)
            self.Escribint = False
            self.canvas.delete("text_animat")
            self.canvas.create_text(
                30, 450,
                text=self.textdialeg, fill="black",
                font=("Courier", 16, "bold"),
                anchor="nw", tags=("dialeg", "text_animat")
            )
            self.ComencarParpadeig()

        elif self.parpadeig_id != None:
            self.app.root.after_cancel(self.parpadeig_id)
            self.parpadeig_id = None
            self.canvas.delete("dialeg")
            self.app.DialegActiu = False

    # Crear funcio de dibuix de seleccio de personatges, amb imatge i label per al nom i descripcio, que canvii
    # sera un menu de entitats, on s'utilitzaran les imatges descripcions i mostres d'estats base
    # Principalment per a crear el personatge, investigar com afegir per a demanar un text per al nom del jugador...
    #
    def dibuixar_menus_seleccio_entitats(self):
        # Activem que estem en el menu de seleccio d'entitats
        self.SeleccioEntitats = True

        # Borrem el que ja tinguem en el canvas
        self.canvas.delete("all")

        # Creem el fons de pantalla del menu...
        self.app.RedimensionarFons()

        self.ActualitzarImatgesSeleccio()
    
    def ActualitzarImatgesSeleccio(self):
        self.canvas.delete("clase")

        prev = (self.index - 1) % len(self.opcions)
        seg = (self.index + 1) % len(self.opcions)

        # Declarem les imatges de les opcions...
        self.opcions[prev].imatge = self.app.RedimensionarImatge(
                                        self.opcions[prev].Imatge,
                                        120, 100, True
                                        )

        self.opcions[seg].imatge = self.app.RedimensionarImatge(
                                        self.opcions[seg].Imatge,
                                        120, 100, True
                                        )
    
        self.opcions[self.index].imatge = self.app.RedimensionarImatge(
                                        self.opcions[self.index].Imatge,
                                        120, 100
                                        )

        # Creem les imatges

        self.canvas.create_image(
            150, 270,
            image=self.opcions[prev].Imatge,
            tags="clase"
        )

        self.canvas.create_image(
            300, 270,
            image=self.opcions[seg].Imatge,
            tags="clase"
        )

        self.canvas.create_image(
            450, 250,
            image=self.opcions[self.index].Imatge,
            tags="clase"
        )

        self.DibuixarInfo()
    
    def DibuixarInfo(self):
        posicionsCaixa = (600, 5)
        

        self.canvas.create_rectangle(
            posicionsCaixa[0], posicionsCaixa[1],
            self.app.Ancho - 5, 
            self.app.Alto - 185,
            fill="white", outline="black",
            width=4, tags="clase"
        )

        # Creem el recuadre de la descripcio
        self.canvas.create_rectangle(
            5, 420,
            self.app.Ancho - 5, 
            self.app.Alto - 5,
            fill="white", outline="black",
            width=4, tags="clase"
        )

        # Mostrem les estadistiques
        stats_clase = (
            f"Estadistiques Base\n"
            f"HP:   {self.app.Entities[self.opcions[self.index].id].Health}\n"
            f"Mana: {self.app.Entities[self.opcions[self.index].id].Magic}\n"
            f"ATK:  {self.app.Entities[self.opcions[self.index].id].Attack}\n"
            f"INT:  {self.app.Entities[self.opcions[self.index].id].Intel}\n"
            f"DEF:  {self.app.Entities[self.opcions[self.index].id].Defense}\n"
            f"SPD:  {self.app.Entities[self.opcions[self.index].id].Speed}\n"
        )

        self.canvas.create_text(
            posicionsCaixa[0] + 60, posicionsCaixa[1] + 150,
            text=stats_clase,
            fill="black",
            font=("Courier", 16, "bold"),
            anchor="nw", tags="clase"
        )

        # Mostrem el nom
        self.canvas.create_text(
            posicionsCaixa[0] + 30, posicionsCaixa[1] + 30,
            text=self.app.Entities[self.opcions[self.index].id].EntityName,
            fill="black",
            font=("Courier", 28, "bold"),
            anchor="nw", tags="clase"
        )

        font = tkfont.Font(family="Courier", size=18, weight="bold")


        descripcio = self.app.Entities[self.opcions[self.index].id].EntityDescription

        # Mostrem la descripcio
        self.canvas.create_text(
            30, 450,
            width=self.app.Ancho - 60,
            text=descripcio, fill="black",
            font=("Courier", 16, "bold"),
            anchor="nw", tags="clase"
        )

    


    # Crear potser algun menu especialitzat en ocupar tota la pantalla, com el de combat o el de objectes, sempre es podria
    # modificar el ja existent i donar-li possibles valors segons com fos, però crec que millor es creao un de nou...


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
        if self.SeleccioEntitats == True:
            if direccio == "a":
                self.index = (self.index - 1) % len(self.opcions)
            elif direccio == "d":
                self.index = (self.index + 1) % len(self.opcions)

            self.ActualitzarImatgesSeleccio()
        else:
            if direccio == "w":
                self.index = (self.index - 1) % len(self.opcions)
            elif direccio == "s":
                self.index = (self.index + 1) % len(self.opcions)
            elif direccio == "a" and self.index % self.columnes != 0:
                self.index -= 1
            elif direccio == "d" and (self.index + 1) % self.columnes != 0 and self.index + 1 < len(self.opcions):
                self.index -= 1

            self.dibuixar()
        


class OpcioMenu():
    def __init__(self,iden, nom, habilitat, descripcio, imatge = None, condicio_habilitat = False):
        self.id = iden
        self.Nom = nom
        self.Descripcio = descripcio
        self.Imatge = imatge
        self.Habilitat = habilitat
        if condicio_habilitat == True:
            self.Habilitat = True
