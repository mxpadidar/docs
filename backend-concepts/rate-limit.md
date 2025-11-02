# Rate Limits — Reference

## Purpose
Rate limiting protects service availability, prevents abuse, and ensures fair resource usage. This document defines terminology, policies, algorithms, enforcement points, client guidance, and practical examples for implementing rate limits across the system.

## Principles
- Fail fast and clear: return HTTP 429 + Retry-After when limits are exceeded.
- Document limits for clients so behavior is predictable.
- Protect sensitive endpoints (auth, token rotation, password reset) with stricter limits.
- Prefer stateless, short-lived access tokens and server-controlled refresh flows rather than DB checks on every request.

## Terminology
- Rate limit: allowed number of operations within a window.
- Window: time span for counting requests (fixed or sliding).
- Quota: longer-term allowance (daily, monthly).
- Burst: short permitted spike above sustained rate.
- Cooldown/lock: temporary block after violations.
- Jitter: randomized delay to avoid synchronized retries.

## Types of Limits
- Global per-IP — mitigates DDoS and abusive networks.
- Per-user (authenticated) — limits by user id.
- Per-session — tied to session_uuid / jti (useful for refresh-token rotation throttling).
- Per-endpoint — apply stricter rules on sensitive endpoints (login, ticket creation, refresh).
- Per-client-id — for OAuth clients or API keys.
- Concurrency limits — max parallel operations (optional).

## Algorithms (overview)
Choose an algorithm by trade-offs between simplicity, accuracy, and storage cost:

- Fixed window: simple counters per window (e.g., 100/min). Fast but allows edge bursts.
- Sliding window log: exact counts by recording timestamps. Accurate but storage-heavy.
- Rolling/sliding counter: approximation using two adjacent windows — smoother than fixed window.
- Token bucket: supports steady rate plus bursts; refill at rate r and consume tokens per request.
- Leaky bucket: smooths bursts into a steady drain.
- Rate-limited queue: queue requests instead of rejecting (rare for public HTTP APIs).

## Recommended Defaults (examples)
Adjust to product needs; these are starting suggestions for auth flows:
- Login / auth-ticket creation: 5–10 requests per 10 minutes per IP or client_id.
- OTP send (SMS/email): 3 per hour per account/IP; 5 per day per account.
- Refresh-token rotation: 3–10 rotations per minute per session (with session lock on abuse).
- Password reset requests: 3 per hour per account/IP.
- General API (protected): 100–1000 per minute per user depending on endpoint.

## Enforcement Pattern (server-side)
1. Identify the rate key: ip, user_id, session_uuid, client_id, endpoint, or a composite key.
2. Atomically check the rate store (Redis recommended).
3. If allowed, increment/update counters and proceed.
4. If exceeded, return 429 with Retry-After and structured body:
   { "error": "rate_limited", "retry_after": N }
5. Log the event for monitoring, analytics, and possible escalation (CAPTCHA, temporary lock).

## Atomicity & Implementation Notes
- Use atomic operations to avoid race conditions:
  - Redis: INCR + EXPIRE, Lua scripts, token-bucket scripts.
  - SQL: SELECT ... FOR UPDATE then UPDATE (heavier, higher latency).
- For token buckets, use integer arithmetic and timestamps inside an atomic script.

## Storage Choices
- Redis (recommended): low latency, TTL support, Lua scripting. Keys examples:
  - rl:ip:{ip}:{endpoint}
  - rl:user:{user_id}:{endpoint}
  - rl:sess:{session_uuid}:{rule}
- Relational DB: use for quotas/audits, not per-request checks.
- Hybrid: Redis for real-time enforcement, DB for durable audit & reporting.

## Per-Session Rotation Rate-Limiting (practical)
- Keep per-session state: rotate_count, rotate_window_start, locked_until (in DB or Redis).
- On a rotation request:
  - Atomically check the window and increment rotate_count.
  - If count > limit: set locked_until (temporary) and reject; optionally escalate to session revoke on repeated abuse.
  - If allowed: proceed, create new refresh token record, and mark previous token as revoked/rotated.
- On revoked-token reuse: revoke the entire session immediately (status = REVOKED), revoke all tokens, and log/alert.

## Client Guidance & Error Responses
- Return 429 when limit exceeded.
- Provide standard headers:
  - Retry-After — seconds until next allowed request.
  - X-RateLimit-Limit — allowed requests in the current window.
  - X-RateLimit-Remaining — remaining requests in window.
  - X-RateLimit-Reset — epoch seconds when window resets.
- Provide a JSON error body:
  { "code": "rate_limited", "message": "...", "retry_after": N }
- Encourage exponential backoff with jitter on clients.

## Locking and Escalation Strategy
- Soft limit → temporary lock (e.g., 5–15 minutes).
- Repeated violations → longer lock or full session revoke and force re-authentication.
- Differentiate benign bursts (legitimate client behavior) from malicious reuse: on token replay, prefer immediate session revoke.

## Monitoring & Alerting
- Track metrics: count of 429 responses, lock events, top offenders (IP/user), and trend anomalies.
- Alert on high 429 rate spikes, many locked sessions, or sudden changes in rejected traffic.
- Provide dashboards for QPS, latencies, and rejected request rates per endpoint.

## Auditing & Logging
- Log keys, endpoint, policy name, check result, client_id, user_id/session_uuid where applicable.
- For security incidents (token reuse or forced revocation), log full context: ip, user agent, metadata for forensic analysis.

## Testing
- Unit tests for algorithm correctness.
- Integration tests to simulate bursts and verify counters and resets.
- Load/chaos tests to validate behavior under Redis failures and high concurrency.
- Define fallback behavior when the rate store is unavailable (fail-open vs fail-closed). For sensitive endpoints prefer fail-closed or stricter fallback limits.

## Data Retention & Privacy
- Keep counters short-lived; use TTL to purge keys automatically.
- Avoid storing PII in rate keys or logs; if required, hash identifiers.
- Limit retention of logs containing user identifiers per privacy policy.

## Security Considerations
- IP limits are imperfect under NAT; combine with per-user, per-client limits.
- Use CAPTCHAs or progressive friction when suspicious patterns are detected.
- Prevent clients from forging rate keys (don’t accept session_uuid as a key without validation).

## Configuration & Rollout
- Make limits configurable by environment and feature flags.
- Rollout gradually: start conservative, monitor, and relax if safe.
- Offer different limits for paid tiers and trusted clients.

## Example Redis Token-Bucket (concept)
Key: rl:tb:{scope}:{key}
Stored fields: last_ts, tokens
On request (atomic script):
- Compute tokens = min(capacity, tokens + (now - last_ts) * refill_rate)
- If tokens >= 1 -> tokens -= 1, allow and persist last_ts, tokens with TTL
- Else -> reject and return Retry-After

## Final Notes
- Document limits in API docs and developer portal.
- Prefer short access tokens + refresh flows; apply rotation limits on refresh tokens per session.
- Keep the implementation observable, auditable, and easily adjustable.
