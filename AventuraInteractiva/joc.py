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
                            True, (False, 0), 0, 5, ("Stat", (["ATK", "DEF"], 0.25))),
    Characteristics.Effects("Sangrat","Tens una ferida greu que fa perdre vida constantment...",
                            True, (False, 0), 0, 8, ("None", "")),
    Characteristics.Effects("Congelacio","Estas congelat durant una certa quantitat de temps...",
                            False, (True, 100), 3, 0, ("None", "")),
    Characteristics.Effects("Sangrat Greu","Tens una ferida greu que fa perdre vida constantment...",
                            True, (False, 0), 0, 16, ("Stat", (["ATK", "DEF", "SPD"], 0.15))),
    Characteristics.Effects("Terror","Causa una sensació de terror en l'objectiu, impedint actuar amb normalitat...",
                            False, (False, 0), 0, 4, ("Stat", (["ATK", "DEF", "INT", "SPD"], 0.25))),
    Characteristics.Effects("Paralisis","Causa una descarrega electrica al excedir-se...",
                            False, (True, 40), 0, 0, ("Stat", (["SPD"], 0.25))),
    Characteristics.Effects("Veri","Causa una quantitat de dany cada vegada que s'actua...",
                            False, (False, 0), 10, 0, ("None", "")),
    Characteristics.Effects("Mon dels Somnis","Entres en el domini dels somnis, aqui no saps que et depara el desti...",
                            False, (False, 0), 0, 0, ("Stat", (["ATK", "DEF", "INT", "SPD"], 0.5))),
    
    
]
        # Moves
movements = [   
    # Per a efectes d'estat dins la tupla un True, Seguit d'una altre tupla amb una llista amb les estadistiques, 
    # i en la segona part de la tupla la quantitat d'augment o reducció, l'augment ha de ser amb base 1 o superior, 
    # la reducció ha de ser de 0  a 0.9, es a dir iferior a 1.

    Characteristics.Moves("Bola de Foc", "Una bola de flamesd'alta temperatura", 40, 100, True, 5, [("Effect", (Effects[0], 30))], False, False, False),
    Characteristics.Moves("Fletxa Perforant", "", 50, 100, False, 5, [("Effect", (Effects[1], 60))], False, False, False),
    Characteristics.Moves("Assalt Llampeg", "Un conjunt d'atacs", 30, 100, False, 5, [("Stat", (["ATK", "SPD"],1.10))], False, False, False),
    Characteristics.Moves("Tall potent", "Un potent tall", 50, 100, False, 5, [("Stat", (["ATK"],1,1))], False, False, False),
    Characteristics.Moves("Aixafar", "", 20, 90, False, 0,  [("None","")], False, False, False),
    Characteristics.Moves("Debuff", "", 10, 100, False, 10, [("Stat", (["ATK", "DEF", "INT", "SPD"],0.25))], False, False, False),
    Characteristics.Moves("Tall", "", 25, 100, False, 0,  [("None","")], False, False, False),
    Characteristics.Moves("Cop de Basto", "", 5, 100, False, 0,  [("None","")], False, False, False),
    Characteristics.Moves("Dispar de Fletxa", "", 15, 100, False, 0,  [("None","")], False, False, False),
    Characteristics.Moves("Fletxa de flames", "", 45, 100, False, 10,  [("None","")], False, False, False),
    Characteristics.Moves("Increment", "", 0, 100, True, 10, [("Stat", (["ATK", "DEF", "INT", "SPD"],1.50))], False, False, False),
    Characteristics.Moves("Fulla de Vent", "", 45, 100, True, 10,  [("None","")], False, False, False),
    Characteristics.Moves("Tall Llampeg", "", 70, 100, False, 10, [("Stat", (["SPD"],))], False, False, False),
    Characteristics.Moves("Crit de Guerra", "", 5, 100, False, 10, [("Stat", (["ATK", "DEF", "SPD", "INT"],1,25)), ("Effect", (Effects[4], 100))], False, True, False),
    Characteristics.Moves("Bloqueig", "", 0, 100, False, 5, [("Stat", (["DEF"],1,5))], False, False, True, 40),
    Characteristics.Moves("Santuari", "", 150, 100, True, 90, [("Stat", (["ATK", "DEF", "INT", "SPD"],2.00))], True, True, False),
    Characteristics.Moves("Cura", "", 25, 100, True, 10,  [("None","")], True, False, False),
    Characteristics.Moves("Mossegada", "", 35, 100, False, 0,  [("None","")], False, False, False),
    Characteristics.Moves("Cop de Cua", "", 15, 100, False, 0,  [("None","")], False, False, False),
    Characteristics.Moves("Urpada", "", 20, 100, False, 0,  [("None","")], False, False, False),
    Characteristics.Moves("Picada", "", 15, 100, False, 0,  [("None","")], False, False, False),
    Characteristics.Moves("Cop", "", 20, 100, False, 0,  [("None","")], False, False, False),
    Characteristics.Moves("Embestir", "", 25, 100, False, 0,  [("None","")], False, False, False),
    Characteristics.Moves("Javelina de Glaç", "", 80, 100, True, 30,  [("None","")], False, False, False),
    Characteristics.Moves("Fletxa de Potencia", "", 160, 100, False, 70, [("Stat", (["ATK"],1,5)), ("Effect", (Effects[1], 100))], False, False, False),
    Characteristics.Moves("Revestiment de Flames", "Utilitzes flames per incrementar les teves capacitats i envoltar la teva arma...", 60, 100, True, 25, [("Stat", (["ATK", "SPD"],1.40))], False, False, False),
    Characteristics.Moves("Foc Infernal", "", 180, 90, True, 130,  [("None","")], False, True, False),
    Characteristics.Moves("Cocytus", "", 180, 90, True, 130,  [("None","")], False, True, False),
    Characteristics.Moves("Gravetat", "", 80, 100, True, 50, [("Stat", (["SPD"],0,4))], False, True, False),
    Characteristics.Moves("Gravidon", "", 150, 70, True, 100, [("Stat", (["SPD"],0,25))], False, False, False),
    Characteristics.Moves("Hydromancia", "", 50, 100, True, 20,  [("None","")], False, True, False),
    Characteristics.Moves("Esfera d'aigua", "", 40, 100, True, 5,  [("None","")], False, False, False),
    Characteristics.Moves("Tempesta", "", 100, 100, True, 70,  [("None","")], False, True, False),
    Characteristics.Moves("Raig", "", 90, 100, True, 50, [("Effect", (Effects[5], 20))], False, False, False),
    Characteristics.Moves("Pluja d'estalactites", "", 90, 100, True, 70,  [("None","")], False, True, False),
    Characteristics.Moves("Camp Electric", "", 90, 100, True, 70, [("Effect", (Effects[5], 90))], False, True, False),
    Characteristics.Moves("Cura en Area", "", 60, 100, True, 70,  [("None","")], True, True, False),
    Characteristics.Moves("Cura Potent", "", 100, 100, True, 60,  [("None","")], True, False, False),
    Characteristics.Moves("Regeneracio", "", 90, 100, True, 60,  [("None","")], True, False, False),
    Characteristics.Moves("Ventisca", "", 100, 100, True, 70, [("Effect", (Effects[2], 60))], False, True, False),
    Characteristics.Moves("Enllaç Electric", "", 70, 100, True, 50,  [("None","")], False, False, False),
    Characteristics.Moves("Gravetat Reduida", "", 40, 100, True, 20, [("Stat", (["SPD"],1,4))], False, False, False),
    Characteristics.Moves("Corrosio", "", 70, 100, True, 40, [("Stat", (["DEF"],0,4))], False, False, False),
    Characteristics.Moves("Mossegada Verinosa", "", 50, 100, False, 15, [("Effect", (Effects[6], 20))], False, False, False),
    Characteristics.Moves("Rafaga de Punyalades", "", 75, 100, False, 25, [("Effect", (Effects[1], 70))], False, False, False),
    Characteristics.Moves("Agulles de Terra", "", 100, 100, True, 90, [("Effect", (Effects[1], 70))], False, True, False),
    Characteristics.Moves("Fletxa Gelida", "", 100, 100, False, 50, [("Effect", (Effects[1], 20))], False, False, False),
    Characteristics.Moves("Fletxa Electrica", "", 100, 100, False, 50, [("Effect", (Effects[5], 90))], False, False, False),
    Characteristics.Moves("Dispar Rapid", "", 30, 100, False, 15, [("Stat", (["SPD"],1,4))], False, False, False),
    Characteristics.Moves("Agilitat", "", 30, 100, False, 5, [("Stat", (["SPD"],1,4))], False, False, False),
    Characteristics.Moves("Martell Sacre", "", 120, 90, True, 60,  [("None","")], False, False, False),
    Characteristics.Moves("Estandard Sacre", "", 20, 100, True, 25, [("Stat", (["ATK", "DEF", "SPD", "INT"],2.00))], False, True, False),
    Characteristics.Moves("Reforçament Sacre", "", 0, 100, True, 25, [("Stat", (["ATK", "DEF", "SPD"],2.00))], False, False, False),
    Characteristics.Moves("Torbelli", "", 40, 100, True, 15,  [("None","")], False, True, False),
    Characteristics.Moves("Tela d'aranya", "", 5, 75, False, 5, [("Stat", (["SPD"],0,3))], False, False, False),
    Characteristics.Moves("Tela Corrosiva", "", 60, 90, False, 25, [("Stat", (["DEF"],0,2))], False, False, False),
    Characteristics.Moves("Control Sanguini", "", 75, 100, True, 60, [("Effect", (Effects[3], 80))], False, True, False),
    Characteristics.Moves("Llança de Sang", "", 90, 90, True, 50, [("Effect", (Effects[3], 90))], False, False, False),
    Characteristics.Moves("Esfera Vital", "", 100, 90, True, 50,  [("None","")], False, False, False),
    Characteristics.Moves("Mirall dels Somnis", "", 150, 100, True, 200, [("Stat", (["ATK", "DEF", "INT", "SPD"],0,5)), ("Effect", (Effects[7], 100))], False, False, False),
    Characteristics.Moves("Dimensio Alterada", "", 200, 100, True, 300, [("Stat", (["SPD", "DEF"],0,5)), ("Effect", (Effects[7], 100))], False, True, False),
    Characteristics.Moves("Gran Resistencia", "", 0, 100, False, 20, [("Stat", (["DEF"],2,5))], False, False, False),
    Characteristics.Moves("Contratac", "", 0, 100, False, 20, [("Stat", (["ATK"],2))], False, False, True, 100),
    Characteristics.Moves("Cant Mortal", "", 0, 30, True, 100,  [("None","")], False, True, False),
    Characteristics.Moves("Espases d'aigua", "", 130, 100, True, 100, [("Effect", (Effects[3], 30))], False, True, False),
    Characteristics.Moves("Escut de Gel", "", 0, 100, True, 15,  [("None","")], False, False, True, 70),
    Characteristics.Moves("Mur de Roca", "", 0, 100, True, 15,  [("None","")], False, False, True, 70),
    Characteristics.Moves("Proteccio del Caballer", "", 0, 100, False, 20, [("Stat", (["DEF", "ATK", "INT"],1.60))], False, True, True, 100),
    Characteristics.Moves("Resurreccio", "", 250, 100, True, 100, [("Stat", (["INT", "ATK", "DEF", "SPD"],2.00))], True, False, False),
    Characteristics.Moves("Disolucio", "", 30, 100, False, 5,  [("None","")], False, False, False),
    Characteristics.Moves("Fum Sospitos", "", 15, 100, False, 10, [("Stat", (["ATK", "DEF", "INT", "SPD"],0.35))], False, True, False),
]
        # Skills
