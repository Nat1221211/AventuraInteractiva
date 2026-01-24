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

        # Efectes d'estat (Cremat, Congelat, Paralitzat, Sangrant, etc.)
Effects = [
    Characteristics.Effects("Cremada","Estar cremat redueix el atac i la defensa i causa dany cada poc temps...",
                            True, False, 0, 5, ("Stat", (["ATK", "DEF"], 0.25))),
    Characteristics.Effects("Sangrat","Tens una ferida greu que fa perdre vida constantment...",
                            True, False, 0, 8, ("None", "")),
    Characteristics.Effects("Congelacio","Estas congelat durant una certa quantitat de temps...",
                            False, True, 3, 0, ("None", "")),
    Characteristics.Effects("Sangrat Greu","Tens una ferida greu que fa perdre vida constantment...",
                            True, False, 0, 16, ("Stat", (["ATK", "DEF", "SPD"], 0.15))),
    Characteristics.Effects("Terror","",
                            False, False, 0, 0, ("Stat", (["ATK", "DEF", "INT", "SPD"], 0.25))),
]
        # Moves
movements = [   
    # Per a efectes d'estat dins la tupla un True, Seguit d'una altre tupla amb una llista amb les estadistiques, 
    # i en la segona part de la tupla la quantitat d'augment o reducció, l'augment ha de ser amb base 1 o superior, 
    # la reducció ha de ser de 0  a 0.9, es a dir iferior a 1.

    Characteristics.Moves("Bola de Foc", "Bola de foc formada amb magia",
                          40, 100, True, 5, [("Effect", (Effects[0], 30))], False),
    Characteristics.Moves("Fletxa Perforant", "Fletxa altament perforant gracies a poder magic",
                          60, 100, False, 5, [("Effect", (Effects[1], 60))], False),
    Characteristics.Moves("Assalt Llampeg", "Impuls de velocitat i atacs repetits",
                          30, 100, False, 5, [("Stat", (["SPD"], 1.1))], False),
    Characteristics.Moves("Tall Potent", "Tall altament poderos, fortaleix el cos amb magia.",
                          50, 100, False, 5, [("Stat", (["ATK"], 1.1))], False),
    Characteristics.Moves("Aixafar", "Potent Mossegada",
                          40, 90, False, 0, [("Effect", (Effects[1], 10))], False),
    Characteristics.Moves("Debuff", "Reduccio d'estadistiques alta",
                          20, 95, True, 10, [("Stat", (["ATK", "DEF", "SPD", "INT"], 0.2))], True),
    
    # Atacs sense consum per a si no queda Mana i no podem realitzar-ne cap altre...
    Characteristics.Moves("Tall", "Un tall d'arma blanca normal",
                          30, 100, False, 0, [("None", "")], False),
    Characteristics.Moves("Cop de Basto", "Un cop de basto normal",
                          20, 100, False, 0, [("None", "")], False),
    Characteristics.Moves("Fletxa", "És dispara una fletxa normal",
                          30, 100, False, 0, [("None", "")], False),
    
    # Continuem amb atacs diversos
        # Mag
    Characteristics.Moves("Fletxa de flames", "",
                          60, 100, True, 20, [("Effect", (Effects[0], 80))]),
    Characteristics.Moves("Increment", "",
                          20, 100, True, 10, [("Stat", (["ATK", "DEF", "SPD", "INT"], 1.3))], False),
    Characteristics.Moves("Fulla de Vent", "",
                          60, 100, True, 20, [("Effect", (Effects[1], 80))]),
        
        # Guerrer
    Characteristics.Moves("Tall Llampeg", "",
                          70, 100, False, 10, [("Effect", (Effects[1], 80))]),
    Characteristics.Moves("Crit de Guerra", "",
                          30, 100, False, 10, [("Stat", (["ATK", "DEF", "SPD"], 1.25)), ("Effect", (Effects[4] , 95))], True),
    Characteristics.Moves("Bloqueig", "Bloqueja un atac enemic dirijit a un company",
                          0, 100, False, 3, [("Stat", (["DEF"], 1.3))], False, False, True, 75),
        
        # Arquer
    Characteristics.Moves("Santuari", "Crea un santuari durant uns instants, recupera molta salut als companys...",
                          120, 100, True, 20,[("Stat", (["ATK", "DEF", "INT", "SPD"], 2))], True, True),
    Characteristics.Moves("Cura", "Cura una petita quantitat de vida a un company",
                          60, 100, True, 4, [("None", "")], False, True),
        
        # Lladre
    Characteristics.Moves("", "",
                          30, 100, True, 10, [("None", "")]),
    Characteristics.Moves("", "",
                          30, 100, True, 10, [("None", "")]),
    
    Characteristics.Moves("Revestiment de Flames", "Utilitzes flames per incrementar les teves capacitats i envoltar la teva arma...", 60, 100, True, 15, [("Stat", (["ATK", "SPD"],1.30)), ("Effect", (Effects[0], 80))])
]
        # Skills
