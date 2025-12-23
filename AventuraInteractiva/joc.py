# Arxiu: joc.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem el programa principal del joc d'aventures per terminal.

# Llibreries
import os
import random

# Moduls
import Entitat
import EntityType
import Zones
import Objectes
import Exits
import Missions
import Titles
import Characteristics

def ClearScreen():
    os.system("cls" if os.name == "nt" else "clear")

    # Preparació Joc
        # Moves
movements = [
    Characteristics.Moves("Bola de Foc", "Bola de foc formada amb magia",
                          50, 100, True, 5, (False, "None")),
    Characteristics.Moves("Fletxa Perforant", "Fletxa altament perforant gracies a poder magic",
                          40, 100, False, 5, (False, "None")),
    Characteristics.Moves("Asalt Relampeg", "Impuls de velocitat i atacs repetits",
                          40, 100, False, 5, (True, ("SPD", 1.1))),
    Characteristics.Moves("Tall Potent", "Tall altament poderos, fortaleix el cos amb magia.",
                          50, 100, False, 5, (False, ("ATK", 1.1))),
    Characteristics.Moves("Aixafar", "Potent Mossegada",
                          50, 90, False, 0, (False, ("None"))),
]
        # Skills
skills = [

]

        # Entitats
entityTypes = [
        EntityType.EntityType("Guerrer", True, 160, 100, 140, 40, 130, 80, 50, ["Human"], 
                              "Alta salut, resistencia i força pero lenta.",
                              {movements[3]: 3}
                              ),
      
        EntityType.EntityType("Mag", True, 80, 200, 60, 180, 100, 100, 50, ["Human"], 
                              "Alt atac, però poca salut, resistencia i velocitat equilibrades.",
                              {movements[0]: 3}),
       
        EntityType.EntityType("Arquer", True, 120, 140, 140, 100, 140, 140, 50, ["Human"], 
                              "Resistencia, Atac i Velocitat equilibrats.",
                              {movements[1]: 3}),
       
        EntityType.EntityType("Lladre", True, 120, 120, 130, 100, 120, 160, 50, ["Human"], 
                              "Alta velocitat, salut i resistencia equilibrades, atac mitja.",
                              {movements[2]: 3}),
       
        EntityType.EntityType("Llop", False, 120, 40, 120, 20, 100, 140, 30, ["Beast"], 
                              "Animal comú, pot ser perillos si no es te cuidado.",
                              {movements[4]: 3}),
       
        EntityType.EntityType("Slime", False, 100, 100, 100, 100, 100, 100, 20, ["Monster"], 
                              "Entitat no massa perillosa, però s'ha de ser cuidados.",
                              {movements[4]: 3}),
       
        EntityType.EntityType("Sombra",False, 150, 150, 150, 150, 150, 150, 70, ["Monster"], 
                              "Dificil de veure, en la foscor.",
                              {movements[4]: 3}),
       
        EntityType.EntityType("Llangardaix de Roca", False, 160, 120, 160, 50, 160, 100, 100, ["Beast", "Monster"], 
                              "Llangardaix amb pell de roca, es molt perillos.",
                              {movements[4]: 3}),
       
        EntityType.EntityType("Driade", False, 100, 230, 100, 250, 100, 100, 120, ["Spirit"], 
                              "Enitat espiritual que formada per la energia de les plantes.",
                              {movements[4]: 3}),
       
        EntityType.EntityType("Treant", False, 200, 140, 150, 120, 150, 100, 220, ["Monster", "Spirit"], 
                              "Un arbre malevol, en algunes ocasions no ho són.",
                              {movements[4]: 3}),
        
        EntityType.EntityType("Golem", False, 250, 100, 160, 80, 200, 60, 500, ["Artificial"], 
                              "Monstre de Roca, es una forma de vida artificial feta de pedra.",
                              {movements[3]: 3}),
]

# Creem la funcio per a generar els grups d'entitats algo aixi com els tipus.
entityGroups = {}
def AddEntityGroups():
    global entityGroups
    for i in entityTypes:
        for j in i.EntityGroup:
            if j not in entityGroups.keys():
                entityGroups[j]=[i]
            else:
                entityGroups[j]+=[i]
AddEntityGroups()

        # Zones
