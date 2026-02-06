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

def CallMove(trobar):
    try:
        base_path = os.path.dirname(__file__)
        ruta = os.path.join(base_path, "Data", "Movements.csv")
        with open(ruta, "r", encoding="utf-8") as moves:
            for move in moves:
                moveFields = move.strip().slice()
                if moveFields[0] == trobar:
                    
    except ValueError:
        print("Ha ocurregut un error carregant els moviments...")


def main():
    print("!! - Joc de Preguntes - !!")

if __name__ == "__main__":
    main()