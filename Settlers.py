import random
from collections import defaultdict
from copy import deepcopy
from mcts import mcts
# https://link.springer.com/content/pdf/10.1007%2F978-3-642-17928-0.pdf
# https://news.ycombinator.com/item?id=10209677
# http://mcts.ai/pubs/mcts-survey-master.pdf
tilesToVertices = dict()

tilesToVertices.update(
    {
        1: (1, 2, 3, 4, 5, 6),
        2: (3, 4, 7, 8, 9, 10),
        3: (8, 9, 11, 12, 13, 14),
        4: (5, 6, 15, 16, 17, 18),
        5: (4, 5, 10, 18, 19, 20),
        6: (9, 10, 14, 20, 21, 22),
        7: (13, 14, 22, 23, 24, 25),
        8: (16, 17, 26, 27, 28, 29),
        9: (17, 18, 19, 29, 30, 31),
        10: (19, 20, 21, 31, 32, 33),
        11: (21, 22, 23, 33, 34, 35),
        12: (23, 24, 35, 36, 37, 38),
        13: (28, 29, 30, 39, 40, 41),
        14: (30, 31, 32, 41, 42, 43),
        15: (32, 33, 34, 43, 44, 45),
        16: (34, 35, 36, 45, 46, 47),
        17: (40, 41, 42, 48, 49, 50),
        18: (42, 43, 44, 50, 51, 52),
        19: (44, 45, 46, 52, 53, 54)
    }
)


def getAssociatedTiles(vNum):
    ans = []
    for i in tilesToVertices:
        if vNum in tilesToVertices[i]:
            ans.append(i)
    return ans


roadsList = [
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (1, 6),
    (3, 7),
    (7, 8),
    (8, 9),
    (9, 10),
    (4, 10),
    (8, 11),
    (11, 12),
    (12, 13),
    (13, 14),
    (9, 14),
    (6, 15),
    (5, 18),
    (17, 18),
    (16, 17),
    (15, 16),
    (18, 19),
    (19, 20),
    (10, 20),
    (20, 21),
    (21, 22),
    (14, 22),
    (22, 23),
    (23, 24),
    (24, 25),
    (13, 25),
    (16, 26),
    (26, 27),
    (27, 28),
    (28, 29),
    (17, 29),
    (29, 30),
    (30, 31),
    (19, 31),
    (31, 32),
    (32, 33),
    (21, 33),
    (33, 34),
    (34, 35),
    (23, 35),
    (35, 36),
    (36, 37),
    (37, 38),
    (24, 38),
    (28, 39),
    (39, 40),
    (40, 41),
    (30, 41),
    (41, 42),
    (42, 43),
    (32, 43),
    (43, 44),
    (44, 45),
    (34, 45),
    (45, 46),
    (46, 47),
    (36, 47),
    (40, 48),
    (48, 49),
    (49, 50),
    (42, 50),
    (50, 51),
    (51, 52),
    (44, 52),
    (52, 53),
    (53, 54),
    (46, 54)
]
verticesToTiles = dict()
for i in range(1, 55):
    verticesToTiles.update({i: getAssociatedTiles(i)})

adjacentVertices = defaultdict(list)
for i in range(0, len(roadsList)):
    road = roadsList[i]
    adjacentVertices[road[0]].append(road[1])
    adjacentVertices[road[1]].append(road[0])


class MonteCarloPlayer:
    def __init__(self, pInd):
        self.index = pInd
        return None

    def chooseAction(self, game):
        my_carlo = mcts(self.index, timeLimit=1000)
        action = my_carlo.search(initialState=game)

        return action


