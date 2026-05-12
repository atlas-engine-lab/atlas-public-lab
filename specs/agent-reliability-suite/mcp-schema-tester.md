# MCP Schema Tester - Public Product Spec

## Module goal
Prevent MCP agent chain failures before deployment by deterministically scanning tool schemas.

## Reliability checks
1. Missing required fields
2. Weak tool descriptions
3. Unsafe broad permissions
4. Ambiguous input schema
5. Ambiguous output schema

## Machine-readable output
JSON with:
- `summary.total_issues`
- `summary.critical`
- `summary.error`
- `summary.warning`
- `summary.pass`
- `issues[]` with severity/code/path/message/recommendation

## API contract
`POST /v1/mcp/schema/test`

Request body: MCP schema JSON with `tools[]`

Response body:
```json
{
  "summary": {
    "total_issues": 4,
    "critical": 1,
    "error": 1,
    "warning": 2,
    "pass": false
  },
  "issues": [
    {
      "severity": "critical",
      "code": "unsafe_broad_permission",
      "path": "tools[0].permissions",
      "message": "Permission 'all' appears overly broad",
      "recommendation": "Scope permissions to least privilege"
    }
  ]
}
```

## CLI contract
```bash
python mcp_schema_tester.py --file examples/failing_schema.json
python mcp_schema_tester.py --serve --port 8791
```

## One clear paid-use case
Hosted pre-deploy scan gate for MCP servers in CI. Teams pay per scan to block schema and permission regressions that would otherwise break production agent workflows.

## Revenue path
- Free local CLI
- Paid hosted API scans per request
- x402/USDC billing added later when infra is approved
