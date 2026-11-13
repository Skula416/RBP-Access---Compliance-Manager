# Specification: rbp-approval-workflow

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-n8n-workflow.md](../guidelines-n8n-workflow.md) — n8n workflow constraints

---

## Overview

This workflow receives an RBP access recommendation from the AI agent, creates a SAP Task Center approval task for the HR Administrator or Compliance Officer, waits for the decision, and — on approval — automatically applies the permission change in SAP SuccessFactors via the RBP API MCP server. It also maintains the audit log and handles quarterly compliance report delivery.

**Error handling (from PRD):**
- SAP MCP Client — read permissions: continue on error path → notify HR Admin; log failure
- SAP Task Center — approval task: stop workflow → notify HR Admin via email
- SAP MCP Client — apply permission change: continue on error path → notify HR Admin via Teams/email; retain in queue for retry

---

## Setup

- [ ] Create folder `assets/workflows/rbp-approval-workflow/`
- [ ] Invoke the `setup-solution` skill to register the workflow asset in `solution.yaml`

---

## Node Catalog Lookup (MANDATORY before any node is written)

- [ ] Call `search-nodes-catalog` with the following keywords to confirm availability and capture exact `type` and `typeVersion` for every planned node:
  - `webhook`, `respond`, `set`, `switch`, `if`, `code`, `wait`, `stickyNote`, `aggregate`, `splitOut`, `microsoftTeams`, `microsoftOutlook`, `sapTaskCenter`, `sapMcpClient`, `scheduleTrigger`
- [ ] Record the `name` (used as `type`) and `version` (used as `typeVersion`) for each returned node
- [ ] Confirm every planned node was returned by the catalog before writing any workflow JSON

---

## Workflow Design

The workflow handles two distinct flows triggered by separate webhook endpoints:

### Flow 1 — Permission Change Approval (`RBP Recommendation Submitted` webhook)

Triggered when the AI agent submits a recommendation for approval.

**Nodes (in order):**

1. **Webhook trigger** — named `RBP Recommendation Submitted`
   - Receives payload: `request_id`, `user_id`, `issue_description`, `diagnosis`, `recommended_group`, `change_type` (`assign`/`revoke`), `justification`
   - `responseMode: "responseNode"`

2. **Body Validation** (Code node, `onError: "continueErrorOutput"`)
   - Validate required fields: `request_id`, `user_id`, `recommended_group`, `change_type`, `justification`
   - On error output: respond with HTTP 400 and validation error message

3. **Write Audit Log — Received** (SAP MCP Client node)
   - Calls the CAP Audit Log Service MCP tool to write a `recommendation_received` event
   - `onError: "continueErrorOutput"` → on error: log failure, continue (non-blocking)

4. **Create Approval Task** (SAP Task Center node)
   - Creates a task for the HR Administrator or Compliance Officer
   - Task title: `"RBP Permission Change Approval — {user_id}"`
   - Task description includes: diagnosis summary, recommended permission group, change type, justification
   - Recipients: HR Administrator role group (or Compliance Officer group)
   - `onError: "stopWorkflow"` → if Task Center is unavailable, notify HR Admin by email (Microsoft Outlook node) and stop

5. **Notify Approver via Teams** (Microsoft Teams node)
   - Sends a message to the HR Admin / Compliance channel summarising the pending task

6. **Wait for Approval Decision** (Wait node)
   - Resumes when Task Center posts the decision back via the `Approval Decision Received` webhook

7. **Route on Decision** (Switch node)
   - `approved` → proceed to Apply Change branch
   - `rejected` → proceed to Notify Rejection branch
   - fallback → respond with error (unknown decision value)

8. **[Approved branch] Apply Permission Change** (SAP MCP Client node)
   - Calls the RBP Permissions MCP server tool `apply_permission_change`
   - Payload: `user_id`, `permission_group`, `change_type`, `approver_id`, `request_id`
   - `onError: "continueErrorOutput"` → on error output: send Teams/Outlook notification to HR Admin with failure details; write `change_failed` audit entry; respond with error

9. **[Approved branch] Write Audit Log — Applied** (SAP MCP Client node)
   - Writes a `permission_change_applied` event with: `request_id`, `user_id`, `group`, `approver_id`, `timestamp`

10. **[Approved branch] Notify Requester — Approved** (Microsoft Outlook node)
    - Sends email to the requester confirming the permission change was applied

11. **[Rejected branch] Write Audit Log — Rejected** (SAP MCP Client node)
    - Writes a `recommendation_rejected` event with: `request_id`, `approver_id`, `reason`

12. **[Rejected branch] Notify Requester — Rejected** (Microsoft Outlook node)
    - Sends email to requester with the rejection reason

13. **Respond to Webhook** — final node on all paths
    - Returns `200` with `{"status": "processed", "request_id": "..."}`

---

### Flow 2 — Quarterly Compliance Report (`Schedule Trigger`)

- [ ] Confirm `scheduleTrigger` node is available in the catalog; if not, use a `Webhook` trigger named `Generate Compliance Report` and document that an external scheduler must invoke it quarterly

**Nodes (in order):**

