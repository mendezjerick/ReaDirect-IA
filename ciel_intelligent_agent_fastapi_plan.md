# Miss Ciel Intelligent Agent Plan

**Project:** ReaDirect  
**Agent:** Miss Ciel  
**Repository Focus:** ReaDirect-IA as a FastAPI-based Ciel agent service  
**Status:** Draft planning document  
**Purpose:** This document records the current planned direction for making Miss Ciel a bounded intelligent pedagogical agent. It can be revised later after the next implementation step.

---

## 1. Current Decision

Miss Ciel will be developed as the main intelligent pedagogical agent of ReaDirect. Vivian and Estelle will remain role-based pedagogical agents for now.

The intelligent behavior of Miss Ciel will not be based on a generative LLM. Instead, Ciel will use a deterministic intelligent-agent loop:

```text
Perceive learner reading event
-> interpret learner state and ASR/expected-centric evidence
-> evaluate coaching goals and rules
-> select feedback strategy
-> return Ciel action, dialogue, and reason codes
-> observe learner's next attempt
-> adjust next support level through a reinforcement mechanism
```

This means Ciel will function as a bounded autonomous agent inside the reading-coaching workflow. She may decide how to respond to learner practice attempts, but she must not control official assessment, scoring, placement, mastery, or progression.

---

## 2. Why Ciel Becomes the Intelligent Agent

Miss Ciel is the most appropriate agent to become intelligent because her role is the actual reading coach. She interacts with learners during practice, remediation, retry guidance, and feedback.

The expected role separation is:

| Agent | Role | Intelligence Level |
|---|---|---|
| Miss Vivian | Assessment guide | Role-based, neutral, scripted |
| Miss Ciel | Reading coach | Intelligent pedagogical agent |
| Miss Estelle | Results and recommendation guide | Role-based, explanatory, scripted |

Ciel becomes intelligent because she will perceive reading conditions, make coaching decisions, and act toward instructional goals.

---

## 3. Intelligent Agent Definition Applied to Ciel

An intelligent agent is an autonomous software entity that perceives its environment, makes decisions, and takes actions to achieve specific goals.

For Miss Ciel:

| Intelligent Agent Part | ReaDirect Equivalent |
|---|---|
| Environment | ReaDirect module/practice reading session |
| Perception | Learner attempt, ASR output, expected-centric result, error type, attempt count, retry status |
| Rules Set | Ciel policies, coaching rules, guardrails, and dialogue templates |
| Decision-Making | ReaDirect-IA FastAPI Ciel decision service |
| Action | Ciel dialogue, TTS cue, animation action, retry guidance, encouragement |
| Goal | Help the learner improve reading while preserving official system decisions |
| Feedback / Reinforcement | Learner's next attempt, repeated error tracking, success after hint, support-level adjustment |

The system should frame Ciel as a **bounded intelligent pedagogical agent**, not a general chatbot and not an unrestricted AI assistant.

---

## 4. Important Boundary

Ciel must not control or modify official educational decisions.

Ciel must not change:

- official score;
- assessment result;
- diagnostic result;
- final assessment result;
- module placement;
- mastery threshold;
- learner progression;
- database authority for official learning status.

Ciel may only influence:

- coaching message;
- feedback type;
- hint level;
- animation/action selection;
- TTS text;
- support level for the next coaching response.

---

## 5. Repository Architecture

The new direction places Ciel's decision-making brain in **ReaDirect-IA** as a FastAPI service.

```text
ReaDirect Laravel
    -> sends learner event + ASR evidence + learner state
ReaDirect-IA FastAPI
    -> Ciel perceives, evaluates rules, applies reinforcement mechanism
    -> returns Ciel action + dialogue + reason codes
ReaDirect Laravel
    -> sends approved message to TTS
    -> sends agent cue to Vue
Vue frontend
    -> displays Ciel animation/dialogue
```

### 5.1 ReaDirect Responsibilities

ReaDirect remains the runtime authority for:

- learner records;
- modules and practice workflow;
- official scoring;
- expected-centric scoring output;
- ASR result handling;
- retry history;
- mastery and progression;
- communication with ReaDirect-IA;
- TTS request triggering;
- Vue/Inertia response delivery;
- fallback behavior if ReaDirect-IA is unavailable.

### 5.2 ReaDirect-IA Responsibilities

ReaDirect-IA becomes the Ciel intelligent-agent service. It owns:

- Ciel perception schema;
- Ciel decision schema;
- coaching rules;
- goal selection logic;
- support-level logic;
- reinforcement mechanism;
- dialogue templates;
- reason codes;
- policy version;
- Ciel-specific tests and scenarios.

