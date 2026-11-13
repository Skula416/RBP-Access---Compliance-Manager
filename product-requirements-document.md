# Product Requirements Document (PRD)

**Title:** RBP Access & Compliance Manager
**Date:** 2026-11-13
**Owner:** HR Technology / People Systems
**Solution Category:** AI Agent, n8n Workflow, MCP Server

---

## Product Purpose & Value Proposition

**Elevator Pitch:**
HR users, managers, and employees cannot easily diagnose or fix Role-Based Permission (RBP) access issues in SAP SuccessFactors. This solution automates the investigation, routes changes through a human approval step, automatically applies approved changes, and delivers ongoing compliance reporting — turning a multi-day manual process into a guided, auditable, near-instant experience.

**Business Need:**
RBP configuration in SAP SuccessFactors is complex. When users lose access or have incorrect permissions, administrators must manually trace permission groups, roles, and targets — a process that is slow, error-prone, and undocumented. There is no structured approval gate before changes are made, and no automated compliance audit against SAP best practices.

**Expected Value:**
- 70% reduction in average RBP issue resolution time
- Zero manual admin effort required after an approval is given
- 100% quarterly coverage of RBP compliance audits
- 100% detection rate for Segregation of Duties (SoD) conflicts

**Product Objectives (Prioritized):**
1. Automate RBP access issue investigation and provide actionable recommendations using AI
2. Enforce human-in-the-loop approval before any permission change is applied
3. Automatically apply approved changes in SAP SuccessFactors with full audit logging
4. Deliver periodic RBP compliance reports based on SAP best practices

---

## Business Metrics

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Average time to resolve an RBP access issue | — | Reduce by 70% | — | RBP Access Issue Resolution | agent-derived |
| Permission changes requiring manual admin effort | — | 0% (fully automated post-approval) | — | Permission Change Management | agent-derived |
| RBP audit compliance coverage | — | 100% of users reviewed per cycle | Quarterly | RBP Compliance Reporting | agent-derived |
| Segregation of Duties (SoD) conflicts identified | — | Detect 100% of flagged conflicts | — | Access Governance | agent-derived |

---

## User Profiles & Personas

### Primary Persona: Emma — Employee (Self-Service Requester)

Emma is a 34-year-old HR Business Partner who uses SAP SuccessFactors daily for talent management. She recently lost access to a compensation module and doesn't know why. She has no idea what permission group controls this access or who to contact. She opens a ticket with IT, waits three days, and gets a partial fix. She is comfortable with technology but expects intuitive self-service — she should not need to understand SuccessFactors' internal permission model to get her job done.

**Frustrations:** Long wait times, no visibility into request status, having to re-explain the same issue multiple times.

### Secondary Persona: Alex — HR Administrator (Approver)

Alex is a 42-year-old HR Systems Administrator responsible for SuccessFactors configuration across the organisation. He reviews permission change requests, manually verifies their legitimacy, and applies changes. He is the bottleneck: every access issue lands in his queue. He needs a fast, reliable way to review AI-generated recommendations and approve or reject them — without spending 30 minutes tracing each case manually.

**Frustrations:** Repetitive, low-complexity cases consuming his time; no clear audit trail of who changed what and why; compliance reviews done manually with spreadsheets.

### Tertiary Persona: Sandra — Security & Compliance Officer

Sandra is a 38-year-old IT Security Officer responsible for access governance and compliance audits. She needs quarterly reports showing who has which permissions, any SoD conflicts, and a history of all permission changes. Today she requests this data manually from Alex and compiles reports in Excel. She requires evidence for auditors that all changes were approved before being applied.

### Other User Types

- **Managers** — submit permission requests on behalf of direct reports via the same interface as employees.

---

## User Goals & Tasks

### For Emma (Employee):

**Goals:**
- Quickly describe an access issue and receive a clear explanation of what is wrong
- Submit a permission change request without needing to know SuccessFactors internals
- Track the status of her request and be notified when it is resolved

**Key Tasks:**
- Open the RBP assistant in SuccessFactors and describe the access problem in plain language
- Review the AI's diagnosis and confirm the recommended fix
- Receive a notification when the change is approved and applied

### For Alex (HR Administrator):

**Goals:**
- Review AI-generated permission recommendations efficiently with full context
- Approve or reject changes with a single action
- Maintain a clean, auditable record of all permission changes made

