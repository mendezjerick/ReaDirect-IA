# ReaDirect-IA

ReaDirect-IA means ReaDirect Intelligent Agent. This repository stores the
visual assets for Miss Ciel, Miss Vivian, and Miss Estelle.

It also runs Miss Ciel's lightweight deterministic tutor agent. The FastAPI
service in `main.py` owns Ciel's coaching decision loop; Laravel remains the
authority for scoring, mastery, placement, and progression.

## Ciel Tutor Agent Runtime

The engine is under `ciel_agent/`:

- `engine.py` implements perceive, decide, act, and memory update.
- `rules.py` classifies attempt and error context.
- `templates.py` contains deterministic Grade 1-friendly messages.
- `memory.py` stores learner/session error counts in local JSON.
- `schemas.py` validates inputs, modes, and exact animation labels.

No LLM, OpenAI, Ollama, or random response generation is used.

Start the service:

```powershell
python -m pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8003
```

Endpoints:

- `GET /health`
- `GET /ia/ciel/status`
- `POST /ia/ciel/decide`

Run tests and examples:

```powershell
python -m unittest discover -s tests -v
python scripts/example_decisions.py
```

## Miss Ciel Intelligent Coach Specifications

- `definitions/ciel.yaml` defines Ciel's role, contexts, actions, and
  guardrails.
- `policies/ciel-coach.yaml` documents deterministic module and future
  listening-game priorities.
- `dialogue/ciel.yaml` contains approved Grade 1-friendly messages.
- `schemas/` contains the Ciel event and decision contracts.
- `scenarios/ciel-coaching.json` contains reusable policy fixtures.
- `manifests/media.json` maps Ciel's exact existing media files.

The future `ReaDirect-Game` contract is listening-based. It supports Ciel
modeling letters, sounds, and words without learner recording, ASR,
transcripts, or scoring. The game repository and UI are not implemented here.

Miss Ciel uses deterministic approved dialogue and has no runtime LLM
dependency.

## Asset Directories

- `assets/images` contains static agent images.
- `assets/videos` contains idle and interaction animations used by ReaDirect.

## Runtime Ownership

ReaDirect-IA remains the source of truth for all agent media. ReaDirect does
not commit copies of these files. Development and production environments
expose `assets` through a static URL such as `/ia-assets`.

ReaDirect-IA is also the source of truth for Ciel tutoring decisions.
Laravel sends already-scored attempt evidence to the service and attaches the
returned `ciel_agent` payload. The agent cannot alter official scoring.

## Phase 5 Media

Idle uses looping videos:

- Ciel: `c-idle.mp4`
- Vivian: `v-idle.mp4`
- Estelle: `e-idle.mp4`

Interaction videos play once:

- Ciel: `c-thinking-1.mp4`, `c-thinking-2.mp4`, `c-thinking-3.mp4`,
  `c-talk.mp4`, `c-happy.mp4`, `c-confused.mp4`, `c-advise.mp4`,
  `c-clap.mp4`, and `c-congrats.mp4`
- Vivian: `v-talk.mp4`, `v-think.mp4`, and `v-congrats.mp4`
- Estelle: `e-talk.mp4`, `e-results-1.mp4`, `e-results-2.mp4`, and
  `e-congrats.mp4`

The runtime flow is idle video loop, interaction video once, then idle video
loop. The PNG images are fallback-only if a video fails or is missing. New
cues are ignored while an interaction prepares or plays; there is no queue.
Congrats videos remain reserved for final-assessment completion flows.

The Vivian idle filename is `v-idle.mp4`. Do not use the old
`idle v.mp4` filename.

## Phase 5 Interaction Ownership

- Miss Vivian owns diagnostic and final-assessment tasks.
  Her general spoken dialogue uses `v-talk.mp4`; processing and retry moments
  continue to use `v-think.mp4`.
- Miss Ciel owns module practice, tutoring, and mastery checks.
- Miss Estelle owns routing, results, summaries, placement, and
  recommendations.
  General spoken dialogue uses `e-talk.mp4`, while result presentation keeps
  priority and uses the `e-results` videos.

Ciel is the most dynamic agent. Ciel talk is used while tutor dialogue TTS is
actively speaking. Ciel confused is used for learner-facing
errors, unclear audio, failed checks, invalid results, mismatches, and
low-confidence responses. Ciel advise is used for correction, hints, missing
answers, and retry instructions. Context-aware mapping prevents the same
label from being interpreted identically for every agent.

## Preloading

ReaDirect preloads all idle videos, interaction videos, and fallback images
only after a homepage user clicks Start Reading, Admin Dashboard, or Teacher
Dashboard. Initial homepage loading does not start media preloading.

The frontend builds preload URLs from `VITE_REA_AGENT_ASSET_BASE_URL` and the
centralized media registry. A simple CSS/vector flipping-book screen remains
visible for at least two seconds while loading. Per-file and global timeouts
make the process fail-safe, so a missing or slow asset cannot block
navigation forever.

Preloading improves the first idle-to-interaction transition while preserving
the playback rules: interactions play once, interactions are not interrupted,
and no interaction queue is created. The current idle media remains visible
until an interaction video is ready, avoiding an empty white box.
