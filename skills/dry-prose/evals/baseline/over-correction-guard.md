# Token Refresh

Refresh the token before the request, or the request returns a 401. Retry
fails because the token expired.

The cache holds the token for 55 minutes. The refresh runs at 50 minutes, a
margin for clock drift.

If the install fails, delete the lockfile.