**Key Tasks:**
- Receive an approval task via SAP Task Center
- Review the diagnosis, the recommended permission group change, and the justification
- Approve or reject — approved changes are applied automatically

### For Sandra (Compliance Officer):

**Goals:**
- Access up-to-date RBP compliance reports without manual effort
- Identify SoD conflicts and excessive permissions proactively
- Provide auditors with a change history log on demand

**Key Tasks:**
- Receive periodic compliance reports by email / Teams
- Review SoD conflict flags and drill into specific user access profiles
- Export or reference the audit log for regulatory evidence

---

## Product Principles

1. **AI proposes, humans approve**: The AI agent never applies a permission change autonomously. Every change requires explicit approval from an authorised person before it is enacted.
2. **No black boxes**: Every recommendation must include a plain-language justification that a non-technical approver can understand and act on.
3. **Auditability by design**: All requests, recommendations, decisions, and applied changes are logged with timestamps, actor identity, and rationale from day one.
4. **Compliance as a continuous output**: Compliance reporting is automated and periodic — not a one-off export. The system surfaces issues proactively, not only when asked.
5. **Minimal footprint**: The solution reads and writes only what is necessary. It does not modify permission structures beyond the scope of a specific approved request.

---

## Goals and Non-Goals

### Goals (In Scope)

- AI-powered investigation of RBP access issues using the SAP SuccessFactors RBP GenAI Troubleshooting API
- Human-in-the-loop approval via SAP Task Center before any permission change is applied
- Automatic application of approved permission changes via the SuccessFactors Role-Based Permissions API
- Audit log of all requests, recommendations, approvals/rejections, and applied changes
- Periodic compliance reports: SoD analysis, change history, best practice deviation detection
- Accessible from within SAP SuccessFactors (via Joule integration)
- Email and/or Microsoft Teams notification for approvers

### Non-Goals (Out of Scope)

- Integration with non-SuccessFactors permission systems (e.g. SAP S/4HANA authorisations, Active Directory)
- Native SAP Cloud Identity Access Governance (IAG) integration — custom reporting is used instead
- Automated employee onboarding provisioning or role lifecycle management
- Modification of SuccessFactors permission groups or role definitions (only assignments are changed)
- GDPR-specific data subject request handling

---

## Requirements

### Must-Have Requirements

**REQ-01: AI-Powered RBP Issue Investigation**

- **Problem to Solve**: Users cannot diagnose why they have lost access or have incorrect permissions in SuccessFactors without deep system knowledge.
- **User Story**: As an employee or HR admin, I need to describe my access issue in plain language so that the AI can identify the root cause and recommend the correct permission fix.
- **Acceptance Criteria**:
  - Given a submitted access issue description, when the agent processes it, then it returns a diagnosis identifying the affected permission group and a specific recommended change with a plain-language justification.
  - Given a request that cannot be diagnosed, when the agent reaches the limit of available information, then it returns a clear explanation of what additional information is needed.
- **Maps to Objective**: Objective 1
- **Priority Rank**: 1

**REQ-02: Human Approval Workflow via SAP Task Center**

- **Problem to Solve**: Permission changes are currently applied without a formal approval gate, creating compliance and audit risk.
- **User Story**: As an HR Administrator or Compliance Officer, I need to receive a structured approval task so that I can review and approve or reject a recommended permission change before it is applied.
- **Acceptance Criteria**:
  - Given an AI recommendation, when the n8n workflow routes the approval task, then it appears in SAP Task Center for the designated HR Admin and/or Compliance Officer.
  - Given a rejection, when the approver rejects the task, then the change is not applied and the requester is notified with the reason.
- **Maps to Objective**: Objective 2
- **Priority Rank**: 2

**REQ-03: Automated Permission Change Application**

- **Problem to Solve**: After an approval, the HR Admin must still manually apply the change in SuccessFactors — a slow and error-prone step.
- **User Story**: As an HR Administrator, I need approved permission changes to be applied automatically so that resolution is instant and requires no manual configuration work.
- **Acceptance Criteria**:
  - Given an approved task, when the workflow receives the approval, then it calls the SuccessFactors Role-Based Permissions API and applies the recommended change within 2 minutes.
  - Given a failed write operation, when the API call fails, then the workflow notifies the HR Admin and does not silently discard the approved change.
- **Maps to Objective**: Objectives 2 and 3
- **Priority Rank**: 3