skills = [

]

        # Entitats
entityTypes = [
    # Cal tenir en compte les estadistiques, els grups als que pertanyen, i el diccionari de moviments i nivell.
        EntityType.EntityType("Guerrer", True, 160, 100, 140, 40, 130, 80, 50, ["Human"], "", {movements[6]: 1, movements[3]: 3, movements[12]: 10, movements[13]: 12, movements[14]: 5}),
        EntityType.EntityType("Mag", True, 80, 200, 60, 180, 100, 100, 50, ["Human"], "", {movements[7]: 1, movements[0]: 3, movements[9]: 6, movements[11]: 6, movements[10]: 10, movements[23]: 14, movements[28]: 20}),
        EntityType.EntityType("Arquer", True, 120, 140, 140, 100, 140, 120, 50, ["Human"], "", {movements[8]: 1, movements[1]: 3, movements[48]: 6, movements[47]: 22, movements[24]: 33}),
        EntityType.EntityType("Lladre", True, 120, 120, 130, 100, 120, 160, 50, ["Human"], "", {movements[6]: 1, movements[2]: 3, movements[44]: 8, movements[49]: 12}),
        EntityType.EntityType("Llop", False, 120, 40, 120, 20, 100, 140, 30, ["Beast"], "", {movements[17]: 1, movements[19]: 5}),
        EntityType.EntityType("Slime", False, 60, 60, 60, 60, 60, 60, 20, ["Monster"], "", {movements[21]: 1, movements[22]: 6, movements[69]: 9}),
        EntityType.EntityType("Sombra", False, 120, 120, 120, 120, 120, 120, 200, ["Monster"], "", {movements[17]: 1}),
        EntityType.EntityType("Llangardaix de Roca", False, 160, 120, 160, 50, 160, 100, 100, ["Monster", "Beast"], "", {movements[17]: 1, movements[18]: 3, movements[4]: 5, movements[45]: 25}),
        EntityType.EntityType("Driade", False, 100, 230, 100, 250, 100, 100, 400, ["Spirit"], "", {movements[17]: 1}),
        EntityType.EntityType("Treant", False, 200, 140, 150, 120, 150, 100, 400, ["Monster"], "", {movements[17]: 1}),
        EntityType.EntityType("Golem", False, 250, 100, 160, 80, 200, 60, 500, ["Artificial"], "", {movements[17]: 1}),
        EntityType.EntityType("Mag de Flames", False, 60, 250, 60, 220, 50, 50, 50, ["Human"], "Un mag centrat en poderosos atacs destructius", {movements[17]: 1}),
        EntityType.EntityType("Griu", False, 200, 200, 220, 160, 160, 220, 1000, ["Beast", "Monster"], "Una bestia llegendaria, amb cap i ales d'aguila i cos de lleó...", {movements[17]: 1}),
        EntityType.EntityType("Expert en Armes", False, 160, 120, 180, 100, 130, 100, 50, ["Human"], "Un expert en diverses armes cos a cos, és molt capaç, és una forma millorada del Guerrer...", {movements[17]: 1}),
        EntityType.EntityType("Caballer", False, 200, 60, 100, 40, 260, 60, 50, ["Human"], "Un expert especialitzat en la resistencia, tot i això te una capacitat ofensiva considerable.", {movements[17]: 1}),
        EntityType.EntityType("Aventurer", True, 140, 120, 140, 140, 115, 115, 50, ["Human"], "No especialitzat en cap camp en excés, no destaca en cap camp però tampoc és dolent en cap d'ells...", {movements[17]: 1}),
        EntityType.EntityType("Porc Senglar", False, 150, 40, 150, 20, 140, 80, 35, ["Beast"], "", {movements[21]: 1, movements[22]: 5}),
        EntityType.EntityType("Sacerdot", True, 120, 160, 80, 120, 120, 120, 50, ["Human"], "", {movements[17]: 1}),
        EntityType.EntityType("Sacerdot Guerrer", False, 200, 160, 250, 180, 150, 150, 150, ["Human"], "", {movements[17]: 1}),
        EntityType.EntityType("Caballer Magic", False, 250, 160, 200, 300, 180, 160, 150, ["Human"], "Un forma avançada de caballeria i magia...", {movements[17]: 1}),
        EntityType.EntityType("Sant", False, 200, 250, 80, 200, 120, 100, 150, ["Human"], "Una especialitzacio en curacio per part del sacerdot", {movements[17]: 1}),
        EntityType.EntityType("Sage", False, 150, 280, 80, 300, 120, 150, 150, ["Human"], "Un Mag que ha entes la veritat de la magia", {movements[17]: 1}),
        EntityType.EntityType("Atacant Veloç", False, 170, 100, 150, 100, 120, 250, 150, ["Human"], "Una disposicio agil permet a un lladre concentrarse en realitzar multiples atacs i acomular dany gradualment", {movements[17]: 1}),
        EntityType.EntityType("Atacant de Descentatges", False, 170, 120, 110, 150, 120, 200, 150, ["Human"], "Un lladre centrat en atacar aplicant desventatges en els enemics", {movements[17]: 1}),
        EntityType.EntityType("Arquer Magic", False, 170, 160, 200, 160, 120, 200, 150, ["Human"], "Un arquer centrat en multiples atacs magics i normals", {movements[17]: 1}),
        EntityType.EntityType("Arquer Potent", False, 180, 120, 200, 100, 120, 50, 150, ["Human"], "Un arquer centrat en el dany per atac mes que en atacar seguit", {movements[17]: 1}),
        EntityType.EntityType("Conill Cornut", False, 100, 20, 80, 20, 100, 110, 25, ["Beast", "Monster"], "", {movements[22]: 1, movements[17]: 5}),
        EntityType.EntityType("Fenrir", False, 400, 400, 400, 400, 400, 400, 4000, ["Divine", "Beast"], "", {movements[17]: 1}),
        EntityType.EntityType("Wight", False, 120, 100, 120, 40, 120, 100, 50, ["Spirit", "Monster"], "", {movements[17]: 1}),
        EntityType.EntityType("Lich", False, 200, 300, 150, 250, 200, 180, 800, ["Spirit", "Monster"], "", {movements[17]: 1}),
        EntityType.EntityType("Vampire", False, 250, 200, 250, 250, 200, 180, 800, ["Monster", "Human"], "", {movements[17]: 1}),
        EntityType.EntityType("Ghoul", False, 140, 100, 140, 80, 130, 110, 75, ["Monster"], "", {movements[17]: 1}),
        EntityType.EntityType("Aranya de Bosc", False, 140, 40, 140, 40, 120, 120, 50, ["Monster"], "", {movements[18]: 1, movements[22]: 3, movements[0]: 10, movements[45]: 30}),
        EntityType.EntityType("Wyrm", False, 180, 120, 160, 160, 140, 140, 75, ["Monster"], "", {movements[17]: 1, movements[20]: 4, movements[54]: 5, movements[55]: 10, movements[43]: 24}),
        EntityType.EntityType("Guivern de Gel", False, 220, 250, 200, 220, 220, 180, 500, ["Monster"], "", {movements[17]: 1}),
        EntityType.EntityType("Guivern", False, 220, 250, 220, 200, 210, 190, 500, ["Monster"], "", {movements[17]: 1}),
        EntityType.EntityType("Guivern de Roca", False, 250, 220, 200, 200, 260, 150, 500, ["Monster"], "", {movements[17]: 1}),
        EntityType.EntityType("Guivern de Vent", False, 220, 250, 200, 200, 190, 200, 500, ["Monster"], "", {movements[17]: 1}),
        EntityType.EntityType("Gran Tortuga", False, 200, 160, 150, 150, 200, 80, 300, ["Monster", "Aquatic"], "", {movements[22]: 1, movements[30]: 5, movements[31]: 7}),
        EntityType.EntityType("Tortuga Marina", False, 150, 80, 120, 120, 150, 60, 100, ["Monster", "Aquatic"], "", {movements[22]: 1, movements[23]: 24, movements[30]: 5, movements[31]: 7}),
        EntityType.EntityType("Serp Marina", False, 150, 180, 150, 180, 140, 120, 220, ["Monster", "Aquatic"], "", {movements[18]: 1, movements[17]: 4, movements[23]: 24, movements[30]: 5, movements[31]: 7}),
        EntityType.EntityType("Leviathan", False, 420, 400, 400, 420, 420, 300, 4000, ["Divine", "Aquatic"], "", {movements[17]: 1}),
        EntityType.EntityType("Cranc Aberrant", False, 140, 100, 150, 120, 130, 100, 150, ["Aquatic", "Monster"], "", {movements[21]: 1, movements[4]: 4}),
        EntityType.EntityType("Gran Cranc Aberrant", False, 180, 150, 180, 160, 180, 120, 370, ["Aquatic", "Monster"], "", {movements[21]: 1, movements[4]: 4, movements[23]: 26, movements[30]: 5, movements[31]: 7}),
        EntityType.EntityType("Os Monstruos", False, 160, 80, 160, 80, 170, 110, 200, ["Monster", "Beast"], "", {movements[19]: 1, movements[17]: 4}),
        EntityType.EntityType("Os de Fang", False, 240, 240, 240, 240, 240, 200, 600, ["Artificial", "Monster"], "", {movements[19]: 1, movements[17]: 4, movements[45]: 30, movements[28]: 23}),
        EntityType.EntityType("Aguila Terrorifica", False, 120, 120, 120, 120, 100, 150, 100, ["Monster", "Beast"], "", {movements[19]: 1, movements[17]: 4, movements[11]: 10}),
        EntityType.EntityType("Aguila Platejada", False, 170, 170, 180, 120, 130, 180, 400, ["Spirit", "Beast"], "", {movements[19]: 1, movements[17]: 4, movements[11]: 10, movements[32]: 30, movements[23]: 25}),
        EntityType.EntityType("Ogre", False, 140, 120, 150, 120, 160, 130, 250, ["Monster", "Human"], "", {movements[21]: 1, movements[3]: 4, movements[12]: 10, movements[25]: 24}),
        EntityType.EntityType("Orc", False, 120, 100, 110, 100, 120, 80, 150, ["Monster", "Human"], "", {movements[21]: 1, movements[8]: 4}),
        EntityType.EntityType("Goblin", False, 80, 20, 80, 20, 100, 120, 25, ["Monster", "Human"], "", {movements[21]: 1, movements[8]: 4}),
        EntityType.EntityType("Formiga Ogre", False, 120, 120, 140, 100, 130, 140, 200, ["Monster"], "", {movements[17]: 1}),
        EntityType.EntityType("Caball d'Acer", False, 150, 50, 140, 50, 170, 170, 250, ["Monster", "Beast"], "", {movements[17]: 1}),
        EntityType.EntityType("Gran Slime", False, 200, 200, 200, 200, 200, 200, 500, ["Monster"], "", {movements[17]: 1}),
        EntityType.EntityType("Golem d'Oricalc", False, 400, 300, 350, 300, 370, 150, 2000, ["Artificial", "Divine"], "", {movements[17]: 1}),
        EntityType.EntityType("Slime de Ferro", False, 170, 170, 170, 170, 170, 160, 200, ["Artificial", "Monster"], "", {movements[17]: 1}),
        EntityType.EntityType("Slime d'Oricalc", False, 400, 400, 320, 350, 340, 250, 3000, ["Divine", "Monster"], "", {movements[17]: 1}),
        EntityType.EntityType("Basilisc", False, 260, 240, 260, 250, 220, 230, 1000, ["Monster"], "", {movements[17]: 1}),
        EntityType.EntityType("Quimera", False, 250, 250, 250, 250, 250, 200, 1000, ["Artificial", "Monster"], "", {movements[17]: 1}),
        EntityType.EntityType("Manticora", False, 240, 240, 280, 240, 250, 270, 1000, ["Human"], "", {movements[17]: 1}),
        EntityType.EntityType("Cor d'Acer Magic", False, 300, 300, 280, 250, 300, 50, 1200, ["Human"], "", {movements[17]: 1}),
        EntityType.EntityType("Siren", False, 120, 120, 130, 130, 100, 160, 200, ["Human"], "Un ocell amb cap huma, causa terror entre els mariners...", {movements[19]: 1, movements[11]: 10, movements[53]: 14}),
        EntityType.EntityType("Ouroboros", False, 500, 500, 400, 450, 500, 250, 5000, ["Divine", "Beast"], "", {movements[17]: 1}),
        EntityType.EntityType("Jormungandr", False, 450, 400, 400, 380, 450, 200, 4000, ["Divine", "Beast"], "", {movements[17]: 1}),
        EntityType.EntityType("Walpurgis", False, 200, 500, 200, 500, 300, 350, 4000, ["Divine", "Spirit"], "", {movements[17]: 1}),
        EntityType.EntityType("Serafi", False, 300, 300, 300, 300, 300, 300, 3000, ["Divine", "Spirit"], "", {movements[17]: 1}),
        EntityType.EntityType("Golem de Metall", False, 300, 150, 250, 150, 280, 100, 1000, ["Artificial"], "", {movements[17]: 1}),
        EntityType.EntityType("Sephirot", False, 450, 450, 350, 420, 420, 150, 3800, ["Divine", "Beast"], "", {movements[17]: 1}),
        EntityType.EntityType("Anogratch", False, 140, 120, 140, 120, 120, 140, 70, ["Monster"], "", {movements[17]: 1}),
        EntityType.EntityType("Bagragratch", False, 170, 150, 170, 150, 150, 170, 340, ["Monster"], "", {movements[17]: 1}),
        EntityType.EntityType("Gran aranya", False, 200, 200, 220, 170, 220, 160, 370, ["Monster"], "", {movements[17]: 1}),
        EntityType.EntityType("Rey Ogre", False, 250, 200, 250, 200, 250, 220, 750, ["Monster", "Human"], "", {movements[17]: 1}),
        EntityType.EntityType("Oni", False, 300, 300, 350, 300, 320, 300, 3000, ["Divine", "Monster"], "", {movements[17]: 1}),
        EntityType.EntityType("Vespa Gegant", False, 150, 120, 150, 120, 100, 160, 120, ["Monster"], "", {movements[20]: 1, movements[43]: 4}),
        EntityType.EntityType("Granota Verinosa", False, 120, 100, 120, 100, 100, 120, 100, ["Monster"], "", {movements[21]: 1, movements[43]: 4}),
        EntityType.EntityType("Gran Granota Verinosa", False, 160, 160, 170, 150, 150, 140, 300, ["Monster"], "", {movements[21]: 1, movements[43]: 4}),
        EntityType.EntityType("Vespa General", False, 170, 120, 170, 140, 120, 190, 300, ["Monster"], "", {movements[20]: 1, movements[43]: 4}),
        EntityType.EntityType("Verdader Ancestre Vampir", False, 420, 420, 400, 400, 300, 300, 3000, ["Divine", "Spirit"], "", {movements[17]: 1}),
        EntityType.EntityType("Oneiros", False, 400, 400, 450, 450, 400, 370, 5000, ["Divine", "Beast"], "", {movements[17]: 1}),
        EntityType.EntityType("Fada", False, 80, 250, 10, 200, 30, 200, 100, ["Spirit"], "", {movements[21]: 1}),
        EntityType.EntityType("Gnom", False, 150, 150, 150, 100, 150, 120, 100, ["Spirit", "Beast"], "", {movements[21]: 1}),
        ]

