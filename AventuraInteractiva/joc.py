# Arxiu: joc.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem el programa principal del joc d'aventures per terminal.

# Llibreries
import os
import random
import tkinter

from Classes import Objectes
from Classes import Exits
from Classes import Entitat
from Classes import EntityType
from Classes import Missions
from Classes import Titles
from Classes import Zones
from Classes import Player
from Classes import Utilitats
import PrepararCridar as Call

Objects = Call.CallObject()
Effects = Call.CallEfect()
Movements = Call.CallMovement(Effects)
Entities = Call.CallEntity(Movements)


# Creem la funcio per a generar els grups d'entitats algo aixi com els tipus.
entityGroups = {""}

        # Zones
zones = Call.CallZones()

# # Botiga
botiga = [Objects["Combat"]["Pocio Inferior"],
          Objects["Combat"]["Pocio"],
          Objects["Combat"]["Pocio Intermitja"]
          ]

achievements = []

missions = Call.CallMissions()


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
    )
}

def MostrarMenus(Menu):
    while True:
        Call.Call.ClearScreen()
        Utilitats.MostrarMenu.Mostrar(Menu)

        print("\n W/S moures, ENTER seleccionar, Q sortir")
        try:
            entrada = input("-> ").lower()

            if entrada == "w":
                Menu.MoureCursor(-1)
            elif entrada == "s":
                Menu.MoureCursor(1)
            elif entrada == "":
                return Menu.SeleccionarOpcio()
            elif entrada == "q":
                return None
            
        except ValueError:
            print("Ha ocurregut un error...")

def CrearMenu(llista, NomMenu, filtre = "Playables"):
    options = []
    for i in llista:
        if isinstance(i[1], EntityType.EntityType):
            if filtre == "Playables" and i[1].isPlayable != True:
                continue
            options.append(Utilitats.OpcioMenu(i[1].id, i[1].EntityName, True, i[1].EntityDescription))
        elif isinstance(i[1], Entitat.Entity):
            options.append(Utilitats.OpcioMenu(i[1].nom, i[1].nom, True, i[1].base.EntityDescription))
    
    
    
    Menus.update({NomMenu: Utilitats.Menu(
                NomMenu,
                options,
                3
            )
        }
    )

def CrearJugador():
    nom = ""
    while nom == "":
        try:
            nom = input("Digues el nom del personatge: ")
        except ValueError:
            print("Ha ocurregut un error...")
    
    CrearMenu(Entities.items(), "Menu Seleccio Inicial")
    
    identifier = MostrarMenus(Menus["Menu Seleccio Inicial"])

    playableentity = Entitat.Entity(nom, 5, True, Entities[identifier])

    return playableentity

# Cridem la funcio per crear el jugador, la variable ubicacio, i la variable de diccionari amb els grups i les seves entitats
personatge = CrearJugador()
ubicacio = zones["dawn_village"]
team = {}
team.update({personatge.nom: personatge})

jugador = Player.Player(personatge.nom, team, ubicacio)


# # Afegim algun objecte al jugador de base
jugador.AfegirObjecte(Objects["Combat"]["Pocio Inferior"], 2)


def AccioMenuPrincipal():
    global jugador
    
    pos = 0

    print(f"Vostè es troba a {jugador.Ubicacio.NameZone}")

    # Seleccionem la accio
    if jugador.Ubicacio.ZoneType == "Poble":
        accio = MostrarMenus(Menus["Menu Poble"])
    elif jugador.Ubicacio.ZoneType != "Poble":
        accio = MostrarMenus(Menus["Menu Wild"])

    Call.Call.ClearScreen()
    # Executem acció seleccionada
    if accio == "mapa":
        Mapa()
    elif accio == "explorar":
        Explorar()
    elif accio == "hostal":
        Posada()
    elif accio == "botiga":
        Botiga()
    elif accio == "estat":
        VeureEstatus()
    elif accio == "missions":
        MenuMisions()
    elif accio == "lluitar":
        GenerarEnemic()
    elif accio == "guardar":
        print("")
    elif accio == "exits":
        #MostrarExits()
        print("No actualitxat")
    elif accio == "motxila":
        jugador.ObjectesMochila(jugador.Team)
    elif accio == "gremi":
        # Gremi()
        print("Desactivat")



