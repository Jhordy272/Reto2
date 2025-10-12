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
