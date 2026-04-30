# Arxiu: AppWindow.py
# Autor: Bernat Puig Casals
# Data: 4 d'Abril de 2026
# Descripcio:
# Creem la classe App.

import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
import os

import PrepararCridar as Call
import SaveGame
import UIManager
import AdventureManager
import TownUtilitiesManager as TUtManager
import CombatManager


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
    def __init__(self):
        self.root = tk.Tk()
        self.root.title = "RPG Python Game"


        # Declarar Logiques del Joc (Llistes Objectes i altres...)
        self.jugador = Player.Player("Nat", {}, "")
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

        # ALtres
        self.DialegActiu = False
        self.Confirmacio = False
        self.QuinaConfirmacio = ""
        self.MostrarEstat = False
        self.Motxila = False
        self.SubMenu = False
        self.ActiveSubMenu = ""
        self.SeleccioAliat = False
        self.UltimObjecteSeleccionat = None
        self.RecuperantVida = False
        self.MenuExits = False

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
        self.MenuCombat = CombatManager.MenuCombat
        self.Combat = False

        self.MostrarPantallaInicial()
    
    def ConfirmarSeleccio(self, event = None):
        if self.Combat == False:
            if self.Menu.id not in ["Motxila"]:
                seleccionat = self.Menu.opcions[self.Menu.index]
        
            if self.Menu.id == "Seleccio Partida":    # Segons la opcio i l'objecte dur a terme una accio
                self.SeleccionarPartida()

            elif self.Menu.id == "Motxila":
                if self.Menu.llistaobjectes[self.Menu.index].id != "sortir":
                    seleccionat = self.Menu.llistaobjectes[self.Menu.index].Objecte["objecte"]
                    self.Motxila = False
                    self.UltimObjecteSeleccionat = seleccionat
                    UIManager.VeureEstatus(self, False)
                
                else:
                    self.Motxila = False
                    UIManager.MostrarMenuPrincipal(self)
                
            elif self.Menu.id == "Confirmacio":
                self.Confirmacio = False
                if  self.QuinaConfirmacio == "Guardar":
                    if seleccionat.id == "si":
                        SaveGame.GuardarPartida(self, self.jugador, self.Missions)
                    elif seleccionat.id == "no":
                        self.Menu.CrearDialeg("Has decidit no guardar la partida...")
                
                elif  self.QuinaConfirmacio == "Hostal":
                    if seleccionat.id == "si":
                        TUtManager.Posada(self)
                    elif seleccionat.id == "no":
                        self.Menu.CrearDialeg("Has decidit no quedar-te al hostal...")
            
            elif self.Menu.id == "Seleccio Equip":
                if self.SeleccioAliat == True:
                    self.SeleccioAliat = False
                    if seleccionat.id == "sortir":
                        if self.Menu.MenuAnterior.id == "Motxila":
                            self.Motxila = True
                            self.MenuMotxila()
                        else:
                            self.Enrere()
                    elif self.Menu.MenuAnterior.id == "Motxila":
                        if seleccionat.id == "sortir":
                            self.Motxila = True
                            self.Enrere()
                        else:
                            self.Motxila = True
                            self.UltimObjecteSeleccionat.Utilitzar(self, seleccionat)
                    else:
                        self.Menu.mostrar_estat_equip()
                

            elif self.Menu.id == "Seleccio Entitats":
                self.CrearEntitatAliada(seleccionat)

            elif self.Menu.id == "Menu Poble" or self.Menu.id == "Menu Wild":
                UIManager.CridarAccioMenuPrincipal(self, seleccionat)
            
            elif self.Menu.id == "Mapa":
                AdventureManager.CanviarZona(self, seleccionat)
        else:
            self.ConfirmarSeleccioCombat(event)
    
    def ConfirmarSeleccioCombat(self, event = None):
        if self.MenuCombat.AccioAliat == True:
            seleccio = self.MenuCombat.AccionsCombat[self.MenuCombat.IndexAccio]
            
         
    def Enrere(self):
        self.Menu = self.Menu.MenuAnterior
        self.MostrarMenu()

    def CanviarMenu(self, menu, x = 300, y = 50):
        menuAnterior = self.Menu
        self.Menu = Utilitats.Menu(self, self.canvas, menu["id"], menu["opcions"], x, y)

        self.Menu.MenuAnterior = menuAnterior

    def MostrarMenu(self):
        self.canvas.delete("all")
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
        self.canvas.tag_lower("fondo")
    
    def RedimensionarImatge(self, imatge, x, y, borros=False, scale = None):

        if imatge != None:
            if os.path.exists(imatge):
                image = Image.open(imatge)
                    
                if borros == True:
                    image.filter(ImageFilter.GaussianBlur(radius=15))

                if scale != None:
                    x = image.height // scale
                    y = image.width // scale

                    # Redimensionem a la mida de la pantalla, i li donem format LANCZOS (de bona qualitat)
                redim_image = image.resize(
                    (x, y), Image.Resampling.LANCZOS
                )

                
                # Convertim a format compatible
                imatge_redimensionada = ImageTk.PhotoImage(redim_image)

                return imatge_redimensionada
                # En acabar el return encara cal crear la imatge al canvas i colocar-la...

            else:
                print("No s'ha trobat la imatge")
    
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

        ruta = os.path.join(filepath, "Saves/save.json")
        if os.path.isfile(ruta):
            UIManager.Menus["Seleccio Partida"]["opcions"].insert(1,
                Utilitats.OpcioMenu("Carregar", "Carregar Partida", True, "Carrega la ultima partida guardada..."),
            )

         # Interaccions
        self.root.bind("<w>", self.ControlBinds)
        self.root.bind("<s>", self.ControlBinds)
        self.root.bind("<a>", self.ControlBinds)
        self.root.bind("<d>", self.ControlBinds)
        self.root.bind("<Return>", self.ControlBinds)
        self.root.bind("<BackSpace>", self.ControlBinds)

        
        self.CanviarMenu(UIManager.Menus["Seleccio Partida"])
        self.MostrarMenu()
    
    def ControlBinds(self, tecla):
        if self.Combat == True:
            self.MenuCombat.MovimentAccions(tecla.keysym)
        else:
            self.ControlBindsMenus(tecla)

    def ControlBindsMenus(self, tecla):
        if self.DialegActiu == True:
            if tecla.keysym == "Return":
                self.Menu.PulsarEnter()
            if tecla.keysym == "BackSpace": 
                self.Menu.PulsarEnter()
        
        elif self.SeleccioAliat == True:
            if tecla.keysym == "w": self.Menu.Moviment("w")
            if tecla.keysym == "s": self.Menu.Moviment("s")
            if tecla.keysym == "Return": self.ConfirmarSeleccio()
            if tecla.keysym == "BackSpace":
                if self.Menu.healthanimation == None:
                    if self.Menu.id not in ["Menu Wild", "Menu Poble", "Seleccio Partida", "Seleccio Entitats"]:
                        self.SeleccioAliat = False
                        if self.Menu.MenuAnterior.id == "Motxila":
                            self.Motxila = True
                            self.MenuMotxila()
                        else:
                            self.Enrere()
        
        elif self.MenuExits == True:
            if tecla.keysym == "w": self.Menu.Moviment("w")
            if tecla.keysym == "s": self.Menu.Moviment("s")
            if tecla.keysym == "a": self.Menu.Moviment("a")
            if tecla.keysym == "d": self.Menu.Moviment("d")
            if tecla.keysym == "BackSpace":
                self.MenuExits = False
                UIManager.MostrarMenuPrincipal(self)

        elif self.MostrarEstat == True:
            if tecla.keysym == "w": self.Menu.Moviment("w")
            if tecla.keysym == "s": self.Menu.Moviment("s")
            # if tecla.keysym == "a": self.Menu.Moviment("a")
            # if tecla.keysym == "d": self.Menu.Moviment("d")
            if tecla.keysym == "BackSpace":
                self.MostrarEstat = False
                self.Menu.dibuixar_menu_equip()

        elif self.Menu.PantallaEscriure == True:
            self.Menu.TeclatEscritura(tecla)

        elif self.Motxila == True:
            if tecla.keysym == "w": self.Menu.Moviment("w")
            if tecla.keysym == "s": self.Menu.Moviment("s")
            if tecla.keysym == "a": self.Menu.Moviment("a")
            if tecla.keysym == "d": self.Menu.Moviment("d")
            if tecla.keysym == "Return": self.ConfirmarSeleccio()
            if tecla.keysym == "BackSpace":
                self.Motxila = False
                UIManager.MostrarMenuPrincipal(self)
        
        else:
            if tecla.keysym == "w": self.Menu.Moviment("w")
            if tecla.keysym == "s": self.Menu.Moviment("s")
            if tecla.keysym == "a": self.Menu.Moviment("a")
            if tecla.keysym == "d": self.Menu.Moviment("d")
            if tecla.keysym == "Return": self.ConfirmarSeleccio()
            if tecla.keysym == "BackSpace":
                if self.Menu.id not in ["Menu Wild", "Menu Poble", "Seleccio Partida", "Seleccio Entitats"]:
                    self.Enrere()


    def SeleccionarPartida(self):
        seleccionat = self.Menu.opcions[self.Menu.index]
        if seleccionat.id == "Nova":
            self.NovaPartida()
        elif seleccionat.id == "Carregar":
            ruta_base = os.path.dirname(__file__)
            ruta = os.path.join(ruta_base, "Saves/save.json")
            self.CarregarPartida(ruta)
            UIManager.MostrarMenuPrincipal(self)
        elif seleccionat.id == "sortir":
            self.TancarJoc()

    def TancarJoc(self):
        self.root.quit()

    def NovaPartida(self):
        self.SeleccioText("Com et dius?")

    def SeleccionarEntitat(self):

        UIManager.CrearMenu(self.Entities.items(), "Seleccio Entitats", ("Tipus Entitat", "Playable"))
        self.CanviarMenu(UIManager.Menus["Seleccio Entitats"])
        self.Menu.dibuixar_menus_seleccio_entitats()

    def SeleccioText(self, textMostrar):
        self.Menu.dibuixar_pantalla_menu_text(textMostrar)

    def CrearEntitatAliada(self, id_entitat):
        if len(self.jugador.Team) < 1:
            id = "Player"
            self.jugador.Name = self.NomEntitat
            nom = self.jugador.Name
        else:
            id = f"ally_{len(self.jugador.Team)}"
            nom = self.NomEntitat
        playableentity = Entitat.Entity(id, nom, 5, True, self.Entities[id_entitat.id])

        self.jugador.Team.update({id: playableentity})
        self.jugador.Ubicacio = self.Zones["dawn_village"]
        self.jugador.UltimPobleVisitat = self.Zones["dawn_village"]
        self.Menu.SeleccioEntitats = False

        UIManager.MostrarMenuPrincipal(self)

    
    def CarregarPartida(self, partida):
        self.jugador = SaveGame.CarregarPartida(partida, self.Missions, self.Objects, self.Zones, self.Entities)
        UIManager.MostrarMenuPrincipal(self)

    def GuardarPartida(self):
        self.QuinaConfirmacio = "Guardar"
        self.MenuConfirmacio("Vols Guardar la Partida?\nFer-ho sobrescriura la ultima partida guardada...")
    

    def PrepararExplorar(self):
        self.canvas.delete("all")
        self.RedimensionarFons()
    
    def MenuConfirmacio(self, dialeg = None):
        self.Confirmacio = True
        self.CanviarMenu(UIManager.Menus["Confirmacio"], 60, self.Alto - 265)
        self.Menu.CrearDialeg(dialeg)

    def MenuMotxila(self):
        self.Motxila = True
        UIManager.CrearMenu(self.jugador.objectes.items(), "Motxila", "Objectes")
        self.CanviarMenu(UIManager.Menus["Motxila"])
        self.Menu.DibuixarMenuMotxila()