from random import *
import math
import time

casedepart=0
nbcases = 12
maisondessus = 0
a=1

indappart = [1,2,4,5,7,8,10,11]

def de():
    return randint(1,6)

def permutation(i):
    lst=[1,2,4,5,7,8,10,11]
    return lst[i]




def creerjoueurs(n):
    joueurs = {}
    for i in range(0,n):
        joueurs[f'joueur{i}'] = {'indice': i, 'case': 0, 'argent': 300, 'propriete': [], 'validite': True, 'prison':0}
    return joueurs

def creerimmobilier(n):
    immobilier = {}
    for i in range(0,n):
       immobilier[f'appart{i}'] = {'indice': i, 'dispo': True, 'prix': 30+10*i, 'loyer': 10+2*i, 'case':permutation(i) , 'proprietaire':-1}
    return immobilier
    
def perte(i,joueurs,immobilier):
    joueurs[f'joueur{i}']['validite']=False
    joueurs[f'joueur{i}']['argent']=0
    for j in joueurs[f'joueur{i}']['propriete']:
        immobilier[f'appart{j}']['dispo']=True
    joueurs[f'joueur{i}']['propriete']=[]
    print()
    print("LE JOUEUR ",i," EST ELIMINE")
    print()

def chance(i,joueurs,immobilier):
    ent=randint(1,4)
    print(ent)
    if ent==1:
        if joueurs[f'joueur{i}']['argent'] > 5:
            joueurs[f'joueur{i}']['argent'] -= 5
        else:
            perte(i,joueurs,immobilier)
    
    if ent==2: joueurs[f'joueur{i}']['argent'] += 5
    if ent==3:
        joueurs[f'joueur{i}']['case'] = 4
        joueurs[f'joueur{i}']['prison']= 3
    if ent==4:
        joueurs[f'joueur{i}']['case'] = 0
        joueurs[f'joueur{i}']['argent'] += casedepart


def simulation(nbjoueurs,nbtours):
    joueurs = creerjoueurs(nbjoueurs)
    immobilier = creerimmobilier(8)
    nbrestant = nbjoueurs
    p=0
    while nbrestant != 1:
        i=p%nbjoueurs
        p+=1
        if joueurs[f'joueur{i}']['validite'] == False:
            joueurs[f'joueur{i}']['argent']=0
        elif joueurs[f'joueur{i}']['prison'] != 0: joueurs[f'joueur{i}']['prison'] -= 1
        else:
            move = de()
            if joueurs[f'joueur{i}']['case'] > (joueurs[f'joueur{i}']['case']+move)%nbcases : joueurs[f'joueur{i}']['argent']+=casedepart
            joueurs[f'joueur{i}']['case'] = (joueurs[f'joueur{i}']['case']+move)%nbcases
            if joueurs[f'joueur{i}']['case'] in indappart:
                for j in immobilier:
                    if immobilier[j]['case'] == joueurs[f'joueur{i}']['case']:
                        maisondessus = immobilier[j]
                        caseappart = immobilier[j]['case']
                        indiceappart = immobilier[j]['indice']
                        break
                if maisondessus['dispo'] == True:
                    if joueurs[f'joueur{i}']['argent'] > maisondessus['prix']:
                        joueurs[f'joueur{i}']['propriete'].append(maisondessus['indice'])
                        joueurs[f'joueur{i}']['argent'] -= maisondessus['prix']
                        immobilier[f'appart{indiceappart}']['dispo'] = False
                        immobilier[f'appart{indiceappart}']['proprietaire'] = i
                        print("le joueur ",i," achete le bien d'exception ",immobilier[f'appart{indiceappart}']['indice'])
                else:
                    if joueurs[f'joueur{i}']['argent'] > maisondessus['loyer']:
                        joueurproprio = maisondessus['proprietaire']
                        print("le joueur ",i," paye ",maisondessus['loyer']," de loyer au joueur ",maisondessus['proprietaire'])
                        joueurs[f'joueur{i}']['argent'] -= maisondessus['loyer']
                        joueurs[f'joueur{joueurproprio}']['argent'] += maisondessus['loyer']
                    else:
                        perte(i,joueurs,immobilier)
                        nbrestant -= 1
            else:
                if joueurs[f'joueur{i}']['case']==0: joueurs[f'joueur{i}']['argent']+=casedepart
                if joueurs[f'joueur{i}']['case']==3: print("le joueur ",i," visite la prison")
                if joueurs[f'joueur{i}']['case']==6:
                    print("le joueur ",i," part en zonz")
                    joueurs[f'joueur{i}']['prison']=2
                    joueurs[f'joueur{i}']['case']=2
                if joueurs[f'joueur{i}']['case']==9:
                    chance(i,joueurs,immobilier)
                    print("carte chance!")

                    

       #print("Le joueur", i, " qui est en ",joueurs[f'joueur{i}']['case'],"a", joueurs[f'joueur{i}']['argent'],"e et a les appart ",joueurs[f'joueur{i}']['propriete'], joueurs[f'joueur{i}']['validite'])
    for k in joueurs:
        if joueurs[k]['validite']==True:
            print("Le vainqueur est ", joueurs[k]['indice']," avec un patrimoine de ",joueurs[k]['propriete'], "et une fortune de ",joueurs[k]['argent'],"e")
            print("Cette partie a duré ", math.trunc(p/nbjoueurs)+1," tours")

                
                        
            
        

    
    
    
    
