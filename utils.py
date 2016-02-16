from music21 import note, stream, chord, roman, pitch
import voice_leading.error_checks
import harmony.error_checks


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

        check_chorale_errors(chorale)
        i += 1



def write_chorale(length):
    print("Enter soprano notes:")
    soprano = write_part(length)
    soprano.id = "soprano"
    print("Enter alto notes:")
    alto = write_part(length)
    alto.id = "alto"
    print("Enter tenor notes:")
    tenor = write_part(length)
    tenor.id = "tenor"
    print("Enter bass notes:")
    bass = write_part(length)
    bass.id = "bass"

    return stream.Score([soprano, alto, tenor, bass])


def get_note(message=None):
    if message:
        print(message)
    return note.Note(input())


def write_part(length):
    part = stream.Part()
    for i in range(length):
        n = note.Note(input())
        n.offset = i
        part.append(n)
    return part


def check_chorale_errors(chorale):
    voice_leading.error_checks.check_chorale(chorale, False)
    harmony.error_checks.check_chorale(chorale, False)


def get_chords(chorale):
    chorale_key = chorale.analyze("key")
    chord_list = filter(lambda x: type(x) is chord.Chord, chorale.chordify().recurse())
    return list(chord_list)


def print_chords(chorale):
    chorale_key = chorale.analyze("key")
    chord_list = get_chords(chorale)
    for c in chord_list:
        rn = roman.romanNumeralFromChord(c, chorale_key)
        print(rn.figure)
        

def make_chorale(soprano, alto, tenor, bass):
    """Given 4 voices, constructs a chorale
    """
    soprano.id = "soprano"
    alto.id = "alto"
    tenor.id = "tenor"
    bass.id = "bass"

    return stream.Score([soprano, alto, tenor, bass])


def make_chorale_from_strings(soprano, alto, tenor, bass):
    """Constructs a chorale given string lists of notes
    """
    soprano = make_part(map(note.Note, soprano))
    alto = make_part(map(note.Note, alto))
    tenor = make_part(map(note.Note, tenor))
    bass = make_part(map(note.Note, bass))

    return make_chorale(soprano, alto, tenor, bass)


def make_part(lst):
    """Given a list of notes, constructs a voice from them
    """
    part = stream.Part()
    for i, n in enumerate(lst):
        n.offset = i
        part.append(n)
    return part


def read_chorale(filename):
    """Reads a chorale from a given file
    """
    f = open(filename)

    s = f.readline().split()
    a = f.readline().split()
    t = f.readline().split()
    b = f.readline().split()
    
    return make_chorale_from_strings(s, a, t, b)

