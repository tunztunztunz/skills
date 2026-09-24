# The Collector Client

The Collector client surfaces the primitives you need to orchestrate your telemetry
lifecycle. The send method, Client.send, provides a powerful and flexible interface that
handles the complexities of batching under the hood, and it has been battle-tested in
production.

Retry behaviour is robust: a rejected batch will be retried 3 times, with 2 seconds between
attempts, subsequent to which a SendError is surfaced to the caller and the batch is
discarded.

The client is capable of supporting multiple transports, namely HttpTransport and
GrpcTransport, either of which may be utilized by passing it to the constructor.
Performance is blazing fast.