**REQ-04: Audit Log for All Permission Changes**

- **Problem to Solve**: There is no structured record of who requested, who approved, and what was changed — making compliance audits manual and unreliable.
- **User Story**: As a Compliance Officer, I need a complete audit log of all access requests, AI recommendations, approval decisions, and applied changes so that I can demonstrate compliance to auditors.
- **Acceptance Criteria**:
  - Given any request lifecycle event (submission, recommendation, approval/rejection, change applied), when the event occurs, then a timestamped entry is written to the audit log with actor identity, action type, and relevant details.
  - Given a compliance audit request, when the officer queries the log, then all entries for the requested period are retrievable.
- **Maps to Objective**: Objectives 3 and 4
- **Priority Rank**: 4

**REQ-05: Periodic RBP Compliance Reports**

- **Problem to Solve**: Compliance reporting on RBP is done manually and infrequently, leaving SoD conflicts and excessive permissions undetected for months.
- **User Story**: As a Compliance Officer, I need automated periodic reports covering SoD conflicts, permission change history, and SAP best practice deviations so that I can identify and act on compliance risks proactively.
- **Acceptance Criteria**:
  - Given the report schedule (quarterly by default), when the reporting cycle triggers, then a report is generated covering: SoD conflict flags, list of permission changes in the period, and any deviations from SAP best practices.
  - Given a generated report, when it is complete, then it is delivered to the Compliance Officer by email and/or Microsoft Teams.
- **Maps to Objective**: Objective 4
- **Priority Rank**: 5

**REQ-06: SuccessFactors UI Accessibility**

- **Problem to Solve**: Employees and managers do not know where to go to report an access issue and should not have to leave SuccessFactors to do so.
- **User Story**: As an employee, I need to access the RBP assistant directly within SAP SuccessFactors so that I can report an issue without switching systems.
- **Acceptance Criteria**:
  - Given a SuccessFactors session, when the user opens the Joule assistant panel, then they can interact with the RBP Access & Compliance Manager agent.
- **Maps to Objective**: Objective 1
- **Priority Rank**: 6

### High-Want Requirements

**REQ-07: Request Status Tracking**

- **Problem to Solve**: Requesters have no visibility into whether their access issue is being investigated, pending approval, or resolved.
- **User Story**: As an employee, I need to see the current status of my access request so that I do not need to chase an HR Admin for updates.
- **Priority Rank**: 1

**REQ-08: Approver Notification via Microsoft Teams**

- **Problem to Solve**: HR Admins and Compliance Officers may not check Task Center immediately; a Teams notification speeds up response.
- **User Story**: As an HR Administrator, I need a Teams message notifying me of a pending approval task so that I can act on it promptly.
- **Priority Rank**: 2

### Nice-to-Have Requirements

**REQ-09: Self-Service Compliance Report on Demand**

- **Problem to Solve**: Compliance Officers occasionally need an ad-hoc report outside the scheduled cycle.
- **User Story**: As a Compliance Officer, I need to trigger a compliance report on demand so that I can respond to unplanned audit requests.
- **Priority Rank**: 1

---

## Non-Functional Requirements

### Performance
- **Latency**: AI agent must return a diagnosis and recommendation within 30 seconds of submission for 95% of requests.
- **Throughput**: The solution must support up to 200 concurrent access requests per day.

### Reliability
- **Availability**: The solution must be available during standard business hours (99.5% uptime).
- **Fallback**: If the SuccessFactors RBP API is unavailable, the agent must notify the requester and queue the request for retry.

### Explainability
- **Traceability**: Every AI recommendation must reference the specific permission group, role assignment, and API response data that informed it.
- **Decision Logging**: All agent reasoning steps, approval decisions, and write operations must be logged.
- **Uncertainty Communication**: If the agent cannot produce a confident recommendation, it must say so explicitly and suggest escalation to an HR Admin.

---

## Solution Architecture

**Architecture Overview:**
Three integrated components deployed on SAP BTP: a Python AI Agent (A2A protocol) for intelligent investigation, an n8n Approval Workflow for orchestration and write-back, and a custom MCP Server exposing SuccessFactors APIs. A lightweight CAP service provides the audit log store.

**Key Components:**