1. **Schedule Trigger** — runs every quarter (first day of the quarter)

2. **Fetch All Users & Permissions** (SAP MCP Client node)
   - Calls the RBP Permissions MCP server to retrieve all users and their current permission group assignments
   - `onError: "stopWorkflow"`

3. **Detect SoD Conflicts** (SAP AI Core / Code node)
   - Evaluates each user's permission groups for Segregation of Duties conflicts (e.g. create + approve in same module)
   - Produces structured list of conflicts with user ID, conflicting groups, and risk level

4. **Fetch Audit Log — Change History** (SAP MCP Client node)
   - Retrieves all `permission_change_applied` and `recommendation_rejected` entries for the reporting period from the CAP Audit Log Service

5. **Generate Report** (Code node)
   - Combines SoD conflict list, change history, and best practice deviation summary
   - Formats as structured JSON report

6. **Deliver Report via Email** (Microsoft Outlook node)
   - Sends the compliance report to the Compliance Officer and HR Administrator

7. **Deliver Report via Teams** (Microsoft Teams node)
   - Posts a summary to the compliance channel with a link to the full report

---

## Implementation Tasks

- [ ] Read the `n8n-sap-task-center` skill reference file before configuring the SAP Task Center node
- [ ] Read the `n8n-sap-mcp-client` skill reference file before configuring any SAP MCP Client node
- [ ] Read the `n8n-trigger-nodes-webhook` skill reference file before configuring webhook nodes and body validation
- [ ] Build the complete workflow JSON in memory, then apply all pre-write checks (topology, convergence, caller contract, error handling, pinData) before writing
- [ ] Write the workflow to `assets/workflows/rbp-approval-workflow/rbp-approval-workflow.n8n.json`

---

## Post-Write Tasks

- [ ] Run `node scripts/generate-workflow-asset.js assets/workflows/rbp-approval-workflow/rbp-approval-workflow.n8n.json rbp-approval-workflow <solution-name>` to generate `workflow:` and `provides.apis[]` blocks for `asset.yaml`
- [ ] Paste the generated output into `assets/workflows/rbp-approval-workflow/asset.yaml`; fill in the `description` for each `kind: rest` entry:
  - `RBP Recommendation Submitted`: "Receives an RBP permission change recommendation from the AI agent for human approval"
  - `Approval Decision Received`: "Receives the approval or rejection decision from SAP Task Center to resume the workflow"
- [ ] Refine `workflow-schema.openapi.json`: replace all `<...>` placeholders, set correct field types (`request_id: string`, `user_id: string`, `recommended_group: string`, `change_type: string (enum: assign, revoke)`, `justification: string`, `decision: string (enum: approved, rejected)`), add `required` arrays, verify Switch operator types align with schema types
- [ ] Add body validation flow after the `RBP Recommendation Submitted` webhook node (Code node with `REQUIRED_FIELDS` matching the schema `required[]`)
- [ ] Fetch pinData schemas for all node types used and embed sample pinData in the workflow JSON
- [ ] Validate with `validate-n8n-workflow` MCP tool (pass workflow JSON + asset.yaml content); fix all errors before writing

---

## MCP Server for Agent Consumption (MANDATORY — Steps A–F)

The AI agent must invoke this workflow via MCP tool (not direct webhook call). Complete Steps A–F from `execution.md`:

- [ ] **Step A**: Run `node scripts/generate-webhook-openapi.js assets/workflows/rbp-approval-workflow/rbp-approval-workflow.n8n.json rbp-approval-workflow > specification/rbp-approval-workflow-mcp-server/api-specs/rbp-approval-workflow-webhook-api.json`
- [ ] **Step B**: Create `specification/rbp-approval-workflow-mcp-server/specification.md` referencing the REST ORD ID from the workflow's `asset.yaml`
- [ ] **Step C**: Invoke `mcp-translation-file` skill with asset name `rbp-approval-workflow-mcp-server`; copy translation artifacts to `assets/rbp-approval-workflow-mcp-server/mcp-translation/`
- [ ] **Step D**: Write `assets/rbp-approval-workflow-mcp-server/asset.yaml` with the MCP card ORD ID derived from the REST ORD ID (replace `_` separator with `.`, append `-mcp-server` to the workflow name segment)
- [ ] **Step E**: Add `rbp-approval-workflow-mcp-server` ref to `solution.yaml`
- [ ] **Step F**: Add `requires` entry to `assets/rbp-access-agent/asset.yaml` for the workflow MCP server; add system prompt instruction: "To submit a recommendation for approval, use the `rbpRecommendationSubmitted` MCP tool. Do not call workflow webhook URLs directly."

---

## Validation

- [ ] Verify `assets/workflows/rbp-approval-workflow/rbp-approval-workflow.n8n.json` is valid JSON
- [ ] Verify `assets/workflows/rbp-approval-workflow/asset.yaml` exists and contains `workflow:`, `provides.apis[]`, and correct `ordId` values
- [ ] Verify `assets/rbp-approval-workflow-mcp-server/asset.yaml` exists with the correct MCP card ORD ID
- [ ] Verify `solution.yaml` references both the workflow and the MCP server assets