### 5.3 ReaDirect-AI-ASR Responsibilities

ReaDirect-AI-ASR remains responsible only for speech-related evidence:

- transcript;
- ASR confidence;
- uncertainty flags;
- retry-required flags;
- pronunciation evidence;
- phoneme/GOP evidence if available;
- expected-centric comparison support;
- error type support.

It must not decide what Ciel says.

### 5.4 ReaDirect-TTS Responsibilities

ReaDirect-TTS remains a renderer only:

```text
approved Ciel message + Ciel voice -> audio output
```

It must not decide the message or coaching strategy.

### 5.5 ReaDirect-Game Status

ReaDirect-Game is paused/idle for now. It is not part of the current intelligent-agent implementation.

The current focus is only Ciel's module/practice coaching intelligence.

---

## 6. Ciel Agent Processing Loop

The planned Ciel loop is:

```text
1. Learner performs a reading attempt.
2. ReaDirect receives ASR and expected-centric analysis.
3. ReaDirect builds a Ciel perception event.
4. ReaDirect sends the event to ReaDirect-IA FastAPI.
5. Ciel interprets the learner condition.
6. Ciel checks rules, goals, learner state, and support level.
7. Ciel returns a decision.
8. ReaDirect sends the message to TTS and sends the cue to Vue.
9. Learner retries or continues.
10. ReaDirect sends the next outcome to Ciel's reinforcement mechanism.
11. Ciel adjusts the next support level or strategy.
```

---

## 7. FastAPI Service Endpoints

The initial ReaDirect-IA FastAPI service should start small.

Recommended endpoints:

```text
GET  /health
GET  /ciel/policy-version
POST /ciel/decide
POST /ciel/reinforce
```

### 7.1 `GET /health`

Purpose: confirm the Ciel agent service is running.

Example response:

```json
{
  "status": "ok",
  "service": "readirect-ia",
  "agent": "ciel",
  "mode": "deterministic",
  "llm_enabled": false
}
```

### 7.2 `GET /ciel/policy-version`

Purpose: return the current Ciel policy/rule version.

Example response:

```json
{
  "agent": "ciel",
  "policy_version": "0.1.0",
  "decision_mode": "rule_based_with_reinforcement_mechanism"
}
```

### 7.3 `POST /ciel/decide`

Purpose: receive a learner event and return Ciel's coaching decision.

Example input:

```json
{
  "event_type": "learner.response_checked",
  "learner_id": "hashed-or-internal-id",
  "context": "module_practice",
  "activity_type": "display_word_reading",
  "expected_text": "log",
  "transcript": "lug",
  "is_correct": false,
  "error_type": "vowel_confusion",
  "similarity_label": "close",
  "attempt_number": 2,
  "remaining_attempts": 1,
  "retry_required": false,
  "uncertain": false,
  "learner_state": {
    "correct_streak": 0,
    "incorrect_streak": 2,
    "repeated_error_type": "vowel_confusion",
    "support_level": "guided"
  }
}
```

Example response:

```json
{
  "decision_id": "uuid",
  "agent": "ciel",
  "goal": "correct_specific_reading_error",
  "action": "advise",
  "dialogue_key": "ciel.vowel_confusion.guided",
  "message": "Almost there. Listen to the middle sound and try again.",
  "reason_codes": [
    "VOWEL_CONFUSION",
    "RETRY_AVAILABLE",
    "GUIDED_SUPPORT"
  ],
  "support_level": "guided",
  "should_request_tts": true,
  "official_progression_changed": false
}
```

### 7.4 `POST /ciel/reinforce`

Purpose: send learner outcome after Ciel's previous feedback, so Ciel can update the next support strategy.

Example input:

```json
{
  "learner_id": "hashed-or-internal-id",
  "previous_decision_id": "uuid",
  "previous_error_type": "vowel_confusion",
  "previous_action": "advise",
  "next_attempt_correct": true,
  "same_error_repeated": false,
  "learner_continued": true
}
```

Example response:

```json
{
  "updated_support_level": "normal",
  "reinforcement_result": "hint_helped",
  "next_strategy": "encourage_progress"
}
```

---

## 8. Perception Event Contract

Ciel should receive structured, learner-safe information only.

Suggested input fields:

