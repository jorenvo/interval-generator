from typing import Tuple

from playsound import playsound  # type: ignore
from tones import SINE_WAVE  # type: ignore
from tones.mixer import Mixer  # type: ignore
from random import randint

NOTES = ("a", "a#", "b", "c", "c#", "d", "d#", "e", "f", "f#", "g", "g#")
assert len(NOTES) == 12


class Note:
    def __init__(self, name: str, octave: int):
        self.name = name
        self.octave = octave


def generate_interval(semitones: int) -> Tuple[Note, Note]:
    assert 0 <= semitones <= len(NOTES)
    octave = randint(3, 5)
    root = randint(0, len(NOTES) - 1)

    extra = root + semitones
    octave_extra = octave
    if extra >= len(NOTES):
        extra -= len(NOTES)
        octave_extra += 1

    return Note(NOTES[root], octave), Note(NOTES[extra], octave_extra)


def setup_mixer():
    mixer = Mixer(44100, 0.5)
    mixer.create_track(0, SINE_WAVE, attack=0.01, decay=0.1)
    mixer.create_track(1, SINE_WAVE, attack=0.01, decay=0.1)
    return mixer


def generate_intervals(mixer, interval_semitones: int):
    duration_s = 4
    amount = 4

    for _ in range(amount):
        note_a, note_b = generate_interval(interval_semitones)
        mixer.add_note(0, note=note_a.name, octave=note_a.octave, duration=duration_s)
        mixer.add_note(1, note=note_b.name, octave=note_b.octave, duration=duration_s)
        mixer.add_silence(0, 0.1)
        mixer.add_silence(1, 0.1)


def write_and_play(mixer):
    wave_file = "/tmp/tones.wav"
    mixer.write_wav(wave_file)
    playsound(wave_file)


def run():
    mixer = setup_mixer()
    generate_intervals(mixer, 4)
    write_and_play(mixer)


if __name__ == "__main__":
    run()
