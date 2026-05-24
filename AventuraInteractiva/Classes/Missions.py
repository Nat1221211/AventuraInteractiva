# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe Mission.

import random
from Classes import Entitat
from Classes import Objectes
from Classes import Zones
from Classes import EntityType

import os
from tkinter import font as tkfont

class Mission():
    
    Name = ""
    Description = ""
    Status = "Bloquejada"
    Rewards = {}
    Requisite = []
    Place = Zones.Zona
    Finished = False
    Categoria = ""
    # Metodes
    def __init__(self, iden, name, description, rewards, cat):
        self.id = iden
        self.Name = name
        self.Description = description
        self.Rewards = rewards
        self.Categoria = cat
    


    
    def MostrarRecompenses(self, app):
        text = f"Recompenses: "
        if "XP" in self.Rewards.keys():
            text += f"\n  - XP: {self.Rewards["XP"]}"
        if "Gold" in self.Rewards.keys():
            text += f"\n  - Or: {self.Rewards["Gold"]}"
        if "Objects" in self.Rewards.keys():
            text += f"\n  - Objects: "
            for object in self.Rewards["Objects"]:
                text += f"\n    + {app.Objects[object["type"]][object["id"]].ObjectName} x{object["Amount"]}"
        
        return text

    def ShowRequisites(self):
        if len(self.Requisite) > 0:
            print("-- Requisites:")
            for i in self.Requisite:
                if type(i) == tuple:
                    if i[0] == "Lv":
                        print(f"    Player Level >= {i[1]}")
                elif type(i) in [Mission, FindMission, ObjectMission, KillMission]:
                    print(f"    {i.Name} Completed")
            print("\n")

    def MissioDesbloquejable(self, jugador):
        resultat = True
        for key, value in self.Requisite.items():
            if key == "Lv":
                if jugador.Team["Player"].Lv < value:
                    resultat = False
            elif key == "Mission":
                for id in self.Requisite["Mission"]:
                    if id not in jugador.MissionsFinalitzades:
                        resultat = False        
        return resultat
    
    def Reclamar(self, app):
        if self.Status == "Pendent Reclamar":
            for id, value in self.Rewards.items():
                if id == "Gold":
                    app.jugador.Gold += value
                elif id == "Objects":
                    for obj in value:
                        app.jugador.AfegirObjecte(app.Objects[obj["type"]][obj["id"]], obj["Amount"])
                elif id == "Title":
                    app.jugador.Titles.append(value)
            self.Status = "Completada"
            app.jugador.MissionsFinalitzades.append(self.id)
            app.jugador.MisionsAcceptades.remove(self.id)
            app.event.CridarEvent("Missio Finalitzada", self, app)
            return True
        else:
            return False
    
    def dibuixar_Pantalla_Reclamar_Missio(self, app):
        app.ReclamarMissio = True

        app.canvas.delete("all")
        app.canvas.create_rectangle(
            5, 5,
            app.Ancho - 5, 
            app.Alto -5,
            fill="white", outline="black",
            width=5, tags="reclamar_missio"
        )

        app.canvas.create_rectangle(
            5, 5,
            app.Ancho - 5, 
            75,
            fill="white", outline="black",
            width=5, tags=("enunciat", "reclamar_missio")
        )

        enunciat = "Missio Completada !!"
        
        font = tkfont.Font(family="Courier", size=24, weight="bold")
        mida = font.measure(enunciat)

        app.canvas.create_text(
            (app.Ancho // 2) - (mida // 2), 40,
            text=enunciat,
            fill="black",
            font=("Courier", 24, "bold"),
            anchor="w", tags=("text_enunciat", "enunciat", "reclamar_missio")
        )

        app.canvas.create_rectangle(
            5, 80,
            app.Ancho - 5, 
            395,
            fill="white", outline="black",
            width=5, tags=("zona_objectes", "fi_combat")
        )

        app.canvas.create_text(
            30, 110,
            text="Objectes Adquirits",
            fill="black",
            font=("Courier", 24, "bold"),
            anchor="w", tags=("enunciat_objectes", "zona_objectes", "reclamar_missio")
        )

        app.canvas.create_rectangle(
            5, 400,
            app.Ancho - 5, 
            app.Alto - 5,
            fill="white", outline="black",
            width=5, tags=("zona_experiencia", "reclamar_missio")
        )

        x = 5
        y = 400
        
        for num, ally in enumerate(app.jugador.Team.values()):
            salt = 295 if num <= 2 else 300
            app.canvas.create_rectangle(
                x, y,
                x + salt, 
                app.Alto - 5,
                fill="white", outline="black",
                width=5, tags=("zona_experiencia", "reclamar_missio")
            )
            if "MostrarExp" not in ally.ImatgeAjustada.keys():
                ally.ImatgeAjustada["MostrarExp"]={}

            ally.ImatgeAjustada["MostrarExp"].update({
                "Frontal":
                app.RedimensionarImatge(
                ally.Imatges["Frontal"],
                60, 90, False
                )
            })
            
            app.canvas.create_image(
                x + 20, y + 20,
                image=ally.ImatgeAjustada["MostrarExp"]["Frontal"],
                anchor="nw",
                tags=("zona_experiencia", "reclamar_missio")
            )
            
            app.canvas.create_text(
                x + 95, y + 25,
                text=ally.nom,
                fill="black",
                width=180,
                font=("Courier", 16, "bold"),
                anchor="nw", tags=("zona_experiencia", "reclamar_missio")
            )

            app.canvas.create_text(
                x + 95, y + 55,
                text=f"Lv: {ally.Lv} / {ally.LvLimit}",
                fill="black",
                font=("Courier", 16, "bold"),
                anchor="nw", tags=(f"text_nivell_{ally.id}", "zona_experiencia", "reclamar_missio")
            )

            app.canvas.create_rectangle(
                x + 20, app.Alto - 65,
                x + salt - 20, 
                app.Alto - 45,
                fill="white", outline="black",
                width=5, tags=(f"barra_xp_fons_{ally.id}", "zona_experiencia", "reclamar_missio")
            )

            percentatgeXP = (round(ally.Xp, 2) / round(ally.XpRequired, 2))
            amplebarraxp = (salt - 20 - 20)
            midabarraxp = amplebarraxp * percentatgeXP
            
            app.canvas.create_rectangle(
                x + 20, app.Alto - 65,
                x + 20 + midabarraxp, 
                app.Alto - 45,
                fill="cyan",
                width=5, tags=(f"barra_xp_{ally.id}", "zona_experiencia", "reclamar_missio")
            )

            text_xp = f"{round(ally.Xp, 2)} / {round(ally.XpRequired, 2)}"
            app.canvas.create_text(
                x + 20, app.Alto - 40,
                text=f"EXP: {text_xp}",
                fill="black",
                font=("Courier", 14, "bold"),
                anchor="nw", tags=(f"text_experiencia_{ally.id}", "zona_experiencia", "reclamar_missio")
            )
            
            x+= salt
        
        clonrecompenses = {}
        clonobjectes = self.Rewards["Objects"].copy()
        for pos, ent in enumerate(app.jugador.Team.values()):
            clonrecompenses.update({ent.id: self.Rewards["XP"]})
        
        app.levelingUp = True
        self.dibuixar_experiencia_pantalla_missions(app, clonrecompenses, clonobjectes)

    def dibuixar_experiencia_pantalla_missions(self, app, experienciarestant, clonobjectes = None):
    # En aquesta només incrementarem la barra i creearem la de color, i la reduirem a zero si ja esta al limit del nivell
    # enunciarem que s'ha pujat de nivell, etc...
        for num, ally in enumerate(app.jugador.Team.values()):
            levelUp = False
            if ally.id in experienciarestant.keys():
                if experienciarestant[ally.id] > (ally.XpRequired / 100) and app.saltarPantallaReclamarMissio == False:
                    levelUp = ally.LvlUp((ally.XpRequired / 100))
                    experienciarestant[ally.id] -= (ally.XpRequired / 100)
                else:
                    if app.saltarPantallaReclamarMissio == True:
                        app.levelingUp = False
                    levelUp = ally.LvlUp(experienciarestant[ally.id])
                    experienciarestant[ally.id] = 0

            midesBarraFons = app.canvas.coords(f"barra_xp_fons_{ally.id}")

            coordsBarraXP = app.canvas.coords(f"barra_xp_{ally.id}")
            percentatgeXP = (round(ally.Xp, 2) / round(ally.XpRequired, 2))
            amplebarraxp = midesBarraFons[2] - midesBarraFons[0]
            coordsBarraXP[2] = coordsBarraXP[0] + (amplebarraxp * percentatgeXP)
    
            coordsBarraXP = app.canvas.coords(f"barra_xp_{ally.id}", coordsBarraXP)

            text_xp = f"EXP: {round(ally.Xp, 2)} / {round(ally.XpRequired, 2)}"
            app.canvas.itemconfig(f"text_experiencia_{ally.id}", text=text_xp)
        
            if levelUp == True:
                posicio = app.canvas.coords(f"text_nivell_{ally.id}")
                app.canvas.create_text(
                    posicio[0], posicio[1] + 20,
                    text=f"Level UP !!",
                    fill="black",
                    font=("Courier", 14, "bold"),
                    anchor="nw", tags=(f"text_pujatnivell_{ally.id}", "zona_experiencia", "reclamar_missio")
                )
                app.canvas.itemconfig(f"text_nivell_{ally.id}", text=f"Lv: {ally.Lv} / {ally.LvLimit}")

        completats = 0
        for i in experienciarestant.values():
            if i == 0:
                completats+=1
        if completats == len(experienciarestant.keys()):
            app.levelingUp = False
           
        
        if app.levelingUp == True:
                if clonobjectes != None and len(clonobjectes) > 0:
                    app.ObtainingObjects = True
                else:
                    app.ObtainingObjects = False

                if app.ObtainingObjects == False:
                    if app.ObjectesDibuixats == False:
                        app.canvas.create_text(
                            30, 140,
                            text="No s'han adquirit objectes en aquest combat...",
                            fill="black",
                            font=("Courier", 18, "bold"),
                            anchor="w", tags=("text_objectes", "zona_objectes", "reclamar_missio")
                        )
                        app.ObjectesDibuixats = True
                    app.levelAnimation = app.root.after(10, lambda: self.dibuixar_experiencia_pantalla_missions(app, experienciarestant))
                else:
                    
                    if app.ObtainingObjects == True:
                        app.ObjectsAnimation = app.root.after(10, lambda: self.dibuixar_objectes_pantalla_missions(app, 140, clonobjectes, experienciarestant))
                    else:
                        app.levelAnimation = app.root.after(10, lambda: self.dibuixar_experiencia_pantalla_missions(app, experienciarestant, clonobjectes))

        else:
            if app.levelAnimation != None:
                app.root.after_cancel(app.levelAnimation)
                app.ReclamarMissioFinalitzat = True

    def dibuixar_objectes_pantalla_missions(self, app, y, objectesrestants, experienciarestant):

        ultimObjecte = objectesrestants[-1]
        objectesrestants.pop(-1)

        app.canvas.create_text(
            30, app.YRecompenses,
            text=f"{app.Objects[ultimObjecte["type"]][ultimObjecte["id"]].ObjectName}",
            fill="black",
            font=("Courier", 18, "bold"),
            anchor="w", tags=("text_objectes", "zona_objectes", "reclamar_missio")
        )
        app.canvas.create_text(
            400, app.YRecompenses,
            text=f"x{ultimObjecte["Amount"]}",
            fill="black",
            font=("Courier", 18, "bold"),
            anchor="w", tags=("text_objectes", "zona_objectes", "reclamar_missio")
        )
        app.ObjectesDibuixats = True
        app.YRecompenses+= 30

        app.levelAnimation = app.root.after(10, lambda: self.dibuixar_experiencia_pantalla_missions(app, experienciarestant, objectesrestants))





    
class FindMission(Mission):
    
    Objective = {}
    
    # Metodes
    def __init__(self, iden, name, description, cat, rewards, objective, requisite):
        self.id = iden
        self.Name = name
        self.Description = description
        self.Categoria = cat
        self.Rewards = rewards
        self.Objective = objective
        self.Requisite = requisite
    
    def TextProgres(self, app):

        text = f"Missio {self.Categoria} \nVisitat {self.Objective["find"]}: "

        if self.Status == "Pendent Reclamar":
            text += "Progres: 1 / 1"
        else:
            text += "Progres: 0 / 1"

        return text


class ObjectMission(Mission):
    
    Objective = {}
    
    # Metodes
    def __init__(self, iden, name, description, cat, rewards, objective, requisite):
        self.id = iden
        self.Name = name
        self.Description = description
        self.Categoria = cat
        self.Rewards = rewards
        self.Objective = objective
        self.Requisite = requisite
    
    def TextProgres(self, app):

        text = f"Missio {self.Categoria} \nTrobar en/la {self.Objective["ObjName"]}: "

        if self.Status == "Pendent Reclamar":
            text += "Progres: 1 / 1"
        else:
            text += "Progres: 0 / 1"

        return text
  
class PlaceMission(Mission):
    
    Objective = Zones.Zona
    
    # Metodes
    def __init__(self, iden, name, description, cat, rewards, objective, requisite):
        self.id = iden
        self.Name = name
        self.Description = description
        self.Categoria = cat
        self.Rewards = rewards
        self.Objective = objective
        self.Requisite = requisite
    
    def TextProgres(self, app):

        text = f"Missio {self.Categoria} \nArribar a {app.Zones[self.Objective["place"]].NameZone}: "

        if self.Status == "Pendent Reclamar":
            text += "Progres: 1 / 1"
        else:
            text += "Progres: 0 / 1"
        
        return text


class KillMission(Mission):
    
    Objective = []
    Count = 0
    
    # Metodes
    def __init__(self, iden, name, description, cat, rewards, objective, requisite, generic = True, entitats = None):
        self.id = iden
        self.Name = name
        self.Description = description
        self.Categoria = cat
        self.Rewards = rewards
        self.Objective = objective
        self.Requisite = requisite
        self.Generic = generic
        self.Count = 0
        if self.Generic == False:
            self.Enemic = {}
            
            for pos, j in enumerate(self.Objective["enemy"]):
                self.Enemic.update({
                    f"enemy_{pos}":
                    Entitat.Entity(f"enemy_{pos}", j["name"],
                                    j["level"], False, entitats[j["entity"]])
                })

    def IncrementCount(self, enemy):
        if self.Generic == True:
            if enemy.base in self.Objective:
                self.Count += 1
            if self.Count >= self.Quantity:
                os.system("cls" if os.name == "nt" else "clear")
                self.Status = "Rewards Unclaimed"
                print(f"\nHas completat la missió {self.Name}.\n")
                input("Presiona per a continuar...")
        else:
            if enemy == self.Enemic:
                self.Status = "Rewards Unclaimed"
        
    def TextProgres(self, app):

        if self.Generic == True:
            text = f"Derrotar {self.Objective["Amount"]}"
            if len(self.Objective["enemy"]) > 1:
                text+= "dels seguents enemics:\n"

                for pos, i in enumerate(self.Objective["enemy"]):
                    ent = app.Entities[i]
                    if pos != 0:
                        text += ", "
                    text += f"{ent.EntityName}"
            else:
                text+= f" enemics de tipus {app.Entities[self.Objective["enemy"][0]].EntityName}."
            text += f"\n"
        else:
            nom_entitat = self.Objective["enemy"][0]["name"]

            text = f"Missio {self.Categoria} \nDerrotar {nom_entitat}: "

        text += f"Progres: {self.Count} / {self.Objective["Amount"]}"

        return text