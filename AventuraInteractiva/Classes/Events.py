# Arxiu: Events.py
# Autor: Bernat Puig Casals
# Data: 5 de Març de 2026
# Descripcio:
# Creem la classe events.

import random

class ControladorEvents():
    
    # Metodes
    def __init__(self):
        self.Events = {} # Clau: Event, Valor: Llista d'Acció (Funció)
    
    def NouEvent(self, event, accio):
        if event in self.Events.keys():
            self.Events[event].append(accio)
        else:
            self.Events[event] = [accio]
    
    def CridarEvent(self, event, dades, app):
        if event in self.Events.keys():
            for accio in self.Events[event]:
                accio(dades, app)
