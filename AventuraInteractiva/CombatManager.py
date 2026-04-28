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
        self.app = app
        self.canvas = canvas
        self.id = ident
        self.equip = self.app.jugador.Team
        self.enemic = {}
        self.OpcionsCombat = [
            OpcionsCombat("atacar", "Atacar", True, ""),
            OpcionsCombat("motxila", "Motxila", True, ""),
            OpcionsCombat("estat", "Veure Estat", True, ""),
            OpcionsCombat("fugir", "Fugir", True, ""),
            OpcionsCombat("pasar", "Pasar Torn", True, "")
        ]
    
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
                tags=("ent_estat", "mostrar_estat")
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
                width=2, tags=("vida_entitats", "info_enemics", "zona_enemics", "combat")
            )

            health = ent[1].StatsCombat["CurHP"] / ent[1].StatsCombat["MaxHP"]
            mida = 95 * health

            self.canvas.create_rectangle(
                x + 40, y + 85,
                x + 40 + mida, 
                y + 100,
                fill="green", outline="black",
                width=2, tags=("vida_actual_entitats", "info_enemics", "zona_enemics", "combat")
            )
            self.canvas.tag_raise("vida_actual_entitats", "vida_entitats")
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
                width=5, tags=("info_enemics", "zona_enemics", "combat")
            )
            
            self.canvas.create_image(
                x + 10, y + 10,
                image=ent[1].ImatgeAjustada["Mini"]["Frontal"],
                anchor="nw",
                tags=("ent_estat", "mostrar_estat")
            )
            
            self.canvas.create_text(
                x + 50, y + 15,
                text=ent[1].nom,
                fill="black",
                width=180,
                font=("Courier", 16, "bold"),
                anchor="nw", tags=("info_enemics", "zona_enemics", "combat")
            )

            self.canvas.create_text(
                x + 50, y + 35,
                text=f"Lv: {ent[1].Lv}",
                fill="black",
                font=("Courier", 16, "bold"),
                anchor="nw", tags=("info_enemics", "zona_enemics", "combat")
            )

            self.canvas.create_text(
                x + 28, y + 63,
                text=f"HP:",
                fill="black",
                font=("Courier", 13, "bold"),
                anchor="nw", tags=("info_enemics", "zona_enemics", "combat")
            )

            self.canvas.create_rectangle(
                x + 60, y + 65,
                self.app.Ancho - 15, 
                y + 80,
                fill="white", outline="black",
                width=2, tags=("vida_entitats", "info_enemics", "zona_enemics", "combat")
            )

            health = ent[1].StatsCombat["CurHP"] / ent[1].StatsCombat["MaxHP"]
            amplada = (self.app.Ancho - 15) - (x + 60)
            mida = amplada * health

            self.canvas.create_rectangle(
                x + 60, y + 65,
                x + 60 + mida, 
                y + 80,
                fill="green", outline="black",
                width=2, tags=("vida_actual_entitats", "info_enemics", "zona_enemics", "combat")
            )
            self.canvas.tag_raise("vida_actual_entitats", "vida_entitats")

            font = tkfont.Font(family="Courier", size=11, weight="bold")

            texthealth = f"{round(ent[1].StatsCombat["CurHP"])}/{round(ent[1].StatsCombat["MaxHP"])}"
            midatext = font.measure(texthealth)

            self.canvas.create_text(
                self.app.Ancho - 20 - midatext, y + 65,
                text=texthealth,
                fill="black",
                font=("Courier", 11, "bold"),
                anchor="nw", tags=("info_enemics", "zona_enemics", "combat")
            )

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
                width=2, tags=("mana_actual_entitats", "info_enemics", "zona_enemics", "combat")
            )
            self.canvas.tag_raise("mana_actual_entitats", "mana_entitats")

            textmana = f"{round(ent[1].StatsCombat["Mana"])}/{round(ent[1].StatsCombat["MaxMana"])}"
            midatext = font.measure(textmana)

            self.canvas.create_text(
                self.app.Ancho - 20 - midatext, y + 90,
                text=textmana,
                fill="black",
                font=("Courier", 11, "bold"),
                anchor="nw", tags=("info_enemics", "zona_enemics", "combat")
            )


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
                    tags=("ent_estat", "mostrar_estat")
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
                160, 240, False
                )
            })
            
            self.canvas.create_image(
                    x + 10, y + 10,
                    image=ent[1].ImatgeAjustada["Combat"]["Frontal"],
                    anchor="nw",
                    tags=("ent_estat", "mostrar_estat")
                )
            x += 150 if len(self.equip) > 1 else 210
            
    def dibuixar_seleccio_accio(self):
        self.canvas.create_rectangle(
            5, self.app.Alto - 200,
            self.app.Ancho - 5, 
            self.app.Alto - 5,
            fill="white", outline="black",
            width=5, tags=("zona_seleccio", "combat")
        )

        self.canvas.create_rectangle(
            5, self.app.Alto - 200,
            self.app.Ancho - 5, 
            self.app.Alto - 5,
            fill="white", outline="black",
            width=5, tags=("zona_descripcio", "combat")
        )

        for i in self.OpcionsCombat:
            pass

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
            if i.StatsCombat["SPD"] == maxSpeed:
                i.Priority = 100
            else:
                i.Priority = (i.StatsCombat["SPD"] / maxSpeed) * 100

            amplada = self.app.Ancho - 80
            x = amplada * (i.Priority / 100)

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
                width=5, tags=(f"accio_entitat_aliada_{pos}", "barra_accio", "zona_accio", "combat")
            )

            self.canvas.create_rectangle(
                x, y,
                x - 30, 
                55,
                fill="white", outline="gray",
                width=1, tags=(f"accio_entitat_aliada_{pos}", "barra_accio", "zona_accio", "combat")
            )

            self.canvas.create_image(
                x - 25, y,
                image=i.ImatgeAjustada["Accio"]["Frontal"],
                anchor="nw",
                tags=(f"accio_entitat_aliada_{pos}", "ent_estat", "mostrar_estat")
            )


        for pos, j in enumerate(self.enemic.values()):
            if j.StatsCombat["SPD"] == maxSpeed:
                j.Priority = 100
            else:
                j.Priority = (j.StatsCombat["SPD"] / maxSpeed) * 100

            amplada = self.app.Ancho - 80
            x = amplada * (j.Priority / 100)

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
                width=5, tags=(f"accio_entitat_enemiga_{pos}", "barra_accio", "zona_accio", "combat")
            )

            self.canvas.create_rectangle(
                x, y,
                x - 30, 
                55,
                fill="white", outline="gray",
                width=1, tags=(f"accio_entitat_enemiga_{pos}", "barra_accio", "zona_accio", "combat")
            )

            self.canvas.create_image(
                x - 25, y,
                image=j.ImatgeAjustada["Accio"]["Frontal"],
                anchor="nw",
                tags=(f"accio_entitat_enemiga_{pos}", "ent_estat", "mostrar_estat")
            )

    def IncrementarPrioritat(self):
        for pos, i in enumerate(self.equip.values()):
            if i.StatsCombat["CurHP"] > 0:
                i.Priority += i.StatsCombat["SPD"] / 100
                amplada = self.app.Ancho - 80
                x = amplada * (j.Priority / 100)

                old_x = self.canvas.coords(f"accio_entitat_aliada_{pos}")
                x -= old_x[0]

                self.canvas.move(f"accio_entitat_aliada_{pos}", x, 0)
        
        for pos, j in enumerate(self.enemic.values()):
            if j.StatsCombat["CurHP"] > 0:
                j.Priority += j.StatsCombat["SPD"] / 100
                amplada = self.app.Ancho - 80
                x = amplada * (j.Priority / 100)

                old_x = self.canvas.coords(f"accio_entitat_enemiga_{pos}")
                x -= old_x[0]

                self.canvas.move(f"accio_entitat_enemiga_{pos}", x, 0)
        
        self.app.root.after(10, self.Lluitar)

    def Lluitar(self):
        if self.combat == True and self.fugir[0] == False: 
            # Turn Aliat
            for aliat in self.equip.values():
                # if aliat.Priority >= 100 and len(self.enemic) >= 1 and aliat.StatsCombat["CurHP"] > 0.1 and self.combat == True:
                #     turn = True
                #     while turn == True:
                #         turn = False
                #         self.AccionsLluita(aliat)
                        
                #         if turn == False:
                #             aliat.Priority = 0
                # if self.combat == True:
                #     self.ComprobarFiCombat()
                aliat.Priority = 0

            # Turn enemic
            for j in self.enemic.values():
                if j.Priority >= 100 and self.fugir[0] == False and len(self.equip) >= 1 and j.StatsCombat["CurHP"] > 0 and self.combat == True:
                    pass
                    # UIManager.ClearScreen()
                    # UIManager.BattleScreenShow(jugador.Team)
                    # UIManager.BattleScreenShow(enemy)
                    # enemyMove = random.choice([e for e in j.Moves.values()])
                    # targetable = [e.id for e in jugador.Team.values() if e.StatsCombat["CurHP"] > 0]
                    # # for e in jugador.Team.values():
                    # #     if e.StatsCombat["CurHP"] > 0:
                    # #         targetable.append(e)
                    # target = random.choice(targetable)
                    # jugador.Team, derrotats = j.atacar(jugador.Team, target, enemyMove)
                    # j.Priority = 0
                    # j, derrotats = ComprobarEfectEstat(j, derrotats)
                    # teamderr = DescartarDerrotats(derrotats, teamderr, jugador, event, exits)
                    # UIManager.ClearScreen()
                # if combat == True:
                #     combat = ComprobarFiCombat(combat, enemyderr, enemy, teamderr, event, missions, jugador)
            
            self.IncrementarPrioritat()
        # self.finalitzarCombat()

    def DescartarDerrotats(llista, derr, jugador, event, exits):
        for p in llista:
            if p.StatsCombat["CurHP"] <= 0.1:
                derr += 1
                if p.isPlayer == False:
                    UIManager.ClearScreen()
                    alive = 0
                    for i in jugador.Team.values(): 
                        if i.StatsCombat["CurHP"] > 0:
                            i.LvlUp(event, jugador, exits, p)
                            alive += 1
                    if alive >= 1:
                        jugador.Gold += p.Lv * 10 # 10 monedes per cada nivell, representa que es ven el derrotat.
                        print(f"Has guanyat {p.Lv * 10} gold.")
                        input("Presiona per a continuar...")
        return derr

    def ComprobarFiCombat(combat, enemyderr, enemy, teamderr, event, missions, jugador):
        if enemyderr == len(enemy) or teamderr == len(jugador.Team):
            combat = False
            if len(enemy) == enemyderr:
                UIManager.ClearScreen()
                print("Tos els enemics han estat derrotats !!")
                input("Presiona per a continuar")
                for id, val in enemy.items():
                    event.CridarEvent("Derrotar Enemic", val, jugador, missions)
        return combat


    def finalitzarCombat(clon, jugador):
        for i in jugador.Team.keys(): 
            # if i in clon.keys():
            #     jugador.Team[i].StatsCombat["CurHP"] = clon[i].StatsCombat["CurHP"]
            #     jugador.Team[i].StatsCombat["Mana"] = clon[i].StatsCombat["Mana"]
            # else:
            #     i.StatsCombat["CurHP"] = 0
            #     i.StatsCombat["Mana"] = 0
            jugador.Team[i].afected = []
            jugador.Team[i].DefinirCombatStats()

    def ComprobarEfectEstat(entitat, derrotats = []):
        if len(entitat.afected) > 0:
            eliminar = []
            for i in entitat.afected:
                if i.RemainingTurns <= 0 and i.Turns > 0:
                    statsafected = entitat.afected.StatEffects[1][0]
                    eliminar.append(i)
                    # Regenerar Estadistiques
                    print(f"{entitat.nom}, ja no esta afectat per {i.Name}, les seves estadistiques han retornat al que eren...")
                elif entitat.StatsCombat["CurHP"] > 0:
                    if i.Damage > 0:
                        damagepereffect = ((entitat.StatsCombat["MaxHP"] / 100) * i.Damage)
                        entitat.StatsCombat["CurHP"] -= damagepereffect
                        print(f"{entitat.nom}, ha perdut {round(damagepereffect, 2)} HP degut a la {i.Name}.")
                        if entitat.StatsCombat["CurHP"] <= 0:
                            print(f"{entitat.nom}, ha estat derrotat per {i.Name}.")
                            derrotats.append(entitat)
                    i.RemainingTurns -= 1
            for j in eliminar:
                entitat.afected.remove(j)
        return entitat, derrotats

    def MenuAtacar(personatge):
        UIManager.ClearScreen()
        
        UIManager.CrearMenu(personatge.Moves.items(), "Moviments", "Moves")

        sel = UIManager.MostrarMenus(UIManager.Menus["Moviments"])
        if sel != None:
            use = personatge.Moves[sel]
            if use.Cost > personatge.StatsCombat["Mana"]:
                print("No tens suficient Mana per a realitzar aquest atac...")
                input("Presiona per a continuar...")
                return None
            else:
                return use
        else:
            return sel
        
    def AccionsLluita(atacant, jugador, enemy, enemyderr, objectes, event, exits):
        print(f"És el torn de {atacant.nom}")
        
        seleccio = UIManager.MostrarMenus(UIManager.Menus["Accions Lluita"], False, True, jugador, enemy)
        
        turn = False
        fugir = [False]
        
        print("\n")
        if seleccio == "atacar":
            move = MenuAtacar(atacant)
            target = None
            UIManager.ClearScreen()
            UIManager.BattleScreenShow(jugador.Team)
            UIManager.BattleScreenShow(enemy)
            print("\n")
            if move != None:
                if move.MultiTarget == False:
                    if move.Healing == False and move.Protective == False:
                        if len(enemy) > 1:
                            target = TriarObjectius(enemy)
                        else:
                            target = "enemy_0"
                    elif move.Healing == True or move.Protective == True:
                        target = TriarObjectius(jugador.Team)
                else:
                    target = "All"
                if target != None:
                    if move.Healing == False and move.Protective == False:
                        enemy, derrotats = atacant.atacar(enemy, target, move)
                        enemyderr = DescartarDerrotats(derrotats, enemyderr, jugador, event, exits)
                    else:
                        jugador.Team = atacant.MoveProtHeal(jugador.Team, target, move)
            
            if move == None or target == None:
                turn = True
            else:
                atacant.StatsCombat["Mana"] -= move.Cost

        elif seleccio == "fugir":
            fugir = Fugir(enemy, jugador)
            if fugir[0] == False:
                atacant, derrotats = ComprobarEfectEstat(atacant)
        elif seleccio == "motxila":
            obj = jugador.ObjectesMochila(objectes, True)
            used = None

            if obj != None:
                used = UseObject(jugador, jugador.Team, obj, True)
            if obj == None or used == None:
                turn = True
        elif seleccio == "status":
            UIManager.VeureEstatus(jugador, True)
            turn = True
        elif seleccio == "pasar":
            print("Has decidit pasar torn...")
            input("Presiona per a continuar...")
        
        return atacant, enemy, turn, fugir, enemyderr

    def TriarObjectius(list):

        UIManager.ClearScreen()
        targetable = [i for i in list.items() if i[1].StatsCombat["CurHP"] > 0]
        
        UIManager.CrearMenu(targetable, "Qui és l'objectiu?", "Entitat")

        target = UIManager.MostrarMenus(UIManager.Menus["Qui és l'objectiu?"], True)
            
        return target

    def UseObject(jugador, equip, obj, combat = False):
        target = TriarObjectius(equip)
        if target != None:
            obj.Utilitzar(jugador.Team[target])
            if jugador.objectes[obj.id]["amount"] > 1:
                jugador.objectes[obj.id]["amount"] -= 1
            else:
                jugador.objectes.pop(obj)
            UIManager.CrearMenu(jugador.objectes.items(), "Motxila", "Objectes", opcionsvisibles=6)
            if combat == False:
                return ""
        else:
            return None
            

    def Fugir(enemy, jugador):
        print("Has intentat Fugir...")
        teamSPD = 0
        for i in jugador.Team.values():
            teamSPD += i.StatsCombat["SPD"]
        enemySPD = 0
        for j in enemy.values():
            enemySPD += j.StatsCombat["SPD"]
        prob = jugador.fleeProb * (teamSPD / enemySPD)   # fleeProb = 75 de base
    
        # 75% base * resultat de velocitat del jugador entre la del enemic. (75 * (22 / 20) = 1.1) = 82.5)
        if prob < 100:
            fugir = random.choices([True, False], cum_weights=[prob, 100 - prob])
        else:
            fugir = [True]
        if fugir[0] == True:
            print("Has aconseguit escapar !!")
        else:
            print("No has aconseguit escapar...")
        return fugir