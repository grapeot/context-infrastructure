## 元数据

- **类型**: Workflow
- **分类**: Workflow
- **适用场景**: Handle production incidents — triage, mitigate, communicate, and write postmortems.
- **上游来源**: [incident-response](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/incident-response)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Incident Response

Handle production incidents systematically.

## Severity Levels

| Level | Definition | Response Time | Examples |
|-------|-----------|---------------|----------|
| SEV1 | Service down, all users affected | Immediate | Database crash, DNS failure, auth broken |
| SEV2 | Major feature broken, many users affected | < 30 min | Payments failing, search not working |
| SEV3 | Minor feature broken, workaround exists | < 4 hours | Export button broken, slow dashboard |
| SEV4 | Cosmetic or low-impact issue | Next business day | Typo in UI, minor styling bug |

## Incident Workflow

### 1. Detect & Triage (first 5 minutes)

- Acknowledge the incident — "I'm looking into this"
- Determine severity level
- Check monitoring dashboards (error rates, latency, status page)
- Check recent deployments: `git log --oneline -10` — was anything deployed recently?

### 2. Mitigate (next 15-30 minutes)

**The goal is to stop the bleeding, not find the root cause.**

Quick mitigations:
- **Rollback**: `git revert <commit> && deploy` — fastest option if a deploy caused it
- **Feature flag**: Disable the broken feature
- **Scale up**: Add more instances if it's a capacity issue
- **Failover**: Switch to backup/secondary if primary is down
- **Block traffic**: Rate-limit or block specific abusive traffic

### 3. Communicate

**Internal:**
- Open an incident channel (`#incident-2026-04-10`)
- Post status updates every 15-30 minutes
- Assign roles: Incident Commander, Communicator, Engineers

**External:**
- Update status page
- Send email/notification to affected users if the outage is extended
- Be honest: "We're experiencing issues with X. We've identified the cause and are working on a fix."

### 4. Resolve

- Deploy the fix
- Verify the fix works in production (check metrics, not just absence of errors)
- Close the incident channel with a summary

### 5. Postmortem (within 48 hours)

Write a blameless postmortem:

```markdown
# Incident: Payments failing for Stripe webhook
**Date:** 2026-04-10
**Duration:** 45 minutes (14:30 — 15:15 UTC)
**Severity:** SEV2
**Impact:** ~200 users unable to complete purchases

## Timeline
- 14:30 — Alert fires: payment success rate drops to 20%
- 14:35 — On-call engineer acknowledges, begins investigation
- 14:40 — Identified: Stripe webhook endpoint returning 500
- 14:45 — Root cause: migration added NOT NULL column without default
- 14:50 — Fix deployed: added default value to migration
- 15:00 — Payment success rate recovering
- 15:15 — Metrics back to normal, incident closed

## Root Cause
Database migration #47 added a `currency` column with NOT NULL 
but no DEFAULT value. Existing rows were fine (backfilled), but 
new webhook events failed because the insert didn't include `currency`.

## What Went Well
- Alert fired within 5 minutes of the issue starting
- Rollback was considered but the fix was faster

## What Went Wrong
- Migration wasn't tested with live webhook payloads
- No staging test for the webhook flow

## Action Items
- [ ] Add webhook integration test to CI (@alice, due 2026-04-17)
- [ ] Require DEFAULT for all new NOT NULL columns in migration review (@bob)
- [ ] Add runbook for payment failures (@charlie, due 2026-04-14)
```

## Tips

- Rollback first, investigate later — speed matters more than elegance
- The most recent deploy is the most likely cause
- Don't assign blame in postmortems — focus on process improvements
- Maintain a runbook for common failure modes
- Practice incident response with game days before real incidents happen
