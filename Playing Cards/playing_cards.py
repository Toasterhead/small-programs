#A solution to Chapter 1, Exercise 14 of the book Problem Solving with Algorithms and Data Structures Using Python.

#Simulates a deck of cards and provides a function automatically playing a game of War.

import random

class Card(object):
    """Class for a playing card."""

    TWO     = 0
    THREE   = 1
    FOUR    = 2
    FIVE    = 3
    SIX     = 4
    SEVEN   = 5
    EIGHT   = 6
    NINE    = 7
    TEN     = 8
    JACK    = 9
    QUEEN   = 10
    KING    = 11
    ACE     = 12

    HEARTS      = 0
    DIAMONDS    = 1
    SPADES      = 2
    CLUBS       = 3

    def __init__(self, rank, suit):

        assert type(rank) is int and rank >= Card.TWO   
        assert type(suit) is int and suit >= Card.HEARTS and suit <= Card.CLUBS
        
        self.rank = rank
        self.suit = suit

    @property
    def Rank(self): return self.rank
    @property
    def Suit(self): return self.suit
    
    def is_red(self):
        
        if (self.suit == HEARTS or self.suit == DIAMONDS):return True

        return False

    def __str__(self):

        sRank = ""
        sSuit = ""

        if   self.rank == Card.TWO:     sRank = "Two"
        elif self.rank == Card.THREE:   sRank = "Three"
        elif self.rank == Card.FOUR:    sRank = "Four"
        elif self.rank == Card.FIVE:    sRank = "Five"
        elif self.rank == Card.SIX:     sRank = "Six"
        elif self.rank == Card.SEVEN:   sRank = "Seven"
        elif self.rank == Card.EIGHT:   sRank = "Eight"
        elif self.rank == Card.NINE:    sRank = "Nine"
        elif self.rank == Card.TEN:     sRank = "Ten"
        elif self.rank == Card.JACK:    sRank = "Jack"
        elif self.rank == Card.QUEEN:   sRank = "Queen"
        elif self.rank == Card.KING:    sRank = "King"
        elif self.rank == Card.ACE:     sRank = "Ace"
        else:                           return  "Joker"

        if   self.suit == Card.HEARTS:      sSuit = "Hearts"
        elif self.suit == Card.DIAMONDS:    sSuit = "Diamonds"
        elif self.suit == Card.SPADES:      sSuit = "Spades"
        elif self.suit == Card.CLUBS:       sSuit = "Clubs"

        return sRank + " of " + sSuit

def create_deck():
    """Creates and returns a standard deck of 52 playing cards."""

    deck = []

    for suit in range(4):
        for rank in range(13): deck.append(Card(rank, suit))

    return deck

def shuffle(deck):
    """Shuffles a deck of cards based on the indicated size of the deck."""

    assert type(deck) is list

    size = len(deck)
    random.seed()
    
    for i in range(10 * size):
        drawn = deck.pop()
        deck.insert(random.randint(0, size - 1), drawn)
    
def deal(deck, numCards, numPlayers):
    """Returns an array of hands containing the specified number of cards from
    the given deck."""

    assert type(deck)       is list
    assert type(numCards)   is int and numCards     >= 0
    assert type(numPlayers) is int and numPlayers   >= 0

    hands = [[] for i in range(numPlayers)]

    for i in range(numPlayers):
        for j in range(numCards):
            if (len(deck) > 0): hands[i].append(deck.pop())

    return hands

def play_war(playerOne, playerTwo, printingOn = True):
    """The computer plays war based on the two hands provided."""

    assert type(playerOne) is list and len(playerOne) == 26
    assert type(playerTwo) is list and len(playerTwo) == 26

    turns = 0

    gainedOne = []
    gainedTwo = []

    playerOneWins = len(playerOne) == 0 and len(gainedOne) == 0
    playerTwoWins = len(playerTwo) == 0 and len(gainedTwo) == 0

    while ((not playerOneWins) and (not playerTwoWins)):

        drawOne = []
        drawTwo = []

        if sub_play_war(
                playerOne,
                playerTwo,
                drawOne,
                drawTwo,
                gainedOne,
                gainedTwo,
                printingOn) == -1: break

        if printingOn:
            print(
                "Player one now has " +
                str(len(playerOne) + len(gainedOne)) +
                " cards.")
            print(
                "Player two now has " +
                str(len(playerTwo) + len(gainedTwo)) +
                " cards.")
            print()

        turns += 1

        playerOneWins = len(playerOne) == 0 and len(gainedOne) == 0
        playerTwoWins = len(playerTwo) == 0 and len(gainedTwo) == 0

    result = ""
    
    if (playerOneWins): result += "Player one wins the game.\n"
    else:               result += "Player two wins the game.\n"

    result += str(turns) + " turns were taken.\n"

    if printingOn: print(result)

    return result

def sub_play_war(
    playerOne,
    playerTwo,
    drawOne,
    drawTwo,
    gainedOne,
    gainedTwo,
    printingOn):
    """Draws, compares, and then reassigns cards for each turn. Is called
    recursively in the event of a tie."""

    play_war_check(playerOne, playerTwo, gainedOne, gainedTwo)

    try:
        drawOne.append(playerOne.pop())
        drawTwo.append(playerTwo.pop())
    except: return -1

    if printingOn: 
        print("Player one draws the " + str(drawOne[len(drawOne) - 1]) + ".")
        print("Player two draws the " + str(drawTwo[len(drawTwo) - 1]) + ".")

    play_war_check(playerOne, playerTwo, gainedOne, gainedTwo)

    drawOneLength = len(drawOne)
    drawTwoLength = len(drawTwo)

    if   drawOne[len(drawOne) - 1].Rank > drawTwo[len(drawTwo) - 1].Rank:
        for i in range(drawOneLength): gainedTwo.append(drawOne.pop())
        for i in range(drawTwoLength): gainedTwo.append(drawTwo.pop())
        if printingOn: print("Player one beats player two.")
    elif drawTwo[len(drawTwo) - 1].Rank > drawOne[len(drawOne) - 1].Rank:
        for i in range(drawOneLength): gainedOne.append(drawOne.pop())
        for i in range(drawTwoLength): gainedOne.append(drawTwo.pop())
        if printingOn: print("Player two beats player one.")
    else:
        if printingOn: print("It's a tie. Drawing again...")
        if sub_play_war(
            playerOne,
            playerTwo,
            drawOne,
            drawTwo,
            gainedOne,
            gainedTwo,
            printingOn) == -1: return -1

def play_war_check(playerOne, playerTwo, gainedOne, gainedTwo):
    """Performs a check to see if a player has run out of cards in his or her
    hand and, if so, reassigns cards accordingly."""

    if len(playerOne) == 0:
        shuffle(gainedOne)
        gainedLength = len(gainedOne)
        for i in range(gainedLength): playerOne.append(gainedOne.pop())
        
    if len(playerTwo) == 0:
        shuffle(gainedTwo)
        gainedLength = len(gainedTwo)
        for i in range(gainedLength): playerTwo.append(gainedTwo.pop())

def auto_run_war(rounds = 1, printingOn = False):

    for i in range(rounds):
        deck = create_deck()
        shuffle(deck)
        hands = deal(deck, 26, 2)
        if not printingOn: print(play_war(hands[0], hands[1], printingOn))
