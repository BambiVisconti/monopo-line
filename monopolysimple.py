import random
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, LongTable, TableStyle
from reportlab.lib.units import mm


joueurs = {}
tours=0
aquidejouer=0
quartier=[-1,-1,-1,-1]
houses=[0 for j in range(12)]
ROI=[0 for h in range(12)]
hot=[0 for j in range(12)]
owners=[-1 for j in range(12)]
price=[0,40,60,0,120,140,0,200,220,0,300,350]
revenu=[0 for i in range(12)]
rent=[int(j/7) for j in price]
timestamp=[0 for i in range(12)]
taxes = 0
matrice= [[0 for i in range(12)] for j in range(12)]

def inigame():
    joueurs = {}
    tours=0
    aquidejouer=0
    quartier=[-1,-1,-1,-1]
    houses=[0 for j in range(12)]
    ROI=[0 for h in range(12)]
    hot=[0 for j in range(12)]
    owners=[-1 for j in range(12)]
    price=[0,40,60,0,120,140,0,200,220,0,300,350]
    revenu=[0 for i in range(12)]
    rent=[int(j/7) for j in price]
    timestamp=[0 for i in range(12)]
    taxes = 0
    matrice= [[0 for i in range(12)] for j in range(12)]

    

def matricedecon(n,money,time):
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
                    matricebien(tours)
                    matrix_to_pdf(matrice,"matrixfacile.pdf")
                    break
    else:
        for j in range(0,time):
            play(aquidejouer%n)
        matricebien(tours)
        matrix_to_pdf(matrice,"matrixfacile.pdf")

def strategiedachatmaison(i):
    place=joueurs[f"joueur{i}"]["pos"]
    taro=50*int(place/3) + 50
    if i!=0:
        if joueurs[f"joueur{i}"]["money"] > taro*2: buyhouse(i)
    else:
        if joueurs[f"joueur{i}"]["money"] > taro*1.5: buyhouse(i)
        

def buyhouse(i):
    place=joueurs[f"joueur{i}"]["pos"]
    if quartier[int(place/3)]==i and houses[place]<6:
        taro=50*int(place/3) + 50
        if joueurs[f"joueur{i}"]["money"]>taro:
            houses[place]+=1
            joueurs[f"joueur{i}"]["money"] -= taro
            

def verifierquartier():
    for j in range(11):
        if owners[j]==owners[j+1] and owners[j]!=-1:
            quartier[int(j/3)]= owners[j]

def matricebien(t):
    for i in range(12):
        for j in range(12):
            matrice[i][j]=round(((matrice[i][j])*100)/t,2)

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
    inigame()
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
            if aquidejouer%n==0 :
               if gamevalidity(n)==False:
                   endgame(n)
                   break
        if gamevalidity(n)==True:
            endgame(n)
            

def roll(i):
    first=random.randint(1, 3)
    return first

def play(i):
    global aquidejouer
    #print(joueurs[f"joueur{i}"]["pos"])
    #print(joueurs[f"joueur{i}"]["jailtime"])
    #print(i)
    dices = roll(i)
    if joueurs[f"joueur{i}"]["jailtime"]>0: joueurs[f"joueur{i}"]["jailtime"] += -1
    elif joueurs[f"joueur{i}"]["validity"] == False: aquidejouer+=1 #rien return juste continuer
    else:
        if joueurs[f"joueur{i}"]["pos"] + dices >11: joueurs[f"joueur{i}"]["money"]+=150
        before = joueurs[f"joueur{i}"]["pos"]
        joueurs[f"joueur{i}"]["pos"] = (joueurs[f"joueur{i}"]["pos"] + dices)%12
        after=joueurs[f"joueur{i}"]["pos"]
        matrice[before][after]+=1
        aquidejouer+=1
        position(i)
        
        