# Afegint Paths (Posibles SUbclasses)
entityTypes[1].AddPaths({entityTypes[11]: [[("Lv", 30), ("Stat", [("Mana", 120)])], False]})


# Afegint monstres que poden apareixer conjuntament amb un altre.
entityTypes[43].AddCompanions({entityTypes[42]: 99, entityTypes[43]: 1})    # Gran Cranc Abberrant
entityTypes[38].AddCompanions({entityTypes[39]: 99, entityTypes[38]: 1})    # Gran Toruga Marina
entityTypes[34].AddCompanions({entityTypes[33]: 100})   # Guiverns els 4 d'aball
entityTypes[35].AddCompanions({entityTypes[33]: 100})
entityTypes[36].AddCompanions({entityTypes[33]: 100})
entityTypes[37].AddCompanions({entityTypes[33]: 100})
entityTypes[53].AddCompanions({entityTypes[5]: 99, entityTypes[53]: 1}) # Gran Slime
entityTypes[69].AddCompanions({entityTypes[68]: 100})   # Bagragratch
entityTypes[75].AddCompanions({entityTypes[74]: 95, entityTypes[75]: 5})    # Granota
entityTypes[76].AddCompanions({entityTypes[73]: 95, entityTypes[76]: 5})    # Vespa





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
                   "Bosc", {entityTypes[4]: 35, entityTypes[5]: 40, entityTypes[15]: 25},
                   # Llista amb probabilitat de cada un dels enemics per ordre d'apareixer en grups de fins a 3.
                   # Cada llista representa un enemic, i cada valor la prob per 1, 2, 3 enemics.
                   [[85, 13, 2], [95, 5], [99, 1]], (8, 14), {"Bronze": [(1, 7), 100]}, True),
        
        Zones.Zona("Profunditats del Bosc Obscur",
                   "Les profunditats del bosc obscur, una perillosa zona de la que és diu que qui hi entra no en surt...",
                   "Bosc", {entityTypes[4]: 32, entityTypes[5]: 40, entityTypes[6]: 20, entityTypes[8]: 5, entityTypes[9]: 3}, 
                   [[85, 13, 2], [95, 5], [99, 1], [99, 1], [99, 1]], (37, 45), {"Plata": [(15, 25), 100]}),
        
        Zones.Zona("Centre del Bosc Obscur",
                   "La zona central del bosc obscur, hi habiten monstres desconeguts, ningú ha tornat mai d'aquest lloc...",
                   "Bosc", {entityTypes[6]: 30, entityTypes[8]: 30, entityTypes[9]: 40}, 
                    [[85, 13, 2], [95, 5], [99, 1]], (43, 52), {"Or": [(1, 10), 40], "Plata": [(20, 40), 60]}),
        
        Zones.Zona("Muntanyes del Origen",
                   "Unes muntanyes només conegudes per llegendes, es diu que són el primer lloc en ser creat d'aquest món...",
                   "Muntanya", {entityTypes[7]: 50, entityTypes[8]: 20, entityTypes[9]: 20, entityTypes[10]: 10}, 
                   [[85, 13, 2], [95, 5], [99, 1], [99, 1]], (50, 55), {"Or": [(6, 15), 90], "Or Platejat": [(1, 3), 10]}),
        
        Zones.Zona("Cavernes del Origen",
                   "Les cavernes de les muntanyes del origen, no és te coneixement de la existencia d'aquestes...",
                   "Cavernes", {entityTypes[6]: 40, entityTypes[7]: 30, entityTypes[10]: 30}, 
                    [[85, 13, 2], [95, 5], [99, 1]], (52, 57), {"Or Platejat": [(2, 5), 100]}),
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
                   "Bosc", {entityTypes[4]: 8, entityTypes[5]: 30, entityTypes[26]: 47, entityTypes[15]: 5, 
                            entityTypes[0]: 3, entityTypes[2]: 3, entityTypes[3]: 4}, 
                   [[15, 83, 2], [93, 5, 2], [95, 5], [99, 1], [30, 50, 20], [30, 50, 20], [30, 50, 20]], 
                   (3, 5), {"Bronze": [(1, 5), 100]}, True),

        Zones.Zona("Rocklink",
                   "Unes muntanyes que presenten el cami cap a la capital del regne...",
                   "Muntanya", {entityTypes[4]: 40, entityTypes[33]: 20, entityTypes[7]: 30, 
                            entityTypes[0]: 3, entityTypes[2]: 3, entityTypes[3]: 4}, 
                   [[20, 75, 5], [100], [95, 5], [50, 40], [50, 40], [50, 40]], 
                   (5, 9), {"Bronze": [(10, 20), 90], "Plata": [(2, 5), 10]}, False),

        Zones.Zona("Camps de Knightshire",
                   "Els camps a les afores de knightshire, aquestes \"afores\" son bastant grans...",
                   "Camps", {entityTypes[5]: 90, entityTypes[4]: 10, entityTypes[26]: 50}, 
                   [[95, 5], [40, 55, 5], [95, 5]], (3, 5), {"Bronze": [(1, 5), 100]}, False),
            
            # Cami de Knightshire a Lakestar o Faylight (Pasant per Muntayes Estelars)
        
        Zones.Zona("Bosc Estelar",
                   "Un bosc que guia cap a les muntanyes estelars...",
                   "Bosc", {entityTypes[26]: 50, entityTypes[32]: 50, entityTypes[28]: 50}, 
                   [], 
                   (8, 13), {"Bronze": [(12, 25), 70], "Plata": [(4, 9), 30]}, False),
        
        Zones.Zona("Muntanyes Estelars",
                   "Unes muntanyes de les que es diu que les estrelles guien a les persones que hi passen...",
                   "Muntanya", {entityTypes[4]: 30, entityTypes[5]: 40, entityTypes[7]: 35, entityTypes[44]: 8, 
                                entityTypes[1]: 1, entityTypes[0]: 2, entityTypes[2]: 2, entityTypes[3]: 2}, 
                   [[82, 15, 3],[92, 6, 2], [98,2], [100], [30, 50, 20], [30, 50, 20], [30, 50, 20], [30, 50, 20]], 
                   (12, 17), {"Bronze": [(16, 25), 70], "Plata": [(7, 9), 30]}, False),
        
        Zones.Zona("Cami de Roca",
                   "Un cami rocos que guia cap a la platja de Lakestar.",
                   "Muntanya i Platja", {entityTypes[4]: 50, entityTypes[46]: 20, entityTypes[7]: 18, 
                                         entityTypes[1]: 3, entityTypes[0]: 4, entityTypes[2]: 3, entityTypes[3]: 3}, 
                   [[82, 15, 3],[92, 6, 2], [98,2], [30, 50, 20], [30, 50, 20], [30, 50, 20], [30, 50, 20]], 
                   (15, 17), {"Bronze": [(16, 25), 70], "Plata": [(7, 9), 30]}, False),
        
        Zones.Zona("Platja de Lakestar",
                   "La platja del Gran llac Lakestar...",
                   "Platja", {entityTypes[46]: 32, entityTypes[38]: 2, entityTypes[39]: 30, entityTypes[40]: 15,
                              entityTypes[42]: 20, entityTypes[43]: 1}, 
                   [[95, 5], [100], [95, 5], [100], [95, 5], [100]], 
                   (10, 15), {"Bronze": [(10, 20), 100]}, False)
]

