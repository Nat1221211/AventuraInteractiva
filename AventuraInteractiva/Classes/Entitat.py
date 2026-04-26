# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe entitat.

import random
from Classes import EntityType
import PrepararCridar as Call
import UIManager

import os

class Entity():
    
    nom = ""
    base = EntityType.EntityType

    # Level
    Lv = int()
    LvLimit = int()

    # Characteristics
    Moves = list()
    PastClasses = []
    subAcquirable = False

    # Combat Priority Variables
    Priority = int()
    Protected = False
    ProtectedBy = tuple()
    afected = []
    

    # Xp
    Xp = 0
    XpRequired = 14

    # Other
    isPlayer = bool()
    fleeProb = 75

    # Metodes
    def __init__(self, iden, nom, level, IsPlayer, BaseEntity, limit = 100, Xp = 0):
        self.id = iden
        self.nom = nom
        self.Lv = level
        self.isPlayer = IsPlayer
        self.LvLimit = limit
        self.base = BaseEntity
        self.Moves = {}
        self.Xp = Xp

            # Stats
        self.StatsBase = {
            "MaxHP": int(),
            "MaxMana": int(),
            "ATK": int(),
            "INT": int(),
            "DEF": int(),
            "SPD": int()
        }

        self.StatsPermanents = {
            "MaxHP": {"%": float(), "Flat": int()},
            "MaxMana": {"%": float(), "Flat": int()},
            "ATK": {"%": float(), "Flat": int()},
            "INT": {"%": float(), "Flat": int()},
            "DEF": {"%": float(), "Flat": int()},
            "SPD": {"%": float(), "Flat": int()},
        }

        self.StatsCombat = {
            "MaxHP": int(),
            "CurHP": int(),
            "MaxMana": int(),
            "Mana": int(),
            "ATK": int(),
            "INT": int(),
            "DEF": int(),
            "SPD": int()
        }

        self.DefinirStats()
        self.DefinirCombatStats()
        if IsPlayer == False:
            if nom == "":
                if "Human" in self.base.EntityGroup:
                    self.nom = "Bandit"
                else:
                    self.nom = self.base.EntityName
        self.afected = []
        self.subclass = []
        self.Equipment = {
            "Weapon": "",
            "Armor": "",
            "Helmet": "",
            "Boots": "",
            "Accesory_1": "",
            "Accesory_2": "",
        }

        self.ImatgeAjustada = {}

    def Recuperacio(self):
        self.StatsCombat["CurHP"] = self.StatsCombat["MaxHP"]
        self.StatsCombat["Mana"] = self.StatsCombat["MaxMana"]
        self.afected = []
        
    def DefinirMoves(self):
        for k in self.base.EntityMoves.items():
            if k[1]["Lv"] <= self.Lv and k[0] not in self.Moves.keys():
                self.Moves.update({k[0]: k[1]["Move"]})
        # if len(self.PastClasses) > 0:
        #     for i in self.PastClasses:
        #         for j in i.EntityMoves.items():
        #             if j[1]["Lv"] <= self.Lv and j[0] not in self.Moves.keys():
        #                 self.Moves.update({j[0]: j[1]["Move"]})

    def DefinirStats(self,LvOrNot = False):
        baseHealth = self.base.Health / 50
        baseMagic = self.base.Magic / 50
        baseAttack = self.base.Attack / 50
        baseIntel = self.base.Intel / 50
        baseDefense = self.base.Defense / 50
        baseSpeed = self.base.Speed / 50
        
        # if len(self.PastClasses) > 0:
        #     for i in self.PastClasses:
        #         baseHealth += i.Health / 100
        #         baseMagic += i.Magic / 100
        #         baseAttack += i.Attack / 100
        #         baseIntel += i.Intel / 100
        #         baseDefense += i.Defense / 100
        #         baseSpeed += i.Speed / 100            

        self.StatsBase["MaxHP"] = 10 + (baseHealth * self.Lv)
        self.StatsBase["MaxMana"] = 10 + (baseMagic * self.Lv)
        self.StatsBase["ATK"] = 10 + (baseAttack * self.Lv)
        self.StatsBase["INT"] = 10 + (baseIntel * self.Lv)
        self.StatsBase["DEF"] = 10 + (baseDefense * self.Lv)
        self.StatsBase["SPD"] = 10 + (baseSpeed * self.Lv)
        
        if LvOrNot == False:
            self.StatsCombat["CurHP"] = self.StatsBase["MaxHP"]
            self.StatsCombat["Mana"] = self.StatsBase["MaxMana"]
            self.XpRequired = float(round(self.CalcXPRequired(), 2))
            self.afected = []
        self.DefinirMoves()
    
    # def DefinirPermanentStats(self, jugador):
    #     for k, v in jugador.StatIncrement.items():
    #         self.StatsPermanents[k][v[0]]+=v[1]
    
    def DefinirCombatStats(self):
        for k, v in self.StatsBase.items():
            PostBuff = v + self.StatsPermanents[k]["Flat"]
            PostBuff *= (1 + self.StatsPermanents[k]["%"])
            self.StatsCombat[k] = PostBuff
    
    def ChangeCombatStats(self, changes):
        self.DefinirCombatStats()
        for k, v in changes.items():
            self.StatsCombat[k] *= v

    def AplicarCanvisEfectesEstat(self):
        StatChanges = {}

        for i in self.afected:
            for k, v in i.StatEffects.items():
                if k in StatChanges.keys():
                    if v < 1:
                        StatChanges[k]-=v
                    else:
                        StatChanges[k]+= (v-1)
                else:
                    if v < 1:
                        value = 1 - v
                    else:
                        value = v
                    StatChanges[k]=value
        for id, value in StatChanges.items():
            if value > 4:
                value = 4
            elif value < 0.3:
                value = 0.3
        self.ChangeCombatStats(StatChanges)
    
    
    def ApplyStatusEffects(self, effect, prob):
        if prob < 100:
            apply = random.choices([True, False], [prob, 100 - prob])
        else:
            apply = [True]
        if apply[0] == True:
            efectNames = []
            for i in self.afected:
                efectNames.append(i.Name)
            
            aplicable = True
            if effect.Name in efectNames:
                effectCount = 0
                for i in self.afected:
                    if effect.Name == i.Name:
                        effectCount += 1
                limit = effect.EffectLimit
                if effectCount + 1 > limit and limit != 0:
                    aplicable = False
                    print(f"{self.nom} ha arribat al limit d'aplicacions de l'efecte {effect.Name}")

            if aplicable == True:
                effect.RemainingTurns = effect.Turns
                self.afected.append(effect)
                print(f"{self.nom} ha estat afectat per {effect.Name}.")
                self.AplicarCanvisEfectesEstat()

                

    def CalcularDamage(self, enemy, move):
        
        # Calcul dels danys
        if move.Type == False:
            dif = self.StatsCombat["ATK"] / enemy.StatsCombat["DEF"]
        else:
            dif = self.StatsCombat["INT"] / enemy.StatsCombat["DEF"]
        damage = (((((self.Lv * 2)/5)+2) * move.Power * dif) / 50) + 2
        crit = random.choices([True, False], cum_weights=[5, 95])
        if crit[0] == True:
            damage *= 1.75
            print(f"{enemy.nom} ha rebut un critic...")

        # Reduim les estadistiques per efectes d'estat despres de calcular el dany.
        for i in move.Debuff.items():
            enemy.ApplyStatusEffects(i[0], i[1])
        return damage

    def atacar(self, enemy, target, move):
        impedit = [False]
        if len(self.afected) > 0:
            for i in self.afected:
                if i.Blocking[0] == True and impedit[0] == False:
                    if i.Blocking[1] >= 100:
                        impedit = [True]
                    else:
                        impedit = random.choices([True, False], cum_weights=[self.afected.Blocking[1], 100 - self.afected.Blocking[1]])
                        if impedit[0] == True:
                            impedit[1] = i
        if impedit[0] == False:
            # Cridar icrements d'stats en cas de ser necessari
            for i in move.Buff.items():
                self.ApplyStatusEffects(i[0], i[1])

            derrotats = []
            for id, ent in enemy.items():
                if move.MultiTarget or id == target or target == "All":
                    print(f"{self.nom} ha atacat.")
                    if move.Precision < 100:
                        atac = random.choices([True, False], cum_weights=[move.Precision, 100 - move.Precision])
                    else:
                        atac = [True]
                    if atac == [True]:
                        if ent.Protected == False or ent.ProtectedBy[0] != None:
                            damage = self.CalcularDamage(ent, move)
                            damage = round(damage, 2)
                            if ent.Protected == True:
                                if ent.ProtectedBy[0] != None:
                                    damage = damage * ((100 - ent.ProtectedBy[1]) / 100)
                                    ent.ProtectedBy[0].StatsCombat["CurHP"] -= damage
                                    print(f"{ent.ProtectedBy[0].nom}, ha entomat el {ent.ProtectedBy[1]}% del dany...")
                                    if ent.ProtectedBy[0].StatsCombat["CurHP"] < 0.1:
                                        print(f"{ent.ProtectedBy[0].nom}, ha estat derrotat...")
                                        derrotats.append(ent)
                                    else:
                                        print(f"{ent.ProtectedBy[0].nom}, ha recibit {damage} de dany...")
                                else:
                                    enemy.StatsCombat["CurHP"] -= damage
                                    if enemy.StatsCombat["CurHP"] < 0.1:
                                        print(f"{enemy.nom} ha estat derrotat.")
                                        derrotats.append(ent)
                                    else:
                                        print(f"{enemy.nom} ha perdut {damage} punts de vida...")
                            else:
                                ent.StatsCombat["CurHP"] -= damage
                                if ent.StatsCombat["CurHP"] < 0.1:
                                    print(f"{ent.nom} ha estat derrotat.")
                                    derrotats.append(ent)
                                else:
                                    print(f"{ent.nom} ha perdut {damage} punts de vida...")
                        else:
                            print(f"{ent.nom} esta protegit i per tant l'atac no ha causat res...")
                    else:
                        print("Ha fallat l'atac...")
                    
                    if ent.Protected == True:
                        ent.Protected = False
        else:
            print(f"Has estat impedit per {impedit.Name}")
        input("Presiona per a continuar...")
        return enemy, derrotats

    def MoveProtHeal(self, targets, target, move):
        for id, ent in targets.items():
            if id == target or move.MultiTarget:
                if move.Healing == True:
                    if (ent.StatsCombat["CurHP"] + (move.Power * (self.StatsCombat["INT"] / 100))) > ent.StatsCombat["MaxHP"]:
                        ent.StatsCombat["CurHP"] = ent.StatsCombat["MaxHP"]
                        print(f"{ent.nom} ha recuperat vida fins al seu limit...")
                    else:
                        ent.StatsCombat["CurHP"] += (move.Power * (self.StatsCombat["INT"] / 100))
                        print(f"{ent.nom} ha recuperat {move.Power * (self.StatsCombat["INT"] / 100)} punts de vida...")
                    for i in move.Buff.items():
                        ent.ApplyStatusEffects(i[0], i[1])
                if move.Protective == True:
                    ent.Protected = True
                    if self == ent:
                        print(f"{self.nom} s'ha preparat per protegir-se")
                    else:
                        print(f"{self.nom} s'ha preparat per protegir a {ent.nom}")
                    if move.AutoDamaging > 0:
                        target.ProtectedBy = (self, move.AutoDamaging)
                        
                    for i in move.Buff.items():
                        target.ApplyStatusEffects(i[0], i[1])
        input("Presiona per a continuar...")
        return targets

    def ShowStatus(self, jugador, combat = False):
        UIManager.ClearScreen()
        print(f"Nom: {self.nom}")
        if self.base.isPlayable == True:
            print(f"Clase: {self.base.EntityName}")
            if len(self.PastClasses) > 0:
                subclasses = ""
                for i in self.PastClasses:
                    if i == self.PastClasses[len(self.PastClasses)]:
                        subclasses += {i.EntityName}
                    else:
                        subclasses += ({i.EntityName} + ", ")
                print(f"Classe Secundaria: {subclasses}")
        else:
            print(f"Raça: {self.base.EntityName}")
        print(f"Or: {jugador.Gold}")
        print(f"Lv: {self.Lv} / {self.LvLimit}")
        print(f"XP: {round(self.Xp, 2)} / {round(self.XpRequired, 2)}")
        print(f"HP: {round(self.StatsCombat["CurHP"], 2)} / {round(self.StatsCombat["MaxHP"], 2)}")
        print(f"Mana: {round(self.StatsCombat["Mana"], 2)} / {round(self.StatsCombat["MaxMana"], 2)}")
        print(f"ATK: {round(self.StatsCombat["ATK"], 2)}")
        print(f"INT: {round(self.StatsCombat["INT"], 2)}")
        print(f"DEF: {round(self.StatsCombat["DEF"], 2)}")
        print(f"SPD: {round(self.StatsCombat["SPD"], 2)}")
        print("\nTitols: ")
        # if self.isPlayer == True:
        #     count = 0
        #     for i in self.Titles:
        #         if count < 3:
        #             print(i.TitleName, end=", ")
        #         else:
        #             print(i)
        #             count = 0
        print("")
        if combat == False and self.subAcquirable == True:
            res = int(input("Digues si vols sortir (1), o obtenir una segona classe (2): "))
            if res not in [1, 2]:
                self.ShowStatus()
            if res == 2:
                self.DefinirSubClass()
        # elif combat == False:
        input("Presiona per a continuar...")

    def LvlUp(self, event, jugador, exits, enemy = None, XP = None):
        if self.Lv < self.LvLimit:
            if XP == None and enemy != None:
                XP = float(round(self.XPObtained(enemy), 2))
                self.Xp += XP
                self.Xp = float(round(self.Xp, 2))
            elif XP != None and enemy == None:
                self.Xp += XP
                self.Xp = float(round(self.Xp, 2))
            
            print(f"{self.nom} ha guanyat {XP} punts d'experiencia.")

            while self.Xp > self.XpRequired:
                self.Lv += 1
                print(f"{self.nom} ha pujat de nivell... Ara es nivell {self.Lv}")
                self.DefinirStats(True)
                self.DefinirCombatStats()
                self.Xp -= self.XpRequired
                self.XpRequired = float(round(self.CalcXPRequired(), 2))
                event.CridarEvent("Nivell Incrementat", self, jugador, exits)
                self.AplicarCanvisEfectesEstat()
            input("Presiona per a continuar...")
    
    def CalcXPRequired(self):
        baseAmount = 5
        multiplierToLvl = 600

        exponentForLvl = 2


        addToExponent = (self.Lv * (1 / multiplierToLvl))

        xpMultiplier = (self.Lv ** (exponentForLvl + addToExponent))
        xpRequired = baseAmount * xpMultiplier

        return xpRequired


    def XPObtained(self, enemy):
        baseXP = enemy.base.baseXP
        
        # Exponents / Multiplicadors
        lvlExponent = 0.3
        lvlDiffExponent = 1.4

        # Valors
        multiplierperLevel = 1 + (lvlExponent*enemy.Lv)
        multiplierPerDiff = (enemy.Lv / self.Lv) ** lvlDiffExponent

        # Resultat
        xpObtained = baseXP * multiplierperLevel * multiplierPerDiff

        xpObtained = max(xpObtained, baseXP * 0.1)
        xpObtained = min(xpObtained, baseXP * 100)

        return xpObtained

