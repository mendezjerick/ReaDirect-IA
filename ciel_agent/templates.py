from __future__ import annotations


def correct_praise(expected: str) -> str:
    return f"Good job. You read {expected} correctly." if expected else "Good job. That is correct."


def final_completion() -> str:
    return "You completed the final assessment. Well done. Let's see your results."


def low_confidence() -> str:
    return "I could not hear that clearly. Speak clearly and try recording again."


def first_retry(expected: str) -> str:
    return f"Good try. Read {expected} once more." if expected else "Good try. Please try once more."


def focus_teach(expected: str) -> str:
    return (
        f"Let's practice {expected}. Listen carefully. {expected}."
        if expected
        else "Let's practice this together. Listen carefully, then repeat."
    )


def letter_confusion(expected: str, transcript: str) -> str:
    if expected and transcript:
        return f"{expected} and {transcript} sound close. Let's listen carefully: {expected}."
    return focus_teach(expected)


def vowel_confusion(expected: str) -> str:
    return (
        f"Listen to the middle sound in {expected.lower()}."
        if expected
        else "Listen carefully to the middle sound."
    )


def final_sound_missing(expected: str) -> str:
    return (
        f"Good start. Let's finish {expected.lower()} with the last sound."
        if expected
        else "Good start. Let's finish the word with the last sound."
    )


def slow_practice(expected: str) -> str:
    return (
        f"Read slowly, one part at a time: {expected}."
        if expected
        else "Read slowly, one part at a time."
    )
