"""
AI Chat Interface - Streamlit component for conversational AI assistant
Provides interactive chat with context awareness and multi-turn conversations
"""

import streamlit as st
import requests
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid


class AIChatInterface:
    """AI Chat Interface for Streamlit"""

    def __init__(self, api_base_url: str = "http://localhost:8000"):
        """
        Initialize chat interface

        Args:
            api_base_url: Base URL for AI Assistant API
        """
        self.api_base_url = api_base_url
        self.chat_endpoint = f"{api_base_url}/api/v1/ai/chat"
        self.intent_endpoint = f"{api_base_url}/api/v1/ai/intent"

    def render(self):
        """Render the chat interface"""
        st.title("🤖 AI Assistant")
        st.markdown("*Your intelligent companion for Solar PV Lab operations*")

        # Initialize session state
        self._init_session_state()

        # Sidebar configuration
        self._render_sidebar()

        # Chat history
        self._render_chat_history()

        # Input area
        self._render_input_area()

        # Quick actions
        self._render_quick_actions()

    def _init_session_state(self):
        """Initialize session state variables"""
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []

        if "session_id" not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())

        if "user_id" not in st.session_state:
            st.session_state.user_id = "streamlit_user"

        if "include_context" not in st.session_state:
            st.session_state.include_context = True

        if "total_tokens" not in st.session_state:
            st.session_state.total_tokens = {"input": 0, "output": 0}

    def _render_sidebar(self):
        """Render sidebar with settings and info"""
        with st.sidebar:
            st.header("Chat Settings")

            # Context setting
            st.session_state.include_context = st.checkbox(
                "Include Knowledge Base",
                value=st.session_state.include_context,
                help="Include relevant knowledge from standards, procedures, and best practices"
            )

            # Session info
            st.divider()
            st.subheader("Session Info")
            st.text(f"Session ID: {st.session_state.session_id[:8]}...")
            st.text(f"Messages: {len(st.session_state.chat_messages)}")

            # Token usage
            if st.session_state.total_tokens["input"] > 0:
                st.text(f"Input Tokens: {st.session_state.total_tokens['input']}")
                st.text(f"Output Tokens: {st.session_state.total_tokens['output']}")

            # Reset button
            if st.button("🔄 New Session", use_container_width=True):
                st.session_state.chat_messages = []
                st.session_state.session_id = str(uuid.uuid4())
                st.session_state.total_tokens = {"input": 0, "output": 0}
                st.rerun()

            # Export chat
            if st.session_state.chat_messages:
                if st.button("💾 Export Chat", use_container_width=True):
                    self._export_chat()

    def _render_chat_history(self):
        """Render chat message history"""
        # Container for messages
        chat_container = st.container()

        with chat_container:
            if not st.session_state.chat_messages:
                st.info("👋 Welcome! Ask me anything about PV testing, standards, troubleshooting, or data analysis.")
            else:
                for message in st.session_state.chat_messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
                        if "timestamp" in message:
                            st.caption(f"_{message['timestamp']}_")

    def _render_input_area(self):
        """Render message input area"""
        # Chat input
        user_input = st.chat_input("Ask me anything about PV testing...")

        if user_input:
            self._handle_user_message(user_input)

    def _render_quick_actions(self):
        """Render quick action buttons"""
        st.divider()
        st.subheader("Quick Actions")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📊 Analyze Data", use_container_width=True):
                self._quick_action("How do I analyze my test data?")

        with col2:
            if st.button("🔧 Troubleshoot", use_container_width=True):
                self._quick_action("I'm having an issue with my test equipment.")

        with col3:
            if st.button("📋 Review Report", use_container_width=True):
                self._quick_action("Can you review my test report?")

        col4, col5, col6 = st.columns(3)

        with col4:
            if st.button("📖 Standards Help", use_container_width=True):
                self._quick_action("What are the key requirements for IEC 61215?")

        with col5:
            if st.button("🎯 Best Practices", use_container_width=True):
                self._quick_action("What are best practices for data quality?")

        with col6:
            if st.button("💡 Recommendations", use_container_width=True):
                self._quick_action("What equipment do you recommend for IV curve testing?")

    def _handle_user_message(self, message: str):
        """
        Handle user message

        Args:
            message: User message text
        """
        # Add user message to chat
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.chat_messages.append({
            "role": "user",
            "content": message,
            "timestamp": timestamp
        })

        # Display user message
        with st.chat_message("user"):
            st.markdown(message)
            st.caption(f"_{timestamp}_")

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = self._call_chat_api(message)

                if response and response.get("success"):
                    assistant_message = response["message"]
                    st.markdown(assistant_message)

                    # Update token usage
                    if "usage" in response:
                        st.session_state.total_tokens["input"] += response["usage"].get("input_tokens", 0)
                        st.session_state.total_tokens["output"] += response["usage"].get("output_tokens", 0)

                    # Show if context was used
                    if response.get("context_used"):
                        st.caption("_✓ Knowledge base consulted_")

                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.caption(f"_{timestamp}_")

                    # Add to chat history
                    st.session_state.chat_messages.append({
                        "role": "assistant",
                        "content": assistant_message,
                        "timestamp": timestamp
                    })
                else:
                    error_msg = response.get("error", "Failed to get response") if response else "API connection error"
                    st.error(f"Error: {error_msg}")

    def _call_chat_api(self, message: str) -> Optional[Dict[str, Any]]:
        """
        Call chat API

        Args:
            message: User message

        Returns:
            API response or None
        """
        try:
            payload = {
                "message": message,
                "session_id": st.session_state.session_id,
                "user_id": st.session_state.user_id,
                "include_context": st.session_state.include_context
            }

            response = requests.post(
                self.chat_endpoint,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "success": False,
                    "error": f"API returned status {response.status_code}"
                }

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Connection error: {str(e)}"
            }

    def _quick_action(self, message: str):
        """Handle quick action button"""
        self._handle_user_message(message)
        st.rerun()

    def _export_chat(self):
        """Export chat history"""
        chat_data = {
            "session_id": st.session_state.session_id,
            "user_id": st.session_state.user_id,
            "messages": st.session_state.chat_messages,
            "exported_at": datetime.now().isoformat()
        }

        # Convert to JSON
        json_str = json.dumps(chat_data, indent=2)

        # Download button
        st.download_button(
            label="Download Chat History",
            data=json_str,
            file_name=f"chat_history_{st.session_state.session_id[:8]}.json",
            mime="application/json"
        )


def render_standalone():
    """Render as standalone Streamlit app"""
    st.set_page_config(
        page_title="AI Assistant - Solar PV Lab",
        page_icon="🤖",
        layout="wide"
    )

    # Custom CSS
    st.markdown("""
        <style>
        .stChatMessage {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }
        .stChatInput {
            border-radius: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

    chat_interface = AIChatInterface()
    chat_interface.render()


if __name__ == "__main__":
    render_standalone()
