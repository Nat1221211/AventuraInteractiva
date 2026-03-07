# Arxiu: PrepararCridar.py
# Autor: Bernat Puig Casals
# Data: 7 de Març de 2026
# Descripcio:
# Creem el modul per a guardar i carregar la partida.

from Classes import Utilitats
from Classes import Characteristics
from Classes import EntityType
from Classes import Events

import os

Menus = {
    "Menu Poble": Utilitats.Menu(
        "Menu Principal",
        [
            Utilitats.OpcioMenu("mapa", "Mapa", True, "Veure el Mapa i Canviar de Zona."),
            Utilitats.OpcioMenu("motxila", "Motxila", True, "Veure els objectes i utilitzar-los."),
            Utilitats.OpcioMenu("hostal", "Hostal", True, "Anar al hostal a descansar (Recuperar Salut i altres...)"),
            Utilitats.OpcioMenu("botiga", "Botiga", True, "Comprar Objectes."),
            Utilitats.OpcioMenu("estat", "Estat", True, "Veure el estat dels personatges del jugador..."),
            Utilitats.OpcioMenu("missions", "Missions", True, "Veure les missions disponibles, aceptar-les i reclamar-les..."),
            Utilitats.OpcioMenu("exits", "Éxits", True, "Veure els exits que pots i has adquirit..."),
            Utilitats.OpcioMenu("gremi","Gremi", True, "Anar al gremi a contractar companys..."),
            Utilitats.OpcioMenu("guardar", "Guardar", True, "Guardar la Partida.")
        ],
        9
    ),

    "Menu Wild": Utilitats.Menu(
        "Menu Principal",
        [
            Utilitats.OpcioMenu("mapa", "Mapa", True, "Veure el Mapa i Canviar de Zona"),
            Utilitats.OpcioMenu("motxila","Motxila", True, "Veure els objectes i utilitzar-los."),
            Utilitats.OpcioMenu("explorar","Explorar", True, "Anar a explorar la zona, pots trobar or, enemics i involucrar-te en missions..."),
            Utilitats.OpcioMenu("lluitar","Lluitar", True, "Entrar forçosament en combat amb un dels enemcis de la zona..."),
            Utilitats.OpcioMenu("estat","Estat", True, "Veure el estat dels personatges del jugador..."),
            Utilitats.OpcioMenu("missions", "Missions", True, "Veure les missions disponibles, aceptar-les i reclamar-les..."),
            Utilitats.OpcioMenu("exits", "Éxits", True, "Veure els exits que pots i has adquirit..."),
            Utilitats.OpcioMenu("guardar", "Guardar", True, "Guardar la Partida.")
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
    ),

    "Pantalla de Titol": Utilitats.Menu(
        "Pantalla de Titol",
        [
            Utilitats.OpcioMenu("carregar", "Carregar Partida", True, "Carregar una partida guardada."),
            Utilitats.OpcioMenu("nova", "Començar Nova Partida", True, "Començar una nova partida."),
        ],
        2
    )
}


def ClearScreen():
    os.system("cls" if os.name == "nt" else "clear")

def MostrarMenus(Menu, sortir = True, combat = False, jugador = None, enemy = None, TextExtra = "", seleccionar = True):
    if len(Menu.Opcions) >= 1:
        while True:
            ClearScreen()
            if combat == True:
                BattleScreenShow(jugador.Team)
                BattleScreenShow(enemy)
            
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

def MenuMisions(jugador, missions):
    sel = MostrarMenus(Menus["Missions"])

    if sel == "aceptar":
        CrearMenuMissions(missions, "Aceptar Missions", jugador.MissionsDisponibles, "Disponible", 4)
        res = MostrarMenus(Menus["Aceptar Missions"])
        if res != None:
            jugador.MisionsAcceptades.append(res)
            jugador.MissionsDisponibles.remove(res)
        else:
            print("Has sortit del Menu")
            input("Presiona per a continuar...")
    elif sel == "veure":
        res = MostrarMenus(Menus["Veure Missions"])
        if res == "disponibles":
            CrearMenuMissions(missions, "Missions Disponibles", jugador.MissionsDisponibles, "Disponible", 6)
            res = MostrarMenus(Menus["Missions Disponibles"], True, False, None, "", False)
        elif res == "completades":
            CrearMenuMissions(missions, "Missions Completades", jugador.MissionsFinalitzades, "Completada", 6)
            res = MostrarMenus(Menus["Missions Completades"], True, False, None, "", False)
        elif res == "acceptades":
            CrearMenuMissions(missions, "Missions Acceptades", jugador.MisionsAcceptades, "Acceptada", 6)
            res = MostrarMenus(Menus["Missions Acceptades"], True, False, None, "", False)
    
    elif sel == "reclamar":
        CrearMenuMissions(missions, "Reclamar Missions", jugador.MisionsAcceptades, "Pendent Reclamar", 4)
        id, tipus = MostrarMenus(Menus["Reclamar Missions"])
        if id != None and tipus != None:
            missions[tipus][id].Reclamar(jugador)
            event.CridarEvent("Missio Finalitzada", id, jugador, missions)
        else:
            input("Has sortit del menu missions...")


def CrearMenu(llista, NomMenu, jugador, zones, filtre = "Playables", opcionsvisibles = 3):
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
                    if estat == "Pendent Reclamar":
                        opcions.append(Utilitats.OpcioMenu(j[0], j[1].Name, True, j[1].Description, i[0]))
                    else:
                        opcions.append(Utilitats.OpcioMenu(j[0], j[1].Name, True, j[1].Description))
                
    Menus.update({NomMenu: Utilitats.Menu(
                NomMenu,
                opcions,
                opcionsvisibles
            )
        }
    )
