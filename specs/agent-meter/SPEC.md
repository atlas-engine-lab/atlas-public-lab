# Agent Meter - Product Spec (v0)

## Problem
Agent builders lack a cheap, programmable quality gate for response usefulness before shipping outputs to users.

## Hypothesis
If we provide a low-latency API that scores usefulness and flags non-actionable outputs, agent teams will integrate it as a pre-send guardrail and pay per request once usage scales.

## Why agents would pay
- Reduces bad outputs reaching users
- Saves human review time
- Easy integration in agent pipelines
- Works as a universal QA layer across tasks

## MVP scope
- API: `/v1/validate` returning usefulness score + issue flags
- Free tier: limited daily usage
- Transparent scoring rules

## Validation status
- Prototype implemented in `atlas-sandbox/tools/agent-meter`
- Public spec published
- Revenue validation pending first external integrations

## First monetization path
- Keep limited free request quota
- Introduce paid per-request API using x402/USDC-compatible rail when approved infrastructure is ready
- Price anchor: low cents per validation call

## Next test
- Get 3 agent builders to run 20+ requests each
- Measure repeat usage and issue-resolution lift
- Decide keep/pivot based on repeat usage + paid intent
