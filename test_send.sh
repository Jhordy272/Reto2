#!/usr/bin/env bash
set -euo pipefail

API="http://localhost:8090/logs"
content_type="Content-Type: application/json"

# 1) Warmup: muchos logs "normales"
echo "=== Warmup: 200 logs normales ==="
for i in $(seq 1 200); do
  user="qa$(( (i % 20) + 1 ))"
  service="service-$(( (i % 6) + 1 ))"
  msg="Routine heartbeat OK #$i"
  curl -s -X POST "$API" -H "$content_type" -d "{\"service\":\"$service\",\"level\":\"INFO\",\"message\":\"$msg\",\"context\":{\"user\":\"$user\"}}" >/dev/null
done
echo "Warmup done."

# 2) Algunos eventos sospechosos variados
echo "=== Enviando eventos sospechosos ==="

# Unauthorized admin attempt
curl -s -X POST "$API" -H "$content_type" -d '{"service":"invoice-controller","level":"ERROR","message":"Unauthorized admin access attempt at 03:12 UTC from 10.0.5.23","context":{"user":"qa6","ip":"10.0.5.23"}}'

# Privilege escalation
curl -s -X POST "$API" -H "$content_type" -d '{"service":"rbac","level":"ERROR","message":"Privilege escalation attempt detected","context":{"user":"guest-223","role_from":"viewer","role_to":"admin"}}'

# Unauthorized config push
curl -s -X POST "$API" -H "$content_type" -d '{"service":"config-service","level":"ERROR","message":"Unauthorized config push to production","context":{"actor":"ci-bot","branch":"hotfix/unknown"}}'

# DB errors burst
for i in $(seq 1 8); do
  curl -s -X POST "$API" -H "$content_type" -d "{\"service\":\"payment-gateway\",\"level\":\"ERROR\",\"message\":\"Fatal exception: DB connection refused #$i\",\"context\":{\"user\":\"payment-svc\"}}" >/dev/null
done

# Login brute-like
for ip in 10.0.0.{10,11,12,13,14}; do
  curl -s -X POST "$API" -H "$content_type" -d "{\"service\":\"auth-service\",\"level\":\"ERROR\",\"message\":\"Login failed for user admin from $ip\",\"context\":{\"ip\":\"$ip\",\"user\":\"unknown\"}}" >/dev/null
done

echo "Suspect events sent."
