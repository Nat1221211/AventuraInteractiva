# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe entitat.

import random
import EntityType

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
    Moves = list()

    # temp stats
    tempATK = int()
    tempINT = int()
    tempDEF = int()
    tempSPD = int()
    buffATK = 1
    buffINT = 1
    buffSPD = 1
    buffDEF = 1

    # Xp
    Xp = 0
    XpRequired = 14

    # Other
    isPlayer = bool()
    gold = 0
    objectes = {} # Diccionari, objecte i quantitat
    fleeProb = 75
    Tituls = []
    PostGame = False

    # Metodes
    def __init__(self, nom, level, IsPlayer, BaseEntity, limit = 100, objectes = {}, gold = 10, post = False):
        self.nom = nom
        self.Lv = level
        self.isPlayer = IsPlayer
        self.LvLimit = limit
        self.base = BaseEntity
        self.Moves = list()
        self.DefinirStats()
        self.CurHP = self.MaxHP
        if IsPlayer == True:
            self.gold = 2000
        else:
            if nom == "":
                self.nom = self.base.EntityName
            self.gold = gold
        self.objectes = objectes
        self.PostGame = post
        
    def DefinirMoves(self):
        for i in self.base.EntityMoves.items():
            if i[1] <= self.Lv and i[0] not in self.Moves:
                self.Moves.append(i[0])

    def DefinirStats(self,LvOrNot = False):
        self.MaxHP = 10 + ((self.base.Health / 50) * self.Lv)
        self.MaxMana = 10 + ((self.base.Magic / 50) * self.Lv)
        self.ATK = 10 + ((self.base.Attack / 50) * self.Lv)
        self.INT = 10 + ((self.base.Intel / 50) * self.Lv)
        self.DEF = 10 + ((self.base.Defense / 50) * self.Lv)
        self.SPD = 10 + ((self.base.Speed / 50) * self.Lv)
        if LvOrNot == False:
            self.CurHP = self.MaxHP
            self.Mana = self.MaxMana
        self.DefinirTempStats()
        self.DefinirMoves()
    
    def DefinirTempStats(self):
        self.tempATK = self.ATK
        self.tempINT = self.INT
        self.tempDEF = self.DEF
        self.tempSPD = self.SPD
    
    def BuffTempStats(self, buff, statbuffed):
        self.DefinirTempStats()
        for i in statbuffed:
            if buff > 1:
                buff -= 1
            else:
                buff = abs(buff)
                buff = -(buff)
                print(f"La estadistica {i} s'ha reduit en {abs(buff * 100)}%")
            if i == "ATK":
                self.buffATK += buff
                self.tempATK *= self.buffATK
            if i == "INT":
                self.buffINT += buff
                self.tempINT *= self.buffINT
            if i == "SPD":
                self.buffSPD += buff
                self.tempSPD *= self.buffSPD
            if i == "DEF":
                self.buffDEF += buff
                self.tempDEF *= self.buffDEF

    
    def ResetBuffs(self):
        self.buffATK = 1
        self.buffINT = 1
        self.buffSPD = 1
        self.buffDEF = 1

    def CalcularDamage(self, enemy, move):
        # Cridar icrements d'stats en cas de ser necessari
        if move.StatusEffect[0] == True:
            if move.StatusEffect[1][1] > 1:
                self.BuffTempStats(move.StatusEffect[1][1], move.StatusEffect[1][0])
                print(f"{move.StatusEffect[1][0]} ha incrementat.\n")
            else:
                enemy.BuffTempStats(move.StatusEffect[1][1], move.StatusEffect[1][0])
                enemy.ShowStatus(True)
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
        return damage

    def atacar(self, enemy, move):
        if move.Precision < 100:
            atac = random.choices([True, False], cum_weights=[move.Precision, 100 - move.Precision])
        else:
            atac = [True]
        if atac == [True]:
            damage = self.CalcularDamage(enemy, move)
            damage = round(damage, 2)
            enemy.CurHP -= damage
            if enemy.CurHP <= 0 and enemy.isPlayer == False:
                print(f"{enemy.nom} ha estat derrotat.")
            else:
                print(f"{enemy.nom} ha perdut {damage} punts de vida...")
        else:
            if self.isPlayer == True:
                print("Has fallat l'atac...")
            else:
                print("L'atac enemic a fallat...")
        return enemy

    def ShowStatus(self, combat = False):
        print(f"Nom: {self.nom}")
        if self.base.isPlayable == True:
            print(f"Clase: {self.base.EntityName}")
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
        if combat == False:
            input("Presiona per a sortir...")

    def LvlUp(self, enemy):
        if self.Lv < self.LvLimit:
            obtainedXP = float(round(5 + enemy.base.baseXP * (enemy.Lv * 0.2), 2))
            print(f"Has guanyat {obtainedXP}.")
            self.Xp += obtainedXP
            self.Xp = float(round(self.Xp, 2))
            if self.Xp > self.XpRequired:
                self.Lv += 1
                print(f"Has pujat de nivell... Ara ets nivell {self.Lv}")
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
    
    def ObjectesMochila(self, combat = bool(False)):
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
                    objectNames[obj - 1].Utilitzar(self)
                    self.objectes[objectNames[obj - 1]]-= 1
                    print(f"Has utilitzat: {objectNames[obj - 1].ObjectName}")
                    if combat == True:
                        used = True
                        res = 3
                else:
                    print("Has sortit del menu d'utilització.")
        if combat == True:
            return used
        
            
    