contractatsAnteriorment = []
# def Gremi():
#     res = 0
#     while res not in [1, 2, 3]:
#         ClearScreen()
#         print("- Gremi d'Aventurers -")
#         print("1 -> Descontractar Aventurer")
#         print("2 -> Contractar Aventurer")
#         print(f"3 -> Sortir")
#         res = int(input("Digues una de les opcions: "))
#         if res not in [1, 2, 3]:
#             print("Has de dir un dels numeros corresponents...")
#     if res in [1, 2, 3]:
#         ClearScreen()
#         if res == 3:
#             print("Has sortit del gremi d'aventurers")
#         elif res == 1:
#             if len(jugador.Team) > 1:
#                 print(" - Separem els nostres camins - ")
#                 count = 1
#                 for i in range(len(jugador.Team)):
#                     if jugador.Team[i] != jugador:
#                         print(f"{count} -> {jugador.Team[i].nom}, Lv: {jugador.Team[i].Lv}")
#                         count += 1
#                 print(f"{count} -> Sortir")
#                 try:
#                     sel = int(input("Digues amb qui vols separar camins: "))
#                     if sel not in range(len(jugador.Team)):
#                         print("Has de dir un dels personatges seleccionables...")
#                     contractatsAnteriorment.append(jugador.Team[sel])
#                     print(f"Has decidit separar camins amb {jugador.Team[sel].nom}...")
#                     jugador.Team.pop(jugador.Team[sel])
#                 except ValueError:
#                     print("Ha ocurrgut un error...")
#             else:
#                 print("No tens cap company del que separarte...")
#         elif res == 2:
#             res2 = 0
#             while res2 not in [1, 2, 3]:
#                 ClearScreen()
#                 print("- Contractació - Gremi d'Aventurers -")
#                 print("1 -> Nou Aventurer")
#                 print("2 -> Antic Company")
#                 print(f"3 -> Sortir")
#                 res2 = int(input("Digues una de les opcions: "))
#                 if res2 not in [1, 2, 3]:
#                     print("Has de dir un dels numeros corresponents...")
#             if res2 in [1, 2, 3]:
#                 ClearScreen()
#                 if res2 == 3:
#                     print("Has sortit del menu de contractació...")
#                 elif res2 == 1:
#                     if len(jugador.Team) < 3:
#                         cost = ((len(contractatsAnteriorment)) + (len(jugador.Team))) * 5000
#                         if jugador.Gold >= cost:
#                             crear = ""
#                             while crear not in ["s", "n"]:
#                                 ClearScreen()
#                                 print(f"Contractar un aventurer costara {cost} gold...")
#                                 crear = input(f"Contractaras a un nou aventurer tot i això: S / N\n").lower()
#                                 if crear not in ["s", "n"]:
#                                     print("Has de dir una de les opcions...")
#                             if crear == "s":
#                                 aventurer = CrearJugador()
#                                 jugador.Team.append(aventurer)
#                                 jugador.Team[0].Gold -= cost
#                             else:
#                                 print("Has sortit del menu de contractació...")
#                         else:
#                             print(f"No tens suficient gold per a contractar a un aventurer...")
#                             print(f"Costa {cost} gold...")
#                     else:
#                         print("Tens massa persones al equip...")
#                     res = 0
#                 elif res2 == 2:
#                     if len(contractatsAnteriorment) > 0:
#                         if len(jugador.Team) < 3: 
#                             sel = -1
#                             while sel not in range(len(contractatsAnteriorment) + 1):
#                                 ClearScreen()
#                                 count = 1
#                                 for i in range(len(contractatsAnteriorment)):
#                                     print(f"{count} -> {contractatsAnteriorment[i].nom}, Lv: {contractatsAnteriorment[i].Lv}")
#                                     print(f"Classe: {contractatsAnteriorment[i].base.EntityName}")
#                                     if contractatsAnteriorment[i].subclass != None:
#                                         print(f"Segona Classe: {contractatsAnteriorment[i].subclass}")
#                                     print()
#                                     count += 1
#                                 print(f"{count} -> Sortir")
#                                 try:
#                                     sel = int(input("Digues a qui vols reclutar de nou: "))
#                                 except ValueError:
#                                     print("Ha ocurregut un error...")
#                             if sel not in range(len(contractatsAnteriorment) + 1):
#                                 print("Has de dir un dels numeros...")
#                             else:
#                                 if sel == count:
#                                     print("Has sortit del menu de contractació...")
#                                 else:
#                                     aventurer = contractatsAnteriorment[sel - 1]
#                                     jugador.Team.append(aventurer)
#                                     contractatsAnteriorment.remove(aventurer)
#                                     sel = 1
#                                     print(f"Has començat de nou un viatge amb {aventurer.nom}...")
#                         else:
#                             print("Tens massa persones al equip...")
#                     else:
#                         print("No has separat camins amb ningu...")
#                     res = 0
#     input("\nPresiona per a continuar...")


def VeureEstatus(combat = False):
    res = 0
    while res not in range(1, len(jugador.Team) + 2):
        Call.ClearScreen()
        CrearMenu(jugador.Team.items(), "Seleccio Equip", "")

        seleccio = MostrarMenus(Menus["Seleccio Equip"])

        if combat == False:
            jugador.Team[seleccio].ShowStatus(jugador)
        else:
            jugador.Team[seleccio].ShowStatus(jugador, True)
    else:
        input("Has sortit del menu d'estatus...")



