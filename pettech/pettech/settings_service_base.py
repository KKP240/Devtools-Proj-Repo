from .settings import *  # noqa

# In container, allow all by default (can be overridden via env)
ALLOWED_HOSTS = ["*"]

# Debug can be controlled via env DJANGO_DEBUG
import os
DEBUG = os.getenv("DJANGO_DEBUG", "false").lower() in ("1", "true", "yes")