class HeuristicPlayer:
    def __init__(self, pInd):
        self.index = pInd
        return None
    
    def chooseAction(self, game):
        actions = game.getPossibleActions()
        settlementActions = []
        cityActions = []
        roadActions = []
        tradeActions = []
        for action in actions:
            if action.isSettlement:
                settlementActions.append(action)
            if action.isCity:
                cityActions.append(action)
            if action.isRoad:
                roadActions.append(action)
            if action.isTrade:
                tradeActions.append(action)
        bestSA = None
        bestSAScore = 0.0
        for sA in settlementActions:
            if bestSA == None:
                bestSA = sA
                bestSAScore = self.scoreVertex(game, sA.index)
            else:
                newScore = self.scoreVertex(game, sA.index)
                if newScore>bestSAScore:
                    bestSAScore = newScore
                    bestSA = sA 
        if bestSA != None:
            return bestSA
        bestCA = None
        bestCAScore = 0.0
        for cA in cityActions:
            if bestCA == None:
                bestCA = cA
                bestCAScore = self.scoreVertex(game, cA.index)
            else:
                newScore = self.scoreVertex(game, cA.index)
                if newScore>bestCAScore:
                    bestCAScore = newScore
                    bestCA = cA 
        if bestCA != None:
            return bestCA
        
        bestRA = None
        bestRAScore = 0.0
        for rA in roadActions:
            if bestRA == None:
                bestRA = rA
                bestRAScore = self.scoreVertex(game, roadsList[rA.index][0]) + self.scoreVertex(game, roadsList[rA.index][1])
            else:
                newScore = self.scoreVertex(game, roadsList[rA.index][0]) + self.scoreVertex(game, roadsList[rA.index][1])
                if newScore>bestRAScore:
                    bestRAScore = newScore
                    bestRA = rA 
        if bestRA != None:
            return bestRA
        for tA in tradeActions:
            if self.index == 0 and game.firstPlayerCards[tA.tradeFrom] > 7:
                return tA 
            if self.index == 1 and game.secondPlayerCards[tA.tradeFrom] > 7:
                return tA
            if self.index == 2 and game.thirdPlayerCards[tA.tradeFrom] > 7:
                return tA
            
        index = random.randint(0, len(actions) - 1)
        action = actions[index]

        return action
    def scoreVertex(self, game, vIndex):
        tiles = getAssociatedTiles(vIndex)
        score = 0.0
        for tile in tiles:
            tile_score = 0.0
            if game.terrains[tile-1] == 1:
                tile_score += 3
            if game.terrains[tile-1] == 2:
                tile_score += 1
            if game.terrains[tile-1] == 3:
                tile_score += 1
            if game.terrains[tile-1] == 4:
                tile_score += 2
            if game.terrains[tile-1] == 5:
                tile_score += 3
            tile_score *= (6.0 - abs(6.0 - game.chances[tile-1])) / 36.0
            score += tile_score
        return score

class RandomPlayer:
    def __init__(self, pInd):
        self.index = pInd
        return None

    def chooseAction(self, game):
        actions = game.getPossibleActions()
        index = random.randint(0, len(actions) - 1)
        action = actions[index]

        return action


class Action:
    def __init__(
        self, pIndex, isRoad, isSettlement, isCity, isTrade, tradeFrom, tradeTo, index, wasFree
    ):
        self.pIndex = pIndex
        self.isRoad = isRoad
        self.isSettlement = isSettlement
        self.isCity = isCity
        self.isTrade = isTrade
        self.index = index
        self.tradeFrom = tradeFrom
        self.tradeTo = tradeTo
        self.wasFree = wasFree

    def __str__(self):
        return str(
            (
                self.pIndex,
                self.isRoad,
                self.isSettlement,
                self.isCity,
                self.isTrade,
                self.tradeFrom,
                self.tradeTo,
                self.index,
                self.wasFree
            )
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
            and self.pIndex == other.pIndex
            and self.isRoad == other.isRoad
            and self.isSettlement == other.isSettlement
            and self.isCity == other.isCity
            and self.isTrade == other.isTrade
            and self.tradeFrom == other.tradeFrom
            and self.tradeTo == other.tradeTo
            and self.index == other.index
            and self.wasFree == other.wasFree
        )

    def __hash__(self):
        return hash(
            (
                self.pIndex,
                self.isRoad,
                self.isSettlement,
                self.isCity,
                self.isTrade,
                self.tradeFrom,
                self.tradeTo,
                self.index,
                self.wasFree
            )
        )


