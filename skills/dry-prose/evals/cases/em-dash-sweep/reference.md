# Retry policy

The collector retries only on 5xx responses, plus the 408 and 504 timeouts. It leaves every
other 4xx response alone.

The backoff window is 2-8 seconds.
