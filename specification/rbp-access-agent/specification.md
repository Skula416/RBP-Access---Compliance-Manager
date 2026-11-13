# Specification: rbp-access-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [ ] Read `product-requirements-document.md` and `intent.md` for full context before starting
- [ ] Bootstrap agent code in `assets/rbp-access-agent/` using instructions from the `sap-agent-bootstrap` skill (invoke from inside `assets/rbp-access-agent/`, use copy commands — do NOT create files manually)
- [ ] Install dependencies; validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

The agent requires runtime skills due to the complexity of the RBP investigation and compliance workflows.

- [ ] Create `assets/rbp-access-agent/app/skills/rbp-investigation/SKILL.md` with:
  - YAML frontmatter: `name: rbp-investigation`, `description: Step-by-step workflow for investigating and diagnosing RBP access issues in SAP SuccessFactors`
  - Body covering:
    - Step 1: Collect issue details (user ID, module/feature they cannot access, error message if any)
    - Step 2: Retrieve the user's current permission group assignments via the User Management MCP tool
    - Step 3: Call the RBP GenAI Troubleshooting tool with the user ID and access issue description
    - Step 4: Cross-reference the diagnosis result with current assignments from the Role-Based Permissions tool
    - Step 5: Produce a structured recommendation (affected permission group, recommended change, justification in plain language)
    - Step 6: If confidence is low or diagnosis is inconclusive, escalate to HR Admin rather than guessing
  - Include a reference table `references/rbp-issue-types.md` listing common RBP issue categories and typical permission group fixes

- [ ] Create `assets/rbp-access-agent/app/skills/compliance-reporting/SKILL.md` with:
  - YAML frontmatter: `name: compliance-reporting`, `description: Generates quarterly RBP compliance reports including SoD analysis, change history, and best practice deviations`
  - Body covering:
    - Step 1: Query all users and their current permission group assignments via the Role-Based Permissions tool
    - Step 2: Identify users with multiple permission groups that create Segregation of Duties (SoD) conflicts (e.g. create + approve in the same module)
    - Step 3: Retrieve change history from the audit log for the reporting period
    - Step 4: Compare current assignments against SAP SuccessFactors RBP best practices (least-privilege, no broad admin permissions for end users)
    - Step 5: Produce a structured report with sections: SoD Conflicts, Change History, Best Practice Deviations, Recommended Actions
    - Step 6: Format report for email/Teams delivery

---

## Project-Specific Tasks

### Agent System Prompt

- [ ] Open `assets/rbp-access-agent/app/agent.py` and set the system prompt to include:
  - The agent's purpose: investigate and resolve SAP SuccessFactors RBP access issues, route for approval, and support compliance reporting
  - Instruction to use MCP tools for all SuccessFactors data — never fabricate or guess permission data
  - Instruction: "When calling tools that support pagination, always set the page size parameter to a maximum of 100 items."
  - Instruction: "If a tool returns an error, report the error message exactly as received. Do not suggest workarounds."
  - Instruction: "To submit a recommendation for approval, use the `submit_for_approval` MCP tool. Do not call workflow webhook URLs directly."
  - Instruction to load the `rbp-investigation` skill when an access issue is submitted
  - Instruction to load the `compliance-reporting` skill when a compliance report is requested

### RBP Investigation Tool Integration

- [ ] Invoke the `mcp-translation-file` skill for `specification/rbp-access-agent/api-specs/PLTRBPGenAI-api-spec.json` (REST/OpenAPI) to generate a translation card at `specification/rbp-access-agent/mcps/PLTRBPGenAI/`
  - MCP tool scope: `read-only`
  - Resources in scope: all (full RBP GenAI Troubleshooting surface)

- [ ] Invoke the `mcp-translation-file` skill for `specification/rbp-access-agent/api-specs/PLTRoleBasedPermissions-api-spec.edmx` (OData) to generate a translation card at `specification/rbp-access-agent/mcps/PLTRoleBasedPermissions/`
  - MCP tool scope: `read-write`
  - Resources in scope: `PermissionRole, PermissionRoleData, PermissionGroup, PermissionGroupMember, PermissionUserGroup, RoleAssignment`

- [ ] Invoke the `mcp-translation-file` skill for `specification/rbp-access-agent/api-specs/PLTUserManagement-api-spec.edmx` (OData) to generate a translation card at `specification/rbp-access-agent/mcps/PLTUserManagement/`
  - MCP tool scope: `read-only`
  - Resources in scope: `User, PerPerson, PerPersonal, PerEmail`

- [ ] Invoke the `mcp-translation-file` skill for `specification/rbp-access-agent/api-specs/FoundationPlatformPLT-api-spec.edmx` (OData) to generate a translation card at `specification/rbp-access-agent/mcps/FoundationPlatformPLT/`
  - MCP tool scope: `read-only`
  - Resources in scope: `Department, Division, JobCode, Location`

### MCP Server Assets

- [ ] Invoke the `setup-solution` skill to register MCP server assets for each generated translation card:
  - `rbp-genai-mcp-server` — RBP GenAI Troubleshooting API
  - `rbp-permissions-mcp-server` — Role-Based Permissions API
  - `rbp-user-management-mcp-server` — User Management API
  - `rbp-foundation-mcp-server` — Common Platform (Foundation) API

### Wire MCP Tools into Agent

