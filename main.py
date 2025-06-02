from random import *
import math

casedepart=0
nbcases = 12
maisondessus = 0
a=1

indappart = [1,2,4,5,7,8,10,11]

def de():
    return randint(1,6)

def creerjoueurs(n):
    joueurs = {}
    for i in range(0,n):
        joueurs[f'joueur{i}'] = {'case': 0, 'argent': 200, 'propriete': [], 'validite': True, 'prison':0}
    return joueurs

def creerimmobilier(n):
    immobilier = {}
    for i in range(1,n+1):
       immobilier[f'appart{i}'] = {'indice': i, 'dispo': True, 'prix': 30+10*i, 'loyer': 10+2*i, 'case':math.trunc(i*1.4), 'proprietaire':0}
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
    for p in range(0,nbtours*nbjoueurs):
        i=p%nbjoueurs
        if joueurs[f'joueur{i}']['validite'] == False : a=1
        elif joueurs[f'joueur{i}']['prison'] != 0: joueurs[f'joueur{i}']['prison'] -= 1
        else:
            move = de()
            if joueurs[f'joueur{i}']['case'] > (joueurs[f'joueur{i}']['case']+move)%nbcases : joueurs[f'joueur{i}']['argent']+=casedepart
            joueurs[f'joueur{i}']['case'] = (joueurs[f'joueur{i}']['case']+move)%nbcases
            if joueurs[f'joueur{i}']['case'] in indappart:
                for j in immobilier:
                    if immobilier[j]['case']==joueurs[f'joueur{i}']['case']:
                        maisondessus = immobilier[j]
                        caseappart = immobilier[j]['case']
                        indiceappart = immobilier[j]['indice']
                if immobilier[j]['dispo']==True:
                    if joueurs[f'joueur{i}']['argent']>immobilier[j]['prix'] :
                        (joueurs[f'joueur{i}']['propriete']).append(immobilier[j]['case'])
                        joueurs[f'joueur{i}']['argent'] -= immobilier[j]['prix']
                        immobilier[f'appart{indiceappart}']['dispo']=False
                else:
                    if joueurs[f'joueur{i}']['argent']>immobilier[j]['loyer']:
                        joueurproprio = immobilier[j]['proprietaire']
                        joueurs[f'joueur{i}']['argent'] -= immobilier[j]['loyer']
                        joueurs[f'joueur{i}']['argent'] += immobilier[j]['loyer']
                    else:
                        joueurs[f'joueur{i}']['validite'] = False
                        nbrestant -= 1
    return joueurs

                
                        
            
        
    def caca():
        for i in range(1,9):
            print(math.truc(i*1.49))
            
    
    
    
    
