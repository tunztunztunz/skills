# Retry Policy

| Response | Retried |
|---|---|
| 5xx | Yes |
| Timeouts (408, 504) | Yes |
| Other 4xx | No |

The backoff window is 2–8 seconds. The collector retries, waits, then retries again.
