---
name: compliance-reporting
description: Generates quarterly RBP compliance reports including Segregation of Duties (SoD) analysis, permission change history, and SAP best practice deviation detection. Load this skill when the user requests a compliance report or audit.
---

# RBP Compliance Report Generation

## When to Use This Skill

Load this skill when a user requests a compliance report — for example: "Generate the quarterly RBP compliance report", "Show me any SoD conflicts", or "I need an audit report of permission changes".

## Prerequisites

- Confirm the reporting period (default: current quarter)
- Confirm the recipient (default: Compliance Officer and HR Administrator)

## Instructions

### Step 1: Fetch All Users and Permission Assignments

Use the Role-Based Permissions MCP tool to retrieve all users and their current permission group assignments. Set page size to 100 and paginate through all results.

### Step 2: Detect Segregation of Duties (SoD) Conflicts

For each user, check for the following high-risk permission group combinations:
- Create + Approve in the same module (e.g. Create Purchase Order + Approve Purchase Order)
- Compensation planning + Compensation approval for the same group
- Payroll input + Payroll approval
- Any user with both a standard employee group AND a broad admin group

Flag each conflict with:
- User ID
- Conflicting permission groups
- Risk level: High (direct financial impact), Medium (data integrity risk), Low (access scope too broad)

### Step 3: Retrieve Change History from Audit Log

Use the Audit Log MCP tool to retrieve all `permission_change_applied` and `recommendation_rejected` events for the reporting period. For each entry record:
- Request ID
- Affected user ID
- Permission group changed
- Change type (assign/revoke)
- Approver ID
- Timestamp

### Step 4: Check for SAP Best Practice Deviations

Review the permission assignments against SAP SuccessFactors RBP best practices:
- No end user should have a system admin or super admin permission group
- Every employee should have at least the Employee Self-Service (ESS) group
- Manager groups should only be assigned to users with direct reports
- Broad data access groups (e.g. View All Employees) should be restricted to HR roles only

List any deviations found with the user ID and the specific deviation.

### Step 5: Compile the Report

Structure the report as follows:

```
## RBP Compliance Report — [Quarter] [Year]
Generated: [timestamp]

### Summary
- Total users reviewed: X
- SoD conflicts detected: X (High: X, Medium: X, Low: X)
- Permission changes in period: X
- Best practice deviations: X

### SoD Conflicts
[Table: User ID | Conflicting Groups | Risk Level | Recommended Action]

### Permission Change History
[Table: Date | User ID | Group | Change Type | Approver | Request ID]

### Best Practice Deviations
[Table: User ID | Deviation | Recommended Fix]

### Recommended Actions
[Prioritised list of actions based on findings]
```

### Step 6: Deliver the Report

Present the report summary to the user in the chat. Note that the full report has been queued for email delivery to the Compliance Officer and HR Administrator.

## Error Handling

- If permission data retrieval fails: report the error and note the report is incomplete
- If audit log is unavailable: include a note in the report that change history could not be retrieved
- Never fabricate user counts, conflict counts, or permission data
