# ReaDirect-IA Automatic Mode Contract Readiness

Date prepared: 2026-06-17

Scope: small schema extension and documentation only. No Ciel decision behavior, deterministic engine rules, animation list, memory behavior, or final-congrats validation was changed.

Prompt 3 implementation note: Laravel now sends the optional automatic-session context fields when Automatic Ciel Listening Mode checks a module item. ReaDirect-IA code was not changed in Prompt 3; the fields remain optional and decision behavior remains deterministic and scoring-neutral.

## Current Endpoint Status

The current endpoint for Ciel decisions is:

```text
POST /ia/ciel/decide
```

The service receives already-scored learner attempt evidence and returns a constrained `ciel_agent` payload. It remains decision-only and cannot alter official scoring, placement, mastery, or progression.

## Current Request Contract

Existing evidence fields:

- `learner_id`
- `session_id`
- `module_type`
- `expected`
- `transcript`
- `is_correct`
- `attempt`
- `asr_confidence`
- `gop_score`
- `phoneme_errors`
- `error_type`
- `target_phoneme`
- `activity_id`
- `is_final_assessment_completion`
- `audio_duration_seconds`
- `audio_too_short`
- `retry_required`
- `uncertain`

Prompt 2 added optional future context fields:

- `listening_mode`
- `session_mode`
- `automatic_session_id`
- `current_agent_state`
- `silence_timeout`
- `chunk_id`

These fields are optional and are not used by the Ciel engine yet. They are accepted only to make Prompt 3 integration explicit and backward compatible.

## Current Response Contract

`/ia/ciel/decide` returns:

```json
{
  "ciel_agent": {
    "agent": "ciel",
    "mode": "focus_teach",
    "animation": "c-advise",
    "emotion": "gentle_correction",
    "message": "Let's practice CAT. Listen carefully. CAT.",
    "display_target": "CAT",
    "next_action": "listen_then_retry",
    "lock_interaction": true,
    "repeat_after_agent": true,
    "teaching_focus": "final_sound_missing",
    "focus_mode": {
      "enabled": true,
      "layout": "blank_screen",
      "target_position": "center",
      "agent_position": "bottom",
      "target_size": "large"
    },
    "memory_update": {
      "error_key": "FINAL_SOUND_MISSING",
      "count_increment": 1,
      "current_count": 1,
      "learner_id": "1",
      "session_id": "module-session"
    },
    "reason_codes": ["FINAL_SOUND_MISSING"],
    "official_progression_changed": false,
    "decision_trace": ["perceive", "decide", "act", "observe_update"]
  }
}
```

## Animation Safety

Allowed Ciel animations remain:

- `c-advise`
- `c-clap`
- `c-confused`
- `c-congrats`
- `c-happy`
- `c-idle`
- `c-talk`
- `c-thinking-1`
- `c-thinking-2`
- `c-thinking-3`

`c-congrats` remains restricted to `final_assessment_completion`. Normal correct answers, retries, and automatic listening sessions must not use it.

## Prompt 3 Guidance

Prompt 3 should call IA only after Laravel has uploaded/analyzed audio and applied official scoring/progression rules. Laravel should pass the scored attempt evidence plus optional automatic-session fields. IA should continue to return Ciel presentation decisions only.
