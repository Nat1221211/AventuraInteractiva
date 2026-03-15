# Arxiu: PrepararCridar.py
# Autor: Bernat Puig Casals
# Data: 7 de Març de 2026
# Descripcio:
# Creem el modul per a guardar i carregar la partida.

import csv
import json
import os
import random

# Importar Classes
from Classes import Entitat
import UIManager


def GenerarEnemic(Entities, jugador, event, missions, objectes):

    pesos = []
    for j in jugador.Ubicacio.Enemies.values():
        pesos.append(j["prob"])
    opcions = list(jugador.Ubicacio.Enemies.keys())
    seleccio = random.choices(opcions, pesos)
    
    prob = jugador.Ubicacio.Enemies[seleccio[0]]["group_probs"]
    
    num = []
    count = 1
    for i in prob:
        num.append(count)
        count += 1
    qty = random.choices(num, prob)
    enemy = {}

    enemy.update({
        "enemy_0":
        Entitat.Entity("enemy_0", "", random.randrange(
            jugador.Ubicacio.Enemies[seleccio[0]]["level_range"][0], 
            jugador.Ubicacio.Enemies[seleccio[0]]["level_range"][1] + 1), 
            False, 
            Entities[seleccio[0]])})

    probs = []
    opcionsPosib = []

    for v in jugador.Ubicacio.Enemies[seleccio[0]]["companions"]:
        probs.append(v[1])
        opcionsPosib.append(v[0])


    if qty[0] > 1:
        for l in range(qty[0] - 1):
            if len(probs) >= 1:
                apareix = random.choices(opcionsPosib, probs)
            else:
                apareix = seleccio[0]
            entitat = Entitat.Entity(f"enemy_{l+1}","", 
                        random.randrange(
                            jugador.Ubicacio.Enemies[seleccio[0]]["level_range"][0] - 2, enemy["enemy_0"].Lv), 
                            False, Entities[apareix])
            
            enemy.update({entitat.id: entitat})
    
    Lluitar(jugador, enemy, event, missions, objectes)



def PrepararPerCombat(jugador, enemy):
    for i in jugador.Team.values():
        i.DefinirCombatStats()
    
    for j in enemy.values():
        j.DefinirCombatStats()
    
    return enemy

def PrioritatInicial(jugador, enemy):
    maxSpeedPlayer = max(jugador.Team.values(), key=lambda j: j.StatsCombat["SPD"])
    maxSpeedEnemies = max(enemy.values(), key=lambda e: e.StatsCombat["SPD"])

    maxSpeed = max(maxSpeedPlayer.StatsCombat["SPD"], maxSpeedEnemies.StatsCombat["SPD"])

    for i in jugador.Team.values():
        if i.StatsCombat["SPD"] == maxSpeed:
           i.Priority = 100
        else:
            i.Priority = (i.StatsCombat["SPD"] / maxSpeed) * 100
    
    for j in enemy.values():
        if j.StatsCombat["SPD"] == maxSpeed:
            j.Priority = 100
        else:
            j.Priority = (j.StatsCombat["SPD"] / maxSpeed) * 100

    return enemy

