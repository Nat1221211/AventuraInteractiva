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

    # Preparació Joc
        # Entitats
EntityTypes = [
        EntityType.EntityType("Guerrer",True,160,140,130,80,50, "Alta salut, resistencia i força pero lenta."),
        EntityType.EntityType("Mag",True,80,180,100,100,50, "Alt atac, però poca salut, resistencia i velocitat equilibrades."),
        EntityType.EntityType("Arquer",True,120,140,140,140,50, "Resistencia, Atac i Velocitat equilibrats."),
        EntityType.EntityType("Lladre",True,120,130,120,160,50, "Alta velocitat, salut i resistencia equilibrades, atac mitja."),
        EntityType.EntityType("Llop",False,120,120,100,140,30, "Animal comú, pot ser perillos si no es te cuidado."),
        EntityType.EntityType("Slime",False,100,100,100,100,20, "Entitat no massa perillosa, però s'ha de ser cuidados."),
        EntityType.EntityType("Sombra",False,150,150,150,150,70, "Dificil de veure, en la foscor."),
        EntityType.EntityType("Llangardaix de Roca",False,160,160,160,100,100, "Llangardaix amb pell de roca, es molt perillos."),
        EntityType.EntityType("Driade",False,100,200,100,100,120, "Enitat espiritual que formada per la energia de les plantes."),
        EntityType.EntityType("Treant",False,200,150,150,100,220, "Un arbre malevol, en algunes ocasions no ho són."),
        EntityType.EntityType("Golem",False,200,160,200,60,500, "Monstre de Roca, es una forma de vida artificial feta de pedra."),
]
        # Zones
