from __future__ import annotations

from . import templates
from .memory import JsonSessionMemory, SessionMemory
from .rules import Perception, perceive
from .schemas import AttemptContext, CielAgentDecision, FocusMode


class CielTutorAgent:
    version = "0.1.0"

    def __init__(self, memory: SessionMemory | None = None) -> None:
        self.memory = memory or JsonSessionMemory()

    def decide(self, context: AttemptContext | dict) -> CielAgentDecision:
        attempt = (
            context
            if isinstance(context, AttemptContext)
            else AttemptContext.model_validate(context)
        )
        perception = perceive(attempt)
        memory_update = self.memory.increment(
            attempt.learner_id,
            attempt.session_id,
            perception.memory_key,
        )
        values = self._decision_values(perception)
        return CielAgentDecision(memory_update=memory_update, **values)

    def _decision_values(self, event: Perception) -> dict:
        if event.is_final_completion:
            return self._base(
                mode="final_assessment_completion",
                animation="c-congrats",
                emotion="celebratory",
                message=templates.final_completion(),
                display_target=event.expected,
                next_action="show_results",
                reason_codes=["FINAL_ASSESSMENT_COMPLETION"],
            )

        if event.is_correct:
            return self._base(
                mode="correct_praise",
                animation="c-clap",
                emotion="positive_praise",
                message=templates.correct_praise(event.expected),
                display_target=event.expected,
                next_action="continue",
                reason_codes=["CORRECT_RESPONSE"],
            )

        if event.low_confidence_audio:
            return self._base(
                mode="hint",
                animation="c-thinking-1",
                emotion="patient_guidance",
                message=templates.low_confidence(),
                display_target=event.expected,
                next_action="retry_recording",
                teaching_focus="low_confidence_audio",
                reason_codes=["LOW_CONFIDENCE_AUDIO"],
            )

        if event.error_type in {
            "word_deletion",
            "word_insertion",
            "word_boundary_error",
        }:
            mode = "focus_teach" if event.attempt >= 2 else "slow_practice"
            return self._base(
                mode=mode,
                animation="c-advise",
                emotion="gentle_correction",
                message=templates.slow_practice(event.expected),
                display_target=event.expected,
                next_action=(
                    "listen_then_retry" if mode == "focus_teach" else "retry_slowly"
                ),
                lock_interaction=mode == "focus_teach",
                repeat_after_agent=mode == "focus_teach",
                teaching_focus=event.error_type,
                focus_mode=self._focus_mode(mode == "focus_teach"),
                reason_codes=[event.error_type.upper()],
            )

        if event.attempt >= 2:
            message = self._teaching_message(event)
            return self._base(
                mode="focus_teach",
                animation="c-advise",
                emotion="gentle_correction",
                message=message,
                display_target=event.expected,
                next_action="listen_then_retry",
                lock_interaction=True,
                repeat_after_agent=True,
                teaching_focus=event.error_type or "generic_error",
                focus_mode=self._focus_mode(True),
                reason_codes=[(event.error_type or "generic_error").upper()],
            )

        message = self._teaching_message(event)
        animation = (
            "c-advise"
            if event.error_type in {"vowel_confusion", "final_sound_missing"}
            else "c-confused"
        )
        return self._base(
            mode="soft_retry",
            animation=animation,
            emotion="encouraging_retry",
            message=message,
            display_target=event.expected,
            next_action="retry",
            teaching_focus=event.error_type,
            reason_codes=[(event.error_type or "generic_error").upper()],
        )

    @staticmethod
    def _teaching_message(event: Perception) -> str:
        if event.error_type == "letter_confusion":
            return templates.letter_confusion(event.expected, event.transcript)
        if event.error_type == "vowel_confusion":
            return templates.vowel_confusion(event.expected)
        if event.error_type == "final_sound_missing":
            return templates.final_sound_missing(event.expected)
        if event.attempt >= 2:
            return templates.focus_teach(event.expected)
        return templates.first_retry(event.expected)

    @staticmethod
    def _focus_mode(enabled: bool) -> FocusMode:
        if not enabled:
            return FocusMode()
        return FocusMode(
            enabled=True,
            layout="blank_screen",
            target_position="center",
            agent_position="bottom",
            target_size="large",
        )

    @staticmethod
    def _base(**overrides: object) -> dict:
        values = {
            "display_target": "",
            "lock_interaction": False,
            "repeat_after_agent": False,
            "teaching_focus": None,
            "focus_mode": FocusMode(),
            "reason_codes": [],
            "official_progression_changed": False,
        }
        values.update(overrides)
        return values
