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

    # Preparació Joc
        # Entitats
EntityTypes = [
        EntityType.EntityType("A",True,100,100,100,100,20, "Abecedari A"),
        EntityType.EntityType("B",True,100,100,100,100,20, "Abecedari B"),
        EntityType.EntityType("C",True,100,100,100,100,20, "Abecedari C"),
        EntityType.EntityType("D",True,100,100,100,100,20, "Abecedari D"),
        EntityType.EntityType("E",False,100,100,100,100,20, "Abecedari E"),
        EntityType.EntityType("F",False,100,100,100,100,20, "Abecedari F"),
        EntityType.EntityType("G",False,100,100,100,100,20, "Abecedari G"),
        EntityType.EntityType("H",False,100,100,100,100,20, "Abecedari H"),
        EntityType.EntityType("I",False,100,100,100,100,20, "Abecedari I"),
        EntityType.EntityType("J",False,100,100,100,100,20, "Abecedari J"),
        EntityType.EntityType("K",False,100,100,100,100,20, "Abecedari K"),
]
        # Zones
zones = [
        Zones.Zona("Dawn Village",
                   "Un poble que representa l'inici, es diu que és el poble on va neixer l'heroi de les llegendes...",
                   "Poble", {EntityTypes[6]: 20, EntityTypes[6]: 10, EntityTypes[6]: 10, EntityTypes[6]: 60},
                    (1, 5)),
        Zones.Zona("Bosc Obscur",
                   "La zona exterior del bosc obscur, d'on es diu que surjeren els monstres...",
                   "Bosc", {EntityTypes[6]: 20, EntityTypes[6]: 10, EntityTypes[6]: 10, EntityTypes[6]: 60}, 
                   (3, 7)),
        Zones.Zona("Profunditats del Bosc Obscur",
                   "Les profunditats del bosc obscur, una perillosa zona de la que és diu que qui hi entra no en surt...",
                   "Bosc", {EntityTypes[6]: 20, EntityTypes[6]: 10, EntityTypes[6]: 10, EntityTypes[6]: 60}, 
                   (5, 15)),
        Zones.Zona("Centre del Bosc Obscur",
                   "La zona central del bosc obscur, hi habiten monstres desconeguts, ningú ha tornat mai d'aquest lloc...",
                   "Bosc", {EntityTypes[6]: 20, EntityTypes[6]: 10, EntityTypes[6]: 10, EntityTypes[6]: 60}, 
                   (14, 30)),
        Zones.Zona("Muntanyes del Origen",
                   "Unes muntanyes només conegudes per llegendes, es diu que són el primer lloc en ser creat d'aquest món...",
                   "Muntanya", {EntityTypes[6]: 20, EntityTypes[6]: 10, EntityTypes[6]: 10, EntityTypes[6]: 60}, 
                   (30, 45)),
        Zones.Zona("Cavernes del Origen",
                   "Les cavernes de les muntanyes del origen, no és te coneixement de la existencia d'aquestes...",
                   "Cavernes", {EntityTypes[6]: 20, EntityTypes[6]: 10, EntityTypes[6]: 10, EntityTypes[6]: 60}, 
                   (43, 60))
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
            Objectes.ObjecteCombat("Pocio Inferior", "Descripcio", "Health", 10),
            Objectes.ObjecteCombat("Pocio", "Descripcio", "Health", 20),
            Objectes.ObjecteCombat("Pocio Intermitja", "Descripcio", "Health", 40),
            Objectes.ObjecteCombat("Pocio Avançada", "Descripcio", "Health", 60),
            Objectes.ObjecteCombat("Pocio Completa", "Descripcio", "Health", 100),
            Objectes.ObjecteCombat("Elixir", "Descripcio", "Health", 9999),
            Objectes.ObjecteCombat("Força", "Descripcio", "ATK", 1.3),
            Objectes.ObjecteCombat("Força Superior", "Descripcio", "ATK", 2),
            Objectes.ObjecteCombat("Força Colerica", "Descripcio", "ATK", 2.5),
            Objectes.ObjecteCombat("Resistencia", "Descripcio", "DEF", 1.3),
            Objectes.ObjecteCombat("Mur de Roca", "Descripcio", "DEF", 2),
            Objectes.ObjecteCombat("Mur d'acer", "Descripcio", "DEF", 2.5),
            Objectes.ObjecteCombat("Carrera", "Descripcio", "SPD", 1.3),
            Objectes.ObjecteCombat("Llampeg", "Descripcio", "SPD", 2),
            Objectes.ObjecteCombat("Raig", "Descripcio", "SPD", 2.5),
            
            # Objectes de Combat
            Objectes.ObjecteClau("Pedra Misteriosa", "???"),
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
    for i in EntityTypes:
        if i.isPlayable == True:
            clases.append(i)
            nomclases.append(i.EntityName)
    # nomclases =  list(map(lambda x: x.EntityName, clases))
    while clase not in nomclases:
        try:
            for i in clases:
                print(f"{i.EntityName}, {i.EntityDescription}.")
            clase = input("Digues una de les clases mostrades anteriorment: ")
            if clase not in nomclases:
                print(f"Has de dir una de les clases anteriors: {nomclases}")
        except ValueError:
            print("Ha ocurregut un error...")
    
    jugador = None
    temp = 0
    while jugador == None:
        if clases[temp].EntityName == clase:
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
        print("")
    elif menu.get(pos) == "Estat":
        jugador.ShowStatus()
    elif menu.get(pos) == "Misions":
        print("")
    elif menu.get(pos) == "Lluitar":
        Lluitar()
    elif menu.get(pos) == "Guardar":
        print("")
    elif menu.get(pos) == "Exits":
        print("")
    elif menu.get(pos) == "Mochila":
        jugador.ObjectesMochila()
    elif menu.get(pos) == "Info":
        print("Info (Ajuda sobre les opcions del menu...)")

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
    for i in ubicacio.Connections:  # Mostrem ubicacions disponibles
        print(f"{ubicacio.Connections.index(i) + 1} -> {i.NameZone}")
    pos = 0
    while pos not in range(1, len(ubicacio.Connections)+1): # Demanem a on anar.
        try:
            pos = int(input("Digues el numero de la zona a la que vols anar: "))
        except ValueError:
            print("Ha courregut un error...")
    ubicacio = ubicacio.Connections[pos - 1]    # Canviem la zona i la retornem

def Explorar():
    global jugador, ubicacio
    print("Has començar a explorar...")
    prob = random.randrange(1, 100)
    if prob <= 20:  # Or
        found = random.randrange(1, 7)
        print(f"Has trobat {found} monedes de bronze !")
        jugador.gold += found * 10  # Monedes de bronze = 10 gold
    elif prob > 20 and prob <= 60:  # Res
        print("No has trobat res...")
    elif prob > 60 and prob <= 90:  # Lluitar
        Lluitar()
    elif prob > 90 and prob <= 100:
        print("Has trobat una ruta a la seguent zona...")
    
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
        jugador.ShowStatus()
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
    print(f"{entity.nom}, LV: {entity.Lv}, HP: {entity.CurHP} / {entity.MaxHP}")

def main():
    print("!! - Joc Interactiu - !!")
    while jugador.CurHP > 0:
        os.system("cls")
        AccioMenuPrincipal()
        input(f"\nPresiona per a continuar...")
        
    

if __name__ == "__main__":
    main()