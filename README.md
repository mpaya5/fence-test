# Fence Test - Asset Interest Rate Management API

## Overview

This project implements a FastAPI application for managing financial assets and calculating average interest rates. The system is designed with a flexible architecture that supports multiple storage backends (in-memory, database, or smart contracts).

## Architecture & Design Decisions

### 🏗️ **Architecture Approach: Clean & Simple**

I chose a **simple, clean architecture** because:
- **Interview Context**: For a 2-4 hour technical test, simplicity demonstrates clear thinking
- **Pragmatic**: Right tool for the job - no over-engineering
- **Maintainable**: Easy to understand and extend
- **Future-ready**: Easy to add complexity (database/smart contracts) when needed

### 📁 **Project Structure**

```
app/
├── api/                    # Presentation Layer (FastAPI endpoints)
│   └── v1/
│       ├── endpoints/      # API route handlers
│       └── router.py       # Route aggregation
├── core/                   # Infrastructure concerns
│   ├── config.py          # Application configuration
│   ├── security.py        # API key authentication
│   └── logger.py          # Logging configuration
├── services/               # Business Logic Layer
│   ├── __init__.py        # Service factory functions
│   └── interest_rate_service.py  # Service with storage abstraction
├── schemas/                # Data Transfer Objects
│   └── endpoints/         # Request/Response schemas
└── main.py                # Application entry point
```

### 🎯 **Key Design Principles Applied**

1. **Clean Code**
   - Single Responsibility Principle
   - Clear naming conventions
   - Comprehensive error handling
   - Simple, readable functions

2. **Pragmatic Architecture**
   - **YAGNI**: You Aren't Gonna Need It - no over-engineering
   - **KISS**: Keep It Simple, Stupid - direct approach
   - **SOLID**: Focused on maintainable code structure

3. **FastAPI Best Practices**
   - Pydantic models for validation
   - Proper HTTP status codes
   - Clear API documentation
   - Dependency injection for security

## 🚀 **Setup & Usage Instructions**

### Prerequisites
- Docker and Docker Compose
- Python 3.13+ (for local development)

### Quick Start with Docker

1. **Clone and setup**:
   ```bash
   git clone <repository>
   cd fence-test
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   # Edit .env with your API key
   ```

3. **Run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

4. **Access the API**:
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**:
   ```bash
   export API_KEY_AUTH="your-secret-api-key-here"
   ```

3. **Run the application**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📡 **API Endpoints**

### POST /asset
Updates assets and calculates average interest rate.

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
  "interest_rate": "55.0",
  "updated_at": "2024-01-15T10:30:00.000000"
}
```

### GET /interest_rate
Retrieves the current average interest rate.

**Request**:
```bash
curl -X GET "http://localhost:8000/interest_rate" \
  -H "api_key: your-secret-api-key-here"
```

**Response**:
```json
{
  "interest_rate": "55.0",
  "updated_at": "2024-01-15T10:30:00.000000"
}
```

## 🔧 **Trade-offs Considered**

### 1. **Storage Implementation**
- **Current**: Service layer with in-memory storage abstraction
- **Trade-off**: Data is lost on restart, no persistence
- **Rationale**: Clean architecture with easy extensibility for different backends
- **Production**: Easy to swap `InMemoryStorage` for `DatabaseStorage` or `SmartContractStorage`

### 2. **API Key Authentication**
- **Choice**: Simple API key header authentication
- **Trade-off**: Not as secure as JWT tokens
- **Rationale**: Sufficient for technical test, easy to implement
- **Production**: Would use OAuth2/JWT with proper key management

### 3. **Error Handling**
- **Choice**: Comprehensive HTTP status codes and error messages
- **Trade-off**: Exposes some internal details
- **Rationale**: Better debugging experience for development
- **Production**: Would sanitize error messages for security

### 4. **Data Validation**
- **Choice**: Pydantic models with strict validation
- **Trade-off**: More verbose than simple dicts
- **Rationale**: Type safety, automatic documentation, clear contracts

## 🏭 **Production Considerations**

### Security Enhancements
1. **Authentication**: Implement OAuth2/JWT with proper token management
2. **Rate Limiting**: Add request rate limiting (Redis-based)
3. **Input Sanitization**: Enhanced validation and sanitization
4. **HTTPS**: Force HTTPS in production
5. **API Versioning**: Implement proper API versioning strategy

### Performance Optimizations
1. **Caching**: Redis cache for frequently accessed data
2. **Database Connection Pooling**: For database implementations
3. **Async Operations**: Full async/await pattern throughout
4. **Monitoring**: APM tools (DataDog, New Relic)
5. **Load Balancing**: Multiple instances behind load balancer

### Infrastructure
1. **Container Orchestration**: Kubernetes deployment
2. **Database**: PostgreSQL with connection pooling
3. **Monitoring**: Prometheus + Grafana
4. **Logging**: Structured logging with ELK stack
5. **CI/CD**: Automated testing and deployment pipeline

### Scalability
1. **Horizontal Scaling**: Stateless application design
2. **Database Sharding**: For high-volume scenarios
3. **Message Queues**: For async processing
4. **CDN**: For static content and caching

## 🧪 **Testing Strategy**

The current implementation includes:
- **Unit Tests**: Repository and business logic testing
- **Integration Tests**: API endpoint testing
- **Contract Tests**: Schema validation testing

For production:
- **Load Testing**: Performance under high traffic
- **Security Testing**: Penetration testing and vulnerability scans
- **Chaos Engineering**: Resilience testing

## 🔮 **Future Implementations**

The service layer architecture makes it trivial to extend:

1. **Database Version** (`database` branch):
   ```python
   # In services/__init__.py
   def get_interest_rate_service() -> InterestRateService:
       storage = DatabaseStorage()  # Only change this line
       return InterestRateService(storage)
   ```

2. **Smart Contract Version** (`smart-contract` branch):
   ```python
   # In services/__init__.py
   def get_interest_rate_service() -> InterestRateService:
       storage = SmartContractStorage()  # Only change this line
       return InterestRateService(storage)
   ```

The endpoints and business logic remain unchanged - only the storage implementation changes.

## 📝 **Assumptions Made**

1. **Interest Rate Calculation**: Simple arithmetic average (could be weighted)
2. **Asset IDs**: String-based unique identifiers
3. **Timestamps**: UTC timezone for consistency
4. **Decimal Precision**: Using Python Decimal for financial calculations
5. **API Response**: JSON format with human-readable timestamps

## 🤝 **Contributing**

1. Create feature branches from `main`
2. Implement database version in `database` branch
3. Implement smart contract version in `smart-contract` branch
4. Follow the established architecture patterns
5. Add comprehensive tests for new features

---

*This implementation prioritizes clean architecture, maintainability, and extensibility while meeting the core requirements of the technical exercise.*

