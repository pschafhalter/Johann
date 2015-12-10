class AugmentedSecondError(Exception):
    def __init__(self, index):
        self.message = "Found augmented second at index " + str(index)
        self.index = index
        Exception.__init__(self, self.message)


class UnresolvedLeapError(Exception):
    def __init__(self, index):
        self.message = "Found unresolved leap at index " + str(index)
        self.index = index
        Exception.__init__(self, self.message)

class SpacingError(Exception):
    def __init__(self, index):
        self.message = "Found spacing error at index " + str(index)
        self.index = index
        Exception.__init__(self, self.message)


class VoiceCrossingError(Exception):
    def __init__(self, index):
        self.message = "Found voice crossing at index " + str(index)
        self.index = index
        Exception.__init__(self, self.message)


class VoiceOverlappingError(Exception):
    def __init__(self, index):
        self.message = "Found voice overlapping at index " + str(index)
        self.index = index
        Exception.__init__(self, self.message)


class ParallelFourthsError(Exception):
    def __init__(self, index):
        self.message = "Found parallel fourths at index " + str(index)
        self.index = index
        Exception.__init__(self, self.message)


class ParallelFifthsError(Exception):
    def __init__(self, index):
        self.message = "Found parallel fifths at index " + str(index)
        self.index = index
        Exception.__init__(self, self.message)


class ParallelOctavesError(Exception):
    def __init__(self, index):
        self.message = "Found parallel octaves at index " + str(index)
        self.index = index
        Exception.__init__(self, self.message)


class DirectFifthsError(Exception):
    def __init__(self, index):
        self.message = "Found direct fifth at index " + str(index)
        self.index = index
        Exception.__init__(self, self.message)


class DirectOctavesError(Exception):
    def __init__(self, index):
        self.message = "Found direct octave at index " + str(index)
        self.index = index
        Exception.__init__(self, self.message)