skills = [

]

        # Entitats
entityTypes = [
    # Cal tenir en compte les estadistiques, els grups als que pertanyen, i el diccionari de moviments i nivell.

        EntityType.EntityType("Guerrer", True, 160, 100, 140, 40, 130, 80, 50, ["Human"], 
                              "Alta salut, resistencia i força pero lenta.",
                              {movements[6]: 1, movements[3]: 3, movements[12]: 3, movements[13]: 3, movements[14]: 4}
                              ),
      
        EntityType.EntityType("Mag", True, 80, 200, 60, 180, 100, 100, 50, ["Human"], 
                              "Alt atac, però poca salut, resistencia i velocitat equilibrades.",
                              {movements[7]: 1, movements[0]: 3, movements[5]: 5, movements[15]: 5, movements[16]: 2}),
       
        EntityType.EntityType("Arquer", True, 120, 140, 140, 100, 140, 140, 50, ["Human"],
                              "Resistencia, Atac i Velocitat equilibrats.",
                              {movements[8]: 1, movements[1]: 3}),
       
        EntityType.EntityType("Lladre", True, 120, 120, 130, 100, 120, 160, 50, ["Human"], 
                              "Alta velocitat, salut i resistencia equilibrades, atac mitja.",
                              {movements[6]: 1, movements[2]: 3}),
       
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
                              "Un arbre malevol, en algunes ocasions no en són.",
                              {movements[4]: 3}),
        
        EntityType.EntityType("Golem", False, 250, 100, 160, 80, 200, 60, 500, ["Artificial"], 
                              "Monstre de Roca, es una forma de vida artificial feta de pedra.",
                              {movements[3]: 3}),
        
        EntityType.EntityType("Mag de Flames", False, 60, 250, 60, 220, 50, 50, 40, ["Human"], 
                              "Molt Atac altres estadistiques baixen, augmentara molt l'atac i el mana pero" \
                              "\nles altres estadistiques no canviaran massa...",
                              {movements[9]: 25}),
        EntityType.EntityType("Expert en Armes", False, 160, 120, 180, 100, 130, 100, 50, ["Human"], "Un expert en diverses armes cos a cos, és molt capaç, és una forma millorada del Guerrer...", {}),
        
        EntityType.EntityType("Caballer", False, 200, 60, 100, 40, 260, 60, 50, ["Human"], "Un expert especialitzat en la resistencia, tot i això te una capacitat ofensiva considerable.", {}),

        EntityType.EntityType("Aventurer", True, 140, 120, 140, 140, 115, 115, 50, ["Human"], "No especialitzat en cap camp en excés, no destaca en cap camp però tampoc és dolent en cap d'ells...", {movements[6]: 1, movements[3]: 3, movements[19]: 3})
]

