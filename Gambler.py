import random
from typing import Tuple, Dict, Any

class Gamble:

    # Holds wagers keyed to user IDs
    bets = dict()


    def __init__(self):
        a = 0 # filler


    def setBet(self, wager, user):
        global bets
        bets[user] = wager


    def get_bet(self, user):
        return bets[user]


    def roll_slots(self, user):
        rolls = []

        global bets

        if bets[user] is not None:
            for i in range(0,2):
                rolls.append(random.randint(0,9))

            if rolls[0] == rolls[1] and rolls[1] == rolls[2]:
                return 1, (bets[user] * 2)
            else:
                return 0, 0
        else:
            return 2, 0
