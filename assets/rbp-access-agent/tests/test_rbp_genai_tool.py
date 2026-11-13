"""Unit tests for RBP GenAI Troubleshooting MCP tool mock."""
import json
import pytest


def test_rbp_genai_tool_returns_diagnosis(add_agent_to_path):
    """Mock RBP GenAI tool should return a structured diagnosis."""
    mock_path = __import__("pathlib").Path(__file__).parent.parent / "mcp-mock.json"
    mock_data = json.loads(mock_path.read_text())

    server = mock_data["servers"]["sf-rbp-genai"]
    tool = server["tools"]["POST_rest_iam_authorization_genai_v1_permissions"]

    assert tool["description"] is not None
    assert "diagnosis" in tool["mock_response"]
    assert "recommendedPermissionGroup" in tool["mock_response"]["diagnosis"]
    assert tool["mock_response"]["diagnosis"]["confidence"] == "HIGH"


def test_rbp_genai_tool_input_schema(add_agent_to_path):
    """RBP GenAI tool should require userId and issueDescription."""
    mock_path = __import__("pathlib").Path(__file__).parent.parent / "mcp-mock.json"  # noqa
    mock_data = json.loads(mock_path.read_text())

    tool = mock_data["servers"]["sf-rbp-genai"]["tools"][
        "POST_rest_iam_authorization_genai_v1_permissions"
    ]
    schema = tool["input_schema"]
    assert "userId" in schema["properties"]
    assert "issueDescription" in schema["properties"]
    assert "userId" in schema["required"]
    assert "issueDescription" in schema["required"]


def test_rbp_genai_roles_tool_returns_list(add_agent_to_path):
    """GET roles tool should return a list of available RBP roles."""
    mock_path = __import__("pathlib").Path(__file__).parent.parent / "mcp-mock.json"
    mock_data = json.loads(mock_path.read_text())

    tool = mock_data["servers"]["sf-rbp-genai"]["tools"][
        "GET_rest_iam_authorization_genai_v1_roles"
    ]
    response = tool["mock_response"]
    assert "results" in response
    assert len(response["results"]) > 0
    assert "roleName" in response["results"][0]