def position(i):
    global tours
    tours+=1
    if joueurs[f"joueur{i}"]["pos"] in [1,2,4,5,7,8,10,11]: onproprio(i)
    elif joueurs[f"joueur{i}"]["pos"] == 9:
        joueurs[f"joueur{i}"]["pos"]=3
        hot[joueurs[f"joueur{i}"]["pos"]]+=1
        joueurs[f"joueur{i}"]["jailtime"]=3
        hot[9]+=1
    else:
        hot[joueurs[f"joueur{i}"]["pos"]]+=1

def playervalidity(i):
    if joueurs[f"joueur{i}"]["money"] < 0:
        joueurs[f"joueur{i}"]["validity"]=False
        for k in range(12):
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
    if owners[place]==i:
        strategiedachatmaison(i)
    elif owners[place]==-1:
        if joueurs[f"joueur{i}"]["money"]> 1.5*(price[place]):
            owners[place]=i
            timestamp[place]=tours
            verifierquartier()
            joueurs[f"joueur{i}"]["money"] += -price[place]
            #print("le joueur ",i," achete propriété ",place)
    else:
        loyer=(rent[place])*(2**(houses[place]))
        owner=owners[place]
        joueurs[f"joueur{i}"]["money"] += -loyer
        joueurs[f"joueur{owner}"]["money"] += loyer
        revenu[place] += loyer
        playervalidity(i)
        #print("le joueur ",i," tombe chez le joueur ",owner," et lui reste $",joueurs[f"joueur{i}"]["money"])
        
def calculROI():
    for h in range(12):
        if price[h]==0: ROI[h]=0
        else: ROI[h]= int((revenu[h]*(tours-timestamp[h]))/(tours*price[h]))

def endgame(n):
    for j in range(12):
        hot[j]=100*((hot[j])/tours)
    print("La partie a durée ",int(aquidejouer/n)," tours")
    calculROI()
    print("ROI:",ROI)
    print("REVENU:", revenu)
    print("HOUSES:", houses)
    print("QUARTIERS", quartier)
    print(joueurs)
    print(owners)
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





def matrix_to_pdf(matrix, filename="matrix.pdf", header=False):
    # Normalisation: liste de listes
    try:
        import numpy as np, pandas as pd
    except Exception:
        np = pd = None

    if pd is not None and isinstance(matrix, pd.DataFrame):
        data = [list(matrix.columns)] + matrix.values.tolist() if header else matrix.values.tolist()
    elif np is not None and isinstance(matrix, np.ndarray):
        data = matrix.tolist()
    else:
        data = [list(row) for row in matrix]

    if not data:
        raise ValueError("Matrice vide")

    # Vérif rectangulaire
    w = len(data[0])
    if any(len(r) != w for r in data):
        raise ValueError("Toutes les lignes doivent avoir la même longueur")

    # Doc paysage A4 avec petites marges
    doc = SimpleDocTemplate(
        filename,
        pagesize=landscape(A4),
        leftMargin=10*mm, rightMargin=10*mm,
        topMargin=0*mm, bottomMargin=0*mm
    )

    # Largeur utile (en points)
    available_w = doc.pagesize[0] - doc.leftMargin - doc.rightMargin

    # Réduction: largeur de chaque colonne pour tenir dans la page
    col_w = available_w / w
    colWidths = [col_w] * w

    # Table longue (se coupe verticalement si beaucoup de lignes)
    tbl = LongTable(data, colWidths=colWidths, repeatRows=1 if header else 0)

    # Style compact pour "dézoomer"
    tbl.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.3, colors.black),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("FONTSIZE", (0,0), (-1,-1), 6),           # ← petite police
        ("TOPPADDING", (0,0), (-1,-1), 1),
        ("BOTTOMPADDING", (0,0), (-1,-1), 1),
        ("LEFTPADDING", (0,0), (-1,-1), 1),
        ("RIGHTPADDING", (0,0), (-1,-1), 1),
    ]))

    if header:
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.grey),
            ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ]))

    doc.build([tbl])
