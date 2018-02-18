"""
Controls intake wheels, the elevator, and the metabox.
"""

class MetaBox(object):
    def __init__(self, encoder, elevatorM):
        self.encoder = encoder
        self.elevatorM = elevatorM

    def run(self, value):
        self.elevatorM.set(value)
        #print(self.getEncoder())

    def getEncoder(self):
        return self.encoder.getDistance()