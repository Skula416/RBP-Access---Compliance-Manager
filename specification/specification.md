# Specification

> **Guidelines**: Read [guidelines.md](./guidelines.md) before executing ANY tasks below.

Check off items as completed.

---

## Solution Setup

- [x] Create asset directories:
  ```bash
  mkdir -p assets/rbp-access-agent/
  mkdir -p assets/workflows/rbp-approval-workflow/
  ```
- [x] Invoke the `setup-solution` skill to create `solution.yaml` and `asset.yaml` files for every asset in the solution:
  - Asset 1: `rbp-access-agent` (type: `agent`)
  - Asset 2: `rbp-approval-workflow` (type: `n8nworkflow`, under `assets/workflows/rbp-approval-workflow/`)
  - Asset 3: MCP server assets will be generated during implementation (one per SuccessFactors API + one for the workflow webhook)
- [x] Validate all `asset.yaml` and `solution.yaml` files exist and are well-formed

---

## Asset Implementation

- [x] Execute `specification/rbp-access-agent/specification.md` (all items)
  - Bootstraps the Python AI agent
  - Generates MCP translation files for the 4 SuccessFactors APIs
  - Creates MCP server assets for each API
  - Instruments all 5 business milestones (M1–M5)
  - Runs tests with ≥70% coverage and produces `test_report.json`

- [x] Execute `specification/rbp-approval-workflow/specification.md` (all items)
  - Builds the n8n approval workflow (Flow 1: permission change approval + Flow 2: quarterly compliance report)
  - Configures SAP Task Center for human-in-the-loop approval
  - Wires error handling per PRD decisions
  - Generates MCP server for agent consumption (Steps A–F)
  - Validates workflow JSON and asset.yaml

- [x] **Cross-implementation compatibility check** — verify the following before declaring the solution complete:
  - The agent's `asset.yaml` `requires` section includes all 4 SuccessFactors MCP servers and the `rbp-approval-workflow-mcp-server`
  - The agent's system prompt instructs it to use the `rbpRecommendationSubmitted` MCP tool (not a direct webhook URL)
  - The `rbp-approval-workflow-mcp-server` `asset.yaml` ORD ID is correctly derived from the workflow's REST ORD ID (`.` separator, `-mcp-server` suffix on the workflow name segment)
  - `solution.yaml` references all assets: `rbp-access-agent`, `rbp-approval-workflow`, all SuccessFactors MCP server assets, and `rbp-approval-workflow-mcp-server`
  - Milestone log patterns (`M1.achieved`, `M2.achieved`, etc.) are present in the agent code
  - Workflow JSON passes `validate-n8n-workflow` with no blocking errors

---

## Asset Summary

| Asset | Type | Path | Purpose |
|---|---|---|---|
| `rbp-access-agent` | Python AI Agent (A2A) | `assets/rbp-access-agent/` | Investigates RBP access issues, produces recommendations, submits for approval |
| `rbp-approval-workflow` | n8n Workflow | `assets/workflows/rbp-approval-workflow/` | Human-in-the-loop approval, auto-applies approved changes, quarterly compliance reports |
| `rbp-genai-mcp-server` | MCP Server | `assets/rbp-genai-mcp-server/` | Exposes RBP GenAI Troubleshooting API to the agent |
| `rbp-permissions-mcp-server` | MCP Server | `assets/rbp-permissions-mcp-server/` | Exposes Role-Based Permissions API (read + write) to the agent and workflow |
| `rbp-user-management-mcp-server` | MCP Server | `assets/rbp-user-management-mcp-server/` | Exposes User Management API to the agent |
| `rbp-foundation-mcp-server` | MCP Server | `assets/rbp-foundation-mcp-server/` | Exposes Common Platform (Foundation) API to the agent |
| `rbp-approval-workflow-mcp-server` | MCP Server | `assets/rbp-approval-workflow-mcp-server/` | Exposes the workflow webhook to the agent as an MCP tool |

---

## API Specs Available

| File | API | Type | Used by |
|---|---|---|---|
| `specification/rbp-access-agent/api-specs/PLTRBPGenAI-api-spec.json` | RBP GenAI Troubleshooting | REST (OpenAPI JSON) | rbp-access-agent |
| `specification/rbp-access-agent/api-specs/PLTRoleBasedPermissions-api-spec.edmx` | Role-Based Permissions | OData (EDMX) | rbp-access-agent, rbp-approval-workflow |
| `specification/rbp-access-agent/api-specs/PLTUserManagement-api-spec.edmx` | User Management | OData (EDMX) | rbp-access-agent |
| `specification/rbp-access-agent/api-specs/FoundationPlatformPLT-api-spec.edmx` | Common Platform / Foundation | OData (EDMX) | rbp-access-agent |