- [ ] Wire MCP tool loading in `assets/rbp-access-agent/app/agent.py` using `get_mcp_tools()` from the `mcp_tools` module (lazy loading pattern — see `guidelines-agent-python.md`)
- [ ] Add all four MCP server dependencies to `assets/rbp-access-agent/asset.yaml` under `requires`, using exact ORD IDs from the generated `asset.yaml` files for each MCP server asset
- [ ] Add a `requires` entry to `assets/rbp-access-agent/asset.yaml` for the approval workflow MCP server (Path C) once the n8n workflow asset is created:
  - Derive the MCP card ORD ID from the workflow's `asset.yaml` REST ORD ID (replace `_` separator with `.` and append `-mcp-server` to the workflow name segment)
  - Add system prompt instruction: "To submit a recommendation for approval, use the `submit_for_approval` MCP tool exposed by the rbp-approval-workflow. Do not call workflow webhook URLs directly."

### Approval Submission Tool

- [ ] Ensure the agent's system prompt instructs it to call the `submit_for_approval` MCP tool (from the rbp-approval-workflow n8n MCP server) with the following payload:
  - `user_id`: ID of the user with the access issue
  - `issue_description`: plain-language description of the problem
  - `diagnosis`: structured diagnosis from the RBP GenAI tool
  - `recommended_group`: permission group to be assigned or removed
  - `change_type`: `assign` or `revoke`
  - `justification`: plain-language rationale for the approver

### Audit Log Integration

- [ ] The agent must log every key lifecycle event to the CAP Audit Log Service. Implement an MCP tool or direct CAP service call (via MCP) to write audit entries with:
  - `request_id`, `user_id`, `event_type` (submitted / recommendation_produced / escalated), `timestamp`, `actor_id`, `details`
- [ ] Ensure audit log writes are non-blocking — a failure to write the log must not halt the investigation flow, but must emit `M5.missed` log

---

## MCP API Scope Summary

```
MCP API: sap.sf:apiResource:PLTRBPGenAI:v1
MCP tool scope: read-only
Resources in scope: all

MCP API: sap.sf:apiResource:PLTRoleBasedPermissions:v1
MCP tool scope: read-write
Resources in scope: PermissionRole, PermissionRoleData, PermissionGroup, PermissionGroupMember, PermissionUserGroup, RoleAssignment

MCP API: sap.sf:apiResource:PLTUserManagement:v1
MCP tool scope: read-only
Resources in scope: User, PerPerson, PerPersonal, PerEmail

MCP API: sap.sf:apiResource:FoundationPlatformPLT:v1
MCP tool scope: read-only
Resources in scope: Department, Division, JobCode, Location
```

---

## Business Instrumentation

- [ ] Implement the following milestones in `assets/rbp-access-agent/app/agent.py` with structured log statements and OpenTelemetry spans. Extract all business logic from `stream()` into a plain async helper `_run_agent()` to avoid `GeneratorExit` context errors:

  - **M1 — Issue Submitted**
    - `M1.achieved`: `M1.achieved: RBP access issue submitted by user {user_id}, request_id={request_id}`
    - `M1.missed`: `M1.missed: Issue submission did not complete — no valid input received`

  - **M2 — AI Investigation Complete**
    - `M2.achieved`: `M2.achieved: Diagnosis complete for request_id={request_id}, recommended_group={group_name}`
    - `M2.missed`: `M2.missed: Agent could not produce a recommendation for request_id={request_id} — escalating to HR Admin`

  - **M3 — Approval Task Sent**
    - `M3.achieved`: `M3.achieved: Approval task created for request_id={request_id}, approver={approver_id}`
    - `M3.missed`: `M3.missed: Approval task could not be created for request_id={request_id}`

  - **M4 — Permission Change Applied**
    - `M4.achieved`: `M4.achieved: Permission change applied for user_id={user_id}, group={group_name}, request_id={request_id}`
    - `M4.missed`: `M4.missed: Permission change could not be applied for request_id={request_id} — manual intervention required`

  - **M5 — Audit Entry Recorded**
    - `M5.achieved`: `M5.achieved: Audit entry persisted for request_id={request_id}`
    - `M5.missed`: `M5.missed: Audit log write failed for request_id={request_id} — data integrity risk`

- [ ] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`

---

## Mock & Testing Setup

- [ ] Generate `mcp-mock.json` using the `mcp-mock-config` skill after all MCP translation cards are created
- [ ] Write unit tests in `assets/rbp-access-agent/tests/` — one per MCP tool:
  - `test_rbp_genai_tool.py` — mock diagnosis response; assert structured recommendation returned
  - `test_rbp_permissions_tool.py` — mock permission group read; assert correct user assignments returned
  - `test_user_management_tool.py` — mock user profile read; assert user ID and details returned
  - `test_foundation_tool.py` — mock department/division lookup; assert org data returned
  - `test_submit_for_approval_tool.py` — mock approval workflow MCP tool; assert payload is correctly formed
  - `test_audit_log_tool.py` — mock audit log write; assert event entry is written
- [ ] Write one integration test (`tests/test_integration.py`) exercising the full flow:
  - User submits "I cannot access the Compensation module"
  - Agent calls RBP GenAI tool → receives diagnosis → calls RBP Permissions tool → produces recommendation → calls `submit_for_approval`
  - Assert M1–M3 log entries emitted; assert recommendation payload is well-formed
- [ ] Run `pytest` from `assets/rbp-access-agent/` (no args) — fix failures before proceeding
- [ ] Verify coverage ≥ 70%; add tests if below threshold
- [ ] Run `pytest` again (no args) to produce final `test_report.json`
- [ ] Verify `test_report.json` exists in `assets/rbp-access-agent/`

---

## Validation

```bash
# Instrumentation check
grep -r "M[0-9]\.achieved" assets/rbp-access-agent/app/

# Test report check
ls assets/rbp-access-agent/test_report.json
```