zones = [
        Zones.Zona("Dawn Village",
                   "Un poble que representa l'inici, es diu que és el poble on va neixer l'heroi de les llegendes...",
                   "Poble", {entityTypes[6]: 20, entityTypes[6]: 10, entityTypes[6]: 10, entityTypes[6]: 60},
                    (1, 5), {"Bronze": [(1, 7), 100]}, True),
        Zones.Zona("Bosc Obscur",
                   "La zona exterior del bosc obscur, d'on es diu que surjeren els monstres...",
                   "Bosc", {entityTypes[4]: 65, entityTypes[5]: 30, entityTypes[6]: 5}, 
                   (3, 7), {"Bronze": [(1, 7), 100]}, True),
        Zones.Zona("Profunditats del Bosc Obscur",
                   "Les profunditats del bosc obscur, una perillosa zona de la que és diu que qui hi entra no en surt...",
                   "Bosc", {entityTypes[4]: 32, entityTypes[5]: 40, entityTypes[6]: 20, entityTypes[8]: 5, entityTypes[9]: 3}, 
                   (5, 15), {"Bronze": [(5, 15), 100]}),
        Zones.Zona("Centre del Bosc Obscur",
                   "La zona central del bosc obscur, hi habiten monstres desconeguts, ningú ha tornat mai d'aquest lloc...",
                   "Bosc", {entityTypes[6]: 30, entityTypes[8]: 30, entityTypes[9]: 40}, 
                   (14, 30), {"Bronze": [(20, 50), 60], "Plata": [(3, 10), 40]}),
        Zones.Zona("Muntanyes del Origen",
                   "Unes muntanyes només conegudes per llegendes, es diu que són el primer lloc en ser creat d'aquest món...",
                   "Muntanya", {entityTypes[7]: 50, entityTypes[8]: 20, entityTypes[9]: 20, entityTypes[10]: 10}, 
                   (30, 45), {"Plata": [(40, 100), 70], "Or": [(1, 10), 30]}),
        Zones.Zona("Cavernes del Origen",
                   "Les cavernes de les muntanyes del origen, no és te coneixement de la existencia d'aquestes...",
                   "Cavernes", {entityTypes[6]: 40, entityTypes[7]: 30, entityTypes[10]: 30}, 
                   (43, 60), {"Plata": [(40, 100), 70], "Or": [(1, 10), 20], "Or Platejat": [(1, 1), 10]})
]
        # Connexions de cada zona
zones[0].AddConnections([zones[1]])
zones[1].AddConnections([zones[0], zones[2]])
zones[2].AddConnections([zones[1], zones[3]])
zones[3].AddConnections([zones[2], zones[4]])
zones[4].AddConnections([zones[3], zones[5]])
zones[5].AddConnections([zones[4]])

        # Objectes
objectes = [
            # Objectes de Combat
            Objectes.ObjecteCombat("Pocio Inferior", "Cura 10 punts de vida", "Health", 10, 100),
            Objectes.ObjecteCombat("Pocio", "Descripcio", "Health", 20, 300),
            Objectes.ObjecteCombat("Pocio Intermitja", "Descripcio", "Health", 40, 750),
            Objectes.ObjecteCombat("Pocio Avançada", "Descripcio", "Health", 60, 2000),
            Objectes.ObjecteCombat("Pocio Completa", "Descripcio", "Health", 100, 4000),
            Objectes.ObjecteCombat("Elixir", "Descripcio", "Health", 9999, 10000),
            Objectes.ObjecteCombat("Millora", "Descripcio", "ATK", 1.3, 300),
            Objectes.ObjecteCombat("Millora Superior", "Descripcio", "ATK", 2, 750),
            Objectes.ObjecteCombat("Millora Divina", "Descripcio", "ATK", 2.5, 2000),
            Objectes.ObjecteCombat("Barrera", "Descripcio", "DEF", 1.3, 300),
            Objectes.ObjecteCombat("Barrera Pentagonal", "Descripcio", "DEF", 2, 750),
            Objectes.ObjecteCombat("Barrera Octagonal", "Descripcio", "DEF", 2.5, 2000),
            Objectes.ObjecteCombat("Carrera", "Descripcio", "SPD", 1.3, 300),
            Objectes.ObjecteCombat("Llampeg", "Descripcio", "SPD", 2, 750),
            Objectes.ObjecteCombat("Raig", "Descripcio", "SPD", 2.5, 2000),
            
            # Objectes de Combat
            Objectes.ObjecteClau("Pedra Misteriosa", "???"),
            ]
