"""Unit tests for submit-for-approval MCP tool mock (workflow webhook)."""
import json
import pytest


def _get_mock(tool_name: str):
    mock_path = __import__("pathlib").Path(__file__).parent.parent / "mcp-mock.json"
    mock_data = json.loads(mock_path.read_text())
    return mock_data["servers"]["rbp-approval-workflow"]["tools"][tool_name]


def test_submit_recommendation_returns_submitted_status(add_agent_to_path):
    """RbpRecommendationSubmittedUsingPOST should return submitted status."""
    tool = _get_mock("RbpRecommendationSubmittedUsingPOST")
    response = tool["mock_response"]
    assert response["status"] == "submitted"
    assert "request_id" in response
    assert "message" in response


def test_submit_recommendation_requires_key_fields(add_agent_to_path):
    """Submission tool must require request_id, user_id, recommended_group, change_type, justification."""
    tool = _get_mock("RbpRecommendationSubmittedUsingPOST")
    required = tool["input_schema"]["required"]
    for field in ["request_id", "user_id", "recommended_group", "change_type", "justification"]:
        assert field in required, f"Missing required field: {field}"


def test_submit_recommendation_change_type_enum(add_agent_to_path):
    """change_type must be enum of assign/revoke."""
    tool = _get_mock("RbpRecommendationSubmittedUsingPOST")
    change_type_schema = tool["input_schema"]["properties"]["change_type"]
    assert "enum" in change_type_schema
    assert "assign" in change_type_schema["enum"]
    assert "revoke" in change_type_schema["enum"]


def test_compliance_report_tool_exists(add_agent_to_path):
    """GenerateComplianceReportUsingPOST should be available."""
    tool = _get_mock("GenerateComplianceReportUsingPOST")
    assert tool["mock_response"]["status"] == "completed"
    assert "period" in tool["mock_response"]
    assert "sodConflicts" in tool["mock_response"]