def Lluitar(jugador, enemy, event, missions, objectes):

    teamderr = 0
    enemyderr = 0

    enemy = PrepararPerCombat(jugador, enemy)

    enemy = PrioritatInicial(jugador, enemy)

    primer = False
    for i in jugador.Team.values():
        if i.Priority >= 100:
            primer = True
    
    if primer == False:
        print(f"Has estat emboscat per {enemy.keys()}s.")
    else:
        print(f"Han aparegut {enemy.keys()}s.")
        
    fugir = [False]
    combat = True
    while combat == True and fugir[0] == False: 
        # Turn Aliat
        
        for i in jugador.Team.values():
            if i.Priority >= 100 and len(enemy) >= 1 and i.StatsCombat["CurHP"] > 0.1 and combat == True:
                turn = True
                while turn == True:
                    UIManager.ClearScreen()
                    UIManager.BattleScreenShow(jugador.Team)
                    UIManager.BattleScreenShow(enemy)
                    turn = False
                    i, enemy, turn, fugir, enemyderr = AccionsLluita(i, jugador, enemy, enemyderr, objectes)
                    
                    if turn == False:
                        i.Priority = 0
                UIManager.ClearScreen()
            if combat == True:
                combat = ComprobarFiCombat(combat, enemyderr, enemy, teamderr, event, missions, jugador)

        # Turn enemic
        for j in enemy.values():
            if j.Priority >= 100 and fugir[0] == False and len(jugador.Team) >= 1 and j.StatsCombat["CurHP"] > 0.1 and combat == True:
                UIManager.ClearScreen()
                UIManager.BattleScreenShow(jugador.Team)
                UIManager.BattleScreenShow(enemy)
                enemyMove = random.choice([e for e in j.Moves.values()])
                targetable = [e.id for e in jugador.Team.values() if e.StatsCombat["CurHP"] > 0]
                # for e in jugador.Team.values():
                #     if e.StatsCombat["CurHP"] > 0:
                #         targetable.append(e)
                target = random.choice(targetable)
                jugador.Team, derrotats = j.atacar(jugador.Team, target, enemyMove)
                j.Priority = 0
                j, derrotats = ComprobarEfectEstat(j, derrotats)
                teamderr = DescartarDerrotats(derrotats, teamderr, jugador)
                UIManager.ClearScreen()
            if combat == True:
                combat = ComprobarFiCombat(combat, enemyderr, enemy, teamderr, event, missions, jugador)
        
        enemy = IncrementarPrioritat(jugador, enemy)
    finalitzarCombat(jugador.Team, jugador)

def IncrementarPrioritat(jugador, enemy):
    for i in jugador.Team.values():
        if i.StatsCombat["CurHP"] > 0:
            i.Priority += i.StatsCombat["SPD"] / 100  
    
    for j in enemy.values():
        if j.StatsCombat["CurHP"] > 0:
            j.Priority += j.StatsCombat["SPD"] / 100
    return enemy

def DescartarDerrotats(llista, derr, jugador):
    for p in llista:
        if p.StatsCombat["CurHP"] <= 0.1:
            derr += 1
            if p.isPlayer == False:
                UIManager.ClearScreen()
                alive = 0
                for i in jugador.Team.values(): 
                    if i.StatsCombat["CurHP"] > 0:
                        i.LvlUp(p)
                        alive += 1
                if alive >= 1:
                    jugador.Gold += p.Lv * 10 # 10 monedes per cada nivell, representa que es ven el derrotat.
                    print(f"Has guanyat {p.Lv * 10} gold.")
                    input("Presiona per a continuar...")
    return derr

def ComprobarFiCombat(combat, enemyderr, enemy, teamderr, event, missions, jugador):
    if enemyderr == len(enemy) or teamderr == len(jugador.Team):
        combat = False
        if len(enemy) == enemyderr:
            UIManager.ClearScreen()
            print("Tos els enemics han estat derrotats !!")
            input("Presiona per a continuar")
            for id, val in enemy.items():
                event.CridarEvent("Derrotar Enemic", val, jugador, missions)
    return combat


def finalitzarCombat(clon, jugador):
    for i in jugador.Team.keys(): 
        # if i in clon.keys():
        #     jugador.Team[i].StatsCombat["CurHP"] = clon[i].StatsCombat["CurHP"]
        #     jugador.Team[i].StatsCombat["Mana"] = clon[i].StatsCombat["Mana"]
        # else:
        #     i.StatsCombat["CurHP"] = 0
        #     i.StatsCombat["Mana"] = 0
        jugador.Team[i].afected = []
        jugador.Team[i].DefinirCombatStats()

def ComprobarEfectEstat(entitat, derrotats):
    if len(entitat.afected) > 0:
        eliminar = []
        for i in entitat.afected:
            if i.RemainingTurns <= 0 and i.Turns > 0:
                statsafected = entitat.afected.StatEffects[1][0]
                eliminar.append(i)
                # Regenerar Estadistiques
                print(f"{entitat.nom}, ja no esta afectat per {i.Name}, les seves estadistiques han retornat al que eren...")
            elif entitat.StatsCombat["CurHP"] > 0:
                if i.Damage > 0:
                    damagepereffect = ((entitat.StatsCombat["MaxHP"] / 100) * i.Damage)
                    entitat.StatsCombat["CurHP"] -= damagepereffect
                    print(f"{entitat.nom}, ha perdut {round(damagepereffect, 2)} HP degut a la {i.Name}.")
                    if entitat.StatsCombat["CurHP"] <= 0:
                        print(f"{entitat.nom}, ha estat derrotat per {i.Name}.")
                        derrotats.append(entitat)
                i.RemainingTurns -= 1
        for j in eliminar:
            entitat.afected.remove(j)
    return entitat, derrotats