# Botiga
botiga = [objectes[0],
          objectes[6],
          objectes[9],
          objectes[12],
          ]

titles = [
    # Basic Grade
    Titles.Titles("Beast Slayer", "Augmenta el dany causat contra enemics de tipus Bestia",
                  entityGroups["Beast"], 1.3),
    Titles.Titles("Human Slayer", "Augmenta el dany causat contra enemics de tipus Human",
                  entityGroups["Human"], 1.3),
    Titles.Titles("Spirit Slayer", "Augmenta el dany causat contra enemics de tipus Spirit",
                  entityGroups["Spirit"], 1.3),
    Titles.Titles("Monster Slayer", "Augmenta el dany causat contra enemics de tipus Monster",
                  entityGroups["Monster"], 1.3),
    Titles.Titles("Artificial Slayer", "Augmenta el dany causat contra enemics de tipus Artificial",
                  entityGroups["Artificial"], 1.3),
    
    # Intermediate Grade
    Titles.Titles("Beast Slayer", "Augmenta el dany causat contra enemics de tipus Bestia",
                  entityGroups["Beast"], 1.2),
    Titles.Titles("Human Slayer", "Augmenta el dany causat contra enemics de tipus Human",
                  entityGroups["Human"], 1.2),
    Titles.Titles("Spirit Slayer", "Augmenta el dany causat contra enemics de tipus Spirit",
                  entityGroups["Spirit"], 1.2),
    Titles.Titles("Monster Slayer", "Augmenta el dany causat contra enemics de tipus Monster",
                  entityGroups["Monster"], 1.2),
    Titles.Titles("Artificial Slayer", "Augmenta el dany causat contra enemics de tipus Artificial",
                  entityGroups["Artificial"], 1.2),
    
    # Advanced
    Titles.Titles("Beast Slayer", "Augmenta el dany causat contra enemics de tipus Bestia",
                  entityGroups["Beast"], 1.5),
    Titles.Titles("Human Slayer", "Augmenta el dany causat contra enemics de tipus Human",
                  entityGroups["Human"], 1.5),
    Titles.Titles("Spirit Slayer", "Augmenta el dany causat contra enemics de tipus Spirit",
                  entityGroups["Spirit"], 1.5),
    Titles.Titles("Monster Slayer", "Augmenta el dany causat contra enemics de tipus Monster",
                  entityGroups["Monster"], 1.5),
    Titles.Titles("Artificial Slayer", "Augmenta el dany causat contra enemics de tipus Artificial",
                  entityGroups["Artificial"], 1.5),
    
]

    # Exits (Achievements / Logros)
