"""Unit tests for RBP Permissions MCP tool mock."""
import json
import pytest


def _get_mock(tool_name: str):
    mock_path = __import__("pathlib").Path(__file__).parent.parent / "mcp-mock.json"
    mock_data = json.loads(mock_path.read_text())
    return mock_data["servers"]["sf-rbp-permissions"]["tools"][tool_name]


def test_list_rbp_roles_returns_results(add_agent_to_path):
    """list_rbprole should return a list of RBP roles."""
    tool = _get_mock("list_rbprole_for_sfodata")
    response = tool["mock_response"]
    assert "results" in response
    assert len(response["results"]) > 0
    assert "roleId" in response["results"][0]
    assert "roleName" in response["results"][0]


def test_get_user_permissions_returns_permission_list(add_agent_to_path):
    """function_getuserspermissions should return user's permissions."""
    tool = _get_mock("function_getuserspermissions_for_sfodata")
    assert "userId" in tool["input_schema"]["required"]
    response = tool["mock_response"]
    assert "permissions" in response
    assert isinstance(response["permissions"], list)


def test_get_user_roles_by_user_id_returns_roles(add_agent_to_path):
    """function_getuserrolesbyuserid should return roles for a user."""
    tool = _get_mock("function_getuserrolesbyuserid_for_sfodata")
    response = tool["mock_response"]
    assert "userId" in response
    assert "roles" in response
    assert isinstance(response["roles"], list)


def test_update_static_group_returns_success(add_agent_to_path):
    """function_updatestaticgroup should return success status."""
    tool = _get_mock("function_updatestaticgroup_for_sfodata")
    assert "userId" in tool["input_schema"]["required"]
    assert "groupId" in tool["input_schema"]["required"]
    assert "action" in tool["input_schema"]["required"]
    assert tool["mock_response"]["success"] is True


def test_check_user_permission_returns_bool(add_agent_to_path):
    """function_checkuserpermission should return hasPermission flag."""
    tool = _get_mock("function_checkuserpermission_for_sfodata")
    response = tool["mock_response"]
    assert "hasPermission" in response
    assert isinstance(response["hasPermission"], bool)
