from __future__ import annotations

import unittest
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

import main
from ciel_agent.engine import CielTutorAgent
from ciel_agent.memory import JsonSessionMemory


class CielAgentApiTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        main.engine = CielTutorAgent(
            JsonSessionMemory(Path(self.temporary.name) / "memory.json")
        )
        self.client = TestClient(main.app)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_status_exposes_exact_modes_and_animations(self):
        response = self.client.get("/ia/ciel/status")
        self.assertEqual(200, response.status_code)
        payload = response.json()
        self.assertTrue(payload["engine_loaded"])
        self.assertFalse(payload["llm_enabled"])
        self.assertIn("focus_teach", payload["available_modes"])
        self.assertEqual(
            {
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
            },
            set(payload["available_animations"]),
        )

    def test_decide_returns_ciel_agent_wrapper(self):
        response = self.client.post(
            "/ia/ciel/decide",
            json={
                "learner_id": 1,
                "session_id": "api-unit-test",
                "module_type": "letter_reading",
                "expected": "B",
                "transcript": "D",
                "is_correct": False,
                "attempt": 2,
                "asr_confidence": 0.72,
                "error_type": "letter_confusion",
            },
        )
        self.assertEqual(200, response.status_code)
        decision = response.json()["ciel_agent"]
        self.assertEqual("focus_teach", decision["mode"])
        self.assertEqual("c-advise", decision["animation"])
        self.assertFalse(decision["official_progression_changed"])


if __name__ == "__main__":
    unittest.main()
