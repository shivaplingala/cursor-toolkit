# AWS Diagnose

Local Cursor plugin for **read-only** AWS/SST diagnosis (serverless)
and bundled **Amazon Bedrock AgentCore** skills.

## Install

Already under `~/.cursor/plugins/local/aws-diagnose/` — available in
Cursor with no extra install step. Reload the window if skills/commands do not
appear.

## Commands

| Command | Purpose |
| ------- | ------- |
| `/aws-diagnose` | Read-only AWS/SST diagnosis → `.aws-details/reports/` |
| `/agents-debug` | AgentCore: wrong answers, tool failures, traces/logs, CLI doctor |
| `/agents-build` | AgentCore: memory, VPC, multi-agent, browser, integrate, teardown |
| `/agents-optimize` | AgentCore: evals, online monitoring, observability, cost |
| `/agents-harden` | AgentCore: IAM, auth, secrets, cold start, sessions, quotas |

## Skills

- `aws-diagnose-read` — orchestrated WRAP (`aws_read.py`) + SST scan; never mutates AWS
- `agents-debug` / `agents-build` / `agents-optimize` / `agents-harden` — AgentCore toolkit (from AWS Agents plugin)

When `/aws-diagnose` classifies an **AgentCore** issue, it loads
`skills/aws-diagnose-read/references/agentcore-handoff.md` and routes to the
matching agents skill. Mutating `agentcore add|deploy|…` stays suggest-only
until that handoff skill is active.

## Rules

- `aws-diagnose-readonly` — keep WRAP-only AWS access during diagnose sessions

## License

MIT (plugin scaffolding). Bundled AgentCore skill text originates from the
[AWS Agents](https://github.com/aws/agent-toolkit-for-aws) plugin (Apache-2.0);
retain upstream attribution when redistributing those skill files.
