# RBP Access & Compliance Manager

SAP SuccessFactors Role-Based Permission investigation, resolution, approval workflow, and compliance reporting solution.

## Business Challenge

Businesses struggle with RBP (Role-Based Permission) access issues in SAP SuccessFactors. End users and HR administrators don't know where to look or what permissions to grant. The goal is to investigate and resolve access issues quickly, enforce a human-in-the-loop approval before any permission change is applied, automatically implement approved changes, and deliver RBP audit and compliance reports based on SAP best practices.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Average time to resolve an RBP access issue | — | Reduce by 70% | — | RBP Access Issue Resolution | agent-derived |
| Permission changes requiring manual admin effort | — | 0% (fully automated post-approval) | — | Permission Change Management | agent-derived |
| RBP audit compliance coverage | — | 100% of users reviewed per cycle | Quarterly | RBP Compliance Reporting | agent-derived |
| Segregation of Duties (SoD) conflicts identified | — | Detect 100% of flagged conflicts | — | Access Governance | agent-derived |

## Key Milestones

1. **Issue Submitted** — Employee, HR admin, or manager submits an RBP access issue or permission request via SAP SuccessFactors UI
2. **AI Investigation Complete** — The AI agent analyses the issue using the RBP GenAI Troubleshooting API and RBP permissions data, produces a diagnosis and recommended permission change
3. **Approval Task Sent** — The approval workflow routes the recommendation to the HR Administrator and/or Security/Compliance team via SAP Task Center
4. **Change Applied** — The approved permission change is automatically applied in SAP SuccessFactors via the Role-Based Permissions API
5. **Audit Recorded** — All actions are logged; periodic compliance reports (SoD analysis, change history, best practice deviations) are generated and available

## Business Architecture (RBA)

### End-to-End Process

Governance → Manage Governance, Risk and Compliance (generic)

### Process Hierarchy

```
Governance (E2E)
└── Manage Governance, Risk and Compliance (generic)
    └── Manage Identity and Access Governance (BPS-399)
        └── Manage access governance and authorisations
        └── Manage authentication
        └── Manage identity
    └── Manage Enterprise Risk and Compliance (BPS-398)
        └── Manage audits and assurance
```

### Summary

The challenge maps to the Manage Identity and Access Governance sub-process (BPS-399) covering access governance and authorisations, with compliance reporting covered by Manage Enterprise Risk and Compliance (BPS-398), both under the Governance E2E.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Gap? | Notes / assumptions |
|---|---|---|---|---|---|---|---|---|
| Investigate RBP access issues using AI | RBP GenAI Troubleshooting API (SAP SuccessFactors) | `sap.sf:apiResource:PLTRBPGenAI:v1` | — | — | — | — | No | Available in landscape; custom MCP server required to expose it to the agent |
| Read and query RBP permissions | Role-Based Permissions API (SAP SuccessFactors) | `sap.sf:apiResource:PLTRoleBasedPermissions:v1` | — | — | — | — | No | Available; custom MCP server required |
| Read user profile data | User Management API (SAP SuccessFactors) | `sap.sf:apiResource:PLTUserManagement:v1` | — | — | — | — | No | Available; custom MCP server required |
| Common platform / foundation data | Common Platform APIs (SAP SuccessFactors) | `sap.sf:apiResource:FoundationPlatformPLT:v1` | — | — | — | — | No | Available; custom MCP server required |
| SCIM-based identity provisioning | SCIM for SuccessFactors Workforce | `sap.sf:apiResource:PLTScim:v2` | — | — | — | — | No | Available; used for identity management alignment |
| Human-in-the-loop approval workflow | SAP Task Center (n8n node CUSTOM.sapTaskCenter) | — | — | — | — | — | No | SAP Task Center node available on this n8n instance |
| Notification on approval task | Microsoft Outlook / Teams (n8n nodes) | — | — | — | — | — | No | Both available on this n8n instance |
| Audit trail and change logging | Security Audit Log API, Audit Trail API | — | — | — | — | — | Yes | Unavailable in this landscape; audit log must be maintained within the solution (custom store) |
| RBP compliance audit reporting | SAP Cloud Identity Access Governance (IAG) | — | — | — | — | — | Maybe | IAG provides native access governance; if not licensed, custom reporting from API data is required |
| Automatically apply approved permission changes | Role-Based Permissions API (write) | `sap.sf:apiResource:PLTRoleBasedPermissions:v1` | — | — | — | — | No | API supports write operations; custom MCP server tool required |
| Embedded SuccessFactors UI experience | SAP SuccessFactors extensibility | — | — | — | — | — | Maybe | Agent can be surfaced via Joule in SuccessFactors; UI embedding scope to confirm |