# Afegint Paths (Posibles SUbclasses)
entityTypes[1].AddPaths({entityTypes[11]: [[("Lv", 30), ("Stat", [("Mana", 120)])], False]})



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
    # Diccionari per a les entitats en la zona, essent la entitat i la probabilitat de que apareixi.
    # Altre diccionari per a les monedes, essent la moneda, una tupla amb els dos valors limits (min, max), i 
    # la probabilitat de que surtin al explorar la zona.  
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
                   (5, 12), {"Bronze": [(5, 15), 100]}),
        Zones.Zona("Centre del Bosc Obscur",
                   "La zona central del bosc obscur, hi habiten monstres desconeguts, ningú ha tornat mai d'aquest lloc...",
                   "Bosc", {entityTypes[6]: 30, entityTypes[8]: 30, entityTypes[9]: 40}, 
                   (10, 18), {"Bronze": [(20, 50), 60], "Plata": [(3, 10), 40]}),
        Zones.Zona("Muntanyes del Origen",
                   "Unes muntanyes només conegudes per llegendes, es diu que són el primer lloc en ser creat d'aquest món...",
                   "Muntanya", {entityTypes[7]: 50, entityTypes[8]: 20, entityTypes[9]: 20, entityTypes[10]: 10}, 
                   (15, 25), {"Plata": [(40, 100), 70], "Or": [(1, 10), 30]}),
        Zones.Zona("Cavernes del Origen",
                   "Les cavernes de les muntanyes del origen, no és te coneixement de la existencia d'aquestes...",
                   "Cavernes", {entityTypes[6]: 40, entityTypes[7]: 30, entityTypes[10]: 30}, 
                   (30, 45), {"Plata": [(40, 100), 70], "Or": [(1, 10), 20], "Or Platejat": [(1, 1), 10]})
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
    # En els objectes cal tenir en compte la estadistica en la que actuen si son de combat, en forma de llista cada stat.
            # Objectes de Combat
            Objectes.ObjecteCombat("Pocio Inferior", "Cura 10 punts de vida", ["Health"], 10, 100, True),
            Objectes.ObjecteCombat("Pocio", "Descripcio", ["Health"], 20, 300, True),
            Objectes.ObjecteCombat("Pocio Intermitja", "Descripcio", ["Health"], 40, 750, True),
            Objectes.ObjecteCombat("Pocio Avançada", "Descripcio", ["Health"], 60, 2000, True),
            Objectes.ObjecteCombat("Pocio Completa", "Descripcio", ["Health"], 100, 4000, True),
            Objectes.ObjecteCombat("Elixir", "Descripcio", ["Health", "Mana"], 9999, 30000, True),
            Objectes.ObjecteCombat("Millora", "Descripcio", ["ATK"], 1.3, 300),
            Objectes.ObjecteCombat("Millora Superior", "Descripcio", ["ATK"], 2, 750),
            Objectes.ObjecteCombat("Millora Divina", "Descripcio", ["ATK"], 2.5, 2000),
            Objectes.ObjecteCombat("Barrera", "Descripcio", ["DEF"], 1.3, 300),
            Objectes.ObjecteCombat("Barrera Pentagonal", "Descripcio", ["DEF"], 2, 750),
            Objectes.ObjecteCombat("Barrera Octagonal", "Descripcio", ["DEF"], 2.5, 2000),
            Objectes.ObjecteCombat("Carrera", "Descripcio", ["SPD"], 1.3, 300),
            Objectes.ObjecteCombat("Llampeg", "Descripcio", ["SPD"], 2, 750),
            Objectes.ObjecteCombat("Raig", "Descripcio", ["SPD"], 2.5, 2000),
            
            # Objectes Clau
            Objectes.ObjecteClau("Pedra Misteriosa", "???"),
            Objectes.ObjecteClau("Tronc extrany", "Tronc d'un arbre extrany"),

            # Mes objectes de Combat
            Objectes.ObjecteCombat("Pocio de Mana Inferior", "Regenera 10 punts de Mana", ["Mana"], 10, 100, True),
            Objectes.ObjecteCombat("Pocio de Mana", "Descripcio", ["Mana"], 20, 300, True),
            Objectes.ObjecteCombat("Pocio  de Mana Intermitja", "Descripcio", ["Mana"], 40, 750, True),
            Objectes.ObjecteCombat("Pocio de Mana Avançada", "Descripcio", ["Mana"], 60, 2000, True),
            Objectes.ObjecteCombat("Pocio de Mana Completa", "Descripcio", ["Mana"], 100, 4000, True),
            Objectes.ObjecteCombat("Millora Magica", "Descripcio", ["INT"], 1.3, 300),
            Objectes.ObjecteCombat("Alta Millora Magica", "Descripcio", ["INT"], 2, 750),
            Objectes.ObjecteCombat("Super Millora Magica", "Descripcio", ["INT"], 2.5, 2000),
            ]

# Afegir Objectes per Trobar explorant cada zona
zones[1].AfegirObjectePerTrobar([
    [objectes[16], [30, 2]],
    [objectes[1], [40, 3]],
    [objectes[17], [30, 3]],
    ])




# Botiga
botiga = [objectes[0],
          objectes[6],
          objectes[9],
          objectes[12],
          objectes[16],
          objectes[21],
          ]

titles = [
    # En els titols cal entendre el grup sobre el que actuen, i l'increment d'estadistiques contra aquell grup.

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
    # Cal tenir en compte El Requisit que són els 3 i 4 apartats, essent tipus i quantitat.
    # També les recompenses, essent quantitat i a que afecten en cas dels statusExit.

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


    # En els killexit son els grups que s'ha de derrotar i la quantitat, així com el titul recibit en cas de ser titul la
    # recompensa.

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
                         [("XP", 3000), ("Gold", 10000), (objectes[15], 1)], 1, [entityTypes[10]], [("Lv", 5)], zones[3], False,
                         Entitat.Entity("El Golem de Roca", 40, False, entityTypes[10])),

    Missions.KillMission("Mostra de Confiança", 
                         "Troba i elimina al Llop lider, diuen que s'ha vist recentment per el Bosc Obscur", 
                         [("XP", 120), ("Gold", 1000), (objectes[1], 1)], 1, [entityTypes[4]], [("Lv", 5)], zones[1], False,
                         Entitat.Entity("Llop Lider", 9, False, entityTypes[4])),
]

# Afegir missions amb append, ja que si el requisit es una altre missio aquella ha d'estar ja definida.

