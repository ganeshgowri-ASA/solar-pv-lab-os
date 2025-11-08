"""
Tests for AI Engine
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.ai_engine import AIEngine


class TestAIEngine:
    """Test AI Engine functionality"""

    def test_detect_intent_analyze(self):
        """Test intent detection for data analysis"""
        engine = AIEngine()
        result = engine.detect_intent("Can you analyze my test data?")

        assert result["intent"] == "analyze_data"
        assert result["confidence"] > 0

    def test_detect_intent_troubleshoot(self):
        """Test intent detection for troubleshooting"""
        engine = AIEngine()
        result = engine.detect_intent("I have an error with my equipment")

        assert result["intent"] == "troubleshoot"
        assert result["confidence"] > 0

    def test_detect_intent_question(self):
        """Test intent detection for questions"""
        engine = AIEngine()
        result = engine.detect_intent("What is IEC 61215?")

        assert result["intent"] == "question"
        assert result["confidence"] > 0

    def test_detect_intent_review(self):
        """Test intent detection for report review"""
        engine = AIEngine()
        result = engine.detect_intent("Can you review my test report?")

        assert result["intent"] == "review_report"
        assert result["confidence"] > 0

    def test_detect_intent_decision(self):
        """Test intent detection for decision support"""
        engine = AIEngine()
        result = engine.detect_intent("Which equipment should I choose?")

        assert result["intent"] == "decision_support"
        assert result["confidence"] > 0

    def test_estimate_completeness(self):
        """Test completeness score estimation"""
        engine = AIEngine()

        # Positive review
        score = engine._estimate_completeness("Report is complete and adequate")
        assert score > 0.5

        # Negative review
        score = engine._estimate_completeness("Report is missing critical data")
        assert score < 0.5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
