# Arxiu: PrepararCridar.py
# Autor: Bernat Puig Casals
# Data: 7 de Març de 2026
# Descripcio:
# Creem el modul per a guardar i carregar la partida.

import csv
import json
import os
import random

import tkinter as Tk
from tkinter import font as tkfont
import UIManager


# Importar Classes
from Classes import Entitat
import UIManager

def StartCombat(app, canvas, ident, misio = False, enemic = None):
    app.Combat = True
    app.MenuCombat = MenuCombat(app, canvas, ident)
    if misio == False:
        app.MenuCombat.GenerarEnemic()
    else:
        app.MenuCombat.CarregarEnemic(enemic)
        app.MenuCombat.dibuixar_combat()


class OpcionsCombat():
    def __init__(self, ident, nom, habilitat, descript, moviment = None):
        self.id = ident
        self.Nom = nom
        self.Descripcio = descript
        self.Habilitat = habilitat
        self.Moviment = moviment

class MenuCombat():
    def __init__(self, app, canvas, ident):
        
        # Obligatoris
        self.app = app
        self.canvas = canvas
        self.id = ident
        self.equip = self.app.jugador.Team
        self.enemic = {}
        self.Recompenses = {
            "XP": {
            },
            "Objects": {},
        }


        # Llistat de derrotats
        self.EnemicsDerrotats = {}
        self.AliatsDerrotats = {}
        
        # Lllistes permanents, probablement només aquesta...
        self.IndexAccio = 0
        self.AccionsCombat = [
            OpcionsCombat("atacar", "Atacar", True, ""),
            OpcionsCombat("motxila", "Motxila", True, ""),
            OpcionsCombat("estat", "Veure Estat", True, ""),
            OpcionsCombat("fugir", "Fugir", True, ""),
            OpcionsCombat("pasar", "Pasar Torn", True, "")
        ]

        self.IndexMoviment = 0
        self.IndexObjectiu = 0

        # Estats, seran booleanes.
        self.AccioAliat = False
        self.AccioEnemic = False
        self.DialegActiu = False
        self.Atacar = False
        self.PassarTorn = False
        self.MenuAccioAliat = False
        self.PantallaFICombat = False
        self.Derrotat = False
        self.AccioFugirEstat = False
        self.levelingUp = False
        self.saltarPantallaFi = False
        self.CombatAcabat = False
        self.levelAnimation = None
        self.UpdatingHP = False
        self.UpdateHPAnimation = None
        self.ComprobarEfectes = False
        self.SeleccionarObjectiu = False
        self.AtacARealitzar = None
        self.AnimacioSeleccioObjectiu = None
        self.ObjectiuMoviment = None
        self.GrupObjectiuMoviment = ""

        self.Fugir = [False]
        self.combat = False

        # Altres variables necessaries
        self.AtacantAliat = None
        self.AtacantEnemic = None
        self.MovimentsAliat = []


    def CridarMenuSegonsAccio(self, accio):
        self.MenuAccioAliat = False

        self.canvas.delete("seleccio_accio_aliat")

        AccionsDisponibles={
            "atacar": lambda: self.dibuixar_seleccio_Moviment(),
            "motxila": lambda: self.app.MenuMotxila(),
            "estat": lambda: UIManager.VeureEstatus(self.app),
            "fugir": lambda: self.AccioFugir(),
            "pasar": lambda: self.AccioPasarTorn()
        }
        if accio.id in AccionsDisponibles:
            AccionsDisponibles[accio.id]()
    
    def CarregarEnemic(self, enemic):
        self.enemic = enemic
    
    def dibuixar_combat(self):
        self.canvas.delete("all")
        self.app.RedimensionarFons()

        # Preparacions Inicials del COmbat
        self.PrepararPerCombat()
        self.teamderr = 0
        self.enemyderr = 0
            
        self.fugir = [False]
        self.combat = True

        # Començem el combat
        self.dibuixar_entitats()

        self.canvas.create_rectangle(
            5, self.app.Alto - 150,
            self.app.Ancho - 5, 
            self.app.Alto - 5,
            fill="white", outline="black",
            width=5, tags=("zona_info", "combat")
        )

        self.dibuixar_recuadres_informacio()
        self.PrioritatInicial()

    def dibuixar_recuadres_informacio(self):
        self.canvas.create_rectangle(
            5, 5,
            self.app.Ancho - 5, 
            60,
            fill="white", outline="black",
            width=5, tags=("zona_accio", "combat")
        )

        self.canvas.create_rectangle(
            40, 15,
            self.app.Ancho - 40, 
            20,
            fill="black", outline="black",
            width=5, tags=("barra_accio", "zona_accio", "combat")
        )

        self.canvas.create_text(
            30, 25,
            text="0%",
            fill="black",
            font=("Courier", 14, "bold"),
            anchor="nw", tags=("info_enemics", "zona_enemics", "combat")
        )

        self.canvas.create_text(
            self.app.Ancho - 55, 
            25,
            text="100%",
            fill="black",
            font=("Courier", 14, "bold"),
            anchor="nw", tags=("info_enemics", "zona_enemics", "combat")
        )

        self.canvas.create_rectangle(
            5, 65,
            150, 
            self.app.Alto - 155,
            fill="white", outline="black",
            width=5, tags=("zona_enemics", "combat")
        )

        self.canvas.create_rectangle(
            self.app.Ancho - 250, 65,
            self.app.Ancho - 5, 
            self.app.Alto - 155,
            fill="white", outline="black",
            width=5, tags=("zona_aliats", "combat")
        )

        self.dibuixar_info_enemics()
        self.dibuixar_info_aliats()

    def dibuixar_info_enemics(self):

        x = 5
        y = 100
        self.canvas.create_text(
            x + 20, y - 30,
            text="Enemics",
            fill="black",
            font=("Courier", 18, "bold"),
            anchor="nw", tags=("info_enemics", "zona_enemics", "combat")
        )
        salt = 115

        for i, ent in enumerate(self.enemic.items()):
            if "Mini" not in ent[1].ImatgeAjustada.keys():
                ent[1].ImatgeAjustada["Mini"]={}

            ent[1].ImatgeAjustada["Mini"].update({
                "Frontal":
                self.app.RedimensionarImatge(
                ent[1].Imatges["Frontal"],
                33, 50, False
                )
            })

            self.canvas.create_rectangle(
                x, y,
                150, 
                y + salt,
                fill="white", outline="black",
                width=5, tags=("info_enemics", "zona_enemics", "combat")
            )
            
            self.canvas.create_image(
                x + 10, y + 10,
                image=ent[1].ImatgeAjustada["Mini"]["Frontal"],
                anchor="nw",
                tags=("ent_estat_combat", "combat")
            )
            
            self.canvas.create_text(
                x + 50, y + 15,
                text=ent[1].nom,
                fill="black",
                width=150,
                font=("Courier", 16, "bold"),
                anchor="nw", tags=("info_enemics", "zona_enemics", "combat")
            )

            self.canvas.create_text(
                x + 10, y + 58,
                text=f"Lv: {ent[1].Lv}",
                fill="black",
                font=("Courier", 16, "bold"),
                anchor="nw", tags=("info_enemics", "zona_enemics", "combat")
            )

            self.canvas.create_text(
                x + 10, y + 83,
                text=f"HP: ",
                fill="black",
                font=("Courier", 12, "bold"),
                anchor="nw", tags=("info_enemics", "zona_enemics", "combat")
            )

            self.canvas.create_rectangle(
                x + 40, y + 85,
                x + 40 + 95, 
                y + 100,
                fill="white", outline="black",
                width=2, tags=("vida_entitats_enemigues", "info_enemics", "zona_enemics", "combat")
            )

            health = ent[1].StatsCombat["CurHP"] / ent[1].StatsCombat["MaxHP"]
            mida = 95 * health

            self.canvas.create_rectangle(
                x + 40, y + 85,
                x + 40 + mida, 
                y + 100,
                fill="green", outline="black",
                width=2, tags=(f"hp_enemic_{ent[1].id}", "vida_actual_entitats", "info_enemics", "zona_enemics", "combat")
            )
            self.canvas.tag_raise("vida_actual_entitats", "vida_entitats_enemigues")
            
            font = tkfont.Font(family="Courier", size=11, weight="bold")

            texthealth = f"{round(ent[1].StatsCombat["CurHP"])}/{round(ent[1].StatsCombat["MaxHP"])}"
            midatext = font.measure(texthealth)

            self.canvas.create_text(
                x + 40 + 90 - midatext, y + 85,
                text=texthealth,
                fill="black",
                font=("Courier", 11, "bold"),
                anchor="nw", tags=(f"texthp_enemic_{ent[1].id}", "vida_actual_entitats", "text_vida_actual", "vida_entitats", "combat")
            )

            self.canvas.tag_raise("text_vida_actual", "vida_actual_entitats")

            y += salt
        
    def dibuixar_info_aliats(self):

        x = self.app.Ancho - 250
        y = 100
        self.canvas.create_text(
            x + 20, y - 30,
            text="Aliats",
            fill="black",
            font=("Courier", 18, "bold"),
            anchor="nw", tags=("info_enemics", "zona_enemics", "combat")
        )
        salt = 115

        for i, ent in enumerate(self.equip.items()):
            if "Mini" not in ent[1].ImatgeAjustada.keys():
                ent[1].ImatgeAjustada["Mini"]={}

            ent[1].ImatgeAjustada["Mini"].update({
                "Frontal":
                self.app.RedimensionarImatge(
                ent[1].Imatges["Frontal"],
                33, 50, False
                )
            })

            self.canvas.create_rectangle(
                x, y,
                self.app.Ancho - 5, 
                y + salt,
                fill="white", outline="black",
                width=5, tags=("info_aliats", "zona_aliats", "combat")
            )
            
            self.canvas.create_image(
                x + 10, y + 10,
                image=ent[1].ImatgeAjustada["Mini"]["Frontal"],
                anchor="nw",
                tags=("ent_estat_combat", "combat")
            )
            
            self.canvas.create_text(
                x + 50, y + 15,
                text=ent[1].nom,
                fill="black",
                width=180,
                font=("Courier", 16, "bold"),
                anchor="nw", tags=("info_aliats", "zona_aliats", "combat")
            )

            self.canvas.create_text(
                x + 50, y + 35,
                text=f"Lv: {ent[1].Lv}",
                fill="black",
                font=("Courier", 16, "bold"),
                anchor="nw", tags=("info_aliats", "zona_aliats", "combat")
            )

            self.canvas.create_text(
                x + 28, y + 63,
                text=f"HP:",
                fill="black",
                font=("Courier", 13, "bold"),
                anchor="nw", tags=("info_aliats", "zona_aliats", "combat")
            )

            self.canvas.create_rectangle(
                x + 60, y + 65,
                self.app.Ancho - 15, 
                y + 80,
                fill="white", outline="black",
                width=2, tags=("vida_entitats_aliades", "info_aliats", "zona_aliats", "combat")
            )

            health = ent[1].StatsCombat["CurHP"] / ent[1].StatsCombat["MaxHP"]
            amplada = (self.app.Ancho - 15) - (x + 60)
            mida = amplada * health

            self.canvas.create_rectangle(
                x + 60, y + 65,
                x + 60 + mida, 
                y + 80,
                fill="green", outline="black",
                width=2, tags=(f"vida_entitats_{ent[1].id}", "vida_actual_entitats", "combat")
            )
            self.canvas.tag_raise("vida_actual_entitats", "vida_entitats_aliades")

            font = tkfont.Font(family="Courier", size=11, weight="bold")

            texthealth = f"{round(ent[1].StatsCombat["CurHP"])}/{round(ent[1].StatsCombat["MaxHP"])}"
            midatext = font.measure(texthealth)

            self.canvas.create_text(
                self.app.Ancho - 20 - midatext, y + 65,
                text=texthealth,
                fill="black",
                font=("Courier", 11, "bold"),
                anchor="nw", tags=(f"textvida_entitats_{ent[1].id}", "vida_actual_entitats", "text_vida_actual", "vida_entitats", "combat")
            )

            self.canvas.tag_raise("text_vida_actual", "vida_actual_entitats")

            self.canvas.create_text(
                x + 10, y + 88,
                text=f"Mana:",
                fill="black",
                font=("Courier", 13, "bold"),
                anchor="nw", tags=("info_enemics", "zona_enemics", "combat")
            )

            self.canvas.create_rectangle(
                x + 60, y + 90,
                self.app.Ancho - 15, 
                y + 105,
                fill="white", outline="black",
                width=2, tags=("mana_entitats", "info_enemics", "zona_enemics", "combat")
            )

            mana = ent[1].StatsCombat["Mana"] / ent[1].StatsCombat["MaxMana"]
            amplada = (self.app.Ancho - 15) - (x + 60)
            mida = amplada * mana

            self.canvas.create_rectangle(
                x + 60, y + 90,
                x + 60 + mida, 
                y + 105,
                fill="cyan", outline="black",
                width=2, tags=(f"mana_entitats_{ent[1].id}", "mana_actual_entitats", "info_enemics", "zona_enemics", "combat")
            )
            self.canvas.tag_raise("mana_actual_entitats", "mana_entitats")

            textmana = f"{round(ent[1].StatsCombat["Mana"])}/{round(ent[1].StatsCombat["MaxMana"])}"
            midatext = font.measure(textmana)

            self.canvas.create_text(
                self.app.Ancho - 20 - midatext, y + 90,
                text=textmana,
                fill="black",
                font=("Courier", 11, "bold"),
                anchor="nw", tags=(f"textmana_entitats_{ent[1].id}", "text_mana_actual", "mana_actual_entitats", "combat")
            )

            self.canvas.tag_raise("text_vida_actual", "vida_actual_entitats")

            y += salt
    
    def dibuixar_entitats(self):
        y = self.app.Alto - 280
        x = 300 if len(self.equip) == 1 else 220 if len(self.equip) == 2 else 150
        for i, ent in enumerate(self.equip.items()):
            if "Combat" not in ent[1].ImatgeAjustada.keys():
                ent[1].ImatgeAjustada["Combat"]={}

            ent[1].ImatgeAjustada["Combat"].update({
                "Back":
                self.app.RedimensionarImatge(
                ent[1].Imatges["Back"],
                160, 240, False
                )
            })
            
            self.canvas.create_image(
                    x + 10, y + 10,
                    image=ent[1].ImatgeAjustada["Combat"]["Back"],
                    anchor="nw",
                    tags=(f"ent_ally_img_{ent[1].id}", "ent_estat_combat", "combat")
                )
            x += 150 if len(self.equip) > 1 else 210
        
        y = 50
        x = 300 if len(self.enemic) == 1 else 220 if len(self.enemic) == 2 else 150

        for i, ent in enumerate(self.enemic.items()):
            if "Combat" not in ent[1].ImatgeAjustada.keys():
                ent[1].ImatgeAjustada["Combat"]={}

            ent[1].ImatgeAjustada["Combat"].update({
                "Frontal":
                self.app.RedimensionarImatge(
                ent[1].Imatges["Frontal"],
                100, 150, False
                )
            })
            
            self.canvas.create_image(
                    x + 10, y + 50,
                    image=ent[1].ImatgeAjustada["Combat"]["Frontal"],
                    anchor="nw",
                    tags=(f"ent_enemy_img_{ent[1].id}", "ent_estat_combat", "combat")
                )
            x += 150 if len(self.equip) > 1 else 210
            
    def dibuixar_seleccio_accio_aliat(self):
        self.AccioAliat = True
        self.MenuAccioAliat = True
        self.canvas.delete("seleccio_accio_aliat")

        self.canvas.create_rectangle(
            5, self.app.Alto - 150,
            self.app.Ancho - 205, 
            self.app.Alto - 5,
            fill="white", outline="black",
            width=5, tags=("zona_seleccio", "seleccio_accio_aliat", "combat")
        )

        self.canvas.create_rectangle(
            400, self.app.Alto - 150,
            self.app.Ancho - 5, 
            self.app.Alto - 5,
            fill="white", outline="black",
            width=5, tags=("zona_descripcio", "seleccio_accio_aliat", "combat")
        )

        x = 25
        y = self.app.Alto - 130
        for pos, opcio in enumerate(self.AccionsCombat):
            color = "black"
            if self.IndexAccio == pos:
                color = "blue"
            
            if opcio.Habilitat == False:
                color="grey"

            self.canvas.create_text(
                x, y,
                text=opcio.Nom,
                fill=color,
                font=("Courier", 16, "bold"),
                anchor="nw", tags=("accions_aliat", "seleccio_accio_aliat", "combat")
            )
            y += 20
        
        self.canvas.create_text(
                420, self.app.Alto - 130,
                text=f"És el torn de {self.AtacantAliat.nom}, que vols fer?",
                fill="black",
                width= 350,
                font=("Courier", 16, "bold"),
                anchor="nw", tags=("info_turn_aliat","seleccio_accio_aliat", "combat")
            )
            
    def MovimentAccions(self, direccio):
        if self.Atacar == True:
            if self.SeleccionarObjectiu == True:
                if self.GrupObjectiuMoviment == "Enemics":
                    grup = self.enemic
                else:
                    grup = self.equip

                viu = False
                while viu == False:
                    if direccio == "a":
                        self.IndexObjectiu = (self.IndexObjectiu - 1) % len(grup)
                    elif direccio == "d":
                        self.IndexObjectiu = (self.IndexObjectiu + 1) % len(grup)

                    for pos, i in enumerate(grup.values()):
                        if pos == self.IndexObjectiu:
                            if i.StatsCombat["CurHP"] > 0:
                                viu = True
                
            else:
                if direccio == "BackSpace":
                    self.Atacar = False
                    self.canvas.delete("seleccio_atac_aliat")
                    self.Lluitar()
                else:
                    if direccio == "w":
                        self.IndexMoviment = (self.IndexMoviment - 1) % len(self.MovimentsAliat)
                    elif direccio == "s":
                        self.IndexMoviment = (self.IndexMoviment + 1) % len(self.MovimentsAliat)
                    self.dibuixar_info_moviment()
            
        elif self.AccioAliat == True:
            if direccio == "w":
                self.IndexAccio = (self.IndexAccio - 1) % len(self.AccionsCombat)
            elif direccio == "s":
                self.IndexAccio = (self.IndexAccio + 1) % len(self.AccionsCombat)

            while self.AccionsCombat[self.IndexAccio].Habilitat == False:
                if direccio == "w":
                    self.IndexAccio = (self.IndexAccio - 1) % len(self.AccionsCombat)
                elif direccio == "s":
                    self.IndexAccio = (self.IndexAccio + 1) % len(self.AccionsCombat)

            self.dibuixar_seleccio_accio_aliat()
        
    def GenerarEnemic(self):

        pesos = []
        for j in self.app.jugador.Ubicacio.Enemies.values():
            pesos.append(j["prob"])
        opcions = list(self.app.jugador.Ubicacio.Enemies.keys())
        seleccio = random.choices(opcions, pesos)
        
        prob = self.app.jugador.Ubicacio.Enemies[seleccio[0]]["group_probs"]
        
        num = []
        count = 1
        for i in prob:
            num.append(count)
            count += 1
        qty = random.choices(num, prob)
        enemy = {}

        self.enemic.update({
            "enemy_0":
            Entitat.Entity("enemy_0", "", random.randrange(
                self.app.jugador.Ubicacio.Enemies[seleccio[0]]["level_range"][0], 
                self.app.jugador.Ubicacio.Enemies[seleccio[0]]["level_range"][1] + 1), 
                False, 
                self.app.Entities[seleccio[0]])})

        probs = []
        opcionsPosib = []

        for v in self.app.jugador.Ubicacio.Enemies[seleccio[0]]["companions"]:
            probs.append(v[1])
            opcionsPosib.append(v[0])


        if qty[0] > 1:
            for l in range(qty[0] - 1):
                if len(probs) >= 1:
                    apareix = random.choices(opcionsPosib, probs)
                else:
                    apareix = seleccio[0]
                entitat = Entitat.Entity(f"enemy_{l+1}","", 
                            random.randrange(
                                self.app.jugador.Ubicacio.Enemies[seleccio[0]]["level_range"][0] - 2, self.enemic["enemy_0"].Lv), 
                                False, self.app.Entities[apareix])
                
                self.enemic.update({entitat.id: entitat})
        
        self.dibuixar_combat()

    def PrepararPerCombat(self):
        for i in self.equip.values():
            i.DefinirCombatStats()
        
        for j in self.enemic.values():
            j.DefinirCombatStats()
        
    def PrioritatInicial(self):
        maxSpeedPlayer = max(self.equip.values(), key=lambda j: j.StatsCombat["SPD"])
        maxSpeedEnemies = max(self.enemic.values(), key=lambda e: e.StatsCombat["SPD"])

        maxSpeed = max(maxSpeedPlayer.StatsCombat["SPD"], maxSpeedEnemies.StatsCombat["SPD"])

        y = 25
        for pos, i in enumerate(self.equip.values()):
            if i.StatsCombat["CurHP"] > 0:
                if i.StatsCombat["SPD"] == maxSpeed:
                    i.Priority = 100
                else:
                    i.Priority = (i.StatsCombat["SPD"] / maxSpeed) * 100

                amplada = self.app.Ancho - 80
                x = 40 + (amplada * (i.Priority / 100))

                if "Accio" not in i.ImatgeAjustada.keys():
                    i.ImatgeAjustada["Accio"]={}

                i.ImatgeAjustada["Accio"].update({
                    "Frontal":
                    self.app.RedimensionarImatge(
                    i.Imatges["Frontal"],
                    20, 30, False
                    )
                })
                
                self.canvas.create_rectangle(
                    x, y,
                    x - 2, 
                    y + 2,
                    fill="black", outline="black",
                    width=5, tags=(f"action_x_ally_{i.id}", f"accio_entitat_aliada_{i.id}", "barra_accio", "zona_accio", "combat")
                )

                self.canvas.create_rectangle(
                    x, y,
                    x - 30, 
                    55,
                    fill="white", outline="gray",
                    width=1, tags=(f"accio_entitat_aliada_{i.id}", "barra_accio", "zona_accio", "combat")
                )

                self.canvas.create_image(
                    x - 25, y,
                    image=i.ImatgeAjustada["Accio"]["Frontal"],
                    anchor="nw",
                    tags=(f"accio_entitat_aliada_{i.id}", "ent_estat_combat", "combat")
                )


        for pos, j in enumerate(self.enemic.values()):
            if j.StatsCombat["SPD"] == maxSpeed:
                j.Priority = 100
            else:
                j.Priority = (j.StatsCombat["SPD"] / maxSpeed) * 100

            amplada = self.app.Ancho - 80
            x = 40 + (amplada * (j.Priority / 100))

            if "Accio" not in j.ImatgeAjustada.keys():
                j.ImatgeAjustada["Accio"]={}

            j.ImatgeAjustada["Accio"].update({
                "Frontal":
                self.app.RedimensionarImatge(
                j.Imatges["Frontal"],
                20, 30, False
                )
            })
                        
            self.canvas.create_rectangle(
                x, y,
                x - 2, 
                y + 2,
                fill="black", outline="black",
                width=5, tags=(f"action_x_enemy_{j.id}", f"accio_entitat_enemiga_{j.id}", "barra_accio", "zona_accio", "combat")
            )

            self.canvas.create_rectangle(
                x, y,
                x - 30, 
                55,
                fill="white", outline="gray",
                width=1, tags=(f"accio_entitat_enemiga_{j.id}", "barra_accio", "zona_accio", "combat")
            )

            self.canvas.create_image(
                x - 25, y,
                image=j.ImatgeAjustada["Accio"]["Frontal"],
                anchor="nw",
                tags=(f"accio_entitat_enemiga_{j.id}", "ent_estat_combat", "combat")
            )

        if maxSpeedPlayer.StatsCombat["SPD"] > maxSpeedEnemies.StatsCombat["SPD"]:
            self.app.Menu.CrearDialeg(f"Has entrat en combat...")
            if len(self.enemic) < 2 and pos == 0:
                self.app.Menu.CrearDialeg(f"És un unic enemic, un/a {self.enemic["enemy_0"].nom}.")
                
            else:
                self.app.Menu.CrearDialeg(f"És un grup d'enemics...")
            

        else:
            self.app.Menu.CrearDialeg(f"Has estat emboscat...")

    def IncrementarPrioritat(self):
        divVel = 100    # Variable que controla quina part de la velocitat es suma cada cop a la prioritat.
                        # Quan mes alta sigui més lent recorren la barra d'acció.

        for pos, i in enumerate(self.equip.values()):
            if i.StatsCombat["CurHP"] > 0.1:
                i.Priority += i.StatsCombat["SPD"] / divVel
                amplada = self.app.Ancho - 80
                x = 40 + (amplada * (i.Priority / 100))

                old_x = self.canvas.coords(f"action_x_ally_{i.id}")
                x -= old_x[0]

                self.canvas.move(f"accio_entitat_aliada_{i.id}", x, 0)
        
        for pos, j in enumerate(self.enemic.values()):
            if j.StatsCombat["CurHP"] > 0.1:
                j.Priority += j.StatsCombat["SPD"] / divVel
                amplada = self.app.Ancho - 80
                x = 40 + (amplada * (j.Priority / 100))

                old_x = self.canvas.coords(f"action_x_enemy_{j.id}")
                x -= old_x[0]

                self.canvas.move(f"accio_entitat_enemiga_{j.id}", x, 0)

        self.app.root.after(10, self.Lluitar)

    def ColocarVistaLiniaPrioritat(self):
        if self.AtacantEnemic != None:
            self.canvas.tag_raise(f"accio_entitat_aliada_{self.AtacantEnemic.id}", "all")
        if self.AtacantAliat != None:
            self.canvas.tag_raise(f"accio_entitat_aliada_{self.AtacantAliat.id}", "all")
    
    def Lluitar(self):
        
        if self.combat == True and self.Fugir[0] == False:
            if self.UpdatingHP == False:
                if len(self.enemic) >= 1 and len(self.equip) >= 1:
                    maxPriorityPlayer = max(self.equip.values(), key=lambda j: j.Priority)
                    maxPriorityEnemies = max(self.enemic.values(), key=lambda e: e.Priority)

                    actuant = max(maxPriorityEnemies, maxPriorityPlayer, key=lambda e: e.Priority)
                
                    if actuant.Priority >= 100:

                        if actuant in self.equip.values():
                            self.AtacantAliat = actuant
                            self.ColocarVistaLiniaPrioritat()
                            self.dibuixar_seleccio_accio_aliat()
                        else:
                            self.AccioEnemic = True
                            self.AtacantEnemic = actuant
                            self.ColocarVistaLiniaPrioritat()
                            self.AccioEnemiga()
                            
                if self.combat == True:
                    self.ComprobarFiCombat()
                
                if self.AccioAliat == False and self.AccioEnemic == False:
                    self.IncrementarPrioritat()

        else:
            if self.app.DialegActiu == False:
                self.dibuixar_Pantalla_fi_combat()
    
    def dibuixar_Pantalla_fi_combat(self):
        self.PantallaFICombat = True
        self.finalitzarCombat()

        self.AccioAliat = False
        self.AccioFugirEstat = False

        self.canvas.delete("all")
        self.canvas.create_rectangle(
            5, 5,
            self.app.Ancho - 5, 
            self.app.Alto -5,
            fill="white", outline="black",
            width=5, tags=("fi_combat_fons", "fi_combat")
        )

        self.canvas.create_rectangle(
            5, 5,
            self.app.Ancho - 5, 
            75,
            fill="white", outline="black",
            width=5, tags=("enunciat", "fi_combat")
        )

        enunciat = "Victoria !!"
        if self.Derrotat == True:
            enunciat = "Derrota..."

        font = tkfont.Font(family="Courier", size=24, weight="bold")
        mida = font.measure(enunciat)

        self.canvas.create_text(
            (self.app.Ancho // 2) - (mida // 2), 40,
            text=enunciat,
            fill="black",
            font=("Courier", 24, "bold"),
            anchor="w", tags=("text_enunciat", "enunciat", "fi_combat")
        )

        self.canvas.create_rectangle(
            5, 80,
            self.app.Ancho - 5, 
            395,
            fill="white", outline="black",
            width=5, tags=("zona_objectes", "fi_combat")
        )

        self.canvas.create_text(
            30, 110,
            text="Objectes Adquirits",
            fill="black",
            font=("Courier", 24, "bold"),
            anchor="w", tags=("enunciat_objectes", "zona_objectes", "fi_combat")
        )

        self.canvas.create_text(
            30, 140,
            text="No s'han adquirit objectes en aquest combat...",
            fill="black",
            font=("Courier", 18, "bold"),
            anchor="w", tags=("text_objectes", "zona_objectes", "fi_combat")
        )

        self.canvas.create_rectangle(
            5, 400,
            self.app.Ancho - 5, 
            self.app.Alto - 5,
            fill="white", outline="black",
            width=5, tags=("zona_experiencia", "fi_combat")
        )

        x = 5
        y = 400
        
        for num, ally in enumerate(self.equip.values()):
            salt = 295 if num <= 2 else 300
            self.canvas.create_rectangle(
                x, y,
                x + salt, 
                self.app.Alto - 5,
                fill="white", outline="black",
                width=5, tags=("zona_experiencia", "fi_combat")
            )
            if "MostrarExp" not in ally.ImatgeAjustada.keys():
                ally.ImatgeAjustada["MostrarExp"]={}

            ally.ImatgeAjustada["Mini"].update({
                "Frontal":
                self.app.RedimensionarImatge(
                ally.Imatges["Frontal"],
                60, 90, False
                )
            })
            
            self.canvas.create_image(
                x + 20, y + 20,
                image=ally.ImatgeAjustada["Mini"]["Frontal"],
                anchor="nw",
                tags=("zona_experiencia", "fi_combat")
            )
            
            self.canvas.create_text(
                x + 95, y + 25,
                text=ally.nom,
                fill="black",
                width=180,
                font=("Courier", 16, "bold"),
                anchor="nw", tags=("zona_experiencia", "fi_combat")
            )

            self.canvas.create_text(
                x + 95, y + 55,
                text=f"Lv: {ally.Lv} / {ally.LvLimit}",
                fill="black",
                font=("Courier", 16, "bold"),
                anchor="nw", tags=(f"text_nivell_{ally.id}", "zona_experiencia", "fi_combat")
            )

            self.canvas.create_rectangle(
                x + 20, self.app.Alto - 65,
                x + salt - 20, 
                self.app.Alto - 45,
                fill="white", outline="black",
                width=5, tags=(f"barra_xp_fons_{ally.id}", "zona_experiencia", "fi_combat")
            )

            percentatgeXP = (round(ally.Xp, 2) / round(ally.XpRequired, 2))
            amplebarraxp = (salt - 20 - 20)
            midabarraxp = amplebarraxp * percentatgeXP
            
            self.canvas.create_rectangle(
                x + 20, self.app.Alto - 65,
                x + 20 + midabarraxp, 
                self.app.Alto - 45,
                fill="cyan",
                width=5, tags=(f"barra_xp_{ally.id}", "zona_experiencia", "fi_combat")
            )

            text_xp = f"{round(ally.Xp, 2)} / {round(ally.XpRequired, 2)}"
            self.canvas.create_text(
                x + 20, self.app.Alto - 40,
                text=f"EXP: {text_xp}",
                fill="black",
                font=("Courier", 14, "bold"),
                anchor="nw", tags=(f"text_experiencia_{ally.id}", "zona_experiencia", "fi_combat")
            )
            
            x+= salt

        self.levelingUp = True
        self.dibuixar_experiencia_pantalla_fi()
            # Falta crear la barra d'experiencia... (el fons d'aquesta, la de color en la altre funcio)

    def dibuixar_experiencia_pantalla_fi(self):
    # En aquesta només incrementarem la barra i creearem la de color, i la reduirem a zero si ja esta al limit del nivell
    # enunciarem que s'ha pujat de nivell, etc...
        for num, ally in enumerate(self.equip.values()):
            levelUp = False
            if ally.id in self.Recompenses["XP"].keys():
                if self.Recompenses["XP"][ally.id] > (ally.XpRequired / 100) and self.saltarPantallaFi == False:
                    levelUp = ally.LvlUp((ally.XpRequired / 100))
                    self.Recompenses["XP"][ally.id] -= (ally.XpRequired / 100)
                else:
                    if self.saltarPantallaFi == True:
                        self.levelingUp = False
                    levelUp = ally.LvlUp(self.Recompenses["XP"][ally.id])
                    self.Recompenses["XP"][ally.id] = 0

            midesBarraFons = self.canvas.coords(f"barra_xp_fons_{ally.id}")

            coordsBarraXP = self.canvas.coords(f"barra_xp_{ally.id}")
            percentatgeXP = (round(ally.Xp, 2) / round(ally.XpRequired, 2))
            amplebarraxp = midesBarraFons[2] - midesBarraFons[0]
            coordsBarraXP[2] = coordsBarraXP[0] + (amplebarraxp * percentatgeXP)
    
            coordsBarraXP = self.canvas.coords(f"barra_xp_{ally.id}", coordsBarraXP)

            text_xp = f"EXP: {round(ally.Xp, 2)} / {round(ally.XpRequired, 2)}"
            self.canvas.itemconfig(f"text_experiencia_{ally.id}", text=text_xp)
        
            if levelUp == True:
                posicio = self.canvas.coords(f"text_nivell_{ally.id}")
                self.canvas.create_text(
                    posicio[0], posicio[1] + 20,
                    text=f"Level UP !!",
                    fill="black",
                    font=("Courier", 14, "bold"),
                    anchor="nw", tags=(f"text_pujatnivell_{ally.id}", "zona_experiencia", "fi_combat")
                )
                self.canvas.itemconfig(f"text_nivell_{ally.id}", text=f"Lv: {ally.Lv} / {ally.LvLimit}")

        completats = 0
        for i in self.Recompenses["XP"].values():
            if i == 0:
                completats+=1
        if completats == len(self.Recompenses["XP"].keys()):
            self.levelingUp = False
           
        
        if self.levelingUp == True:
            self.levelAnimation = self.app.root.after(10, self.dibuixar_experiencia_pantalla_fi)
        else:
            if self.levelAnimation != None:
                self.app.root.after_cancel(self.levelAnimation)
            self.CombatAcabat = True

    def dibuixar_objectes_pantalla_fi(self):
        pass
    # dibuixar obtencio d'or, de moment res més, ja que en un combat no obtenim objectes...

    def AccioEnemiga(self):
        # Seleccionem Atac
        llistaMoviments = []
        probMoviment = []
        for id, move in self.AtacantEnemic.Moves.items():
            if self.AtacantEnemic.StatsCombat["Mana"] >= move.Cost:
                llistaMoviments.append(move)
                if move.Healing == True:
                    prob = 50
                elif move.Protective == True:
                    prob = 50
                else:
                    if move.MultiTarget == True:
                        prob = 70 - (move.Power / 10)
                    else:
                        prob = 100 - (move.Power / 10)
                    
                    if len(move.Buff) > 0 or len(move.Debuff) > 0:
                        prob -= ((len(move.Buff) * 5) + (len(move.Debuff) * 5))

                probMoviment.append(prob)


        accio = random.choices(llistaMoviments, weights=probMoviment)
        
        # Busquem entitat a atacar
        if accio[0].MultiTarget == False:

            if accio[0].Protective == False and accio[0].Healing == False:
                llistaObjectius = []
                llistaProb = []

                atacCategoria = "ATK"
                if accio[0].Type == True:
                    atacCategoria = "INT"

                for id, ent in self.equip.items():
                    if ent.StatsCombat["CurHP"] > 0:
                        llistaObjectius.append(id)
                        if ent.StatsCombat["DEF"] > self.AtacantEnemic.StatsCombat[atacCategoria]:
                            prob = 30
                        elif ent.StatsCombat["DEF"] < self.AtacantEnemic.StatsCombat[atacCategoria]:
                            prob = 45
                        else:
                            prob = 40
                        
                        prob += (ent.Priority // 10)
                        llistaProb.append(prob)

                target = random.choices(llistaObjectius, weights=llistaProb)
            else:
                llistaObjectius = []
                llistaProb = []

                atacCategoria = "ATK"
                if accio[0].Type == True:
                    atacCategoria = "INT"

                for id, ent in self.equip.items():
                    if ent.StatsCombat["CurHP"] > 0:
                        llistaObjectius.append(id)
                        if ent.StatsCombat["CurHP"] < ent.StatsCombat["MaxHP"] / 10:
                            prob = 70
                        elif ent.StatsCombat["CurHP"] < ent.StatsCombat["MaxHP"] / 4:
                            prob = 45
                        elif ent.StatsCombat["CurHP"] < ent.StatsCombat["MaxHP"] / 2:
                            prob = 30
                        else:
                            prob = 15
                        
                        llistaProb.append(prob)

                target = random.choices(llistaObjectius, weights=llistaProb)
                
        else:
            target = ["All"]

        self.app.Menu.CrearDialeg(f"{self.AtacantEnemic.nom} ha utilitzat {accio[0].Name}!")
        self.AtacantEnemic.atacar(self, target[0], accio[0])

    def DescartarDerrotats(self):
        comprobat = False
        for id, enemy in self.enemic.items():
            if enemy.StatsCombat["CurHP"] <= 0.1:
                if id not in self.EnemicsDerrotats.keys():
                    self.EnemicsDerrotats[id]=enemy
                    self.app.jugador.Gold += enemy.Lv * 10
                    comprobat = True
                    self.EliminarVistaAccioDescartats(enemy, False)
                    self.DescartarDerrotatsAliats(enemy)
        if comprobat == False:
            self.DescartarDerrotatsAliats()
    
    def DescartarDerrotatsAliats(self, enemy = None):
        for ally_id, ally in self.equip.items():
            if ally.StatsCombat["CurHP"] <= 0.1:
                if ally_id not in self.AliatsDerrotats.keys():
                    self.AliatsDerrotats[ally_id]=ally
                    self.EliminarVistaAccioDescartats(ally, True)
            else:
                if enemy != None:
                    xp = ally.XPObtained(enemy)
                    if ally_id not in self.Recompenses["XP"].keys():
                        self.Recompenses["XP"].update({ ally_id: xp })
                    else:
                        self.Recompenses["XP"][ally_id]+=xp
    
    def EliminarVistaAccioDescartats(self, entitat, boolAliat = True):
        grup = None
        if boolAliat == True:
            self.canvas.delete(f"accio_entitat_aliada_{entitat.id}")
            self.canvas.itemconfig(f"ent_ally_img_{entitat.id}", state="hidden")
            if len(self.equip) != len(self.AliatsDerrotats):
                grup = self.equip
        else:
            self.canvas.delete(f"accio_entitat_enemiga_{entitat.id}")
            self.canvas.itemconfig(f"ent_enemy_img_{entitat.id}", state="hidden")
            if len(self.enemic) != len(self.EnemicsDerrotats):
                grup = self.enemic
        
        if grup != None:
            viu = False
            while viu == False:
                for pos, i in enumerate(grup.values()):
                    if i.StatsCombat["CurHP"] > 0:
                        viu = True
                    else:
                        self.IndexObjectiu = (self.IndexObjectiu + 1) % len(grup)

    def ComprobarFiCombat(self):
        if len(self.EnemicsDerrotats) == len(self.enemic) or len(self.AliatsDerrotats) == len(self.equip):
            self.combat = False
            # if len(self.enemic) == self.enemyderr:
            #     for id, val in self.enemic.items():
            #         self.app.event.CridarEvent("Derrotar Enemic", val, self.app)
            if len(self.AliatsDerrotats) == len(self.equip):
                self.Derrotat = True
                
    def finalitzarCombat(self):
        for i in self.equip.values():
            i.afected = []
            i.DefinirCombatStats()
        for id, ent in self.EnemicsDerrotats.items():
            self.app.event.CridarEvent("Derrotar Enemic", ent, self.app)


    def ComprobarEfecteEstat(self, aliat = True):
        if aliat == True:
            comprobar = self.AtacantAliat
        else:
            comprobar = self.AtacantEnemic

        self.danyEfectes = {}
        self.entitats_afectades = []
        if len(comprobar.afected) > 0:
            eliminar = []
            
            for i in comprobar.afected:
                if i.RemainingTurns <= 0 and i.Turns > 0:
                    eliminar.append(i)
                elif comprobar.StatsCombat["CurHP"] > 0:
                    i.RemainingTurns -= 1
            for j in eliminar:
                comprobar.afected.remove(j)
            comprobar.AplicarCanvisEfectesEstat()

    def CrearLlistatMoviments(self):
        self.MovimentsAliat = []
        for id, move in self.AtacantAliat.Moves.items():
            estat = True
            if move.Cost > self.AtacantAliat.StatsCombat["Mana"]:
                estat = False
            self.MovimentsAliat.append(
                OpcionsCombat(id, move.Name, estat, "", move)
            )

    def dibuixar_seleccio_Moviment(self):
        self.Atacar = True

        self.canvas.delete("seleccio_accio_aliat")
        self.canvas.delete("seleccio_atac_aliat")
        self.CrearLlistatMoviments()
        
        self.canvas.create_rectangle(
            5, self.app.Alto - 150,
            self.app.Ancho - 305, 
            self.app.Alto - 5,
            fill="white", outline="black",
            width=5, tags=("zona_seleccio", "seleccio_atac_aliat", "combat")
        )

        self.canvas.create_rectangle(
            self.app.Ancho - 300,
            self.app.Alto - 150,
            self.app.Ancho - 5, 
            self.app.Alto - 5,
            fill="white", outline="black",
            width=5, tags=("zona_descripcio", "seleccio_atac_aliat", "combat")
        )

        self.dibuixar_info_moviment()

    def dibuixar_info_moviment(self):
        self.IndexMoviment = self.IndexMoviment % len(self.MovimentsAliat)
        move = self.MovimentsAliat[self.IndexMoviment]

        pos_seg, pos_ant = None, None
        if len(self.MovimentsAliat) > 1:
            pos_seg = (self.IndexMoviment + 1) % len(self.MovimentsAliat)
        if len(self.MovimentsAliat) > 2:
            pos_ant = (self.IndexMoviment - 1) % len(self.MovimentsAliat)

        self.canvas.delete("info_atac")
        self.canvas.delete("atacs")

        font1 = tkfont.Font(family="Courier", size=18, weight="bold")
        lenght = font1.measure(move.Moviment.Name)

        self.canvas.create_text(
                5 + (((self.app.Ancho - 305) - lenght) / 2), 
                self.app.Alto - 80,
                text=move.Moviment.Name,
                fill="blue" if move.Habilitat == True else "grey",
                width= 350,
                font=("Courier", 18, "bold"),
                anchor="nw", tags=("atac_actual", "atacs","seleccio_atac_aliat", "combat")
            )
        
        if pos_ant != None or pos_seg != None:
            font2 = tkfont.Font(family="Courier", size=16, weight="bold")
            if pos_ant != None:
                font2 = tkfont.Font(family="Courier", size=16, weight="bold")
                lenght = font2.measure(self.MovimentsAliat[pos_ant].Moviment.Name)

                self.canvas.create_text(
                        5 + (((self.app.Ancho - 305) - lenght) / 2),
                        self.app.Alto - 110,
                        text=self.MovimentsAliat[pos_ant].Moviment.Name,
                        fill="#202020" if self.MovimentsAliat[pos_ant].Habilitat == True else "grey",
                        width= 350,
                        font=("Courier", 16, "bold"),
                        anchor="nw", tags=("atac_ant", "atacs", "seleccio_atac_aliat", "combat")
                    )

            if pos_seg != None:
                lenght = font2.measure(self.MovimentsAliat[pos_seg].Moviment.Name)
                self.canvas.create_text(
                        5 + (((self.app.Ancho - 305) - lenght) / 2),
                        self.app.Alto - 50,
                        text=self.MovimentsAliat[pos_seg].Moviment.Name,
                        fill="#202020" if self.MovimentsAliat[pos_seg].Habilitat == True else "grey",
                        width= 350,
                        font=("Courier", 16, "bold"),
                        anchor="nw", tags=("atac_seg", "atacs", "seleccio_atac_aliat", "combat")
                    )
        
        # Informacio Moviment
        self.canvas.create_text(
            self.app.Ancho - 255, 
            self.app.Alto - 130,
            text=f"Potencia: {move.Moviment.Power}",
            fill="black",
            width= 350,
            font=("Courier", 16, "bold"),
            anchor="nw", tags=("info_atac","seleccio_atac_aliat", "combat")
        )

        self.canvas.create_text(
            self.app.Ancho - 255,
            self.app.Alto - 100,
            text=f"Precisio: {move.Moviment.Precision}",
            fill="black",
            width= 350,
            font=("Courier", 16, "bold"),
            anchor="nw", tags=("info_atac","seleccio_atac_aliat", "combat")
        )

        self.canvas.create_text(
            self.app.Ancho - 255,
            self.app.Alto - 70,
            text=f"Mana Cost: {move.Moviment.Cost}",
            fill="black",
            width= 350,
            font=("Courier", 16, "bold"),
            anchor="nw", tags=("info_atac","seleccio_atac_aliat", "combat")
        )

        if move.Moviment.Type == True:
            tipus = "Magic"
        else:
            tipus = "Fisic"

        self.canvas.create_text(
            self.app.Ancho - 255,
            self.app.Alto - 40,
            text=f"Tipus: {tipus}",
            fill="black",
            width= 350,
            font=("Courier", 16, "bold"),
            anchor="nw", tags=("info_atac","seleccio_atac_aliat", "combat")
        )

        # Mostrar Posicio en llista
        self.canvas.create_text(
            self.app.Ancho - 515,
            self.app.Alto - 30,
            text=f"Moviment {self.IndexMoviment + 1} de {len(self.MovimentsAliat)}",
            fill="black",
            width= 350,
            font=("Courier", 16, "bold"),
            anchor="nw", tags=("info_atac","seleccio_atac_aliat", "combat")
        )
    
    def dibuixar_seleccio_objectiu(self, moviment, mostrar = True):
        self.SeleccionarObjectiu = True
        if self.AtacARealitzar != moviment.Moviment:
            self.AtacARealitzar = moviment.Moviment
        
        stat = "hidden"
        if mostrar == True:
            stat = "normal"

        if self.AtacARealitzar.MultiTarget == False:
            if self.AtacARealitzar.Healing == False and self.AtacARealitzar.Protective == False:
                self.GrupObjectiuMoviment = "Enemics"
                for pos, ent in enumerate(self.enemic.values()):
                    if pos == self.IndexObjectiu:
                        if self.ObjectiuMoviment != ent:
                            self.ObjectiuMoviment = ent
                    else:
                        if ent.StatsCombat["CurHP"] > 0.1:
                            self.canvas.itemconfig(f"ent_enemy_img_{ent.id}", state="normal")

                self.canvas.itemconfig(f"ent_enemy_img_{self.ObjectiuMoviment.id}", state=stat)
            else:
                self.GrupObjectiuMoviment = "Aliats"
                for pos, ent in enumerate(self.equip.values()):
                    if pos == self.IndexObjectiu:
                        if self.ObjectiuMoviment != ent:
                            self.ObjectiuMoviment = ent
                    else:
                        if ent.StatsCombat["CurHP"] > 0.1:
                            self.canvas.itemconfig(f"ent_ally_img_{ent.id}", state="normal")

                self.canvas.itemconfig(f"ent_ally_img_{self.ObjectiuMoviment.id}", state=stat)
            
            self.AnimacioSeleccioObjectiu = self.app.root.after(200, 
                            lambda: self.dibuixar_seleccio_objectiu(moviment, not mostrar))

        else:
            self.ObjectiuMoviment = "All"
            self.RealitzarAtac()
    
    def CancelarSeleccioObjectiu(self):
        self.SeleccionarObjectiu = False
        if self.ObjectiuMoviment.id in self.equip.keys():
            self.canvas.itemconfig(f"ent_ally_img_{self.ObjectiuMoviment.id}", state="normal")
        else:
            self.canvas.itemconfig(f"ent_enemy_img_{self.ObjectiuMoviment.id}", state="normal")
        self.app.root.after_cancel(self.AnimacioSeleccioObjectiu)

    def RealitzarAtac(self):
        self.SeleccionarObjectiu = False
        self.app.Menu.CrearDialeg(f"{self.AtacantAliat.nom}, ha utilitzat {self.AtacARealitzar.Name} !!")
        # Cal canviar per a poder seleccionar enemic...
        if self.AtacARealitzar.MultiTarget == True:
            target = self.ObjectiuMoviment
        else:
            target = self.ObjectiuMoviment.id

        if self.AtacARealitzar.Healing == True or self.AtacARealitzar.Protective == True:
            self.AtacantAliat.MoveProtHeal(self, target, self.AtacARealitzar)
        else:
            self.AtacantAliat.atacar(self, target, self.AtacARealitzar)
    
    def ActualitzarBarresEstat(self, entitat = None):
        if entitat != None:
            grup = [entitat]

        if entitat in self.enemic.values():
            tag = {
            "barraHP": "hp_enemic_",
            "textHP": "texthp_enemic_",
            "barraBase": "vida_entitats_enemigues",
            "posBaseXHP": (135)
            }
        elif entitat == None or entitat in self.equip.values():
            if entitat == None:
                grup = self.equip.values()

            tag = {
            "barraHP": "vida_entitats_",
            "barraMP": "",
            "textHP": "textvida_entitats_",
            "textMP": "",
            "barraBase": "vida_entitats_aliades",
            "posBaseXHP": (self.app.Ancho - 20)
            }

        for pos, ent in enumerate(grup):
            x = self.app.Ancho - 250

            coords_barraBase = self.canvas.coords(f"{tag["barraBase"]}")

            actual_coords = self.canvas.coords(f"{tag["barraHP"]}{ent.id}")

            health = ent.StatsCombat["CurHP"] / ent.StatsCombat["MaxHP"]
            amplada = coords_barraBase[2] - coords_barraBase[0]
            mida = amplada * health

            new_coords = actual_coords
            new_coords[2] =  coords_barraBase[0] + mida

            self.canvas.coords(f"{tag["barraHP"]}{ent.id}", new_coords)

            actual_coords = self.canvas.coords(f"{tag["textHP"]}{ent.id}")
            new_coords = actual_coords
            font = tkfont.Font(family="Courier", size=11, weight="bold")

            texthealth = f"{round(ent.StatsCombat["CurHP"])}/{round(ent.StatsCombat["MaxHP"])}"
            midatext = font.measure(texthealth)
            new_coords[0] = tag["posBaseXHP"] - midatext
            self.canvas.itemconfig(f"{tag["textHP"]}{ent.id}", text=texthealth)
            self.canvas.coords(f"{tag["textHP"]}{ent.id}", new_coords)

            if "textMP" in tag.keys():
                if entitat == None:
                    x = self.app.Ancho - 250
                mana = ent.StatsCombat["Mana"] / ent.StatsCombat["MaxMana"]
                amplada = (self.app.Ancho - 15) - (x + 60)
                mida = amplada * mana
                
                actual_coords = self.canvas.coords(f"mana_entitats_{ent.id}")

                new_coords = actual_coords
                new_coords[2] = x + 60 + mida

                self.canvas.coords(f"mana_entitats_{ent.id}", new_coords)

                textmana = f"{round(ent.StatsCombat["Mana"])}/{round(ent.StatsCombat["MaxMana"])}"

                actual_coords = self.canvas.coords(f"textmana_entitats_{ent.id}")
                new_coords = actual_coords

                font = tkfont.Font(family="Courier", size=11, weight="bold")
                midatext = font.measure(textmana)

                new_coords[0] = self.app.Ancho - 20 - midatext
                self.canvas.itemconfig(f"textmana_entitats_{ent.id}", text=textmana)
                self.canvas.coords(f"textmana_entitats_{ent.id}", new_coords)

    
    def AplicarDany(self, dany, managastat, atacats, atacant, manacost = 0, danyrestant = "No Aplicat"):
        self.Atacar = False
        popEnt = []

        if danyrestant == "No Aplicat":
            danyrestant = dany.copy()
            if atacant.id in self.equip.keys():
                if managastat > 0:
                    manacost = managastat

        for pos, ent in enumerate(atacats):
            if ent.id in dany.keys():
                self.UpdatingHP = True

                if dany[ent.id] > 0:
                    if danyrestant[ent.id] > (ent.StatsCombat["MaxHP"] / 100) and ent.StatsCombat["CurHP"] > 0:
                        ent.StatsCombat["CurHP"] -= (ent.StatsCombat["MaxHP"] / 100)
                        danyrestant[ent.id] -= (ent.StatsCombat["MaxHP"] / 100)
                    
                    elif danyrestant[ent.id] <= (ent.StatsCombat["MaxHP"] / 100) and ent.StatsCombat["CurHP"] > 0:
                        ent.StatsCombat["CurHP"] -= danyrestant[ent.id]
                        if ent.id in dany:
                            dany.pop(ent.id)
                    else:
                        if ent not in popEnt:
                            popEnt.append(ent)
                        if ent.id in dany:
                            dany.pop(ent.id)
                
                elif dany[ent.id] < 0:
                    danyrestant[ent.id] = abs(danyrestant[ent.id])

                    if danyrestant[ent.id] > (ent.StatsCombat["MaxHP"] / 100):
                        ent.StatsCombat["CurHP"] += (ent.StatsCombat["MaxHP"] / 100)
                        danyrestant[ent.id] -= (ent.StatsCombat["MaxHP"] / 100)
                    
                    elif danyrestant[ent.id] <= (ent.StatsCombat["MaxHP"] / 100):
                        ent.StatsCombat["CurHP"] += abs(danyrestant[ent.id])
                        if ent.id in dany:
                            dany.pop(ent.id)
                else:
                    if ent.id in dany:
                        dany.pop(ent.id)
                
                if ent.StatsCombat["CurHP"] <= 0.01:
                    ent.StatsCombat["CurHP"] = 0
                
                ent.StatsCombat["CurHP"] = round(ent.StatsCombat["CurHP"], 1)
                danyrestant[ent.id] = round(danyrestant[ent.id], 1)

                self.ActualitzarBarresEstat(ent)
            
            if atacant.id in self.equip.keys() and managastat > 0:

                if manacost >= (atacant.StatsCombat["MaxMana"] / 100):
                    atacant.StatsCombat["Mana"] -= (atacant.StatsCombat["MaxMana"] / 100)
                    manacost -= (atacant.StatsCombat["MaxMana"] / 100)
                else:
                    atacant.StatsCombat["Mana"] -= manacost
                    manacost = 0

                x = self.app.Ancho - 250
                mana = atacant.StatsCombat["Mana"] / atacant.StatsCombat["MaxMana"]
                amplada = (self.app.Ancho - 15) - (x + 60)
                mida = amplada * mana
                
                actual_coords = self.canvas.coords(f"mana_entitats_{atacant.id}")

                new_coords = actual_coords
                new_coords[2] = x + 60 + mida

                self.canvas.coords(f"mana_entitats_{atacant.id}", new_coords)

                textmana = f"{round(atacant.StatsCombat["Mana"])}/{round(atacant.StatsCombat["MaxMana"])}"

                actual_coords = self.canvas.coords(f"textmana_entitats_{atacant.id}")
                new_coords = actual_coords

                font = tkfont.Font(family="Courier", size=11, weight="bold")
                midatext = font.measure(textmana)

                new_coords[0] = self.app.Ancho - 20 - midatext
                self.canvas.itemconfig(f"textmana_entitats_{atacant.id}", text=textmana)
                self.canvas.coords(f"textmana_entitats_{atacant.id}", new_coords)
                    
        for ent in popEnt:
            atacats.remove(ent)

        mana_actualitzat = True
        if managastat > 0 and manacost > 0:
            mana_actualitzat = False

        if len(atacats) == 0 or len(dany.keys()) == 0 and mana_actualitzat == True:
            self.UpdatingHP = False
            if self.UpdateHPAnimation != None:
                self.app.root.after_cancel(self.UpdateHPAnimation)
            self.canvas.delete("seleccio_atac_aliat")
            if atacant.id in self.equip.keys():
                self.FinalitzarTorn()
            else:
                self.FinalitzarTorn(False)
        else:
            self.UpdateHPAnimation = self.app.root.after(10, lambda: self.AplicarDany(dany, managastat, atacats, atacant, manacost, danyrestant))
        
    def FinalitzarTorn(self, aliat = True):
        self.ComprobarEfecteEstat(aliat)
        self.DescartarDerrotats()
        if aliat == True:
            self.AtacantAliat.Priority = 0
            self.AccioAliat = False
            self.Atacar = False
        else:
            self.AtacantEnemic.Priority = 0
            self.AccioEnemic = False
                       
    def AccioPasarTorn(self):
        # Cridar un dialeg que mostri amb text que s'ha passat el torn...
        self.PassarTorn = True
        self.canvas.delete("seleccio_accio_aliat")
        self.app.Menu.CrearDialeg("Has decidit passar el torn...")
        self.FinalitzarTorn()

    def EleccioDespresPostDialegIntern(self):
        if self.AccioAliat == True:
            if self.PassarTorn == True: self.PasarTornSystem()
            if self.AccioFugirEstat == True:
                if self.Fugir[0] == True:
                    self.dibuixar_Pantalla_fi_combat()
            elif self.Atacar == True:
                self.Lluitar()
            
        else:
            self.Lluitar()
    
    def PasarTornSystem(self):
        self.PassarTorn = False
        self.AccioAliat = False
        self.AtacantAliat.Priority = 0
        self.Lluitar()

    def AccioFugir(self):
        self.AccioFugirEstat = True
        self.canvas.delete("seleccio_accio_aliat")


        teamSPD = 0
        for i in self.equip.values():
            teamSPD += i.StatsCombat["SPD"]
        enemySPD = 0
        for j in self.enemic.values():
            enemySPD += j.StatsCombat["SPD"]
        prob = self.app.jugador.fleeProb * (teamSPD / enemySPD)   # fleeProb = 75 de base
    
        # 75% base * resultat de velocitat del jugador entre la del enemic. (75 * (22 / 20) = 1.1) = 82.5)
        if prob < 100:
            fugir = random.choices([True, False], cum_weights=[prob, 100 - prob])
        else:
            fugir = [True]

        self.Fugir = fugir

        if self.Fugir[0] == True:
            self.app.Menu.CrearDialeg("Has conseguit Fugir !!")
        else:
            self.app.Menu.CrearDialeg("No has aconseguit fugir...")
            self.FinalitzarTorn()
