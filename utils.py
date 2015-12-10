from music21 import note, stream, chord, roman
from voice_leading import error_checks


def make_chorale(length):
    print("Enter soprano notes:")
    soprano = make_part(length)
    soprano.id = "soprano"
    print("Enter alto notes:")
    alto = make_part(length)
    alto.id = "alto"
    print("Enter tenor notes:")
    tenor = make_part(length)
    tenor.id = "tenor"
    print("Enter bass notes:")
    bass = make_part(length)
    bass.id = "bass"

    return stream.Score([soprano, alto, tenor, bass])


def make_part(length):
    part = stream.Part()
    for i in range(length):
        n = note.Note(input())
        n.offset = i
        part.append(n)
    return part


def check_chorale_errors(chorale):
    error_checks.check_chorale(chorale)


def print_chords(chorale):
    chorale_key = chorale.analyze("key")
    chord_list = filter(lambda x: type(x) is chord.Chord, chorale.chordify().recurse())
    for c in chord_list:
        rn = roman.romanNumeralFromChord(c, chorale_key)
        print(rn.figure)
