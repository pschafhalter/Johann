from music21 import roman, key, chord


class ChordWalker:
    def __init__(self, chords, chorale_key):
        """Chords is a list of music21 chord objects.
        chorale_key is a music21 key object
        """
        assert len(chords) > 0, "No given chords to walk"
        self.chords = chords
        self.key = chorale_key
        self.labeled_chords = []
        self.index = 0

    def find_next(self, expected_chords):
        """Returns the index and chord of the next chord in
        the list of expected chords
        """
        assert len(expected_chords) > 0, "No expected chords given"
        
    def get_expected_next(self, chord_label):
        """Returns a list of gramatically correct next chords
        given a chord label
        """
        pass


def get_inversions(parent_chord, inversions):
    """Returns labeled chord inversions provided
    """
    if "7" in parent_chord:
        c = parent_chord[:len(parent_chord) - 1]
        inverted_chords = [parent_chord, c + "65", c + "43", c + "42"]
    else:
        inverted_chords = [parent_chord, parent_chord + "6", parent_chord + "64"]
    
    return [inverted_chords[i] for i in inversions]
    

def get_tonics(major_key = True):
    if major_key:
        return get_inversions("I", [0, 1]) + ["iii"]
    return get_inversions("i", [0, 1])


def is_tonic(chord_label, major_key = True):
    return chord_label in get_tonics(major_key)


def get_dominants():
    result = get_inversions("V", [0, 1])
    result += get_inversions("V7", range(0, 4))
    result += get_inversions("viio7", range(0, 4))
    result += ["I64", "iii6"]
    return result


def is_dominant(chord_label):
    return chord_label in get_dominants()


def get_predominants(major_key = True):
    if major_key:
        result = get_inversions("ii", [0, 1])
        result += get_inversions("IV", [0, 1])
        result += get_inversions("ii7", range(0, 4))
        result += get_inversions("IV7", range(0, 4))
        result += ["vi"]
        return result

    result = get_inversions("iv", [0, 1])
    result += get_inversions("iio7", range(0, 4))
    result += get_inversions("iv7", range(0, 4))
    result += ["VI"]
    return result


def is_predominant(chord_label, major_key = True):
    return chord_label in get_predominants(major_key)

