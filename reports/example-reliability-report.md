# Example Reliability Report (Redacted)

## Client profile
Mid-market automation team operating 14 MCP tools across internal support and billing workflows.

## Executive summary
We identified 3 high-impact reliability risks likely to cause agent-chain failures in production.

## Top 3 failure points

### 1) Critical: Over-broad permission on billing tool
- Evidence: tool permission value `all`
- Risk: unauthorized action surface and accidental destructive execution
- Recommended fix: replace with scoped permission `billing:read:customer_balance`
- Owner: platform engineer
- Priority: P0 (24h)

### 2) Error: Missing required input field in contract
- Evidence: `customer_id` absent from required array
- Risk: nondeterministic runtime behavior and downstream null handling failures
- Recommended fix: enforce required field and schema-level validation gate in CI
- Owner: service owner
- Priority: P0 (24h)

### 3) Warning: Ambiguous output schema for orchestration tool
- Evidence: output type set to string, no structured properties
- Risk: brittle parsing and branch logic failures in multi-tool chains
- Recommended fix: output object schema with explicit fields and required list
- Owner: agent workflow maintainer
- Priority: P1 (72h)

## Proof artifacts
- Contract Validator output JSON
- MCP Schema Tester issue log
- Severity-ranked finding table

## Remediation plan
1. Apply permission scope patch (P0)
2. Add schema required field enforcement (P0)
3. Normalize output schema to object (P1)
4. Add regression scan to pre-deploy gate (P1)

## Expected reliability impact
- Immediate reduction in high-severity failure triggers
- Higher deterministic tool-call success in production chains
