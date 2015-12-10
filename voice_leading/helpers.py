from music21 import interval


def is_lower_note(first_note, second_note):
    """Given two notes, returns whether the first note is lower or equal to the second note.

    >>> from music21 import note
    >>> is_lower_note(note.Note('C3'), note.Note('D3'))
    True
    >>> is_lower_note(note.Note('C3'), note.Note('B2'))
    False
    """
    return interval.getAbsoluteLowerNote(first_note, second_note) is first_note


def is_fourth(lower_note, upper_note):
    """Returns whether the interval between two given notes reduced to an octave is a is_fourth.

    >>> from music21 import note
    >>> c4 = note.Note('C4')
    >>> f4 = note.Note('F4')
    >>> g4 = note.Note('G4')
    >>> is_fourth(c4, f4)
    True
    >>> is_fourth(c4, g4)
    False
    """
    test_interval = interval.notesToGeneric(lower_note, upper_note)
    if test_interval.simpleUndirected == 4:
        return True
    return False


def is_perfect_fifth(lower_note, upper_note):
    """Returns whether the interval between two given notes reduced to an octave is a perfect fifth.

    >>> from music21 import note
    >>> c4 = note.Note('C4')
    >>> g4 = note.Note('G4')
    >>> g7 = note.Note('G7')
    >>> is_perfect_fifth(c4, g4)
    True
    >>> is_perfect_fifth(c4, g7)
    True
    >>> is_perfect_fifth(g4, g7)
    False
    """
    test_interval = interval.Interval(lower_note, upper_note)
    if test_interval.simpleName == "P5":
        return True
    return False


def is_perfect_octave(lower_note, upper_note):
    """Returns whether the interval between two given notes reduced to an octave is a perfect octave.

    >>> from music21 import note
    >>> c4 = note.Note('C4')
    >>> c5 = note.Note('C5')
    >>> is_perfect_octave(c4, c5)
    True
    >>> c6 = note.Note('C6')
    >>> is_perfect_octave(c4, c6)
    True
    >>> g4 = note.Note('G4')
    >>> is_perfect_octave(c4, g4)
    False
    """

    test_interval = interval.Interval(lower_note, upper_note)
    if test_interval.semiSimpleName == "P8":
        return True
    return False