# Cami de Lakestar a Faylight o (Pendent)
zones.append(
Zones.Zona(
    "Serra del Bosc de Llum",
    "Una gran serra que bloqueja el pas cap el Gran Bosc de llum, si hi vols arribar, has de passar per aquestes...",
    "Muntanya", {entityTypes[33]: 22, entityTypes[7]: 25, entityTypes[48]: 5, entityTypes[49]: 8,
                 entityTypes[44]: 10, entityTypes[50]: 30}, 
    [[90, 10], [95, 5], [100], [95, 5], [100], [40, 55, 5]],
    (15, 20), {"Plata": [(10, 15), 100]}, False, (("Ubicacio", [zones[8]]))),
)

            
zones.append(
Zones.Zona(
    "Gran Bosc de Llum",
    "Un Bosc on la llum no desapareix ni tant sols durant la nit, d'aqui el seu nou...",
    "Bosc", {entityTypes[50]: 30, entityTypes[32]: 40, entityTypes[70]: 2, entityTypes[73]: 14, entityTypes[74]: 14}, 
    [[30, 65, 5], [80, 20], [100], [90, 10], [90, 10]], 
    (18, 23), {"Plata": [(10, 15), 100]}, False)
)      

zones.append(
Zones.Zona(
    "Bosc de les Fades",
    "Un bosc que quasi ningu coneix, encara que esta dins d'un bosc molt conegut...",
    "Bosc", {entityTypes[79]: 80, entityTypes[80]: 20}, [[100], [100]],
    (21, 26), {"Plata": [(10, 15), 100]}, False))

