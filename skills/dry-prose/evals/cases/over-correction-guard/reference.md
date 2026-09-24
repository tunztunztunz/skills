# Token refresh

Refresh the token before the request, or the request returns 401.

A retry fails because the token expired. The cache holds the token for 55 minutes, and the
refresh runs at 50 minutes so that clock drift cannot outrun it.

If the install fails, delete the lockfile.
