from __future__ import annotations

import json
import os
from pathlib import Path
from threading import RLock
from typing import Protocol

from .schemas import MemoryUpdate


class SessionMemory(Protocol):
    backend_name: str

    def increment(
        self,
        learner_id: int | str,
        session_id: str,
        error_key: str | None,
    ) -> MemoryUpdate: ...


class JsonSessionMemory:
    backend_name = "json_file"

    def __init__(self, path: str | Path | None = None) -> None:
        default_path = Path(__file__).resolve().parents[1] / "data/ciel_memory.json"
        self.path = Path(path or os.getenv("CIEL_MEMORY_PATH", default_path))
        self._lock = RLock()

    def increment(
        self,
        learner_id: int | str,
        session_id: str,
        error_key: str | None,
    ) -> MemoryUpdate:
        learner = str(learner_id)
        session = str(session_id)
        if error_key is None:
            return MemoryUpdate(
                learner_id=learner,
                session_id=session,
                error_key=None,
                count_increment=0,
                current_count=0,
            )

        with self._lock:
            data = self._read()
            learner_data = data.setdefault("learners", {}).setdefault(learner, {})
            session_data = learner_data.setdefault(session, {"errors": {}})
            errors = session_data.setdefault("errors", {})
            errors[error_key] = int(errors.get(error_key, 0)) + 1
            self._write(data)
            current_count = errors[error_key]

        return MemoryUpdate(
            learner_id=learner,
            session_id=session,
            error_key=error_key,
            count_increment=1,
            current_count=current_count,
        )

    def _read(self) -> dict:
        if not self.path.exists():
            return {"version": 1, "learners": {}}
        try:
            value = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {"version": 1, "learners": {}}
        return value if isinstance(value, dict) else {"version": 1, "learners": {}}

    def _write(self, data: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        temporary.replace(self.path)