achievements = [
    # Exits d'estadistiques
    Exits.StatusExit("Lv 10", "Arriba al nivell 10", "Lv", 10, 5, "AllStats"),
    Exits.StatusExit("Lv 20", "Arriba al nivell 10", "Lv", 20, 5, "AllStats"),
    Exits.StatusExit("Lv 30", "Arriba al nivell 10", "Lv", 30, 5, "AllStats"),
    Exits.StatusExit("Lv 40", "Arriba al nivell 10", "Lv", 40, 5, "AllStats"),
    Exits.StatusExit("Lv 50", "Arriba al nivell 10", "Lv", 50, 5, "AllStats"),
    Exits.StatusExit("ATK 50", "Arriba a 50 ATK", "ATK", 50, 3, "ATK"),
    Exits.StatusExit("ATK 100", "Arriba a 100 ATK", "ATK", 100, 3, "ATK"),
    Exits.StatusExit("ATK 150", "Arriba a 150 ATK", "ATK", 150, 3, "ATK"),
    Exits.StatusExit("ATK 200", "Arriba a 200 ATK", "ATK", 200, 3, "ATK"),
    Exits.StatusExit("DEF 50", "Arriba a 50 ATK", "DEF", 50, 3, "DEF"),
    Exits.StatusExit("DEF 100", "Arriba a 100 ATK", "DEF", 100, 3, "DEF"),
    Exits.StatusExit("DEF 150", "Arriba a 150 ATK", "DEF", 150, 3, "DEF"),
    Exits.StatusExit("DEF 200", "Arriba a 200 ATK", "DEF", 200, 3, "DEF"),
    Exits.StatusExit("SPD 50", "Arriba a 50 ATK", "SPD", 50, 3, "SPD"),
    Exits.StatusExit("SPD 100", "Arriba a 100 ATK", "SPD", 100, 3, "SPD"),
    Exits.StatusExit("SPD 150", "Arriba a 150 ATK", "SPD", 150, 3, "SPD"),
    Exits.StatusExit("SPD 200", "Arriba a 200 ATK", "SPD", 200, 3, "SPD"),
    Exits.StatusExit("HP 50", "Arriba a 50 HP", "HP", 50, 5, "HP"),
    Exits.StatusExit("HP 100", "Arriba a 100 HP", "HP", 100, 5, "HP"),
    Exits.StatusExit("HP 150", "Arriba a 150 HP", "HP", 150, 5, "HP"),
    Exits.StatusExit("HP 200", "Arriba a 200 HP", "HP", 200, 5, "HP"),

    # Exits de Derrotar Enemics
    Exits.KillExit("Beast Slayer", "Derrota 10 monstres de tipus bestia", 
                   entityGroups["Beast"], 10, titles[0], "Title"),
    Exits.KillExit("Exterminador de Besties", "Derrota 50 monstres de tipus bestia", 
                   entityGroups["Beast"], 50, titles[5], "Title"),
    Exits.KillExit("Aniquilador de Besties", "Derrota 100 monstres de tipus bestia", 
                   entityGroups["Beast"], 100, titles[10], "Title"),
    Exits.KillExit("Monster Slayer", "Derrota 10 monstres de tipus Monstre", 
                   entityGroups["Monster"], 10, titles[3], "Title"),
    Exits.KillExit("Exterminador de Monstres", "Derrota 50 monstres de tipus Monstre", 
                   entityGroups["Monster"], 50, titles[8], "Title"),
    Exits.KillExit("Aniquilador de Monstres", "Derrota 100 monstres de tipus Monstre", 
                   entityGroups["Monster"], 100, titles[13], "Title"),
    Exits.KillExit("Human Slayer", "Derrota 10 monstres de tipus Huma", 
                   entityGroups["Human"], 10, titles[1], "Title"),
    Exits.KillExit("Exterminador d'Humans", "Derrota 50 monstres de tipus Huma", 
                   entityGroups["Human"], 50, titles[6], "Title"),
    Exits.KillExit("Aniquilador d'Humans", "Derrota 100 monstres de tipus Huma", 
                   entityGroups["Human"], 100, titles[11], "Title"),
    Exits.KillExit("Spirit Slayer", "Derrota 10 monstres de tipus esperit", 
                   entityGroups["Spirit"], 10, titles[2], "Title"),
    Exits.KillExit("Exterminador d'esperits", "Derrota 50 monstres de tipus esperit", 
                   entityGroups["Spirit"], 50, titles[7], "Title"),
    Exits.KillExit("Aniquilador d'esperits", "Derrota 100 monstres de tipus esperit", 
                   entityGroups["Spirit"], 100, titles[12], "Title"),
    Exits.KillExit("Artificial Slayer", "Derrota 10 monstres de tipus Artificial", 
                   entityGroups["Artificial"], 10, titles[4], "Title"),
    Exits.KillExit("Exterminador Artificial", "Derrota 50 monstres de tipus Artificial", 
                   entityGroups["Artificial"], 50, titles[9], "Title"),
    Exits.KillExit("Aniquilador Artificial", "Derrota 100 monstres de tipus Artificial", 
                   entityGroups["Artificial"], 100, titles[14], "Title"),
]

missions = [
    Missions.KillMission("Eliminant el Perill", 
                         "Troba i elimina al perillos golem que amenaça el poble, diuen que s'ha vist recentment per el Bosc Obscur", 
                         [("XP", 3000), ("Gold", 10000), (objectes[15], 1)], 1, entityTypes[10], [("Lv", 5)], zones[3], False,
                         Entitat.Entity("El Golem de Roca", 40, False, entityTypes[10])),

    Missions.KillMission("Mostra de Confiança", 
                         "Troba i elimina al Llop lider, diuen que s'ha vist recentment per el Bosc Obscur", 
                         [("XP", 120), ("Gold", 1000), (objectes[1], 1)], 1, entityTypes[4], [("Lv", 5)], zones[1], False,
                         Entitat.Entity("Llop Lider", 9, False, entityTypes[4])),
]

