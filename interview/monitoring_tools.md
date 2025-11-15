# Monitoring & Observability — Tools and Best Practices

Purpose: A standalone primer on observability: metrics, logs, traces, common tools (Prometheus, Grafana, Sentry, ELK/Opensearch, Datadog), and operational best practices.

## Observability signals

- Metrics: numerical, aggregated time-series (latency, error rates, QPS). Use Prometheus for pull-based metrics or pushgateway for short-lived jobs.
- Logs: detailed event records for troubleshooting and audit. Centralize logs (ELK/Opensearch) and index for search.
- Traces: distributed request traces showing timing across services (OpenTelemetry, Jaeger). Useful for latency hotspots and call graphs.

## Common tools

- Prometheus: metrics scraping, dimensional data model, alerting rules.
- Grafana: visualization and dashboards (connects to Prometheus, Elasticsearch, Loki, etc.).
- Alertmanager: works with Prometheus to deduplicate/route alerts to channels (pager, Slack, email).
- Sentry: error aggregation and stack traces for exceptions; integrates with languages, frameworks, and issue trackers.
- ELK / OpenSearch: log ingestion (Logstash/Beats), storage (Elasticsearch/OpenSearch), visualization (Kibana).
- Datadog: commercial APM, metrics, logs and infrastructure monitoring unified.

## Instrumentation & patterns

- Use libraries compatible with OpenTelemetry to collect traces and metrics.
- Semantic metrics: use consistent naming and labels (service, endpoint, method).
- Avoid high-cardinality labels for metrics (user_id, request_id should not be label keys).
- Logging best practices: structured JSON logs with request IDs and severity levels.

## SLIs, SLOs, SLAs

- SLI (Service Level Indicator): metric that indicates service health (e.g., request latency P99).
- SLO (Service Level Objective): target for SLI (e.g., 99.9% requests < 300ms).
- SLA (Service Level Agreement): contractual guarantee often with penalties.
- Define SLOs that reflect user experience and use them to prioritize engineering work and alert thresholds.

## Alerting best practices

- Alert on symptoms (high error rate, high latency), not on causes.
- Use severity levels, runbooks, and on-call playbooks.
- Avoid alert fatigue: tune thresholds, use aggregates, and apply suppression windows for noisy signals.

## Example setup

- Instrument service with Prometheus client -> scrape endpoint /metrics -> Grafana dashboard for latency/error rate -> Alertmanager sends high-priority alerts to PagerDuty and lower-priority to Slack.
- Use Sentry to capture uncaught exceptions and map to source code with release tracking.

## Interview prompts

- How would you instrument a new service to track latency end-to-end?
- Define an SLO for a customer-facing API and describe how you'd monitor breaches and respond.

Operational tips:

- Keep dashboards focused for on-call: top-level health, error budget, latency percentiles, queue lengths, and infrastructure metrics.
- Test alerts periodically and runbook steps in drills (game days).
