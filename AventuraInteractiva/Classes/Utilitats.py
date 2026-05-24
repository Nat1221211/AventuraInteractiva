# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe titles.

import random
import tkinter as tk
from tkinter import font as tkfont
import os
import UIManager

filepath = os.path.dirname(__file__)

class Menu():
    def __init__(self, app, canvas, ident, opcions, x = 300, y = 50, imatgeFons = None, limitfila = 10):
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
        self.espaiat_y = 0
        self.x_inicial = self.app.Ancho - x
        self.y_inicial = y
        if self.MenuAnterior != None:
            self.IndexColumna = self.MenuAnterior.IndexColumna
        else:
            self.IndexColumna = 0

        # Estats Dialeg
        self.Esciribint = False
        self.Parpadeig = None
        self.SeleccioEntitats = False
        self.PantallaEscriure = False
        self.SeguentDialeg = []

        # estats Animacio Recuperació Vida
        self.healthanimation = None


        # estats Confirmacio
        self.CaixaConfirmacio = False
        self.Confirmacio = False

    def APlicarMenuAnterior(self, menuAnterior):
        self.MenuAnterior = menuAnterior
        if self.MenuAnterior != None and isinstance(self.opcions, dict):
            self.IndexColumna = self.MenuAnterior.IndexColumna % len(self.opcions)
        else:
            self.IndexColumna = 0
        

    def dibuixar(self):
        self.canvas.delete("menu_interactiu")
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
            self.DibuixarNomZona()
        
        self.dibuixar_fons_menus()
        
    def DibuixarNomZona(self):
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
    
    def dibuixar_dialeg(self, dialeg):
        self.textdialeg = dialeg
        self.mostrat = ""
        self.canvas.delete("dialeg")
        self.Escribint = True
        self.app.DialegActiu = True

        midacuadre = 180
        if self.app.Combat == True:
            midacuadre = 150
        
        rect2 = self.canvas.create_rectangle(
            5, self.app.Alto - midacuadre,
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
        
        midacuadre = 180
        if self.app.Combat == True:
            if self.app.MenuCombat.PantallaFICombat == True:
                midacuadre = 240
            else:
                midacuadre = 150
        
        
        if index <= len(self.textdialeg):
            
            rect2 = self.canvas.create_rectangle(
                5, self.app.Alto - midacuadre,
                self.app.Ancho - 5,
                self.app.Alto - 5,
                fill="white", outline="black",
                width=4, tags="dialeg"
            )
            self.canvas.tag_raise("dialeg")
            mostrat = self.textdialeg[:index]

            y = 450
            if self.app.Combat == True:
                y = 470

            self.canvas.delete("text_animat")
            self.dialeg = self.canvas.create_text(
                30, y,
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

    def PulsarEnter(self, tecla = None):  # Funcio per a determinar que ocurreix si estem en un menu i es presiona enter...
        
        if self.Escribint == True:
            saltar = True
            if self.app.Combat == True:
                if self.app.MenuCombat.AccioAliat == True or self.app.MenuCombat.AccioAliat == True: # UpdatingHP
                    saltar = False
            
            if saltar == True:
                self.app.root.after_cancel(self.after_id)
                self.Escribint = False
                self.canvas.delete("text_animat")

                y = 450
                if self.app.Combat == True:
                    y = 470

                self.canvas.create_text(
                    30, y,
                    text=self.textdialeg, fill="black",
                    width=self.app.Ancho - 60,
                    font=("Courier", 16, "bold"),
                    anchor="nw", tags=("dialeg", "text_animat")
                )
                self.ComencarParpadeig()

        elif self.parpadeig_id != None:
            self.app.root.after_cancel(self.parpadeig_id)
            self.parpadeig_id = None
            self.app.DialegActiu = False
            if len(self.SeguentDialeg) > 0:
                for i in self.SeguentDialeg:
                    self.canvas.delete("dialeg")
                    passarDialeg = i
                    self.SeguentDialeg.remove(i)
                    self.dibuixar_dialeg(passarDialeg)
            else:
                if self.app.Confirmacio == True and self.app.Combat == False:
                    self.dibuixar()

                elif self.app.Combat == True:
                    if self.app.MenuCombat.DialegMissions == True:
                        self.app.MenuCombat.DialegMissions = False
                        self.canvas.delete("dialeg")
                    else:
                        self.canvas.delete("dialeg")
                        self.app.MenuCombat.EleccioDespresPostDialegIntern()

                else:
                    if self.id == "Confirmacio":
                        self.canvas.delete("all")
                        self.app.Enrere()

                    elif self.app.MenuMissions == True:
                        self.canvas.delete("all")
                        self.app.MostrarMenuMissions(False)
                    
                    else:
                        self.canvas.delete("all")
                        self.dibuixar()
            
    def CrearDialeg(self, text):
        if self.app.DialegActiu == True:
            self.SeguentDialeg.append(text)
        else:
            self.dibuixar_dialeg(text)

    # Crear funcio de dibuix de seleccio de personatges, amb imatge i label per al nom i descripcio, que canvii
    # sera un menu de entitats, on s'utilitzaran les imatges descripcions i mostres d'estats base

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

    def dibuixar_menu_equip(self):
        if self.app.Combat == False:
            self.canvas.delete("all")

        self.app.SeleccioAliat = True

        self.canvas.create_rectangle(
            5, 5,
            self.app.Ancho - 5, 
            self.app.Alto - 5,
            fill="black", outline="black",
            width=4, tags=("background_equip", "mostrar_equip")
        )
        self.ActualitzarEstatMenuEquip()

    def ActualitzarEstatMenuEquip(self, objecte = None, recup = None, cur = None, max = None, rec_actual = 0):
        x = 60
        y = 50

        self.app.SeleccioAliat = True

        if self.app.RecuperantVida == True:
            if rec_actual < recup:
                rec_actual += recup / 10
                if (recup / 10) + objecte.StatsCombat[cur] < objecte.StatsCombat[max]:
                    objecte.StatsCombat[cur] += recup / 10
                else:
                    objecte.StatsCombat[cur] = objecte.StatsCombat[max]
            else:
                self.app.RecuperantVida = False

        for i, ent in enumerate(self.opcions):
            color = "black"
            if i == self.index:
                color = "blue"

            if ent.id != "sortir":
                self.canvas.create_rectangle(
                x, y,
                self.app.Ancho - 120, 
                y + 130,
                fill="white", outline="grey",
                width=4, tags=("recuadre_entitat", "mostrar_equip")
                )

                ent.Objecte.ImatgeAjustada["MenuEstat"] = self.app.RedimensionarImatge(
                                        ent.Objecte.Imatges["Frontal"],
                                        75, 108, False
                                        )

                self.canvas.create_image(
                    x + 20, y + 10,
                    image=ent.Objecte.ImatgeAjustada["MenuEstat"],
                    anchor="nw",
                    tags=("ent_estat", "mostrar_estat", "mostrar_equip")
                )

                self.canvas.create_text(
                    self.app.Ancho - 670, y + 35,
                    text=f"Name: {ent.Objecte.nom}",
                    fill=color,
                    font=("Courier", 16, "bold"),
                    anchor="nw", tags=("recuadre_entitat", "stats", "mostrar_equip")
                )

                self.canvas.create_text(
                    self.app.Ancho - 670, y + 65,
                    text=f"Level: {ent.Objecte.Lv} / {ent.Objecte.LvLimit}",
                    fill="black",
                    font=("Courier", 16, "bold"),
                    anchor="nw", tags=("recuadre_entitat", "stats", "mostrar_equip")
                )
                
                self.canvas.create_text(
                    self.app.Ancho - 400, y + 35,
                    text=f"HP: {round(ent.Objecte.StatsCombat["CurHP"], 2)} / {round(ent.Objecte.StatsCombat["MaxHP"], 2)}",
                    fill="black",
                    font=("Courier", 16, "bold"),
                    anchor="nw", tags=("recuadre_entitat", "stats", "hp", "mostrar_equip")
                )

                self.canvas.create_text(
                    self.app.Ancho - 400, y + 65,
                    text=f"Mana: {round(ent.Objecte.StatsCombat["Mana"], 2)} / {round(ent.Objecte.StatsCombat["MaxMana"], 2)}",
                    fill="black",
                    font=("Courier", 16, "bold"),
                    anchor="nw", tags=("recuadre_entitat", "stats", "mana", "mostrar_equip")
                )
                
                y+= 150
            else:
                self.canvas.create_rectangle(
                760, 520,
                self.app.Ancho - 20, 
                self.app.Alto - 20,
                fill="white", outline="grey",
                width=4, tags=("recuadre_entitat", "mostrar_equip")
                )

                self.canvas.create_text(
                    780, 540,
                    text="Sortir",
                    fill=color,
                    font=("Courier", 16, "bold"),
                    anchor="nw", tags=("recuadre_entitat", "sortir", "mostrar_equip")
                )
            
        if self.app.RecuperantVida == True:
            self.healthanimation = self.app.root.after(50, lambda: self.ActualitzarEstatMenuEquip(objecte, recup, cur, max, rec_actual))
        else:
            if self.healthanimation != None:
                self.app.root.after_cancel(self.healthanimation)
                self.healthanimation = None
                self.app.SeleccioAliat = False
                if self.app.Combat == False:
                    self.app.Motxila = True
                    self.app.root.after(200, self.app.MenuMotxila())
                else:
                    self.canvas.delete("mostrar_equip")
                    self.canvas.delete("menu_motxila")
                    self.app.MenuCombat.FinalitzarTorn()
                    self.app.MenuCombat.ActualitzarBarresEstat()
                    self.app.root.after(200, self.app.MenuCombat.Lluitar())
   
    def mostrar_estat_equip(self):
        if self.app.Combat == False:
            self.canvas.delete("all")
        else:
            self.canvas.delete("mostrar_equip")

        self.app.SeleccioAliat = False
        self.app.MostrarEstat = True

        self.canvas.create_rectangle(
            5, 5,
            self.app.Ancho - 5, 
            self.app.Alto - 5,
            fill="white", outline="black",
            width=4, tags=("zona_seleccio", "mostrar_estat")
        )

    # Zones de la finestra d'estat en forma de rectangles...
        self.canvas.create_rectangle(
            self.app.Ancho - 200, 5,
            self.app.Ancho - 5, 
            self.app.Alto - 5,
            fill="white", outline="black",
            width=4, tags=("zona_seleccio", "mostrar_estat")
        )

        self.canvas.create_rectangle(
            5, 5,
            self.app.Ancho - 205, 
            self.app.Alto - 185,
            fill="white", outline="black",
            width=4, tags=("zona_estat", "mostrar_estat")
        )

        self.canvas.create_rectangle(
            5, self.app.Alto - 180,
            self.app.Ancho - 205, 
            self.app.Alto - 5,
            fill="white", outline="black",
            width=4, tags=("zona_descripcio", "mostrar_estat")
        )


        self.ActualitzarEstat()
    
    def ActualitzarEstat(self):
        self.canvas.delete("ent_estat")
 
        y = 50
        for i, opc in enumerate(self.opcions):
            if opc.id != "sortir":
                x = self.app.Ancho - 160
                if i == self.index: 
                    x -= 20
                
                opc.Objecte.ImatgeAjustada["VeureEstat"] = self.app.RedimensionarImatge(
                                            opc.Objecte.Imatges["Frontal"],
                                            100, 150, False
                                            )

                self.canvas.create_image(
                    x, y,
                    image=opc.Objecte.ImatgeAjustada["VeureEstat"],
                    anchor="nw",
                    tags=("ent_estat", "mostrar_estat")
                )
                y += 175

        self.DibuixarEstat()
    
    def DibuixarEstat(self):
        self.canvas.delete("ent_info")

        # Mostrem el nom
        self.canvas.create_text(
            30, 30,
            text=self.opcions[self.index].Objecte.nom,
            fill="black",
            font=("Courier", 28, "bold"),
            anchor="nw", tags=("ent_info", "mostrar_estat")
        )
        
        self.canvas.create_text(
                30, 70,
                text=f"Clase: {self.opcions[self.index].Objecte.base.EntityName}",
                fill="black",
                font=("Courier", 16, "bold"),
                anchor="nw", tags=("ent_info", "mostrar_estat")
            )

        text_nivell = f"Nivell: {self.opcions[self.index].Objecte.Lv} / {self.opcions[self.index].Objecte.LvLimit}"
        self.canvas.create_text(
                30, 100,
                text=text_nivell,
                fill="black",
                font=("Courier", 16, "bold"),
                anchor="nw", tags=("ent_info", "mostrar_estat")
            )
        
        text_xp = f"XP: {self.opcions[self.index].Objecte.Xp} / {self.opcions[self.index].Objecte.XpRequired}"
        self.canvas.create_text(
                30, 130,
                text=text_xp,
                fill="black",
                font=("Courier", 16, "bold"),
                anchor="nw", tags=("ent_info", "mostrar_estat")
            )

        stats_colors = ["green", "green", "blue", "blue", "red", "purple", "orange", "cyan"]
        y = 170
        for pos, stat in enumerate(self.opcions[self.index].Objecte.StatsCombat.items()):
            if stat[0] in ["MaxHP", "MaxMana"]:
                if stat[0] == "MaxHP":
                    text_mostrat = f"HP: {round(self.opcions[self.index].Objecte.StatsCombat["CurHP"], 1)} / {round(stat[1], 1)}"
                else:
                    text_mostrat = f"Mana: {round(self.opcions[self.index].Objecte.StatsCombat["Mana"], 1)} / {round(stat[1], 1)}"
            else:
                text_mostrat = f"{stat[0]}: {round(stat[1], 1)}"

            if stat[0] in ["CurHP", "Mana"]:
                continue

            self.canvas.create_text(
                30, y,
                text=text_mostrat,
                fill=stats_colors[pos],
                font=("Courier", 16, "bold"),
                anchor="nw", tags=("ent_info", "mostrar_estat")
            )
            y += 20

        # Mostrem efectes d'estat
        self.opcions[self.index].Objecte.afected
        self.canvas.create_text(
            30, self.app.Alto - 300,
            text="Efectes d'estat",
            fill="black",
            font=("Courier", 16, "bold"),
            anchor="nw", tags=("ent_info", "mostrar_estat")
        )

        y = self.app.Alto - 270
        x = 30
        for pos, i in enumerate(self.opcions[self.index].Objecte.afected):

            color = "cyan"
            if i.Debuff == True:
                color = "red"

            textShown = f"{i.Name}\nTurns: {i.Turns}"

            self.canvas.create_text(
                x, y,
                text=textShown,
                fill=color,
                font=("Courier", 16, "bold"),
                anchor="nw", tags=("ent_info", "mostrar_estat")
            )
            if (pos + 1) // 3 == 1:
                x = 30
                y += 50
            else:
                x += 200
        
        if len(self.opcions[self.index].Objecte.afected) < 1:
            self.canvas.create_text(
                x, y,
                text="Ningun",
                fill="black",
                font=("Courier", 16, "bold"),
                anchor="nw", tags=("ent_info", "mostrar_estat")
            )


        # Mostrem la descripcio
        self.canvas.create_text(
            30, self.app.Alto - 100,
            width=self.app.Ancho - 265,
            text=self.opcions[self.index].Objecte.base.EntityDescription, fill="black",
            font=("Courier", 16, "bold"),
            anchor="nw", tags=("ent_info", "mostrar_estat")
        )

        self.canvas.tag_lower("zona_descripcio")
        self.canvas.tag_lower("zona_estat")
        self.canvas.tag_raise("ent_info")

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
        if self.app.DialegActiu == True:
            self.app.root.after_cancel(self.after_id)
            self.Escribint = False
            self.canvas.delete("text_animat")
            self.canvas.create_text(
                30, 450,
                text=self.textdialeg, fill="black",
                font=("Courier", 16, "bold"),
                anchor="nw", tags=("dialeg", "text_animat")
            )
        
        if self.SeleccioEntitats == True:
            prev_ind = self.index
            if direccio == "a":
                self.index = (self.index - 1) % len(self.opcions)
            elif direccio == "d":
                self.index = (self.index + 1) % len(self.opcions)

            if prev_ind != self.index:
                self.ActualitzarImatgesSeleccio()

        elif self.app.Motxila == True:
            if direccio == "w":
                self.index = (self.index - 1) % len(self.llistaobjectes)
            elif direccio == "s":
                self.index = (self.index + 1) % len(self.llistaobjectes)
            elif direccio == "a":
                self.IndexColumna = (self.IndexColumna - 1) % len(self.opcions.keys())
            elif direccio == "d":
                self.IndexColumna = (self.IndexColumna + 1) % len(self.opcions.keys())
            self.OmplirInformacioMotxila()
        
        elif self.app.MenuMissions == True:
            if direccio == "w":
                self.index = (self.index - 1) % len(self.llistamissions)
            elif direccio == "s":
                self.index = (self.index + 1) % len(self.llistamissions)
            elif direccio == "a":
                self.IndexColumna = (self.IndexColumna - 1) % len(self.opcions.keys())
            elif direccio == "d":
                self.IndexColumna = (self.IndexColumna + 1) % len(self.opcions.keys())
            self.OmplirInformacioMissions()

        elif self.app.MenuExits == True:
            if direccio == "w":
                self.index = (self.index - 1) % len(self.llistaexits)
            elif direccio == "s":
                self.index = (self.index + 1) % len(self.llistaexits)
            elif direccio == "a":
                self.IndexColumna = (self.IndexColumna - 1) % len(self.opcions.keys())
            elif direccio == "d":
                self.IndexColumna = (self.IndexColumna + 1) % len(self.opcions.keys())
            self.OmplirInformacioExits()
            
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

            if self.app.MostrarEstat == True:
                if self.opcions[self.index].id == "sortir":
                    if direccio == "w":
                        self.index = (self.index - 1) % len(self.opcions)
                    elif direccio == "s":
                        self.index = (self.index + 1) % len(self.opcions)
                self.ActualitzarEstat()
            elif self.app.SeleccioAliat == True:
                self.dibuixar_menu_equip()
            else:
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
    
    def DibuixarMenuMotxila(self):
        if self.app.Combat == False:
            self.canvas.delete("all")
        
        # Barra SUperior on es mostraran els menus disponibles dins de la motxila
        self.canvas.create_rectangle(
            5, 5,
            self.app.Ancho - 650, 60,
            fill="white", outline="black",
            width=5, tags=("zona_nommenu", "menu_motxila")
        )

        self.canvas.create_rectangle(
            self.app.Ancho - 645, 5,
            self.app.Ancho - 5, 60,
            fill="white", outline="black",
            width=5, tags=("zona_submenus", "menu_motxila")
        )

        self.canvas.create_rectangle(
            5, 65,
            self.app.Ancho - 450,
            self.app.Alto - 190,
            fill="white", outline="black",
            width=5, tags=("zona_objectes", "menu_motxila")
        )

        self.canvas.create_rectangle(
            self.app.Ancho - 445, 65,
            self.app.Ancho - 5,
            self.app.Alto - 190,
            fill="white", outline="black",
            width=5, tags=("zona_inventari", "menu_motxila")
        )

        self.canvas.create_rectangle(
            5, self.app.Alto - 185,
            self.app.Ancho - 5,
            self.app.Alto - 45,
            fill="white", outline="black",
            width=5, tags=("zona_descripcio", "menu_motxila")
        )

        self.canvas.create_rectangle(
            5, self.app.Alto - 40,
            self.app.Ancho - 5,
            self.app.Alto - 5,
            fill="white", outline="black",
            width=5, tags=("zona_instruccions", "menu_motxila")
        )

        self.canvas.create_text(
            15, self.app.Alto - 25,
            text="Return per a Utilitzar un Objecte, <-- Per a sortir del menu, a-d per a canviar de submenu, w-s canviar d'objecte.", 
            fill="black",
            width=self.app.Ancho - 20,
            font=("Courier", 8, "bold"),
            anchor="nw", tags=("zona_instruccions", "menu_motxila", "instruccions")
        )

        y_inv = 85
        inventari = ["Informació de Grup", f"Or: {self.app.jugador.Gold}"]

        for i, inv_obj in enumerate(inventari):
            textfont = ("Courier", 16, "bold")
            if i == 0:
                textfont = ("Courier", 18, "bold")

            self.canvas.create_text(
                self.app.Ancho - 415, y_inv,
                text=inv_obj,
                fill="black",
                width=self.app.Ancho - 20,
                font= textfont,
                anchor="nw", tags=("zona_inventari", "menu_motxila", "inventari")
            )
            y_inv += 30

        self.OmplirInformacioMotxila()
    
    def OmplirInformacioMotxila(self):
        self.canvas.delete("informacio_motxila")

        x = 280
        for i, opc in enumerate(self.opcions.items()):
            color = "black"
            if i == self.IndexColumna:
                color = "blue"
                self.canvas.create_text(
                    30, 30,
                    text="Objectes " + str(opc[0]), fill="black",
                    font=("Courier", 16, "bold"),
                    anchor="w", tags=("titol_menu", "informacio_motxila", "menu_motxila")
                )

                self.llistaobjectes = opc[1]["Objectes"]

                if self.index > len(self.llistaobjectes) - 1:
                    self.index = len(self.llistaobjectes) -1
                elif len(self.llistaobjectes) == 0:
                    self.index = 0
                
                qty_mostrar = 8
                if self.index >= qty_mostrar:
                    limit_inf = self.index - (qty_mostrar)
                    limit_sup = self.index + 1
                else:
                    limit_sup = qty_mostrar + 1
                    limit_inf = 0

                y_obj = 95
                
                for j, obj in enumerate(self.llistaobjectes[limit_inf:limit_sup]):
                    color_obj = "black"
                    if self.index == self.llistaobjectes.index(obj):
                        color_obj = "blue"

                        descript = "Selecciona per a sortir de la motxila..."
                        if obj.id != "sortir":
                            descript = obj.Objecte["objecte"].ObjectDescription
                            
                        self.canvas.create_text(
                            200, self.app.Alto - 165,
                            text=descript, 
                            fill="black",
                            font=("Courier", 16, "bold"),
                            width=self.app.Ancho - 235,
                            anchor="nw", tags=("descripcio_objecte", "informacio_motxila", "menu_motxila")
                        )

                    qty = None
                    if obj.id != "sortir":
                        text = obj.Objecte["objecte"].ObjectName
                        qty = obj.Objecte["amount"]
                    else:
                        text = obj.Nom

                    self.canvas.create_text(
                        30, y_obj,
                        text=text, fill=color_obj,
                        font=("Courier", 16, "bold"),
                        anchor="nw", tags=("objecte_inventari", "informacio_motxila", "menu_motxila")
                    )
                    if qty != None:
                        self.canvas.create_text(
                        400, y_obj,
                        text=f"x{qty}", fill=color_obj,
                        font=("Courier", 16, "bold"),
                        anchor="nw", tags=("objecte_inventari", "informacio_motxila", "menu_motxila")
                    )
                    
                    y_obj += 30                

            self.canvas.create_text(
                x, 30,
                text=opc[0], fill=color,
                font=("Courier", 16, "bold"),
                anchor="w", tags=("titol_menu", "informacio_motxila", "menu_motxila")
            )

            font = tkfont.Font(family="Courier", size=16, weight="bold")

            midatext = font.measure(opc[0])
            x+=midatext + 30
    
    def CrearMenuExits(self):
        self.canvas.delete("all")
        self.app.MenuExits = True
        self.IndexColumna = 0

        self.canvas.create_rectangle(
            5, 5,
            self.app.Ancho - 5, 
            self.app.Alto - 5,
            fill="white", outline="black",
            width=5, tags=("fons_exits", "menu_exits")
        )

        self.OmplirInformacioExits()
    
    def OmplirInformacioExits(self):
        self.canvas.delete("informacio_exits")

        x = 280
        for i, opc in enumerate(self.opcions):
            color = "black"
            if i == self.IndexColumna:
                color = "blue"
                self.canvas.create_text(
                    30, 30,
                    text=str(opc) + " Exits", fill="black",
                    font=("Courier", 16, "bold"),
                    anchor="w", tags=("titol_menu", "informacio_exits", "menu_exits")
                )

                self.llistaexits = self.opcions[opc]["achievements"]

                if self.index > len(self.llistaexits) - 1:
                    self.index = len(self.llistaexits) -1
                elif len(self.llistaexits) == 0:
                    self.index = 0
                
                qty_mostrar = 8
                if self.index >= qty_mostrar:
                    limit_inf = self.index - (qty_mostrar)
                    limit_sup = self.index + 1
                else:
                    limit_sup = qty_mostrar + 1
                    limit_inf = 0

                y_obj = 95
                
                for j, exit in enumerate(self.llistaexits[limit_inf:limit_sup]):
                    color_obj = "black"
                    if self.index == self.llistaexits.index(exit):
                        color_obj = "blue"

                        descript = "Selecciona per a sortir de la finestra d'exits..."
                        if exit.id != "sortir":
                            descript = exit.Objecte.Description

                        self.canvas.create_text(
                            200, self.app.Alto - 165,
                            text=descript, 
                            fill="black",
                            width=self.app.Ancho - 235,
                            font=("Courier", 16, "bold"),
                            anchor="nw", tags=("descripcio_exit", "informacio_exits", "menu_exits")
                        )

                    if exit.id != "sortir":
                        text = exit.Objecte.Name
                    else:
                        text = exit.Nom

                    self.canvas.create_text(
                        30, y_obj,
                        text=text, fill=color_obj,
                        font=("Courier", 16, "bold"),
                        anchor="nw", tags=("exit", "informacio_exits", "menu_exits")
                    )
                    
                    y_obj += 30                

            self.canvas.create_text(
                x, 30,
                text=str(opc), fill=color,
                font=("Courier", 16, "bold"),
                anchor="w", tags=("titol_exits", "informacio_exits", "menu_exits")
            )

            font = tkfont.Font(family="Courier", size=16, weight="bold")

            midatext = font.measure(opc)
            x+=midatext + 30

    def DibuixarMenuMissions(self):
        # Barra Superior on es mostraran els menus disponibles dins de la motxila
        self.canvas.delete("all")

        self.canvas.create_rectangle(
            5, 5,
            self.app.Ancho - 580, 60,
            fill="white", outline="black",
            width=5, tags=("zona_nommenu", "menu_missions")
        )

        self.canvas.create_rectangle(
            self.app.Ancho - 575, 5,
            self.app.Ancho - 5, 60,
            fill="white", outline="black",
            width=5, tags=("zona_submenus", "menu_missions")
        )

        self.canvas.create_rectangle(
            5, 65,
            self.app.Ancho - 450,
            self.app.Alto - 190,
            fill="white", outline="black",
            width=5, tags=("zona_missions", "menu_missions")
        )

        self.canvas.create_rectangle(
            self.app.Ancho - 445, 65,
            self.app.Ancho - 5,
            self.app.Alto - 190,
            fill="white", outline="black",
            width=5, tags=("zona_informacio", "menu_missions")
        )

        self.canvas.create_rectangle(
            5, self.app.Alto - 185,
            self.app.Ancho - 5,
            self.app.Alto - 5,
            fill="white", outline="black",
            width=5, tags=("zona_descripcio", "menu_missions")
        )

        self.OmplirInformacioMissions()
    
    def OmplirInformacioMissions(self):
        self.canvas.delete("informacio_missions")

        x = 340
        for i, opc in enumerate(self.opcions.items()):
            color = "black"
            if i == self.IndexColumna:
                color = "blue"
                self.canvas.create_text(
                    30, 30,
                    text="Missions " + str(opc[0]), fill="black",
                    font=("Courier", 16, "bold"),
                    anchor="w", tags=("titol_menu", "informacio_missions", "menu_motxila")
                )

                self.llistamissions = opc[1]

                if self.index > len(self.llistamissions) - 1:
                    self.index = len(self.llistamissions) -1
                elif len(self.llistamissions) == 0:
                    self.index = 0
                
                qty_mostrar = 8
                if self.index >= qty_mostrar:
                    limit_inf = self.index - (qty_mostrar)
                    limit_sup = self.index + 1
                else:
                    limit_sup = qty_mostrar + 1
                    limit_inf = 0

                y_obj = 95
                
                for j, missio in enumerate(self.llistamissions[limit_inf:limit_sup]):
                    color_obj = "black"
                    if self.index == self.llistamissions.index(missio):
                        color_obj = "blue"

                        descript = "Selecciona per a sortir de la motxila..."
                        if missio.id != "sortir":
                            descript = missio.Objecte.Description

                            textProgres = missio.Objecte.TextProgres(self.app)

                            self.canvas.create_text(
                                self.app.Ancho - 415, 95,
                                text=textProgres, 
                                fill="black",
                                font=("Courier", 16, "bold"),
                                width=390,
                                anchor="nw", tags=("descripcio_objecte", "informacio_missions", "menu_motxila")
                            )

                            textRecompenses = missio.Objecte.MostrarRecompenses(self.app)
                            
                            self.canvas.create_text(
                                self.app.Ancho - 415, 175,
                                text=textRecompenses, 
                                fill="black",
                                font=("Courier", 16, "bold"),
                                width=390,
                                anchor="nw", tags=("descripcio_objecte", "informacio_missions", "menu_motxila")
                            )
                            
                        self.canvas.create_text(
                            200, self.app.Alto - 165,
                            text=descript,
                            fill="black",
                            font=("Courier", 16, "bold"),
                            width=self.app.Ancho - 235,
                            anchor="nw", tags=("descripcio_objecte", "informacio_missions", "menu_motxila")
                        )

                        

                    if missio.id != "sortir":
                        text = missio.Objecte.Name
                    else:
                        text = missio.Nom

                    self.canvas.create_text(
                        30, y_obj,
                        text=text, fill=color_obj,
                        font=("Courier", 16, "bold"),
                        anchor="nw", tags=("objecte_inventari", "informacio_missions", "menu_motxila")
                    )
                    
                    y_obj += 30                

            self.canvas.create_text(
                x, 30,
                text=opc[0], fill=color,
                font=("Courier", 16, "bold"),
                anchor="w", tags=("titol_menu", "informacio_missions", "menu_motxila")
            )

            font = tkfont.Font(family="Courier", size=16, weight="bold")

            midatext = font.measure(opc[0])
            x+=midatext + 30
    
    def AccioMissio(self, seleccionat):
        # Aqui decidim si aceptem, reclamem, etc... la missio.
        if seleccionat.id in self.app.jugador.MissionsDisponibles:
            self.app.jugador.MisionsAcceptades.append(seleccionat.id)
            self.app.jugador.MissionsDisponibles.remove(seleccionat.id)
            self.CrearDialeg(f"Has acceptat la missio {seleccionat.Name} !")
        
        elif seleccionat.id in self.app.jugador.MisionsAcceptades:
            if seleccionat.Reclamar(self.app) == True:
                seleccionat.dibuixar_Pantalla_Reclamar_Missio(self.app)
            else:
                print("Acceptada")
        else:
            print("Completades")
    


class OpcioMenu():
    def __init__(self,iden, nom, habilitat, descripcio, imatge = None, objecte = None, condicio_habilitat = False):
        self.id = iden
        self.Nom = nom
        self.Descripcio = descripcio
        self.Imatge = {
            "Path": imatge,
            "Carregada": None
        }
        self.Objecte = objecte
        self.Habilitat = habilitat
        if condicio_habilitat == True:
            self.Habilitat = True