# Cami de Faylight a Silverhorn
zones.append(
Zones.Zona(
    "Grans Muntanyes Blanques",
    "Una gran serralada blanca, és diu que en aquestes muntanyes hi ha un poble llegendari...",
    "Muntanya", {entityTypes[7]: 40, entityTypes[31]: 15, entityTypes[33]: 30, entityTypes[34]: 15, entityTypes[35]: 15,
                entityTypes[36]: 15, entityTypes[37]: 15, entityTypes[44]: 15, entityTypes[45]: 7, entityTypes[47]: 20, 
                entityTypes[48]: 20, entityTypes[51]: 20, entityTypes[52]: 20, entityTypes[68]: 7, entityTypes[69]: 7,
                entityTypes[46]: 20, entityTypes[27]: 1},
                [[90, 10], [100], [100], [100], [100], [100], [100], [95, 5], [100], [100], [95, 5], [88, 10, 2], [95, 5], [70, 25, 5], [100], [60, 35, 5], [100]], 
    (24, 29), {"Plata": [(10, 15), 100]}, 
    False, None, 20)
    )
                
zones.append(
# Conectat a lakestar mitjançant el llac, necessita haber trobat silverhorn i cert objecte per trobar la zona...
Zones.Zona( 
    "Profunditats de Lakestar",
    "Un cami subterrani que avança dins el Gran llac, normalment ningú en sabria la existencia...",
    "Cavernes", {entityTypes[68]: 20, entityTypes[69]: 5, entityTypes[42]: 20, entityTypes[43]: 5, 
                 entityTypes[39]: 20, entityTypes[38]: 5, entityTypes[74]: 20, entityTypes[75]: 5},
    [[75, 25], [98, 2], [75, 25], [98, 2], [75, 25], [98, 2], [75, 25], [98, 2]], 
    (30, 35), {"Plata": [(20, 25), 100]}, False,
    (("Ubicacio", [zones[6]])), 25)
    )

