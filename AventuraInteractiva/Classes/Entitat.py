# Arxiu: Entitat.py
# Autor: Bernat Puig Casals
# Data: 2 de Desembre de 2025
# Descripcio:
# Creem la classe entitat.

import random
from Classes import EntityType
import PrepararCridar as Call

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
    def __init__(self, iden, nom, level, IsPlayer, BaseEntity, limit = 100):
        self.id = iden
        self.nom = nom
        self.Lv = level
        self.isPlayer = IsPlayer
        self.LvLimit = limit
        self.base = BaseEntity
        self.Moves = {}

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
            self.XpRequired = float(round(self.XpRequired + 5 * (self.Lv ** 1.2), 2))
            self.afected = []
        self.DefinirMoves()
    
    def DefinirPermanentStats(self):
        # if "%" in permanentbuff:
        #     self.StatsPermanents[permanentbuff[0]]["%"] += float(permanentbuff[1])
        # else:
        #     self.StatsPermanents[permanentbuff[0]]["Flat"] += float(permanentbuff[1])
        print()
    
    def DefinirCombatStats(self):
        for k, v in self.StatsBase.items():
            PostBuff = v + self.StatsPermanents[k]["Flat"]
            PostBuff *= (1 + self.StatsPermanents[k]["%"])
            self.StatsCombat[k] = PostBuff
    
    def ChangeCombatStats(self, changes):
        for k, v in changes.items():
            self.StatsCombat[k] *= v
    
    
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
            if effect in efectNames:
                effectCount = 0
                for i in self.afected:
                    if effect == i.Name:
                        effectCount += 1
                        limit = i.EffectLimit
                if effectCount + 1 > limit and limit != 0:
                    aplicable = False
                    print(f"{self.nom} ha arribat al limit d'aplicacions de l'efecte {effect}")

            if aplicable == True:
                effect.RemainingTurns = effect.Turns
                self.afected.append(effect)
                print(f"{self.nom} ha estat afectat per {effect.Name}.")

                StatChanges = {}

                for i in self.afected:
                    for k, v in i.StatEffects.items():
                        if v < 1:
                            value = 1 - v
                        else:
                            value = v
                        if k in StatChanges.keys():
                            StatChanges[k]+=value
                        else:
                            StatChanges[k]=value
                for k, v in StatChanges.items():
                    self.StatsCombat[k] *= v

    def CalcularDamage(self, enemy, move):
        # Cridar icrements d'stats en cas de ser necessari
        for i in move.Buff.items():
            self.ApplyStatusEffects(i[0], i[1])
        
        # Calcul dels danys
        if move.Type == False:
            dif = self.StatsCombat["ATK"] / enemy.StatsCombat["DEF"]
        else:
            dif = self.StatsCombat["INT"] / enemy.StatsCombat["DEF"]
        damage = (((((self.Lv * 2)/5)+2) * move.Power * dif) / 50) + 2
        crit = random.choices([True, False], cum_weights=[5, 95])
        if crit[0] == True:
            damage *= 1.75
            print("Ha estat un cop critic...")
        # amplify = 1
        # for i in self.Tituls:
        #     if enemy.base in i.Afects:
        #         amplify += i.DamageAmplify - 1
        # if amplify != 1:
        #     print("El dany causat a incrementat a causa dels titols.")
        #     damage *= amplify
        # damage *= (random.randint(90,111) / 100)

        # Reduim les estadistiques per efectes d'estat despres de calcular el dany.
        for i in move.Debuff.items():
            enemy.ApplyStatusEffects(i[0], i[1])
        return damage

    def atacar(self, enemy,  move):
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
                            enemy.ProtectedBy[0].StatsCombat["CurHP"] -= damage
                            print(f"{enemy.ProtectedBy[0].nom}, ha entomat el {enemy.ProtectedBy[1]}% del dany...")
                            if enemy.ProtectedBy[0].StatsCombat["CurHP"] < 0.1:
                                print(f"{enemy.ProtectedBy[0].nom}, ha estat derrotat...")
                            else:
                                print(f"{enemy.ProtectedBy[0].nom}, ha recibit {damage} de dany...")
                        else:
                            enemy.StatsCombat["CurHP"] -= damage
                            if enemy.StatsCombat["CurHP"] < 0.1:
                                print(f"{enemy.nom} ha estat derrotat.")
                            else:
                                print(f"{enemy.nom} ha perdut {damage} punts de vida...")
                    else:
                        enemy.StatsCombat["CurHP"] -= damage
                        if enemy.StatsCombat["CurHP"] < 0.1:
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
            print(f"Has estat impedit per {impedit.Name}")
        input("Presiona per a continuar...")
        return enemy

    def MoveProtHeal(self, target, move):
        if move.Healing == True:
            if (target.StatsCombat["CurHP"] + (move.Power * (self.StatsCombat["INT"] / 100))) > target.StatsCombat["MaxHP"]:
                target.StatsCombat["CurHP"] = target.StatsCombat["MaxHP"]
                print(f"{target.nom} ha recuperat vida fins al seu limit...")
            else:
                target.StatsCombat["CurHP"] += (move.Power * (self.StatsCombat["INT"] / 100))
                print(f"{target.nom} ha recuperat {move.Power * (self.StatsCombat["INT"] / 100)} punts de vida...")
            for i in move.Buff.items():
                target.ApplyStatusEffects(i[0], i[1])
        if move.Protective == True:
            target.Protected = True
            if self == target:
                print(f"{self.nom} s'ha preparat per protegir-se")
            else:
                print(f"{self.nom} s'ha preparat per protegir a {target.nom}")
            if move.AutoDamaging > 0:
                target.ProtectedBy = (self, move.AutoDamaging)
                
            for i in move.Buff.items():
                target.ApplyStatusEffects(i[0], i[1])
        input("Presiona per a continuar...")
        return target

    def ShowStatus(self, jugador, combat = False):
        Call.ClearScreen()
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

    def LvlUp(self, enemy = None, XP = None):
        if self.Lv < self.LvLimit:
            if XP == None and enemy != None:
                XP = float(round(5 + enemy.base.baseXP * (enemy.Lv * 0.2), 2))
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
                self.XpRequired = float(round(self.XpRequired + 5 * (self.Lv ** 1.2), 2))
            input("Presiona per a continuar...")
    
    
   