missions.append(
    Missions.KillMission("Mostra de Confiança II", 
    "Elimina les restes de la manada de Llops en el bosc obscur.", 
    [("XP", 300), ("Gold", 2000), (objectes[1], 1)], 10, entityTypes[4], 
    [("Lv", 5), missions[1]], zones[1], False),
    )



def CrearJugador():
    nom = ""
    while nom == "":
        try:
            nom = input("Digues el nom del teu personatge: ")
        except ValueError:
            print("Ha ocurregut un error...")
    clase = ""
    clases = []
    nomclases = []
    print("")
    for i in entityTypes:
        if i.isPlayable == True:
            clases.append(i)
            nomclases.append(i.EntityName.lower())
    while clase not in nomclases:
        try:
            for i in clases:
                print(f"{i.EntityName}, {i.EntityDescription}.")
            clase = input("\nDigues una de les clases mostrades anteriorment: ").lower()
            if clase not in nomclases:
                print(f"Has de dir una de les clases anteriors: {nomclases}")
        except ValueError:
            print("Ha ocurregut un error...")
    
    jugador = None
    temp = 0
    while jugador == None:
        if clases[temp].EntityName.lower() == clase:
            jugador = Entitat.Entity(nom, 5, True, clases[temp])
        temp += 1

    return jugador

# Cridem la funcio per crear el jugador, la variable ubicacio, i la variable de diccionari amb els grups i les seves entitats
jugador = CrearJugador()
ubicacio = zones[0]


# Afegim algun objecte al jugador de base
jugador.AfegirObjecte(objectes[0], 2)
jugador.AfegirObjecte(objectes[6], 2)

def AccioMenuPrincipal():
    global jugador, ubicacio
    
    pos = 0

    # Seleccionem el menu
    if ubicacio.ZoneType == "Poble":
        menu = {1: "Mapa", 2: "Mochila", 3: "Posada", 4: "Botiga", 5: "Estat", 6: "Misions", 7: "Exits", 8: "Guardar", 9: "Info"}
    elif ubicacio.ZoneType != "Poble":
        menu = {1: "Explorar", 2: "Mochila", 3: "Lluitar", 4: "Estat", 5: "Mapa", 6: "Misions", 7: "Exits", 8: "Guardar", 9: "Info"}

    print(f"Vostre es troba a {ubicacio.NameZone}")
    while pos not in menu.keys():   # Generem la llista del menu
        for i in menu.keys():
            print(f"{i} -> {menu.get(i)}")
        try:
            pos = int(input("Digues quina acció vols fer: "))   # Demanem accio del menu
        except ValueError:
            print("Ha ocurregut un error...")
            input("Presiona per a continuar...")
        ClearScreen()

    # Executem acció seleccionada
    if menu.get(pos) == "Mapa":
        Mapa()
    elif menu.get(pos) == "Explorar":
        Explorar()
    elif menu.get(pos) == "Posada":
        Posada()
    elif menu.get(pos) == "Botiga":
        Botiga()
    elif menu.get(pos) == "Estat":
        jugador.ShowStatus()
    elif menu.get(pos) == "Misions":
        MenuMisions()
    elif menu.get(pos) == "Lluitar":
        GenerarEnemic()
    elif menu.get(pos) == "Guardar":
        print("")
    elif menu.get(pos) == "Exits":
        MostrarExits()
    elif menu.get(pos) == "Mochila":
        jugador.ObjectesMochila()
    elif menu.get(pos) == "Info":
        print("Info (Ajuda sobre les opcions del menu...)")

