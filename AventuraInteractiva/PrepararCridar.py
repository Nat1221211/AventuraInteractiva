# Arxiu: PrepararCridar.py
# Autor: Bernat Puig Casals
# Data: 2 de Febrer de 2026
# Descripcio:
# Creem el modul per a crear o cridar els valors dels documents quan siguin necessaris.


# Altres Imports
import os

# Moduls
from Classes import Characteristics
from Classes import Entitat
from Classes import EntityType
from Classes import Exits
from Classes import Missions
from Classes import Objectes
from Classes import Titles
from Classes import Zones

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

def CallEntity(trobar, isPlayer = False):
    entities = CallCSV("Data/EntityTypes.csv")
    llista = []
    for i in entities:
        if i["Nom"] == trobar or isPlayer == True and i["Playable?"] == True:

            moves = {}
            for m, n in i["Movements"].items():
                moves[CallMovement(m)]=n

            entitat = EntityType.EntityType(i["Nom"],  i["Playable?"], i["Vida"], i["Mana"], i["ATK"], i["INT"], 
                                  i["DEF"], i["SPD"], i["XP"], i["Groups"],  i["Descripcio"], moves)
            if isPlayer == True:
                llista.append(entitat)
    if isPlayer == True:
        return llista
    else:
        return entitat

def CallEfect(trobar):
    effects = CallCSV("Data/effects.csv")
    for i in effects:
        if i["Nom"] == trobar:
            if i["ImpedeixAccions?"] == True:
                bloqueig = (i["ImpedeixAccions?"], i["ProbabilitatImpedirAccio"])
            else:
                bloqueig = (False, 0)
            entitat = Characteristics.Effects(i["Nom"],  i["Descripcio"], bloqueig, i["Duracio"], i["Dany"],
                                              i["StatAfected"])
    return entitat

def CallMovement(trobar):
    movements = CallCSV("Data/Movements.csv")
    for i in movements:
        if i["Nom"] == trobar:
            Buff = {}
            if len(i["Buff"]) > 1 and i["Buff"] == list:
                for j in range(len(i["Buff"])):
                    Buff[i["Buff"][j]]=i["ProbEfecteBuff"][j]
            else:
                Buff[i["Buff"]]=i["ProbEfecteBuff"]

            Debuff = {}
            if len(i["Debuff"]) > 1 and i["Debuff"] == list:
                for j in range(len(i["Debuff"])):
                    Debuff[i["Debuff"][j]]=i["ProbEfecteDebuff"][j]
            else:
                Debuff[i["Debuff"]]=i["ProbEfecteDebuff"]
            move = Characteristics.Moves(i["Nom"], i["Descripcio"], i["Potencia"], i["Precisio"],  i["Magic?"], 
                                            i["Cost"], Buff, Debuff, i["MultipleObjectiu?"], i["Cura?"], i["Protegeix?"], i["DanyperProteccio"])
    return move

def CallObject(trobar):
    objects = CallCSV("Data/Objects.csv")
    for i in objects:
       if i["Nom"] == trobar:
            if i["Tipus"] == "Combat":
                obj = Objectes.ObjecteCombat(i["Nom"], i["Descripcio"], i[""], i[""],  i[""], i[""])
            elif i["Tipus"] == "Clau":
                obj = Objectes.ObjecteClau(i["Nom"], i["Descripcio"])
    return obj

def main():
    print("!! - Joc de Preguntes - !!")
    

if __name__ == "__main__":
    main()