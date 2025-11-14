"""
Context Manager - Manages conversation context and RAG for AI Assistant
Provides context-aware responses and knowledge retrieval
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
import json
from collections import defaultdict
import hashlib


class ConversationContext:
    """Manages context for a single conversation session"""

    def __init__(self, session_id: str, user_id: Optional[str] = None):
        """
        Initialize conversation context

        Args:
            session_id: Unique session identifier
            user_id: User identifier (optional)
        """
        self.session_id = session_id
        self.user_id = user_id
        self.messages: List[Dict[str, str]] = []
        self.metadata: Dict[str, Any] = {}
        self.created_at = datetime.utcnow()
        self.last_updated = datetime.utcnow()
        self.context_window = 10  # Number of messages to keep in context

    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to the conversation

        Args:
            role: 'user' or 'assistant'
            content: Message content
        """
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.last_updated = datetime.utcnow()

    def get_messages(self, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Get conversation messages

        Args:
            limit: Maximum number of messages to return (default: context_window)

        Returns:
            List of messages for API consumption
        """
        if limit is None:
            limit = self.context_window

        # Return only role and content for API
        recent_messages = self.messages[-limit:] if limit > 0 else self.messages
        return [{"role": msg["role"], "content": msg["content"]} for msg in recent_messages]

    def get_full_history(self) -> List[Dict[str, Any]]:
        """Get complete conversation history with timestamps"""
        return self.messages.copy()

    def set_metadata(self, key: str, value: Any) -> None:
        """Set metadata for the conversation"""
        self.metadata[key] = value
        self.last_updated = datetime.utcnow()

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value"""
        return self.metadata.get(key, default)

    def clear_messages(self) -> None:
        """Clear conversation history"""
        self.messages.clear()
        self.last_updated = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary"""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "messages": self.messages,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat()
        }


class ContextManager:
    """Manages multiple conversation contexts and provides knowledge retrieval"""

    def __init__(self):
        """Initialize context manager"""
        self.sessions: Dict[str, ConversationContext] = {}
        self.knowledge_base: Dict[str, Any] = self._initialize_knowledge_base()
        self.session_timeout = 3600  # 1 hour in seconds

    def create_session(
        self,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> ConversationContext:
        """
        Create a new conversation session

        Args:
            session_id: Session ID (auto-generated if not provided)
            user_id: User ID

        Returns:
            New conversation context
        """
        if session_id is None:
            session_id = self._generate_session_id(user_id)

        context = ConversationContext(session_id, user_id)
        self.sessions[session_id] = context
        return context

    def get_session(self, session_id: str) -> Optional[ConversationContext]:
        """
        Get existing conversation session

        Args:
            session_id: Session identifier

        Returns:
            Conversation context or None if not found
        """
        return self.sessions.get(session_id)

    def get_or_create_session(
        self,
        session_id: str,
        user_id: Optional[str] = None
    ) -> ConversationContext:
        """
        Get existing session or create new one

        Args:
            session_id: Session identifier
            user_id: User identifier

        Returns:
            Conversation context
        """
        session = self.get_session(session_id)
        if session is None:
            session = self.create_session(session_id, user_id)
        return session

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a conversation session

        Args:
            session_id: Session identifier

        Returns:
            True if deleted, False if not found
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    def cleanup_old_sessions(self) -> int:
        """
        Remove expired sessions

        Returns:
            Number of sessions removed
        """
        current_time = datetime.utcnow()
        expired_sessions = []

        for session_id, context in self.sessions.items():
            age = (current_time - context.last_updated).total_seconds()
            if age > self.session_timeout:
                expired_sessions.append(session_id)

        for session_id in expired_sessions:
            del self.sessions[session_id]

        return len(expired_sessions)

    def get_relevant_context(
        self,
        query: str,
        session_id: Optional[str] = None,
        context_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get relevant context for a query (RAG - Retrieval Augmented Generation)

        Args:
            query: User query
            session_id: Session ID for conversation history
            context_types: Types of context to retrieve (standards, procedures, equipment, etc.)

        Returns:
            Relevant context information
        """
        context = {
            "conversation_history": [],
            "knowledge": {},
            "query": query
        }

        # Get conversation history if session exists
        if session_id:
            session = self.get_session(session_id)
            if session:
                context["conversation_history"] = session.get_messages(limit=5)

        # Retrieve relevant knowledge based on query
        if context_types is None:
            context_types = ["standards", "procedures", "equipment", "best_practices"]

        for context_type in context_types:
            relevant_info = self._retrieve_knowledge(query, context_type)
            if relevant_info:
                context["knowledge"][context_type] = relevant_info

        return context

    def add_knowledge(
        self,
        category: str,
        key: str,
        content: Any
    ) -> None:
        """
        Add information to knowledge base

        Args:
            category: Knowledge category
            key: Unique identifier
            content: Knowledge content
        """
        if category not in self.knowledge_base:
            self.knowledge_base[category] = {}

        self.knowledge_base[category][key] = {
            "content": content,
            "added_at": datetime.utcnow().isoformat()
        }

    def get_knowledge(
        self,
        category: str,
        key: Optional[str] = None
    ) -> Optional[Any]:
        """
        Retrieve knowledge from knowledge base

        Args:
            category: Knowledge category
            key: Specific item key (optional)

        Returns:
            Knowledge content or None
        """
        if category not in self.knowledge_base:
            return None

        if key is None:
            return self.knowledge_base[category]

        return self.knowledge_base[category].get(key)

    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """Initialize knowledge base with core PV testing information"""
        return {
            "standards": {
                "iec_61215": {
                    "content": "IEC 61215 - Design qualification and type approval for crystalline silicon PV modules",
                    "tests": ["Visual inspection", "Performance at STC", "Insulation test", "Temperature coefficients", "NOCT", "Low irradiance", "Outdoor exposure", "Hot-spot endurance", "UV preconditioning", "Thermal cycling", "Humidity freeze", "Damp heat", "Robustness of terminations", "Wet leakage current", "Mechanical load", "Hail test", "Bypass diode"]
                },
                "iec_61730": {
                    "content": "IEC 61730 - PV module safety qualification",
                    "tests": ["Construction", "Accessible parts", "Insulation", "Fire resistance", "Mechanical stress", "Environmental stress"]
                },
                "ul_1703": {
                    "content": "UL 1703 - Flat-Plate Photovoltaic Modules and Panels",
                    "tests": ["Electrical", "Fire", "Mechanical", "Environmental"]
                }
            },
            "test_procedures": {
                "iv_curve": {
                    "content": "I-V Curve measurement procedure",
                    "steps": ["Set up test conditions", "Connect module", "Stabilize temperature", "Perform measurement", "Validate data", "Calculate parameters"]
                },
                "insulation_test": {
                    "content": "Insulation resistance test",
                    "voltage": "1000V DC",
                    "duration": "60 seconds",
                    "pass_criteria": ">40 MΩ for modules <50kW"
                },
                "thermal_cycling": {
                    "content": "Thermal cycling test (TC200)",
                    "cycles": 200,
                    "temperature_range": "-40°C to +85°C",
                    "pass_criteria": "Pmax degradation <5%"
                }
            },
            "equipment": {
                "solar_simulator": {
                    "content": "Solar simulator for STC testing",
                    "requirements": ["Class AAA", "1000 W/m²", "AM1.5G spectrum", "25°C cell temperature"]
                },
                "thermal_chamber": {
                    "content": "Environmental chamber for thermal testing",
                    "requirements": ["Temperature range: -40°C to +85°C", "Humidity control", "Programmable cycles"]
                }
            },
            "best_practices": {
                "data_quality": {
                    "content": "Best practices for data quality",
                    "guidelines": ["Regular calibration", "Duplicate measurements", "Statistical analysis", "Document uncertainties", "Validate anomalies"]
                },
                "safety": {
                    "content": "Laboratory safety guidelines",
                    "guidelines": ["PPE requirements", "Electrical safety", "Chemical handling", "Emergency procedures"]
                }
            }
        }

    def _retrieve_knowledge(
        self,
        query: str,
        category: str
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve relevant knowledge for a query

        Args:
            query: User query
            category: Knowledge category

        Returns:
            Relevant knowledge items
        """
        if category not in self.knowledge_base:
            return None

        # Simple keyword-based retrieval (can be enhanced with embeddings/semantic search)
        query_lower = query.lower()
        relevant_items = {}

        for key, value in self.knowledge_base[category].items():
            # Check if key or content contains query terms
            if (key.lower() in query_lower or
                query_lower in key.lower() or
                self._content_matches_query(value.get("content", ""), query_lower)):
                relevant_items[key] = value

        return relevant_items if relevant_items else None

    def _content_matches_query(self, content: Any, query: str) -> bool:
        """Check if content matches query"""
        if isinstance(content, str):
            return query in content.lower()
        elif isinstance(content, dict):
            return any(query in str(v).lower() for v in content.values())
        elif isinstance(content, list):
            return any(query in str(item).lower() for item in content)
        return False

    def _generate_session_id(self, user_id: Optional[str] = None) -> str:
        """Generate unique session ID"""
        timestamp = datetime.utcnow().isoformat()
        data = f"{user_id or 'anonymous'}_{timestamp}".encode()
        return hashlib.md5(data).hexdigest()

    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics about active sessions"""
        return {
            "total_sessions": len(self.sessions),
            "sessions_by_user": defaultdict(int, {
                session.user_id: sum(1 for s in self.sessions.values() if s.user_id == session.user_id)
                for session in self.sessions.values() if session.user_id
            }),
            "oldest_session": min(
                (s.created_at for s in self.sessions.values()),
                default=None
            ),
            "newest_session": max(
                (s.created_at for s in self.sessions.values()),
                default=None
            )
        }


# Singleton instance
_context_manager_instance = None


def get_context_manager() -> ContextManager:
    """Get singleton instance of context manager"""
    global _context_manager_instance
    if _context_manager_instance is None:
        _context_manager_instance = ContextManager()
    return _context_manager_instance
