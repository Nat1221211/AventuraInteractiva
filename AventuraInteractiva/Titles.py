# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe titles.

import random

class Titles():
    
    TitleName = ""
    Description = ""
    Afects = []
    DamageAmplify = float()
    


    # Metodes
    def __init__(self, name, description, afects, amplify):
        self.TitleName = name
        self.Description = description
        self.Afects = afects
        self.DamageAmplify = amplify