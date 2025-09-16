import random

joueurs = {}
tours=0

hot=[0 for j in range(40)]
owners=[-1 for j in range(40)]
price=[30+5*j for j in range(40)]
rent=[j for j in range(40)]

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
    tours=0
    createplayers(n,money)
    if time==0:
        while True:
            play(tours%n)
            if tours%n==0 :
                if gamevalidity(n)==False:
                    endgame(n)
                    break
    else:
        for j in range(0,time):
            play(tours%n)

        endgame(n)
            

def roll(i):
    first=random.randint(1, 6)
    second=random.randint(1, 6)
    if first == second:
        joueurs[f"joueur{i}"]["jailtime"]=0
    return first + second

def play(i):
    dices = roll(i)
    if joueurs[f"joueur{i}"]["jailtime"]>0: joueurs[f"joueur{i}"]["jailtime"] += -1
    elif joueurs[f"joueur{i}"]["validity"] == False: pass #rien return juste continuer
    else:
        joueurs[f"joueur{i}"]["pos"] = (joueurs[f"joueur{i}"]["pos"] + dices)%40
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
    else:
        tours-=1

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

def onluck(i):
    hot[joueurs[f"joueur{i}"]["pos"]]+=1


def endgame(n):
    for j in range(40):
        hot[j]=(hot[j])/tours
    print("La partie a durée ",int(tours/n)," tours")
    print("les cases chaudes", hot)
    print(joueurs)
    print(owners)
    a=0
    for j in hot: a+=j 
    print(a)
        
    
    
