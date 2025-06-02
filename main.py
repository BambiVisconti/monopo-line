from random import *
import math
import time

casedepart=3
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
        joueurs[f'joueur{i}'] = {'indice': i, 'case': 0, 'argent': 200, 'propriete': [], 'validite': True, 'prison':0}
    return joueurs

def creerimmobilier(n):
    immobilier = {}
    for i in range(0,n):
       immobilier[f'appart{i}'] = {'indice': i, 'dispo': True, 'prix': 30+10*i, 'loyer': 10+2*i, 'case':permutation(i) , 'proprietaire':-1}
    return immobilier
    

def chance(i):
    ent=randint(1,4)
    if ent==1: joueurs[f'joueur{i}']['argent'] -= 10
    if ent==2: joueurs[f'joueur{i}']['argent'] += 10
    if ent==3:
        joueurs[f'joueur{i}']['case'] = 4
        joueurs[f'joueur{i}']['prison']= 3
    if ent==4:
        joueurs[f'joueur{i}']['case'] = 0
        joueurs[f'joueur{i}']['argent'] += casedepart

def simulation(nbjoueurs,nbtours,nbappart):
    joueurs = creerjoueurs(nbjoueurs)
    immobilier = creerimmobilier(nbappart)
    nbrestant = nbjoueurs
    p=0
    while nbrestant != 1:
        time.sleep(0.02)
        i=p%nbjoueurs
        p+=1
        if joueurs[f'joueur{i}']['validite'] == False : a=1
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
                        joueurs[f'joueur{i}']['propriete'].append(maisondessus['case'])
                        joueurs[f'joueur{i}']['argent'] -= maisondessus['prix']
                        immobilier[f'appart{indiceappart}']['dispo'] = False
                        immobilier[f'appart{indiceappart}']['proprietaire'] = i
                else:
                    if joueurs[f'joueur{i}']['argent'] > maisondessus['loyer']:
                        joueurproprio = maisondessus['proprietaire']
                        joueurs[f'joueur{i}']['argent'] -= maisondessus['loyer']
                        joueurs[f'joueur{joueurproprio}']['argent'] += maisondessus['loyer']
                    else:
                        joueurs[f'joueur{i}']['validite'] = False
                        nbrestant -= 1
            else:
                if joueurs[f'joueur{i}']['case']==0: joueurs[f'joueur{i}']['argent']+=2
                if joueurs[f'joueur{i}']['case']==3: print("le joueur ",i," visite la prison")
                if joueurs[f'joueur{i}']['case']==6:
                    joueurs[f'joueur{i}']['prison']=2
                    joueurs[f'joueur{i}']['case']=2
                if joueurs[f'joueur{i}']['case']==9:
                    #chance(i)
                    print("carte chance!")

                    

        print("Le joueur", i, " qui est en ",joueurs[f'joueur{i}']['case'],"a", joueurs[f'joueur{i}']['argent'],"e et a les appart ",joueurs[f'joueur{i}']['propriete'], joueurs[f'joueur{i}']['validite'])
    for k in joueurs:
        if joueurs[k]['validite']==True: return ("caca",joueurs[k]['indice'])
    

                
                        
            
        

    
    
    
    
