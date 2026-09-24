```ts
if (response.status === 404) {
  // GitHub uses 404 for private repositories the installation token cannot access.
  return undefined;
}
```
