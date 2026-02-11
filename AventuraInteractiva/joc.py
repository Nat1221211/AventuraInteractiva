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
from Classes import Missions
from Classes import Titles
from Classes import Zones
from Classes import Player
import PrepararCridar as Call


def ClearScreen():
    os.system("cls" if os.name == "nt" else "clear")


# # Afegint Paths (Posibles SUbclasses)
# entityTypes[1].AddPaths({entityTypes[11]: [[("Lv", 30), ("Stat", [("Mana", 120)])], False]})


# # Afegint monstres que poden apareixer conjuntament amb un altre.
# entityTypes[43].AddCompanions({entityTypes[42]: 99, entityTypes[43]: 1})    # Gran Cranc Abberrant
# entityTypes[38].AddCompanions({entityTypes[39]: 99, entityTypes[38]: 1})    # Gran Toruga Marina
# entityTypes[34].AddCompanions({entityTypes[33]: 100})   # Guiverns els 4 d'aball
# entityTypes[35].AddCompanions({entityTypes[33]: 100})
# entityTypes[36].AddCompanions({entityTypes[33]: 100})
# entityTypes[37].AddCompanions({entityTypes[33]: 100})
# entityTypes[53].AddCompanions({entityTypes[5]: 99, entityTypes[53]: 1}) # Gran Slime
# entityTypes[69].AddCompanions({entityTypes[68]: 100})   # Bagragratch
# entityTypes[75].AddCompanions({entityTypes[74]: 95, entityTypes[75]: 5})    # Granota
# entityTypes[76].AddCompanions({entityTypes[73]: 95, entityTypes[76]: 5})    # Vespa





# Creem la funcio per a generar els grups d'entitats algo aixi com els tipus.
entityGroups = {""}

        # Zones