missions.append(
    Missions.KillMission("Mostra de Confiança II", 
    "Elimina les restes de la manada de Llops en el bosc obscur.", 
    [("XP", 300), ("Gold", 2000), (objectes[1], 2)], 10, [entityTypes[4]], 
    [("Lv", 5), missions[1]], zones[1], False),
    )

missions.append(
    Missions.KillMission("Eliminant Sombres", 
    "Elimina 15 sombres del bosc obscur.", 
    [("XP", 500), ("Gold", 3000), (objectes[1], 5)], 15, [entityTypes[6]], 
    [("Lv", 10), missions[2]], zones[1], False),
    )

missions.append(
    Missions.FindMission("Troba a en Jack", 
    "Un nen del pobla s'ha perdut, és diu Jack, creuen que s'ha endinsat massa en el bosc obscur...",
    [("XP", 500), ("Gold", 2000)], "Jack", 
    [("Lv", 5)], zones[2])
)



def CrearJugador():
    nom = ""
    while nom == "":
        try:
            nom = input("Digues el nom del personatge: ")
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
    
    playableentity = None
    temp = 0
    while playableentity == None:
        if clases[temp].EntityName.lower() == clase:
            playableentity = Entitat.Entity(nom, 5, True, clases[temp])
        temp += 1

    return playableentity

# Cridem la funcio per crear el jugador, la variable ubicacio, i la variable de diccionari amb els grups i les seves entitats
jugador = CrearJugador()
jugador.gold += 2000
ubicacio = zones[0]
team = []

team.append(jugador)

# Afegim algun objecte al jugador de base
team[0].AfegirObjecte(objectes[0], 2)
team[0].AfegirObjecte(objectes[6], 2)

def AccioMenuPrincipal():
    global team, ubicacio
    
    pos = 0

    # Seleccionem el menu
    if ubicacio.ZoneType == "Poble":
        menu = {1: "Mapa", 2: "Motxila", 3: "Hostal", 4: "Botiga", 5: "Estat", 6: "Missions", 7: "Éxits", 8: "Gremi", 9: "Guardar"}
    elif ubicacio.ZoneType != "Poble":
        menu = {1: "Mapa", 2: "Motxila", 3: "Explorar", 4: "Lluitar", 5: "Estat", 6: "Missions", 7: "Éxits", 8: "Guardar"}

    print(f"Vostè es troba a {ubicacio.NameZone}")
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
    elif menu.get(pos) == "Hostal":
        Posada()
    elif menu.get(pos) == "Botiga":
        Botiga()
    elif menu.get(pos) == "Estat":
        VeureEstatus()
    elif menu.get(pos) == "Missions":
        MenuMisions()
    elif menu.get(pos) == "Lluitar":
        GenerarEnemic()
    elif menu.get(pos) == "Guardar":
        print("")
    elif menu.get(pos) == "Éxits":
        MostrarExits()
    elif menu.get(pos) == "Motxila":
        team[0].ObjectesMochila()
    elif menu.get(pos) == "Gremi":
        Gremi()