def MenuAtacar(personatge):
    UIManager.ClearScreen()
    
    UIManager.CrearMenu(personatge.Moves.items(), "Moviments", "Moves")

    sel = UIManager.MostrarMenus(UIManager.Menus["Moviments"])

    use = personatge.Moves[sel]
    if use.Cost > personatge.StatsCombat["Mana"]:
        print("No tens suficient Mana per a realitzar aquest atac...")
        input("Presiona per a continuar...")
        return None
    else:
        return use
    
def AccionsLluita(atacant, jugador, enemy, enemyderr, objectes):
    print(f"És el torn de {atacant.nom}")
    
    seleccio = UIManager.MostrarMenus(UIManager.Menus["Accions Lluita"], False, True, jugador, enemy)
    
    turn = False
    fugir = [False]
    
    print("\n")
    if seleccio == "atacar":
        move = MenuAtacar(atacant)
        target = None
        UIManager.ClearScreen()
        UIManager.BattleScreenShow(jugador.Team)
        UIManager.BattleScreenShow(enemy)
        print("\n")
        if move != None:
            if move.MultiTarget == False:
                if move.Healing == False and move.Protective == False:
                    if len(enemy) > 1:
                        target = TriarObjectius(enemy)
                elif move.Healing == True or move.Protective == True:
                    target = TriarObjectius(jugador.Team)
            if move.Healing == False and move.Protective == False:
                enemy, derrotats = atacant.atacar(enemy, target, move)
                enemyderr = DescartarDerrotats(derrotats, enemyderr, jugador)
            else:
                jugador.Team, derrotats = atacant.MoveProtHeal(jugador.Team, target, move)
                
            atacant.StatsCombat["Mana"] -= move.Cost
        if move == None or target == False:
            turn = True
    elif seleccio == "fugir":
        fugir = Fugir(enemy, jugador)
        if fugir[0] == False:
            atacant, derrotats = ComprobarEfectEstat(atacant, derrotats)
    elif seleccio == "motxila":
        obj = jugador.ObjectesMochila(objectes, True)
        used = None

        if obj != None:
            used = UseObject(jugador, jugador.Team, obj, True)
        if obj == None or used == None:
            turn = True
    elif seleccio == "status":
        UIManager.VeureEstatus(jugador, True)
        turn = True
    elif seleccio == "pasar":
        print("Has decidit pasar torn...")
        input("Presiona per a continuar...")
    
    return atacant, enemy, turn, fugir, enemyderr

def TriarObjectius(list):

    UIManager.ClearScreen()
    targetable = [i for i in list.items() if i[1].StatsCombat["CurHP"] > 0]
    
    UIManager.CrearMenu(targetable, "Qui Vols Atacar?", "Entitat")

    target = UIManager.MostrarMenus(UIManager.Menus["Qui Vols Atacar?"], True)
        
    return target

def UseObject(jugador, equip, obj, combat = False):
    target = TriarObjectius(equip)
    if target != None:
        obj.Utilitzar(jugador.Team[target])
        if jugador.objectes[obj.id]["amount"] > 1:
            jugador.objectes[obj.id]["amount"] -= 1
        else:
            jugador.objectes.pop(obj)
        UIManager.CrearMenu(jugador.objectes.items(), "Motxila", "Objectes", opcionsvisibles=6)
        if combat == False:
            return ""
    else:
        return None
        

def Fugir(enemy, jugador):
    print("Has intentat Fugir...")
    teamSPD = 0
    for i in jugador.Team.values():
        teamSPD += i.StatsCombat["SPD"]
    enemySPD = 0
    for j in enemy.values():
        enemySPD += j.StatsCombat["SPD"]
    prob = jugador.fleeProb * (teamSPD / enemySPD)   # fleeProb = 75 de base
   
    # 75% base * resultat de velocitat del jugador entre la del enemic. (75 * (22 / 20) = 1.1) = 82.5)
    if prob < 100:
        fugir = random.choices([True, False], cum_weights=[prob, 100 - prob])
    else:
        fugir = [True]
    if fugir[0] == True:
        print("Has aconseguit escapar !!")
    else:
        print("No has aconseguit escapar...")
    return fugir