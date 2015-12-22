from music21 import interval, chord
from .errors import *
from . import helpers


def check_chorale(chorale, print_result=True):
    num_errors = 0
    soprano = chorale.getElementById("soprano")
    alto = chorale.getElementById("alto")
    tenor = chorale.getElementById("tenor")
    bass = chorale.getElementById("bass")
    voices = [bass, tenor, alto, soprano]

    for voice in voices:
        try:
            check_augmented_seconds(voice)
            if voice.id != "bass":
                check_unresolved_leaps(voice)
        except (AugmentedSecondError, UnresolvedLeapError) as e:
            num_errors += 1
            print(voice.id + ":", e.message)

    try:
        check_unresolved_sevenths(voices)
    except UnresolvedSeventhError as e:
        num_errors += 1
        print(e.voice_id + ":", e.message)

    for pair in zip(voices[:-1], voices[1:]):
        try:
            if pair[0].id != 'bass':
                check_spacing(*pair)
            check_voice_crossing(*pair)
            check_voice_overlapping(*pair)
        except (SpacingError, VoiceCrossingError, VoiceOverlappingError) as e:
            num_errors += 1
            print("%s & %s:" % (pair[0].id, pair[1].id), e.message)

    from itertools import combinations

    for pair in combinations(voices, 2):
        try:
            check_parallel_fifths(*pair)
            check_parallel_octaves(*pair)
        except (ParallelFifthsError, ParallelOctavesError) as e:
            num_errors += 1
            print("%s & %s:" % (pair[0].id, pair[1].id), e.message)

    try:
        check_parallel_fourths(bass, soprano)
    except ParallelFourthsError:
        num_errors += 1
        print("%s & %s:" % (bass.id, soprano.id), e.message)

    if print_result:
        if num_errors == 0:
            print("Check completed\n Result: no errors!")
        else:
            print("Check completed\nResult: %d errors" % num_errors)


def check_augmented_seconds(voice):
    """Raises an error if the interval between two notes in a voice
    is an augmented second.

    >>> from music21 import note, stream
    >>> soprano = stream.Part(map(note.Note, ['D5', 'E-5', 'F#5']))
    >>> bass = stream.Part(map(note.Note, ['B-2', 'G2', 'A2']))
    >>> check_augmented_seconds(soprano)
    Traceback (most recent call last):
    ...
    errors.AugmentedSecondError: Found augmented second at index 2
    >>> check_augmented_seconds(bass)
    """
    previous_note = None
    for i, current_note in enumerate(voice):
        if i > 0:
            test_interval = interval.notesToInterval(previous_note, current_note)
            if test_interval.name == "A2":
                raise AugmentedSecondError(i)
        previous_note = current_note


def check_unresolved_leaps(voice):
    """Raises an error if a voice does not resolve its leap.

    >>> from music21 import note, stream
    >>> soprano = stream.Part(map(note.Note, ['C5', 'F5', 'E5']))
    >>> alto = stream.Part(map(note.Note, ['G4', 'D4', 'C4']))
    >>> check_unresolved_leaps(soprano)
    >>> check_unresolved_leaps(alto)
    Traceback (most recent call last):
    ...
    errors.UnresolvedLeapError: Found unresolved leap at index 2
    """
    previous_note, must_resolve = None, 0
    for i, current_note in enumerate(voice):
        if previous_note == current_note:
            pass
        elif must_resolve:
            test_interval = interval.notesToGeneric(previous_note, current_note)
            if test_interval.directed != must_resolve:
                raise UnresolvedLeapError(i)
            must_resolve = 0
        elif i > 0:
            test_interval = interval.notesToGeneric(previous_note, current_note)
            if test_interval.undirected >= 4:
                must_resolve = -2*test_interval.directed//test_interval.undirected
        previous_note = current_note


def check_unresolved_sevenths(voices):
    if len(voices) < 2:
        return

    chords = [chord.Chord([voice[k] for voice in voices]) for k in range(len(voices[0]))]
    for i, current_chord in enumerate(chords):
        if current_chord.seventh:
            for voice in voices:
                if current_chord.seventh == voice[i]:
                    if not helpers.resolves(voice, -2):
                        raise UnresolvedSeventhError(i, voice.id)