zones = [
        Zones.Zona("Dawn Village",
                   "Un poble que representa l'inici, es diu que és el poble on va neixer l'heroi de les llegendes...",
                   "Poble", {EntityTypes[6]: 20, EntityTypes[6]: 10, EntityTypes[6]: 10, EntityTypes[6]: 60},
                    (1, 5), {"Bronze": [(1, 7), 100]}, True),
        Zones.Zona("Bosc Obscur",
                   "La zona exterior del bosc obscur, d'on es diu que surjeren els monstres...",
                   "Bosc", {EntityTypes[4]: 65, EntityTypes[5]: 30, EntityTypes[6]: 5}, 
                   (3, 7), {"Bronze": [(1, 7), 100]}, True),
        Zones.Zona("Profunditats del Bosc Obscur",
                   "Les profunditats del bosc obscur, una perillosa zona de la que és diu que qui hi entra no en surt...",
                   "Bosc", {EntityTypes[4]: 32, EntityTypes[5]: 40, EntityTypes[6]: 20, EntityTypes[8]: 5, EntityTypes[9]: 3}, 
                   (5, 15), {"Bronze": [(5, 15), 100]}),
        Zones.Zona("Centre del Bosc Obscur",
                   "La zona central del bosc obscur, hi habiten monstres desconeguts, ningú ha tornat mai d'aquest lloc...",
                   "Bosc", {EntityTypes[6]: 30, EntityTypes[8]: 30, EntityTypes[9]: 40}, 
                   (14, 30), {"Bronze": [(20, 50), 60], "Plata": [(3, 10), 40]}),
        Zones.Zona("Muntanyes del Origen",
                   "Unes muntanyes només conegudes per llegendes, es diu que són el primer lloc en ser creat d'aquest món...",
                   "Muntanya", {EntityTypes[7]: 50, EntityTypes[8]: 20, EntityTypes[9]: 20, EntityTypes[10]: 10}, 
                   (30, 45), {"Plata": [(40, 100), 70], "Or": [(1, 10), 30]}),
        Zones.Zona("Cavernes del Origen",
                   "Les cavernes de les muntanyes del origen, no és te coneixement de la existencia d'aquestes...",
                   "Cavernes", {EntityTypes[6]: 40, EntityTypes[7]: 30, EntityTypes[10]: 30}, 
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
            Objectes.ObjecteCombat("Força", "Descripcio", "ATK", 1.3, 300),
            Objectes.ObjecteCombat("Força Superior", "Descripcio", "ATK", 2, 750),
            Objectes.ObjecteCombat("Força Colerica", "Descripcio", "ATK", 2.5, 2000),
            Objectes.ObjecteCombat("Resistencia", "Descripcio", "DEF", 1.3, 300),
            Objectes.ObjecteCombat("Mur de Roca", "Descripcio", "DEF", 2, 750),
            Objectes.ObjecteCombat("Mur d'acer", "Descripcio", "DEF", 2.5, 2000),
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
    Exits.KillExit("Beast Slayer", "Derrota ... de tipus bestia", [], 10, "Beast Slayer", "ExitBuff")
]


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
    for i in EntityTypes:
        if i.isPlayable == True:
            clases.append(i)
            nomclases.append(i.EntityName.lower())
    # nomclases =  list(map(lambda x: x.EntityName, clases))
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
            jugador = Entitat.Entity(nom, 5, True,clases[temp])
        temp += 1

    return jugador

# Cridem la funcio per crear el jugador.
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
    os.system("cls")
    while pos not in menu.keys():   # Generem la llista del menu
        for i in menu.keys():
            print(f"{i} -> {menu.get(i)}")
        try:
            pos = int(input("Digues quina acció vols fer: "))   # Demanem accio del menu
        except ValueError:
            print("Ha ocurregut un error...")
        os.system("cls")

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
        print("")
    elif menu.get(pos) == "Lluitar":
        Lluitar()
    elif menu.get(pos) == "Guardar":
        print("")
    elif menu.get(pos) == "Exits":
        MostrarExits()
    elif menu.get(pos) == "Mochila":
        jugador.ObjectesMochila()
    elif menu.get(pos) == "Info":
        print("Info (Ajuda sobre les opcions del menu...)")

def MostrarExits():
    print("Exits")
    for i in achievements:
        if i.Obtained == True:
            obtingut = "Obtingut"
        else:
            obtingut = "No Obtingut"
        print(f"{i.Name}, {obtingut}")
        if type(i) != type(Exits.KillExit):
            print(f"{i.Description} \n")
        else:
            print(f"{i.Description}, \n{i.Count} / {i.Quantity}")


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
        os.system("cls")
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
    for i in ubicacio.Connections:  # Mostrem ubicacions disponibles
        if i.Trobada == True:
            print(f"{count} -> {i.NameZone}")
            count += 1
            disponibles.append(i)
    pos = 0
    while pos not in range(1, count + 1): # Demanem a on anar.
        try:
            pos = int(input("Digues el numero de la zona a la que vols anar: "))
        except ValueError:
            print("Ha ocurregut un error...")
    ubicacio = disponibles[pos - 1]    # Canviem la zona i la retornem

def Explorar():
    global jugador, ubicacio
    print("Has començar a explorar...")
    prob = random.randrange(1, 100)
    if prob <= 20:  # Or
        TrobarOr(ubicacio.Or.keys())
    elif prob > 20 and prob <= 60:  # Res
        print("No has trobat res...")
    elif prob > 60 and prob <= 90:  # Lluitar
        Lluitar()
    elif prob > 90 and prob <= 100:
        print("Has trobat una ruta a la seguent zona...")
        for i in ubicacio.Connections:
            if i.Trobada == False:
                i.Trobada = True

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
        print(weight)
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
    if accio == 1:
        enemy = jugador.atacar(enemy)
    elif accio == 2:
        Fugir(enemy)
    elif accio == 3:
        used = jugador.ObjectesMochila(True)
        if used == False:
            turn = True
    elif accio == 4:
        os.system("cls")
        jugador.ShowStatus(True)
        turn = True
    
    return enemy, turn

def Fugir(enemy):
    global jugador
    print("Has intentat Fugir...")
    prob = jugador.fleeProb * (jugador.SPD / enemy.SPD)   # fleeProb = 75 de base
    # 75% base * resultat de velocitat del jugador entre la del enemic. (75 * (22 / 20) = 1.1) = 82.5)
    fugir = random.choices([True, False], cum_weights=[prob, 100 - prob])
    if fugir[0] == True:
        print("Has aconseguit escapar !!")
        input("\nPresiona per a continuar...")
        main()
    else:
        print("No has aconseguit escapar...")
    
    

def Lluitar():
    global jugador, ubicacio
    opcions = list(ubicacio.Enemies.keys())
    seleccio = random.choices(opcions, ubicacio.Enemies.values())
    enemy = Entitat.Entity("", random.randrange(ubicacio.LevelRange[0], ubicacio.LevelRange[1] + 1), False, seleccio[0])
    print(f"Ha aparegut un {enemy.nom}")

    turn = False
    if jugador.SPD >= enemy.SPD:
        turn = True

    while jugador.CurHP > 0 and enemy.CurHP > 0:
        os.system("cls")
        EntityState(jugador)
        EntityState(enemy)
        print("\n")
        if turn == True:
            enemy, turn = AccionsLluita(enemy)
        else:
            enemy.atacar(jugador)
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

def finalitzarCombat():
    global jugador
    jugador.DefinirTempStats()
        
def EntityState(entity):
    print(f"{entity.nom}, LV: {entity.Lv}, HP: {round(entity.CurHP, 2)} / {entity.MaxHP}")

def main():
    print("!! - Joc Interactiu - !!")
    while jugador.CurHP > 0:
        os.system("cls")
        AccioMenuPrincipal()
        input(f"\nPresiona per a continuar...")
        
    

if __name__ == "__main__":
    main()