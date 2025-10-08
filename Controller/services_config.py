import os

PRECISION = int(os.getenv("VOTE_PRECISION", "2"))
ENABLE_PYTHON = os.getenv("ENABLE_PYTHON", "true").lower() == "true"
ENABLE_JAVA = os.getenv("ENABLE_JAVA", "false").lower() == "true"
ENABLE_CSHARP = os.getenv("ENABLE_CSHARP", "false").lower() == "true"
PYTHON_URL = os.getenv("PYTHON_URL", "http://invoice-calculator-python:8081")
JAVA_URL = os.getenv("JAVA_URL", "http://invoice-calculator-java:8080")
CSHARP_URL = os.getenv("CSHARP_URL", "http://invoice-calculator-csharp:5000")
TIMEOUT_SECS = float(os.getenv("SERVICE_TIMEOUT_SECS", "15"))

def enabled_services():
    m = {}
    if ENABLE_PYTHON:
        m["python"] = PYTHON_URL
    if ENABLE_JAVA:
        m["java"] = JAVA_URL
    if ENABLE_CSHARP:
        m["csharp"] = CSHARP_URL
    return m
