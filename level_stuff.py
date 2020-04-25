import random
import math


def xp_cap(level):
# Determine and return the amount of xp required to mine a spaghett
#    cap = math.log(level,3)+59.523
#    cap = 3*(math.sqrt(level))+level+50
    cap = 3*(math.sqrt(level))+100
    return float(cap)


def xp_yield(level):
    dividend1 = 3*(level**2)+10
    dividend2 = (level**2)
    xp = (dividend1/dividend2)+10

    return float(xp)
