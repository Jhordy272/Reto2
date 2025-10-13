#!/bin/bash
# send_50.sh — envía 50 logs al Log API (localhost:8090)
# Uso: chmod +x send_50.sh && ./send_50.sh

BASE="http://localhost:8090/logs"
H="Content-Type: application/json"

# 1-25: warmup / normales
curl -s -X POST "$BASE" -H "$H" -d '{"service":"warmup-1","level":"INFO","message":"Scheduled job completed","context":{"user":"qa1"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"warmup-2","level":"INFO","message":"Cache refreshed","context":{"user":"qa2"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"warmup-3","level":"INFO","message":"Request processed OK","context":{"path":"/api/health"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"scheduler","level":"INFO","message":"heartbeat","context":{"job_id":"sync-1"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"web","level":"INFO","message":"GET /static/logo.png 200","context":{"path":"/static/logo.png","user":"anon"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"service-a","level":"INFO","message":"User list fetched","context":{"user":"client-7"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"service-b","level":"INFO","message":"Background cleanup done","context":{}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"payments","level":"INFO","message":"Payment processed","context":{"order_id":1001,"user":"buyer-3"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"orders","level":"INFO","message":"Order enqueued","context":{"order_id":1002}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"auth-service","level":"INFO","message":"Token issued","context":{"user":"bob"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"sync","level":"INFO","message":"Sync finished in 120ms","context":{"duration_ms":120}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"cache","level":"INFO","message":"Cache miss for key user:42","context":{"key":"user:42"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"notifier","level":"INFO","message":"Email sent to alice","context":{"to":"alice@example.com"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"frontend","level":"INFO","message":"Build success","context":{"version":"1.2.3"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"metrics","level":"INFO","message":"Metrics flush complete","context":{}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"backup","level":"INFO","message":"Backup finished","context":{"size":"120MB"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"monitor","level":"INFO","message":"All checks OK","context":{}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"billing","level":"INFO","message":"Invoice generated #7701","context":{"invoice":7701}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"gateway","level":"INFO","message":"Upstream responded 200","context":{"upstream":"svc-x"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"worker","level":"INFO","message":"Job completed","context":{"job":"resize"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"cron","level":"INFO","message":"Daily report created","context":{}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"sync","level":"INFO","message":"Delta applied","context":{"rows":12}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"api-gateway","level":"INFO","message":"Route OK","context":{"path":"/v1/pay"}}'; sleep 0.02

# 26-50: sospechosos / fallas / intentos
curl -s -X POST "$BASE" -H "$H" -d '{"service":"invoice-controller","level":"ERROR","message":"Fatal exception: DB connection refused","context":{"user":"dsaa"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"auth-service","level":"WARN","message":"Permission denied for /admin by user alice","context":{"user":"alice","path":"/admin"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"rbac","level":"ERROR","message":"Privilege escalation attempt detected","context":{"user":"guest-223","role_from":"viewer","role_to":"admin"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"config-service","level":"ERROR","message":"Unauthorized config push to production","context":{"actor":"ci-bot","branch":"hotfix/unknown"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"payment-gateway","level":"ERROR","message":"Payment processor unreachable: timeout","context":{"attempt":3}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"web","level":"ERROR","message":"SQL error near \"DROP TABLE users;\"","context":{"input":"DROP TABLE users;"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"app","level":"ERROR","message":"Suspicious command execution: sudo rm -rf /tmp/attack","context":{"cmd":"sudo rm -rf /tmp/attack","user":"script"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"orders","level":"WARN","message":"Row deleted unexpectedly: order_id 12345","context":{"order_id":12345,"user":"unknown"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"db-service","level":"ERROR","message":"Massive inventory change: decreased 500 rows by user deployer","context":{"user":"deployer","rows_changed":500}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"auth-service","level":"ERROR","message":"Login failed for user admin from 10.0.0.11","context":{"ip":"10.0.0.11","user":"admin"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"auth-service","level":"ERROR","message":"Multiple failed logins from 10.0.0.12","context":{"ip":"10.0.0.12","user":"admin"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"payment-gateway","level":"ERROR","message":"Unhandled exception: NullPointer in module X","context":{"module":"X","trace":"...stack..."}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"service-x","level":"WARN","message":"Suspicious payload size change detected: 900MB","context":{"size":"900MB"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"service-y","level":"WARN","message":"Config checksum mismatch on node-7","context":{"node":"node-7","expected":"abc","got":"def"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"rbac","level":"ERROR","message":"Unauthorized role assignment: user bob -> admin","context":{"user":"bob","actor":"script"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"monitor","level":"ERROR","message":"Alert: config tamper detected on prod-db","context":{"node":"prod-db","actor":"unknown"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"deploy","level":"WARN","message":"Manual deploy performed outside pipeline","context":{"user":"ops-admin"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"gateway","level":"ERROR","message":"Upstream returned 502 repeatedly","context":{"upstream":"svc-x"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"auth-service","level":"ERROR","message":"Brute force: 50 failed logins from 10.0.9.9","context":{"ip":"10.0.9.9"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"admin-ui","level":"ERROR","message":"Unauthorized admin access attempt at 03:12 UTC from 10.0.5.23","context":{"user":"qa6","ip":"10.0.5.23"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"api-gateway","level":"ERROR","message":"Too many requests: 429 from client 10.0.2.5","context":{"ip":"10.0.2.5"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"security","level":"ERROR","message":"Configuration rollback detected","context":{"user":"infra","reason":"suspected tamper"}}'; sleep 0.02
curl -s -X POST "$BASE" -H "$H" -d '{"service":"probe","level":"ERROR","message":"test notify","context":{}}'; sleep 0.02

echo "Sent 50 logs to $BASE"
