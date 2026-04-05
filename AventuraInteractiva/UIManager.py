# Arxiu: UIManager.py
# Autor: Bernat Puig Casals
# Data: 7 de Març de 2026
# Descripcio:
# Creem el modul per a generar interficies.

from Classes import Utilitats
from Classes import Characteristics
from Classes import EntityType
from Classes import Entitat
from Classes import Events
from Classes import Objectes

import CombatManager
import AdventureManager
import TownUtilitiesManager as TUtManager

import os

Menus = {
    "Menu Poble":{
        "id": "Menu Poble",
        "opcions":
        [
            Utilitats.OpcioMenu("mapa", "Mapa", True, "Veure el Mapa i Canviar de Zona."),
            Utilitats.OpcioMenu("motxila", "Motxila", True, "Veure els objectes i utilitzar-los."),
            Utilitats.OpcioMenu("hostal", "Hostal", True, "Anar al hostal a descansar (Recuperar Salut i altres...)"),
            Utilitats.OpcioMenu("botiga", "Botiga", True, "Comprar Objectes."),
            Utilitats.OpcioMenu("estat", "Estat", True, "Veure el estat dels personatges del jugador..."),
            Utilitats.OpcioMenu("missions", "Missions", True, "Veure les missions disponibles, aceptar-les i reclamar-les..."),
            Utilitats.OpcioMenu("exits", "Éxits", True, "Veure els exits que pots i has adquirit..."),
            Utilitats.OpcioMenu("guardar", "Guardar", True, "Guardar la Partida."),
            Utilitats.OpcioMenu("sortir", "Sortir", True, "Sortir del menu.")
        ]
    },

    "Menu Wild":{
        "id": "Menu Wild",
        "opcions":
        [
            Utilitats.OpcioMenu("mapa", "Mapa", True, "Veure el Mapa i Canviar de Zona"),
            Utilitats.OpcioMenu("motxila","Motxila", True, "Veure els objectes i utilitzar-los."),
            Utilitats.OpcioMenu("explorar","Explorar", True, "Anar a explorar la zona, pots trobar or, enemics i involucrar-te en missions..."),
            Utilitats.OpcioMenu("lluitar","Lluitar", True, "Entrar forçosament en combat amb un dels enemcis de la zona..."),
            Utilitats.OpcioMenu("estat","Estat", True, "Veure el estat dels personatges del jugador..."),
            Utilitats.OpcioMenu("missions", "Missions", True, "Veure les missions disponibles, aceptar-les i reclamar-les..."),
            Utilitats.OpcioMenu("exits", "Éxits", True, "Veure els exits que pots i has adquirit..."),
            Utilitats.OpcioMenu("guardar", "Guardar", True, "Guardar la Partida."),
            Utilitats.OpcioMenu("sortir", "Sortir", True, "Sortir del menu.")

        ]
    },

    "Accions Lluita":{
        "id": "",
        "opcions":
        [
            Utilitats.OpcioMenu("atacar", "Atacar", True, "Seleccionar un atac entre els poseits per atacar l'objectiu..."),
            Utilitats.OpcioMenu("motxila", "Motxila", True, "Obre La motxila i utilitza o revisa el que hi tens..."),
            Utilitats.OpcioMenu("status", "Veure Estat", True, "veure l'estat d'un dels jugadors de l'equip.."),
            Utilitats.OpcioMenu("fugir", "Fugir", True, "Intentar fugir del enemic..."),
            Utilitats.OpcioMenu("pasar", "Pasar Torn", True, "Deixar pasar el torn sense fer res..."),
            Utilitats.OpcioMenu("sortir", "Sortir", True, "Sortir del menu.")
        ]
    },

    "Missions":{
        "id": "",
        "opcions":
        [
            Utilitats.OpcioMenu("aceptar", "Aceptar Missio", True, "Aceptar una nova missio disponible"),
            Utilitats.OpcioMenu("veure", "Veure Missio", True, "Veure les missions (disponibles, aceptades, completades)."),
            Utilitats.OpcioMenu("reclamar", "Reclamar Missio", True, "Reclamar una missio completada."),
            Utilitats.OpcioMenu("sortir", "Sortir", True, "Sortir del menu.")
        ]
    },

    "Veure Missions":{
        "id": "",
        "opcions":
        [
            Utilitats.OpcioMenu("disponibles", "Veure Missions Disponibles", True, "Veure les missions que estan per aceptar."),
            Utilitats.OpcioMenu("completades", "Veure Missions Compleatdes", True, "Veure les missions que estan completades."),
            Utilitats.OpcioMenu("acceptades", "Veure Missions Acceptades", True, "Veure les missions acceptades."),
            Utilitats.OpcioMenu("sortir", "Sortir", True, "Sortir del menu.")
        ]
    },

    "Posada":{
        "id": "",
        "opcions":        
        [
            Utilitats.OpcioMenu("si", "Descansar al hostal",  True, "Recupera als jugadors a canvi de 100 d'or."),
            Utilitats.OpcioMenu("no", "No descansar al hostal",  True, "Surt del hostal."),
        ]
    },

    "Exits":{
        "id": "",
        "opcions":
        [
            Utilitats.OpcioMenu("acquired", "Veure Exits adquirits", True, "Mostra els exits que han estat adquirits per el jugador..."),
            Utilitats.OpcioMenu("locked", "Veure Exits per adquirir",  True, "Mostra els exits que no han estat adquirits per el jugador."),
            Utilitats.OpcioMenu("sortir", "Sortir", True, "Sortir del menu.")
        ]
    },

    "Guardar":{
        "id": "",
        "opcions":
        [
            Utilitats.OpcioMenu("si", "Si", True, "Sobrescriu la ultima partida guardada, permetint accedir a la nova..."),
            Utilitats.OpcioMenu("no", "No", True, "Decideix no sobrescriure la anterior partida guardada, mantenint la ultima si n'hi ha una..."),
            Utilitats.OpcioMenu("sortir", "Sortir", True, "Sortir del menu.")
        ]
    },

    "Seleccio Partida": {
        "id": "Seleccio Partida",
        "opcions":
        [
            Utilitats.OpcioMenu("Nova", "Nova Partida", True, "Crea una nova partida, cuidado, guardar-la borra la actual..."),
            Utilitats.OpcioMenu("sortir", "Sortir", True, "Sortir del menu.")
        ],
    }
}


