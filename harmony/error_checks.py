from music21 import chord
from .errors import *
from . import helpers


def check_chorale(chorale, print_result=True):
    num_errors = 0
    chorale_key = chorale.analyze("key")
    chorale_chords = helpers.get_chords(chorale)

    # Check chord progressions
    # TODO: support passing chords, secondary dominants, sequences
    chord_walker = helpers.ChordWalker(chorale_chords, chorale_key)

    for i in range(len(chorale_chords) - 1):
        try:
            next(chord_walker)
        except ChordProgressionError as e:
            num_errors += 1
            print("Chord progression error found at index", e.index)
            chord_walker.index += 1
        except AssertionError as e:
            num_errors += 1
            print(e.args[0])
            chord_walker.index += 1

    if print_result:
            print("Harmony check completed\n Result: %d errors" % num_errors)

