from music21 import note, stream, chord, roman, pitch
from voice_leading import error_checks


def live_check_chorale(chorale=None):
    """Checks chorale from user input chord by chord.
    """
    print("Input notes as instructed or enter 0 to exit")
    if chorale:
        parts = [chorale.getElementById(p) for p in ["soprano", "alto", "tenor", "bass"]]
    else:
        parts = []
        for p in ["soprano", "alto", "tenor", "bass"]:
            part = stream.Part()
            part.id = p
            parts.append(part)
        chorale = stream.Score(parts)
    i = 0
    while True:
        print("Enter chord #" + str(i))
        try:
            notes = [get_note(msg) for msg in ["Soprano:", "Alto:", "Tenor:", "Bass:"]]
        except pitch.PitchException as e:
            print("Returning chorale...")
            return chorale
        for part, note in zip(parts, notes):
            note.offset = i
            part.append(note)
        error_checks.check_chorale(chorale, False)
        i += 1


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

def get_note(message=None):
    if message:
        print(message)
    return note.Note(input())

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
