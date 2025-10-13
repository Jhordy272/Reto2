# Invoice Calculator

This repository contains two implementations of an Invoice Calculator API:
- **InvoiceCalculatorJava**: Spring Boot REST API
- **InvoiceCalculatorPython**: FastAPI REST API

Both applications provide the same functionality for calculating invoices based on product information stored in a PostgreSQL database.

## Architecture


Both implementations follow a layered architecture:
- **Models/Entities**: Database entities
- **DTOs/Schemas**: Data transfer objects for API requests/responses
- **Repositories**: Data access layer
- **Services**: Business logic layer
- **Controllers/Routers**: REST API endpoints

## Quick Start with Docker Compose

The easiest way to run all services (PostgreSQL + both APIs) is using Docker Compose:

```bash
docker-compose up --build
```

This will start:
- **PostgreSQL** on port 5432 (with automatic database initialization)
- **Java API** on port 8080
- **Python API** on port 8081

To run in detached mode:
```bash
docker-compose up --build -d
```

To stop all services:
```bash
docker-compose down
```

To stop and remove volumes (database data):
```bash
docker-compose down -v
```

### Database Setup

Both applications use the same PostgreSQL database schema. Run the initialization script:

```bash
psql -U postgres -d inventary -f init.sql
```

Or import `init.sql` using your preferred PostgreSQL client.

## InvoiceCalculatorJava (Spring Boot)

### Prerequisites
- Java 21
- Maven
- PostgreSQL

### Environment Variables
Set the following environment variables or update `application.properties`:

```properties
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=inventary
```

### Running the Application

```bash
cd InvoiceCalculatorJava
mvn spring-boot:run
```

The API will be available at `http://localhost:8080`

### API Documentation
Swagger UI: `http://localhost:8080/swagger-ui/index.html`

## InvoiceCalculatorPython (FastAPI)

### Prerequisites
- Python 3.8 or higher
- pip
- PostgreSQL

### Setup

1. Create a virtual environment:
```bash
cd InvoiceCalculatorPython
python -m venv venv
```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update values if needed (defaults match Java configuration)

### Running the Application

```bash
uvicorn main:app --host 0.0.0.0 --port 8081 --reload
```

The API will be available at `http://localhost:8081`

### API Documentation
- Swagger UI: `http://localhost:8081/docs`
- ReDoc: `http://localhost:8081/redoc`

## API Endpoints

### POST /invoice/calculate

Calculate the total amount for an invoice based on product IDs and quantities.

**Request Body:**
```json
{
  "items": [
    {
      "productId": 1,
      "quantity": 10
    },
    {
      "productId": 2,
      "quantity": 5
    }
  ]
}
```

**Response:**
```json
{
  "items": [
    {
      "productId": 1,
      "productName": "Laptop Dell XPS 13",
      "quantity": 10,
      "unitPrice": 1299.99,
      "subtotal": 12999.9
    },
    {
      "productId": 2,
      "productName": "Mouse Logitech MX Master 3",
      "quantity": 5,
      "unitPrice": 99.99,
      "subtotal": 499.95
    }
  ],
  "total": 13499.85
}
```

## Testing

### Using Swagger/OpenAPI
Both implementations provide interactive API documentation where you can test endpoints directly in your browser.

## Error Handling

Both APIs handle the following error cases:
- **404**: Product not found
- **400**: Insufficient stock for product
- **500**: Internal server error





AQUI PARA PROBAR

curl -X POST "http://localhost:8090/logs" \
  -H "Content-Type: application/json" \
  -d '{"service":"invoice-controller","level":"ERROR","message":"Fatal exception: DB connection refused","context":{"user":"dsaa"}}'

curl "http://localhost:8090/logs?limit=5"

PGPASSWORD=password psql -h localhost -p 5433 -U postgres -d logsdb -c \
"SELECT detected_at,service,rule,score,sample_log_id FROM log_insights ORDER BY id DESC LIMIT 5;"



curl -X POST "http://localhost:8090/logs" \
  -H "Content-Type: application/json" \
  -d '{"service":"invoice-controller","level":"ERROR","message":"Fatal anomaly: checksum mismatch in payment DAG block 392","context":{"user":"qa-rare"}}'



borrado masivo sospechoso

curl -X POST "http://localhost:8090/logs" \
  -H "Content-Type: application/json" \
  -d '{"service":"invoice-controller","level":"ERROR","message":"Fatal: 1024 records deleted from invoices without change request","context":{"user":"qa5"}}'


curl -X POST "http://localhost:8090/logs" \
  -H "Content-Type: application/json" \
  -d '{"service":"invoice-controller","level":"ERROR","message":"Unauthorized admin access attempt at 03:12 UTC from 10.0.5.23","context":{"user":"qa6","ip":"10.0.5.23"}}'


ACCESO FUERA DE HORAS


# 1) unauthorized + denied  -> sk >= 3.0
curl -X POST "http://localhost:8090/logs" \
  -H "Content-Type: application/json" \
  -d '{"service":"invoice-controller","level":"ERROR","message":"Unauthorized admin access denied at 03:12 UTC from 10.0.5.23","context":{"user":"qa6","ip":"10.0.5.23"}}'


curl -X POST "http://localhost:8090/logs" \
  -H "Content-Type: application/json" \
  -d '{"service":"invoice-controller","level":"ERROR","message":"Unauthorized admin access attempt at 03:12 UTC from 10.0.5.23","context":{"user":"qa6","ip":"10.0.5.23"}}'




CON ESTO SE REQALIZA EL CALENTAMIENTO

