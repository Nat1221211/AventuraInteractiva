# Arxiu: SaveGame.py
# Autor: Bernat Puig Casals
# Data: 7 de Març de 2026
# Descripcio:
# Creem el modul per a guardar i carregar la partida.

import csv
import json
import os

# Importar Classes
from Classes import Entitat
from Classes import Player
from Classes import Objectes

import UIManager
from Classes import Utilitats

def GuardarPartida(App, jugador, missions):

    dades = {
        # Detalls Generals
        "Nom": jugador.Name,
        "Ubicacio": jugador.Ubicacio.id,
        "Or": jugador.Gold,
        "Ultim_Visitat": jugador.UltimPobleVisitat.id,
        
        # Seguiment
        "Missions_Acceptades": {},
        "Missions_Finalitzades": jugador.MissionsFinalitzades,
        "Missions_Disponibles": {},
        "Llocs_Trobats": jugador.LlocsTrobats,
        "Llocs_Visitats": jugador.LlocsVisitats,
        "AchievementsProgress": {},
        "AchievementsObtained": jugador.AcquiredAchievements,

        # Equip Jugador
        "Team": [],

        # Inventari
        "Inventari": {},

        # Altres
        "Titols": [],

        "Estadistiques": {},
        "Increment_Stats": jugador.StatIncrement,
        "Companys": []
    }
    dades["Team"]=GuardarPersonatges(jugador.Team)
    dades["Inventari"]=GuardarInventari(jugador)
    dades["Missions_Acceptades"]=GuardarMissions(jugador.MisionsAcceptades, missions)
    dades["Missions_Disponibles"]=GuardarMissions(jugador.MissionsDisponibles, missions)

    ruta = os.path.dirname(__file__)
    ruta_final = os.path.join(ruta, "Saves/save.json")
    with open(ruta_final, "w", encoding="utf-8") as save:
        json.dump(dades, save, indent=4, ensure_ascii=False)
    
    App.Enrere()

def CarregarPartida(partida, missions, objectes, zones, entitats):
    with open(partida, "r", encoding="utf-8") as save:
        dades = json.load(save)

    equip = {}
    for i in dades["Team"]:
        equip.update({
                i["id"]:
                Entitat.Entity(i["id"], i["Nom"], i["Lv"], True,
                               entitats[i["Base"]], i["Lv_Limit"],
                               i["XP"])
            }
        )

    ubicacio = zones[dades["Ubicacio"]]
    ultim_visitat = zones[dades["Ultim_Visitat"]]

    missions_acceptades = []
    for id, value in dades["Missions_Acceptades"].items():
        missions_acceptades.append(id)
        if value["type"] == "Kill":
            missions[value["type"]][id].Count = value["Progress"]
        missions[value["type"]][id].Status = value["Status"]
    
    missions_disponibles = []
    for id, value in dades["Missions_Disponibles"].items():
        missions_disponibles.append(id)
        missions[value["type"]][id].Status = value["Status"]

    inventari = {}
    for o in dades["Inventari"]:
        inventari.update({o["id"]: {"objecte": objectes[o["Clase"]][o["id"]], "amount": o["Amount"]}})

    jugador = Player.Player(dades["Nom"], equip, ubicacio)
    jugador.MissionsFinalitzades = dades["Missions_Finalitzades"]
    jugador.MissionsDisponibles = missions_disponibles
    jugador.LlocsTrobats = dades["Llocs_Trobats"]
    jugador.LlocsVisitats = dades["Llocs_Visitats"]
    jugador.MisionsAcceptades = missions_acceptades
    jugador.Gold = dades["Or"]
    jugador.objectes = inventari
    jugador.UltimPobleVisitat = ultim_visitat
    jugador.StatIncrement = dades["Increment_Stats"]
    jugador.AplicarStatsGenerals()

    for k, v in jugador.Team.items():
        v.DefinirCombatStats()

    return jugador


def GuardarExits(exits):
    for id, value in exits:
        print()

def GuardarMissions(aguardar, missions):
    guardar = {}
    for id, value in missions.items():
        for id2, mision in value.items():
            if id2 in aguardar:
                progres = 0
                if id == "Kill":
                    progres = mision.Count
                status = mision.Status
                        

                guardar.update(
                    {
                        id2: {
                            "id": id2,
                            "type": id,
                            "Progress": progres,
                            "Status": status
                        }
                    }
                )
    return guardar
        

def GuardarInventari(jugador):
    inventari = []
    for id, dict in jugador.objectes.items():
        if isinstance(dict["objecte"], Objectes.ObjecteCombat):
            clase = "Combat"
        elif isinstance(dict["objecte"], Objectes.ObjecteClau):
            clase = "Clau"

        inventari.append(
            {
                "id": dict["objecte"].id,
                "Amount": dict["amount"],
                "Clase": clase
            }
        )
    return inventari

def GuardarPersonatges(personatges):
    equip = []
    for id, val in personatges.items():
        # moves = []
        # for id, v in val.Moves.items():
        #     moves.append(id)
        # Aixo en cas de necessitar canviar algo amb els moviments, 
        # o de posar un limit als que es poden tenir al mateix temps...

        afected = []
        for effect in val.afected:
            afected.append(
                {
                    "id": effect.Name,
                    "Remaining_Turns": effect.Turns
                }
            )

        equip.append(
            {
                "id": id,
                "Nom": val.nom,
                "Base": val.base.id,
                "Lv": val.Lv,
                "Lv_Limit": val.LvLimit,
                "Moves": [],
                "Afected": afected,
                "XP": val.Xp,
            }
        )

    return equip