zones = [
    # Diccionari per a les entitats en la zona, essent la entitat i la probabilitat de que apareixi.
    # Altre diccionari per a les monedes, essent la moneda, una tupla amb els dos valors limits (min, max), i 
    # la probabilitat de que surtin al explorar la zona.  
        Zones.Zona("Dawn Village",
                   "Un poble que representa l'inici, es diu que és el poble on va neixer l'heroi de les llegendes...",
                   "Poble", {}, [], (1, 5), {}, True),

        Zones.Zona("Bosc Obscur",
                   "La zona exterior del bosc obscur, d'on es diu que surjeren els monstres...",
                   "Bosc", {"Llop": 40, "Slime": 60},
                   # Llista amb probabilitat de cada un dels enemics per ordre d'apareixer en grups de fins a 3.
                   # Cada llista representa un enemic, i cada valor la prob per 1, 2, 3 enemics.
                   [[85, 13, 2], [95, 5]], (8, 14), {"Bronze": [(1, 7), 100]}, True),
        
        # Zones.Zona("Profunditats del Bosc Obscur",
        #            "Les profunditats del bosc obscur, una perillosa zona de la que és diu que qui hi entra no en surt...",
        #            "Bosc", {entityTypes[4]: 32, entityTypes[5]: 40, entityTypes[6]: 20, entityTypes[8]: 5, entityTypes[9]: 3}, 
        #            [[85, 13, 2], [95, 5], [99, 1], [99, 1], [99, 1]], (37, 45), {"Plata": [(15, 25), 100]}),
        
        # Zones.Zona("Centre del Bosc Obscur",
        #            "La zona central del bosc obscur, hi habiten monstres desconeguts, ningú ha tornat mai d'aquest lloc...",
        #            "Bosc", {entityTypes[6]: 30, entityTypes[8]: 30, entityTypes[9]: 40}, 
        #             [[85, 13, 2], [95, 5], [99, 1]], (43, 52), {"Or": [(1, 10), 40], "Plata": [(20, 40), 60]}),
        
        # Zones.Zona("Muntanyes del Origen",
        #            "Unes muntanyes només conegudes per llegendes, es diu que són el primer lloc en ser creat d'aquest món...",
        #            "Muntanya", {entityTypes[7]: 50, entityTypes[8]: 20, entityTypes[9]: 20, entityTypes[10]: 10}, 
        #            [[85, 13, 2], [95, 5], [99, 1], [99, 1]], (50, 55), {"Or": [(6, 15), 90], "Or Platejat": [(1, 3), 10]}),
        
        # Zones.Zona("Cavernes del Origen",
        #            "Les cavernes de les muntanyes del origen, no és te coneixement de la existencia d'aquestes...",
        #            "Cavernes", {entityTypes[6]: 40, entityTypes[7]: 30, entityTypes[10]: 30}, 
        #             [[85, 13, 2], [95, 5], [99, 1]], (52, 57), {"Or Platejat": [(2, 5), 100]}),
        # Pobles
        Zones.Zona("Silverhorn",
                   "Un poble envoltat de munatanyes, del que ningú coneix la existencia...",
                   "Poble", {}, [], (1, 5), {}, False),
        Zones.Zona("Faylight",
                   "Un poble enmig d'un gran bosc molt lluminos...",
                   "Poble", {}, [], (1, 5), {}, False),
        Zones.Zona("Lakestar",
                   "Un pobla al costat d'un gran llac, és diu que en el llac s'hi amaga una estrella...",
                   "Poble", {}, [], (1, 5), {}, False),
        Zones.Zona("Knightshire",
                   "La capital del regne, una gran terra de caballers...",
                   "Poble", {}, [], (1, 5), {}, False),
        
        # Camins i zones
            # Cami de Dawn Village a Knightshire
        Zones.Zona("Bosc del Sud",
                   "Un bosc ubicat al sud de Dawn Village, un bosc relativament segur...",
                   "Bosc", {"Llop": 8, "Slime": 30, "Conill Cornut": 47}, 
                   [[15, 83, 2], [93, 5, 2], [95, 5]], 
                   (3, 5), {"Bronze": [(1, 5), 100]}, True),

        # Zones.Zona("Rocklink",
        #            "Unes muntanyes que presenten el cami cap a la capital del regne...",
        #            "Muntanya", {entityTypes[4]: 40, entityTypes[33]: 20, entityTypes[7]: 30, 
        #                     entityTypes[0]: 3, entityTypes[2]: 3, entityTypes[3]: 4}, 
        #            [[20, 75, 5], [100], [95, 5], [50, 40], [50, 40], [50, 40]], 
        #            (5, 9), {"Bronze": [(10, 20), 90], "Plata": [(2, 5), 10]}, False),

        # Zones.Zona("Camps de Knightshire",
        #            "Els camps a les afores de knightshire, aquestes \"afores\" son bastant grans...",
        #            "Camps", {entityTypes[5]: 90, entityTypes[4]: 10, entityTypes[26]: 50}, 
        #            [[95, 5], [40, 55, 5], [95, 5]], (3, 5), {"Bronze": [(1, 5), 100]}, False),
            
            # Cami de Knightshire a Lakestar o Faylight (Pasant per Muntayes Estelars)
        
#         Zones.Zona("Bosc Estelar",
#                    "Un bosc que guia cap a les muntanyes estelars...",
#                    "Bosc", {entityTypes[26]: 50, entityTypes[32]: 50, entityTypes[28]: 50}, 
#                    [], 
#                    (8, 13), {"Bronze": [(12, 25), 70], "Plata": [(4, 9), 30]}, False),
        
#         Zones.Zona("Muntanyes Estelars",
#                    "Unes muntanyes de les que es diu que les estrelles guien a les persones que hi passen...",
#                    "Muntanya", {entityTypes[4]: 30, entityTypes[5]: 40, entityTypes[7]: 35, entityTypes[44]: 8, 
#                                 entityTypes[1]: 1, entityTypes[0]: 2, entityTypes[2]: 2, entityTypes[3]: 2}, 
#                    [[82, 15, 3],[92, 6, 2], [98,2], [100], [30, 50, 20], [30, 50, 20], [30, 50, 20], [30, 50, 20]], 
#                    (12, 17), {"Bronze": [(16, 25), 70], "Plata": [(7, 9), 30]}, False),
        
#         Zones.Zona("Cami de Roca",
#                    "Un cami rocos que guia cap a la platja de Lakestar.",
#                    "Muntanya i Platja", {entityTypes[4]: 50, entityTypes[46]: 20, entityTypes[7]: 18, 
#                                          entityTypes[1]: 3, entityTypes[0]: 4, entityTypes[2]: 3, entityTypes[3]: 3}, 
#                    [[82, 15, 3],[92, 6, 2], [98,2], [30, 50, 20], [30, 50, 20], [30, 50, 20], [30, 50, 20]], 
#                    (15, 17), {"Bronze": [(16, 25), 70], "Plata": [(7, 9), 30]}, False),
        
#         Zones.Zona("Platja de Lakestar",
#                    "La platja del Gran llac Lakestar...",
#                    "Platja", {entityTypes[46]: 32, entityTypes[38]: 2, entityTypes[39]: 30, entityTypes[40]: 15,
#                               entityTypes[42]: 20, entityTypes[43]: 1}, 
#                    [[95, 5], [100], [95, 5], [100], [95, 5], [100]], 
#                    (10, 15), {"Bronze": [(10, 20), 100]}, False)
 ]

# # Cami de Lakestar a Faylight o (Pendent)
# zones.append(
# Zones.Zona(
#     "Serra del Bosc de Llum",
#     "Una gran serra que bloqueja el pas cap el Gran Bosc de llum, si hi vols arribar, has de passar per aquestes...",
#     "Muntanya", {entityTypes[33]: 22, entityTypes[7]: 25, entityTypes[48]: 5, entityTypes[49]: 8,
#                  entityTypes[44]: 10, entityTypes[50]: 30}, 
#     [[90, 10], [95, 5], [100], [95, 5], [100], [40, 55, 5]],
#     (15, 20), {"Plata": [(10, 15), 100]}, False, (("Ubicacio", [zones[8]]))),
# )

            
# zones.append(
# Zones.Zona(
#     "Gran Bosc de Llum",
#     "Un Bosc on la llum no desapareix ni tant sols durant la nit, d'aqui el seu nou...",
#     "Bosc", {entityTypes[50]: 30, entityTypes[32]: 40, entityTypes[70]: 2, entityTypes[73]: 14, entityTypes[74]: 14}, 
#     [[30, 65, 5], [80, 20], [100], [90, 10], [90, 10]], 
#     (18, 23), {"Plata": [(10, 15), 100]}, False)
# )      

# zones.append(
# Zones.Zona(
#     "Bosc de les Fades",
#     "Un bosc que quasi ningu coneix, encara que esta dins d'un bosc molt conegut...",
#     "Bosc", {entityTypes[79]: 80, entityTypes[80]: 20}, [[100], [100]],
#     (21, 26), {"Plata": [(10, 15), 100]}, False))

