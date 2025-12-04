import tkinter as tk
from PIL import Image, ImageTk
import random
import numpy as np
from OuiSiAI import compareTwo

root = tk.Tk()
root.title("OuiSi!")
pathRoot = "../Downloads/OuiSiOG/"
box = Image.open(pathRoot+"box.png")  
box = ImageTk.PhotoImage(box)
cardDeck = list(range(1,210))
random.shuffle(cardDeck)
matchDict = {}
openImages = {}
board = np.zeros((6,12))

for row in range(6):
    for col in range(12):
        if (row==2 and col==5):
            filepath = pathRoot+"ouisi-nature-"+str(0)*(3-len(str(cardDeck[0])))+str(cardDeck[0])+".jpg"
            openImages["imgstarter"] = Image.open(filepath)
            openImages["imgstarter"] = ImageTk.PhotoImage(openImages["imgstarter"])
            im = openImages["imgstarter"]
            cardDeck = cardDeck[1:]
        else:
            im=box,
        tk.Button(
                root,
                image = im,
                width=80,
                height=80
        ).grid(row=row, column=col, padx=1, pady=1)

for column in range(0,10,2):
    filepath = pathRoot+"ouisi-nature-"+str(0)*(3-len(str(cardDeck[0])))+str(cardDeck[0])+".jpg"
    openImages["img"+str(column)] = Image.open(filepath)
    openImages["img"+str(column)] = ImageTk.PhotoImage(openImages["img"+str(column)])
    cardDeck = cardDeck[1:]
    tk.Button(
        root,
        image=openImages["img"+str(column)],
        width=160,
        height=160
    ).grid(row=6, column=column, padx=1, pady=1, columnspan=2, rowspan=2) 

aiHand = cardDeck[:6]
cardDeck = cardDeck[6:]

def score(card, match):
    cardPath = pathRoot+"ouisi-nature-"+str(0)*(3-len(str(card)))+str(card)+".jpg"
    matchPath = pathRoot+"ouisi-nature-"+str(0)*(3-len(str(match)))+str(match)+".jpg"
    if card < match:
        if str(card)+str(match) in matchDict:
            return matchDict[str(card)+str(match)]
        else:
            score = compareTwo(cardPath, matchPath)
            matchDict[str(card)+str(match)] = score
            return score
    else:
        if str(match)+str(card) in matchDict:
            return matchDict[str(match)+str(card)]
        else:
            score = compareTwo(cardPath, matchPath)
            matchDict[str(match)+str(card)] = score
            return score



def playerTurn():
    """
    let player click own card and place on board
    update board 2d array
    """
    #play card
    #dont forget to draw card

def getAllOpenCards():
    """
    input: none
    output: numbers of all images on board
    """
    return 0

def aiTurn():
    bestScore = (0, 0, 0) #(card matched with, card played, score)
    boardCards = getAllOpenCards()
    for card in aiHand:
        for match in boardCards:
            newScore = score(card, match)
            if newScore > bestScore[2]:
                bestScore[0] = match
                bestScore[1] = card
                bestScore[2] = newScore
                
    #play card, draw card



root.mainloop()
#figure out how to take turns :D