def MenuMisions():
    res = 0
    while res not in [1, 2, 3, 4]:
        res = 0
        Call.ClearScreen()
        print("1 -> Veure Misions")
        print("2 -> Acceptar Misions")
        print("3 -> Reclamar Misions")
        print("4 -> Sortir")
        try:
            res = int(input("Digues el numero segons el que vols fer: "))
            if res not in [1, 2, 3, 4]:
                print("Has de dir un dels numeros segons el que vols fer...")
            if res in [2, 3] and jugador.Ubicacio.ZoneType != "Poble":
                print(f"Per acceptar o reclamar missions has d'estar en un Poblat.")
            else:
                if res == 1:
                    filtrar = 0
                    while filtrar not in [1, 2, 3, 4, 5]:
                        Call.ClearScreen()
                        print("1 -> Aceptades")
                        print("2 -> Per aceptar")
                        print("3 -> Completades")
                        print("4 -> Sortir")
                        try:
                            filtrar = int(input("Digues que vols fer: "))
                            if filtrar not in [1, 2, 3, 4]:
                                print("Has de dir un dels numeros segons el que vols fer...")
                        except ValueError:
                            print("Ha ocurregut un error...")
                    if filtrar in [2] and jugador.Ubicacio.ZoneType != "Poble":
                        print(f"Per revisar aquestes missions hauries d'estar en una zona segura (Poble).")
                    else:
                        if filtrar == 1:
                            count, reclamar = ShowMisions("Accepted", "Res", jugador.MisionsAcceptades)
                        elif filtrar == 3:
                            count, reclamar = ShowMisions("Completed", "Res", jugador.MissionsFinalitzades)
                        elif filtrar == 2:
                            count, reclamar  = ShowMisions("Requisites", "Res", missions)
                        if len(reclamar) == 0:
                            print("No hi ha cap missio en aquest apartat...")
                elif res == 2:
                    count, reclamar  = ShowMisions("Requisites", "Aceptar", missions)
                    aceptar = 0
                    while aceptar not in range(1, count + 1):
                        Call.ClearScreen()
                        count, reclamar = ShowMisions("Requisites", "Aceptar", missions)
                        try:
                            aceptar = int(input("Digues quina misio vols aceptar: "))
                            if aceptar < count + 1 and aceptar > 0:
                                if aceptar == count:
                                    print("Has sortit")
                                else:
                                    jugador.MisionsAcceptades.append(reclamar[aceptar - 1])
                        except ValueError:
                            print("Ha ocurregut un error...")
                elif res == 3:
                    count, reclamar  = ShowMisions("Rewards Unclaimed", "Aceptar", jugador.MisionsAcceptades)
                    aceptar = 0
                    while aceptar not in range(1, count + 1):
                        Call.ClearScreen()
                        count, reclamar  = ShowMisions("Rewards Unclaimed", "Aceptar", jugador.MisionsAcceptades)
                        try:
                            aceptar = int(input("Digues quina misio vols reclamar: "))
                            if aceptar < count + 1 and aceptar > 0:
                                if aceptar == count:
                                    print("Has sortit")
                                else:
                                    reclamar[aceptar - 1].ClaimedRewards(jugador)
                        except ValueError:
                            print("Ha ocurregut un error...")
                if res != 4:
                    res = 0
                else:
                    print("Has sortit del menu de misions...")
            
        except ValueError:
            print("Ha ocurregut un error...")
        
        input("Presiona per a continuar...")
    
def ShowMisions(filter, accio, mision):
    count = 1
    if mision.keys():
        mision = [i for i in mision.keys()]
    llista = []
    for i in mision:
        if accio != "res":
            print(f"{count} ->", end=" ")
        print(f"{missions[i].Name}")
        print(f"{missions[i].Description}\n")
        llista.append(missions[i])
        count += 1
    if accio != "Res":
        print(f"{count} -> Sortir")
    return count, llista


# def MostrarExits():
#     print("Exits")
#     for i in achievements:
#         if i.Obtained == True:
#             obtingut = "Obtingut"
#         else:
#             obtingut = "No Obtingut"
#         print(f"{i.Name}, {obtingut}")
#         if type(i) != Exits.KillExit:
#             print(f"{i.Description} \n")
#         else:
#             print(f"{i.Description}, \n{i.Count} / {i.Quantity}\n")
#     input("Presiona per a continuar...")

# def ComprovarExits(enemy):
#     for i in achievements:
#         if i.Obtained == False:
#             if type(i) == Exits.KillExit:
#                 i.IncrementCount(enemy)
#             i.Completed(team[0])
#             team[0].AcquiredAchievements.append(i)


def PrepararBotiga(): # Afegir objectes segons nivell
    global jugador
    if jugador.Team[0].Lv > 35:
        print()
    elif jugador.Team[0].Lv > 20:
        print()
    elif jugador.Team[0].Lv > 10:
        print()

