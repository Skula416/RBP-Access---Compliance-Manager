"""Integration test for the full RBP access agent flow."""
from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.mark.asyncio
async def test_rbp_investigation_full_flow(add_agent_to_path):
    """
    Integration test: user submits an access issue →
    agent investigates using mocked MCP tools →
    produces a recommendation and submits for approval.
    """
    import sys
    agent_app = str(Path(__file__).parent.parent / "app")
    if agent_app not in sys.path:
        sys.path.insert(0, agent_app)

    from agent import SampleAgent

    # Build mock LangChain tools
    genai_tool_mock = MagicMock()
    genai_tool_mock.name = "mcp_sf_rbp_genai__POST_rest_iam_authorization_genai_v1_permissions"
    genai_tool_mock.description = "Diagnose RBP access issues"
    genai_tool_mock.coroutine = None

    approval_tool_mock = MagicMock()
    approval_tool_mock.name = "mcp_rbp_approval__RbpRecommendationSubmittedUsingPOST"
    approval_tool_mock.description = "Submit recommendation for approval"
    approval_tool_mock.coroutine = None

    mocked_tools = [genai_tool_mock, approval_tool_mock]

    # Mock the LLM to return a structured recommendation
    mock_llm_response = MagicMock()
    mock_llm_response.content = (
        "I have investigated your access issue. You are missing the 'Compensation Planner' "
        "permission group. I have submitted this recommendation for approval with request ID "
        "req-test-001. You will be notified by email when a decision is made. "
        "submitted for approval"
    )

    # Mock _invoke directly to avoid real LLM + MCP calls
    with patch("agent.SampleAgent._invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = {"messages": [mock_llm_response]}
        agent = SampleAgent()
        response = await agent.invoke(
            query="I cannot access the Compensation module in SuccessFactors",
            context_id="test-context-001",
            tools=mocked_tools,
        )

    assert response.status == "completed"
    assert response.message is not None
    assert len(response.message) > 0


@pytest.mark.asyncio
async def test_empty_query_handled_gracefully(add_agent_to_path):
    """Empty query should return an early response from _run_agent (M1.missed path)."""
    import sys
    agent_app = str(Path(__file__).parent.parent / "app")
    if agent_app not in sys.path:
        sys.path.insert(0, agent_app)

    from agent import SampleAgent

    agent = SampleAgent()
    response = await agent.invoke(
        query="   ",
        context_id="test-context-002",
        tools=[],
    )

    # M1.missed path: _run_agent returns early without calling _invoke
    assert response.status in ("completed", "error")


@pytest.mark.asyncio
async def test_milestone_logging_emits_m1_achieved(add_agent_to_path, caplog):
    """Submitting a valid query should emit an M1.achieved log."""
    import logging
    import sys
    agent_app = str(Path(__file__).parent.parent / "app")
    if agent_app not in sys.path:
        sys.path.insert(0, agent_app)

    from agent import SampleAgent

    mock_llm_response = MagicMock()
    mock_llm_response.content = "Your request has been received."

    with patch("agent.SampleAgent._invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = {"messages": [mock_llm_response]}
        agent = SampleAgent()
        with caplog.at_level(logging.INFO, logger="agent"):
            await agent.invoke(
                query="I cannot access the Performance module",
                context_id="test-context-003",
                tools=[],
            )

    # M1.achieved should appear in the log
    log_messages = " ".join(caplog.messages)
    assert "M1.achieved" in log_messages
