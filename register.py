class register:
    def __init__(self, typeR, tag):
        # The register has a type field to indicate if it's logical or physical.
        # It also has a unique (type, digit ID) couple to identify.
        self.t = typeR
        self.tag = tag
        
    def getType(self):
        return self.t
    def getTag(self):
        return self.tag
    def getID(self):
        return [self.t, self.tag]