contractatsAnteriorment = []
def Gremi():
    res = 0
    while res not in [1, 2, 3]:
        ClearScreen()
        print("- Gremi d'Aventurers -")
        print("1 -> Descontractar Aventurer")
        print("2 -> Contractar Aventurer")
        print(f"3 -> Sortir")
        res = int(input("Digues una de les opcions: "))
        if res not in [1, 2, 3]:
            print("Has de dir un dels numeros corresponents...")
    if res in [1, 2, 3]:
        ClearScreen()
        if res == 3:
            print("Has sortit del gremi d'aventurers")
        elif res == 1:
            if len(team) > 1:
                print(" - Separem els nostres camins - ")
                count = 1
                for i in range(len(team)):
                    if team[i] != jugador:
                        print(f"{count} -> {team[i].nom}, Lv: {team[i].Lv}")
                        count += 1
                print(f"{count} -> Sortir")
                try:
                    sel = int(input("Digues amb qui vols separar camins: "))
                    if sel not in range(len(team)):
                        print("Has de dir un dels personatges seleccionables...")
                    contractatsAnteriorment.append(team[sel])
                    print(f"Has decidit separar camins amb {team[sel].nom}...")
                    team.remove(team[sel])
                except ValueError:
                    print("Ha ocurrgut un error...")
            else:
                print("No tens cap company del que separarte...")
        elif res == 2:
            res2 = 0
            while res2 not in [1, 2, 3]:
                ClearScreen()
                print("- Contractació - Gremi d'Aventurers -")
                print("1 -> Nou Aventurer")
                print("2 -> Antic Company")
                print(f"3 -> Sortir")
                res2 = int(input("Digues una de les opcions: "))
                if res2 not in [1, 2, 3]:
                    print("Has de dir un dels numeros corresponents...")
            if res2 in [1, 2, 3]:
                ClearScreen()
                if res2 == 3:
                    print("Has sortit del menu de contractació...")
                elif res2 == 1:
                    if len(team) < 3:
                        cost = ((len(contractatsAnteriorment)) + (len(team))) * 1000
                        if team[0].gold >= cost:
                            crear = ""
                            while crear not in ["s", "n"]:
                                ClearScreen()
                                print(f"Contractar un aventurer costara {cost} gold...")
                                crear = input(f"Contractaras a un nou aventurer tot i això: S / N\n").lower()
                                if crear not in ["s", "n"]:
                                    print("Has de dir una de les opcions...")
                            if crear == "s":
                                aventurer = CrearJugador()
                                team.append(aventurer)
                                team[0].gold -= cost
                            else:
                                print("Has sortit del menu de contractació...")
                        else:
                            print(f"No tens suficient gold per a contractar a un aventurer...")
                            print(f"Costa {cost} gold...")
                    else:
                        print("Tens massa persones al equip...")
                    res = 0
                elif res2 == 2:
                    if len(contractatsAnteriorment) > 0:
                        if len(team) < 3: 
                            sel = -1
                            while sel not in range(len(contractatsAnteriorment) + 1):
                                ClearScreen()
                                count = 1
                                for i in range(len(contractatsAnteriorment)):
                                    print(f"{count} -> {contractatsAnteriorment[i].nom}, Lv: {contractatsAnteriorment[i].Lv}")
                                    print(f"Classe: {contractatsAnteriorment[i].base.EntityName}")
                                    if contractatsAnteriorment[i].subclass != None:
                                        print(f"Segona Classe: {contractatsAnteriorment[i].subclass}")
                                    print()
                                    count += 1
                                print(f"{count} -> Sortir")
                                try:
                                    sel = int(input("Digues a qui vols reclutar de nou: "))
                                except ValueError:
                                    print("Ha ocurregut un error...")
                            if sel not in range(len(contractatsAnteriorment) + 1):
                                print("Has de dir un dels numeros...")
                            else:
                                if sel == count:
                                    print("Has sortit del menu de contractació...")
                                else:
                                    aventurer = contractatsAnteriorment[sel - 1]
                                    team.append(aventurer)
                                    contractatsAnteriorment.remove(aventurer)
                                    sel = 1
                                    print(f"Has començat de nou un viatge amb {aventurer.nom}...")
                        else:
                            print("Tens massa persones al equip...")
                    else:
                        print("No has separat camins amb ningu...")
                    res = 0
    input("\nPresiona per a continuar...")


def VeureEstatus(combat = False):
    res = 0
    while res not in range(1, len(team) + 2):
        ClearScreen()
        print("- De Qui vols veure les estadistiques -")
        count = 1
        for i in team:
            print(f"{count} -> {i.nom}")
            count += 1
        print(f"{count} -> Sortir")
        res = int(input("Digues de qui vols veure l'estat: "))
        if res not in range(1, count + 1):
            print("Has de dir un dels numeros corresponents...")
    if res in range(1, count):
        ClearScreen()
        if combat == False:
            team[res - 1].ShowStatus()
        else:
            team[res - 1].ShowStatus(True)
    else:
        input("Has sortit del menu d'estatus...")

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
                                reclamar[aceptar - 1].Aceptar(team[0])
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
                                reclamar[aceptar - 1].ClaimedRewards(team[0])
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
        i.RequisitesCompleted(team[0])
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
            i.Completed(team[0])
            team[0].AcquiredAchievements.append(i)


def PrepararBotiga(): # Afegir objectes segons nivell
    global team
    if team[0].Lv > 10:
        if [objectes[1], objectes[7], objectes[10], objectes[13]] not in botiga:
            botiga.append(objectes[1])
            botiga.append(objectes[7])
            botiga.append(objectes[10])
            botiga.append(objectes[13])
    if team[0].Lv > 20:
        if [objectes[2], objectes[8], objectes[11], objectes[14]] not in botiga:
            botiga.append(objectes[2])
            botiga.append(objectes[8])
            botiga.append(objectes[11])
            botiga.append(objectes[14])
    if team[0].Lv > 35:
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
        team[0].AfegirObjecte(botiga[res], qty)
        team[0].gold -= botiga[res].Preu * qty
        print(f"Has comprat {qty} {botiga[res].ObjectName} per {botiga[res].Preu * qty} gold !")

