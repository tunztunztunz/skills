# Log levels

| Level | What it writes | Volume per hour |
|---|---|---|
| `trace` | Every span | 40 MB |
| `debug` | Spans that fail | 5 MB |
| `info` | Batch summaries | 200 KB |
| `error` | Failures only | 10 KB |

Set the level with `--log-level`.
