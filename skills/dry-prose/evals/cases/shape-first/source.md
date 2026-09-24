# Log Levels

The collector supports four log levels. The trace level writes every span and is
approximately 40 MB per hour, debug writes the spans that fail and is about 5 MB per hour,
info writes only batch summaries at roughly 200 KB per hour, and error writes nothing but
failures, which is under 10 KB per hour. The level is set with the --log-level flag.
