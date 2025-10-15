# Fence Test - Smart Contract Asset Interest Rate Management API

## Overview

This project implements a FastAPI application with a Smart Contract backend for managing financial assets and calculating average interest rates. The system uses a Hardhat local blockchain with automated contract deployment and seamless integration between the API and Smart Contract.

## Architecture & Design Decisions

### 🏗️ **Architecture Approach: Clean & Simple**

I chose a **simple, clean architecture** because:
- **Interview Context**: For a 2-4 hour technical test, simplicity demonstrates clear thinking
- **Pragmatic**: Right tool for the job - no over-engineering
- **Maintainable**: Easy to understand and extend
- **Future-ready**: Easy to add complexity (database/smart contracts) when needed

### 📁 **Project Structure**

```
fence-test/
├── app/                    # FastAPI Application
│   ├── api/               # Presentation Layer (FastAPI endpoints)
│   │   └── v1/
│   │       ├── endpoints/ # API route handlers
│   │       └── router.py  # Route aggregation
│   ├── core/              # Infrastructure concerns
│   │   ├── config.py      # Application configuration
│   │   ├── security.py    # API key authentication
│   │   └── logger.py      # Logging configuration
│   ├── services/          # Business Logic Layer
│   │   ├── __init__.py    # Service factory functions
│   │   └── interest_rate_service.py  # Service with storage abstraction
│   ├── smart_contracts/   # Smart Contract Integration
│   │   ├── client/        # Web3 client for blockchain interaction
│   │   ├── contracts/     # Solidity contract source
│   │   └── smart_contract_storage.py  # Smart Contract storage implementation
│   ├── schemas/           # Data Transfer Objects
│   │   └── endpoints/     # Request/Response schemas
│   └── main.py           # Application entry point
├── contracts/             # Hardhat Solidity contracts
├── deploy/               # Hardhat deployment scripts
├── docker/               # Docker configurations
│   ├── Dockerfile.backend
│   └── Dockerfile.hardhat
├── hardhat.config.js     # Hardhat configuration
├── package.json          # Node.js dependencies
├── docker-compose.yml    # Multi-service orchestration
└── requirements.txt      # Python dependencies
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
- Node.js 18+ (for local Hardhat development)
- Python 3.13+ (for local development)

### Quick Start with Docker (Recommended)

1. **Clone and setup**:
   ```bash
   git clone <repository>
   cd fence-test
   ```

2. **Run with Docker Compose** (No additional configuration needed):
   ```bash
   docker compose up --build
   ```

   **What happens automatically:**
   - ✅ Hardhat local blockchain starts
   - ✅ Smart Contract compiles and deploys
   - ✅ FastAPI reads contract address and ABI automatically
   - ✅ Both services become available

3. **Access the services**:
   - **API Documentation**: http://localhost:8000/docs
   - **FastAPI Health**: http://localhost:8000/
   - **Hardhat Node**: http://localhost:8545
   - **Smart Contract**: Automatically deployed and connected

### Local Development

1. **Start Hardhat blockchain**:
   ```bash
   cd fence-test
   npm install
   npx hardhat node
   ```

2. **Deploy Smart Contract** (in another terminal):
   ```bash
   npx hardhat deploy --network localhost
   ```

3. **Start FastAPI** (in another terminal):
   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📡 **API Endpoints**

### POST /asset
Updates assets and calculates average interest rate, saving it to the Smart Contract.

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
Retrieves the current average interest rate from the Smart Contract.

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

### 1. **Smart Contract vs Database Storage**
- **Current**: Smart Contract with Hardhat local blockchain
- **Trade-off**: More complex setup, blockchain dependency, slower transactions
- **Rationale**: Meets the Smart Contract requirement, demonstrates Web3 integration
- **Alternative**: Database would be simpler and faster for production use

### 2. **Hardhat vs Ganache**
- **Choice**: Hardhat for local development
- **Trade-off**: More complex than Ganache, requires Node.js setup
- **Rationale**: Industry standard, better tooling, easier contract deployment
- **Benefits**: Automated deployment, better debugging, comprehensive testing

### 3. **Automatic Contract Discovery**
- **Choice**: Reading contract address and ABI from Hardhat artifacts
- **Trade-off**: Tight coupling with Hardhat deployment structure
- **Rationale**: Zero configuration, no manual setup required
- **Benefits**: Seamless integration, no environment variables needed

### 4. **API Key Authentication**
- **Choice**: Simple API key header authentication
- **Trade-off**: Not as secure as JWT tokens
- **Rationale**: Sufficient for technical test, easy to implement
- **Production**: Would use OAuth2/JWT with proper key management

### 5. **Fixed Private Key for Development**
- **Choice**: Using Hardhat's default private key
- **Trade-off**: Not realistic for production
- **Rationale**: Simplifies setup, works out of the box
- **Production**: Would use proper key management (HSM, key vaults)

### 6. **Decimal Precision Handling**
- **Choice**: Converting to uint256 with 2 decimal precision (multiply by 100)
- **Trade-off**: Limited to 2 decimal places
- **Rationale**: Smart contracts don't support floating point
- **Alternative**: Could use higher precision (multiply by 10000 for 4 decimals)

## 🏭 **Production Considerations**

### Security Enhancements
1. **Authentication**: Implement OAuth2/JWT with proper token management
2. **Private Key Management**: Use HSM or key vault services (AWS KMS, Azure Key Vault)
3. **Smart Contract Security**: Implement multi-signature wallets, access controls
4. **Rate Limiting**: Add request rate limiting (Redis-based)
5. **Input Sanitization**: Enhanced validation and sanitization
6. **HTTPS**: Force HTTPS in production
7. **API Versioning**: Implement proper API versioning strategy

### Performance Optimizations
1. **Blockchain Optimization**: 
   - Use Layer 2 solutions (Polygon, Arbitrum) for lower costs
   - Implement batch transactions
   - Optimize gas usage in Smart Contracts
2. **Caching**: Redis cache for frequently accessed data
3. **Async Operations**: Full async/await pattern throughout
4. **Monitoring**: APM tools (DataDog, New Relic) + blockchain monitoring
5. **Load Balancing**: Multiple instances behind load balancer

### Infrastructure
1. **Container Orchestration**: Kubernetes deployment
2. **Blockchain Infrastructure**: 
   - Production blockchain nodes (Infura, Alchemy)
   - Multi-chain support (Ethereum, Polygon, BSC)
   - Fallback mechanisms for blockchain outages
3. **Monitoring**: Prometheus + Grafana + blockchain explorers
4. **Logging**: Structured logging with ELK stack
5. **CI/CD**: Automated testing, contract verification, and deployment pipeline

### Scalability
1. **Horizontal Scaling**: Stateless application design
2. **Blockchain Scaling**: 
   - Layer 2 solutions for high throughput
   - Sharding strategies for large datasets
3. **Message Queues**: For async processing and event handling
4. **CDN**: For static content and caching

## 🧪 **Testing Strategy**

The current implementation includes:
- **Unit Tests**: Business logic and Smart Contract interaction testing
- **Integration Tests**: API endpoint testing with blockchain
- **Contract Tests**: Schema validation and Smart Contract function testing
- **End-to-End Tests**: Full flow from API to Smart Contract

For production:
- **Load Testing**: Performance under high traffic and blockchain congestion
- **Security Testing**: Smart Contract security audits, penetration testing
- **Chaos Engineering**: Resilience testing for blockchain outages
- **Gas Optimization**: Testing gas usage and optimization strategies

## 🔮 **Smart Contract Architecture**

The current implementation uses a clean separation of concerns:

```python
# Service layer remains unchanged
class InterestRateService:
    def __init__(self, storage: InterestRateStorage):
        self.storage = storage  # Abstract storage interface

