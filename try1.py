import random

joueurs = {}


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
    tours=0
    createplayers(n,money)
    if time==0:
        while True:
            play(tours%n)
            tours +=1
            if tours%n==0 :
                if gamevalidity(n)==False:
                    break
    else:
        for j in range(0,time):
            play(tours%n)
            tours +=1
            

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
    if joueurs[f"joueur{i}"]["pos"] in [1,3,6,8,9,11,13,14,16,18,19,21,23,24,26,27,29,31,32,34,37,39]: onproprio(i)
    elif joueurs[f"joueur{i}"]["pos"] in [5,15,25,35]: ontrain(i)
    elif joueurs[f"joueur{i}"]["pos"] in [7,22,36]: onluck(i)
    elif joueurs[f"joueur{i}"]["pos"] == 30:
        joueurs[f"joueur{i}"]["pos"]=10
        joueurs[f"joueur{i}"]["jailtile"]=3


def gamevalidity(n):
    number=0
    for k in range(0,n):
        if joueurs[f"joueur{k}"]["validity"]==True: number +=1
    if number<2 : return False
    else: return True

def onproprio(i):
    print("joueur ",i," sur la case ",joueurs[f"joueur{i}"]["pos"])

def ontrain(i):
    print("joueur ",i," sur la case ",joueurs[f"joueur{i}"]["pos"])

def onluck(i):
    print("joueur ",i," sur la case ",joueurs[f"joueur{i}"]["pos"])



    
