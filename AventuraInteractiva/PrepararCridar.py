# Arxiu: PrepararCridar.py
# Autor: Bernat Puig Casals
# Data: 2 de Febrer de 2026
# Descripcio:
# Creem el modul per a crear o cridar els valors dels documents quan siguin necessaris.


# Altres Imports
import os
import json

# Moduls
from Classes import Characteristics
from Classes import Entitat
from Classes import EntityType
from Classes import Exits
from Classes import Missions
from Classes import Objectes
from Classes import Titles
from Classes import Zones
from Classes import Utilitats
import PrepararCridar as Call

from PIL import Image


def CallCSV(cami):
    try:
        base_path = os.path.dirname(__file__)
        ruta = os.path.join(base_path, cami)

        with open(ruta, "r", encoding="utf-8") as Entities:
            data = Entities.read().splitlines(False)
            caps = data[0].strip().split(";")

            Data = []
            DictData = {}
            for i in data[1:]:
                linia = i.strip().split(";")
                for j in range(len(linia)):
                    linia[j] = linia[j].strip()
                    if caps[j].endswith("?"):
                        if linia[j] == "TRUE":
                            linia[j] = "True"
                        elif linia[j] == "FALSE":
                            linia[j] = "False"
                        linia[j] = eval(linia[j])
                    elif linia[j].isnumeric():
                        linia[j] = int(linia[j])
                    elif len(linia[j].split(": ")) > 1:
                        items = linia[j].split("| ").copy()
                        linia[j] = dict()
                        for v in items:
                            kv = v.strip().split(": ")
                            linia[j][kv[0]] = kv[1] if kv[1].endswith("%") or kv[0].startswith("Titol") else float(kv[1])
                    elif len(linia[j].split("| ")) > 1:
                        linia[j] = linia[j].split("| ")
                    DictData[caps[j]] = linia[j]
                Data.append(DictData.copy())
            return Data


    except FileNotFoundError:
        print("Ha ocurregut un error carregant el fitxer...")

def CallEntity(movements):
    entitats = CallCSV("Data/EntityTypes.csv")
    entities = {}
    for i in entitats:
        moves = {}
        for m, n in i["Movements"].items():
            if m not in moves.keys():
                dictio = {
                    "Move": movements[m],
                    "Lv": n
                }
                moves.update({m: dictio})
        
        base_path = os.path.dirname(__file__)
        ruta_imatges_entitat = os.path.join(base_path, f"Assets/Entities/{i["id"]}_sprite")

        entitat = EntityType.EntityType(i["id"], i["Nom"],  i["Playable?"], i["Vida"], i["Mana"], i["ATK"], i["INT"], 
                                        i["DEF"], i["SPD"], i["XP"], i["Groups"],  i["Descripcio"], moves)
        
        
        imatges = {}
        if os.path.exists(ruta_imatges_entitat):
            if os.path.exists(os.path.join(ruta_imatges_entitat, f"front.png")):
                imatges.update({"Frontal": os.path.join(ruta_imatges_entitat, f"front.png")})
            if os.path.exists(os.path.join(ruta_imatges_entitat, f"back.png")):
                imatges.update({"Back": os.path.join(ruta_imatges_entitat, f"back.png")})
            if os.path.exists(os.path.join(ruta_imatges_entitat, f"mini.png")):
                imatges.update({"Mini": os.path.join(ruta_imatges_entitat, f"mini.png")})
        else:
            imatges.update({"Frontal": os.path.join(base_path, f"Assets/Entities/undefined_sprite/front.png")})
            imatges.update({"Back": os.path.join(ruta_imatges_entitat, f"Assets/Entities/undefined_sprite/back.png")})

        entitat.AddImages(imatges)

        entities.update({i["id"]: entitat})
    return entities

def CallEfect():
    effects = CallCSV("Data/effects.csv")
    efectes = {}
    for i in effects:
        if i["ImpedeixAccions?"] == True:
            bloqueig = (i["ImpedeixAccions?"], i["ProbabilitatImpedirAccio"])
        else:
            bloqueig = (False, 0)

        efecte = Characteristics.Effects(i["id"], i["Nom"],  i["Descripcio"], bloqueig, i["Duracio"], 
                                            i["Dany"], i["StatAfected"], i["Limit"])
        efectes.update({efecte.id: efecte})
    return efectes