```json
{
  "event_type": "learner.response_checked",
  "learner_id": "hashed-or-internal-id",
  "context": "module_practice",
  "activity_type": "module lesson key, mastery_check, read_passage, or listening-game key",
  "expected_text": "string or null",
  "transcript": "string or null",
  "is_correct": true,
  "error_type": "vowel_confusion | initial_sound_error | middle_sound_error | final_sound_error | omission | insertion | substitution | word_boundary_error | unclear_audio | unknown | null",
  "similarity_label": "exact | very_close | close | far | unclear | null",
  "attempt_number": 1,
  "remaining_attempts": 2,
  "retry_required": false,
  "uncertain": false,
  "learner_state": {
    "correct_streak": 0,
    "incorrect_streak": 1,
    "repeated_error_type": "vowel_confusion",
    "weak_skill": "middle_vowel_sound",
    "support_level": "normal"
  }
}
```

Do not send unnecessary technical details to Ciel, such as:

- raw tensors;
- logits;
- full acoustic arrays;
- private learner information;
- unnecessary database fields;
- internal model debugging output.

---

## 9. Decision Contract

Ciel should return a stable, frontend-ready decision.

Suggested response fields:

```json
{
  "decision_id": "uuid",
  "agent": "ciel",
  "goal": "correct_specific_reading_error",
  "action": "advise",
  "dialogue_key": "ciel.final_sound.guided",
  "message": "Almost there. Say the ending sound clearly this time.",
  "reason_codes": ["FINAL_SOUND_ERROR", "RETRY_AVAILABLE"],
  "support_level": "guided",
  "should_request_tts": true,
  "official_progression_changed": false
}
```

The field `official_progression_changed` must always be `false`.

---

## 10. Ciel Goals

Ciel's decision-making should be goal-based.

Suggested goals:

| Goal Key | Meaning |
|---|---|
| `request_clear_audio` | Ask learner to retry because the audio is unclear or unusable |
| `correct_specific_reading_error` | Give a targeted hint based on the detected error type |
| `encourage_retry` | Encourage learner to try again after a mistake |
| `reinforce_success` | Praise correct reading |
| `support_repeated_error` | Provide stronger guidance when the same error repeats |
| `reduce_frustration` | Use kinder encouragement after repeated incorrect attempts |
| `celebrate_progress` | Congratulate learner for streaks or section completion |
| `stay_idle` | Avoid unnecessary intervention |

---

## 11. Ciel Actions

Ciel's decisions should map to visible actions and media.

| Action | Use Case |
|---|---|
| `idle` | No active feedback needed |
| `talk` | General instruction or explanation |
| `thinking` | ASR/checking/processing state |
| `confused` | Unclear audio, uncertain result, or system could not understand |
| `advise` | Corrective hint or retry guidance |
| `happy` | Correct answer or ordinary success |
| `clap` | Strong streak or section completion |
| `congrats` | Explicit completion flow only |

---

## 12. Rule Set

The initial Ciel brain can use deterministic rules.

### 12.1 Highest-Priority Guardrails

1. If context is diagnostic or final assessment, return no Ciel tutoring decision.
2. Ciel must not reveal hidden answers in assessment.
3. Ciel must not change official scoring or progression.
4. Ciel must not use LLM-generated text.
5. If ASR is uncertain or audio is unclear, do not treat it as learner failure.

### 12.2 Processing Rule

If ASR or checking is in progress:

```text
action = thinking
goal = stay_supportive_during_processing
```

### 12.3 Unclear Audio Rule

If `retry_required = true`, `uncertain = true`, `error_type = unclear_audio`, or `similarity_label = unclear`:

```text
action = confused
goal = request_clear_audio
message = ask learner to try recording again clearly
```

### 12.4 Corrective Hint Rule

If answer is wrong and retry is available:

| Error Type | Coaching Focus |
|---|---|
| `vowel_confusion` | Middle vowel sound |
| `initial_sound_error` | First sound |
| `middle_sound_error` | Middle sound |
| `final_sound_error` | Ending sound |
| `omission` | Say every part |
| `insertion` | Say only what is shown |
| `word_boundary_error` | Pause between words |
| `substitution` or `unknown` | Try again slowly and clearly |

### 12.5 Success Rule

If learner is correct:

```text
action = happy
goal = reinforce_success
```

### 12.6 Strong Progress Rule

If learner has a correct streak or completed a section:

```text
action = clap
goal = celebrate_progress
```

### 12.7 Completion Rule

If final completion is explicitly allowed:

```text
action = congrats
goal = celebrate_progress
```

---

## 13. Reinforcement Mechanism

This plan uses a **reinforcement mechanism**, not full reinforcement learning.

The mechanism observes whether Ciel's last coaching action helped the learner improve.

Example loop:

```text
Learner makes vowel confusion error
-> Ciel gives middle-sound hint
-> Learner retries
-> System checks if learner corrected the error
-> Ciel adjusts support level for the next response
```

### 13.1 Support Levels

Suggested support levels:

| Support Level | Meaning |
|---|---|
| `normal` | Basic hint or encouragement |
| `guided` | More specific guidance after repeated error |
| `strong_guidance` | Slower, clearer instruction after repeated failure |
| `encouragement` | Positive reinforcement after improvement |
| `retry_clear_audio` | Audio clarity retry support |

### 13.2 Reinforcement Outcomes

Possible reinforcement results:

| Result | Meaning |
|---|---|
| `hint_helped` | Learner corrected the error after Ciel's feedback |
| `same_error_repeated` | Learner repeated the same error |
| `learner_improved_but_not_correct` | Learner got closer but not fully correct |
| `learner_disengaged` | Learner did not continue or stopped attempt |
| `audio_issue_persisted` | Recording/audio remained unclear |

### 13.3 Example Support Adjustment

```text
If hint_helped:
    support_level = normal or encouragement

If same_error_repeated once:
    support_level = guided

If same_error_repeated multiple times:
    support_level = strong_guidance

If audio_issue_persisted:
    support_level = retry_clear_audio
```

This allows Ciel to adapt without unsafe trial-and-error learning.

---

## 14. Dialogue Templates

Ciel should not generate free-form text. Messages should come from approved templates.

Example templates:

```yaml
ciel.audio_unclear:
  - "I could not hear that clearly. Please try again with your clear reading voice."
  - "Let us try that again. Speak clearly when you are ready."

ciel.vowel_confusion.normal:
  - "Almost there. Listen to the middle sound and try again."

ciel.vowel_confusion.guided:
  - "Good try. Let us focus on the middle sound this time."

ciel.final_sound.normal:
  - "Almost there. Say the ending sound clearly this time."

ciel.word_boundary.normal:
  - "Almost. Pause a little between the words."

ciel.success:
  - "Good job. You read it correctly."

ciel.strong_success:
  - "Great reading. You are getting stronger."
```

Template selection can use deterministic variation, such as:

```text
variant index = hash(learner_id + dialogue_key + attempt_number) % number_of_variants
```

---

## 15. FastAPI Internal Structure

Suggested ReaDirect-IA structure:

```text
ReaDirect-IA/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── ciel.py
│   ├── schemas/
│   │   ├── ciel_event.py
│   │   ├── ciel_decision.py
│   │   └── ciel_reinforcement.py
│   ├── services/
│   │   ├── ciel_agent_service.py
│   │   ├── ciel_policy_engine.py
│   │   ├── learner_state_service.py
│   │   ├── reinforcement_service.py
│   │   └── dialogue_service.py
│   ├── policies/
│   │   └── ciel_rules.yaml
│   ├── dialogue/
│   │   └── ciel.yaml
│   └── tests/
│       ├── test_ciel_decide.py
│       └── test_ciel_reinforce.py
├── requirements.txt
├── README.md
└── .env.example
```

---

## 16. Laravel Integration Plan

ReaDirect should call ReaDirect-IA after module ASR/scoring result is available.

Recommended Laravel-side service:

```text
CielAgentClient
```

Responsibilities:

- build request payload;
- call `POST /ciel/decide`;
- handle timeout safely;
- handle service unavailable fallback;
- return `agent_cue` to Vue;
- never block official scoring if Ciel service fails.

### 16.1 Recommended Timeout

Use a short timeout, such as:

```text
1.5 to 3 seconds
```

If ReaDirect-IA is unavailable, ReaDirect should use a safe local fallback message.

### 16.2 Vue Response Shape

ReaDirect can return:

```json
{
  "agent_cue": {
    "agent": "ciel",
    "action": "advise",
    "message": "Almost there. Listen to the middle sound and try again.",
    "dialogue_key": "ciel.vowel_confusion.normal",
    "reason_codes": ["VOWEL_CONFUSION", "RETRY_AVAILABLE"],
    "should_request_tts": true,
    "official_progression_changed": false
  }
}
```

Vue should display the resolved Ciel action. It should not reinterpret correct/wrong labels into animations if `agent_cue.action` is already present.

---

## 17. Fallback Behavior

The system must fail safely.

| Failure | Required Fallback |
|---|---|
| ReaDirect-IA offline | Use local scripted fallback |
| `/ciel/decide` timeout | Continue learner flow with generic Ciel message |
| Invalid Ciel response | Ignore response and use fallback |
| TTS unavailable | Show text only |
| Ciel media unavailable | Use idle video or PNG fallback |
| Logging fails | Do not block learner flow |

Ciel failure must never break learner scoring or progression.

---

## 18. No-LLM Rule

Ciel must not use:

- OpenAI;
- Ollama;
- Claude;
- any local LLM;
- any cloud LLM;
- free-form generated text.

