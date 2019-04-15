# This Class is a representation of a vertex in Settlers of Catan


class CatanVertex():
    def __init__(self, tiles, id, settlementType):

        self.id = id
        self.tiles = tiles
        self.roads = None
        self.settlementType = 0

    def connectRoads(self, r):
        self.roads = r

    def getPlayer(self):
        return self.player

    def getTiles(self):
        return self.tiles

    def getRoads(self):
        return self.roads

    def getSettlementType(self):
        return self.settlementType

    def canBuild(self, player):

        if len(self.roads) > 2:
            for road in self.roads:
                for vertex in road.getVertices():
                    if vertex is not None:
                        return False
            return True
        return False

    def build(self, player):
        self.player = player