def Posada():
    global team
    res = ""
    while res not in ["S", "N"]:
        ClearScreen()
        try:
            res = input("\nVols descansar? Costa 100 gold (S / N): ").capitalize()
        except ValueError:
            print("Ha ocurregut un error...")
    if res == "S":
        if team[0].gold >= 100:
            print("Has descansat comodament, t'has recuperat completament...")
            team[0].gold -= 100
            for i in team:
                i.CurHP = i.MaxHP
                i.Mana = i.MaxMana
                i.afected = "None"
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
        ubicacio = disponibles[pos - 1]    # Canviem la zona i la retornem

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
    global team, ubicacio
    perTrobar = len(ubicacio.ObjectesPerTrobar)
    if perTrobar >= 1:
        choice = random.choices(["res", "objecte"], [10, 90])
        if choice == ["objecte"]:
            objectes = list(ubicacio.ObjectesPerTrobar.keys())
            probabilitat = [j[0] for j in ubicacio.ObjectesPerTrobar.values()]
            trobat = random.choices(objectes, probabilitat)
            ubicacio.ObjecteTrobat(trobat[0])
            print(f"Has trobat un/a {trobat[0].ObjectName}.")
            team[0].AfegirObjecte(trobat[0], 1)

    if perTrobar == 0 or choice == ["res"]:
        print("No has trobat res...")

def Explorar():
    global team, ubicacio
    print("Has començar a explorar...")
    prob = random.randrange(1, 100)
    choice = [""]
    if prob <= 20:  # Or
        TrobarOr(ubicacio.Or.keys())
    elif prob > 20 and prob <= 70:  # Res / Missions / Ocurrencies
        llista = []
        for i in missions:
            if i.Status == "Accepted" and i.Place == ubicacio:
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
        print("Has trobat una ruta a la seguent zona...")
        for i in ubicacio.Connections:
            if i.Trobada == False:
                i.Trobada = True
    if choice[0] != "missio" and prob < 70 or prob > 95:
        input("Presiona per a continuar...")

def TrobarOr(moneda):
    global ubicacio, team
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
            print(f"Has trobat {found} monedes de {moneda[0]}.")
        elif moneda[0] == "Plata":
            mult = 100
            print(f"Has trobat {found} monedes de {moneda[0]}.")
        elif moneda[0] == "Or":
            mult = 1000
            print(f"Has trobat {found} monedes d'{moneda[0]}.")
        elif moneda[0] == "Or Platejat":
            mult = 10000
            print(f"Has trobat {found} monedes d'{moneda[0]}.")
    team[0].gold += found * mult
    

def MenuAtacar(jug):
    global team
    res = 0
    while res not in range(1, len(jug.Moves) + 2):
        ClearScreen()
        count = 1
        for i in jug.Moves:
            print(f"{count} -> {i.Name}")
            print(f"Power: {i.Power}, Precision: {i.Precision}")
            print(f"Mana Cost: {i.Cost}\n")
            count += 1
        print(f"{count} -> Sortir")
        try:
            res = int(input("Digues quin atac vols fer: "))
            if res not in range(1, len(jug.Moves) + 2):
                print("Has de dir que vols fer...")
            if res == count:
                print("Has sortit")
            else:
                use = jug.Moves[res - 1]
                if use.Cost > jug.Mana:
                    print("No tens suficient Mana per a realitzar aquest atac...")
                    input("Presiona per a continuar...")
                    return None
                else:
                    return use
        except ValueError:
            print("Ha ocurregut un error...")
    
def AccionsLluita(jug, enemy, enemyderr):
    global team
    print(f"És el torn de {jug.nom}")
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
    ClearScreen()
    BattleScreenShow(team)
    BattleScreenShow(enemy)
    print("\n")
    if accio == 1:
        move = MenuAtacar(jug)
        target = None
        ClearScreen()
        BattleScreenShow(team)
        BattleScreenShow(enemy)
        print("\n")
        if move != None:
            if move.MultiTarget == False:
                if move.Healing == False and move.Protective == False:
                    target = TriarObjectius(enemy)
                else:
                    target = TriarObjectius(team)
            else:
                target = "All"
            if move.Healing == False and move.Protective == False:
                for i in range(len(enemy)):
                    if enemy[i] == target or target == "All":
                        enemy[i] = jug.atacar(enemy[i], move)
                        enemyderr = DescartarDerrotats(enemy[i], enemyderr)
            else:
                for i in range(len(team)):
                    if team[i] == target or target == "All":
                        team[i] = jug.MoveProtHeal(team[i], move)
            jug.Mana -= move.Cost
        if move == None or target == False:
            turn = True
    elif accio == 2:
        fugir = Fugir(enemy)
    elif accio == 3:
        used = team[0].ObjectesMochila(jug, True)
        if used == False:
            turn = True
    elif accio == 4:
        ClearScreen()
        VeureEstatus(True)
        turn = True
    
    return jug, enemy, turn, fugir, enemyderr