def ClearScreen():
    os.system("cls" if os.name == "nt" else "clear")


def MostrarMenuPrincipal(App):
    
    # Seleccionem la accio
    if App.jugador.Ubicacio.ZoneType == "Poble":
       App.CanviarMenu(Menus["Menu Poble"])
    elif App.jugador.Ubicacio.ZoneType != "Poble":
       App.CanviarMenu(Menus["Menu Wild"])

    App.MostrarMenu()

def CridarAccioMenuPrincipal(App, accio):
    # Executem acció seleccionada

    accions = {
        "mapa": lambda: AdventureManager.Mapa(App),
        "explorar": lambda: AdventureManager.Explorar(App),
        "hostal": lambda: TUtManager.Posada(App.jugador),
        "botiga": lambda: TUtManager.Botiga(App.jugador, App.Objects),
        # "estat": lambda e: VeureEstatus(App.jugador)
        # "missions": lambda e: MenuMisions(App)
        "lluitar": lambda: CombatManager.GenerarEnemic(App),
        "guardar": lambda: App.GuardarPartida(),
        # "exits": lambda e: MostrarExits(App.achievements, App.jugador)
        "motxila": lambda: App.jugador.ObjectesMochila(App.Objects, False),
        # "sortir": lambda e: (Mostra una funcio que demana si vols sortir del joc, si la resposta es si surt...)
    }

    if accio.id in accions:
        accions[accio.id]()

# def MenuMisions(jugador, missions, event, objects, exits):
#     sel = ""
#     while sel != None:
#         sel = MostrarMenus(Menus["Missions"])

#         if sel == "aceptar":
#             CrearMenuMissions(missions, "Aceptar Missions", jugador.MissionsDisponibles, None, 4)
#             try:
#                 res = MostrarMenus(Menus["Aceptar Missions"])
#                 if res != None:
#                     jugador.MisionsAcceptades.append(res)
#                     jugador.MissionsDisponibles.remove(res)
#                 else:
#                     print("Has sortit del Menu")
#                     input("Presiona per a continuar...")
#             except ValueError:
#                 print("Ha ocurregut un error...")
#         elif sel == "veure":
#             res = ""
#             while res != None:
#                 res = MostrarMenus(Menus["Veure Missions"])
#                 if res == "disponibles":
#                     CrearMenuMissions(missions, "Missions Disponibles", jugador.MissionsDisponibles, None, 6)
#                     res = MostrarMenus(Menus["Missions Disponibles"], True, False, None, "", False)
#                 elif res == "completades":
#                     CrearMenuMissions(missions, "Missions Completades", jugador.MissionsFinalitzades, None, 6)
#                     res = MostrarMenus(Menus["Missions Completades"], True, False, None, "", False)
#                 elif res == "acceptades":
#                     CrearMenuMissions(missions, "Missions Acceptades", jugador.MisionsAcceptades, None, 6)
#                     res = MostrarMenus(Menus["Missions Acceptades"], True, False, None, "", False)
        
