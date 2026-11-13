---
name: rbp-investigation
description: Step-by-step workflow for investigating and diagnosing RBP access issues in SAP SuccessFactors. Load this skill when a user reports they cannot access a module, feature, or action in SuccessFactors.
---

# RBP Access Issue Investigation

## When to Use This Skill

Load this skill when a user reports an access issue in SAP SuccessFactors — for example: "I cannot access the Compensation module", "I get a permission error when trying to approve a leave request", or "My manager cannot see the org chart".

## Prerequisites

Before starting:
- Confirm the user ID of the affected person
- Confirm which module, feature, or action they cannot access
- Confirm the error message if available

## Instructions

### Step 1: Collect Issue Details

Ask the user (if not already provided):
1. The user ID of the affected person (or ask them to confirm their own ID if self-service)
2. The module or feature they cannot access (e.g. Compensation, Performance, Recruiting, Org Chart)
3. Any error message they see
4. Whether this is a new issue or something that worked before

### Step 2: Retrieve User Profile

Use the User Management MCP tool to retrieve the user's profile:
- Get the user's current role, department, job code, and reporting structure
- Confirm the user is active in the system

### Step 3: Call the RBP GenAI Troubleshooting Tool

Use the RBP GenAI Troubleshooting MCP tool with:
- The user's ID
- The module/feature they cannot access
- The error message if available

This returns a diagnosis identifying the likely missing or misconfigured permission group.

### Step 4: Retrieve Current Permission Assignments

Use the Role-Based Permissions MCP tool to read the user's current permission group assignments:
- List all permission groups currently assigned to the user
- Note any groups that are relevant to the reported module

### Step 5: Cross-Reference and Formulate Recommendation

Compare the GenAI diagnosis with the user's current assignments:
- Identify the specific permission group that should be assigned or modified
- Determine the change type: `assign` (add a permission group) or `revoke` (remove one)
- Write a plain-language justification a non-technical approver can understand

### Step 6: Confidence Check

Before proceeding:
- If the diagnosis is clear and a specific permission group is identified → proceed to Step 7
- If the diagnosis is ambiguous or no matching permission group is found → do NOT guess. Tell the user: "I was unable to identify a specific permission fix with confidence. I recommend escalating this to your HR Administrator for manual review." Log `M2.missed`.

### Step 7: Present Recommendation to User

Present the diagnosis and recommended change to the user:
- Explain what the issue is in plain language
- State the recommended permission group change and why
- Ask the user to confirm they want to submit this for approval

### Step 8: Submit for Approval

Once the user confirms:
- Call the `rbpRecommendationSubmitted` MCP tool with the full payload:
  - `request_id`: generate a unique ID (timestamp + user_id)
  - `user_id`: affected user's ID
  - `issue_description`: user's original description
  - `diagnosis`: structured output from the GenAI tool
  - `recommended_group`: name of the permission group
  - `change_type`: `assign` or `revoke`
  - `justification`: plain-language explanation for the approver
- Confirm to the user that their request has been submitted for approval and they will be notified by email when a decision is made

## Error Handling

- If the User Management tool fails: report the error verbatim and ask the user to try again later
- If the RBP GenAI tool fails: fall back to retrieving current permissions manually and presenting them to the user for context
- If the submit-for-approval tool fails: inform the user that submission failed and suggest they contact their HR Administrator directly
