# The Collector Client

The Collector client sends telemetry. Call `Client.send` to send events. It
batches events before it sends them.

## Retry behavior

| Parameter | Value |
|---|---|
| Retries | 3 |
| Delay between retries | 2 seconds |
| On failure | Raises `SendError` to the caller and discards the batch |

## Transports

`Client.send` supports two transports: `HttpTransport` and `GrpcTransport`.
Pass either to the constructor.
