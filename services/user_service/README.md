User Service

- Issues and validates JWT tokens using SimpleJWT.
- Uses shared signing secret so other services can validate tokens.

Endpoints
- POST /auth/token/ -> obtain access/refresh
- POST /auth/refresh/ -> refresh access