def TriarObjectius(list):
    global team
    res = 0
    while res not in range(1, len(list) + 2):
        BattleScreenShow(team)
        BattleScreenShow(list)
        ClearScreen()
        targetable = []
        for i in list:
            if i.CurHP > 0:
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
    global team
    print("Has intentat Fugir...")
    teamSPD = 0
    for i in team:
        teamSPD += i.SPD
    enemySPD = 0
    for j in enemy:
        enemySPD += j.SPD
    prob = team[0].fleeProb * (teamSPD / enemySPD)   # fleeProb = 75 de base
   
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
    qty = random.choices([1, 2, 3], [88, 10, 2])
    enemy = []
    for i in range(qty[0]):
        entitat = Entitat.Entity("", random.randrange(ubicacio.LevelRange[0], ubicacio.LevelRange[1] + 1), False, seleccio[0])
        enemy.append(entitat)
    Lluitar(enemy)

def ComprobarEfectEstat(entitat, derr):
    if entitat.afected != "None":
        if entitat.timer <= 0 and entitat.afected.Turns > 0:
            entitat.afected = "None"
        else:
            if entitat.afected.Damaging == True:
                damagepereffect = ((entitat.MaxHP / 100) * entitat.afected.Damage)
                entitat.CurHP -= damagepereffect
                print(f"{entitat.nom}, ha perdut {damagepereffect} HP degut a la {entitat.afected.Name}.")
                if entitat.CurHP <= 0:
                    print(f"{entitat.nom}, ha estat derrotat per {entitat.afected.Name}.")
                    derr += 1
            entitat.timer -= 1
    return entitat, derr

def PrioritatInicial(enemy):
    maxSpeedPlayer = max(team, key=lambda j: j.SPD)
    maxSpeedEnemies = max(enemy, key=lambda e: e.SPD)

    maxSpeed = max(maxSpeedPlayer.SPD, maxSpeedEnemies.SPD)

    for i in range(len(team)):
        if team[i].SPD == maxSpeed:
            team[i].Priority = 100
        else:
            team[i].Priority = (team[i].SPD / maxSpeed) * 100
    
    for j in range(len(enemy)):
        if enemy[j].SPD == maxSpeed:
            enemy[j].Priority = 100
        else:
            enemy[j].Priority = (enemy[j].SPD / maxSpeed) * 100

    return enemy

def IncrementarPrioritat(enemy):
    global team
    for i in range(len(team)):
        if team[i].CurHP > 0:
            team[i].Priority += team[i].SPD / 300  
    
    for j in range(len(enemy)):
        if enemy[j].CurHP > 0:
            enemy[j].Priority += enemy[j].SPD / 300
    return enemy

def BattleScreenShow(teamlist):
    teamlis = teamlist[:]

    for i in teamlis:
        if i.CurHP < 0:
            teamlis.remove(i)

    for i in teamlis:
        llarg = len(f"{i.nom}, LV: {i.Lv}")
        espaiat = ""
        for j in range(30 - llarg):
            espaiat += " "
        print(f"{i.nom}, LV: {i.Lv}", end=espaiat)
    
    print()
    for i in teamlis:
        llarg = len(f"HP: {round(i.CurHP, 2)} / {round(i.MaxHP, 2)}")
        espaiat = ""
        for j in range(30 - llarg):
            espaiat += " "
        print(f"HP: {round(i.CurHP, 2)} / {round(i.MaxHP, 2)}", end=espaiat)
    
    saltdeLinia = False
    for i in teamlis:
        if i.isPlayer == True:
            if saltdeLinia == False:
                print()
            llarg = len(f"Mana: {round(i.Mana, 2)} / {round(i.MaxMana, 2)}")
            espaiat = ""
            for j in range(30 - llarg):
                espaiat += " "
            print(f"Mana: {round(i.Mana, 2)} / {round(i.MaxMana, 2)}", end=espaiat)
            saltdeLinia = True

    saltdeLinia = False
    for i in range(len(teamlis)):
        if teamlis[i].afected != "None":
            if saltdeLinia == False:
                print()
            llarg = len(f"{teamlis[i].afected.Name}")
            espaiat = ""
            for j in range(30 - llarg):
                espaiat += " "
            print(f"{teamlis[i].afected.Name}", end=espaiat)
            saltdeLinia = True
        else:
            afectats = False
            for k in range(i, len(teamlis)):
                if teamlis[k].afected != "None":
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