def MenuMisions():
    res = 0
    while res not in [1, 2, 3, 4]:
        res = 0
        ClearScreen()
        print("1 -> Veure Misions")
        print("2 -> Acceptar Misions")
        print("3 -> Reclamar Misions")
        print("4 -> Sortir")
        try:
            res = int(input("Digues el numero segons el que vols fer: "))
            if res not in [1, 2, 3, 4]:
                print("Has de dir un dels numeros segons el que vols fer...")
            elif res == 1:
                filtrar = 0
                while filtrar not in [1, 2, 3, 4, 5]:
                    ClearScreen()
                    print("1 -> Totes")
                    print("2 -> Aceptades")
                    print("3 -> Requisits Complerts per aceptar")
                    print("4 -> Completades")
                    print("5 -> Sortir")
                    try:
                        filtrar = int(input("Digues que vols fer: "))
                        if filtrar not in [1, 2, 3, 4, 5]:
                            print("Has de dir un dels numeros segons el que vols fer...")
                    except ValueError:
                        print("Ha ocurregut un error...")
                if filtrar == 2:
                    count, reclamar = ShowMisions("Accepted", "Res")
                elif filtrar == 4:
                    count, reclamar = ShowMisions("Completed", "Res")
                elif filtrar == 3:
                    count, reclamar  = ShowMisions("Requisites", "Res")
                elif filtrar == 1:
                    count, reclamar  = ShowMisions("Totes", "Res")
            elif res == 2:
                count, reclamar  = ShowMisions("Requisites", "Aceptar")
                aceptar = 0
                while aceptar not in range(1, count + 1):
                    ClearScreen()
                    count, reclamar  = ShowMisions("Requisites", "Aceptar")
                    try:
                        aceptar = int(input("Digues quina misio vols aceptar: "))
                        if aceptar < count + 1 and aceptar > 0:
                            if aceptar == count:
                                print("Has sortit")
                            else:
                                reclamar[aceptar - 1].Aceptar(jugador)
                    except ValueError:
                        print("Ha ocurregut un error...")
            elif res == 3:
                count, reclamar  = ShowMisions("Rewards Unclaimed", "Aceptar")
                aceptar = 0
                while aceptar not in range(1, count + 1):
                    ClearScreen()
                    count, reclamar  = ShowMisions("Rewards Unclaimed", "Aceptar")
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
    
def ShowMisions(filter, accio):
    count = 1
    llista = []
    for i in missions:
        i.RequisitesCompleted(jugador)
        if i.Status == filter:
            print(f"\n{count} -> {i.Name}")
            print(f"Estat: {i.Status}")
            print(f"{i.Description}")
            count += 1
            llista.append(i)
            if filter == "Requisites":
                i.ShowRequisites()
        if filter == "Totes":
            print(f"\n{count} -> {i.Name}")
            print(f"Estat: {i.Status}\n")
            count += 1
    if accio != "Res":
        print(f"{count} -> Sortir")
    return count, llista


def MostrarExits():
    print("Exits")
    for i in achievements:
        if i.Obtained == True:
            obtingut = "Obtingut"
        else:
            obtingut = "No Obtingut"
        print(f"{i.Name}, {obtingut}")
        if type(i) != Exits.KillExit:
            print(f"{i.Description} \n")
        else:
            print(f"{i.Description}, \n{i.Count} / {i.Quantity}\n")
    input("Presiona per a continuar...")

def ComprovarExits(enemy):
    for i in achievements:
        if i.Obtained == False:
            if type(i) == Exits.KillExit:
                i.IncrementCount(enemy)
            i.Completed(jugador)


def PrepararBotiga(): # Afegir objectes segons nivell
    global jugador
    if jugador.Lv > 10:
        if [objectes[1], objectes[7], objectes[10], objectes[13]] not in botiga:
            botiga.append(objectes[1])
            botiga.append(objectes[7])
            botiga.append(objectes[10])
            botiga.append(objectes[13])
    if jugador.Lv > 20:
        if [objectes[2], objectes[8], objectes[11], objectes[14]] not in botiga:
            botiga.append(objectes[2])
            botiga.append(objectes[8])
            botiga.append(objectes[11])
            botiga.append(objectes[14])
    if jugador.Lv > 35:
        if [objectes[3], objectes[4], objectes[5]] not in botiga:
            botiga.append(objectes[3])
            botiga.append(objectes[4])
            botiga.append(objectes[5])

def Botiga():
    PrepararBotiga()
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
        jugador.gold -= botiga[res].Preu * qty
        print(f"Has comprat {qty} {botiga[res].ObjectName} per {botiga[res].Preu * qty} gold !")

