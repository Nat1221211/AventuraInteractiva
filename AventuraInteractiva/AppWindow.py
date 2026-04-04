# Arxiu: AppWindow.py
# Autor: Bernat Puig Casals
# Data: 4 d'Abril de 2026
# Descripcio:
# Creem la classe App.

import tkinter as tk
from PIL import Image, ImageTk
import os

import PrepararCridar as Call
import SaveGame
import UIManager


from Classes import Player
from Classes import Entitat
from Classes import Player
from Classes import Events
from Classes import Utilitats

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
        self.Objects = Call.CallObject()
        self.Effects = Call.CallEfect()
        self.Movements = Call.CallMovement(self.Effects)
        self.Entities = Call.CallEntity(self.Movements)
        self.Zones = Call.CallZones()
        self.Achievements = Call.CallAchievements()

        # Declarem els events
        self.event = Events.ControladorEvents()

        self.event.NouEvent("Derrotar Enemic", ControladorMissions.sistemaMissionsDerrota)
        self.event.NouEvent("Lloc Visitat", ControladorMissions.sistemaMissionsVisita)
        self.event.NouEvent("Objecte Missio Trobat", ControladorMissions.sistemaMissionsObject)
        self.event.NouEvent("Persona Missio Trobada", ControladorMissions.sistemaMissionsFind)
        self.event.NouEvent("Missio Finalitzada", ControladorMissions.DesbloquejarMissio)
        self.event.NouEvent("Nivell Incrementat",  ControladorExits.sistemaExitsStatChange)

        # Missions
        self.Missions = Call.CallMissions(self.Entities)
        self.Missions["Place"]["first_adventure"].Status = "Disponible"


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

        self.Menu = Utilitats.Menu(self, self.canvas, "", [])

        self.MostrarPantallaInicial()
    
    def ConfirmarSeleccio(self, event = None):
        if self.Menu.id == "Seleccio Partida":    # Segons la opcio i l'objecte dur a terme una accio
            self.SeleccionarPartida()
    
    def CanviarMenu(self, menu):
        self.Menu = Utilitats.Menu(self, self.canvas, menu["id"], menu["opcions"])

    def MostrarMenu(self):
        self.Menu.dibuixar()

    def RedimensionarFons(self, image = None):

        if image != None:
            if os.path.exists(image):
                self.ImatgeFons = Image.open(image)
        
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

        ruta_base = os.path.dirname(__file__)
        ruta = os.path.join(ruta_base, "Saves/save.json")
        if os.path.isfile(ruta):
            UIManager.Menus["Seleccio Partida"]["opcions"].append(
                Utilitats.OpcioMenu("Carregar", "Carregar Partida", True, "Carrega la ultima partida guardada..."),
            )

         # Interaccions
        self.root.bind("<w>", lambda event: self.Menu.Moviment("w"))
        self.root.bind("<s>", lambda event: self.Menu.Moviment("s"))
        # self.root.bind("<a>", lambda event: self.MostrarPantallaSeleccio())
        # self.root.bind("<d>", lambda event: self.MostrarPantallaSeleccio())
        self.root.bind("<Return>", lambda event: self.ConfirmarSeleccio())
        self.root.bind("<BackSpace>", lambda event: self.ConfirmarSeleccio())

        
        self.CanviarMenu(UIManager.Menus["Seleccio Partida"])
        self.MostrarMenu()
        

    def SeleccionarPartida(self):
        seleccionat = self.Menu.opcions[self.Menu.index]
        if seleccionat.id == "Nova":
            self.NovaPartida()
        elif seleccionat.id == "Carregar":
            ruta_base = os.path.dirname(__file__)
            ruta = os.path.join(ruta_base, "Saves/save.json")
            self.CarregarPartida(ruta)
        
        if seleccionat.id != None:
            UIManager.MostrarMenuPrincipal(self)

    def NovaPartida(self):
        # Cridem la funcio per crear el jugador, la variable ubicacio, i la variable de diccionari amb els grups i les seves entitats
        personatge = self.CrearJugador(True)
        ubicacio = self.Zones["dawn_village"]
        team = {}
        team.update({"Player": personatge})

        self.jugador = Player.Player(personatge.nom, team, ubicacio)

        # # Afegim algun objecte al jugador de base
        self.jugador.AfegirObjecte(self.Objects["Combat"]["inferior_potion"], 2)
        UIManager.MostrarMenuPrincipal(self)
    
    def CrearJugador(self, first = False):
        nom = ""
        while nom == "":
            try:
                nom = "Nat" # Canviar per a demanar
            except ValueError:
                print("Ha ocurregut un error...")
        
        # UIManager.CrearMenu(self.Entities.items(), "Menu Seleccio Inicial", ("Tipus Entitat", "Playable"))
        # identifier = None
        # while identifier == None:
        #     identifier = UIManager.MostrarMenus(UIManager.Menus["Menu Seleccio Inicial"], False)
        #     if identifier == None:
        #         print("Has de seleccionar una de les opcions")
        if first == True:
            id = "Player"
        else:
            id = f"ally_{len(self.jugador.Team)}"
        playableentity = Entitat.Entity(id, nom, 5, True, self.Entities["mage"])

        return playableentity
    
    def CarregarPartida(self, partida):
        self.jugador = SaveGame.CarregarPartida(partida, self.Missions, self.Objects, self.Zones, self.Entities)
        UIManager.MostrarMenuPrincipal(self)

    def GuardarPartida(self):
        SaveGame.GuardarPartida(self.jugador, self.Missions)

        