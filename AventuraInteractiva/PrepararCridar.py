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


Menus = {
    "Menu Poble": Utilitats.Menu(
        "Menu Principal",
        [
            Utilitats.OpcioMenu("mapa", "Mapa", True, "Veure el Mapa i Canviar de Zona"),
            Utilitats.OpcioMenu("motxila", "Motxila", True, "Veure el Mapa i Canviar de Zona"),
            Utilitats.OpcioMenu("hostal", "Hostal", True, "Veure el Mapa i Canviar de Zona"),
            Utilitats.OpcioMenu("botiga", "Botiga", True, "Veure el Mapa i Canviar de Zona"),
            Utilitats.OpcioMenu("estat", "Estat", True, "Veure el Mapa i Canviar de Zona"),
            Utilitats.OpcioMenu("missions", "Missions", True, "Veure el Mapa i Canviar de Zona"),
            Utilitats.OpcioMenu("exits", "Éxits", True, "Veure el Mapa i Canviar de Zona"),
            Utilitats.OpcioMenu("gremi","Gremi", True, "Veure el Mapa i Canviar de Zona"),
            Utilitats.OpcioMenu("guardar", "Guardar", True, "Veure el Mapa i Canviar de Zona")
        ],
        9
    ),

    "Menu Wild": Utilitats.Menu(
        "Menu Principal",
        [
            Utilitats.OpcioMenu("mapa", "Mapa", True, "Veure el Mapa i Canviar de Zona"),
            Utilitats.OpcioMenu("motxila","Motxila", True, "Veure el Mapa i Canviar de Zona"),
            Utilitats.OpcioMenu("explorar","Explorar", True, "Veure el Mapa i Canviar de Zona"),
            Utilitats.OpcioMenu("lluitar","Lluitar", True, "Veure el Mapa i Canviar de Zona"),
            Utilitats.OpcioMenu("estat","Estat", True, "Veure el Mapa i Canviar de Zona"),
            Utilitats.OpcioMenu("missions","Missions", True, "Veure el Mapa i Canviar de Zona"),
            Utilitats.OpcioMenu("exits","Éxits", True, "Veure el Mapa i Canviar de Zona"),
            Utilitats.OpcioMenu("guardar","Guardar", True, "Veure el Mapa i Canviar de Zona")
        ],
        8
    ),

    "Accions Lluita": Utilitats.Menu(
        "Seleccio d'Accions",
        [
            Utilitats.OpcioMenu("atacar", "Atacar", True, "Seleccionar un atac entre els poseits per atacar l'objectiu..."),
            Utilitats.OpcioMenu("motxila", "Motxila", True, "Obre La motxila i utilitza o revisa el que hi tens..."),
            Utilitats.OpcioMenu("status", "Veure Estat", True, "veure l'estat d'un dels jugadors de l'equip.."),
            Utilitats.OpcioMenu("fugir", "Fugir", True, "Intentar fugir del enemic..."),
            Utilitats.OpcioMenu("pasar", "Pasar Torn", True, "Deixar pasar el torn sense fer res...")
        ],
        5
    ),

    "Missions": Utilitats.Menu(
        "Menu Missions",
        [
            Utilitats.OpcioMenu("aceptar", "Aceptar Missio", True, "Aceptar una nova missio disponible"),
            Utilitats.OpcioMenu("veure", "Veure Missio", True, "Veure les missions (disponibles, aceptades, completades)."),
            Utilitats.OpcioMenu("reclamar", "Reclamar Missio", True, "Reclamar una missio completada."),
        ],
        3
    ),

    "Veure Missions": Utilitats.Menu(
        "Veure Missions",
        [
            Utilitats.OpcioMenu("disponibles", "Veure Missions Disponibles", True, "Veure les missions que estan per aceptar."),
            Utilitats.OpcioMenu("completades", "Veure Missions Compleatdes", True, "Veure les missions que estan completades."),
            Utilitats.OpcioMenu("acceptades", "Veure Missions Acceptades", True, "Veure les missions acceptades."),
        ],
        3
    )
}


def MostrarMenus(Menu, sortir = True, combat = False, enemy = None, TextExtra = "", seleccionar = True):
    if len(Menu.Opcions) >= 1:
        while True:
            Call.ClearScreen()
            if combat == True:
                BattleScreenShow(jugador.Team.values())
                BattleScreenShow(enemy.values())
            
            Utilitats.MostrarMenu.Mostrar(Menu, TextExtra)

            print("\n W/S moures", end="")
            print(", Enter seleccionar" if seleccionar == True else "", end="")
            print(", Q sortir" if sortir == True else "")
            try:
                entrada = input("-> ").lower()

                if entrada == "w":
                    Menu.MoureCursor(-1)
                elif entrada == "s":
                    Menu.MoureCursor(1)
                elif entrada == "" and seleccionar == True:
                    accio = Menu.SeleccionarOpcio()
                    if accio == None:
                        return "bloquejat"
                    return accio
                elif entrada == "q":
                    return None
            
            except ValueError:
                print("Ha ocurregut un error...")
    else:
        print("No hi ha opcions...")
        input("Presiona per a continuar...")

