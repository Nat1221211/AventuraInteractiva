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
                        linia[j] = bool(linia[j])
                    elif linia[j].isnumeric():
                        linia[j] = int(linia[j])
                    elif len(linia[j].split(": ")) > 1:
                        items = linia[j].split(", ").copy()
                        linia[j] = dict()
                        for v in items:
                            kv = v.split(": ")
                            linia[j][kv[0]] = float(kv[1]) if not kv[1].endswith("%") else kv[1]
                    elif len(linia[j].split(", ")) > 1:
                        linia[j] = linia[j].split(", ")
                    DictData[caps[j]] = linia[j]
                Data.append(DictData.copy())
            print(Data)


    except FileNotFoundError:
        print("Ha ocurregut un error carregant el fitxer...")


def main():
    print("!! - Joc de Preguntes - !!")
    print("Entitats")
    CallCSV("Data/EntityTypes.csv")
    print("\n\n\nMoviments")
    CallCSV("Data/Movements.csv")
    print("\n\n\nEfectes")
    CallCSV("Data/effects.csv")
    print("\n\n\nObjectes")
    CallCSV("Data/Objects.csv")

if __name__ == "__main__":
    main()