# Always 3 person
class Game:
    # Attributes:
    # terrains = list of 19 terrain types
    # chances = list of 19 probabilities
    # verticesBuilt = list of 55 vertices
    # roadsBuilt = list of all roads connecting built built vertices
    def __init__(self):
        self.terrains = self.initTerrains()
        self.chances = self.initProbs()
        self.verticesBuilt = []
        for i in range(1, 55):
            self.verticesBuilt.append(0)
        self.roadsBuilt = []
        self.roundsInPick = 4
        for i in range(0, len(roadsList)):
            self.roadsBuilt.append(0)
        self.firstPlayerCards = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        self.secondPlayerCards = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        self.thirdPlayerCards = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        self.firstPlayerScore = 0
        self.secondPlayerScore = 0
        self.thirdPlayerScore = 0
        self.whoseTurn = 0
        self.numTurns = 0

    def distributeCards(self):
        roll = random.randint(1, 6)
        roll2 = random.randint(1, 6)
        two_dice = roll + roll2
        for tile in tilesToVertices:
            if self.chances[tile - 1] == two_dice:
                for vertex in tilesToVertices[tile]:
                    if self.verticesBuilt[vertex - 1] != 0:
                        player = (int)(self.verticesBuilt[vertex - 1] / 3) + 1
                        numCards = self.verticesBuilt[vertex - 1] % 3
                        terrainType = self.terrains[tile - 1]
                        if terrainType==0:
                            continue
                        if player == 1:
                            old = self.firstPlayerCards[terrainType]
                            new = old + numCards
                            # print(self.firstPlayerCards)
                            # print("Please dear god update1")
                            self.firstPlayerCards[terrainType] = new
                            # print (self.firstPlayerCards)
                        if player == 2:
                            old = self.secondPlayerCards[terrainType]
                            new = old + numCards
                            # print(self.secondPlayerCards)
                            # print("Please dear god update2")
                            self.secondPlayerCards[terrainType] = new
                            # print(self.secondPlayerCards)
                        if player == 3:
                            old = self.thirdPlayerCards[terrainType]
                            new = old + numCards
                            # print(self.thirdPlayerCards)
                            # print("Please dear god update3")
                            self.thirdPlayerCards[terrainType] = new
                            # print(self.thirdPlayerCards)