The system may describe Ciel as intelligent because she perceives learner evidence, evaluates goals/rules, acts through feedback, and adjusts using a reinforcement mechanism. She does not need an LLM to qualify as an intelligent agent.

---

## 19. Testing Plan

### 19.1 ReaDirect-IA Tests

Test cases:

- unclear audio -> `confused`;
- processing -> `thinking`;
- vowel confusion -> middle sound hint;
- initial sound error -> first sound hint;
- final sound error -> ending sound hint;
- word boundary error -> pause-between-words hint;
- correct response -> `happy`;
- correct streak -> `clap`;
- assessment context -> no Ciel tutoring;
- repeated same error -> support level increases;
- correct after hint -> support level returns to normal/encouragement;
- no LLM call occurs.

### 19.2 ReaDirect Integration Tests

Test cases:

- ReaDirect sends expected payload to ReaDirect-IA;
- ReaDirect handles successful response;
- ReaDirect handles timeout;
- ReaDirect handles invalid response;
- official scoring remains unchanged;
- Vue receives `agent_cue`;
- TTS receives only approved Ciel message.

---

## 20. Phased Implementation Plan

### Phase 1: ReaDirect-IA Ciel FastAPI Foundation

Goal: create the standalone Ciel agent service.

Tasks:

- create FastAPI app;
- add `/health`;
- add `/ciel/policy-version`;
- add `/ciel/decide`;
- implement deterministic Ciel rules;
- add dialogue templates;
- add tests for core decisions;
- ensure no LLM dependencies.

Exit criteria:

- FastAPI service starts;
- `/health` works;
- `/ciel/decide` returns Ciel action/message/reasons;
- tests pass.

### Phase 2: Laravel Integration

Goal: connect ReaDirect to ReaDirect-IA.

Tasks:

- add CielAgentClient;
- call `/ciel/decide` after module scoring;
- return `agent_cue` to Vue;
- add timeout/fallback handling;
- preserve official scoring and progression.

Exit criteria:

- module practice receives Ciel decision from ReaDirect-IA;
- fallback works when ReaDirect-IA is offline;
- official scoring is unchanged.

### Phase 3: Reinforcement Mechanism

Goal: allow Ciel to adapt support level from learner outcomes.

Tasks:

- add `/ciel/reinforce`;
- send next-attempt outcome from ReaDirect;
- update support level based on repeated errors or improvement;
- store or return lightweight state;
- add tests.

Exit criteria:

- repeated errors produce stronger guidance;
- correct after hint produces encouragement/normal support;
- reinforcement mechanism is deterministic and explainable.

### Phase 4: Frontend and TTS Refinement

Goal: make Ciel decisions visible and natural.

Tasks:

- Vue uses `agent_cue.action` directly;
- Ciel videos match action;
- no-interrupt/no-queue behavior remains;
- TTS uses approved Ciel message only;
- fallback if TTS/media fails.

Exit criteria:

- Ciel speaks and animates according to ReaDirect-IA decision;
- no frontend educational decision duplication;
- learner flow remains stable.

### Phase 5: Documentation and Thesis Framing

Goal: document the agent architecture.

Tasks:

- document Ciel as bounded intelligent pedagogical agent;
- document perception, rules, action, and reinforcement mechanism;
- document boundaries and no-LLM decision;
- update diagrams if needed.

Exit criteria:

- Ciel can be defended as an intelligent agent;
- system remains explainable and reproducible.

---

## 21. Suggested Thesis Framing

Miss Ciel may be described as:

> a bounded intelligent pedagogical agent that perceives learner reading events, interprets ASR and expected-centric evidence, evaluates coaching goals and rules, selects appropriate feedback actions, and adapts later support through a reinforcement mechanism based on learner outcomes.

Avoid describing Ciel as:

- a chatbot;
- a generative AI agent;
- a reinforcement learning model;
- an agent that controls official scoring;
- an agent that replaces teacher judgment.

---

## 22. Immediate Next Step

The next implementation step should be:

```text
Build the ReaDirect-IA FastAPI Ciel service with /health, /ciel/decide, deterministic rule evaluation, dialogue templates, and no LLM dependency.
```

Do not implement reinforcement first. Start with deterministic decisions. Add reinforcement after the first working decision loop is stable.

---

## 23. Notes for Future Revision

This plan may change after the next implementation step. Possible future changes:

- move some fallback logic back into Laravel;
- store Ciel state in ReaDirect instead of ReaDirect-IA;
- add a decision log table;
- add a small admin/debug view;
- revise support levels based on actual testing;
- add teacher-reviewed policy editing;
- reconnect ReaDirect-Game later if needed.
