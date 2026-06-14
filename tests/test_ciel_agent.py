from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from pydantic import ValidationError

from ciel_agent.engine import CielTutorAgent
from ciel_agent.memory import JsonSessionMemory
from ciel_agent.schemas import CielAgentDecision, MemoryUpdate


class CielTutorAgentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        memory = JsonSessionMemory(Path(self.temporary.name) / "memory.json")
        self.agent = CielTutorAgent(memory)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def context(self, **values):
        return {
            "learner_id": 1,
            "session_id": "test-session",
            "module_type": "letter_reading",
            "expected": "B",
            "transcript": "D",
            "is_correct": False,
            "attempt": 1,
            "asr_confidence": 0.9,
            "error_type": None,
            "activity_id": 10,
            **values,
        }

    def test_correct_answer_uses_normal_praise(self):
        decision = self.agent.decide(
            self.context(is_correct=True, transcript="B")
        )
        self.assertEqual("correct_praise", decision.mode)
        self.assertIn(decision.animation, {"c-clap", "c-happy"})
        self.assertNotEqual("c-congrats", decision.animation)
        self.assertEqual("continue", decision.next_action)

    def test_final_assessment_completion_is_only_congrats_case(self):
        decision = self.agent.decide(
            self.context(is_final_assessment_completion=True)
        )
        self.assertEqual("final_assessment_completion", decision.mode)
        self.assertEqual("c-congrats", decision.animation)
        self.assertEqual("show_results", decision.next_action)

    def test_first_wrong_attempt_is_soft_retry(self):
        decision = self.agent.decide(self.context())
        self.assertEqual("soft_retry", decision.mode)
        self.assertEqual("retry", decision.next_action)
        self.assertIn(
            decision.animation,
            {"c-confused", "c-thinking-1", "c-thinking-2", "c-thinking-3"},
        )

    def test_second_wrong_attempt_enables_focus_mode(self):
        decision = self.agent.decide(self.context(attempt=2))
        self.assertEqual("focus_teach", decision.mode)
        self.assertEqual("listen_then_retry", decision.next_action)
        self.assertTrue(decision.lock_interaction)
        self.assertTrue(decision.repeat_after_agent)
        self.assertTrue(decision.focus_mode.enabled)
        self.assertEqual("blank_screen", decision.focus_mode.layout)
        self.assertEqual("center", decision.focus_mode.target_position)
        self.assertEqual("bottom", decision.focus_mode.agent_position)
        self.assertEqual("large", decision.focus_mode.target_size)

    def test_low_confidence_requests_new_recording(self):
        decision = self.agent.decide(self.context(asr_confidence=0.2))
        self.assertEqual("hint", decision.mode)
        self.assertEqual("retry_recording", decision.next_action)
        self.assertEqual("LOW_CONFIDENCE_AUDIO", decision.memory_update.error_key)

    def test_letter_confusion_bd_uses_comparison_message(self):
        decision = self.agent.decide(
            self.context(error_type="letter_confusion", attempt=2)
        )
        self.assertIn("B and D sound close", decision.message)
        self.assertEqual("B_D_CONFUSION", decision.memory_update.error_key)

    def test_vowel_confusion_focuses_middle_sound(self):
        decision = self.agent.decide(
            self.context(
                expected="LOG",
                transcript="LUG",
                error_type="vowel_confusion",
            )
        )
        self.assertIn("middle sound", decision.message)
        self.assertEqual("c-advise", decision.animation)

    def test_final_sound_missing_focuses_last_sound(self):
        decision = self.agent.decide(
            self.context(
                expected="CAT",
                transcript="CA",
                error_type="final_sound_missing",
            )
        )
        self.assertIn("last sound", decision.message)
        self.assertEqual("FINAL_SOUND_MISSING", decision.memory_update.error_key)

    def test_word_boundary_error_uses_slow_practice(self):
        decision = self.agent.decide(
            self.context(
                expected="THE CAT",
                transcript="THECAT",
                error_type="word_boundary_error",
            )
        )
        self.assertEqual("slow_practice", decision.mode)
        self.assertEqual("c-advise", decision.animation)
        self.assertIn("Read slowly", decision.message)

    def test_memory_count_increments(self):
        first = self.agent.decide(
            self.context(error_type="letter_confusion")
        )
        second = self.agent.decide(
            self.context(error_type="letter_confusion", attempt=2)
        )
        self.assertEqual(1, first.memory_update.current_count)
        self.assertEqual(2, second.memory_update.current_count)
        self.assertEqual(1, second.memory_update.count_increment)

    def test_animation_validation_rejects_invented_animation(self):
        with self.assertRaises(ValidationError):
            CielAgentDecision(
                mode="hint",
                animation="thinking",
                emotion="test",
                message="Try again.",
                next_action="retry",
                memory_update=MemoryUpdate(
                    learner_id="1",
                    session_id="s",
                ),
            )

    def test_congrats_validation_rejects_normal_correct_answer(self):
        with self.assertRaises(ValidationError):
            CielAgentDecision(
                mode="correct_praise",
                animation="c-congrats",
                emotion="test",
                message="Good job.",
                next_action="continue",
                memory_update=MemoryUpdate(
                    learner_id="1",
                    session_id="s",
                ),
            )


if __name__ == "__main__":
    unittest.main()