def Lluitar(enemy):
    global team, ubicacio

    teamderr = 0
    enemyderr = 0

    enemy = PrioritatInicial(enemy)

    primer = False
    for i in team:
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
        
        for i in range(len(team)):
            if team[i].Priority >= 100 and len(enemy) >= 1 and team[i].CurHP > 0 and combat == True:
                ClearScreen()
                BattleScreenShow(team)
                BattleScreenShow(enemy)
                turn = False
                team[i], enemy, turn, fugir, enemyderr = AccionsLluita(team[i], enemy, enemyderr)
                if fugir[0] == False:
                    team[i], teamderr = ComprobarEfectEstat(team[i], teamderr)
                if turn == False:
                    team[i].Priority = 0
                input("\nPresiona per a continuar...")
                ClearScreen()
            if combat == True:
                combat = ComprobarFiCombat(combat, enemyderr, enemy, teamderr)

        # Turn enemic
        for j in range(len(enemy)):
            if enemy[j].Priority >= 100 and fugir[0] == False and len(team) >= 1 and enemy[j].CurHP > 0 and combat == True:
                ClearScreen()
                BattleScreenShow(team)
                BattleScreenShow(enemy)
                enemyMove = random.choice(enemy[j].Moves)
                targetable = []
                for e in team:
                    if e.CurHP > 0:
                        targetable.append(e)
                target = random.choice(range(len(targetable)))
                protegitPer = None
                if team[target].Protected == True:
                    if team[target].ProtectedBy[0] != None:
                        protegitPer = team[target].ProtectedBy[0]
                enemy[j].atacar(team[target], enemyMove)
                enemy[j].Priority = 0
                enemy[j], enemyderr = ComprobarEfectEstat(enemy[j], enemyderr)
                teamderr = DescartarDerrotats(team[target], teamderr)
                if protegitPer != None:
                    teamderr = DescartarDerrotats(protegitPer, teamderr)
                input("\nPresiona per a continuar...")
                ClearScreen()
            if combat == True:
                combat = ComprobarFiCombat(combat, enemyderr, enemy, teamderr)
        
        enemy = IncrementarPrioritat(enemy)
    finalitzarCombat(team)

def ComprobarFiCombat(combat, enemyderr, enemy, teamderr):
    if enemyderr == len(enemy) or teamderr == len(team):
            combat = False
            if len(enemy) == enemyderr:
                ClearScreen()
                print("Tos els enemics han estat derrotats !!")
                input("Presiona per a continuar")
    return combat

def DescartarDerrotats(p, derr):
    global team
    if p.CurHP <= 0:
        derr += 1
        if p.isPlayer == False:
            ClearScreen()
            alive = 0
            for i in range(len(team)): 
                if team[i].CurHP > 0:
                    team[i].LvlUp(p)
                    alive += 1
            if alive >= 1:
                team[0].gold += p.Lv * 10 # 10 monedes per cada nivell, representa que es ven el derrotat.
                print(f"Has guanyat {p.Lv * 10} gold.")
    return derr

def Comprovacions(enemy):
    for i in missions:
        if type(i) == Missions.KillMission:
            i.IncrementCount(enemy)
    for i in achievements:
        if i.Obtained == False:
            if type(i) == Exits.KillExit:
                i.IncrementCount(enemy)
            i.Completed(team[0])
            team[0].AcquiredAchievements.append(i)
    for i in team:
        i.ComprovarSubClassesDisponibles()

def finalitzarCombat(clon):
    global team
    for i in range(len(team)):
        team[i].DefinirTempStats()
        team[i].ResetBuffs()
        if team[i] in clon:
            for j in clon:
                if j == team[i]:
                    team[i].CurHP = j.CurHP
                    team[i].Mana = j.Mana
        else:
            team[i].CurHP = 0
            team[i].Mana = 0


        
def EntityState(entity):
    print(f"{entity.nom}, LV: {entity.Lv}")
    print(f"HP: {round(entity.CurHP, 2)} / {round(entity.MaxHP, 2)}", f", Mana: {round(entity.Mana, 2)} / {round(entity.MaxMana, 2)}" if entity.isPlayer == True else "")
    if entity.afected != "None":
        print(f"{entity.afected.Name}")
    print(f"Prioritat: {round(entity.Priority, 1)}")
    print("")


def main():
    print("!! - Joc Interactiu - !!")
    PostGame = False
    alive = 1
    while alive > 0:
        ClearScreen()
        AccioMenuPrincipal()
        alive = 0
        for i in team:
            if i.CurHP > 0:
                alive += 1
    if PostGame == False and objectes[15] in team[0].objectes.keys(): # Es pot eliminar aquest easter egg eliminant la funcio EasterEgg() i les 3 linies baix aquesta.
        PostGame = True   # Faria falta eliminar també el bool Easter dins el main()
        EasterEgg()

def EasterEgg():
    global team
    list = []
    for i in entityTypes:
        if i.isPlayable == False:
            list.append(i)
    res = random.choice(list)
    team[0] = Entitat.Entity(team[0].nom, 5, True, res, 999, {}, 0, True)
    print("L'efecte de la joia de la reencarnació s'ha activat...")
    input("\nPresiona per a continuar....")
    main()
        
    

if __name__ == "__main__":
    main()