zones.append(
# Conectat a lakestar mitjançant el llac, necessita haber trobat silverhorn i cert objecte per trobar la zona...
Zones.Zona( 
    "Mon Subterrani",
    "Un mon subterrani sota el Gran Llac, aquest lloc sembla donar sentit a la historia de la estrella...",
    "Cavernes", {entityTypes[68]: 50, entityTypes[69]: 15, entityTypes[51]: 30, entityTypes[53]: 10,
                 entityTypes[42]: 50, entityTypes[43]: 15, entityTypes[74]: 30, entityTypes[75]: 10, entityTypes[57]: 1},
    [[40, 40, 20], [80, 20], [50, 40, 10], [60, 35, 5], [40, 40, 20], [60, 35, 5], [40, 40, 20], [80, 20], [100]],
    (35, 40), {"Plata": [(30, 45), 100]}, False)
    )

zones.append(
# Conectat a lakestar mitjançant el llac, necessita haber trobat silverhorn i cert objecte per trobar la zona...
Zones.Zona( 
    "Illa estelar",
    "Es pot veure l'estrella en el crater d'aquesta illa..., rodejada per un munt de monstres marins.",
    "Cavernes", {entityTypes[40]: 50, entityTypes[41]: 1, entityTypes[42]: 50, entityTypes[43]: 15,
                 entityTypes[39]: 50, entityTypes[38]: 15, entityTypes[53]: 15},
    [[40, 40, 20], [100], [50, 40, 10], [60, 35, 5], [40, 40, 20], [60, 35, 5], [60, 35, 5]],
    (35, 40), {"Plata": [(35, 45), 100]}, False)
    )



        # Connexions de cada zona
    # Pobles
zones[0].AddConnections([zones[1], zones[10]])  # Dawn Viallage
zones[6].AddConnections([zones[1]])  # Silverhorn
zones[7].AddConnections([zones[18], zones[20]]) # Faylight
zones[8].AddConnections([zones[16]]) # Lakestar
zones[9].AddConnections([zones[12]]) # Knightshire

    # Salvatge
