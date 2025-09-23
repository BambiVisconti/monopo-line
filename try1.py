import random
import matplotlib.pyplot as plt

joueurs = {}
tours=0
aquidejouer=0

hot=[0 for j in range(40)]
owners=[-1 for j in range(40)]
price=[0,60,0,60,200,200,100,0,100,120,0,140,150,140,160,200,280,0,180,200,0,220,0,220,240,200,260,260,150,280,0,300,300,0,320,200,0,350,100,400]
rent=[j for j in range(40)]
trainsowner=[-1,-1,-1,-1]
taxes =0

def createplayers(n, money):
    for i in range(n):
        joueurs[f"joueur{i}"] = {
            "money": money,
            "pos": 0,
            "jailtime": 0,
            "proprio": [],
            "validity": True
        }

def game(n,money,time): #time=0 infini
    global tours
    global taxes
    global aquidejouer
    tours=0
    aquidejouer=0
    createplayers(n,money)
    if time==0:
        while True:
            play(aquidejouer%n)
            if aquidejouer%n==0 :
                if gamevalidity(n)==False:
                    endgame(n)
                    break
    else:
        for j in range(0,time):
            play(aquidejouer%n)

        endgame(n)
            

def roll(i):
    first=random.randint(1, 6)
    second=random.randint(1, 6)
    if first == second:
        joueurs[f"joueur{i}"]["jailtime"]=0
    return first + second

def play(i):
    global aquidejouer
    #print(joueurs[f"joueur{i}"]["pos"])
    #print(joueurs[f"joueur{i}"]["jailtime"])
    #print(i)
    dices = roll(i)
    if joueurs[f"joueur{i}"]["jailtime"]>0: joueurs[f"joueur{i}"]["jailtime"] += -1
    elif joueurs[f"joueur{i}"]["validity"] == False: aquidejouer+=1 #rien return juste continuer
    else:
        if joueurs[f"joueur{i}"]["pos"] + dices >39: joueurs[f"joueur{i}"]["money"]+=200
        joueurs[f"joueur{i}"]["pos"] = (joueurs[f"joueur{i}"]["pos"] + dices)%40
        aquidejouer+=1
        position(i)
        
        
def position(i):
    global tours
    tours+=1
    if joueurs[f"joueur{i}"]["pos"] in [1,3,6,8,9,11,13,14,16,18,19,21,23,24,26,27,29,31,32,34,37,39]: onproprio(i)
    elif joueurs[f"joueur{i}"]["pos"] in [5,15,25,35]: ontrain(i)
    elif joueurs[f"joueur{i}"]["pos"] in [7,22,36]: onluck(i)
    elif joueurs[f"joueur{i}"]["pos"] == 30:
        joueurs[f"joueur{i}"]["pos"]=10
        hot[joueurs[f"joueur{i}"]["pos"]]+=1
        joueurs[f"joueur{i}"]["jailtime"]=3
        hot[30]+=1
    else:
        hot[joueurs[f"joueur{i}"]["pos"]]+=1

def playervalidity(i):
    if joueurs[f"joueur{i}"]["money"] < 0:
        joueurs[f"joueur{i}"]["validity"]=False
        for k in range(40):
            if owners[k]==i: owners[k]= -1


def gamevalidity(n):
    number=0
    for k in range(0,n):
        if joueurs[f"joueur{k}"]["validity"]==True: number +=1
    if number<2 : return False
    else: return True

def onproprio(i):
    hot[joueurs[f"joueur{i}"]["pos"]]+=1
    place = joueurs[f"joueur{i}"]["pos"]
    if owners[place]==i: pass
    elif owners[place]==-1:
        if joueurs[f"joueur{i}"]["money"]> 1.5*(price[place]):
            owners[place]=i
            joueurs[f"joueur{i}"]["money"] += -price[place]
            #print("le joueur ",i," achete propriété ",place)
    else:
        owner=owners[place]
        joueurs[f"joueur{i}"]["money"] += -rent[place]
        joueurs[f"joueur{owner}"]["money"] += rent[place]
        playervalidity(i)
        #print("le joueur ",i," tombe chez le joueur ",owner," et lui reste $",joueurs[f"joueur{i}"]["money"])
        

def ontrain(i):
    hot[joueurs[f"joueur{i}"]["pos"]]+=1
    place = joueurs[f"joueur{i}"]["pos"]
    if owners[place]==i: pass
    elif owners[place]==-1:
        if joueurs[f"joueur{i}"]["money"]> 1.5*(price[place]):
            owners[place]=i
            trainsowner[int((place-5)/10)]=i
            joueurs[f"joueur{i}"]["money"] += -price[place]
            #print("le joueur ",i," achete propriété ",place)
    else:
        owner=owners[place]
        account=trainsowner.count(owner)
        joueurs[f"joueur{i}"]["money"] += -50*account
        joueurs[f"joueur{owner}"]["money"] += 50*account
        playervalidity(i)
        #print("TRAIN",i,owner,account,trainsowner)
        #print("le joueur ",i," tombe chez le joueur ",owner," et lui reste $",joueurs[f"joueur{i}"]["money"])
    

def onluck(i):
    hot[joueurs[f"joueur{i}"]["pos"]]+=1


def endgame(n):
    for j in range(40):
        hot[j]=100*((hot[j])/tours)
    print("La partie a durée ",int(aquidejouer/n)," tours")
    print(joueurs)
    print(owners)
    print(trainsowner)
    a=0
    for j in hot: a+=j 
    print(a)
    plot_hot(hot)
        
    

def plot_hot(hot):
    """
    Affiche un histogramme de l'indice de chaleur (fréquence de passage)
    pour chaque case du plateau Monopoly.
    
    Paramètres
    ----------
    hot : list[int]
        Liste des fréquences de passage, de longueur 40 (une par case).
    """
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(hot)), hot, color="skyblue", edgecolor="black")
    plt.xlabel("Numéro de case du plateau")
    plt.ylabel("Indice de chaleur (fréquence)")
    plt.title("Histogramme des cases chaudes du plateau Monopoly")
    plt.xticks(range(len(hot)))
    plt.show()
