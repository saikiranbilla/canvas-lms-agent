"""
Keywords AI Utilities for Canvas LMS Agent

This module provides utilities for integrating Keywords AI features:
- Prompt Management
- Logging API
- Evaluations/Scoring
"""

import os
import requests
from typing import Optional, Dict, Any, List
from datetime import datetime


class KeywordsAIClient:
    """Client for Keywords AI API operations."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("KEYWORDSAI_API_KEY")
        self.base_url = os.getenv("KEYWORDSAI_BASE_URL", "https://api.keywordsai.co/api")

        if not self.api_key:
            raise ValueError("KEYWORDSAI_API_KEY is required")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Keywords-Cache-TTL": "3600", # Enable semantic caching for 1 hour
            "X-Keywords-Source": "CanvasAI-PromptClient"
        }

    # ========== PROMPT MANAGEMENT ==========

    def chat_with_prompt(
        self,
        prompt_id: str,
        variables: Dict[str, str] = None,
        user_message: str = None,
        override: bool = True
    ) -> Dict[str, Any]:
        """
        Make a chat completion using a managed prompt from Keywords AI.

        Args:
            prompt_id: The ID of the prompt template (from Keywords AI dashboard)
            variables: Dictionary of variable values to fill in the prompt template
            user_message: Optional additional user message
            override: If True, use prompt config instead of SDK parameters

        Returns:
            The chat completion response

        Example:
            client = KeywordsAIClient()
            response = client.chat_with_prompt(
                prompt_id="042f5f",
                variables={
                    "task_description": "create a quiz",
                    "course_name": "Psychology 101"
                }
            )
            print(response["choices"][0]["message"]["content"])
        """
        data = {
            "model": "gpt-4o-mini",  # Will be overridden by prompt config
            "messages": [{"role": "user", "content": user_message or "placeholder"}],
            "prompt": {
                "prompt_id": prompt_id,
                "variables": variables or {},
                "override": override
            }
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self._headers(),
            json=data
        )
        response.raise_for_status()
        return response.json()

    # ========== LOGGING API ==========

    def log_request(
        self,
        input_messages: List[Dict[str, str]],
        output_message: Dict[str, str],
        model: str = "gpt-4o-mini",
        customer_identifier: str = None,
        thread_identifier: str = None,
        metadata: Dict[str, Any] = None,
        latency: float = None,
        usage: Dict[str, int] = None,
        status: str = "success",
        log_type: str = "chat"
    ) -> Dict[str, Any]:
        """
        Log an LLM request to Keywords AI for observability.

        This is useful for logging requests that bypass the gateway
        or for adding additional context to existing logs.

        Args:
            input_messages: List of input messages [{"role": "user", "content": "..."}]
            output_message: The output message {"role": "assistant", "content": "..."}
            model: The model used
            customer_identifier: User identifier for analytics
            thread_identifier: Conversation thread ID
            metadata: Custom metadata
            latency: Request latency in seconds
            usage: Token usage {"prompt_tokens": X, "completion_tokens": Y, "total_tokens": Z}
            status: "success" or "error"
            log_type: Type of log ("chat", "workflow", "task", etc.)

        Returns:
            The API response

        Example:
            client = KeywordsAIClient()
            client.log_request(
                input_messages=[{"role": "user", "content": "Hello"}],
                output_message={"role": "assistant", "content": "Hi there!"},
                customer_identifier="user_123",
                thread_identifier="thread_456",
                metadata={"feature": "chat"}
            )
        """
        import json

        payload = {
            "input": json.dumps(input_messages),
            "output": json.dumps(output_message),
            "model": model,
            "log_type": log_type,
            "status": status,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        if customer_identifier:
            payload["customer_identifier"] = customer_identifier
        if thread_identifier:
            payload["thread_identifier"] = thread_identifier
        if metadata:
            payload["metadata"] = metadata
        if latency:
            payload["latency"] = latency
        if usage:
            payload["usage"] = usage

        response = requests.post(
            f"{self.base_url.replace('/api/', '/api/')}/request-logs/create/",
            headers=self._headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()

    # ========== EVALUATIONS / SCORING ==========

    def submit_feedback(
        self,
        log_id: str,
        positive_feedback: bool,
        score: float = None,
        comment: str = None
    ) -> Dict[str, Any]:
        """
        Submit feedback/evaluation for a logged request.

        Args:
            log_id: The ID of the log to provide feedback for
            positive_feedback: True for positive, False for negative
            score: Optional numeric score (0.0 to 1.0)
            comment: Optional feedback comment

        Returns:
            The API response
        """
        payload = {
            "positive_feedback": positive_feedback
        }
        if score is not None:
            payload["score"] = score
        if comment:
            payload["metadata"] = {"feedback_comment": comment}

        response = requests.patch(
            f"https://api.keywordsai.co/api/request-logs/{log_id}/",
            headers=self._headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()

    def log_with_score(
        self,
        input_messages: List[Dict[str, str]],
        output_message: Dict[str, str],
        score: float,
        score_name: str = "quality",
        model: str = "gpt-4o-mini",
        customer_identifier: str = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Log a request with an evaluation score.

        Useful for logging evaluated outputs (e.g., after human review
        or automated evaluation).

        Args:
            input_messages: Input messages
            output_message: Output message
            score: Score value (0.0 to 1.0)
            score_name: Name of the score metric
            model: Model used
            customer_identifier: User identifier
            metadata: Additional metadata

        Returns:
            The API response
        """
        import json

        combined_metadata = metadata or {}
        combined_metadata[f"score_{score_name}"] = score

        payload = {
            "input": json.dumps(input_messages),
            "output": json.dumps(output_message),
            "model": model,
            "log_type": "chat",
            "metadata": combined_metadata,
            "positive_feedback": score >= 0.5  # Consider >= 0.5 as positive
        }

        if customer_identifier:
            payload["customer_identifier"] = customer_identifier

        response = requests.post(
            "https://api.keywordsai.co/api/request-logs/create/",
            headers=self._headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


    def log_custom_event(
        self,
        event_name: str,
        customer_identifier: str = None,
        thread_identifier: str = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Log a custom business event (e.g., "assignment_created").
        """
        import json
        
        payload = {
            "log_type": "custom_event",
            "model": "custom-event-model", # Placeholder
            "status": "success",
            "input": json.dumps([{"role": "system", "content": event_name}]),
            "output": json.dumps({"role": "assistant", "content": "Event recorded"}),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "metadata": metadata or {}
        }
        
        if customer_identifier:
            payload["customer_identifier"] = customer_identifier
        if thread_identifier:
            payload["thread_identifier"] = thread_identifier
            
        # Add event name to metadata for easier filtering
        payload["metadata"]["event_name"] = event_name

        try:
            response = requests.post(
                f"{self.base_url.replace('/api/', '/api/')}/request-logs/create/",
                headers=self._headers(),
                json=payload,
                timeout=2 # Short timeout to not block
            )
            # Don't raise error for custom events to avoid breaking main flow
            return response.json() if response.ok else {}
        except Exception as e:
            print(f"Warning: Failed to log custom event {event_name}: {e}")
            return {}

def determine_model_complexity(input_text: str) -> str:
    """
    Analyzes the input text to determine if it requires a 'fast' (low complexity)
    or 'smart' (high complexity) model.
    
    Returns:
        "gpt-4o-mini" (fast) or "gpt-4o" (smart)
    """
    if not input_text:
        return "gpt-4o-mini"
        
    text = input_text.lower()
    
    # Complexity indicators
    complex_keywords = [
        "analyze", "reason", "explain", "compare", "evaluate", "critique",
        "draft", "compose", "write a", "essay", "comprehensive",
        "syllabus", "curriculum", "strategy", "intervention", "why"
    ]
    
    # Simple action indicators (override complexity if purely functional)
    simple_keywords = [
        "list", "get", "show", "what is", "when is", "update", "change",
        "delete", "remove", "set date", "create assignment", "create quiz"
    ]
    
    # 1. Check for simple actions first (functional tasks are best for mini)
    for word in simple_keywords:
        if word in text:
            return "gpt-4o-mini"
            
    # 2. Check for complexity keywords
    for word in complex_keywords:
        if word in text:
            return "gpt-4o"
            
    # 3. Check length (longer prompts usually need more reasoning)
    if len(text.split()) > 50:
        return "gpt-4o"
        
    # Default to fast model
    return "gpt-4o-mini"

# Convenience functions for common operations

def get_keywordsai_client() -> KeywordsAIClient:
    """Get a Keywords AI client instance."""
    return KeywordsAIClient()


def log_agent_run(
    user_message: str,
    agent_response: str,
    agent_name: str,
    thread_id: str = None,
    customer_id: str = None,
    duration_seconds: float = None,
    tools_used: List[str] = None
) -> Dict[str, Any]:
    """
    Convenience function to log an agent run to Keywords AI.

    Args:
        user_message: The user's input message
        agent_response: The agent's response
        agent_name: Name of the agent (e.g., "Canvas_Executor")
        thread_id: Conversation thread ID
        customer_id: Customer identifier
        duration_seconds: How long the run took
        tools_used: List of tools that were invoked

    Returns:
        The API response
    """
    client = KeywordsAIClient()
    return client.log_request(
        input_messages=[{"role": "user", "content": user_message}],
        output_message={"role": "assistant", "content": agent_response},
        model="gpt-4o-mini",
        customer_identifier=customer_id,
        thread_identifier=thread_id,
        metadata={
            "agent": agent_name,
            "tools_used": tools_used or [],
            "source": "canvas-lms-agent"
        },
        latency=duration_seconds,
        log_type="workflow"
    )
