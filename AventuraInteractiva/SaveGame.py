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


def GuardarPartida(jugador, missions):
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

        # Equip Jugador
        "Team": [],

        # Inventari
        "Inventari": {},

        # Altres
        "Titols": [],

        "Estadistiques": {},
        "Increment_Stats": {},
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
        inventari.update({objectes[o["Clase"]][o["id"]]: o["Amount"]})

    jugador = Player.Player(dades["Nom"], equip, ubicacio)
    jugador.MissionsFinalitzades = dades["Missions_Finalitzades"]
    jugador.MissionsDisponibles = missions_disponibles
    jugador.LlocsTrobats = dades["Llocs_Trobats"]
    jugador.LlocsVisitats = dades["Llocs_Visitats"]
    jugador.MisionsAcceptades = missions_acceptades
    jugador.Gold = dades["Or"]
    jugador.objectes = inventari
    jugador.UltimPobleVisitat = ultim_visitat

    UIManager.CrearMenu(jugador.objectes.items(), "Motxila", "Objectes",jugador, opcionsvisibles=6)

    return jugador


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
    for obj, amt in jugador.objectes.items():
        if isinstance(obj, Objectes.ObjecteCombat):
            clase = "Combat"
        elif isinstance(obj, Objectes.ObjecteClau):
            clase = "Clau"

        inventari.append(
            {
                "id": obj.id,
                "Amount": amt,
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