def Botiga():
    res = -1
    while res not in (range(0, len(botiga) + 2)):
        temp = 0
        for i in botiga:
            print(f"{temp + 1} -> {i.ObjectName}")
            print(f"Preu: {i.Preu} gold\n")
            temp += 1
            if temp == len(botiga):
                print(f"{temp + 1} -> Sortir")
        res = int(input("Que vols comprar: "))
        if res not in (range(0, len(botiga) + 2)):
            print("Has de dir un dels objectes o el numero equivalent a sortir.")
    if res == len(botiga) + 1:
        print("Has sortit de la botiga...")
    else:
        qty = 0
        res = res -1
        while qty < 1:
            qty = int(input(f"\nQuants/es {botiga[res].ObjectName} vols comprar: "))
        jugador.AfegirObjecte(botiga[res], qty)
        jugador.Gold -= botiga[res].Preu * qty
        print(f"Has comprat {qty} {botiga[res].ObjectName} per {botiga[res].Preu * qty} gold !")

def Posada(free = False):
    global jugador
    res = ""
    if free == False:
        while res not in ["S", "N"]:
            Call.ClearScreen()
            try:
                res = input("\nVols descansar? Costa 100 gold (S / N): ").capitalize()
            except ValueError:
                print("Ha ocurregut un error...")
    if res == "S" or free == True:
        if jugador.Gold >= 100 or free == True:
            print("Has descansat comodament, t'has recuperat completament...")
            if free == False:
                jugador.Gold -= 100
            for i in jugador.Team:
                i.StatsCombat["CurHP"] = i.StatsCombat["MaxHP"]
                i.StatsCombat["Mana"] = i.StatsCombat["MaxMana"]
                i.afected = []
        else:
            print("No tens suficient gold per pagar la posada, has marxat sense poder descansar...")
    else:
        print("Has marxat...")

def Mapa():
    global jugador
    count = 1
    disponibles = []
    print(f"Vosté és a {jugador.Ubicacio.NameZone}.\n")
    for i in jugador.Ubicacio.Connections:  # Mostrem ubicacions disponibles
        if i in jugador.LlocsTrobats:
            print(f"{count} -> {zones[i].NameZone}")
            count += 1
            disponibles.append(i)
    if count > len(disponibles):
        print(f"{count} -> Sortir")
    pos = 0
    while pos not in range(1, count + 2): # Demanem a on anar.
        try:
            pos = int(input("Digues el numero de la zona a la que vols anar: "))
        except ValueError:
            print("Ha ocurregut un error...")
    if pos == count:
        print("Ha decidit quedar-se on es...")
    else:
        jugador.Ubicacio = zones[disponibles[pos -1]]    # Canviem la zona i la retornem
        jugador.ActualitzarUltimPobleVisitat()
        for i in jugador.MisionsAcceptades:
            if type(i) == Missions.PlaceMission:
                if i.Objective == ubicacio:
                    i.Completed()

def OcurrenciaMisio(misio):
    if type(misio) == Missions.KillMission:
        if misio.Enemic == 1:
            aLluitar = [misio.Enemic]
        Lluitar(aLluitar)
    elif type(misio) == Missions.FindMission:
        print(f"Has trobat en/la {misio.Objective}")
        misio.Completed()
    elif type(misio) == Missions.ObjectMission:
        print(f"Has trobat l'objecte {misio.Objective.ObjectName}")
        misio.Completed()
    if type(misio) != Missions.KillMission:
        input("Presiona per a Continuar...")

def ExplorarTrobaroNo():
    global jugador
    perTrobar = len(ubicacio.Objectes)
    if perTrobar >= 1:
        choice = random.choices(["res", "objecte"], [10, 90])
        if choice == ["objecte"]:
            objectes = list(ubicacio.Objectes.keys())
            probabilitat = [j[0] for j in ubicacio.Objectes.values()]
            trobat = random.choices(objectes, probabilitat)
            ubicacio.ObjecteTrobat(trobat[0])
            print(f"Has trobat un/a {trobat[0].ObjectName}.")
            jugador.AfegirObjecte(trobat[0], 1)

    if perTrobar == 0 or choice == ["res"]:
        print("No has trobat res...")

def Explorar():
    global jugador
    print("Has començar a explorar...")
    prob = random.randrange(1, 100)
    choice = [""]
    if prob <= 20:  # Or
        TrobarOr(jugador.Ubicacio.Or)
    elif prob > 20 and prob <= 70:  # Res / Missions / Ocurrencies
        llista = []
        for i in missions:
            if i.Status == "Accepted" and i.Place == jugador.Ubicacio:
                if type(i) == Missions.KillMission:
                    if i.Generic == False:
                        llista.append(i)
                else:
                    llista.append(i)
        if len(llista) > 0:
            choice = random.choices(["res", "missio"], [80, 20])
            if choice[0] == "missio":
                misio = random.choice(llista)
                OcurrenciaMisio(misio)
        if len(llista) == 0 or choice == ["res"]:
            ExplorarTrobaroNo()
    elif prob > 70 and prob <= 95:  # Lluitar
        GenerarEnemic()
    elif prob > 95 and prob <= 100: # Seguent ruta
        TrobarSeguentZona()
        
    jugador.Ubicacio.ExplorarCount += 1
    rutaTrobada = False
    for i in jugador.Ubicacio.Connections:
        if zones[i].ZoneType == "Poble":
            if i not in jugador.LlocsTrobats:
                jugador.LlocsTrobats.append(i)
                print(f"Has trobat un cami a {zones[i].NameZone}")
                rutaTrobada = True
        else:
            if jugador.Ubicacio.ExplorarCount >= zones[i].IntentsPerTrobar and i not in jugador.LlocsTrobats:
                jugador.LlocsTrobats.append(i)
                print(f"Has trobat un cami a {zones[i].NameZone}")
                rutaTrobada = True
    if choice[0] != "missio" and prob < 70 or rutaTrobada == True:
        input("Presiona per a continuar...")
    
