# Arxiu: AppWindow.py
# Autor: Bernat Puig Casals
# Data: 4 d'Abril de 2026
# Descripcio:
# Creem la classe App.

import tkinter as tk
from PIL import Image, ImageTk
import os

import PrepararCridar as Call

from Classes import Player
from Classes import Entitat
from Classes import Player
from Classes import Events

from Controladors import ControladorMissions
from Controladors import ControladorExits

filepath = os.path.dirname(__file__)

class App():
    
    # Metodes
    def __init__(self, player = Player.Player):
        self.root = tk.Tk()
        self.root.title = "RPG Python Game"


        # Declarar Logiques del Joc (Llistes Objectes i altres...)
        self.jugador = player
        Objects = Call.CallObject()
        Effects = Call.CallEfect()
        Movements = Call.CallMovement(Effects)
        Entities = Call.CallEntity(Movements)
        Zones = Call.CallZones()
        Achievements = Call.CallAchievements()

        # Declarem els events
        event = Events.ControladorEvents()

        event.NouEvent("Derrotar Enemic", ControladorMissions.sistemaMissionsDerrota)
        event.NouEvent("Lloc Visitat", ControladorMissions.sistemaMissionsVisita)
        event.NouEvent("Objecte Missio Trobat", ControladorMissions.sistemaMissionsObject)
        event.NouEvent("Persona Missio Trobada", ControladorMissions.sistemaMissionsFind)
        event.NouEvent("Missio Finalitzada", ControladorMissions.DesbloquejarMissio)
        event.NouEvent("Nivell Incrementat",  ControladorExits.sistemaExitsStatChange)

        # Missions
        Missions = Call.CallMissions(Entities)
        Missions["Place"]["first_adventure"].Status = "Disponible"


        # Midas pantalla
        self.Alto = 600 # Declarem mides en variables per a utilitzarles facilment.
        self.Ancho = 900

        self.root.geometry(f"{self.Ancho}x{self.Alto}") # Declarem les mides de la finestra
        self.root.resizable(False, False)   # Aixi no podra canviar de mida la finestra

        imageroute = os.path.join(filepath, "Assets/Backgrounds/Window/TitleBackground.png") 
        if not os.path.exists(imageroute):
            self.root.destroy()
            return

        self.ImatgeFons = Image.open(imageroute)

        # Creem el canvas de la finestra
        self.canvas = tk.Canvas(self.root, width=self.Ancho, height=self.Alto)
        self.canvas.pack(fill="both", expand=True)

        self.fondo = None

        self.MostrarPantallaInicial()

    def RedimensionarFons(self):

        # Redimensionem a la mida de la pantalla, i li donem format LANCZOS (de bona qualitat)
        redim_image = self.ImatgeFons.resize(
            (self.Ancho, self.Alto), Image.Resampling.LANCZOS
        )

        # Convertim a format compatible
        self.fondo = ImageTk.PhotoImage(redim_image)

        # Posicionem la imatge en la finestra
        self.canvas.create_image(0, 0, image=self.fondo, anchor="nw", tags="fondo")

    
    def MostrarPantallaInicial(self):
        self.RedimensionarFons()

        # Mostrar Titol
        titol = tk.Label(self.root, text="RPG Python Game", font=("Helvetica", 32, "bold"),
                         fg="white", bg="black")
        
        self.canvas.create_window(self.Ancho // 2, self.Alto // 6, window=titol)

        # Instruccions per a avançar de finestra
        instruccions = tk.Label(self.root, text="Pulsa qualquier boton o la ventana...", font=("Arial", 32, "bold"),
                         fg="white", bg="black")
        
        self.canvas.create_window(self.Ancho // 2, self.Alto - self.Alto // 6, window=instruccions)
    
        # Interaccions
        
        # Clic Ratoli
        self.canvas.bind("<Button-1>", lambda event: self.MostrarPantallaSeleccio())

        # Cualsevol tecla en la finestra root, ja que qui escolta les tecles es la finestra no la imatge de fons...
        self.root.bind("<Key>", lambda event: self.MostrarPantallaSeleccio())

        # Donar acces al canvas a escoltar les pulsacions de les tecles
        self.canvas.focus_set()

    def MostrarPantallaSeleccio(self):
        # Desanclem les tecles declarades en la finestra anterior.
        self.canvas.unbind("<Button-1>")
        self.root.unbind("<Key>")

        self.canvas.delete("all") # Borrem el que tingues el canvas

        self.RedimensionarFons()

         # Mostrar Titol
        titol = tk.Label(self.root, text="Seleccionar Partida", font=("Helvetica", 32, "bold"),
                         fg="white", bg="black")
        
        self.canvas.create_window(self.Ancho // 2, self.Alto // 6, window=titol)

        # Creem els botons

        posicio = (self.Ancho // 2, self.Alto - self.Alto // 6)

        ruta_base = os.path.dirname(__file__)
        ruta = os.path.join(ruta_base, "Saves/save.json")
        if os.path.isfile(ruta):
            carregar = tk.Button(self.root, text="Carregar Partida", font=("Helvetica", 18), command="")
            self.canvas.create_window(posicio[0], posicio[1], window=carregar)
            posicio = (self.Ancho // 2, self.Alto - (self.Alto // 6)*2)

        novaPartida = tk.Button(self.root, text="Carregar Partida", font=("Helvetica", 18), command="")
        self.canvas.create_window(posicio[0], posicio[1], window=novaPartida)


    def NovaPartida(self):
        # Cridem la funcio per crear el jugador, la variable ubicacio, i la variable de diccionari amb els grups i les seves entitats
        personatge = self.jugador.CrearJugador(True)
        ubicacio = self.Zones["dawn_village"]
        team = {}
        team.update({"Player": personatge})

        jugador = Player.Player(personatge.nom, team, ubicacio)

        # # Afegim algun objecte al jugador de base
        jugador.AfegirObjecte(self.Objects["Combat"]["inferior_potion"], 2)