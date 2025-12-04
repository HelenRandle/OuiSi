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

def on_button_click(self, boardOrHand):
    button_id = button_var.get()
    print(f"The ID of the button is: {button_id}")
    return

for row in range(6):
    for col in range(12):
        board_id=0
        if (row==2 and col==5):
            board_id = cardDeck[0]
            board[row][col] = board_id

            filepath = pathRoot+"ouisi-nature-"+str(0)*(3-len(str(board_id)))+str(board_id)+".jpg"
            openImages["img"+str(board_id)] = Image.open(filepath)
            openImages["img"+str(board_id)] = ImageTk.PhotoImage(openImages["img"+str(board_id)])
            im = openImages["img"+str(board_id)]

            cardDeck = cardDeck[1:]
        else:
            im=box
        button_var = tk.StringVar(value=str(board_id))
        button = tk.Button(
                root,
                image = im,
                width=80,
                height=80,
                command=lambda: on_button_click(self, "board"),
                textvariable=button_var
        ).grid(row=row, column=col, padx=1, pady=1)

for column in range(0,10,2):
    id = cardDeck[0]
    filepath = pathRoot+"ouisi-nature-"+str(0)*(3-len(str(id)))+str(id)+".jpg"
    openImages["img"+str(id)] = Image.open(filepath,)
    openImages["img"+str(id)] = ImageTk.PhotoImage(openImages["img"+str(id)])
    cardDeck = cardDeck[1:]
    button_var = tk.StringVar(value=str(id))
    tk.Button( 
        root,
        image=openImages["img"+str(id)],
        width=160,
        height=160,
        command=lambda: on_button_click(self, "hand"),
        textvariable=button_var
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

def inRange(r,c):
    return 0 <= r < 6 and 0 <= c < 12

def getAllOpenCards():
    """
    input: none
    output: numbers and locations of available tiles nearby for of all open images on board
    """
    directions = [(1,0),(-1,0),(0,1),(0,-1)]
    spots = []

    #loop through board
    for r in range(6):
        for c in range(12):
            #check if spot is already taken
            if board[r][c]:
                continue
            #loop through neighbors and check if one of them has an image while the other 3 are empty
            for dr,dc in directions:
                    if not inRange(r+dr,c+dc):
                        continue
                    imgNeighbor = board[r+dr][c+dc]
                    othersEmpty = not any(board[r+dr2][c+dc2] for dr2,dc2 in directions if (dr2,dc2) != (dr,dc) and inRange(r+dr2,c+dc2))
                    if imgNeighbor and othersEmpty:
                        spots.append((imgNeighbor, (r, c)))
    return spots

def aiTurn():
    bestScore = ((0,0), 0, 0) #(card matched with, card played, score)

    #find best match
    boardCards = getAllOpenCards()
    for card in aiHand:
        for match in boardCards:
            newScore = score(card, match[0])
            if newScore > bestScore[2]:
                bestScore[0] = match[1]
                bestScore[1] = card
                bestScore[2] = newScore
                
    #play card
    imgPath = pathRoot+"ouisi-nature-"+str(0)*(3-len(str(bestScore[1])))+str(bestScore[1])+".jpg"
    img = Image.open(imgPath)
    img = ImageTk.PhotoImage(img)
    root[bestScore[0]].configure(image = img)
    board[bestScore[0]] = bestScore[1]

    #draw card
    aiHand.remove(bestScore[1])
    aiHand.append(cardDeck[0])
    cardDeck = cardDeck[1:]

root.mainloop()
#figure out how to take turns :D