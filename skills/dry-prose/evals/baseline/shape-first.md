# Log Levels

The collector has 4 log levels, set with the `--log-level` flag.

| Level | Writes | Rate |
|---|---|---|
| trace | every span | about 40 MB per hour |
| debug | spans that fail | about 5 MB per hour |
| info | batch summaries only | about 200 KB per hour |
| error | failures only | under 10 KB per hour |
