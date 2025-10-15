# Fence Test - Asset Interest Rate Management API

## Overview

This project implements a FastAPI application for managing financial assets and calculating average interest rates. Following the exercise instructions, I've implemented the database version as the primary solution, with a clean architecture that can easily be extended to support smart contracts.

## My Reasoning and Assumptions

### 📝 **Key Assumptions Made**

1. **Interest Rate Calculation**: Simple arithmetic average of all provided assets
2. **Data Persistence**: PostgreSQL for reliability and ACID compliance
3. **API Authentication**: Simple API key for the technical test context
4. **Response Format**: JSON with clear confirmation messages and timestamps
5. **Error Handling**: Comprehensive validation with meaningful error messages
6. **Docker Deployment**: Containerized solution for easy setup and consistency

## Architecture & Design Decisions

### 🏗️ **Clean Architecture with Service Layer**

I implemented a **service-oriented architecture** that separates concerns clearly:

```
app/
├── api/                          # Presentation Layer
│   └── v1/endpoints/            # FastAPI route handlers
├── core/                        # Infrastructure
│   ├── config.py               # Application settings
│   ├── security.py             # API key authentication
│   └── logger.py               # Logging setup
├── services/                    # Business Logic Layer
│   ├── __init__.py             # Dependency injection
│   └── interest_rate_service.py # Core business logic
├── repositories/                # Data Access Layer
│   └── interest_rate_repository.py # Database operations
├── database_handler/            # Database Infrastructure
│   ├── models/                 # SQLAlchemy models
│   ├── session.py              # Database session management
│   └── migration/              # Alembic migrations
├── schemas/                     # Data Transfer Objects
│   └── endpoints/              # Request/Response schemas
└── main.py                     # Application entry point
```

### 🎯 **Design Principles Applied**

1. **Single Responsibility**: Each layer has one clear purpose
2. **Dependency Injection**: Services are injected, not instantiated directly
3. **Database Abstraction**: Repository pattern for data access
4. **Clean Separation**: Business logic isolated from infrastructure concerns

## Trade-offs Considered

### 1. **Simple vs Complex Authentication**
- **Choice**: API key authentication
- **Trade-off**: Less secure than OAuth2/JWT tokens
- **Rationale**: Appropriate for technical test, easy to implement and understand
- **Production**: Would upgrade to proper authentication system

### 2. **Direct vs Abstracted Database Access**
- **Choice**: Repository pattern with direct SQLAlchemy
- **Trade-off**: Some coupling to SQLAlchemy
- **Rationale**: Good balance between abstraction and simplicity
- **Alternative**: Could use more abstract ORM or raw SQL

### 3. **Alembic vs Manual Database Management**
- **Choice**: Alembic for database migrations
- **Trade-off**: Additional dependency and configuration
- **Rationale**: 
  - **Easy to install**: Simple pip install, no complex setup
  - **One command migrations**: `alembic revision --autogenerate` creates migration files automatically
  - **Version control**: Track database schema changes in Git
  - **Production ready**: Industry standard for Python database migrations
  - **Convenience**: No manual SQL scripts to maintain
- **Alternative**: Could use raw SQL scripts, but less maintainable

### 4. **Docker vs Local Development**
- **Choice**: Docker-first approach
- **Trade-off**: Slightly more complex setup
- **Rationale**: Ensures consistent environment, easier deployment
- **Benefit**: Production-ready containerization


## Setup & Usage Instructions

### Prerequisites
- Docker and Docker Compose
- Git

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd fence-test
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

3. **Start the application**:
   ```bash
   docker-compose up --build
   ```

4. **Access the API**:
   - **API Documentation**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/
   - **Database**: PostgreSQL on localhost:5432

### Environment Variables

Key environment variables (see `.env.example`):
- `API_KEY_AUTH`: Your API key for authentication
- `POSTGRES_*`: Database connection settings
- All settings have sensible defaults for development

## API Endpoints

### POST /asset
Receives a list of assets and updates the average interest rate in the database.

**Request**:
```bash
curl -X POST "http://localhost:8000/asset" \
  -H "api_key: your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d '[
    {"id": "id-1", "interest_rate": 100},
    {"id": "id-2", "interest_rate": 10}
  ]'
```

**Response**:
```json
{
  "message": "Average interest rate calculated and saved successfully"
}
```

### GET /interest_rate
Returns the interest rate value currently stored in the database.

