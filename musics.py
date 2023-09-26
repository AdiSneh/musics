import random
import re
from enum import Enum

from musicpy.algorithms import detect as detect_chord
from musicpy.structures import circle_of_fifths as CircleOfFifths, scale as Scale


class Mode(str, Enum):
    MAJOR = "major"
    MINOR = "minor"


NOTES = {
    Mode.MAJOR: CircleOfFifths.outer,
    Mode.MINOR: CircleOfFifths.inner,
}


def format_chord(chord: str) -> str:
    if chord.endswith(Mode.MINOR):
        return chord.removesuffix(Mode.MINOR) + "m"
    if chord.endswith(Mode.MAJOR):
        return chord.removesuffix(Mode.MAJOR)
    return chord


def generate_chords(scale: Scale, amount: int) -> list[str]:
    return [
        format_chord(detect_chord(scale(i)))
        for i in random.sample(range(7), amount)
    ]


def parse_scale(scale: str) -> Scale | None:
    scale_regex = re.compile("(?P<note>.*?)(?P<minor_suffix>m)?")
    match_dict = scale_regex.fullmatch(scale).groupdict()
    note = match_dict["note"]
    mode = Mode.MINOR if match_dict["minor_suffix"] else Mode.MAJOR
    try:
        return Scale(note, mode)
    except ValueError:
        return None


def get_scale_name(scale: Scale) -> str:
    return scale.get_scale_name(with_octave=False).removesuffix(" scale")


def main():
    while True:
        mode = random.choice(list(Mode))
        scale = parse_scale(random.choice(NOTES[mode]))
        correct_answers = [scale, scale.relative_key()]
        chords = generate_chords(scale, amount=4)
        guess = input(f"What scale is this: {', '.join(chords)}\n")
        while (parsed_guess := parse_scale(guess)) not in correct_answers:
            if parsed_guess is None:
                print("Your guess must be in the format C/Cm.")
            guess = input("Try again...\n")
        print("Correct!")
        correct_answers_text = ", ".join(get_scale_name(scale) for scale in correct_answers)
        print(f"Correct answers: {correct_answers_text}")


if __name__ == '__main__':
    main()