# # Cami de Faylight a Silverhorn
# zones.append(
# Zones.Zona(
#     "Grans Muntanyes Blanques",
#     "Una gran serralada blanca, és diu que en aquestes muntanyes hi ha un poble llegendari...",
#     "Muntanya", {entityTypes[7]: 40, entityTypes[31]: 15, entityTypes[33]: 30, entityTypes[34]: 15, entityTypes[35]: 15,
#                 entityTypes[36]: 15, entityTypes[37]: 15, entityTypes[44]: 15, entityTypes[45]: 7, entityTypes[47]: 20, 
#                 entityTypes[48]: 20, entityTypes[51]: 20, entityTypes[52]: 20, entityTypes[68]: 7, entityTypes[69]: 7,
#                 entityTypes[46]: 20, entityTypes[27]: 1},
#                 [[90, 10], [100], [100], [100], [100], [100], [100], [95, 5], [100], [100], [95, 5], [88, 10, 2], [95, 5], [70, 25, 5], [100], [60, 35, 5], [100]], 
#     (24, 29), {"Plata": [(10, 15), 100]}, 
#     False, None, 20)
#     )
                
# zones.append(
# # Conectat a lakestar mitjançant el llac, necessita haber trobat silverhorn i cert objecte per trobar la zona...
# Zones.Zona( 
#     "Profunditats de Lakestar",
#     "Un cami subterrani que avança dins el Gran llac, normalment ningú en sabria la existencia...",
#     "Cavernes", {entityTypes[68]: 20, entityTypes[69]: 5, entityTypes[42]: 20, entityTypes[43]: 5, 
#                  entityTypes[39]: 20, entityTypes[38]: 5, entityTypes[74]: 20, entityTypes[75]: 5},
#     [[75, 25], [98, 2], [75, 25], [98, 2], [75, 25], [98, 2], [75, 25], [98, 2]], 
#     (30, 35), {"Plata": [(20, 25), 100]}, False,
#     (("Ubicacio", [zones[6]])), 25)
#     )

# zones.append(
# # Conectat a lakestar mitjançant el llac, necessita haber trobat silverhorn i cert objecte per trobar la zona...
# Zones.Zona( 
#     "Mon Subterrani",
#     "Un mon subterrani sota el Gran Llac, aquest lloc sembla donar sentit a la historia de la estrella...",
#     "Cavernes", {entityTypes[68]: 50, entityTypes[69]: 15, entityTypes[51]: 30, entityTypes[53]: 10,
#                  entityTypes[42]: 50, entityTypes[43]: 15, entityTypes[74]: 30, entityTypes[75]: 10, entityTypes[57]: 1},
#     [[40, 40, 20], [80, 20], [50, 40, 10], [60, 35, 5], [40, 40, 20], [60, 35, 5], [40, 40, 20], [80, 20], [100]],
#     (35, 40), {"Plata": [(30, 45), 100]}, False)
#     )

# zones.append(
# # Conectat a lakestar mitjançant el llac, necessita haber trobat silverhorn i cert objecte per trobar la zona...
# Zones.Zona( 
#     "Illa estelar",
#     "Es pot veure l'estrella en el crater d'aquesta illa..., rodejada per un munt de monstres marins.",
#     "Cavernes", {entityTypes[40]: 50, entityTypes[41]: 1, entityTypes[42]: 50, entityTypes[43]: 15,
#                  entityTypes[39]: 50, entityTypes[38]: 15, entityTypes[53]: 15},
#     [[40, 40, 20], [100], [50, 40, 10], [60, 35, 5], [40, 40, 20], [60, 35, 5], [60, 35, 5]],
#     (35, 40), {"Plata": [(35, 45), 100]}, False)
#     )



        # Connexions de cada zona
    # Pobles
zones[0].AddConnections([zones[1], zones[6]])  # Dawn Viallage
# zones[6].AddConnections([zones[1]])  # Silverhorn
# zones[7].AddConnections([zones[18], zones[20]]) # Faylight
# zones[8].AddConnections([zones[16]]) # Lakestar
# zones[9].AddConnections([zones[12]]) # Knightshire

#     # Salvatge
# zones[1].AddConnections([zones[0], zones[2]])   # Bosc Obscur
# zones[2].AddConnections([zones[1], zones[3]])   # Profunditats Bosc Obscur
# zones[3].AddConnections([zones[2], zones[4]])   # Centre Bosc Obscur
# zones[4].AddConnections([zones[3], zones[5]])   # Muntanyes Origen
# # zones[5].AddConnections([zones[4]]) # Cavernes del origen
zones[6].AddConnections([zones[0]]) # Bosc del SUd
# zones[11].AddConnections([zones[10], zones[12]])    # Rocklink
# zones[12].AddConnections([zones[11], zones[9], zones[13]])  # Camps de Knightshire
# zones[13].AddConnections([zones[12], zones[14]])    # Bosc Estelar
# zones[14].AddConnections([zones[13], zones[15], zones[17]]) # Muntanyes Estelars
# zones[15].AddConnections([zones[14], zones[16], zones[21]])    # Cami Rocos
# zones[16].AddConnections([zones[15], zones[8]]) # Platja de Lakestar
# zones[17].AddConnections([zones[14], zones[18]]) # Serra del Bosc de Llum
# zones[18].AddConnections([zones[17], zones[19]]) # Gran Bosc de Llum
# zones[19].AddConnections([zones[18], zones[7]]) # Bosc de Fades
# zones[20].AddConnections([zones[7], zones[6]]) # Grans Muntanyes Blanques
# zones[21].AddConnections([zones[15], zones[22]]) # Profunditats de Lakestar
# zones[22].AddConnections([zones[21], zones[23]]) # Mon Subterrani
# zones[23].AddConnections([zones[22]]) # Illa Estelar