def Posada():
    global jugador
    res = ""
    while res not in ["S", "N"]:
        ClearScreen()
        try:
            res = input("\nVols descansar? Costa 100 gold (S / N): ").capitalize()
        except ValueError:
            print("Ha ocurregut un error...")
    if res == "S":
        if jugador.gold >= 100:
            print("Has descansat comodament, t'has recuperat completament...")
            jugador.gold -= 100
            jugador.CurHP = jugador.MaxHP
        else:
            print("No tens suficient gold per pagar la posada, has marxat sense poder descansar...")
    else:
        print("Has marxat...")

def Mapa():
    global ubicacio
    count = 1
    disponibles = []
    print(f"VOsté és a {ubicacio.NameZone}.\n")
    for i in ubicacio.Connections:  # Mostrem ubicacions disponibles
        if i.Trobada == True:
            print(f"{count} -> {i.NameZone}")
            count += 1
            disponibles.append(i)
            if count > len(ubicacio.Connections):
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
        ubicacio = disponibles[pos - 1]    # Canviem la zona i la retornem

def OcurrenciaMisio(misio):
    if type(misio) == Missions.KillMission:
        Lluitar(misio.Enemic)
    elif type(misio) == Missions.FindMission:
        print(f"Has trobat {misio.Objective}")
        misio.Completed()
    elif type(misio) == Missions.ObjectMission:
        print(f"Has trobat {misio.Objective}")
        misio.Completed()


def Explorar():
    global jugador, ubicacio
    print("Has començar a explorar...")
    prob = random.randrange(1, 100)
    choice = [""]
    if prob <= 20:  # Or
        TrobarOr(ubicacio.Or.keys())
    elif prob > 20 and prob <= 60:  # Res
        llista = []
        for i in missions:
            if i.Status == "Accepted" and i.Place == ubicacio:
                if type(i) == Missions.KillMission:
                    if i.Generic == False:
                        llista.append(i)
                else:
                    llista.append(i)
        if len(llista) > 0:
            choice = random.choices(["res", "missio"], [90, 10])
            if choice[0] == "missio":
                misio = random.choice(llista)
                OcurrenciaMisio(misio)
            else:
                print("No has trobat res...")   
        else:
            print("No has trobat res...")
    elif prob > 60 and prob <= 90:  # Lluitar
        GenerarEnemic()
    elif prob > 90 and prob <= 100: # Seguent ruta
        print("Has trobat una ruta a la seguent zona...")
        for i in ubicacio.Connections:
            if i.Trobada == False:
                i.Trobada = True
    if prob <= 60 or prob > 90 or choice[0] == "missio":
        input("Presiona per a continuar...")

def TrobarOr(moneda):
    global ubicacio, jugador
    moneda = list(moneda)
    mult = 10
    if len(moneda) < 2:
        found = random.randint(ubicacio.Or[moneda[0]][0][0], ubicacio.Or[moneda[0]][0][1])
        print(f"Has trobat {found} monedes de {moneda[0]}")
    else:
        weight = []
        for i in ubicacio.Or.values():
            weight.append(i[1])
        moneda = random.choices(moneda, weight)
        found = random.randint(ubicacio.Or[moneda[0]][0][0], ubicacio.Or[moneda[0]][0][1])
        if moneda[0] == "Bronze":
            mult = 10
            print(f"Has trobat {found} monedes de {moneda[0]}")
        elif moneda[0] == "Plata":
            mult = 100
            print(f"Has trobat {found} monedes de {moneda[0]}")
        elif moneda[0] == "Or":
            mult = 1000
            print(f"Has trobat {found} monedes d'{moneda[0]}")
        elif moneda[0] == "Or Platejat":
            mult = 10000
            print(f"Has trobat {found} monedes d'{moneda[0]}")
    jugador.gold += found * mult

def MenuAtacar():
    global jugador
    res = 0
    while res not in range(1, len(jugador.Moves) + 2):
        ClearScreen()
        count = 1
        for i in jugador.Moves:
            print(f"{count} -> {i.Name}")
            print(f"Power: {i.Power}, Precision: {i.Precision}\n")
            count += 1
        print(f"{count} -> Sortir")
        try:
            res = int(input("Digues quin atac vols fer: "))
            if res not in range(1, len(jugador.Moves) + 2):
                print("Has de dir que vols fer...")
            if res == count:
                print("Has sortit")
            else:
                use = jugador.Moves[res - 1]
                if use.Cost > jugador.Mana:
                    print("No tens suficient Mana per a realitzar aquest atac...")
                    input("Presiona per a continuar...")
                    return None
                else:
                    return use
        except ValueError:
            print("Ha ocurregut un error...")
    
