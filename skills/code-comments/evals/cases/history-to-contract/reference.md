```ts
// Cache entries remain invalid until both payload and checksum are present.
if (!entry.payload || !entry.checksum) {
  return undefined;
}
```
