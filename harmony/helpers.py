from music21 import roman, key, chord
# TODO: better handling of getting nexts of a 7 chord


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


def get_expected_next(chord_label, major_key = True):
    """Returns a list of gramatically correct next chords
    given a chord label
    """
    if is_tonic(chord_label, major_key):
        return get_dominant_nexts(chord_label, major_key)

    if is_dominant(chord_label, major_key):
        return get_dominant_nexts(chord_label, major_key)

    if is_predominant(chord_label, major_key):
        return get_predominant_nexts(chord_label, major_key)

    return []


def get_inversions(parent_chord, inversions):
    """Returns labeled chord inversions provided
    """
    if "7" in parent_chord:
        c = parent_chord[:len(parent_chord) - 1]
        inverted_chords = [parent_chord, c + "65", c + "43", c + "42"]
    else:
        inverted_chords = [parent_chord, parent_chord + "6", parent_chord + "64"]

    return [inverted_chords[i] for i in inversions]


def is_seven_chord(chord_label):
    for inversion in ["7", "65", "43", "42"]:
        if inversion in chord_label:
            return True
    return False


def get_tonics(major_key = True):
    if major_key:
        return get_inversions("I", [0, 1]) + ["iii"]
    return get_inversions("i", [0, 1])


def get_tonic_nexts(chord_label, major_key = True):
    """Returns a list of chords the provided tonic can go to
    """
    assert chord_label in get_tonics(major_key), "Provided chord must be tonic"
    result = get_tonics(major_key)
    result += get_predominants(major_key)
    result += get_dominants(major_key)
    return result


def is_tonic(chord_label, major_key = True):
    return chord_label in get_tonics(major_key)


def get_dominants(major_key):
    result = get_inversions("V", [0, 1])
    result += get_inversions("V7", range(0, 4))
    result += get_inversions("viio7", range(0, 4))
    if major_key:
        result += ["I64", "iii6"]
    else:
        result += ["i64", "iii6"]
    return result


def get_dominant_nexts(chord_label, major_key = True):
    assert chord_label in get_dominants(major_key), "Provided chord must be dominant"
    result = []
    # TODO: Check if i64 -> iii6 is legal
    if chord_label.lower() == "i64" or chord_label == "iii6":
        return chord_label + ["V"]
    # Reality is a bit more subtle, but we'll use this catch-all for now
    # TODO: better handling of viio6 and viio7
    result += get_tonics(major_key)
    result += get_inversions("V7", range(0, 4))
    if "viio" in chord_label or is_seven_chord(chord_label):
        return result
    # Must be V or V6
    result += get_inversions("V", [0, 1])
    return result


def is_dominant(chord_label, major_key = True):
    return chord_label in get_dominants(major_key)


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


def get_predominant_nexts(chord_label, major_key = True):
    assert chord_label in get_predominants(major_key), "Provided chord must be predominant"
    # TODO: finetune to avoid A2 in minor keys
    result = get_predominants(major_key) + get_dominants(major_key)
    if major_key:
        two_label, four_label, six_label = "ii", "IV", "vi"
    else:
        tw_label, four_label, six_label = "iio", "iv", "VI"

    if chord_label == six_label: 
        return result
    # remove vi
    result.remove(six_label)

    if four_label in chord_label and not is_seven_chord(chord_label):
        return result
    # remove inversions of IV
    result.remove(four_label)
    result.remove(four_label + "6")

    if four_label in chord_label:
        return result
    # remove inversions of IV7
    result = [c for c in result if not c in get_inversions(four_label + "7", [0, 1])]

    # TODO: investigate iio6 as a predominant
    # no iio tolerated!
    # hard coded, could be improved
    if "ii" == chord_label or "ii6" == chord_label:
        return result

    # remove inversons of ii6
    if "ii" in result:
        result.remove("ii")
        result.remove("ii6")

    return result


def is_predominant(chord_label, major_key = True):
    return chord_label in get_predominants(major_key)