#         elif sel == "reclamar":
#             CrearMenuMissions(missions, "Reclamar Missions", jugador.MisionsAcceptades, "Pendent Reclamar", 4)
#             dictio = {"id": None, "tipus": None}
#             while isinstance(dictio, dict) and dictio["id"] == None and dictio["tipus"] == None:
#                 dictio = MostrarMenus(Menus["Reclamar Missions"])
#                 if isinstance(dictio, dict):
#                     if dictio["id"] != None or dictio["tipus"] != None:
#                         missions[dictio["tipus"]][dictio["id"]].Reclamar(jugador, objects, event, exits)
#                         event.CridarEvent("Missio Finalitzada", dictio["id"], jugador, missions)
#                     else:
#                         sel = None
#                 else:
#                     input("Has sortit del menu missions...")

# def MostrarExits(exits, jugador):
#     sel = ""
#     while sel != None:
#         sel = MostrarMenus(Menus["Exits"])

#         if sel == "acquired":
#             CrearMenu(exits.items(), "Acquired Achievements", ("achievements", "acquirits"), jugador, None, 8)
#             MostrarMenus(Menus["Acquired Achievements"], True, False, None, None, "", False)
#         elif sel == "locked":
#             CrearMenu(exits.items(), "Unacquired Achievements", ("achievements", "locked"), jugador, None, 8)
#             MostrarMenus(Menus["Unacquired Achievements"], True, False, None, None, "", False)


def CrearMenu(llista, NomMenu, filtre, jugador = None, zones = None):
    options = []
    
    if filtre == "Zones" and zones != None and jugador != None:
        for i in llista:
            if isinstance(i, str) and i in zones.keys():
                if i in jugador.LlocsTrobats:
                    options.append(Utilitats.OpcioMenu(i, zones[i].NameZone, True, zones[i].Description))
                else:
                    options.append(Utilitats.OpcioMenu(i, zones[i].NameZone, False, zones[i].Description))
    elif filtre[0] == "Tipus Entitat":
        for i in llista:
            if isinstance(filtre, tuple) and isinstance(i[1], EntityType.EntityType):
                if filtre[1] == "Playable" and i[1].isPlayable != True:
                    continue
                options.append(Utilitats.OpcioMenu(i[1].id, i[1].EntityName, True, i[1].EntityDescription))
    elif filtre == "Entitat":
        for i in llista:
            if isinstance(i[1], Entitat.Entity):
                options.append(Utilitats.OpcioMenu(i[1].id, f"{i[1].nom}, Lv {i[1].Lv}", True, i[1].base.EntityDescription, i[1].base.ImageFrontal))
    elif filtre == "Moves":
        for i in llista:
            if isinstance(i[1], Characteristics.Moves):
                description = f"{i[1].Description}\n Characteristics: \n Potencia: {i[1].Power}, Precisio: {i[1].Precision}, Mana Cost: {i[1].Cost}"

                options.append(Utilitats.OpcioMenu(i[1].id, i[1].Name, True, description))
    elif filtre == "Objectes":
        for i in llista:
            espaiat = 30 - len(i[1]["objecte"].ObjectName)
            mostrar = f"{i[1]["objecte"].ObjectName}" + " "*espaiat + f"{i[1]["amount"]}"
            if isinstance(i[1]["objecte"], Objectes.ObjecteCombat):
                tipus = "Combat"
            else:
                tipus = "Clau"
            options.append(Utilitats.OpcioMenu({"id": i[1]["objecte"].id, "type": tipus}, mostrar, (100, 100), True, i[1]["objecte"].ObjectDescription))
    elif filtre == "Botigues":
        for id, val in llista:
            options.append(Utilitats.OpcioMenu(id, val["name"],(100, 100), True, val["description"]))

    elif isinstance(filtre, tuple):
        if filtre[0] == "achievements":
            if filtre[1] == "acquirits":
                for id, value in llista:
                    if value["achievement"].Obtained == True:
                        options.append(Utilitats.OpcioMenu(value["achievement"].id,value["achievement"].Name, (100, 100), True, value["achievement"].Description))
            if filtre[1] == "locked":
                for id, value in llista:
                    if value["achievement"].Obtained == False:
                        options.append(Utilitats.OpcioMenu(value["achievement"].id, value["achievement"].Name,(100, 100), True, value["achievement"].Description))

        
    Menus.update({NomMenu: {
                "id": NomMenu,
                "opcions": options
            }
        }
    )

