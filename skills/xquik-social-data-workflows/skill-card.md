# Skill Card

## Description

Xquik Social Data Workflows helps agents use Xquik REST or MCP to retrieve, monitor, and export public X data for agent workflows.

This skill is for development and production integration guidance when the user already has Xquik access.

## Owner

Xquik-dev

## License/Terms of Use

MIT source repository: `https://github.com/Xquik-dev/x-twitter-scraper`

## Use Case

Use this skill when an AI agent, backend service, or workflow automation needs authenticated access to Xquik REST or MCP for public X data retrieval, monitoring, extraction, and analysis.

## Deployment Geography for Use

Global, subject to the user's Xquik account access, local laws, organization policy, and platform terms.

## Known Risks and Mitigations

Risk: Credential disclosure through prompts, logs, commits, or shared transcripts.

Mitigation: Use environment variables or approved secret stores. Never print, commit, or display real API keys, OAuth tokens, cookies, or account credentials.

Risk: Endpoint behavior drifts from a copied example.

Mitigation: Verify paths and parameters against `https://xquik.com/openapi.json` or `https://docs.xquik.com/openapi.yaml` before executing.

Risk: Accidental write actions from a read workflow.

Mitigation: Keep this skill read-oriented. Require explicit user intent and confirmation before write actions.

Risk: Overcollection of public social data.

Mitigation: Use narrow queries, explicit limits, time windows, and field minimization.

## References

- `https://github.com/Xquik-dev/x-twitter-scraper`
- `https://xquik.com/openapi.json`
- `https://docs.xquik.com/mcp/overview`
- `https://xquik.com/.well-known/mcp.json`

## Skill Output

The skill produces endpoint plans, safe REST or MCP call patterns, normalized result summaries, and follow-up instructions for pagination, retries, exports, monitors, or event processing.

## Skill Version

Initial community catalog contribution.

## Ethical Considerations

Use only authorized Xquik access. Respect privacy, platform terms, applicable law, organizational policy, and user consent. Do not use this skill to bypass access controls or to collect more data than the stated task requires.