**Request**:
```bash
curl -X GET "http://localhost:8000/interest_rate" \
  -H "api_key: your-secret-api-key-here"
```

**Response**:
```json
{
  "interest_rate": "55.0",
  "updated_at": "2025-10-15T18:22:51.768546"
}
```

### Example Workflow

1. **POST assets** → Confirms calculation and saves to database
2. **GET interest_rate** → Retrieves the current stored rate
3. **POST new assets** → Overwrites previous rate with new average
4. **GET interest_rate** → Shows updated rate

## How I Would Productionize This Solution

### 🔒 **Security Enhancements**
1. **Authentication**: Replace API key with OAuth2/JWT tokens
2. **Input Validation**: Enhanced sanitization and validation
3. **HTTPS**: Force TLS encryption in production
4. **Secrets Management**: Use proper secret management (AWS Secrets Manager, etc.)

### ⚡ **Database & Performance Optimizations**
1. **Connection Pool Configuration**: Improve `session.py` engine with proper pool settings:
   ```python
   engine = create_engine(
       settings.SQLALCHEMY_DATABASE_URL,
       pool_size=20,           # Number of connections to maintain
       max_overflow=30,        # Additional connections when pool is exhausted
       pool_timeout=30,        # Seconds to wait for connection
       pool_recycle=3600,      # Recycle connections after 1 hour
       pool_pre_ping=True      # Validate connections before use
   )
   ```
2. **Async Database Operations**: Convert repository and service layers to async:
   ```python
   # Async repository with asyncpg driver
   async def save_interest_rate(self, rate: Decimal, timestamp: datetime) -> None:
       async with self.db.begin():
           await self.db.execute(
               insert(InterestRateModel).values(rate=rate, updated_at=timestamp)
           )
   ```
3. **Connection Health Checks**: Implement database health monitoring

### 🏗️ **Infrastructure & Deployment**
1. **Container Orchestration**: Kubernetes for scalable deployment
2. **Database**: Managed PostgreSQL (AWS RDS, Google Cloud SQL)
3. **CI/CD Pipeline**: Automated testing, building, and deployment
4. **Monitoring**: Prometheus + Grafana for metrics and alerting
5. **Logging**: Structured logging with proper log levels
6. **Backup Strategy**: Automated database backups and disaster recovery

### 📈 **Scalability Considerations**
1. **Horizontal Scaling**: Stateless application design supports multiple instances
2. **Load Balancing**: Multiple application instances behind load balancer
3. **Database Read Replicas**: For read-heavy workloads
4. **API Versioning**: Proper versioning strategy for backward compatibility

### 🧪 **Testing & Quality Assurance**
1. **Unit Tests**: Comprehensive test coverage for business logic and repositories
2. **Integration Tests**: End-to-end API testing with test database
3. **Database Tests**: Migration testing and data integrity validation
4. **Load Testing**: Performance testing under concurrent requests
5. **Security Testing**: Penetration testing and vulnerability scans

## Technical Implementation Details

### 🗄️ **Database Schema**
```sql
CREATE TABLE interest_rates (
    id SERIAL PRIMARY KEY,
    rate DECIMAL(10,2) NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

### 🔄 **Data Flow**
1. **POST /asset**: FastAPI → Service → Repository → PostgreSQL
2. **GET /interest_rate**: FastAPI → Service → Repository → PostgreSQL
3. **Migrations**: Alembic handles database schema changes

### 🛠️ **Key Technologies Used**
- **FastAPI**: Modern Python web framework with automatic API documentation
- **SQLAlchemy**: Python SQL toolkit and ORM for database operations
- **Alembic**: Database migration tool for schema management
- **PostgreSQL**: Robust relational database for data persistence
- **Docker**: Containerization for consistent deployment
- **Pydantic**: Data validation and serialization

### 📊 **Example Calculation**
```python
# Input assets
assets = [
    {"id": "asset-1", "interest_rate": 150.50},
    {"id": "asset-2", "interest_rate": 75.25},
    {"id": "asset-3", "interest_rate": 200.75},
    {"id": "asset-4", "interest_rate": 50.00}
]

# Calculation: (150.50 + 75.25 + 200.75 + 50.00) / 4 = 119.125
# Stored in database with current timestamp
```

---

*This implementation demonstrates clean architecture principles, proper separation of concerns, and production-ready practices while meeting all the technical exercise requirements.*

