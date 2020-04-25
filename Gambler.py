import random
from typing import Tuple, Dict, Any

class Gamble:

    def __init__(self):
        # Holds wagers keyed to user IDs
        self.bets = dict()
        self.cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


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
                return (bets[user] * 2), "You won-a! Congradyulasiones!", rolls
            else:
                return 0, "Mama mia! You-a lost-a!", rolls
        else:
            rolls.append(0)
            rolls.append(0)
            rolls.append(0)
            return 0, "You-a stupido! You place-a no bet-a!", rolls