def CallMovement(effects):
    movements = CallCSV("Data/Movements.csv")
    moves = {}
    for i in movements:
        Buff = {}
        if isinstance(i["Buff"], list) and len(i["Buff"]) > 1:
            for j in range(len(i["Buff"])):
                if i["Buff"][j] != "" and i["ProbEfecteBuff"][j] != "":
                    Buff[effects[i["Buff"][j]]]=int(i["ProbEfecteBuff"][j])
        elif i["Buff"] != "" and i["ProbEfecteBuff"] != "":
            Buff[effects[i["Buff"]]]=int(i["ProbEfecteBuff"])

        Debuff = {}
        if len(i["Debuff"]) > 1 and i["Debuff"] == list:
            for j in range(len(i["Debuff"])):
                if i["Debuff"][j] != "" and i["ProbEfecteDebuff"][j] != "":
                    Debuff[effects[i["Debuff"][j]]]=int(i["ProbEfecteDebuff"][j])
        elif i["Debuff"] != "" and i["ProbEfecteDebuff"] != "":
            Debuff[effects[i["Debuff"]]]=int(i["ProbEfecteDebuff"])
        move = Characteristics.Moves(i["id"], i["Nom"], i["Descripcio"], i["Potencia"], i["Precisio"],  i["Magic?"], 
                                    i["Cost"], Buff, Debuff, i["MultipleObjectiu?"], i["Cura?"], i["Protegeix?"], i["DanyperProteccio"])
        moves.update({move.id: move})
    return moves

def CallObject():
    objects = CallCSV("Data/Objects.csv")
    objectes = {
        "Combat": {},
        "Clau": {},
    }
    for i in objects:
        if i["Tipus"] == "Combat":
            obj = Objectes.ObjecteCombat(i["id"] ,i["Nom"], i["Descripcio"], i["Efectes"], i["Preu"],  i["ForadeCombat?"])
            objectes["Combat"].update({obj.id: obj})
        elif i["Tipus"] == "Clau":
            obj = Objectes.ObjecteClau(i["id"], i["Nom"], i["Descripcio"])
            objectes["Clau"].update({obj.id: obj})    
    return objectes

def CallAchievements():
    chargedlist = CallCSV("Data/Achievements.csv")

    achievements = {}
    for i in chargedlist:
        unlock = {}
        unlock.update({"Type": i["Tipus de Requisit"], "Objective": i["Requisit"], "Amount": i["Quantitat"]})

        achieve = Exits.Exits(i["id"], i["Nom"], i["Descripcio"], i["Ocult?"], i["Recompensa"], unlock)
        achievements.update({i["id"]: {"id": i["id"], "achievement": achieve}})
    return achievements

def CallZones():
    rutabase = os.path.dirname(__file__)
    ruta = os.path.join(rutabase, "Data/Zones/")

    places = {}
    for j in os.listdir(ruta):
        ruta_file = os.path.join(ruta, j)
        with open(ruta_file, "r", encoding="utf-8") as f:
            i = json.load(f)

            shop_dict = {}
            for shop in i["shops"]:
                ruta_shop = os.path.join(rutabase, "Data/Botigues",shop+".json")
                with open(ruta_shop, "r", encoding="utf-8") as shop_file:
                    shop_value = json.load(shop_file)
                
                shop_dict.update(
                    {
                        shop:
                        shop_value
                    }
                )

            place = Zones.Zona(i["id"], i["name"], i["description"], i["zone_type"], i["enemies"], 
                            i["monedes"], i["Intents"], i["objects"], shop_dict)
            
            place.AddConnections(i["connections"])
            place.AfegirCondicio(i["unlock_condition"])


            places.update({i["id"]: place})
    return places

def CallMissions(entitats):
    rutabase = os.path.dirname(__file__)
    ruta = os.path.join(rutabase, "Data/Missions/")

    missions = {}
    for j in os.listdir(ruta):
        ruta_file = os.path.join(ruta, j)
        with open(ruta_file, "r", encoding="utf-8") as f:
            i = json.load(f)

            if i["type"] == "Place":
                mision = Missions.PlaceMission(i["id"], i["name"], i["description"], i["class"], i["rewards"], 
                                              i["objective"], i["requisites"])
            elif i["type"] == "Kill":
                if i["generic"] == "True":
                    i["generic"] = True
                else:
                    i["generic"] = False
                mision = Missions.KillMission(i["id"], i["name"], i["description"], i["class"], i["rewards"], 
                                             i["objective"], i["requisites"], i["generic"], entitats)
            elif i["type"] == "Find":
                mision = Missions.FindMission(i["id"], i["name"], i["description"], i["class"], i["rewards"], 
                                              i["objective"], i["requisites"])
            elif i["type"] == "Object":
                mision = Missions.ObjectMission(i["id"], i["name"], i["description"], i["class"], i["rewards"], 
                                              i["objective"], i["requisites"])

            if i["type"] in missions.keys():
                missions[i["type"]].update({i["id"]: mision})
            else:
                missions.update({i["type"]: {i["id"]: mision}})
    return missions

def main():
    print("!! - Joc de Preguntes - !!")
    

if __name__ == "__main__":
    main()