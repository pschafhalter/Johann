class ChordProgressionError(Exception):
    def __init__(self, index):
        self.index = index
        self.message = "Found invalid chord progression at index " + str(index)
        Exception.__init__(self, self.message)