def CrearMenu(llista, NomMenu, filtre = "Playables", opcionsvisibles = 3):
    options = []
    for i in llista:
        if isinstance(i, str) and i in zones.keys():
            if i in jugador.LlocsTrobats:
                options.append(Utilitats.OpcioMenu(i, zones[i].NameZone, True, zones[i].Description))
            else:
                options.append(Utilitats.OpcioMenu(i, zones[i].NameZone, False, zones[i].Description))
        elif isinstance(i[1], EntityType.EntityType):
            if filtre == "Playables" and i[1].isPlayable != True:
                continue
            options.append(Utilitats.OpcioMenu(i[1].id, i[1].EntityName, True, i[1].EntityDescription))
        elif isinstance(i[1], Entitat.Entity):
            options.append(Utilitats.OpcioMenu(i[1].id, i[1].nom, True, i[1].base.EntityDescription))
        elif isinstance(i[1], Characteristics.Moves):
            options.append(Utilitats.OpcioMenu(i[1].id, i[1].Name, True, i[1].Description))
        
    Menus.update({NomMenu: Utilitats.Menu(
                NomMenu,
                options,
                opcionsvisibles
            )
        }
    )

def CrearMenuMissions(llistamissions, NomMenu, filtre, estat = None, opcionsvisibles = 6):
    opcions = []
    for i in llistamissions.items():
        for j in i[1].items():
            if j[0] in filtre:
                if estat != None and j[1].Status == estat:
                    opcions.append(Utilitats.OpcioMenu(j[0], j[1].Name, True, j[1].Description))
                else:
                    opcions.append(Utilitats.OpcioMenu(j[0], j[1].Name, True, j[1].Description))

    Menus.update({NomMenu: Utilitats.Menu(
                NomMenu,
                opcions,
                opcionsvisibles
            )
        }
    )


def ClearScreen():
    os.system("cls" if os.name == "nt" else "clear")

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
                            kv = v.split(": ")
                            linia[j][kv[0]] = float(kv[1]) if not kv[1].endswith("%") else kv[1]
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

        entitat = EntityType.EntityType(i["id"], i["Nom"],  i["Playable?"], i["Vida"], i["Mana"], i["ATK"], i["INT"], 
                                        i["DEF"], i["SPD"], i["XP"], i["Groups"],  i["Descripcio"], moves)
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
        efecte = Characteristics.Effects(i["Nom"],  i["Descripcio"], bloqueig, i["Duracio"], 
                                            i["Dany"], i["StatAfected"], i["Limit"])
        efectes.update({efecte.Name: efecte})
    return efectes

def CallMovement(effects):
    movements = CallCSV("Data/Movements.csv")
    moves = {}
    for i in movements:
        Buff = {}
        if len(i["Buff"]) > 1 and i["Buff"] == list:
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
            obj = Objectes.ObjecteCombat(i["Nom"], i["Descripcio"], i["Efectes"], i["Preu"],  i["ForadeCombat?"])
            objectes["Combat"].update({obj.ObjectName: obj})
        elif i["Tipus"] == "Clau":
            obj = Objectes.ObjecteClau(i["Nom"], i["Descripcio"])
            objectes["Clau"].update({obj.ObjectName: obj})    
    return objectes

def CallAchievements(Individual = True):
    objects = CallCSV("Data/Achievements.csv")
    for i in objects:
        requisits = {}
        if Individual == True:
            if i["Tipus de Requisit"] == "Kill":
                Exits.KillExit(i["Nom"], i["Descripcio"], i["Requisit"], i["Quantitat"], i["Recompensa"])
        else:
            if i["Tipus de Requisit"] != "Kill":
                requisits[i["Nom"]]={"Type&Amt": (i["Requisit"], i["Quantitat"]), "Qty": 0}
    return requisits

def CallZones():
    rutabase = os.path.dirname(__file__)
    ruta = os.path.join(rutabase, "Data/Zones/")

    places = {}
    for j in os.listdir(ruta):
        ruta_file = os.path.join(ruta, j)
        with open(ruta_file, "r", encoding="utf-8") as f:
            i = json.load(f)

            place = Zones.Zona(i["id"], i["name"], i["description"], i["zone_type"], i["enemies"], 
                            i["monedes"])
            
            place.AddConnections(i["connections"])
            place.AfegirCondicio(i["unlock_condition"])


            places.update({i["id"]: place})
    return places

def CallMissions():
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
                mision = Missions.KillMission(i["id"], i["name"], i["description"], i["class"], i["rewards"], 
                                             i["objective"], i["requisites"])
            elif i["type"] == "Find":
                mision = Missions.FindMission(i["id"], i["name"], i["description"], i["class"], i["rewards"], 
                                              i["objective"], i["requisites"])
            elif i["type"] == "Object":
                mision = Missions.ObjectMission(i["id"], i["name"], i["description"], i["class"], i["rewards"], 
                                              i["objective"], i["requisites"])

            missions.update({i["type"]: {i["id"]: mision}})
    return missions

def main():
    print("!! - Joc de Preguntes - !!")
    

if __name__ == "__main__":
    main()