from abc import ABC, abstractmethod
from typing import List
from core.models import ConversationEntry


class MemoryStore(ABC):
    @abstractmethod
    def save(self, session_id: str, entry: ConversationEntry) -> None:
        pass

    @abstractmethod
    def load(self, session_id: str) -> List[ConversationEntry]:
        pass

    @abstractmethod
    def clear(self, session_id: str) -> None:
        pass


class InMemoryStore(MemoryStore):
    def __init__(self):
        self._sessions = {}

    def save(self, session_id: str, entry: ConversationEntry) -> None:
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        self._sessions[session_id].append(entry)

    def load(self, session_id: str) -> List[ConversationEntry]:
        return self._sessions.get(session_id, [])

    def clear(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)