# Smart Contract implementation
class SmartContractStorage(InterestRateStorage):
    def __init__(self, web3_client: Web3Client):
        self.web3_client = web3_client
    
    async def save_interest_rate(self, rate: Decimal, timestamp: str):
        # Interacts with Smart Contract
```

**Benefits:**
- ✅ **Easy to test**: Mock the storage layer
- ✅ **Easy to extend**: Add database layer alongside Smart Contract
- ✅ **Clean separation**: Business logic independent of storage technology

## 📝 **Assumptions Made**

1. **Interest Rate Calculation**: Simple arithmetic average (could be weighted)
2. **Asset IDs**: String-based unique identifiers
3. **Timestamps**: UTC timezone for consistency
4. **Decimal Precision**: Using Python Decimal, converted to uint256 with 2 decimal precision
5. **API Response**: JSON format with human-readable timestamps
6. **Blockchain Network**: Hardhat local development network (easily configurable for other networks)
7. **Smart Contract Owner**: Uses the deployer account for all transactions
8. **Gas Management**: Fixed gas limit suitable for development (configurable for production)

## 🎯 **Key Features Implemented**

1. ✅ **Smart Contract**: Solidity contract with updateInterestRate() and getInterestRate() functions
2. ✅ **FastAPI Endpoints**: POST /asset and GET /interest_rate as specified
3. ✅ **Automated Deployment**: Hardhat automatically deploys contracts on startup
4. ✅ **Zero Configuration**: No manual setup required - works out of the box
5. ✅ **Clean Architecture**: Service layer abstraction for easy testing and extension
6. ✅ **Comprehensive Error Handling**: Proper HTTP status codes and error messages
7. ✅ **API Documentation**: Auto-generated Swagger documentation
8. ✅ **Docker Integration**: Complete containerized solution

## 🚀 **Getting Started**

The fastest way to test the implementation:

```bash
# 1. Clone and start
git clone <repository>
cd fence-test
docker compose up --build

# 2. Test the API
curl -X POST "http://localhost:8000/asset" \
  -H "api_key: your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d '[{"id": "asset-1", "interest_rate": 100}, {"id": "asset-2", "interest_rate": 200}]'

# 3. Check the result
curl -X GET "http://localhost:8000/interest_rate" \
  -H "api_key: your-secret-api-key-here"
```

---

*This implementation successfully demonstrates Smart Contract integration with FastAPI, following clean architecture principles while meeting all technical exercise requirements.*

