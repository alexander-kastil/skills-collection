---
name: xquik-social-data-workflows
description: "Use Xquik REST or MCP to retrieve and inspect public X data for agent workflows."
source: "https://github.com/Xquik-dev/x-twitter-scraper"
risk: safe
license: MIT
allowed-tools: "Network access to Xquik REST, Xquik MCP, and public Xquik documentation only"
---

# Xquik Social Data Workflows

## Overview

Use this skill to plan and execute read-only workflows with Xquik, a real-time X (Twitter) data platform with REST and MCP surfaces. The skill helps agents choose between REST and MCP, discover the right endpoint from the public specification, inspect existing extraction or monitoring results, handle authentication safely, and normalize public X data for downstream analysis.

This skill has no bundled scripts and does not require local file writes. It assumes the user already has Xquik access through an API key or OAuth-enabled MCP client.

## When to Use This Skill

- Use when the user asks an agent to search, retrieve, inspect, or analyze public X data through Xquik.
- Use when building a backend, workflow automation, or AI-agent integration that needs Xquik REST endpoints.
- Use when connecting Claude Code, Codex, Cursor, VS Code, Windsurf, Claude Desktop, Claude.ai, or ChatGPT Developer Mode to Xquik MCP.
- Use when the task needs endpoint discovery from the Xquik OpenAPI spec before making API calls.

## Do Not Use This Skill

- Do not use for posting, liking, following, removing followers, profile edits, or other write actions unless the user explicitly asks for that separate workflow and confirms the connected account context.
- Do not create extraction jobs, monitors, webhooks, exports, or other persistent resources from this read-only skill.
- Do not use to bypass authentication, rate limits, subscription state, legal restrictions, or platform access controls.
- Do not paste, log, commit, or display API keys, OAuth tokens, cookies, or other credentials.
- Do not claim unsupported freshness, coverage, pricing, affiliation, or scraping behavior.

## Capability Boundaries

- **Network:** Only call `https://xquik.com`, `https://docs.xquik.com`, or the authenticated Xquik MCP endpoint needed for the task.
- **Authentication:** Prefer `x-api-key` for REST and MCP clients that support custom headers. Use OAuth 2.1 Bearer auth only when the MCP client handles the browser flow.
- **MCP:** Use `explore` for endpoint discovery and `xquik` for authenticated API calls.
- **Data:** Treat returned X data as user data. Minimize fields, preserve source URLs or IDs, and keep pagination cursors opaque.
- **Writes:** Do not create or modify resources. Route action tasks through a separate, correctly risk-classified workflow with explicit user confirmation.

## Workflow

### 1. Confirm the Job

Identify the user goal before selecting an endpoint:

- Search tweets, users, communities, or lists.
- Read timelines, threads, replies, quotes, media, articles, or trends.
- Inspect existing extraction jobs and their results.
- Read existing monitor events and webhook-delivery history.

If the task can be answered with existing local data, use that first.

### 2. Choose REST or MCP

Use REST when the user needs deterministic programmatic reads, backend integration, pagination control, or HMAC webhook verification.

Use MCP when an AI agent or IDE needs natural language access to the Xquik account. First call `explore` to find the endpoint and required parameters, then call `xquik` with the selected path.

### 3. Verify the Endpoint

Check the current public sources before executing:

- OpenAPI JSON: `https://xquik.com/openapi.json`
- OpenAPI YAML: `https://docs.xquik.com/openapi.yaml`
- MCP overview: `https://docs.xquik.com/mcp/overview`
- MCP discovery: `https://xquik.com/.well-known/mcp.json`

Xquik is an independent third-party service. Not affiliated with X Corp. "Twitter" and "X" are trademarks of X Corp.

Use endpoint paths exactly as documented. Common read surfaces include:

- `GET /api/v1/x/tweets/search`
- `GET /api/v1/x/tweets/{id}`
- `GET /api/v1/x/tweets/{id}/thread`
- `GET /api/v1/x/users/{id}`
- `GET /api/v1/x/users/{id}/tweets`
- `GET /api/v1/x/users/search`
- `GET /api/v1/x/communities/search`
- `GET /api/v1/extractions/{id}`
- `GET /api/v1/events`
- `GET /api/v1/radar`

### 4. Authenticate Safely

For REST, pass the key with an `x-api-key` header. For MCP, use `x-api-key` or OAuth Bearer auth according to the client.

Never print real credentials. Use placeholders in examples and keep secrets in the user's approved secret store or runtime environment.

### 5. Execute with Bounded Reads

Use narrow queries, explicit limits, and time windows. Respect `Retry-After` on `429` responses and retry only `429` and `5xx` failures, with at most 3 attempts.

Keep pagination cursors opaque. Do not decode, modify, or construct cursors manually.

### 6. Normalize the Output

Return results with:

- Query or endpoint used.
- Timestamp of retrieval.
- Result count.
- Next cursor or existing extraction ID when present.
- Selected fields needed by the task.
- Notes for partial data, authentication errors, rate limits, or insufficient access.

## Examples

### Example 1: Search Recent Tweets with MCP

```javascript
async () => {
  return xquik.request("/api/v1/x/tweets/search", {
    query: {
      q: "from:nvidia AI",
      queryType: "Latest",
      limit: "20"
    }
  });
}
```

### Example 2: Search Recent Tweets with REST

```bash
curl "https://xquik.com/api/v1/x/tweets/search?q=from%3Anvidia%20AI&queryType=Latest&limit=20" \
  -H "x-api-key: $XQUIK_API_KEY"
```

### Example 3: Inspect an Existing Extraction

```bash
curl "https://xquik.com/api/v1/extractions/ext_123" \
  -H "x-api-key: $XQUIK_API_KEY"
```

## Best Practices

- Verify endpoint names and parameters against the OpenAPI spec before calling.
- Keep this skill read-only. Move action requests to a separate workflow with an appropriate risk label.
- Prefer targeted queries over broad collection.
- Store only the fields needed for the user's stated task.
- Preserve raw IDs and URLs so downstream systems can trace records.
- Document retry, cursor, and partial-result handling in integration handoffs.

## Limitations

- Requires an Xquik account, API key, OAuth session, or eligible MCP client.
- Does not provide credentials, accounts, subscriptions, or connected X accounts.
- Does not guarantee full historical coverage or unlimited result volume.
- Does not include a local SDK, scripts, or generated client code.
- Does not replace the current OpenAPI spec or product documentation.

## References

- Xquik source: `https://github.com/Xquik-dev/x-twitter-scraper`
- OpenAPI JSON: `https://xquik.com/openapi.json`
- Documentation index: `https://docs.xquik.com/llms.txt`
- MCP overview: `https://docs.xquik.com/mcp/overview`
- MCP discovery: `https://xquik.com/.well-known/mcp.json`