def CrearMenuProductes(botiga, NomMenu, opcionsvisibles = 5):
    opcions = []

    for id, value in botiga:
        espaiats = 80 - len(value["name"])
        textProd = f"{value["name"]}" + " "*espaiats + f"Preu: {value["price"]}"

        opcions.append(Utilitats.OpcioMenu(value["id"], 
                                           textProd, True, value["description"]))

    Menus.update({NomMenu: {
                "id": NomMenu,
                "opcions": opcions
            }
        }
    )
def CrearMenuMissions(llistamissions, NomMenu, filtre, estat = None, opcionsvisibles = 6):
    opcions = []
    for i in llistamissions.items():
        for j in i[1].items():
            if j[0] in filtre:
                if estat == None or j[1].Status == estat:
                    if estat == "Pendent Reclamar":
                        opcions.append(Utilitats.OpcioMenu({"id": j[0], "tipus": i[0]}, j[1].Name, True, j[1].Description))
                    else:
                        opcions.append(Utilitats.OpcioMenu(j[0], j[1].Name, True, j[1].Description))
                
    Menus.update({NomMenu: {
                "id": NomMenu,
                "opcions": opcions
            }
        }
    )


def BattleScreenShow(teamlis):

    for id, ent in teamlis.items():
        if ent.StatsCombat["CurHP"] > 0:
            llarg = len(f"{ent.nom}, LV: {ent.Lv}")
            espaiat = ""
            for j in range(30 - llarg):
                espaiat += " "
            print(f"{ent.nom}, LV: {ent.Lv}", end=espaiat)
    
    print()
    for id, ent in teamlis.items():
        if ent.StatsCombat["CurHP"] > 0:
            llarg = len(f"HP: {round(ent.StatsCombat["CurHP"], 2)} / {round(ent.StatsCombat["MaxHP"], 2)}")
            espaiat = ""
            for j in range(30 - llarg):
                espaiat += " "
            print(f"HP: {round(ent.StatsCombat["CurHP"], 2)} / {round(ent.StatsCombat["MaxHP"], 2)}", end=espaiat)
    
    saltdeLinia = False
    for id, ent in teamlis.items():
        if ent.StatsCombat["CurHP"] > 0:
            if ent.isPlayer == True:
                if saltdeLinia == False:
                    print()
                llarg = len(f"Mana: {round(ent.StatsCombat["Mana"], 2)} / {round(ent.StatsCombat["MaxMana"], 2)}")
                espaiat = ""
                for j in range(30 - llarg):
                    espaiat += " "
                print(f"Mana: {round(ent.StatsCombat["Mana"], 2)} / {round(ent.StatsCombat["MaxMana"], 2)}", end=espaiat)
                saltdeLinia = True

    saltdeLinia = False
    for id, ent in teamlis.items():
        if ent.StatsCombat["CurHP"] > 0:
            if len(ent.afected) > 0:
                if saltdeLinia == False:
                    print()
                llarg = 0
                effect = ""
                for e in ent.afected:
                    llarg += len(e.Name)
                    effect += e.Name + ", "
                espaiat = ""
                for j in range(30 - llarg):
                    espaiat += " "
                print(f"{effect}", end=espaiat)
                saltdeLinia = True
            else:
                afectats = False
                for k in teamlis.values():
                    if k != ent  and len(k.afected) > 0:
                        afectats = True
                if afectats == True:
                    espaiat = ""
                    for j in range(30):
                        espaiat += " "
                    print(espaiat, end="")
    
    print()
    for id, ent in teamlis.items():
        if ent.StatsCombat["CurHP"] > 0:
            llarg = len(f"Prioritat: {round(ent.Priority, 1)}")
            espaiat = ""
            for j in range(30 - llarg):
                espaiat += " "
            print(f"Prioritat: {round(ent.Priority, 1)}", end=espaiat)
            saltdeLinia = True
    print("\n")

# def VeureEstatus(jugador, combat = False):
#     ClearScreen()
#     CrearMenu(jugador.Team.items(), "Seleccio Equip", "Entitat")

#     seleccio = MostrarMenus(Menus["Seleccio Equip"])

#     if seleccio != None:
#         if combat == False:
#             jugador.Team[seleccio].ShowStatus(jugador)
#         else:
#             jugador.Team[seleccio].ShowStatus(jugador, True)
#     else:
#         input("Has sortit del menu d'estatus...")