def check_spacing(lower_voice, upper_voice):
    """Raises an error if the interval between two voices exceeds an octave.

    >>> from music21 import note, stream
    >>> soprano = stream.Part(map(note.Note, ['C5', 'D5', 'E5']))
    >>> alto = stream.Part(map(note.Note, ['A4', 'B4', 'A4']))
    >>> tenor = stream.Part(map(note.Note, ['A3', 'G3', 'A3']))
    >>> check_spacing(alto, soprano)
    >>> check_spacing(tenor, alto)
    Traceback (most recent call last):
    ...
    errors.SpacingError: Found spacing error at index 1
    """
    for i, (lower_note, upper_note) in enumerate(zip(lower_voice, upper_voice)):
            if interval.notesToGeneric(lower_note, upper_note).undirected > 8:
                raise SpacingError(i)

def check_voice_crossing(lower_voice, upper_voice):
    """Raises an error if two voices intersect.

    >>> from music21 import note, stream
    >>> soprano = stream.Part(map(note.Note, ['C5', 'B4', 'A4']))
    >>> alto = stream.Part(map(note.Note, ['A4', 'B4', 'C5']))
    >>> tenor = stream.Part(map(note.Note, ['A3', 'G3', 'A3']))
    >>> check_voice_crossing(alto, soprano)
    Traceback (most recent call last):
    ...
    errors.VoiceCrossingError: Found voice crossing at index 2
    >>> check_voice_crossing(tenor, soprano)
    """
    for i, (lower_note, upper_note) in enumerate(zip(lower_voice, upper_voice)):
        if not helpers.is_lower_note(lower_note, upper_note):
            raise VoiceCrossingError(i)


def check_voice_overlapping(lower_voice, upper_voice):
    """Raises an error if two voices overlap.

    >>> from music21 import note, stream
    >>> soprano = stream.Part(map(note.Note, ['C5', 'E5', 'G5']))
    >>> alto = stream.Part(map(note.Note, ['A4', 'D5', 'C5']))
    >>> tenor = stream.Part(map(note.Note, ['A3', 'G3', 'A3']))
    >>> check_voice_overlapping(alto, soprano)
    Traceback (most recent call last):
    ...
    errors.VoiceOverlappingError: Found voice overlapping at index 1
    >>> check_voice_overlapping(tenor, alto)
    """
    if len(lower_voice) < 2:
        return False

    previous_lower_note, previous_upper_note = lower_voice.notes[0], upper_voice.notes[0]
    for i, (lower_note, upper_note) in enumerate(zip(lower_voice.notes[1:], upper_voice.notes[1:])):
        if not helpers.is_lower_note(previous_lower_note, previous_upper_note):
            raise VoiceOverlappingError(i + 1)
        if not helpers.is_lower_note(lower_note, previous_upper_note):
            raise VoiceOverlappingError(i + 1)
        previous_lower_note, previous_upper_note = lower_note, upper_note


def check_parallel_fourths(bass, upper_voice):
    """Raises an error if the voices contain parallel fourths.

    >>> from music21 import note, stream
    >>> bass = stream.Part(map(note.Note, ['C2', 'D2', 'E2']))
    >>> tenor = stream.Part(map(note.Note, ['F3', 'G3', 'A3']))
    >>> soprano = stream.Part(map(note.Note, ['A4', 'G4', 'F4']))
    >>> check_parallel_fourths(bass, tenor)
    Traceback (most recent call last):
    ...
    errors.ParallelFourthsError: Found parallel fourths at index 1
    >>> check_parallel_fourths(bass, soprano)
    """
    was_fourth = False
    for i, (lower_note, upper_note) in enumerate(zip(bass, upper_voice)):
        current_fourth = helpers.is_fourth(lower_note, upper_note)
        if current_fourth and was_fourth and lower_note.pitch != bass[i-1].pitch:
            raise ParallelFourthsError(i)
        was_fourth = current_fourth


