import random


class BoardSquare():
    def __init__(self, resource, chance):
        self.type = resource
        self.probability = chance
        self.roads = [False, False, False, False, False, False]

    def getType():
        return self.type

    def getProb():
        return self.probability

    def buildRoad(index):
        self.roads[index] = True

    def roadIsBuilt(index):
        return self.roads[index]


class CatanGame():
    def __init__(self):
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
        terrain_objects = []
        chances = []
        chances.append(2)
        chances.append(12)
        for i in range(3, 12):
            chances.append(i)
            chances.append(i)
        random.shuffle(chances)

        for i in range(0, len(terrains)):
            if (terrains[i] == "Desert"):
                terrain_objects.append(BoardSquare(terrains[i], -1))
            else:
                terrain_objects.append(BoardSquare(terrains[i], chances[i]))
        self.board = [[0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0],
                      [0, 0, 0]]

        self.currentPlayer = 1

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
