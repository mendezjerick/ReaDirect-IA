from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ciel_agent.engine import CielTutorAgent
from ciel_agent.memory import JsonSessionMemory


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        agent = CielTutorAgent(JsonSessionMemory(Path(directory) / "memory.json"))
        examples = [
            {
                "learner_id": 1,
                "session_id": "example-correct",
                "module_type": "letter_reading",
                "expected": "B",
                "transcript": "B",
                "is_correct": True,
                "attempt": 1,
            },
            {
                "learner_id": 1,
                "session_id": "example-focus",
                "module_type": "letter_reading",
                "expected": "B",
                "transcript": "D",
                "is_correct": False,
                "attempt": 2,
                "asr_confidence": 0.72,
                "gop_score": 0.41,
                "phoneme_errors": [],
                "error_type": "letter_confusion",
                "activity_id": 10,
                "is_final_assessment_completion": False,
            },
        ]
        for example in examples:
            print(json.dumps({"ciel_agent": agent.decide(example).model_dump()}, indent=2))


if __name__ == "__main__":
    main()
