import random
import BoardState


class Tile():
    def __init__(self, resource, chance):
        self.type = resource
        self.probability = chance
        self.robber = False

    def getType(self):
        return self.type

    def getProb(self):
        return self.probability

    def rob(self):
        self.robber = True

    def unRob(self):
        self.robber = False


class Road():
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.player = None

    def getVertices():
        return (v1, v2)

    def getOtherVertex(v):
        if v1 == v:
            return v2
        return v1

    def build(p):
        if player is not None:
            return False
        self.player = p
        return True

    def isBuilt():
        return self.player


class Player():
    def __init__(self, name):
        self.name = name
        self.resource_cards = []
        self.roads = []
        self.vertices = []

    def drawResourceCard(card):
        self.resource_cards.append(card)


class CatanGame():
    def __init__(self):
        terrains = self.initTerrains()
        chances = self.initProbs()
        self.tilesToVertices = BoardState.tilesToVertices
        self.roadsList = BoardState.roadsList
        terrain_objects = []
        for i in range(0, len(terrains)):
            if (terrains[i] == "Desert"):
                t = Tile(terrains[i], -1)
                t.rob()
                terrain_objects.append(t)
            else:
                terrain_objects.append(Tile(terrains[i], chances[i]))
        vertices = []
        print self.getAssociatedTiles(18)
        for i in self.tilesToVertices:
            vertices.append(CatanVertex.CatanVertex())
        self.currentPlayer = 1

    def getAssociatedTiles(self, vNum):
        ans = []
        for i in self.tilesToVertices:
            if vNum in self.tilesToVertices[i]:
                ans.append(i)
        return ans

    def initTerrains(self):
        terrains = []
        terrains.append("Desert")
        for i in range(0, 4):
            terrains.append("Forest")
            terrains.append("Fields")
            terrains.append("Pasture")
        for i in range(0, 3):
            terrains.append("Mountains")
            terrains.append("Hills")
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

    def getPossibleActions(self):
        possibleActions = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    possibleActions.append(
                        Action(player=self.currentPlayer, x=i, y=j))
        return possibleActions

    def takeAction(self, action):
        newState = deepcopy(self)
        newState.board[action.x][action.y] = action.player
        newState.currentPlayer = self.currentPlayer * -1
        return newState

    def isTerminal(self):
        for row in self.board:
            if abs(sum(row)) == 3:
                return True
        for column in list(map(list, zip(*self.board))):
            if abs(sum(column)) == 3:
                return True
        for diagonal in [[self.board[i][i] for i in range(len(self.board))], [
                self.board[i][len(self.board) - i - 1]
                for i in range(len(self.board))
        ]]:
            if abs(sum(diagonal)) == 3:
                return True
        return reduce(operator.mul, sum(self.board, []), 1)

    def getReward(self):
        for row in self.board:
            if abs(sum(row)) == 3:
                return sum(row) / 3
        for column in list(map(list, zip(*self.board))):
            if abs(sum(column)) == 3:
                return sum(column) / 3
        for diagonal in [[self.board[i][i] for i in range(len(self.board))], [
                self.board[i][len(self.board) - i - 1]
                for i in range(len(self.board))
        ]]:
            if abs(sum(diagonal)) == 3:
                return sum(diagonal) / 3