def TrobarSeguentZona():
    global jugador
    posiblesRutesATrobar = []
    rutesTrobades = []
    for i in jugador.Ubicacio.Connections:
        complert = zones[i].ComprobarCondicio(jugador.Team)
        if complert == True and i not in jugador.LlocsTrobats:
            posiblesRutesATrobar.append(i)
        if i in jugador.LlocsTrobats:
            rutesTrobades.append(i)
    if len(posiblesRutesATrobar) == 0:
        if len(rutesTrobades) == len(jugador.Ubicacio.Connections):
            print("Ja has trobat totes les rutes en aquesta zona...")
        else:
            print("No sembla haber-hi cap altre ruta...")
    else:
        trobat = random.choice(jugador.Ubicacio.Connections)
        print(f"Has trobat una ruta a {zones[trobat].NameZone}.")
        jugador.LlocsTrobats.append(trobat)
    input("Presiona per a continuar...")

    

def TrobarOr(moneda):
    global jugador
    mult = {"Bronze": 10, "Plata": 100, "Or": 1000, "Or Platejat": 10000}
    
    monedaTrobada = []
    
    claus = []
    weight = []
    for i in jugador.Ubicacio.Or.values():
        weight.append(i["prob"])
        claus.append(i["type"])
    if len(moneda.keys()) > 1:
        monedaTrobada = random.choices(claus, weights=weight)
    else:
        monedaTrobada = [claus[0]]

    found = random.randint(jugador.Ubicacio.Or[monedaTrobada[0]]["amount_range"][0], jugador.Ubicacio.Or[monedaTrobada[0]]["amount_range"][1])
    
    jugador.Gold += found * mult[monedaTrobada[0]]
    if monedaTrobada[0] in ["Bronze", "Plata"]:
        print(f"Has trobat {found} monedes de {monedaTrobada[0]}")
    else:
        print(f"Has trobat {found} monedes d'{monedaTrobada[0]}")
    

def MenuAtacar(personatge):
    global jugador
    res = 0
    while res not in range(1, len(personatge.Moves) + 2):
        Call.ClearScreen()
        count = 1
        for i in personatge.Moves:
            print(f"{count} -> {i.Name}")
            print(f"Power: {i.Power}, Precision: {i.Precision}")
            print(f"Mana Cost: {i.Cost}\n")
            count += 1
        print(f"{count} -> Sortir")
        try:
            res = int(input("Digues quin atac vols fer: "))
            if res not in range(1, len(personatge.Moves) + 2):
                print("Has de dir que vols fer...")
            if res == count:
                print("Has sortit")
            else:
                use = personatge.Moves[res - 1]
                if use.Cost > personatge.StatsCombat["Mana"]:
                    print("No tens suficient Mana per a realitzar aquest atac...")
                    input("Presiona per a continuar...")
                    return None
                else:
                    return use
        except ValueError:
            print("Ha ocurregut un error...")
    
def AccionsLluita(jug, enemy, enemyderr):
    global jugador
    print(f"És el torn de {jug.nom}")
    print("1 -> Atacar")
    print("2 -> Fugir")
    print("3 -> Objectes")
    print("4 -> Estat jugador")
    print("5 -> Pasar Torn")
    accio = 0
    while accio not in [1, 2, 3, 4, 5]:
        try:
            accio = int(input("Que vols fer: "))
        except ValueError:
            print("Ha ocurregut un error...")
    turn = False
    fugir = [False]
    Call.ClearScreen()
    BattleScreenShow(jugador.Team)
    BattleScreenShow(enemy)
    print("\n")
    if accio == 1:
        move = MenuAtacar(jug)
        target = None
        Call.ClearScreen()
        BattleScreenShow(jugador.Team)
        BattleScreenShow(enemy)
        print("\n")
        if move != None:
            if move.MultiTarget == False:
                if move.Healing == False and move.Protective == False:
                    target = TriarObjectius(enemy)
                else:
                    target = TriarObjectius(jugador.Team)
            else:
                target = "All"
            if move.Healing == False and move.Protective == False:
                for i in range(len(enemy)):
                    if enemy[i] == target or target == "All":
                        enemy[i] = jug.atacar(enemy[i], move)
                        enemyderr = DescartarDerrotats(enemy[i], enemyderr)
            else:
                for i in range(len(jugador.Team)):
                    if jugador.Team[i] == target or target == "All":
                        jugador.Team[i] = jug.MoveProtHeal(jugador.Team[i], move)
            jug.StatsCombat["Mana"] -= move.Cost
        if move == None or target == False:
            turn = True
    elif accio == 2:
        fugir = Fugir(enemy)
    elif accio == 3:
        used = jugador.ObjectesMochila(jugador.Team, jug, True)
        if used == False:
            turn = True
    elif accio == 4:
        Call.ClearScreen()
        VeureEstatus(True)
        turn = True
    elif accio == 4:
        print("Has decidit pasar torn...")
        input("Presiona per a continuar...")
    
    return jug, enemy, turn, fugir, enemyderr

