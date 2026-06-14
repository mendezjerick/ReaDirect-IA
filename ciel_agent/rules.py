from __future__ import annotations

import re
from dataclasses import dataclass

from .schemas import AttemptContext


LOW_CONFIDENCE_THRESHOLD = 0.50
TOO_SHORT_SECONDS = 0.30

ERROR_ALIASES = {
    "audio_too_unclear": "low_confidence_audio",
    "unclear_asr": "low_confidence_audio",
    "unclear_audio": "low_confidence_audio",
    "empty_audio": "low_confidence_audio",
    "audio_too_short": "low_confidence_audio",
    "final_sound_error": "final_sound_missing",
    "omission": "word_deletion",
    "skipped_word": "word_deletion",
    "insertion": "word_insertion",
}

KNOWN_CONFUSIONS = {
    frozenset(("B", "D")): "B_D_CONFUSION",
    frozenset(("M", "N")): "M_N_CONFUSION",
    frozenset(("T", "D")): "T_D_CONFUSION",
    frozenset(("O", "U")): "O_U_CONFUSION",
}


@dataclass(frozen=True)
class Perception:
    expected: str
    transcript: str
    error_type: str | None
    attempt: int
    is_correct: bool
    is_final_completion: bool
    low_confidence_audio: bool
    memory_key: str | None


def clean_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip()).upper()


def normalize_error_type(value: str | None) -> str | None:
    normalized = re.sub(r"[\s-]+", "_", str(value or "").strip().lower())
    if not normalized:
        return None
    return ERROR_ALIASES.get(normalized, normalized)


def perceive(context: AttemptContext) -> Perception:
    expected = clean_text(context.expected)
    transcript = clean_text(context.transcript)
    error_type = normalize_error_type(context.error_type)
    duration_too_short = (
        context.audio_duration_seconds is not None
        and context.audio_duration_seconds < TOO_SHORT_SECONDS
    )
    low_confidence = (
        not context.is_correct
        and (
            context.audio_too_short
            or duration_too_short
            or transcript == ""
            or error_type == "low_confidence_audio"
            or context.retry_required
            or context.uncertain
            or (
                context.asr_confidence is not None
                and context.asr_confidence < LOW_CONFIDENCE_THRESHOLD
            )
        )
    )

    return Perception(
        expected=expected,
        transcript=transcript,
        error_type=error_type,
        attempt=context.attempt,
        is_correct=context.is_correct,
        is_final_completion=context.is_final_assessment_completion,
        low_confidence_audio=low_confidence,
        memory_key=memory_key(
            expected=expected,
            transcript=transcript,
            error_type=error_type,
            low_confidence=low_confidence,
            is_correct=context.is_correct,
        ),
    )


def memory_key(
    *,
    expected: str,
    transcript: str,
    error_type: str | None,
    low_confidence: bool,
    is_correct: bool,
) -> str | None:
    if is_correct:
        return None
    if low_confidence:
        return "LOW_CONFIDENCE_AUDIO"
    if error_type == "letter_confusion":
        known = KNOWN_CONFUSIONS.get(frozenset((expected, transcript)))
        if known:
            return known
        pair = "_".join(filter(None, (token_key(expected), token_key(transcript))))
        return f"{pair}_CONFUSION" if pair else "GENERIC_ERROR"
    if error_type == "final_sound_missing":
        return "FINAL_SOUND_MISSING"
    if error_type:
        return token_key(error_type) or "GENERIC_ERROR"
    return "GENERIC_ERROR"


def token_key(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "_", value.upper()).strip("_")