# First index in return value is reward of winning: 1
# Second index is the index of the player who won.  Useful for backprogagation in mcts.py
    def getReward(self):
        if self.firstPlayerScore >=10:
            return (1, 0)
        if self.secondPlayerScore >=10:
            return (1, 1)
        if self.thirdPlayerScore >=10:
            return (1, 2)
        # if self.whoseTurn == 0:
        #     if self.firstPlayerScore >= 10:
        #         return (1, 0)
        #     if self.secondPlayerScore >= 10 or self.thirdPlayerScore >= 10:
        #         return (1, 0)
        # if self.whoseTurn == 1:
        #     if self.secondPlayerScore >= 10:
        #         return (1, 0)
        #     if self.firstPlayerScore >= 10 or self.thirdPlayerScore >= 10:
        #         return (1, 0)
        # if self.whoseTurn == 2:
        #     if self.thirdPlayerScore >= 10:
        #         return (1, 0)
        #     if self.secondPlayerScore >= 10 or self.firstPlayerScore >= 10:
        #         return False
        # return False

    def isTerminal(self):
        return (
            self.firstPlayerScore >= 10
            or self.secondPlayerScore >= 10
            or self.thirdPlayerScore >= 10
        )

    # TODO: pIndex, isRoad, isSettlement, isCity, isTrade, tradeFrom, tradeTo, index, wasFree
    def getPossibleActions(self):
        possibleActions = []
        # First if statement: We're in the set up rounds.  
        if self.roundsInPick > 0:
            # First if statemetn: Everybody picks a road first
            if(self.roundsInPick % 2 == 0):
                for i in range(0, len(self.roadsBuilt)):
                    if self.playerCanBuildR(i, self.whoseTurn, True): #Last parameter for canBuildR is that we're in draft mode
                        ac = Action(self.whoseTurn, True, False, False, False, -1, -1, i, True)
                        possibleActions.append(ac)
            # Otherwise, everybody picks their settlement
            else:
                for i in range(0, 54):
                    if self.playerCanBuildS(i, self.whoseTurn, True): #Last parameter for canBuildS is that we're in draft mode 
                        ac = Action(self.whoseTurn, False, True, False, False, -1, -1, i, True)
                        possibleActions.append(ac)    
            # possibleActions.append(Action(self.whoseTurn, False, False, False, False, -1, -1, -1, False))    
        # Otherwise, we're in the normal game   
        # Options are: building Settlements, cities, roads, trading with the bank, or passing.  
        else:
            for i in range(0, 54):
                if self.playerCanBuildS(i, self.whoseTurn, False):
                    ac = Action(self.whoseTurn, False, True, False, False, -1, -1, i, False)
                    possibleActions.append(ac)
                if self.playerCanBuildC(i, self.whoseTurn):
                    ac = Action(self.whoseTurn, False, False, True, False, -1, -1, i, False)
                    possibleActions.append(ac)
            for i in range(0, len(self.roadsBuilt)):
                if self.playerCanBuildR(i, self.whoseTurn, False):
                    ac = Action(self.whoseTurn, True, False, False, False, -1, -1, i, False)
                    possibleActions.append(ac)
            if self.whoseTurn == 0:
                for cardType in self.firstPlayerCards:
                    if self.firstPlayerCards[cardType] >= 4:
                        for i in range(1, 6):
                            if i == cardType:
                                continue
                            ac = Action(self.whoseTurn, False, False, False, True, cardType, i, -1, False)
                            possibleActions.append(ac)
            if self.whoseTurn == 1:
                for cardType in self.secondPlayerCards:
                    if self.secondPlayerCards[cardType] >= 4:
                        for i in range(1, 6):
                            if i == cardType:
                                continue
                            ac = Action(self.whoseTurn, False, False, False, True, cardType, i, -1, False)
                            possibleActions.append(ac)
            if self.whoseTurn == 2:
                for cardType in self.thirdPlayerCards:
                    if self.thirdPlayerCards[cardType] >= 4:
                        for i in range(1, 6):
                            if i == cardType:
                                continue
                            ac = Action(self.whoseTurn, False, False, False, True, cardType, i, -1, False)
                            possibleActions.append(ac)
                
            possibleActions.append(Action(self.whoseTurn, False, False, False, False, -1, -1, -1, False))
        # print("Length of possible actions:")
        # print(len(possibleActions))
        # print("Rounds In Pick remaining:")
        # print (self.roundsInPick)
        # if len(possibleActions) == 1:
        #     print(self.roundsInPick)
        #     print(self.roadsBuilt)
        #     print(self.verticesBuilt)
        return possibleActions

    def takeAction(self, action):
        newCatan = deepcopy(self)

        # Get a copy of the new state.  To take an action in playGame, set old game to the return value of takeAction
        # Player built a road
        if action.isRoad:
            newCatan.roadsBuilt[action.index] = action.pIndex + 1
            if not action.wasFree: #Make sure this wasn't in the draft when roads are free
                if action.pIndex == 0:
                    newCatan.firstPlayerCards[5] -= 1
                    newCatan.firstPlayerCards[1] -= 1
                if action.pIndex == 1:
                    newCatan.secondPlayerCards[5] -= 1
                    newCatan.secondPlayerCards[1] -= 1
                if action.pIndex == 2:
                    newCatan.thirdPlayerCards[5] -= 1
                    newCatan.thirdPlayerCards[1] -= 1
        # Player built a settlement
        elif action.isSettlement:
            # print("Building settlement")
            newCatan.verticesBuilt[action.index] = (action.pIndex) * 3 + 1
            if not action.wasFree: #Make sure this wasn't in the draft when settlements are free
                if action.pIndex == 0:
                    newCatan.firstPlayerCards[5] -= 1
                    newCatan.firstPlayerCards[1] -= 1
                    newCatan.firstPlayerCards[2] -= 1
                    newCatan.firstPlayerCards[3] -= 1
                if action.pIndex == 1:
                    newCatan.secondPlayerCards[5] -= 1
                    newCatan.secondPlayerCards[1] -= 1
                    newCatan.secondPlayerCards[2] -= 1
                    newCatan.secondPlayerCards[3] -= 1
                if action.pIndex == 2:
                    newCatan.thirdPlayerCards[5] -= 1
                    newCatan.thirdPlayerCards[1] -= 1
                    newCatan.thirdPlayerCards[2] -= 1
                    newCatan.thirdPlayerCards[3] -= 1
        # Player built a city
        elif action.isCity:
            # print("Building city??")
            newCatan.verticesBuilt[action.index] = (action.pIndex) * 3 + 2
            if action.pIndex == 0:
                newCatan.firstPlayerCards[2] -= 2
                newCatan.firstPlayerCards[4] -= 3
            if action.pIndex == 1:
                newCatan.secondPlayerCards[2] -= 2
                newCatan.secondPlayerCards[4] -= 3
            if action.pIndex == 2:
                newCatan.thirdPlayerCards[2] -= 2
                newCatan.thirdPlayerCards[4] -= 3
        if action.isSettlement or action.isCity:
            if action.pIndex == 0:
                newCatan.firstPlayerScore += 1
            if action.pIndex == 1:
                newCatan.secondPlayerScore += 1
            if action.pIndex == 2:
                newCatan.thirdPlayerScore += 1
        if action.isTrade:
            if action.pIndex == 0:
                newCatan.firstPlayerCards[action.tradeFrom] -= 4
                newCatan.firstPlayerCards[action.tradeTo] += 1
            if action.pIndex == 1:
                newCatan.secondPlayerCards[action.tradeFrom] -= 4
                newCatan.secondPlayerCards[action.tradeTo] += 1
            if action.pIndex == 2:
                newCatan.thirdPlayerCards[action.tradeFrom] -= 4
                newCatan.thirdPlayerCards[action.tradeTo] += 1
        for cardType in newCatan.firstPlayerCards:
            if newCatan.firstPlayerCards[cardType] < 0:
                print("first")
                print(cardType)
        for cardType in newCatan.secondPlayerCards:
            if newCatan.secondPlayerCards[cardType] < 0:
                print("second")
                print(cardType)
        for cardType in newCatan.thirdPlayerCards:
            if newCatan.thirdPlayerCards[cardType] < 0:
                print("third")
                print(cardType)
        if (
            (not action.isRoad
            and not action.isSettlement
            and not action.isCity
            and not action.isTrade)
        ):
            newCatan.whoseTurn += 1 
        ###This is where we increment whose turn it is - turn only progresses to the next player if the player before passes.  
        ###elif is for the snake draft
        elif newCatan.roundsInPick> 0: #We're in the draft
            if newCatan.roundsInPick > 2: #We're in the first two rounds of draft - order is (0, 1, 2)
                newCatan.whoseTurn +=1 #Increment whose turn it is
                if newCatan.roundsInPick == 3 and newCatan.whoseTurn == 3: #If it was the last pick in the first round of snake
                    newCatan.whoseTurn =2  #Go to order (2, 1, 0)
                    newCatan.roundsInPick -=1 #Decrement the number of rounds left to pick settlements and roads
            else:
                newCatan.whoseTurn -=1  #Otherwise, we're in the second part of draft - order is (2, 1, 0)
                if newCatan.whoseTurn < 0: #If it's negative, go back to player 2's turn and decrement the number of rounds left
                    newCatan.whoseTurn = 2
                    newCatan.roundsInPick -=1
                    if newCatan.roundsInPick == 0: #It was the last round in the draft --> change whose turn it was to player 1
                        newCatan.whoseTurn = 0
        if newCatan.whoseTurn == 3:
            newCatan.whoseTurn = 0
            if newCatan.roundsInPick > 0:
                newCatan.roundsInPick -= 1
        if newCatan.roundsInPick <=0 and newCatan.whoseTurn != self.whoseTurn: #Everybody gets cards if play has progressed
            newCatan.distributeCards()
            newCatan.numTurns +=1
        return newCatan

    def initTerrains(self):
        terrains = []
        terrains.append(0)
        for i in range(0, 4):
            terrains.append(1)
            terrains.append(2)
            terrains.append(3)
        for i in range(0, 3):
            terrains.append(4)
            terrains.append(5)
        random.shuffle(terrains)
        return terrains

    def initProbs(self):
        chances = []
        chances.append(2)
        chances.append(12)
        for i in range(3, 12):
            chances.append(i)
            chances.append(i)
        random.shuffle(chances)
        return chances

    def playerCanBuildS(self, vIndex, pIndex, isFree):
        if not isFree:
            if pIndex == 0:
                if self.firstPlayerCards[1] < 1 or self.firstPlayerCards[2] < 1 or self.firstPlayerCards[3] < 1 or self.firstPlayerCards[5] < 1:
                    return False
            if pIndex == 1:
                if self.secondPlayerCards[1] < 1 or self.secondPlayerCards[2] < 1 or self.secondPlayerCards[3] < 1 or self.secondPlayerCards[5] < 1:
                    return False
            if pIndex == 2:
                if self.thirdPlayerCards[1] < 1 or self.thirdPlayerCards[2] < 1 or self.thirdPlayerCards[3] < 1 or self.thirdPlayerCards[5] < 1:
                    return False
        vIndexAdjacent = adjacentVertices[vIndex]
        # for i in vIndexAdjacent:
        #     if self.verticesBuilt[i-1] != 0:
        #         return False
        for i in range(0, len(roadsList)):
            roadTuple = roadsList[i]
            if roadTuple[0] == vIndex or roadTuple[1] == vIndex:
                if self.roadsBuilt[i] != 0 and (self.roadsBuilt[i]-1) == pIndex:
                    return True
        return False

    def playerCanBuildC(self, vIndex, pIndex):
        # Enough cards
        if pIndex == 0:
            if self.firstPlayerCards[4] < 3 or self.firstPlayerCards[2] < 2:
                return False
        if pIndex == 1:
            if self.secondPlayerCards[4] < 3 or self.secondPlayerCards[2] < 2:
                return False
        if pIndex == 2:
            if self.thirdPlayerCards[4] < 3 or self.thirdPlayerCards[2] < 2:
                return False   
        if (int)(self.verticesBuilt[vIndex] / 3) == pIndex:
            if self.verticesBuilt[vIndex] % 3 == 1:
                return True #Has this person's settlement on it
        return False

    def playerCanBuildR(self, rIndex, pIndex, isFree):
        if isFree:
            return self.roadsBuilt[rIndex] == 0
        if self.roadsBuilt[rIndex] > 0:
            return False
        if pIndex == 0:
            if self.firstPlayerCards[5] < 1 or self.firstPlayerCards[1] < 1:
                return False
        if pIndex == 1:
            if self.secondPlayerCards[1] < 1 or self.secondPlayerCards[5] < 1:
                return False
        if pIndex == 2:
            if self.thirdPlayerCards[1] < 1 or self.thirdPlayerCards[5] < 1:
                return False        
        toBuild = roadsList[rIndex]
        vA = toBuild[0]
        vB = toBuild[1]
        for i in range(0, len(roadsList)):
            roadTuple = roadsList[i]
            if roadTuple == toBuild:
                continue
            if (
                roadTuple[0] == vA
                or roadTuple[1] == vA
                or roadTuple[0] == vB
                or roadTuple[1] == vB
            ):
                if self.roadsBuilt[i] == pIndex + 1:
                    return True
        return False


def main():
    g = Game()
    playerOrder = [0, 1, 2]
    # random.shuffle(playerOrder)
    player2 = MonteCarloPlayer(2)
    player0 = MonteCarloPlayer(0)
    player1 = MonteCarloPlayer(1)
    players = [player0, player1, player2]
    # players = random.shuffle(players)
    wins = [0, 0, 0]
    numTurnsAVG = 0.0
    for i in range (0, 25):
        g = Game()
        while(True):
            if(g.isTerminal()):
                print(g.getReward())
                wins[g.getReward()[1]] += 1
                numTurnsAVG += g.numTurns / (25.0)
                break
            ac = players[g.whoseTurn].chooseAction(g)
            g = g.takeAction(ac)


    print(wins)
    print (numTurnsAVG)

if __name__ == "__main__":
    main()