def TriarObjectius(list):
    global jugador
    res = 0
    while res not in range(1, len(list) + 2):
        BattleScreenShow(jugador.Team)
        BattleScreenShow(list)
        Call.ClearScreen()
        targetable = []
        for i in list:
            if i.StatsCombat["CurHP"] > 0:
                targetable.append(i)
        count = 1
        for i in targetable:
            print(f"{count} -> {i.nom}, Lv: {i.Lv}")
            count += 1
        print(f"{count} -> Sortir")
        try:
            res = int(input("Digues de a qui vols atacar: "))
            if res not in range(1, count + 1):
                print("Has de dir un dels numeros corresponents...")
        except ValueError:
            print("Ha ocurregut un error...")
            input("Presiona per a continuar...")
    target = False
    if res in range(1, count):
        target = targetable[res - 1]
    return target
        

def Fugir(enemy):
    global jugador
    print("Has intentat Fugir...")
    teamSPD = 0
    for i in jugador.Team:
        teamSPD += i.StatsCombat["SPD"]
    enemySPD = 0
    for j in enemy:
        enemySPD += j.StatsCombat["SPD"]
    prob = jugador.Team[0].fleeProb * (teamSPD / enemySPD)   # fleeProb = 75 de base
   
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
    
def GenerarEnemic():
    global jugador

    pesos = []
    for j in jugador.Ubicacio.Enemies.values():
        pesos.append(j["prob"])
    opcions = list(jugador.Ubicacio.Enemies.keys())
    seleccio = random.choices(opcions, pesos)
    
    prob = jugador.Ubicacio.Enemies[seleccio[0]]["group_probs"]
    
    num = []
    count = 1
    for i in prob:
        num.append(count)
        count += 1
    qty = random.choices(num, prob)
    enemy = []

    enemy.append(Entitat.Entity("", random.randrange(jugador.Ubicacio.Enemies[seleccio[0]]["level_range"][0], jugador.Ubicacio.Enemies[seleccio[0]]["level_range"][1] + 1), False, Entities[seleccio[0]]))

    probs = []
    opcionsPosib = []

    for v in jugador.Ubicacio.Enemies[seleccio[0]]["companions"]:
        probs.append(v[1])
        opcionsPosib.append(v[0])


    if qty[0] > 1:
        for l in range(qty[0] - 1):
            if len(probs) >= 1:
                apareix = random.choices(opcionsPosib, probs)
            else:
                apareix = seleccio[0]
            entitat = Entitat.Entity("", random.randrange(jugador.Ubicacio.Enemies[seleccio[0]]["level_range"][0] - 2, enemy[0].Lv), False, Entities[apareix])
            enemy.append(entitat)
    
    Lluitar(enemy)

def ComprobarEfectEstat(entitat, derr):
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
                        derr = DescartarDerrotats(entitat, derr)
                i.RemainingTurns -= 1
        for j in eliminar:
            entitat.afected.remove(j)
    return entitat, derr

def PrioritatInicial(enemy):
    maxSpeedPlayer = max(jugador.Team, key=lambda j: j.StatsCombat["SPD"])
    maxSpeedEnemies = max(enemy, key=lambda e: e.StatsCombat["SPD"])

    maxSpeed = max(maxSpeedPlayer.StatsCombat["SPD"], maxSpeedEnemies.StatsCombat["SPD"])

    for i in range(len(jugador.Team)):
        if jugador.Team[i].StatsCombat["SPD"] == maxSpeed:
            jugador.Team[i].Priority = 100
        else:
            jugador.Team[i].Priority = (jugador.Team[i].StatsCombat["SPD"] / maxSpeed) * 100
    
    for j in range(len(enemy)):
        if enemy[j].StatsCombat["SPD"] == maxSpeed:
            enemy[j].Priority = 100
        else:
            enemy[j].Priority = (enemy[j].StatsCombat["SPD"] / maxSpeed) * 100

    return enemy

