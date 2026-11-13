"""Unit tests for User Management MCP tool mock."""
import json
import pytest


def _get_mock(tool_name: str):
    mock_path = __import__("pathlib").Path(__file__).parent.parent / "mcp-mock.json"
    mock_data = json.loads(mock_path.read_text())
    return mock_data["servers"]["sf-user-management"]["tools"][tool_name]


def test_get_user_returns_profile(add_agent_to_path):
    """get_user_for_sfodata should return a complete user profile."""
    tool = _get_mock("get_user_for_sfodata")
    assert "userId" in tool["input_schema"]["required"]
    response = tool["mock_response"]
    assert "userId" in response
    assert "firstName" in response
    assert "email" in response
    assert "status" in response


def test_list_users_returns_results(add_agent_to_path):
    """list_user_for_sfodata should return a list of users."""
    tool = _get_mock("list_user_for_sfodata")
    response = tool["mock_response"]
    assert "results" in response
    assert len(response["results"]) > 0
    first_user = response["results"][0]
    assert "userId" in first_user
    assert "email" in first_user