- **AI Agent (Python/A2A)**: Accepts access issue descriptions, investigates using SuccessFactors APIs via MCP tools, and returns a structured diagnosis and recommendation. Surfaced via Joule in SuccessFactors.
- **n8n Approval Workflow**: Receives the agent's recommendation via webhook, creates a SAP Task Center approval task, listens for the decision, and — on approval — calls the SuccessFactors RBP API to apply the change. Triggers compliance report generation on schedule.
- **Custom MCP Server**: Exposes the following SuccessFactors APIs as MCP tools: Role-Based Permissions (read/write), RBP GenAI Troubleshooting, User Management, Common Platform (Foundation), and SCIM.
- **CAP Audit Log Service**: Persists all request lifecycle events (submission, recommendation, approval/rejection, applied change) to a BTP-hosted database. Provides a query interface for compliance reporting.

**Integration Points:**

- SAP SuccessFactors (RBP GenAI, Role-Based Permissions, User Management, Common Platform, SCIM APIs) — bidirectional, event-driven
- SAP Task Center — write (create task), read (approval decision)
- Microsoft Outlook / Teams — write (send notification), outbound only

**Deployment Environments:**

- Development and Production environments on SAP BTP Cloud Foundry; audit data isolated per environment.

### Agent Extensibility & Instrumentation

**Agent Extensibility:**
The AI Agent must be designed with extension points to allow future capabilities to be added without re-architecting the core:
- New MCP tools (e.g. additional SuccessFactors modules) can be registered without modifying the agent's core logic
- The agent's system prompt and knowledge scope must be externalised as configuration, not hardcoded
- The approval workflow invocation is handled via an MCP tool call (not a direct HTTP call), allowing the workflow to evolve independently

**Business Step Instrumentation:**
All five key business milestones must emit structured log statements to enable observability and monitoring in production. Log format: `[MILESTONE_ID].[achieved|missed]: [description]`.

### Automation & Agent Behaviour

**Automation Level:** Hybrid — AI-assisted investigation with rule-based approval routing and automated write-back post-approval.

**Actions the system performs without human approval:**
- Investigating the access issue and reading permission data from SuccessFactors
- Generating a diagnosis and recommendation
- Logging the request to the audit store
- Triggering the compliance report generation on schedule

**Actions that require human review or approval:**
- Applying any permission change to a user's SuccessFactors profile (always requires Task Center approval)
- Escalating unresolvable issues to an HR Admin

**Model / engine used:** SAP Generative AI Hub (via SuccessFactors RBP GenAI Troubleshooting API and SAP AI Core for agent reasoning).

**Knowledge & data sources accessed:**
- SAP SuccessFactors RBP GenAI Troubleshooting API — AI-powered diagnosis of RBP issues
- SAP SuccessFactors Role-Based Permissions API — read current assignments; write approved changes
- SAP SuccessFactors User Management API — resolve user identity and current role context
- SAP SuccessFactors Common Platform API — access foundation/organisational data
- SAP SuccessFactors SCIM API — identity alignment
- CAP Audit Log Service — write all lifecycle events; read for compliance reports

**Tools or connectors invoked:**
- `get_rbp_issue_diagnosis` (MCP tool — RBP GenAI API): investigates the access issue; read-only
- `get_user_permissions` (MCP tool — RBP API): reads current permission group assignments; read-only
- `get_user_profile` (MCP tool — User Management API): resolves user identity; read-only
- `apply_permission_change` (MCP tool — RBP API): writes an approved permission assignment; **high-risk write — only called post-approval**
- `rbp-approval-workflow` workflow (via `submit_for_approval` MCP tool): triggers the n8n approval workflow with the diagnosis and recommendation

**Guardrails & fail-safes:**
- The agent must never call `apply_permission_change` autonomously — only the n8n workflow calls this tool after receiving an explicit Task Center approval
- If the diagnosis confidence is low, the agent must escalate to a human rather than produce a speculative recommendation
- All write operations must be idempotent — re-applying an already-applied change must not produce duplicate assignments
- If the SuccessFactors API is unavailable, the agent must notify the requester and queue the request; it must not silently fail

### Error Handling (per SAP custom node)

| Node (business step) | On error | Error-path action |
|---|---|---|
| SAP MCP Client — read permissions | Continue on error path | Notify requester that investigation could not complete; log the failure |
| SAP Task Center — approval task | Stop the workflow | HR Admin is notified via email that the task could not be created |
| SAP MCP Client — apply permission change | Continue on error path | Notify HR Admin via Teams/email that the approved change failed to apply; retain in queue for retry |