def IncrementarPrioritat(enemy):
    global jugador
    for i in range(len(jugador.Team)):
        if jugador.Team[i].StatsCombat["CurHP"] > 0:
            jugador.Team[i].Priority += jugador.Team[i].StatsCombat["SPD"] / 100  
    
    for j in range(len(enemy)):
        if enemy[j].StatsCombat["CurHP"] > 0:
            enemy[j].Priority += enemy[j].StatsCombat["SPD"] / 100
    return enemy

def BattleScreenShow(teamlist):
    teamlis = teamlist[:]

    for i in teamlis:
        if i.StatsCombat["CurHP"] < 0:
            teamlis.remove(i)

    for i in teamlis:
        llarg = len(f"{i.nom}, LV: {i.Lv}")
        espaiat = ""
        for j in range(30 - llarg):
            espaiat += " "
        print(f"{i.nom}, LV: {i.Lv}", end=espaiat)
    
    print()
    for i in teamlis:
        llarg = len(f"HP: {round(i.StatsCombat["CurHP"], 2)} / {round(i.StatsCombat["MaxHP"], 2)}")
        espaiat = ""
        for j in range(30 - llarg):
            espaiat += " "
        print(f"HP: {round(i.StatsCombat["CurHP"], 2)} / {round(i.StatsCombat["MaxHP"], 2)}", end=espaiat)
    
    saltdeLinia = False
    for i in teamlis:
        if i.isPlayer == True:
            if saltdeLinia == False:
                print()
            llarg = len(f"Mana: {round(i.StatsCombat["Mana"], 2)} / {round(i.StatsCombat["MaxMana"], 2)}")
            espaiat = ""
            for j in range(30 - llarg):
                espaiat += " "
            print(f"Mana: {round(i.StatsCombat["Mana"], 2)} / {round(i.StatsCombat["MaxMana"], 2)}", end=espaiat)
            saltdeLinia = True

    saltdeLinia = False
    for i in range(len(teamlis)):
        if len(teamlis[i].afected) > 0:
            if saltdeLinia == False:
                print()
            llarg = 0
            effect = ""
            for e in teamlis[i].afected:
                llarg += len(e.Name)
                effect += e.Name + ", "
            espaiat = ""
            for j in range(30 - llarg):
                espaiat += " "
            print(f"{effect}", end=espaiat)
            saltdeLinia = True
        else:
            afectats = False
            for k in range(i, len(teamlis)):
                if len(teamlis[k].afected) > 0:
                    afectats = True
            if afectats == True:
                espaiat = ""
                for j in range(30):
                    espaiat += " "
                print(espaiat, end="")
    
    print()
    for i in teamlis:
        llarg = len(f"Prioritat: {round(i.Priority, 1)}")
        espaiat = ""
        for j in range(30 - llarg):
            espaiat += " "
        print(f"Prioritat: {round(i.Priority, 1)}", end=espaiat)
        saltdeLinia = True
    print("\n")

def PrepararPerCombat():
    for i in jugador.Team:
        i.DefinirCombatStats()

def Lluitar(enemy):
    global jugador

    teamderr = 0
    enemyderr = 0

    PrepararPerCombat()

    enemy = PrioritatInicial(enemy)

    primer = False
    for i in jugador.Team:
        if i.Priority >= 100:
            primer = True
    

    if primer == False:
        if len(enemy) == 1:
            print(f"Has estat emboscat per {len(enemy)+1} {enemy[0].nom}s.")
        elif len(enemy) > 1:
            print(f"Has estat emboscat per un {enemy[0].nom}.")
            input("Pressiona per a continuar...")
    else:
        if len(enemy) == 1:
            print(f"Han aparegut {len(enemy)+1} {enemy[0].nom}s.")
        elif len(enemy) > 1:
            print(f"Ha aparegut un {enemy[0].nom}.")
            input("Pressiona per a continuar...")

    fugir = [False]
    combat = True
    while combat == True and fugir[0] == False: 
        # Turn Aliat
        
        for i in range(len(jugador.Team)):
            if jugador.Team[i].Priority >= 100 and len(enemy) >= 1 and jugador.Team[i].StatsCombat["CurHP"] > 0.1 and combat == True:
                turn = True
                while turn == True:
                    Call.ClearScreen()
                    BattleScreenShow(jugador.Team)
                    BattleScreenShow(enemy)
                    turn = False
                    jugador.Team[i], enemy, turn, fugir, enemyderr = AccionsLluita(jugador.Team[i], enemy, enemyderr)
                    if fugir[0] == False:
                        jugador.Team[i], teamderr = ComprobarEfectEstat(jugador.Team[i], teamderr)
                    if turn == False:
                        jugador.Team[i].Priority = 0
                Call.ClearScreen()
            if combat == True:
                combat = ComprobarFiCombat(combat, enemyderr, enemy, teamderr)

        # Turn enemic
        for j in range(len(enemy)):
            if enemy[j].Priority >= 100 and fugir[0] == False and len(jugador.Team) >= 1 and enemy[j].StatsCombat["CurHP"] > 0.1 and combat == True:
                Call.ClearScreen()
                BattleScreenShow(jugador.Team)
                BattleScreenShow(enemy)
                enemyMove = random.choice(enemy[j].Moves)
                targetable = []
                for e in jugador.Team:
                    if e.StatsCombat["CurHP"] > 0:
                        targetable.append(e)
                target = random.choice(range(len(targetable)))
                protegitPer = None
                if jugador.Team[target].Protected == True:
                    if jugador.Team[target].ProtectedBy[0] != None:
                        protegitPer = jugador.Team[target].ProtectedBy[0]
                enemy[j].atacar(jugador.Team[target], enemyMove)
                enemy[j].Priority = 0
                enemy[j], enemyderr = ComprobarEfectEstat(enemy[j], enemyderr)
                teamderr = DescartarDerrotats(jugador.Team[target], teamderr)
                if protegitPer != None:
                    teamderr = DescartarDerrotats(protegitPer, teamderr)
                Call.ClearScreen()
            if combat == True:
                combat = ComprobarFiCombat(combat, enemyderr, enemy, teamderr)
        
        enemy = IncrementarPrioritat(enemy)
    finalitzarCombat(jugador.Team)

