# Collector client

`Client.send` takes a batch of spans and sends it.

The client retries a rejected batch 3 times, with 2 seconds between tries. After the last
try it raises `SendError` and drops the batch.

The client ships 2 transports: `HttpTransport` and `GrpcTransport`. Pass one to the
constructor.
