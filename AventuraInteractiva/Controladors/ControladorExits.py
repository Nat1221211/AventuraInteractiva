# Arxiu: PrepararCridar.py
# Autor: Bernat Puig Casals
# Data: 5 de Març de 2026
# Descripcio:
# Creem el modul per a fer accions relacionades amb les missions.

import os
import random

def sistemaExitsDerrota(enemic, jugador, achievements):
    for id, value in achievements.items():
        if id in achievements.keys():
            print()


def sistemaExitsStatChange(personatge, jugador, achievements):
    for id, value in achievements.items():
        if value["achievement"].UnlockRequirements["Type"] != "Stat" or id in jugador.AcquiredAchievements:
            continue
        else:
            value["achievement"].ComprovarExit(personatge, jugador)


