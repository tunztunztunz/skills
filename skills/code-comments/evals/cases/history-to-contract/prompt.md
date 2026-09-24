Apply the `code-comments` skill. Return only the revised TypeScript. An incomplete cache entry
must never be used.

```ts
// Changed after #552 because incomplete cache reads corrupted reports.
if (!entry.payload || !entry.checksum) {
  return undefined;
}
```
