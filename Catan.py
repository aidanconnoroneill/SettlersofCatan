import random
import BoardState
import CatanVertex
import sys

#added self to a few method parameters
class Action():
    def __init__(self, isRoad, pos, player):
        self.isRoad = isRoad
        self.pos = pos
        self.player = player

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

    def getVertices(self):
        return (self.v1, self.v2)

    def getOtherVertex(self, v):
        if self.v1 == v:
            return self.v2
        return self.v1

    def build(self, p):
        if self.player is not None:
            return False
        self.player = p
        return True

    def isBuilt(self):
        return self.player


class Player():
    def __init__(self, name):
        self.name = name
        self.resource_cards = []
        self.roads = []
        self.vertices = []
        self.victoryPoints = 0

        self.brick = 0
        self.grain = 0
        self.ore = 0
        self.lumber = 0
        self.wool = 0

    # ACTIONS 
    def drawResourceCard(self, card):

        if card == 'Forest':
            self.lumber += 1
        if card == 'Fields':
            self.grain += 1
        if card == 'Pasture':
            self.wool += 1
        if card == 'Mountains':
            self.ore += 1
        if card == 'Hills':
            self.brick += 1

    def settlementSites(self, vertices, player):
        canBuild = []
        for vertex in vertices:
            if (vertex.canBuild(player)):
                canBuild.append(vertex)
        return canBuild

    def roadSites(self, vertices, player):
        canBuild = []

        for vertex in vertices:
            for road in vertex.roads:
                for road2 in vertex.roads:
                    if (road.player == player):
                        if (road2.player == None):
                            canBuild.append(Action(True, road2, player))
        return canBuild

    def buildRoad(self, road):
        road.build(self)

    def settlementsToUpgrade(self, vertices, player):
        canUpgrade = []
        for vertex in vertices:
            if(player.canUpgradeSettlement(vertex)):
                canUpgrade.append(Action(False, vertex, player))

        return canUpgrade

    def canUpgradeSettlement(self, vertex):
        if(vertex.settlementType == 1):
            if(self.ore >= 3 and self.grain >= 2):
                return True

        return False

    def upgradeSettleToCity(self, vertex):
        vertex.settlementType = 2

    def settlementSites(self, vertices, player):
        canBuild = []
        for vertex in vertices:
            if (vertex.canBuild(player)):
                canBuild.append(Action(False, vertex, player))
        return canBuild

    def buildSettlement(self, vertex):
        vertex.build(self)

    def getScore(self, vertex):
        score = 0.0
        for tile in vertex.tiles:
            tile_score = 0.0
            if tile.type == 'Forest':
                tile_score += 3
            if tile.type == 'Fields':
                tile_score += 2
            if tile.type == 'Pasture':
                tile_score += 1
            if tile.type == 'Mountains':
                tile_score += 2
            if tile.type == 'Hills':
                tile_score += 3
            tile_score *= (6.0 - abs(6.0 - tile.probability)) / 36.0
            score += tile_score
        return score

    def pickFirst(self, vertices):
        best = None
        best_score = 0
        for i in range(0, len(vertices)):
            if best is None and vertices[i].player is None:
                best = vertices[i]
                best_score = self.getScore(vertices[i])
            elif vertices[i].player is None:
                score = self.getScore(vertices[i])
                if score > best_score:
                    best_score = score
                    best = vertices[i]

class CatanGame():
    def __init__(self, numPlayers, players):
        if numPlayers < 3 or numPlayers > 5:
            print("The number of players must be 3 or 4")
            sys.exit()
        terrains = self.initTerrains()
        chances = self.initProbs()

        self.tilesToVertices = BoardState.tilesToVertices
        self.roadsList = BoardState.roadsList
        self.players = []
        self.currentPlayer = 0

        terrain_objects = []
        for i in range(0, len(terrains)):
            if (terrains[i] == "Desert"):
                t = Tile(terrains[i], -1)
                t.rob()
                terrain_objects.append(t)
            else:
                terrain_objects.append(Tile(terrains[i], chances[i]))
        vertices = []
        self.terrains = terrain_objects
        for vID in range(1, 55):
            tileIDs = self.getAssociatedTiles(i)
            tiles = []
            for j in tileIDs:
                tiles.append(terrain_objects[i - 1])
            vertices.append(CatanVertex.CatanVertex(tiles, vID))
        self.vertices = vertices
        for i in self.roadsList:
            v1 = self.vertices[i[0] - 1]
            v2 = self.vertices[i[1] - 1]
            road = Road(v1, v2)
            v1.addRoad(road)
            v2.addRoad(road)

    def playGame(self):
        winner = None
        count = 0
        while (True):
            count += 1
            if count > 100:
                break
            for player in self.players:
                roll = random.randint(1, 6)
                roll2 = random.randint(1, 6)
                sum = roll + roll2
                for vertex in self.built_vertices:
                    for tile in vertex.tiles:
                        if tile.probability == sum:
                            for i in range(0, vertex.settlementType):
                                vertex.player.drawResourceCard(tile.type)
                while (True):
                    move = player.makeMoves()
                    if move is None:
                        break
                if player.victoryPoints >= 10:
                    winner = player
                    break
        return winner

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

    def insertPlayers(self, names):
        self.players = names

    def gameIsNotOver(self):
        for player in self.players:
            if player.victoryPoints == 10:
                return True

        return False

    def getPossibleActions(self, player, vertices):
        possibleActions = []
        buildRoadActions = []
        buildSettlementActions = []

        buildRoadActions = player.roadSites(vertices, player)
        buildSettlementActions = player.settlementSites(vertices, player)
        upgradeSettlementActions = player.settlementsToUpgrade(vertices, player)

        possibleActions = buildRoadActions + buildSettlementActions + upgradeSettlementActions

        return possibleActions
    
    def takeAction(self, action):
        newState = self.deepcopy(self)
        # Road Location
        if action.is_road:
            newState.roadsList[action.pos].player = action.player
            newState.action.player.brick -=1
            newState.action.player.lumber -=1
        # Settlement Location
        else:
            # It is a settlement, needs to be upgraded
            if(Action.pos.player != None):
                newState.vertices[action.pos].upgradeSettleToCity(action.pos)
                newState.action.player.ore -= 3
                newState.action.player.grain -= 2
            # It is a vacant place to build a settlement
            else:
                newState.vertices[action.pos].player = action.player
                newState.action.player.brick -= 1
                newState.action.player.lumber -= 1
                newState.action.player.wool -= 1
                newState.action.player.grain -= 1

        newState.currentPlayer += 1
        newState.currentPlayer = newState.players[newState.currentPlayer % len(newState.players)]

        return newState

    def makeMoves():
        # get possible actions
        #WORK ON THIS, GET RUNNING
        
        return

    def isTerminal(self):
        for player in self.players:
            if player.victoryPoints >= 10:
                return True
        return False

    def getReward(self):
        for player in self.players:
            if player.isCurrent:
                return player.victoryPoints
        return -1