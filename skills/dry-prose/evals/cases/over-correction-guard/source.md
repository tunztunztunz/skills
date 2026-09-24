# Token Refresh

Refresh token before request, else request returns 401. Retry fails, token expired.
Cache holds token 55 minutes, refresh runs at 50 minutes — margin for clock drift.
Install fails, delete lockfile.