# # Afegir Objectes per Trobar explorant cada zona
# zones[1].AfegirObjectePerTrobar([
#     [objectes[16], [30, 2]],
#     [objectes[1], [40, 3]],
#     [objectes[17], [30, 3]],
#     ])




# # Botiga
botiga = [Call.CallObject("Pocio Inferior"),
          Call.CallObject("Pocio"),
          Call.CallObject("Pocio Intermitja")
          ]



    # Exits (Achievements / Logros)
# achievements = [
#     # Cal tenir en compte El Requisit que són els 3 i 4 apartats, essent tipus i quantitat.
#     # També les recompenses, essent quantitat i a que afecten en cas dels statusExit.

#     # Exits d'estadistiques
#     Exits.StatusExit("Lv 10", "Arriba al nivell 10", "Lv", 10, 5, "AllStats"),
#     Exits.StatusExit("Lv 20", "Arriba al nivell 10", "Lv", 20, 5, "AllStats"),
#     Exits.StatusExit("Lv 30", "Arriba al nivell 10", "Lv", 30, 5, "AllStats"),
#     Exits.StatusExit("Lv 40", "Arriba al nivell 10", "Lv", 40, 5, "AllStats"),
#     Exits.StatusExit("Lv 50", "Arriba al nivell 10", "Lv", 50, 5, "AllStats"),
#     Exits.StatusExit("ATK 50", "Arriba a 50 ATK", "ATK", 50, 3, "ATK"),
#     Exits.StatusExit("ATK 100", "Arriba a 100 ATK", "ATK", 100, 3, "ATK"),
#     Exits.StatusExit("ATK 150", "Arriba a 150 ATK", "ATK", 150, 3, "ATK"),
#     Exits.StatusExit("ATK 200", "Arriba a 200 ATK", "ATK", 200, 3, "ATK"),
#     Exits.StatusExit("DEF 50", "Arriba a 50 ATK", "DEF", 50, 3, "DEF"),
#     Exits.StatusExit("DEF 100", "Arriba a 100 ATK", "DEF", 100, 3, "DEF"),
#     Exits.StatusExit("DEF 150", "Arriba a 150 ATK", "DEF", 150, 3, "DEF"),
#     Exits.StatusExit("DEF 200", "Arriba a 200 ATK", "DEF", 200, 3, "DEF"),
#     Exits.StatusExit("SPD 50", "Arriba a 50 ATK", "SPD", 50, 3, "SPD"),
#     Exits.StatusExit("SPD 100", "Arriba a 100 ATK", "SPD", 100, 3, "SPD"),
#     Exits.StatusExit("SPD 150", "Arriba a 150 ATK", "SPD", 150, 3, "SPD"),
#     Exits.StatusExit("SPD 200", "Arriba a 200 ATK", "SPD", 200, 3, "SPD"),
#     Exits.StatusExit("HP 50", "Arriba a 50 HP", "HP", 50, 5, "HP"),
#     Exits.StatusExit("HP 100", "Arriba a 100 HP", "HP", 100, 5, "HP"),
#     Exits.StatusExit("HP 150", "Arriba a 150 HP", "HP", 150, 5, "HP"),
#     Exits.StatusExit("HP 200", "Arriba a 200 HP", "HP", 200, 5, "HP"),
# ]
    # En els killexit son els grups que s'ha de derrotar i la quantitat, així com el titul recibit en cas de ser titul la
    # recompensa.
missions = [
    # Missions.KillMission("Eliminant el Perill", 
    #                      "Un perillos golem que amenaça el poble, diuen que s'ha vist recentment per el Bosc Obscur.", 
    #                      "Principal",
    #                      [("XP", 3000), ("Gold", 10000), (objectes[15], 1)], 1, [entityTypes[10]], [("Lv", 35)], zones[3], False,
    #                      Entitat.Entity("El Golem de Roca", 40, False, entityTypes[10])),
]

# Afegir missions amb append, ja que si el requisit es una altre missio aquella ha d'estar ja definida.

#     # Missions Principals
# missions.append(
#     Missions.PlaceMission(
#         "La Primera Parada", 
#         "Com a bon aventurer, vols començar el teu viatge, i la primera parada d'aquest és la ciutat dels caballers, Knightshire.", 
#         "Principal",
#         [("XP", 500), ("Gold", 3000), (objectes[2], 5)], zones[9], [("Lv", 5)]),
# )

# missions.append(
#     Missions.KillMission(
#         "Primera Petició", 
#         "A Knightshire t'han demanat, en el gremi d'aventurers, que derrotis 5 conills cornuts, en els camps de Knioghtshire.", 
#         "Principal", [("XP", 750), ("Gold", 3000), (objectes[2], 4)], 5, [entityTypes[26]], 
#         [("Lv", 7), missions[0]], zones[12], True),
# )

