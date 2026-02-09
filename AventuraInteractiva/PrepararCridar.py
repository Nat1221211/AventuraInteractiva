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
            caps = data[0].strip().replace(" ", "").split(";")

            Data = []
            DictData = {}
            for i in data[1:]:
                linia = i.strip().replace(" ", "").split(";")
                for j in range(len(linia) -1):
                    
                    DictData[caps[j]] = linia[j]
                Data.append(DictData.copy())
            print(Data)


    except ValueError:
        print("Ha ocurregut un error carregant els moviments...")


def main():
    print("!! - Joc de Preguntes - !!")
    CallCSV("Data/Objects.csv")

if __name__ == "__main__":
    main()