def check_parallel_fifths(lower_voice, upper_voice):
    """Raises an error if two voices contain parallel fifths.

    >>> from music21 import note, stream
    >>> soprano = stream.Part(map(note.Note, ['F5', 'G5', 'A5']))
    >>> alto = stream.Part(map(note.Note, ['G4', 'G4', 'G4']))
    >>> bass = stream.Part(map(note.Note, ['C3', 'C3', 'D3']))
    >>> check_parallel_fifths(alto, soprano)
    >>> check_parallel_fifths(bass, soprano)
    Traceback (most recent call last):
    ...
    errors.ParallelFifthsError: Found parallel fifths at index 2
    >>> check_parallel_fifths(bass, alto)
    """
    was_p5 = False
    for i, (lower_note, upper_note) in enumerate(zip(lower_voice, upper_voice)):
        is_p5 = helpers.is_perfect_fifth(lower_note, upper_note)
        if is_p5 and was_p5 and lower_note.pitch != lower_voice[i-1].pitch:
            raise ParallelFifthsError(i)
        was_p5 = is_p5


def check_parallel_octaves(lower_voice, upper_voice):
    """Raises an error if two voices contain parallel octaves.

    >>> from music21 import note, stream
    >>> soprano = stream.Part(map(note.Note, ['D5', 'C5', 'D5']))
    >>> alto = stream.Part(map(note.Note, ['C4', 'C4', 'G4']))
    >>> bass = stream.Part(map(note.Note, ['C3', 'C3', 'D3']))
    >>> check_parallel_octaves(alto, soprano)
    >>> check_parallel_octaves(bass, soprano)
    ...
    Traceback (most recent call last):
    errors.ParallelOctavesError: Found parallel octaves at index 2
    >>> check_parallel_octaves(bass, alto)
    """
    was_p8 = False
    for i, (lower_note, upper_note) in enumerate(zip(lower_voice, upper_voice)):
        is_p8 = helpers.is_perfect_octave(lower_note, upper_note)
        if is_p8 and was_p8 and lower_note.pitch != lower_voice[i-1].pitch:
            raise ParallelOctavesError(i)
        was_p8 = is_p8


def check_direct_fifths(bass, soprano):
    """Raises an error if two voices contain direct fifths.

    >>> from music21 import note, stream
    >>> soprano = stream.Part(map(note.Note, ['C5', 'C5', 'E5']))
    >>> bass = stream.Part(map(note.Note, ['E3', 'G3', 'A3']))
    >>> check_direct_fifths(bass, soprano)
    Traceback (most recent call last):
    errors.DirectFifthsError: Found direct fifth at index 2
    >>> soprano = stream.Part(map(note.Note, ['C5', 'D5', 'E5']))
    >>> check_direct_fifths(bass, soprano)
    """
    if len(bass) <= 1:
        return
    for i, (bass_note, soprano_note) in enumerate(zip(bass, soprano)):
        is_p5 = helpers.is_perfect_fifth(bass_note, soprano_note)
        if is_p5 and i > 0:
            bass_motion = interval.notesToGeneric(bass[i-1], bass_note).directed
            soprano_motion = interval.notesToGeneric(soprano[i-1], soprano_note).directed
            if soprano_motion * bass_motion > 0 and abs(soprano_motion) > 2:
                raise DirectFifthsError(i)


def check_direct_octaves(bass, soprano):
    """Raises an error if two voices contain direct octaves.

    >>> from music21 import note, stream
    >>> soprano = stream.Part(map(note.Note, ['C5', 'D5', 'E5']))
    >>> bass = stream.Part(map(note.Note, ['E3', 'D3', 'A3']))
    >>> check_direct_octaves(bass, soprano)
    >>> soprano = stream.Part(map(note.Note, ['E5', 'E5', 'A5']))
    >>> check_direct_octaves(bass, soprano)
    Traceback (most recent call last):
    ...
    errors.DirectOctavesError: Found direct octave at index 2
    """
    if len(bass) <= 1:
        return
    for i, (bass_note, soprano_note) in enumerate(zip(bass, soprano)):
        is_p8 = helpers.is_perfect_octave(bass_note, soprano_note)
        if is_p8 and i > 0:
            bass_motion = interval.notesToGeneric(bass[i-1], bass_note).directed
            soprano_motion = interval.notesToGeneric(soprano[i-1], soprano_note).directed
            if soprano_motion * bass_motion > 0 and abs(soprano_motion) > 2:
                raise DirectOctavesError(i)
