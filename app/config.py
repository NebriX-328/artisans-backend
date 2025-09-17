# app/config.py
import os

# PUBLIC_DOMAIN should be set as an environment variable (no scheme)
# e.g. my-dca-cert.onrender.com
PUBLIC_DOMAIN = os.getenv("PUBLIC_DOMAIN", "").strip()