# missions.append(
#     Missions.PlaceMission(
#         "Dirigeixte a Lakestar", 
#         "Ves a la segona parada del teu viatge, Lakestar.", 
#         "Principal",
#         [("XP", 700), ("Gold", 3000), (objectes[2], 5)], zones[8], [("Lv", 9), missions[1]]),
# )

# missions.append(
#     Missions.KillMission(
#         "El Gran Cranc", 
#         "A Lakestar decideixes començar una peticio del gremi d'aventurers, consisteix en eliminar a cert Cranc Aberrant... Se'l ha vist per la platja de Lakestar.", 
#         "Principal", [("XP", 1250), ("Gold", 3500)], 1, [entityTypes[43]], 
#         [("Lv", 12), missions[2]], zones[16], False, 
#         Entitat.Entity("Cranc Aberrant Extrany", 12, False, entityTypes[43])),
# )

# missions.append(
#     Missions.KillMission(
#         "Eliminació de Bandits", 
#         "A Lakestar decideixes començar una altre peticio del gremi d'aventurers, eliminar els bandits de les muntanyes estelars.", 
#         "Principal", [("XP", 1000), ("Gold", 3500)], 4, [entityTypes[0], entityTypes[1], entityTypes[2], entityTypes[3]], 
#         [("Lv", 14), missions[3]], zones[14], True),
# )

# missions.append(
#     Missions.PlaceMission(
#         "Un nou destí", 
#         "Ves al Gran Bosc Lluminos, es diu que hi ha un antic poble amagat en aquest...", 
#         "Principal",
#         [("XP", 2000), ("Gold", 5000)], zones[7], [("Lv", 17), missions[4]]),
# )

# missions.append(
#     Missions.KillMission(
#         "La Gran Aranya", 
#         "A Faylight et demanen que elimins una perillosa aranya que habita en el Gran Bosc Lluminos...", 
#         "Principal", [("XP", 2500), ("Gold", 5000)], 1, [entityTypes[70]], 
#         [("Lv", 20), missions[5]], zones[18], False, 
#         Entitat.Entity("Gran Aranya", 22, False, entityTypes[70])),
# )

# missions.append(
#     Missions.PlaceMission(
#         "El poble platejat", 
#         "Despres d'agrairte l'ajuda, en Faylight, has escoltat parlar d'un poble amagat en les muntanyes, un poble d'enans...", 
#         "Principal",
#         [("XP", 6000), ("Gold", 10000)], zones[6], [("Lv", 24), missions[6]]),
# )

# missions.append(
#     Missions.KillMission(
#         "Eliminació de Perills", 
#         "A SIlverhorn et demanen que eliminis diverses amenaçes per el poble...", 
#         "Principal", [("XP", 1000), ("Gold", 3500)], 10, 
#         [entityTypes[7], entityTypes[31], entityTypes[33], entityTypes[34], entityTypes[35],
#         entityTypes[36], entityTypes[37], entityTypes[44], entityTypes[45], entityTypes[47], 
#         entityTypes[48], entityTypes[51], entityTypes[52], entityTypes[68], entityTypes[69],
#         entityTypes[46], entityTypes[27]], 
#         [("Lv", 27), missions[7]], zones[20], True),
# )

# missions.append(
#     Missions.KillMission(
#         "El Gran Gegant", 
#         "A Silverhorn et donen una proba, si la superes et donaran un antic objecte del poble...", 
#         "Principal", [("XP", 2500), ("Gold", 5000)], 1, [entityTypes[70]], 
#         [("Lv", 30), missions[8]], zones[20], False, 
#         Entitat.Entity("Gegant Daurat", 25, False, entityTypes[54])),
# )

# missions.append(
#     Missions.PlaceMission(
#         "Una vella historia sobre una Estrella", 
#         "Escoltes d'una llegenda del poble, sobre una estrella enfonsant-se en un llac, diu la llegenda que en realitat aquesta estrella no es va efnfonsar sino que el va formar...", 
#         "Principal",
#         [("XP", 6000), ("Gold", 10000)], zones[21], [("Lv", 32), missions[9]]),
# )

# missions.append(
#     Missions.PlaceMission(
#         "Buscant una Estrella", 
#         "Un cop confirmat que sota el llac existeix algo, decideixes busacr l'estrella...", 
#         "Principal",
#         [("XP", 9000), ("Gold", 10000)], zones[23], [("Lv", 34), missions[10]]),
# )

# missions.append(
#     Missions.KillMission(
#         "El Guardia del Origen", 
#         "Escoltes d'una bestia sagrada en el lloc de l'estrella, que aquesta originalment hauria d'estar en les Muntanyes del Origen...\n" \
#         "Derroyta al guardia perillos del que t'ha parlat i entra en les Cavernes del Origen, ubicades més enlla del Bosc Obscur.", 
#         "Principal", [("XP", 15000), ("Gold", 25000)], 1, [entityTypes[70]], 
#         [("Lv", 40), missions[11]], zones[4], False,
#         Entitat.Entity("Eternitat", 40, False, entityTypes[62])),
# )

# missions.append(
#     Missions.PlaceMission(
#         "Pedra Misteriosa", 
#         "Dins les cavernes despres de retornar la estrella al seu lloc d'origen, recibeixes una misteriosa pedra des del lloc on has retornat l'estrella...", 
#         "Principal",
#         [("XP", 20000), ("Gold", 30000)], zones[5], [("Lv", 44), missions[12]]),
# )