zones[1].AddConnections([zones[0], zones[2]])   # Bosc Obscur
zones[2].AddConnections([zones[1], zones[3]])   # Profunditats Bosc Obscur
zones[3].AddConnections([zones[2], zones[4]])   # Centre Bosc Obscur
zones[4].AddConnections([zones[3], zones[5]])   # Muntanyes Origen
zones[5].AddConnections([zones[4]]) # Cavernes del origen
zones[10].AddConnections([zones[0], zones[11]]) # Bosc del SUd
zones[11].AddConnections([zones[10], zones[12]])    # Rocklink
zones[12].AddConnections([zones[11], zones[9], zones[13]])  # Camps de Knightshire
zones[13].AddConnections([zones[12], zones[14]])    # Bosc Estelar
zones[14].AddConnections([zones[13], zones[15], zones[17]]) # Muntanyes Estelars
zones[15].AddConnections([zones[14], zones[16], zones[21]])    # Cami Rocos
zones[16].AddConnections([zones[15], zones[8]]) # Platja de Lakestar
zones[17].AddConnections([zones[14], zones[18]]) # Serra del Bosc de Llum
zones[18].AddConnections([zones[17], zones[19]]) # Gran Bosc de Llum
zones[19].AddConnections([zones[18], zones[7]]) # Bosc de Fades
zones[20].AddConnections([zones[7], zones[6]]) # Grans Muntanyes Blanques
zones[21].AddConnections([zones[15], zones[22]]) # Profunditats de Lakestar
zones[22].AddConnections([zones[21], zones[23]]) # Mon Subterrani
zones[23].AddConnections([zones[22]]) # Illa Estelar



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
]
    # En els killexit son els grups que s'ha de derrotar i la quantitat, així com el titul recibit en cas de ser titul la
    # recompensa.
titles = []


def CrearTitolsIKillExits():
    for i in entityGroups.items():
        slayer =Titles.Titles(f"{i[0]} Slayer", f"Augmenta el dany causat contra enemics de tipus {i[0]}", i[1], 1.3)
        anihilator = Titles.Titles(f"{i[0]} Anihilator", f"Augmenta el dany causat contra enemics de tipus {i[0]}", i[1], 1.2)
        terror = Titles.Titles(f"Terror of the {i[0]}", f"Augmenta el dany causat contra enemics de tipus {i[0]}", i[1], 1.5)
        
        achievements.append(
            Exits.KillExit(f"{i[0]} Slayer", f"Derrota 10 entitats de tipus {i[0]}", i[1], 10, "Title", slayer)
        )
        achievements.append(
            Exits.KillExit(f"{i[0]} Anihilator", f"Derrota 50 entitats de tipus {i[0]}", i[1], 50, "Title", anihilator)
        )
        achievements.append(
            Exits.KillExit(f"Terror of the {i[0]}", f"Derrota 100 entitats de tipus {i[0]}", i[1], 100, "Title", terror)
        )

        titles.append(slayer)
        titles.append(anihilator)
        titles.append(terror)
CrearTitolsIKillExits()


missions = [
    # Missions.KillMission("Eliminant el Perill", 
    #                      "Un perillos golem que amenaça el poble, diuen que s'ha vist recentment per el Bosc Obscur.", 
    #                      "Principal",
    #                      [("XP", 3000), ("Gold", 10000), (objectes[15], 1)], 1, [entityTypes[10]], [("Lv", 35)], zones[3], False,
    #                      Entitat.Entity("El Golem de Roca", 40, False, entityTypes[10])),
]

# Afegir missions amb append, ja que si el requisit es una altre missio aquella ha d'estar ja definida.

    # Missions Principals
missions.append(
    Missions.PlaceMission(
        "La Primera Parada", 
        "Com a bon aventurer, vols començar el teu viatge, i la primera parada d'aquest és la ciutat dels caballers, Knightshire.", 
        "Principal",
        [("XP", 500), ("Gold", 3000), (objectes[2], 5)], zones[9], [("Lv", 5)]),
)

missions.append(
    Missions.KillMission(
        "Primera Petició", 
        "A Knightshire t'han demanat, en el gremi d'aventurers, que derrotis 5 conills cornuts, en els camps de Knioghtshire.", 
        "Principal", [("XP", 750), ("Gold", 3000), (objectes[2], 4)], 5, [entityTypes[26]], 
        [("Lv", 7), missions[0]], zones[12], True),
)

missions.append(
    Missions.PlaceMission(
        "Dirigeixte a Lakestar", 
        "Ves a la segona parada del teu viatge, Lakestar.", 
        "Principal",
        [("XP", 700), ("Gold", 3000), (objectes[2], 5)], zones[8], [("Lv", 9), missions[1]]),
)

missions.append(
    Missions.KillMission(
        "El Gran Cranc", 
        "A Lakestar decideixes començar una peticio del gremi d'aventurers, consisteix en eliminar a cert Cranc Aberrant... Se'l ha vist per la platja de Lakestar.", 
        "Principal", [("XP", 1250), ("Gold", 3500)], 1, [entityTypes[43]], 
        [("Lv", 12), missions[2]], zones[16], False, 
        Entitat.Entity("Cranc Aberrant Extrany", 12, False, entityTypes[43])),
)

missions.append(
    Missions.KillMission(
        "Eliminació de Bandits", 
        "A Lakestar decideixes començar una altre peticio del gremi d'aventurers, eliminar els bandits de les muntanyes estelars.", 
        "Principal", [("XP", 1000), ("Gold", 3500)], 4, [entityTypes[0], entityTypes[1], entityTypes[2], entityTypes[3]], 
        [("Lv", 14), missions[3]], zones[14], True),
)

missions.append(
    Missions.PlaceMission(
        "Un nou destí", 
        "Ves al Gran Bosc Lluminos, es diu que hi ha un antic poble amagat en aquest...", 
        "Principal",
        [("XP", 2000), ("Gold", 5000)], zones[7], [("Lv", 17), missions[4]]),
)

missions.append(
    Missions.KillMission(
        "La Gran Aranya", 
        "A Faylight et demanen que elimins una perillosa aranya que habita en el Gran Bosc Lluminos...", 
        "Principal", [("XP", 2500), ("Gold", 5000)], 1, [entityTypes[70]], 
        [("Lv", 20), missions[5]], zones[18], False, 
        Entitat.Entity("Gran Aranya", 22, False, entityTypes[70])),
)

missions.append(
    Missions.PlaceMission(
        "El poble platejat", 
        "Despres d'agrairte l'ajuda, en Faylight, has escoltat parlar d'un poble amagat en les muntanyes, un poble d'enans...", 
        "Principal",
        [("XP", 6000), ("Gold", 10000)], zones[6], [("Lv", 24), missions[6]]),
)

missions.append(
    Missions.KillMission(
        "Eliminació de Perills", 
        "A SIlverhorn et demanen que eliminis diverses amenaçes per el poble...", 
        "Principal", [("XP", 1000), ("Gold", 3500)], 10, 
        [entityTypes[7], entityTypes[31], entityTypes[33], entityTypes[34], entityTypes[35],
        entityTypes[36], entityTypes[37], entityTypes[44], entityTypes[45], entityTypes[47], 
        entityTypes[48], entityTypes[51], entityTypes[52], entityTypes[68], entityTypes[69],
        entityTypes[46], entityTypes[27]], 
        [("Lv", 27), missions[7]], zones[20], True),
)