### Key findings

- SAP SuccessFactors provides a dedicated **RBP Generative AI Troubleshooting API** (`PLTRBPGenAI:v1`) — a strong foundation for the AI investigation capability that avoids building analysis logic from scratch.
- No pre-built MCP servers exist for any of the SuccessFactors APIs; a **custom MCP server** must be built to expose RBP, User Management, and Common Platform APIs to the AI agent.
- **Audit trail APIs are unavailable** in this landscape; the solution must maintain its own change log (e.g. in a CAP service or database).
- SAP Task Center node (`CUSTOM.sapTaskCenter`) is available on this n8n instance, enabling the human-in-the-loop approval step natively in the workflow.
- The solution requires three integrated components: an **AI Agent** (investigation & recommendation), an **n8n Workflow** (approval orchestration & write-back), and a **custom MCP Server** (SuccessFactors API access).
- Microsoft Outlook and Teams notification nodes are available, enabling multi-channel approver notification.

## Recommendations

### RBP Access & Compliance Manager

#### Executive Summary

AI-driven RBP investigation, approval workflow, and compliance reporting for SAP SuccessFactors.

#### Recommended Solution

A three-component solution built on SAP Build:

1. **AI Agent (Python/A2A)**: Accepts an RBP access issue in natural language, investigates using the SuccessFactors RBP GenAI Troubleshooting API and Role-Based Permissions API, and returns a structured diagnosis with a recommended permission change.
2. **n8n Approval Workflow**: Receives the agent's recommendation, routes an approval task to the HR Administrator and/or Security/Compliance team via SAP Task Center, and — once approved — automatically applies the permission change via the RBP API. Maintains an audit log of all changes.
3. **Custom MCP Server**: Exposes the SAP SuccessFactors RBP, User Management, Common Platform, and SCIM APIs as MCP tools for the AI agent to call.

Compliance reports (SoD analysis, change history, best practice deviations) are generated periodically by the workflow and delivered via email/Teams.

#### Problem Statement

HR administrators and end users in SAP SuccessFactors cannot easily diagnose or resolve RBP access issues. The permission structure is complex, changes are risky without oversight, and there is no automated way to audit compliance against SAP best practices.

#### Affected User Roles

- **Employees** — submit access issues or permission requests
- **HR Administrators** — approve/reject permission change recommendations
- **Security / Compliance team** — approve sensitive changes, consume audit reports
- **Managers** — submit requests on behalf of their team

#### Important Factors

##### Reduces manual effort through AI-driven investigation
The RBP GenAI Troubleshooting API provides built-in intelligence for diagnosing permission issues, significantly reducing the effort required to identify the root cause and the correct permission group to assign.

##### Human oversight preserved through Task Center approval
All permission changes must pass through an explicit approval task before being applied, ensuring no uncontrolled changes are made and maintaining an auditable decision trail.

##### Audit log must be custom-built
Since the native Audit Trail API is unavailable in this landscape, a lightweight audit store (e.g. CAP service) is needed to record all submitted requests, recommendations, approvals, and applied changes.

#### Potential Risks

##### MCP server complexity for SuccessFactors APIs
No pre-built MCP servers exist for SuccessFactors APIs; a custom MCP server must be developed and maintained. Authentication and API version management add complexity.

##### RBP API write capability scope
Automated application of permission changes via the RBP API requires careful scoping. Overly broad write permissions in the API configuration could introduce security risks.

##### UI embedding dependency
Embedding the agent experience into the SAP SuccessFactors UI depends on Joule availability and SuccessFactors extensibility options, which may require additional licensing or configuration.

#### Recommended solution category

AI Agent, n8n Workflow, MCP Server

#### Intent fit
85%
