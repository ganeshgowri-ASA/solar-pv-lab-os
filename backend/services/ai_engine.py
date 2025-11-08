"""
AI Engine - Core intelligence layer for Solar PV Lab Assistant
Combines Claude API with context management for intelligent assistance
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json

from .claude_service import get_claude_service, ClaudeService
from .context_manager import get_context_manager, ContextManager


class AIEngine:
    """Core AI engine for intelligent assistance"""

    def __init__(self):
        """Initialize AI engine"""
        self.claude_service: ClaudeService = get_claude_service()
        self.context_manager: ContextManager = get_context_manager()

    def chat(
        self,
        message: str,
        session_id: str,
        user_id: Optional[str] = None,
        include_context: bool = True
    ) -> Dict[str, Any]:
        """
        Handle chat message with context awareness

        Args:
            message: User message
            session_id: Session identifier
            user_id: User identifier
            include_context: Whether to include knowledge base context

        Returns:
            Response with message and metadata
        """
        try:
            # Get or create session
            session = self.context_manager.get_or_create_session(session_id, user_id)

            # Get relevant context if requested
            context_info = None
            enhanced_prompt = message

            if include_context:
                context_info = self.context_manager.get_relevant_context(
                    query=message,
                    session_id=session_id
                )

                # Enhance prompt with relevant knowledge
                if context_info.get("knowledge"):
                    enhanced_prompt = self._build_enhanced_prompt(message, context_info)

            # Get conversation history
            conversation_history = session.get_messages()

            # Call Claude
            response = self.claude_service.chat(
                message=enhanced_prompt,
                conversation_history=conversation_history,
                temperature=0.7
            )

            if response["success"]:
                # Add to conversation history
                session.add_message("user", message)
                session.add_message("assistant", response["message"])

                return {
                    "success": True,
                    "message": response["message"],
                    "session_id": session_id,
                    "context_used": context_info is not None,
                    "usage": response["usage"],
                    "timestamp": response["timestamp"]
                }
            else:
                return response

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def analyze_test_data(
        self,
        data: Dict[str, Any],
        test_type: str,
        analysis_type: str = "comprehensive",
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze test data with AI intelligence

        Args:
            data: Test data to analyze
            test_type: Type of test (iv_curve, thermal_cycling, etc.)
            analysis_type: Type of analysis (anomaly, trend, prediction, comprehensive)
            session_id: Optional session for context

        Returns:
            Analysis results
        """
        try:
            # Build context
            context = f"Test Type: {test_type}\nAnalysis: {analysis_type}"

            # Add session context if available
            if session_id:
                session = self.context_manager.get_session(session_id)
                if session:
                    context += f"\nPrevious Context: {session.get_metadata('last_analysis', 'None')}"

            # Perform analysis
            response = self.claude_service.analyze_data(
                data=data,
                analysis_type=analysis_type,
                context=context
            )

            # Store analysis in session if provided
            if session_id and response["success"]:
                session = self.context_manager.get_or_create_session(session_id)
                session.set_metadata("last_analysis", {
                    "test_type": test_type,
                    "timestamp": datetime.utcnow().isoformat()
                })

            return response

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def review_test_report(
        self,
        report_data: Dict[str, Any],
        standards: Optional[List[str]] = None,
        check_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Review test report for quality and compliance

        Args:
            report_data: Report to review
            standards: Applicable standards
            check_types: Specific checks to perform

        Returns:
            Review results with issues and suggestions
        """
        try:
            # Get standard information from knowledge base
            if standards:
                for standard in standards:
                    std_info = self.context_manager.get_knowledge("standards", standard.lower().replace(" ", "_"))
                    if std_info:
                        report_data["_standard_requirements"] = std_info

            # Perform review
            response = self.claude_service.review_report(
                report_data=report_data,
                standards=standards
            )

            # Parse review results and structure them
            if response["success"]:
                # Add structured results
                response["structured_review"] = self._parse_review_results(response["review"])

            return response

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def get_troubleshooting_help(
        self,
        issue_description: str,
        equipment: Optional[str] = None,
        test_type: Optional[str] = None,
        error_data: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get AI-powered troubleshooting guidance

        Args:
            issue_description: Description of the problem
            equipment: Equipment involved
            test_type: Type of test
            error_data: Error messages or data
            session_id: Session for context

        Returns:
            Troubleshooting guidance
        """
        try:
            # Get equipment info from knowledge base
            equipment_info = None
            if equipment:
                equipment_info = self.context_manager.get_knowledge(
                    "equipment",
                    equipment.lower().replace(" ", "_")
                )

            # Get test procedure info
            procedure_info = None
            if test_type:
                procedure_info = self.context_manager.get_knowledge(
                    "test_procedures",
                    test_type.lower().replace(" ", "_")
                )

            # Add context to error data
            if equipment_info or procedure_info:
                if error_data is None:
                    error_data = {}
                error_data["_equipment_info"] = equipment_info
                error_data["_procedure_info"] = procedure_info

            # Get troubleshooting guidance
            response = self.claude_service.get_troubleshooting_help(
                issue_description=issue_description,
                equipment=equipment,
                test_type=test_type,
                error_data=error_data
            )

            # Save troubleshooting session
            if session_id and response["success"]:
                session = self.context_manager.get_or_create_session(session_id)
                session.add_message("user", f"Troubleshooting: {issue_description}")
                session.add_message("assistant", response["guidance"])

            return response

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def get_decision_support(
        self,
        decision_context: str,
        options: List[Dict[str, Any]],
        criteria: Optional[List[str]] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get AI-powered decision support

        Args:
            decision_context: Context of decision
            options: Available options
            criteria: Decision criteria
            session_id: Session for context

        Returns:
            Decision recommendation
        """
        try:
            # Get relevant best practices
            best_practices = self.context_manager.get_knowledge("best_practices")

            # Add best practices to decision context if relevant
            if best_practices:
                decision_context += f"\n\nRelevant Best Practices:\n{json.dumps(best_practices, indent=2)}"

            # Get decision support
            response = self.claude_service.get_decision_support(
                decision_context=decision_context,
                options=options,
                criteria=criteria
            )

            # Save decision session
            if session_id and response["success"]:
                session = self.context_manager.get_or_create_session(session_id)
                session.add_message("user", f"Decision: {decision_context}")
                session.add_message("assistant", response["recommendation"])

            return response

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def get_insights(
        self,
        data_scope: str = "recent",
        insight_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get automated insights from system data

        Args:
            data_scope: Scope of data to analyze (recent, all, specific_date)
            insight_types: Types of insights (trends, anomalies, predictions, recommendations)

        Returns:
            Insights and recommendations
        """
        try:
            # This would typically integrate with actual data sources
            # For now, return a structured response
            insights = {
                "success": True,
                "scope": data_scope,
                "insights": [],
                "timestamp": datetime.utcnow().isoformat()
            }

            # Placeholder for actual data analysis
            # In production, this would query databases and analyze real data

            return insights

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def detect_intent(self, message: str) -> Dict[str, Any]:
        """
        Detect user intent from message

        Args:
            message: User message

        Returns:
            Detected intent and confidence
        """
        message_lower = message.lower()

        # Simple rule-based intent detection (can be enhanced with ML)
        intents = {
            "analyze_data": ["analyze", "analysis", "check data", "review data", "examine"],
            "troubleshoot": ["error", "problem", "issue", "help", "troubleshoot", "not working"],
            "question": ["what", "how", "why", "when", "where", "explain", "tell me"],
            "review_report": ["review report", "check report", "validate report"],
            "decision_support": ["should i", "recommend", "suggest", "which option", "decide"],
            "chat": []  # default
        }

        detected_intent = "chat"
        confidence = 0.0

        for intent, keywords in intents.items():
            matches = sum(1 for keyword in keywords if keyword in message_lower)
            if matches > 0:
                current_confidence = matches / max(len(keywords), 1)
                if current_confidence > confidence:
                    confidence = current_confidence
                    detected_intent = intent

        return {
            "intent": detected_intent,
            "confidence": confidence,
            "message": message
        }

    def _build_enhanced_prompt(
        self,
        message: str,
        context_info: Dict[str, Any]
    ) -> str:
        """Build enhanced prompt with context"""
        enhanced = message

        if context_info.get("knowledge"):
            enhanced += "\n\n[Relevant Context]:\n"
            for category, items in context_info["knowledge"].items():
                enhanced += f"\n{category.upper()}:\n"
                for key, value in items.items():
                    enhanced += f"- {key}: {value.get('content', value)}\n"

        return enhanced

    def _parse_review_results(self, review_text: str) -> Dict[str, Any]:
        """Parse review results into structured format"""
        # Simple parsing - can be enhanced
        return {
            "raw_review": review_text,
            "has_issues": any(word in review_text.lower() for word in ["error", "missing", "issue", "problem", "incorrect"]),
            "completeness_score": self._estimate_completeness(review_text),
            "timestamp": datetime.utcnow().isoformat()
        }

    def _estimate_completeness(self, review_text: str) -> float:
        """Estimate completeness score from review text"""
        # Simple heuristic - can be enhanced
        positive_words = ["complete", "adequate", "sufficient", "good", "correct"]
        negative_words = ["missing", "incomplete", "insufficient", "error", "incorrect"]

        positive_count = sum(1 for word in positive_words if word in review_text.lower())
        negative_count = sum(1 for word in negative_words if word in review_text.lower())

        total = positive_count + negative_count
        if total == 0:
            return 0.5

        return positive_count / total


# Singleton instance
_ai_engine_instance = None


def get_ai_engine() -> AIEngine:
    """Get singleton instance of AI engine"""
    global _ai_engine_instance
    if _ai_engine_instance is None:
        _ai_engine_instance = AIEngine()
    return _ai_engine_instance
