

# This Class is a representation of a vertex in Settlers of Catan



class CatanVertex():
    
    def __init__(self, player, tiles, id, roads, settlementType):

        self.id = id
        self.self = player
        self.tiles = tiles
        self.roads = roads
        self.settlementType = 0


    def getPlayer(self):
        return self.player

    def getTiles(self):
        return self.tiles

    def getRoads(self):
        return self.roads

    def getSettlementType(self):
        return self.settlementType

    def canBeASettlement(self, player):
        return True