---

## Governance, Risk & Compliance

**Data Handling:**
- No PII beyond what SuccessFactors already holds (user ID, role, permission group); no additional PII is stored in the audit log beyond what is needed for traceability.
- Audit log entries are retained for a minimum of 3 years to support compliance audits.

**Compliance Frameworks:**
- Aligns to SAP SuccessFactors RBP best practices (Segregation of Duties, least-privilege principle)
- Supports internal access governance audit requirements

**Approval Flows:**
- All permission changes require documented Task Center approval before being applied
- Approval decisions (approve/reject + approver identity + timestamp) are immutably logged

---

## Milestones

### M1: Issue Submitted

- **Description**: The requester has submitted an RBP access issue or permission request to the AI agent.
- **Achieved when**: The agent receives a valid issue description and begins investigation.
- **Log on achievement**: `M1.achieved: RBP access issue submitted by user {user_id}, request_id={request_id}`
- **Log on miss**: `M1.missed: Issue submission did not complete — no valid input received`

### M2: AI Investigation Complete

- **Description**: The AI agent has produced a diagnosis and a recommended permission change.
- **Achieved when**: The agent returns a structured recommendation with justification.
- **Log on achievement**: `M2.achieved: Diagnosis complete for request_id={request_id}, recommended_group={group_name}`
- **Log on miss**: `M2.missed: Agent could not produce a recommendation for request_id={request_id} — escalating to HR Admin`

### M3: Approval Task Sent

- **Description**: The n8n workflow has created a SAP Task Center approval task and notified the approver.
- **Achieved when**: The Task Center task is successfully created and the approver is notified.
- **Log on achievement**: `M3.achieved: Approval task created for request_id={request_id}, approver={approver_id}`
- **Log on miss**: `M3.missed: Approval task could not be created for request_id={request_id}`

### M4: Permission Change Applied

- **Description**: The approved permission change has been successfully written to SAP SuccessFactors.
- **Achieved when**: The RBP API write call returns a successful response and the assignment is confirmed.
- **Log on achievement**: `M4.achieved: Permission change applied for user_id={user_id}, group={group_name}, request_id={request_id}`
- **Log on miss**: `M4.missed: Permission change could not be applied for request_id={request_id} — manual intervention required`

### M5: Audit Entry Recorded & Compliance Report Generated

- **Description**: The full request lifecycle is logged and the next compliance report cycle is updated.
- **Achieved when**: The audit log entry is persisted and (on schedule) the compliance report is generated and delivered.
- **Log on achievement**: `M5.achieved: Audit entry persisted for request_id={request_id}; compliance report delivered to {recipient}`
- **Log on miss**: `M5.missed: Audit log write failed for request_id={request_id} — data integrity risk`

---

## Risks, Assumptions, and Dependencies

### Risks

- **RBP API write scope**: Overly broad write permissions in the MCP server configuration could allow unintended changes. Mitigation: scope the write tool tightly to the minimum required permission operations.
- **No native audit trail API**: The absence of a native SuccessFactors audit API means the custom audit log is the only source of truth. If it fails, compliance evidence is lost.
- **Joule/SuccessFactors UI embedding**: Surfacing the agent in SuccessFactors via Joule may require additional licensing or configuration not yet confirmed.

### Assumptions (Validate These)

- The SuccessFactors RBP GenAI Troubleshooting API is accessible with the current tenant's API credentials.
- SAP Task Center is configured and active for the HR Administrator and Compliance Officer roles.
- The Role-Based Permissions API supports write operations for permission group assignments in this tenant.

### Dependencies

- SAP SuccessFactors tenant with RBP GenAI, Role-Based Permissions, User Management, and Common Platform API access
- SAP Task Center service configured on BTP
- Microsoft Teams or Outlook connectivity from the n8n instance
- SAP BTP Cloud Foundry space for deploying the agent, MCP server, and CAP audit service

---

## Open Questions

All previously open questions have been resolved:

- **Joule embedding**: Confirmed — the agent will be surfaced in SAP SuccessFactors via Joule.
- **Approval model**: Single approver — either the HR Administrator or the Compliance Officer (whichever is assigned). No dual sign-off required.
- **Compliance report cadence**: Fixed quarterly schedule.