#     # Missions Secundaries

# missions.append(
#     Missions.KillMission(
#         "Mostra de Confiança", 
#         "Troba i elimina al Llop lider, diuen que s'ha vist recentment per el Bosc Obscur", 
#         "Secundaria",
#         [("XP", 120), ("Gold", 1000), (objectes[1], 1)], 1, [entityTypes[4]], [("Lv", 15)], zones[1], False,
#         Entitat.Entity("Llop Lider", 17, False, entityTypes[4])),
# )

# missions.append(
#     Missions.KillMission("Mostra de Confiança II", 
#     "Elimina les restes de la manada de Llops en el bosc obscur.", 
#     "Secundaria", [("XP", 300), ("Gold", 2000), (objectes[1], 2)], 10, [entityTypes[4]], 
#     [("Lv", 16), missions[1]], zones[1], True),
#     )



# missions.append(
#     Missions.KillMission("Eliminant Sombres", 
#     "Elimina 15 sombres del bosc obscur.", 
#     "Secundaria", [("XP", 500), ("Gold", 3000), (objectes[1], 5)], 15, [entityTypes[6]], 
#     [("Lv", 10), missions[2]], zones[1], True),
#     )

missions.append(
    Missions.FindMission("Troba a en Jack", 
    "Un nen del pobla s'ha perdut, és diu Jack, creuen que s'ha endinsat massa en el bosc obscur...",
    "Secundaria", [("XP", 500), ("Gold", 2000)], "Jack", 
    [("Lv", 5)], zones[1])
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
    lista = Call.CallEntity("", True)
    for i in lista:
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
personatge = CrearJugador()
ubicacio = zones[0]
team = []
team.append(personatge)

jugador = Player.Player(personatge.nom, team, ubicacio)


# # Afegim algun objecte al jugador de base
jugador.AfegirObjecte(Call.CallObject("Pocio Inferior"), 2)

def AccioMenuPrincipal():
    global jugador
    
    pos = 0

    # Seleccionem el menu
    if jugador.Ubicacio.ZoneType == "Poble":
        menu = {1: "Mapa", 2: "Motxila", 3: "Hostal", 4: "Botiga", 5: "Estat", 6: "Missions", 7: "Éxits", 8: "Gremi", 9: "Guardar"}
    elif jugador.Ubicacio.ZoneType != "Poble":
        menu = {1: "Mapa", 2: "Motxila", 3: "Explorar", 4: "Lluitar", 5: "Estat", 6: "Missions", 7: "Éxits", 8: "Guardar"}

    print(f"Vostè es troba a {jugador.Ubicacio.NameZone}")
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
        #Botiga()
        print("No implementat")
    elif menu.get(pos) == "Estat":
        VeureEstatus()
    elif menu.get(pos) == "Missions":
        MenuMisions()
    elif menu.get(pos) == "Lluitar":
        GenerarEnemic()
    elif menu.get(pos) == "Guardar":
        print("")
    elif menu.get(pos) == "Éxits":
        #MostrarExits()
        print("No actualitxat")
    elif menu.get(pos) == "Motxila":
        jugador.ObjectesMochila(jugador.Team)
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
            if len(jugador.Team) > 1:
                print(" - Separem els nostres camins - ")
                count = 1
                for i in range(len(jugador.Team)):
                    if jugador.Team[i] != jugador:
                        print(f"{count} -> {jugador.Team[i].nom}, Lv: {jugador.Team[i].Lv}")
                        count += 1
                print(f"{count} -> Sortir")
                try:
                    sel = int(input("Digues amb qui vols separar camins: "))
                    if sel not in range(len(jugador.Team)):
                        print("Has de dir un dels personatges seleccionables...")
                    contractatsAnteriorment.append(jugador.Team[sel])
                    print(f"Has decidit separar camins amb {jugador.Team[sel].nom}...")
                    jugador.Team.remove(jugador.Team[sel])
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
                    if len(jugador.Team) < 3:
                        cost = ((len(contractatsAnteriorment)) + (len(jugador.Team))) * 5000
                        if jugador.Gold >= cost:
                            crear = ""
                            while crear not in ["s", "n"]:
                                ClearScreen()
                                print(f"Contractar un aventurer costara {cost} gold...")
                                crear = input(f"Contractaras a un nou aventurer tot i això: S / N\n").lower()
                                if crear not in ["s", "n"]:
                                    print("Has de dir una de les opcions...")
                            if crear == "s":
                                aventurer = CrearJugador()
                                jugador.Team.append(aventurer)
                                jugador.Team[0].Gold -= cost
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
                        if len(jugador.Team) < 3: 
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
                                    jugador.Team.append(aventurer)
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
    while res not in range(1, len(jugador.Team) + 2):
        ClearScreen()
        print("- De Qui vols veure les estadistiques -")
        count = 1
        for i in jugador.Team:
            print(f"{count} -> {i.nom}")
            count += 1
        print(f"{count} -> Sortir")
        res = int(input("Digues de qui vols veure l'estat: "))
        if res not in range(1, count + 1):
            print("Has de dir un dels numeros corresponents...")
    if res in range(1, count):
        ClearScreen()
        if combat == False:
            jugador.Team[res - 1].ShowStatus(jugador)
        else:
            jugador.Team[res - 1].ShowStatus(jugador, True)
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
            if res in [2, 3] and ubicacio.ZoneType != "Poble":
                print(f"Per acceptar o reclamar missions has d'estar en un Poblat.")
            else:
                if res == 1:
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
                    if filtrar in [1, 3, 4] and ubicacio.ZoneType != "Poble":
                        print(f"Per revisar aquestes missions hauries d'estar en una zona segura (Poble).")
                    else:
                        if filtrar == 2:
                            count, reclamar = ShowMisions("Accepted", "Res")
                        elif filtrar == 4:
                            count, reclamar = ShowMisions("Completed", "Res")
                        elif filtrar == 3:
                            count, reclamar  = ShowMisions("Requisites", "Res")
                        elif filtrar == 1:
                            count, reclamar  = ShowMisions("Totes", "Res")
                        if len(reclamar) == 0:
                            print("No hi ha cap missio en aquest apartat...")
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
                                    jugador.MisionsAcceptades.append(reclamar[aceptar - 1])
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
            print(f"Categoria: {i.Categoria}")
            print(f"Estat: {i.Status}")
            print(f"{i.Description}")
            if type(i) == Missions.KillMission:
                print(f"{i.Count} / {i.Quantity}")
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
            ClearScreen()
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
                i.afected = ["None"]
        else:
            print("No tens suficient gold per pagar la posada, has marxat sense poder descansar...")
    else:
        print("Has marxat...")

def Mapa():
    global jugador
    count = 1
    disponibles = []
    print(f"VOsté és a {jugador.Ubicacio.NameZone}.\n")
    for i in jugador.Ubicacio.Connections:  # Mostrem ubicacions disponibles
        if i.Trobada == True:
            print(f"{count} -> {i.NameZone}")
            print(f"{i.Description}")
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
        jugador.Ubicacio = disponibles[pos - 1]    # Canviem la zona i la retornem
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
    perTrobar = len(ubicacio.ObjectesPerTrobar)
    if perTrobar >= 1:
        choice = random.choices(["res", "objecte"], [10, 90])
        if choice == ["objecte"]:
            objectes = list(ubicacio.ObjectesPerTrobar.keys())
            probabilitat = [j[0] for j in ubicacio.ObjectesPerTrobar.values()]
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
        TrobarOr(jugador.Ubicacio.Or.keys())
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
        TrobarSeguentZona()
        
    jugador.Ubicacio.ExplorarCount += 1
    rutaTrobada = False
    for i in jugador.Ubicacio.Connections:
        if i.ZoneType == "Poble":
            if i.Trobada == False:
                i.Trobada = True
                print(f"Has trobat un cami a {i.NameZone}")
                rutaTrobada = True
        else:
            if jugador.Ubicacio.ExplorarCount >= i.IntentsPerTrobar and i.Trobada != True:
                i.Trobada = True
                print(f"Has trobat un cami a {i.NameZone}")
                rutaTrobada = True
    if choice[0] != "missio" and prob < 70 or rutaTrobada == True:
        input("Presiona per a continuar...")
    
def TrobarSeguentZona():
    global jugador
    posiblesRutesATrobar = []
    rutesTrobades = []
    for i in jugador.Ubicacio.Connections:
        complert = i.ComprobarCondicio(jugador.Team)
        if complert == True and i.Trobada == False:
            posiblesRutesATrobar.append(i)
        if i.Trobada == True:
            rutesTrobades.append(i)
    if len(posiblesRutesATrobar) == 0:
        if len(rutesTrobades) == len(jugador.Ubicacio.Connections):
            print("Ja has trobat totes les rutes en aquesta zona...")
        else:
            print("No sembla haber-hi cap altre ruta...")
    else:
        trobat = random.choice(jugador.Ubicacio.Connections)
        print(f"Has trobat una ruta a {trobat.NameZone}.")
        trobat.Trobada = True
    input("Presiona per a continuar...")

    

def TrobarOr(moneda):
    global jugador
    moneda = list(moneda)
    mult = 10
    if len(moneda) < 2:
        found = random.randint(jugador.Ubicacio.Or[moneda[0]][0][0], jugador.Ubicacio.Or[moneda[0]][0][1])
        print(f"Has trobat {found} monedes de {moneda[0]}")
    else:
        weight = []
        for i in jugador.Ubicacio.Or.values():
            weight.append(i[1])
        moneda = random.choices(moneda, weight)
        found = random.randint(jugador.Ubicacio.Or[moneda[0]][0][0], jugador.Ubicacio.Or[moneda[0]][0][1])
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
    jugador.Gold += found * mult
    

def MenuAtacar(personatge):
    global jugador
    res = 0
    while res not in range(1, len(personatge.Moves) + 2):
        ClearScreen()
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
    accio = 0
    while accio not in [1, 2, 3, 4]:
        try:
            accio = int(input("Que vols fer: "))
        except ValueError:
            print("Ha ocurregut un error...")
    turn = False
    fugir = [False]
    ClearScreen()
    BattleScreenShow(jugador.Team)
    BattleScreenShow(enemy)
    print("\n")
    if accio == 1:
        move = MenuAtacar(jug)
        target = None
        ClearScreen()
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
        ClearScreen()
        VeureEstatus(True)
        turn = True
    
    return jug, enemy, turn, fugir, enemyderr

def TriarObjectius(list):
    global jugador
    res = 0
    while res not in range(1, len(list) + 2):
        BattleScreenShow(jugador.Team)
        BattleScreenShow(list)
        ClearScreen()
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
    opcions = list(jugador.Ubicacio.Enemies.keys())
    seleccio = random.choices(opcions, jugador.Ubicacio.Enemies.values())
    for j in range(len(opcions)):
        if opcions[j] == seleccio[0]:
            prob = jugador.Ubicacio.ProbOfMultiple[j]
    num = []
    count = 1
    for i in prob:
        num.append(count)
        count += 1
    qty = random.choices(num, prob)
    enemy = []

    generar = Call.CallEntity(seleccio[0])
    enemy.append(Entitat.Entity("", random.randrange(jugador.Ubicacio.LevelRange[0], jugador.Ubicacio.LevelRange[1] + 1), False, generar))

    probs = []
    opcionsPosib = []

    for v in generar.Companions.items():
        probs.append(v[1])
        opcionsPosib.append(v[0])


    if qty[0] > 1:
        for l in range(qty[0] - 1):
            if len(generar.Companions.keys()) >= 1:
                apareix = random.choices(opcionsPosib, probs)
                generar = Call.CallEntity(apareix)
            entitat = Entitat.Entity("", random.randrange(jugador.Ubicacio.LevelRange[0] - 2, enemy[0].Lv), False, generar)
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
            else:
                if i.Damage > 0:
                    damagepereffect = ((entitat.StatsCombat["MaxHP"] / 100) * i.Damage)
                    entitat.StatsCombat["CurHP"] -= damagepereffect
                    print(f"{entitat.nom}, ha perdut {damagepereffect} HP degut a la {i.Name}.")
                    if entitat.StatsCombat["CurHP"] <= 0:
                        print(f"{entitat.nom}, ha estat derrotat per {i.Name}.")
                        derr += 1
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
            if jugador.Team[i].Priority >= 100 and len(enemy) >= 1 and jugador.Team[i].StatsCombat["CurHP"] > 0 and combat == True:
                turn = True
                while turn == True:
                    ClearScreen()
                    BattleScreenShow(jugador.Team)
                    BattleScreenShow(enemy)
                    turn = False
                    jugador.Team[i], enemy, turn, fugir, enemyderr = AccionsLluita(jugador.Team[i], enemy, enemyderr)
                    if fugir[0] == False:
                        jugador.Team[i], teamderr = ComprobarEfectEstat(jugador.Team[i], teamderr)
                    if turn == False:
                        jugador.Team[i].Priority = 0
                    input("\nPresiona per a continuar...")
                ClearScreen()
            if combat == True:
                combat = ComprobarFiCombat(combat, enemyderr, enemy, teamderr)

        # Turn enemic
        for j in range(len(enemy)):
            if enemy[j].Priority >= 100 and fugir[0] == False and len(jugador.Team) >= 1 and enemy[j].StatsCombat["CurHP"] > 0 and combat == True:
                ClearScreen()
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
                input("\nPresiona per a continuar...")
                ClearScreen()
            if combat == True:
                combat = ComprobarFiCombat(combat, enemyderr, enemy, teamderr)
        
        enemy = IncrementarPrioritat(enemy)
    finalitzarCombat(jugador.Team)

def ComprobarFiCombat(combat, enemyderr, enemy, teamderr):
    if enemyderr == len(enemy) or teamderr == len(jugador.Team):
            combat = False
            if len(enemy) == enemyderr:
                ClearScreen()
                print("Tos els enemics han estat derrotats !!")
                input("Presiona per a continuar")
    return combat

def DescartarDerrotats(p, derr):
    global jugador
    if p.StatsCombat["CurHP"] <= 0:
        derr += 1
        if p.isPlayer == False:
            ClearScreen()
            alive = 0
            for i in range(len(jugador.Team)): 
                if jugador.Team[i].StatsCombat["CurHP"] > 0:
                    jugador.Team[i].LvlUp(p)
                    alive += 1
            if alive >= 1:
                jugador.Gold += p.Lv * 10 # 10 monedes per cada nivell, representa que es ven el derrotat.
                print(f"Has guanyat {p.Lv * 10} gold.")
            Comprovacions(p)
    return derr

def Comprovacions(enemy):
    for i in missions:
        if type(i) == Missions.KillMission:
            i.IncrementCount(enemy)
    # for i in achievements:
    #     if i.Obtained == False:
    #         if type(i) == Exits.KillExit:
    #             i.IncrementCount(enemy)
    #         i.Completed(jugador)
    #         jugador.AcquiredAchievements.append(i)
    for i in jugador.Team:
        i.ComprovarSubClassesDisponibles()

def finalitzarCombat(clon):
    global jugador
    for i in range(len(jugador.Team)):
        # team[i].DefinirTempStats()
        # team[i].ResetBuffs()
        if jugador.Team[i] in clon:
            for j in clon:
                if j == jugador.Team[i]:
                    jugador.Team[i].StatsCombat["CurHP"] = j.StatsCombat["CurHP"]
                    jugador.Team[i].StatsCombat["Mana"] = j.StatsCombat["Mana"]
        else:
            jugador.Team[i].StatsCombat["CurHP"] = 0
            jugador.Team[i].StatsCombat["Mana"] = 0


        
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
            ClearScreen()
            AccioMenuPrincipal()
            alive = 0
            for i in jugador.Team:
                if i.StatsCombat["CurHP"] > 0:
                    alive += 1
        print(f"Has estat derrotat, t'han trobat i ara estas en la posada del ultim poble per el que has passat...")
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