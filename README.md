# ReaDirect-IA

ReaDirect-IA means ReaDirect Intelligent Agent. This repository stores the
visual assets for Miss Ciel, Miss Vivian, and Miss Estelle.

## Asset Directories

- `assets/images` contains static agent images.
- `assets/videos` contains the agent animation videos used in Phase 2.

## Runtime Ownership

ReaDirect-IA remains the source of truth for all agent media. ReaDirect does
not commit copies of these files. Development and production environments
expose `assets` through a static URL such as `/ia-assets`.

## Phase 2

Phase 2 uses the static images as fallbacks and these videos:

- Ciel: `c-idle.mp4`, `c-thinking-1.mp4`, `c-thinking-2.mp4`,
  `c-thinking-3.mp4`, `c-happy.mp4`, `c-confused.mp4`, `c-advise.mp4`,
  `c-clap.mp4`, and `c-congrats.mp4`
- Vivian: `v-idle.mp4`, `v-thinking-1.mp4`, `v-thinking-2.mp4`, and
  `v-congrats.mp4`
- Estelle: `e-idle.mp4`, `e-results-1.mp4`, `e-results-2.mp4`, and
  `e-congrats.mp4`

Idle videos loop. Interaction videos play once and return to idle. Congrats
videos are reserved for final-assessment completion flows.

The actual Vivian idle asset is `assets/videos/Vivian/v-idle.mp4`. Media files
must not be renamed or duplicated in ReaDirect.
