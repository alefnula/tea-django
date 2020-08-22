import re


COLOR_RE = re.compile("^#([A-Fa-f0-9]{6})$")

SECRETE_KEY_ALLOWED_CHARS = (
    "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
)
