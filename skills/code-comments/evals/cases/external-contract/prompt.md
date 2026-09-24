Apply the `code-comments` skill. Return only the revised TypeScript. GitHub deliberately returns
404 for private repositories that the installation token cannot access.

```ts
if (response.status === 404) {
  return undefined;
}
```
