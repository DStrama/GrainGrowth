
class Cell:
    id = 0
    color = None
    state = None

    def __init__(self):
        self.state = False
        self.color = 255

    def setIndex(self, index):
        self.id = index

    def getColor(self):
        return self.color

    def getId(self):
        return self.Id