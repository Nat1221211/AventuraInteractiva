# Arxiu: PrepararCridar.py
# Autor: Bernat Puig Casals
# Data: 7 de Març de 2026
# Descripcio:
# Creem el modul per a guardar i carregar la partida.

import csv
import json
import os

def GuardarPartida(jugador, missions):
    dades = {
        # Detalls Generals
        "Nom": jugador.Name,
        "Ubicació": jugador.Ubicacio.id,
        "Or": jugador.Gold,
        "Ultim_Visitat": jugador.UltimPobleVisitat.id,
        
        # Seguiment
        "Missions_Acceptades": jugador.MisionsAcceptades,
        "Missions_Finalitzades": jugador.MissionsFinalitzades,
        "Missions_Disponibles": jugador.MissionsDisponibles,
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
    
    ruta = os.path.dirname(__file__)
    ruta_final = os.path.join(ruta, "Saves/save.json")
    with open(ruta_final, "w", encoding="utf-8") as save:
         json.dump()

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
