import tkinter as tk
from PIL import Image, ImageTk
import random
import numpy as np
from OuiSiAI import compareTwo
import copy

root = tk.Tk()
root.title("OuiSi!")
pathRoot = "../Downloads/OuiSiOG/"
box = Image.open(pathRoot+"box.png")  
box = ImageTk.PhotoImage(box)
cardDeck = list(range(1,210))
random.shuffle(cardDeck)
matchDict = {}
openImages = {} #id: opened img object
buttonGrid  = [] #2d array of button objects
board = np.zeros((6,12))
handCardSelected = (-1,(-1,-1)) #(imNum, (row, col))

def on_button_click(boardOrHand,imNum, boardCoords):
    """
    Input: boardOrHand, a string either "board" or "hand", 
    imNum an int representing the image number, boardCoords a tuple of ints in form (row, col)
    Output: None
    """
    global handCardSelected
    global cardDeck
    allOpenSpaces = getAllOpenCards()
    allOpenSpaces = [x[1] for x in allOpenSpaces]
    if boardOrHand == "board" and handCardSelected[0] > 0:
        if boardCoords in allOpenSpaces:
            #board update
            boardPath = pathRoot+"ouisi-nature-"+str(0)*(3-len(str(handCardSelected[0])))+str(handCardSelected[0])+".jpg"
            openImages["img"+str(handCardSelected[0])] = Image.open(boardPath)
            openImages["img"+str(handCardSelected[0])] = openImages["img"+str(handCardSelected[0])].resize((80,80))
            openImages["img"+str(handCardSelected[0])] = ImageTk.PhotoImage(openImages["img"+str(handCardSelected[0])])
            buttonGrid[boardCoords[0]][boardCoords[1]].configure(image = openImages["img"+str(handCardSelected[0])])
            board[boardCoords[0]][boardCoords[1]] = handCardSelected[0]

            #handupdate
            newCard = cardDeck[0]
            handPath = pathRoot+"ouisi-nature-"+str(0)*(3-len(str(newCard)))+str(newCard)+".jpg"
            openImages["img"+str(newCard)]  = Image.open(handPath)
            openImages["img"+str(newCard)] = openImages["img"+str(newCard)].resize((160,160))
            openImages["img"+str(newCard)] = ImageTk.PhotoImage(openImages["img"+str(newCard)])
            coords = handCardSelected[1] # (row, col)
            buttonGrid[coords[0]][coords[1]].configure(image = openImages["img"+str(newCard)])
            buttonGrid[coords[0]][coords[1]].configure(command=lambda newCard=newCard: on_button_click("hand", newCard, coords))
            cardDeck = cardDeck[1:]
            handCardSelected = (-1, (-1,-1))
            aiTurn()
        else:
            print("That space is not open!")
    elif boardOrHand == "board" and handCardSelected[0] <=0:
        print("Click a card in your hand before choosing a place on the board!")
    elif boardOrHand == "hand":
        handCardSelected = (imNum,boardCoords)
        print("Selected card from hand! Now click on a space on the board to place it!")


    
for row in range(6):
    buttonRow = []
    for col in range(12):
        board_id=0
        if (row==2 and col==5):
            board_id = cardDeck[0]
            board[row][col] = board_id

            filepath = pathRoot+"ouisi-nature-"+str(0)*(3-len(str(board_id)))+str(board_id)+".jpg"
            openImages["img"+str(board_id)] = Image.open(filepath)
            openImages["img"+str(board_id)] = openImages["img"+str(board_id)].resize((80,80))
            openImages["img"+str(board_id)] = ImageTk.PhotoImage(openImages["img"+str(board_id)])
            im = openImages["img"+str(board_id)]

            cardDeck = cardDeck[1:]
        else:
            im=box
        button = tk.Button(
                root,
                image = im,
                width=80,
                height=80,
                command=lambda row=row, col=col: on_button_click("board", 0, (row, col)),
        )
        buttonRow.append(button)
        button.grid(row=row, column=col, padx=1, pady=1)
    buttonGrid.append(buttonRow)

handRow = []
for column in range(0,10,2):
    id = cardDeck[0]
    filepath = pathRoot+"ouisi-nature-"+str(0)*(3-len(str(id)))+str(id)+".jpg"
    openImages["img"+str(id)] = Image.open(filepath,)
    openImages["img"+str(id)] = openImages["img"+str(id)].resize((160,160))
    openImages["img"+str(id)] = ImageTk.PhotoImage(openImages["img"+str(id)])
    cardDeck = cardDeck[1:]
    if column == 0:
        colCoord = 0
    else:
        colCoord = int(column/2)
    button = tk.Button( 
        root,
        image=openImages["img"+str(id)],
        width=160,
        height=160,
        command=lambda id=id,colCoord=colCoord: on_button_click("hand", id, (6,colCoord)),
    )
    handRow.append(button)
    button.grid(row=6, column=column, padx=1, pady=1, columnspan=2, rowspan=2)

buttonGrid.append(handRow)

aiHand = cardDeck[:6]
cardDeck = cardDeck[6:]

# AIhandRow = []
# for column in range(0,10,2):
#     if column == 0:
#         colCoord = 0
#     else:
#         colCoord = int(column/2)
#     filepath = pathRoot+"ouisi-nature-"+str(0)*(3-len(str(aiHand[colCoord])))+str(aiHand[colCoord])+".jpg"
#     openImages["img"+str(aiHand[colCoord])] = Image.open(filepath,)
#     openImages["img"+str(aiHand[colCoord])] = openImages["img"+str(aiHand[colCoord])].resize((160,160))
#     openImages["img"+str(aiHand[colCoord])] = ImageTk.PhotoImage(openImages["img"+str(aiHand[colCoord])])
#     button = tk.Button( 
#         root,
#         image=openImages["img"+str(aiHand[colCoord])],
#         width=160,
#         height=160
#     )
#     AIhandRow.append(button)
#     button.grid(row=8, column=column, padx=1, pady=1, columnspan=2, rowspan=2)

# buttonGrid.append(handRow)

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
    global cardDeck
    bestScore = [(0,0), 0, 0] #(card matched with, card played, score)

    #find best match
    boardCards = getAllOpenCards()
    for card in aiHand:
        for match in boardCards:
            newScore = score(card, int(match[0]))
            if newScore > bestScore[2]:
                bestScore[0] = match[1]
                bestScore[1] = card
                bestScore[2] = newScore
                
    #play card
    # print("The best match was card " + str(bestScore[1]) + " with score " + str(bestScore[2]))
    imgPath = pathRoot+"ouisi-nature-"+str(0)*(3-len(str(bestScore[1])))+str(bestScore[1])+".jpg"
    openImages["img"+str(bestScore[1])] = Image.open(imgPath)
    openImages["img"+str(bestScore[1])] = openImages["img"+str(bestScore[1])].resize((80,80))
    openImages["img"+str(bestScore[1])] = ImageTk.PhotoImage(openImages["img"+str(bestScore[1])])
    buttonGrid[bestScore[0][0]][bestScore[0][1]].config(image = openImages["img"+str(bestScore[1])])
    board[bestScore[0]] = bestScore[1]

    #draw card
    aiHand.remove(bestScore[1])
    aiHand.append(cardDeck[0])
    cardDeck = cardDeck[1:]
    # print(board)

root.mainloop()