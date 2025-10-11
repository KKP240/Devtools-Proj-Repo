from .settings import *  # noqa

# In container, allow all by default (can be overridden via env)
ALLOWED_HOSTS = ["*"]

# Debug can be controlled via env DJANGO_DEBUG
import os
DEBUG = os.getenv("DJANGO_DEBUG", "false").lower() in ("1", "true", "yes")

# CSRF/Session behind gateway at localhost:8000
GATEWAY_HOST = os.getenv("GATEWAY_HOST", "http://localhost:8000")
CSRF_TRUSTED_ORIGINS = list(set((locals().get('CSRF_TRUSTED_ORIGINS') or []) + [
	GATEWAY_HOST,
	"http://localhost:8001",
	"http://localhost:8002",
	"http://localhost:8003",
	"http://localhost:8004",
]))

# Tweak cookies for same-host proxying
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_HTTPONLY = False