def ComprobarFiCombat(combat, enemyderr, enemy, teamderr):
    if enemyderr == len(enemy) or teamderr == len(jugador.Team):
        combat = False
        if len(enemy) == enemyderr:
            Call.ClearScreen()
            print("Tos els enemics han estat derrotats !!")
            input("Presiona per a continuar")
    return combat

def DescartarDerrotats(p, derr):
    global jugador
    if p.StatsCombat["CurHP"] <= 0.1:
        derr += 1
        if p.isPlayer == False:
            Call.ClearScreen()
            alive = 0
            for i in range(len(jugador.Team)): 
                if jugador.Team[i].StatsCombat["CurHP"] > 0:
                    jugador.Team[i].LvlUp(p)
                    alive += 1
            if alive >= 1:
                jugador.Gold += p.Lv * 10 # 10 monedes per cada nivell, representa que es ven el derrotat.
                print(f"Has guanyat {p.Lv * 10} gold.")
                input("Presiona per a continuar...")
            Comprovacions(p)

    return derr

def Comprovacions(enemy):
    for i in missions:
        if type(i) == Missions.KillMission:
            i.IncrementCount(enemy)
    for i in jugador.Team:
        i.ComprovarSubClassesDisponibles()

def finalitzarCombat(clon):
    global jugador
    for i in range(len(jugador.Team)):
        
        if jugador.Team[i] in clon:
            for j in clon:
                if j == jugador.Team[i]:
                    jugador.Team[i].StatsCombat["CurHP"] = j.StatsCombat["CurHP"]
                    jugador.Team[i].StatsCombat["Mana"] = j.StatsCombat["Mana"]
        else:
            jugador.Team[i].StatsCombat["CurHP"] = 0
            jugador.Team[i].StatsCombat["Mana"] = 0
        jugador.Team[i].afected = []
        jugador.Team[i].DefinirCombatStats()


        
def EntityState(entity):
    print(f"{entity.nom}, LV: {entity.Lv}")
    print(f"HP: {round(entity.StatsCombat["CurHP"], 2)} / {round(entity.StatsCombat["MaxHP"], 2)}", f", Mana: {round(entity.StatsCombat["Mana"], 2)} / {round(entity.StatsCombat["MaxMana"], 2)}" if entity.isPlayer == True else "")
    # if entity.afected != "None":
    #     print(f"{entity.afected.Name}")
    print(f"Prioritat: {round(entity.Priority, 1)}")
    print("")


def main():
    print("!! - Joc Interactiu - !!")
    PostGame = False
    while True:
        alive = 1
        while alive > 0:
            Call.ClearScreen()
            AccioMenuPrincipal()
            alive = 0
            for i in jugador.Team:
                if i.StatsCombat["CurHP"] > 0:
                    alive += 1
        print(f"Has estat derrotat, t'han trobat i ara estas en la posada del ultim poble per el que has passat...")
        jugador.Ubicacio = jugador.UltimPobleVisitat
        Posada(True)
        input("Presiona per a continuar...")
        # if PostGame == False and objectes[15] in jugador.objectes.keys(): # Es pot eliminar aquest easter egg eliminant la funcio EasterEgg() i les 3 linies baix aquesta.
        #     PostGame = True   # Faria falta eliminar també el bool Easter dins el main()
        #     EasterEgg()

def EasterEgg():
    global jugador
    list = []
    # for i in entityTypes:
    #     if i.isPlayable == False:
    #         list.append(i)
    res = random.choice(list)
    jugador.Team = []
    jugador.Team[0] = Entitat.Entity(jugador.Name, 5, True, res, 999, {}, 0, True)
    print("L'efecte de la joia de la reencarnació s'ha activat...")
    input("\nPresiona per a continuar....")
    main()
        
    

if __name__ == "__main__":
    main()