import random

class FairRoulette():
    def __init__(self):
        self.pockets = []
        for i in range(1, 37):
            self.pockets.append(i)
        self.ball = None
        self.pocketOdds = len(self.pockets) - 1

    def spin(self):
        self.ball = random.choice(self.pockets)

    def betPocket(self, pocket, amt):
        if pocket == self.ball:
            return amt * self.pocketOdds
        else:
            return -amt

    def __str__(self):
        return 'Fair Roulette'




def play(cant, num, amt):
    plays = []
    ganancia = 0
    perdida = 0
    roulette = FairRoulette()
    for i in range(cant):
        roulette.spin()
        a = roulette.betPocket(num, amt)
        if a > 0:
            ganancia += a
        else:
            perdida += a
    perc = ganancia + perdida
    return perc


