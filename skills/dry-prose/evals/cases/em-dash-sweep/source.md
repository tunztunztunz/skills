# Retry Policy

The collector retries — and this is the important part — only on 5xx responses. Timeouts
are retried too — 408 and 504 — but other 4xx responses are not.

The backoff window is 2-8 seconds. The policy is simple — retry, wait, retry.
