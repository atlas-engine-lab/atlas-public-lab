# Before/After Failure Example

## Scenario
Agent workflow calls `fetch_customer_balance` before generating payment reminders.

## Before (failure state)
### Tool definition issues
- permission: `all`
- inputSchema.required missing `customer_id`
- outputSchema type: `string`

### Observed failure
- Agent sends tool call without customer_id
- Tool returns free-form string
- Downstream reminder generator expects structured fields and fails
- Incident: queue retry storm + manual intervention

## After (fixed state)
### Tool definition fixes
- permission: `billing:read:customer_balance`
- inputSchema.required: `["customer_id"]`
- outputSchema:
  - type: object
  - required: `customer_id`, `balance_usd`, `currency`

### Result
- Invalid calls blocked pre-runtime
- Deterministic response contract for downstream tools
- Retry storm eliminated in this path

## Why this matters commercially
One prevented chain failure can save more than the diagnostic fee in engineer time and incident cost.