# 1) 100 logs normales, con mensajes muy parecidos
for i in $(seq 1 100); do
  curl -s -X POST "http://localhost:8090/logs" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"invoice-controller\",\"level\":\"INFO\",\"message\":\"Invoice processed successfully for user ${i}\",\"context\":{\"user\":\"seed${i}\"}}" >/dev/null
  sleep 0.03   # pequeño delay para NO disparar la regla de burst
done

# 2) 100 más con ligera variación (sigue siendo “normal”)
for i in $(seq 101 200); do
  curl -s -X POST "http://localhost:8090/logs" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"invoice-controller\",\"level\":\"INFO\",\"message\":\"Invoice processed successfully; items=3; total=\$${i}\",\"context\":{\"user\":\"seed${i}\"}}" >/dev/null
  sleep 0.03
done




PASOS


./test_send.sh

LOGS NORMALES

# 1
curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" -d '{"service":"service-a","level":"INFO","message":"Scheduled job completed","context":{"user":"qa1"}}'

# 2
curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" -d '{"service":"service-b","level":"INFO","message":"Cache refreshed","context":{"user":"qa2"}}'

# 3
curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" -d '{"service":"service-c","level":"INFO","message":"Request processed OK","context":{"path":"/api/health"}}'

# 4
curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" -d '{"service":"service-d","level":"INFO","message":"OK healthcheck","context":{}}'

# 5 (heartbeat)
curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" -d '{"service":"scheduler","level":"INFO","message":"heartbeat","context":{"job_id":"sync-1"}}'


for i in $(seq 1 200); do
  curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" \
    -d "{\"service\":\"warmup-$((i%8))\",\"level\":\"INFO\",\"message\":\"Routine heartbeat #$i\",\"context\":{\"user\":\"qa$((i%20))\"}}"
done



LOGS DE FALLA


ACCESOS NO AUTORIZADOS

curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" \
  -d '{"service":"invoice-controller","level":"ERROR","message":"Unauthorized admin access attempt at 03:12 UTC from 10.0.5.23","context":{"user":"qa6","ip":"10.0.5.23"}}'

curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" \
  -d '{"service":"auth-service","level":"WARN","message":"Permission denied for /admin by user alice","context":{"user":"alice","path":"/admin"}}'


Escalada de privilegios

curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" \
  -d '{"service":"rbac","level":"ERROR","message":"Privilege escalation attempt detected","context":{"user":"guest-223","role_from":"viewer","role_to":"admin"}}'


CAMBIOS DE CONFIGURACIÖN SOSPECHPOSOS

curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" \
  -d '{"service":"config-service","level":"ERROR","message":"Unauthorized config push to production","context":{"actor":"ci-bot","branch":"hotfix/unknown"}}'

curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" \
  -d '{"service":"deploy","level":"WARN","message":"Manual deploy performed outside pipeline","context":{"user":"ops-admin","commit":"abc123"}}'


ERRORES CRITICOS

curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" \
  -d '{"service":"payment-gateway","level":"ERROR","message":"Fatal exception: DB connection refused","context":{"user":"payment-svc"}}'

curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" \
  -d '{"service":"api-gateway","level":"ERROR","message":"Unhandled exception: NullPointer in module X","context":{"module":"X","trace":"...stack..."}}'


Picos y bursts (varios errores seguidos)

for i in $(seq 1 8); do
  curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" \
    -d "{\"service\":\"payment-gateway\",\"level\":\"ERROR\",\"message\":\"Fatal exception: DB connection refused #$i\",\"context\":{\"user\":\"payment-svc\"}}"
done



Fuerza bruta / múltiples fallos de login desde IPs

curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" \
  -d '{"service":"auth-service","level":"ERROR","message":"Login failed for user admin from 10.0.0.11","context":{"ip":"10.0.0.11","user":"admin"}}'

for ip in 10.0.0.10 10.0.0.11 10.0.0.12 10.0.0.13 10.0.0.14; do
  curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" \
    -d "{\"service\":\"auth-service\",\"level\":\"ERROR\",\"message\":\"Login failed for user admin from $ip\",\"context\":{\"ip\":\"$ip\",\"user\":\"admin\"}}"
done


Manipulación de datos / cambios sospechosos

curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" \
  -d '{"service":"db-service","level":"ERROR","message":"Massive inventory change: decreased 500 rows by user deployer","context":{"user":"deployer","rows_changed":500}}'

curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" \
  -d '{"service":"orders","level":"WARN","message":"Row deleted unexpectedly: order_id 12345","context":{"order_id":12345,"user":"unknown"}}'


INYECCION

curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" \
  -d '{"service":"web","level":"ERROR","message":"SQL error near \"DROP TABLE users;\"","context":{"input":"DROP TABLE users;"}}'

curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" \
  -d '{"service":"app","level":"ERROR","message":"Suspicious command execution: sudo rm -rf /tmp/attack","context":{"cmd":"sudo rm -rf /tmp/attack","user":"script"}}'


MENSAJES RAROS

curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" \
  -d '{"service":"service-x","level":"WARN","message":"Suspicious payload size change detected: 900MB","context":{"size":"900MB"}}'

curl -s -X POST "http://localhost:8090/logs" -H "Content-Type: application/json" \
  -d '{"service":"service-y","level":"WARN","message":"Config checksum mismatch on node-7","context":{"node":"node-7","expected":"abc","got":"def"}}'


 PGPASSWORD=password psql -h localhost -p 5433 -U postgres -d logsdb -c "SELECT detected_at,service,rule,score,sample_log_id FROM log_insights ORDER BY id DESC LIMIT 5;"

 PGPASSWORD=password psql -h localhost -p 5433 -U postgres -d logsdb -c \
"SELECT id, detected_at, service, rule, score, sample_msg FROM log_insights ORDER BY id DESC LIMIT 20;"