missions.append(
    Missions.KillMission(
        "El Gran Gegant", 
        "A Silverhorn et donen una proba, si la superes et donaran un antic objecte del poble...", 
        "Principal", [("XP", 2500), ("Gold", 5000)], 1, [entityTypes[70]], 
        [("Lv", 30), missions[8]], zones[20], False, 
        Entitat.Entity("Gegant Daurat", 25, False, entityTypes[54])),
)

missions.append(
    Missions.PlaceMission(
        "Una vella historia sobre una Estrella", 
        "Escoltes d'una llegenda del poble, sobre una estrella enfonsant-se en un llac, diu la llegenda que en realitat aquesta estrella no es va efnfonsar sino que el va formar...", 
        "Principal",
        [("XP", 6000), ("Gold", 10000)], zones[21], [("Lv", 32), missions[9]]),
)

missions.append(
    Missions.PlaceMission(
        "Buscant una Estrella", 
        "Un cop confirmat que sota el llac existeix algo, decideixes busacr l'estrella...", 
        "Principal",
        [("XP", 9000), ("Gold", 10000)], zones[23], [("Lv", 34), missions[10]]),
)

missions.append(
    Missions.KillMission(
        "El Guardia del Origen", 
        "Escoltes d'una bestia sagrada en el lloc de l'estrella, que aquesta originalment hauria d'estar en les Muntanyes del Origen...\n" \
        "Derroyta al guardia perillos del que t'ha parlat i entra en les Cavernes del Origen, ubicades més enlla del Bosc Obscur.", 
        "Principal", [("XP", 15000), ("Gold", 25000)], 1, [entityTypes[70]], 
        [("Lv", 40), missions[11]], zones[4], False,
        Entitat.Entity("Eternitat", 40, False, entityTypes[62])),
)

missions.append(
    Missions.PlaceMission(
        "Pedra Misteriosa", 
        "Dins les cavernes despres de retornar la estrella al seu lloc d'origen, recibeixes una misteriosa pedra des del lloc on has retornat l'estrella...", 
        "Principal",
        [("XP", 20000), ("Gold", 30000)], zones[5], [("Lv", 44), missions[12]]),
)

    # Missions Secundaries

missions.append(
    Missions.KillMission(
        "Mostra de Confiança", 
        "Troba i elimina al Llop lider, diuen que s'ha vist recentment per el Bosc Obscur", 
        "Secundaria",
        [("XP", 120), ("Gold", 1000), (objectes[1], 1)], 1, [entityTypes[4]], [("Lv", 15)], zones[1], False,
        Entitat.Entity("Llop Lider", 17, False, entityTypes[4])),
)

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
        team[0].ObjectesMochila(team)
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
                        cost = ((len(contractatsAnteriorment)) + (len(team))) * 5000
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
                                    reclamar[aceptar - 1].Aceptar(team[0])
                                    team[0].MisionsAcceptades.append(reclamar[aceptar - 1])
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
                                    reclamar[aceptar - 1].ClaimedRewards(team)
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

def Posada(free = False):
    global team
    res = ""
    if free == False:
        while res not in ["S", "N"]:
            ClearScreen()
            try:
                res = input("\nVols descansar? Costa 100 gold (S / N): ").capitalize()
            except ValueError:
                print("Ha ocurregut un error...")
    if res == "S" or free == True:
        if team[0].gold >= 100 or free == True:
            print("Has descansat comodament, t'has recuperat completament...")
            if free == False:
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
        ubicacio = disponibles[pos - 1]    # Canviem la zona i la retornem
        for i in team[0].MisionsAcceptades:
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
        TrobarSeguentZona()
        
    ubicacio.ExplorarCount += 1
    rutaTrobada = False
    for i in ubicacio.Connections:
        if i.ZoneType == "Poble":
            if i.Trobada == False:
                i.Trobada = True
                print(f"Has trobat un cami a {i.NameZone}")
                rutaTrobada = True
        else:
            if ubicacio.ExplorarCount >= i.IntentsPerTrobar and i.Trobada != True:
                i.Trobada = True
                print(f"Has trobat un cami a {i.NameZone}")
                rutaTrobada = True
    if choice[0] != "missio" and prob < 70 or rutaTrobada == True:
        input("Presiona per a continuar...")
    
def TrobarSeguentZona():
    global team, ubicacio
    posiblesRutesATrobar = []
    rutesTrobades = []
    for i in ubicacio.Connections:
        complert = i.ComprobarCondicio(team)
        if complert == True and i.Trobada == False:
            posiblesRutesATrobar.append(i)
        if i.Trobada == True:
            rutesTrobades.append(i)
    if len(posiblesRutesATrobar) == 0:
        if len(rutesTrobades) == len(ubicacio.Connections):
            print("Ja has trobat totes les rutes en aquesta zona...")
        else:
            print("No sembla haber-hi cap altre ruta...")
    else:
        trobat = random.choice(ubicacio.Connections)
        print(f"Has trobat una ruta a {trobat.NameZone}.")
        trobat.Trobada = True
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
        used = team[0].ObjectesMochila(team, jug, True)
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
    for j in range(len(opcions)):
        if opcions[j] == seleccio[0]:
            prob = ubicacio.ProbOfMultiple[j]
    num = []
    count = 1
    for i in prob:
        num.append(count)
        count += 1
    qty = random.choices(num, prob)
    enemy = []

    enemy.append(Entitat.Entity("", random.randrange(ubicacio.LevelRange[0], ubicacio.LevelRange[1] + 1), False, seleccio[0]))

    probs = []
    opcionsPosib = []

    for v in seleccio[0].Companions.items():
        probs.append(v[1])
        opcionsPosib.append(v[0])


    if qty[0] > 1:
        for l in range(qty[0] - 1):
            if len(seleccio[0].Companions.keys()) >= 1:
                apareix = random.choices(opcionsPosib, probs)
            else:
                apareix = [seleccio[0]]
            entitat = Entitat.Entity("", random.randrange(ubicacio.LevelRange[0] - 2, enemy[0].Lv), False, apareix[0])
            enemy.append(entitat)
    
    Lluitar(enemy)

def ComprobarEfectEstat(entitat, derr):
    if entitat.afected != "None":
        if entitat.timer <= 0 and entitat.afected.Turns > 0:
            statsafected = entitat.afected.StatEffects[1][0]
            efectname = entitat.afected.Name
            entitat.afected = "None"
            entitat.BuffTempStats(0, statsafected)
            print(f"{entitat.nom}, ja no esta afectat per {efectname}, les seves estadistiques han retornat al que eren...")
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
            Comprovacions(p)
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
    while True:
        alive = 1
        while alive > 0:
            ClearScreen()
            AccioMenuPrincipal()
            alive = 0
            for i in team:
                if i.CurHP > 0:
                    alive += 1
        print(f"Has estat derrotat, t'han trobat i ara estas en la posada del ultim poble per el que has passat...")
        Posada(True)
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