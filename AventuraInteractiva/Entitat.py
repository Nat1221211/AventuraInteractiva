# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe entitat.

import random
import EntityType
import Objectes

import os

class Entity():
    
    nom = ""
    base = EntityType.EntityType

    # Level
    Lv = int()
    LvLimit = int()

    # Stats
    MaxHP = int()
    CurHP = int()
    MaxMana = int()
    Mana = int() 
    ATK = int()
    INT = int()
    DEF = int()
    SPD = int()

    # Characteristics
    Moves = list()
    subclass = None
    subAcquirable = False

    # temp stats / effects
    tempATK = int()
    tempINT = int()
    tempDEF = int()
    tempSPD = int()
    buffATK = 1
    buffINT = 1
    buffSPD = 1
    buffDEF = 1

    # Combat Priority Variables
    Priority = int()
    Protected = False
    ProtectedBy = tuple()
    afected = ""
    timer = 0

    # Xp
    Xp = 0
    XpRequired = 14

    # Other
    isPlayer = bool()
    gold = 0
    objectes = {} # Diccionari, objecte i quantitat
    fleeProb = 75
    Tituls = []
    AcquiredAchievements = []
    MisionsAcceptades = []
    MissionsFinalitzades = []
    PostGame = False

    # Metodes
    def __init__(self, nom, level, IsPlayer, BaseEntity, limit = 100, objectes = {}, gold = 10, subclass = None, paths = None, post = False):
        self.nom = nom
        self.Lv = level
        self.isPlayer = IsPlayer
        self.LvLimit = limit
        self.base = BaseEntity
        self.Moves = list()
        self.DefinirStats()
        self.CurHP = self.MaxHP
        if IsPlayer == False:
            if nom == "":
                self.nom = self.base.EntityName
            self.gold = gold
        self.objectes = objectes
        self.PostGame = post
        self.afected = "None"
        self.subclass = subclass
        self.paths = paths
    
    def ComprovarSubClassesDisponibles(self):
        for i in self.base.paths.items():
            req = True
            for j in i[1][0]:
                if j[0] == "Lv" and self.Lv < j[1]:
                    req = False
                elif j[0] == "Stat":
                    for s in j[1]:
                        if s[0] == "Mana" and self.MaxMana < s[1]:
                            req = False
                        elif s[0] == "Health" and self.MaxHP < s[1]:
                            req = False
                        elif s[0] == "Attack" and self.ATK < s[1]:
                            req = False
                        elif s[0] == "Int" and self.INT < s[1]:
                            req = False
                        elif s[0] == "Defense" and self.DEF < s[1]:
                            req = False
                        elif s[0] == "Speed" and self.SPD < s[1]:
                            req = False
                elif j[0] == "Éxit":
                    if j[1] not in self.AcquiredAchievements:
                        req = False
            if req == True:
                self.base.paths[i[0]][1] = True
                if self.subAcquirable == False and self.subclass == None:
                    self.subAcquirable = True

    def DefinirSubClass(self):
        disponible = []
        for j in self.base.paths.items():
            if j[1][1] == True:
                disponible.append(j[0])
        count = 1
        sel = 0
        while sel < 1:
            os.system("cls" if os.name == "nt" else "clear")
            print(" - Tria la teva Segona Classe - ")
            print("No totes les opcions que existeixen poden ser seleccionables..." \
            "Només és mostren les que es compleixen els requisits...")
            print()
            for i in disponible:
                print(f"{count} -> {i.EntityName}")
                print(f"{i.EntityDescription}\n")
                count += 1
            print(f"{count} -> Sortir\n")
            try:
                sel = int(input(f"Digues quina Segona Classe Vols: "))
                if sel not in range(1, count + 2):
                    print("Has de dir un dels numeros segons la segona classe que vols...")
            except ValueError:
                print("Ha ocurregut un error...")
        if sel == count:
            print("Has sortit del menu de seleccio de subclasse...")
            print("Pots tornar a accedir-hi desde el menu d'estat...")
            input("Presiona per a continuar...")
        else:
            self.subclass = disponible[sel - 1]
            self.subAcquirable = False
            self.DefinirStats(True)


        
    def DefinirMoves(self):
        for i in self.base.EntityMoves.items():
            if i[1] <= self.Lv and i[0] not in self.Moves:
                self.Moves.append(i[0])
        if self.subclass != None:
            for i in self.subclass.EntityMoves.items():
                if i[1] <= self.Lv and i[0] not in self.Moves:
                    self.Moves.append(i[0])

    def DefinirStats(self,LvOrNot = False):
        baseHealth = self.base.Health / 50
        baseMagic = self.base.Magic / 50
        baseAttack = self.base.Attack / 50
        baseIntel = self.base.Intel / 50
        baseDefense = self.base.Defense / 50
        baseSpeed = self.base.Speed / 50
        
        if self.subclass != None:
            baseHealth += self.subclass.Health / 100
            baseMagic += self.subclass.Magic / 100
            baseAttack += self.subclass.Attack / 100
            baseIntel += self.subclass.Intel / 100
            baseDefense += self.subclass.Defense / 100
            baseSpeed += self.subclass.Speed / 100            

        self.MaxHP = 10 + (baseHealth * self.Lv)
        self.MaxMana = 10 + (baseMagic * self.Lv)
        self.ATK = 10 + (baseAttack * self.Lv)
        self.INT = 10 + (baseIntel * self.Lv)
        self.DEF = 10 + (baseDefense * self.Lv)
        self.SPD = 10 + (baseSpeed * self.Lv)
        if LvOrNot == False:
            self.CurHP = self.MaxHP
            self.Mana = self.MaxMana
            self.XpRequired = float(round(self.XpRequired + 5 * (self.Lv ** 1.2), 2))
        self.DefinirTempStats()
        self.DefinirMoves()
        self.afected = "None"
    
    def DefinirTempStats(self):
        self.tempATK = self.ATK
        self.tempINT = self.INT
        self.tempDEF = self.DEF
        self.tempSPD = self.SPD
    
    def BuffTempStats(self, buff, statbuffed):
        self.DefinirTempStats()
        basebuff = buff
        for i in statbuffed:
            buff = basebuff
            if buff >= 1:
                buff -= 1
                print(f"La estadistica {i} de {self.nom} s'ha incrementat en {abs(buff * 100)}%")
            else:
                buff = -(abs(buff))
                print(f"La estadistica {i} de {self.nom} s'ha reduit en {abs(buff * 100)}%")
            if i == "ATK":
                self.buffATK += buff
                if self.buffATK < 0.5:
                    self.buffATK = 0.5
                elif self.buffATK > 4:
                    self.buffATK = 4
                self.tempATK *= self.buffATK
            if i == "INT":
                self.buffINT += buff
                if self.buffINT < 0.5:
                    self.buffINT = 0.5
                elif self.buffINT > 4:
                    self.buffINT = 4
                self.tempINT *= self.buffINT
            if i == "SPD":
                self.buffSPD += buff
                if self.buffSPD < 0.5:
                    self.buffSPD = 0.5
                elif self.buffSPD > 4:
                    self.buffSPD = 4
                self.tempSPD *= self.buffSPD
            if i == "DEF":
                self.buffDEF += buff
                if self.buffDEF < 0.5:
                    self.buffDEF = 0.5
                elif self.buffDEF > 4:
                    self.buffDEF = 4
                self.tempDEF *= self.buffDEF
        if self.afected != "None":
            self.StatusEffectStatReduction()
    
    def ResetBuffs(self):
        self.buffATK = 1
        self.buffINT = 1
        self.buffSPD = 1
        self.buffDEF = 1
    
    def StatusEffectStatReduction(self):
        if self.afected.StatEffects[0] != "None":
            for i in self.afected.StatEffects[1][0]:
                if i == "ATK":
                    self.tempATK *= (1 - self.afected.StatEffects[1][1])
                if i == "INT":
                    self.tempINT *= (1 - self.afected.StatEffects[1][1])
                if i == "SPD":
                    self.tempSPD *= (1 - self.afected.StatEffects[1][1])
                if i == "DEF":
                    self.tempDEF *= (1 - self.afected.StatEffects[1][1])
                print(f"La estadistica {i} de {self.nom} s'ha reduit en {abs(self.afected.StatEffects[1][1] * 100)}%")
    
    
    def ApplyStatusEffects(self, effect, prob):
        if prob < 100:
            apply = random.choices([True, False], [prob, 100 - prob])
        else:
            apply = [True]
        if apply[0] == True:
            if self.afected != effect:
                if self.afected == "None":
                    self.afected = effect
                    self.timer = effect.Turns
                    print(f"{self.nom} ha estat afectat per {effect.Name}.")
                    self.StatusEffectStatReduction()
                else:
                    print(f"{self.nom} ja esta afectat per {self.afected}")

    def CalcularDamage(self, enemy, move):
        # Cridar icrements d'stats en cas de ser necessari
        for i in move.StatusEffect:
            if i[0] == "Stat":
                if i[1][1] > 1:
                    self.BuffTempStats(i[1][1], i[1][0])
                    print(f"{i[1][0]} ha incrementat.\n")
                else:
                    enemy.BuffTempStats(i[1][1], i[1][0])
        
        # Calcul dels danys
        if move.Type == False:
            dif = self.tempATK / enemy.tempDEF
        else:
            dif = self.tempINT / enemy.tempDEF
        damage = (((((self.Lv * 2)/5)+2) * move.Power * dif) / 50) + 2
        crit = random.choices([True, False], cum_weights=[5, 95])
        if crit[0] == True:
            damage *= 1.75
            print("Ha estat un cop critic...")
        amplify = 1
        for i in self.Tituls:
            if enemy.base in i.Afects:
                amplify += i.DamageAmplify - 1
        if amplify != 1:
            print("El dany causat a incrementat a causa dels titols.")
            damage *= amplify
        damage *= (random.randint(90,111) / 100)

        # Reduim les estadistiques per efectes d'estat despres de calcular el dany.
        for i in move.StatusEffect:
            if i[0] == "Effect":
                enemy.ApplyStatusEffects(i[1][0], i[1][1])
        return damage

    def atacar(self, enemy,  move):
        impedit = False
        if self.afected != None:
            if self.afected.Blocking[0] == True:
                if self.afected.Blocking[1] >= 100:
                    impedit = [True]
                else:
                    impedit = random.choices([True, False], cum_weights=[self.afected.Blocking[1], 100 - self.afected.Blocking[1]])
        if impedit[0] == False:
            if move.Precision < 100:
                atac = random.choices([True, False], cum_weights=[move.Precision, 100 - move.Precision])
            else:
                atac = [True]
            if atac == [True]:
                if enemy.Protected == False or enemy.ProtectedBy[0] != None:
                    damage = self.CalcularDamage(enemy, move)
                    damage = round(damage, 2)
                    if enemy.Protected == True:
                        if enemy.ProtectedBy[0] != None:
                            damage = damage * ((100 - enemy.ProtectedBy[1]) / 100)
                            enemy.ProtectedBy[0].CurHP -= damage
                            print(f"{enemy.ProtectedBy[0].nom}, ha entomat el {enemy.ProtectedBy[1]}% del dany...")
                            if enemy.ProtectedBy[0].CurHP < 0:
                                print(f"{enemy.ProtectedBy[0].nom}, ha estat derrotat...")
                            else:
                                print(f"{enemy.ProtectedBy[0].nom}, ha recibit {damage} de dany...")
                        else:
                            enemy.CurHP -= damage
                            if enemy.CurHP <= 0:
                                print(f"{enemy.nom} ha estat derrotat.")
                            else:
                                print(f"{enemy.nom} ha perdut {damage} punts de vida...")
                    else:
                        enemy.CurHP -= damage
                        if enemy.CurHP <= 0:
                            print(f"{enemy.nom} ha estat derrotat.")
                        else:
                            print(f"{enemy.nom} ha perdut {damage} punts de vida...")
                else:
                    print(f"{enemy.nom} esta protegit i per tant l'atac no ha causat res...")
            else:
                if self.isPlayer == True:
                    print("Has fallat l'atac...")
                else:
                    print("L'atac enemic a fallat...")
            if enemy.Protected == True:
                enemy.Protected = False
        else:
            print(f"Has estat impedit per {self.afected.Name}")
        return enemy

    def MoveProtHeal(self, target, move):
        if move.Healing == True:
            if (target.CurHP + (move.Power * (self.INT / 100))) > target.MaxHP:
                target.CurHP = target.MaxHP
                print(f"{target.nom} ha recuperat vida fins al seu limit...")
            else:
                target.CurHP += (move.Power * (self.INT / 100))
                print(f"{target.nom} ha recuperat {move.Power * (self.INT / 100)} punts de vida...")
            for i in move.StatusEffect:
                if i[0] == "Stat":
                    target.BuffTempStats(i[1][1], i[1][0])
                if i[0] == "Effect":
                    target.ApplyStatusEffects(i[1][0], i[1][1])
        if move.Protective == True:
            target.Protected = True
            if self == target:
                print(f"{self.nom} s'ha preparat per protegir-se")
            else:
                print(f"{self.nom} s'ha preparat per protegir a {target.nom}")
            if move.AutoDamaging > 0:
                target.ProtectedBy = (self, move.AutoDamaging)
            for i in move.StatusEffect:
                if i[0] == "Stat":
                    target.BuffTempStats(i[1][1], i[1][0])
                if i[0] == "Effect":
                    target.ApplyStatusEffects(i[1][0], i[1][1])
        return target

    def ShowStatus(self, combat = False):
        print(f"Nom: {self.nom}")
        if self.base.isPlayable == True:
            print(f"Clase: {self.base.EntityName}")
            if self.subclass != None:
                print(f"Classe Secundaria: {self.subclass.EntityName}")
        else:
            print(f"Raça: {self.base.EntityName}")
        print(f"Or: {self.gold}")
        print(f"Lv: {self.Lv} / {self.LvLimit}")
        print(f"XP: {self.Xp} / {self.XpRequired}")
        print(f"HP: {round(self.CurHP, 2)} / {round(self.MaxHP, 2)}")
        print(f"Mana: {round(self.Mana, 2)} / {round(self.MaxMana, 2)}")
        if combat == False:
            print(f"ATK: {round(self.ATK, 2)}")
            print(f"INT: {round(self.INT, 2)}")
            print(f"DEF: {round(self.DEF, 2)}")
            print(f"SPD: {round(self.SPD, 2)}")
        else:
            print(f"ATK: {round(self.tempATK, 2)}")
            print(f"INT: {round(self.tempINT, 2)}")
            print(f"DEF: {round(self.tempDEF, 2)}")
            print(f"SPD: {round(self.tempSPD, 2)}")
        print("\nTitols: ")
        if self.isPlayer == True:
            count = 0
            for i in self.Tituls:
                if count < 3:
                    print(i.TitleName, end=", ")
                else:
                    print(i)
                    count = 0
        print("")
        if combat == False and self.subAcquirable == True:
            res = int(input("Digues si vols sortir (1), o obtenir una segona classe (2): "))
            if res not in [1, 2]:
                self.ShowStatus()
            if res == 2:
                self.DefinirSubClass()
        elif combat == False:
            input("Presiona per a continuar...")

    def LvlUp(self, enemy = None, XP = None):
        if self.Lv < self.LvLimit:
            if XP == None and enemy != None:
                obtainedXP = float(round(5 + enemy.base.baseXP * (enemy.Lv * 0.2), 2))
                print(f"{self.nom} ha guanyat {obtainedXP} punts d'experiencia.")
                self.Xp += obtainedXP
                self.Xp = float(round(self.Xp, 2))
            elif XP != None and enemy == None:
                self.Xp += XP
                self.Xp = float(round(self.Xp, 2))
                print(f"{self.nom} ha guanyat {XP} punts d'experiencia.")

            while self.Xp > self.XpRequired:
                self.Lv += 1
                print(f"{self.nom} ha pujat de nivell... Ara es nivell {self.Lv}")
                self.DefinirStats(True)
                self.Xp -= self.XpRequired
                self.XpRequired = float(round(self.XpRequired + 5 * (self.Lv ** 1.2), 2))
                if self.PostGame == True:
                    self.XpRequired /= 2
                    self.XpRequired = round(self.XpRequired, 2)
            input("Presiona per a continuar...")
    
    def AddXP(self, xpadded):
        if self.Lv < self.LvLimit:
            print(f"Has guanyat {xpadded}.")
            self.Xp += xpadded
            self.Xp = float(round(self.Xp, 2))
            if self.Xp > self.XpRequired:
                self.Lv += 1
                print(f"Has pujat de nivell... Ara ets nivell {self.Lv}")
                self.DefinirStats(True)
                self.XpRequired = float(round(self.XpRequired + 5 * (self.Lv ** 1.2), 2))
                self.Xp = 0
                input("Presiona per a continuar...")
    
    def AfegirObjecte(self, afegit, quantitat):
        if afegit in self.objectes:
            self.objectes[afegit] += quantitat
        else:
            self.objectes[afegit]=quantitat
    
    def MostrarObjectes(self):
        os.system("cls")
        for i in self.objectes.items():
            print(f"{i[0].ObjectName}, Qty: {i[1]}")
            print(f"{i[0].ObjectDescription}")
            print("\n")
    
    def ObjectesMochila(self, team, target = None, combat = bool(False)):
        res = 0
        if combat == True:
            used = False
        while res != 3:
            res = 0
            while res not in [1, 2, 3]:
                os.system("cls")
                print("1 -> Veure")
                print("2 -> Utilitzar")
                print("3 -> Sortir")
                try:
                    res = int(input("\nQue vols fer: "))
                    if res not in [1, 2, 3]:
                        print("Has de dir un dels 3 numeros...")
                except ValueError:
                    print("Ha ocurregut un error...")
            if res == 1:
                os.system("cls")
                self.MostrarObjectes()
                input("Presiona per a continuar...")
            if res == 2:
                obj = -2
                objectNames = list(self.objectes.keys())
                while obj not in range(1, len(objectNames) + 1) and obj != 0:
                    try:
                        os.system("cls")
                        ind = 1
                        for i in objectNames:
                            print(f"{ind} - > {i.ObjectName}")
                            ind += 1
                        print("Per a sortir de la seleccio escriu 0.")
                        obj = int(input("\nQuin objecte vols utilitzar: "))
                        if obj not in range(1, len(objectNames) + 1) and obj != 0:
                            print("\nHas de dir un dels objectes... o escriure 0")
                    except ValueError:
                        print("\nHa ocurregut un error...")
                        input("\nPresiona per a continuar...")
                if obj != 0:
                    if type(objectNames[obj - 1]) != Objectes.ObjecteClau:
                        if objectNames[obj - 1].OutCombat == False and combat == False:
                            print("Aquest objecte només es pot utilitzar en combat...")
                            input("Presiona per a continuar...")
                        else:
                            utilitzat = True
                            if target == None:
                                res = 0
                                while res not in range(1, len(team) + 2):
                                    os.system("cls" if os.name == "nt" else "clear")
                                    targetable = []
                                    for i in team:
                                        if i.CurHP > 0:
                                            targetable.append(i)
                                    count = 1
                                    for i in targetable:
                                        print(f"{count} -> {i.nom}, Lv: {i.Lv}")
                                        count += 1
                                    print(f"{count} -> Sortir")
                                    try:
                                        res = int(input("Digues de a qui vols atacar: "))
                                        if res not in range(1, count + 1):
                                            print("Has de dir un dels numeros corresponents...")
                                    except ValueError:
                                        print("Ha ocurregut un error...")
                                        input("Presiona per a continuar...")
                                if res in range(1, count):
                                    target = targetable[res - 1]
                                if res == count:
                                    print("Has deixat d'utilitzar aquest objecte...")
                                    utilitzat = False
                            if utilitzat == True:
                                objectNames[obj - 1].Utilitzar(target)
                                target.objectes[objectNames[obj - 1]]-= 1
                                print(f"Has utilitzat: {objectNames[obj - 1].ObjectName}")
                                if combat == True:
                                    used = True
                                    res = 3
                                if self.objectes[objectNames[obj - 1]] <= 0:
                                    target.objectes.pop(objectNames[obj - 1])
                    else:
                        print("Els objectes clau no es poden utilitzar, son objectes de missio o amb altres finalitats...")
                        input("Presiona per a continuar")
                else:
                    print("Has sortit del menu d'utilització.")
        if combat == True:
            return used
        
            
    