def AccionsLluita(enemy):
    global jugador
    print("1 -> Atacar")
    print("2 -> Fugir")
    print("3 -> Objectes")
    print("4 -> Estat jugador")
    accio = 0
    while accio not in [1, 2, 3, 4]:
        try:
            accio = int(input("Que vols fer: "))
        except ValueError:
            print("Ha ocurregut un error...")
    turn = False
    fugir = [False]
    if accio == 1:
        move = MenuAtacar()
        ClearScreen()
        EntityState(jugador)
        EntityState(enemy)
        print("\n")
        if move != None:
            enemy = jugador.atacar(enemy, move)
        else:
            turn = True
    elif accio == 2:
        fugir = Fugir(enemy)
    elif accio == 3:
        used = jugador.ObjectesMochila(True)
        if used == False:
            turn = True
    elif accio == 4:
        ClearScreen()
        jugador.ShowStatus(True)
        turn = True
    
    return enemy, turn, fugir

def Fugir(enemy):
    global jugador
    print("Has intentat Fugir...")
    prob = jugador.fleeProb * (jugador.SPD / enemy.SPD)   # fleeProb = 75 de base
   
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
    global ubicacio
    opcions = list(ubicacio.Enemies.keys())
    seleccio = random.choices(opcions, ubicacio.Enemies.values())
    enemy = Entitat.Entity("", random.randrange(ubicacio.LevelRange[0], ubicacio.LevelRange[1] + 1), False, seleccio[0])
    Lluitar(enemy)

def Lluitar(enemy):
    global jugador, ubicacio

    print(f"Ha aparegut un {enemy.nom}")

    turn = False
    if jugador.SPD >= enemy.SPD:
        turn = True
    fugir = [False]
    while jugador.CurHP > 0 and enemy.CurHP > 0 and fugir[0] == False: 
        ClearScreen()
        EntityState(jugador)
        EntityState(enemy)
        print("\n")
        if turn == True:
            enemy, turn, fugir = AccionsLluita(enemy)
        else:
            enemyMove = random.choice(enemy.Moves)
            enemy.atacar(jugador, enemyMove)
            if jugador.CurHP <= 0:
                print("Has estat derrotat...")
            else:
                turn = True
        input("\nPresiona per a continuar...")
    if enemy.CurHP <= 0:
        print(f"{enemy.nom}, ha estat derrotat !!")
        finalitzarCombat()
        jugador.LvlUp(enemy)
        jugador.gold += enemy.Lv * 10 # 10 monedes per cada nivell, representa que es ven el derrotat.
        print(f"Has guanyat {enemy.Lv * 10} gold.")
        ComprovarExits(enemy)
        ComprovarMisions(enemy)
    else:
        finalitzarCombat()

def ComprovarMisions(enemy):
    for i in missions:
        if type(i) == Missions.KillMission:
            i.IncrementCount(enemy)

def finalitzarCombat():
    global jugador
    jugador.DefinirTempStats()
        
def EntityState(entity):
    print(f"{entity.nom}, LV: {entity.Lv}, HP: {round(entity.CurHP, 2)} / {round(entity.MaxHP, 2)}", f", Mana: {round(entity.Mana, 2)} / {round(entity.MaxMana, 2)}" if entity.isPlayer == True else "")

def main():
    print("!! - Joc Interactiu - !!")
    PostGame = False
    while jugador.CurHP > 0:
        ClearScreen()
        AccioMenuPrincipal()
    if PostGame == False and objectes[15] in jugador.objectes.keys(): # Es pot eliminar aquest easter egg eliminant la funcio EasterEgg() i les 3 linies baix aquesta.
        PostGame = True   # Faria falta eliminar també el bool Easter dins el main()
        EasterEgg()

def EasterEgg():
    global jugador
    list = []
    for i in entityTypes:
        if i.isPlayable == False:
            list.append(i)
    res = random.choice(list)
    jugador = Entitat.Entity(jugador.nom, 5, True, res, 999, {}, 0, True)
    print("L'efecte de la joia de la reencarnació s'ha activat...")
    input("\nPresiona per a continuar....")
    main()
        
    

if __name__ == "__main__":
    main()