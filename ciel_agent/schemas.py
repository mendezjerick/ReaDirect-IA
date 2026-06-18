from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


Animation = Literal[
    "c-advise",
    "c-clap",
    "c-confused",
    "c-congrats",
    "c-happy",
    "c-idle",
    "c-talk",
    "c-thinking-1",
    "c-thinking-2",
    "c-thinking-3",
]

CielMode = Literal[
    "idle",
    "instruction",
    "listening",
    "checking",
    "correct_praise",
    "soft_retry",
    "hint",
    "focus_teach",
    "slow_practice",
    "final_encouragement",
    "final_assessment_completion",
]

AVAILABLE_ANIMATIONS = [
    "c-advise",
    "c-clap",
    "c-confused",
    "c-congrats",
    "c-happy",
    "c-idle",
    "c-talk",
    "c-thinking-1",
    "c-thinking-2",
    "c-thinking-3",
]

AVAILABLE_MODES = [
    "idle",
    "instruction",
    "listening",
    "checking",
    "correct_praise",
    "soft_retry",
    "hint",
    "focus_teach",
    "slow_practice",
    "final_encouragement",
    "final_assessment_completion",
]


class AttemptContext(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    learner_id: int | str
    session_id: str
    module_type: str = "module_practice"
    expected: str = ""
    transcript: str = ""
    is_correct: bool = False
    attempt: int = Field(default=1, ge=1)
    asr_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    gop_score: float | None = None
    phoneme_errors: list[Any] = Field(default_factory=list)
    error_type: str | None = None
    target_phoneme: str | None = None
    activity_id: int | str | None = None
    is_final_assessment_completion: bool = False
    audio_duration_seconds: float | None = Field(default=None, ge=0.0)
    audio_too_short: bool = False
    retry_required: bool = False
    uncertain: bool = False
    listening_mode: str | None = None
    session_mode: str | None = None
    automatic_session_id: str | None = None
    current_agent_state: str | None = None
    silence_timeout: float | None = Field(default=None, ge=0.0)
    chunk_id: str | None = None


class FocusMode(BaseModel):
    enabled: bool = False
    layout: Literal["standard", "blank_screen"] = "standard"
    target_position: Literal["default", "center"] = "default"
    agent_position: Literal["default", "bottom"] = "default"
    target_size: Literal["normal", "large"] = "normal"


class MemoryUpdate(BaseModel):
    error_key: str | None = None
    count_increment: int = 0
    current_count: int = 0
    learner_id: str
    session_id: str


class CielAgentDecision(BaseModel):
    agent: Literal["ciel"] = "ciel"
    mode: CielMode
    animation: Animation
    emotion: str
    message: str = Field(min_length=1, max_length=300)
    display_target: str = ""
    next_action: str
    lock_interaction: bool = False
    repeat_after_agent: bool = False
    teaching_focus: str | None = None
    focus_mode: FocusMode = Field(default_factory=FocusMode)
    memory_update: MemoryUpdate
    reason_codes: list[str] = Field(default_factory=list)
    official_progression_changed: Literal[False] = False
    decision_trace: list[Literal["perceive", "decide", "act", "observe_update"]] = Field(
        default_factory=lambda: ["perceive", "decide", "act", "observe_update"]
    )

    @model_validator(mode="after")
    def enforce_animation_policy(self) -> "CielAgentDecision":
        if self.animation == "c-congrats" and self.mode != "final_assessment_completion":
            raise ValueError(
                "c-congrats is reserved for final_assessment_completion"
            )
        if (
            self.mode == "final_assessment_completion"
            and self.animation != "c-congrats"
        ):
            raise ValueError(
                "final_assessment_completion must use c-congrats"
            )
        return self


class CielDecisionResponse(BaseModel):
    ciel_agent: CielAgentDecision


class CielStatusResponse(BaseModel):
    service: Literal["readirect-ia"] = "readirect-ia"
    engine_loaded: bool
    available_modes: list[str]
    available_animations: list[str]
    memory_backend: str
    version: str
    status: Literal["healthy", "error"]
    deterministic: Literal[True] = True
    llm_enabled: Literal[False] = False
