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
        self.MenuAnterior = None
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
        self.PantallaEscriure = False
    
    def dibuixar(self, x = None, y = None):
        self.canvas.delete("all")
        self.labels = []

        self.app.RedimensionarFons()

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
                color = "grey" if opcio.Habilitat != True else color

                label = self.canvas.create_text(
                    x, y + (i*40),
                    text=opcio.Nom, fill=color,
                    font=("Courier", 18, "bold"),
                    anchor="w", tags="menu_interactiu"
                )
                self.labels.append(label)
        if self.id == "Menu Poble" or self.id == "Menu Wild":

            nomZona = self.app.jugador.Ubicacio.NameZone

            self.canvas.create_text(
                30, 20,
                text=nomZona,
                anchor="nw",
                font=("Courier", 16, "bold"),
                fill="black",
                tags="text_zona"
            )

            bbox = self.canvas.bbox("text_zona")

            if bbox:
                margin = 20

                self.canvas.create_rectangle(
                    5, 
                    5, 
                    bbox[2] + margin, 
                    bbox[3] + margin - 5,
                    fill="white", outline="black",
                    width=4, tags="text_zona_fons"
                )
            self.canvas.tag_raise("text_zona")
            self.canvas.tag_lower("text_zona_fons", "menu_interactiu")
        
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
        self.canvas.tag_raise("text_zona")

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
        self.opcions[prev].Imatge["Carregada"] = self.app.RedimensionarImatge(
                                        self.opcions[prev].Imatge["Path"],
                                        200, 300, True
                                        )

        self.opcions[seg].Imatge["Carregada"] = self.app.RedimensionarImatge(
                                        self.opcions[seg].Imatge["Path"],
                                        200, 300, True
                                        )
    
        self.opcions[self.index].Imatge["Carregada"] = self.app.RedimensionarImatge(
                                        self.opcions[self.index].Imatge["Path"],
                                        200, 300
                                        )

        # Creem les imatges

        self.canvas.create_image(
            80, 220,
            image=self.opcions[prev].Imatge["Carregada"],
            tags="clase"
        )

        self.canvas.create_image(
            500, 220,
            image=self.opcions[seg].Imatge["Carregada"],
            tags="clase"
        )

        self.canvas.create_image(
            320, 250,
            image=self.opcions[self.index].Imatge["Carregada"],
            tags="clase"
        )

        self.canvas.tag_raise("clase")

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
            f"\n"
            f"HP:   {self.app.Entities[self.opcions[self.index].id].Health}\n"
            f"Mana: {self.app.Entities[self.opcions[self.index].id].Magic}\n"
            f"ATK:  {self.app.Entities[self.opcions[self.index].id].Attack}\n"
            f"INT:  {self.app.Entities[self.opcions[self.index].id].Intel}\n"
            f"DEF:  {self.app.Entities[self.opcions[self.index].id].Defense}\n"
            f"SPD:  {self.app.Entities[self.opcions[self.index].id].Speed}\n"
        )

        self.canvas.create_text(
            posicionsCaixa[0] + 40, posicionsCaixa[1] + 150,
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
            prev_ind = self.index
            if direccio == "a":
                self.index = (self.index - 1) % len(self.opcions)
            elif direccio == "d":
                self.index = (self.index + 1) % len(self.opcions)

            if prev_ind != self.index:
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
            
            while self.opcions[self.index].Habilitat != True:
                if direccio == "w":
                    self.index = (self.index - 1) % len(self.opcions)
                elif direccio == "s":
                    self.index = (self.index + 1) % len(self.opcions)

            self.dibuixar()
    
    def dibuixar_pantalla_menu_text(self, mostrar):
        self.PantallaEscriure = True
        self.canvas.delete("all")
        self.app.root.unbind("<Key>")

        self.app.RedimensionarFons()
        self.textEscrit = ""

        self.canvas.create_rectangle(
            5, 5,
            self.app.Ancho - 5,
            self.app.Alto - 5,
            fill="white", outline="black",
            width=4, tags="finestra_escriptura"
        )

        font = tkfont.Font(family="Courier", size=16, weight="bold")
        mida = font.measure(mostrar)

        self.canvas.create_text(
            self.app.Ancho // 2 - (mida // 2), 200,
            text=mostrar, fill="black",
            font=("Courier", 16, "bold"),
            anchor="w", tags="finestra_escriptura"
        )

        self.canvas.create_rectangle(
            300, 300,
            600,
            370,
            fill="white", outline="black",
            width=8, tags="finestra_escriptura"
        )

        self.MostrarText = self.canvas.create_text(
            330, 330,
            text="_", fill="black",
            font=("Courier", 16, "bold"),
            anchor="w", tags=("finestra_escriptura", "textescrit")
        )

        self.app.root.bind("<Key>", self.TeclatEscritura)
    
    def TeclatEscritura(self, tecla):
        if self.PantallaEscriure == False:
            return
    
        # Si presiona enter finalitzem el nom.
        if tecla.keysym == "Return" and len(self.textEscrit) > 0:
            self.FinalitzarEscrituraTeclat()
        
        # Borrar Lletres
        elif tecla.keysym == "BackSpace":
            self.textEscrit = self.textEscrit[:-1]
        
        # Afegir lletres
        elif len(tecla.char) == 1 and tecla.char.isalnum() and len(self.textEscrit) < 12:
            self.textEscrit += tecla.char


        self.canvas.itemconfig(self.MostrarText, text=self.textEscrit + "_")
    
    def FinalitzarEscrituraTeclat(self):
        self.PantallaEscriure = False
        self.app.root.unbind("<Key>")

        self.app.NomEntitat = self.textEscrit
        self.app.SeleccionarEntitat()


class OpcioMenu():
    def __init__(self,iden, nom, habilitat, descripcio, imatge = None, condicio_habilitat = False):
        self.id = iden
        self.Nom = nom
        self.Descripcio = descripcio
        self.Imatge = {
            "Path": imatge,
            "Carregada": None
        }
        self.Habilitat = habilitat
        if condicio_habilitat == True:
            self.Habilitat = True
