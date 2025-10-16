# Fence Test - Smart Contract Asset Interest Rate Management API

## Overview

This project implements a FastAPI application with a Smart Contract backend for managing financial assets and calculating average interest rates. Following the exercise instructions, I've implemented the Smart Contract version as the primary solution, using Hardhat for local blockchain development with automated contract deployment.

## My Reasoning and Assumptions

### 📝 **Key Assumptions Made**

1. **Interest Rate Calculation**: Simple arithmetic average of all provided assets
2. **Smart Contract Storage**: Solidity contract for decentralized data persistence
3. **Blockchain Network**: Hardhat local development network (industry standard)
4. **API Authentication**: Simple API key for the technical test context
5. **Response Format**: JSON with clear confirmation messages and timestamps
6. **Development Tooling**: Hardhat + hardhat-deploy for familiarity and superior tooling over deprecated Ganache
7. **Error Handling**: Comprehensive validation with meaningful error messages
8. **Docker Deployment**: Containerized solution for easy setup and consistency

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
├── smart_contracts/             # Smart Contract Integration
│   ├── client/                 # Web3 client for blockchain interaction
│   ├── contracts/              # Solidity contract source
│   └── smart_contract_storage.py # Smart Contract storage implementation
├── schemas/                     # Data Transfer Objects
│   └── endpoints/              # Request/Response schemas
└── main.py                     # Application entry point
├── contracts/                  # Hardhat Solidity contracts
├── deploy/                    # Hardhat deployment scripts
├── docker/                    # Docker configurations
│   ├── Dockerfile.backend
│   └── Dockerfile.hardhat
├── hardhat.config.js          # Hardhat configuration
├── package.json               # Node.js dependencies
├── docker-compose.yml         # Multi-service orchestration
└── requirements.txt           # Python dependencies
```

### 🎯 **Design Principles Applied**

1. **Single Responsibility**: Each layer has one clear purpose
2. **Dependency Injection**: Services are injected, not instantiated directly
3. **Smart Contract Abstraction**: Clean separation between API and blockchain logic
4. **Clean Separation**: Business logic isolated from infrastructure concerns

## Trade-offs Considered

### 1. **Smart Contract vs Database Storage**
- **Choice**: Smart Contract with Hardhat local blockchain
- **Trade-off**: More complex setup, blockchain dependency, slower transactions
- **Rationale**: Meets the Smart Contract requirement, demonstrates Web3 integration
- **Alternative**: Database would be simpler and faster for production use

### 2. **Hardhat vs Ganache**
- **Choice**: Hardhat for local development
- **Trade-off**: More complex than Ganache, requires Node.js setup
- **Rationale**: 
  - **Industry Standard**: Hardhat is the current industry standard for Ethereum development
  - **Ganache Obsolete**: Ganache is deprecated and no longer maintained
  - **Personal Experience**: Familiar tooling from previous projects
  - **Better Tooling**: Superior debugging, testing, and deployment capabilities
- **Benefits**: 
  - Automated deployment with `hardhat-deploy` plugin
  - Better debugging with built-in console.log support
  - Comprehensive testing framework
  - Easy integration with CI/CD pipelines
- **Future Enhancement**: Could add Geth for ephemeral nodes if needed

### 3. **Automatic Contract Discovery**
- **Choice**: Reading contract address and ABI from Hardhat artifacts
- **Trade-off**: Tight coupling with Hardhat deployment structure
- **Rationale**: Zero configuration, no manual setup required
- **Benefits**: Seamless integration, no environment variables needed

### 4. **Simple vs Complex Authentication**
- **Choice**: API key authentication
- **Trade-off**: Less secure than OAuth2/JWT tokens
- **Rationale**: Appropriate for technical test, easy to implement and understand
- **Production**: Would upgrade to proper authentication system

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

2. **Start the application**:
   ```bash
   docker-compose up --build
   ```

   **What happens automatically:**
   - ✅ Hardhat local blockchain starts
   - ✅ Smart Contract compiles and deploys
   - ✅ FastAPI reads contract address and ABI automatically
   - ✅ Both services become available

3. **Access the services**:
   - **API Documentation**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/
   - **Hardhat Node**: http://localhost:8545
   - **Smart Contract**: Automatically deployed and connected

### Environment Variables

Key environment variables (optional - defaults provided):
- `API_KEY_AUTH`: Your API key for authentication (default: your-secret-api-key-here)
- `BLOCKCHAIN_RPC_URL`: Hardhat node URL (default: http://hardhat-node:8545)
- `HARDHAT_PRIVATE_KEY`: Private key for transactions (default: Hardhat's first account)
- All settings have sensible defaults for development

## API Endpoints

### POST /asset
Receives a list of assets and updates the average interest rate in the Smart Contract.

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
Returns the interest rate value currently stored in the Smart Contract.

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

1. **POST assets** → Confirms calculation and saves to Smart Contract
2. **GET interest_rate** → Retrieves the current stored rate from blockchain
3. **POST new assets** → Overwrites previous rate with new average
4. **GET interest_rate** → Shows updated rate from Smart Contract

## How I Would Productionize This Solution

### 🔒 **Security Enhancements**
1. **Authentication**: Replace API key with OAuth2/JWT tokens
2. **Private Key Management**: Use HSM or key vault services (AWS KMS, Azure Key Vault)
3. **Smart Contract Security**: Implement multi-signature wallets, access controls
4. **Input Validation**: Enhanced sanitization and validation
5. **HTTPS**: Force TLS encryption in production
6. **Rate Limiting**: Add request rate limiting (Redis-based)
7. **API Versioning**: Implement proper API versioning strategy

### ⚡ **Blockchain & Performance Optimizations**
1. **Blockchain Infrastructure**: 
   - Use Layer 2 solutions (Polygon, Arbitrum) for lower costs
   - Implement batch transactions
   - Optimize gas usage in Smart Contracts
   - Production blockchain nodes (Infura, Alchemy)
   - Multi-chain support (Ethereum, Polygon, BSC)
   - Fallback mechanisms for blockchain outages
2. **Web3Client Optimization**: 
   - Connection pooling for blockchain interactions
   - Transaction retry mechanisms
   - Gas price optimization strategies
3. **Caching**: Redis cache for frequently accessed blockchain data
4. **Async Operations**: Full async/await pattern throughout

### 🏗️ **Infrastructure & Deployment**
1. **Container Orchestration**: Kubernetes for scalable deployment
2. **Blockchain Infrastructure**: 
   - Production blockchain nodes (Infura, Alchemy)
   - Multi-chain support (Ethereum, Polygon, BSC)
   - Fallback mechanisms for blockchain outages
3. **CI/CD Pipeline**: Automated testing, contract verification, and deployment pipeline
4. **Monitoring**: Prometheus + Grafana + blockchain explorers
5. **Logging**: Structured logging with ELK stack
6. **Backup Strategy**: Automated blockchain state monitoring and disaster recovery

### 📈 **Scalability Considerations**
1. **Horizontal Scaling**: Stateless application design supports multiple instances
2. **Blockchain Scaling**: 
   - Layer 2 solutions for high throughput
   - Sharding strategies for large datasets
3. **Load Balancing**: Multiple application instances behind load balancer
4. **Message Queues**: For async processing and event handling

### 🧪 **Testing & Quality Assurance**
1. **Unit Tests**: Business logic and Smart Contract interaction testing
2. **Integration Tests**: End-to-end API testing with blockchain
3. **Contract Tests**: Schema validation and Smart Contract function testing
4. **Load Testing**: Performance under high traffic and blockchain congestion
5. **Security Testing**: Smart Contract security audits, penetration testing
6. **Chaos Engineering**: Resilience testing for blockchain outages
7. **Gas Optimization**: Testing gas usage and optimization strategies

### 🔄 **CI/CD Pipeline & Quality Gates**
1. **GitHub Actions Workflows**:
   - **Linting & Formatting**: Automated code quality checks with Black, isort, flake8
   - **Pre-commit Hooks**: Local validation before commits (Black, isort, mypy, security scans)
   - **Automated Testing**: Unit tests, integration tests, and Smart Contract tests on every PR
   - **Security Scanning**: Dependabot for dependency updates, CodeQL for security analysis
   - **Contract Verification**: Automated Smart Contract verification on testnets
2. **Branch Protection Rules**:
   - **Required Status Checks**: All workflows must pass before merge
   - **Required Reviews**: At least 1 approved review for main branch
   - **Up-to-date Branches**: PR must be up-to-date with main before merge
   - **Dismiss Stale Reviews**: Reviews dismissed when new commits are pushed
3. **Quality Gates**:
   - **Code Coverage**: Test coverage requirement
   - **Security Checks**: No high/critical vulnerabilities allowed
   - **Performance Tests**: API response time and blockchain transaction validation
   - **Contract Tests**: Smart Contract function testing and gas optimization

## Technical Implementation Details

### 🔗 **Smart Contract Schema**
```solidity
contract InterestRateContract {
    uint256 private currentRate;
    uint256 private lastUpdated;
    address private owner;
    
    function updateInterestRate(uint256 newRate, uint256 timestamp) external onlyOwner;
    function getInterestRate() external view returns (uint256 rate, uint256 timestamp);
}
```

### 🔄 **Data Flow**
1. **POST /asset**: FastAPI → Service → SmartContractStorage → Web3Client → Hardhat Blockchain
2. **GET /interest_rate**: FastAPI → Service → SmartContractStorage → Web3Client → Hardhat Blockchain
3. **Deployment**: Hardhat automatically compiles and deploys contracts on startup

### 🛠️ **Key Technologies Used**
- **FastAPI**: Modern Python web framework with automatic API documentation
- **Web3.py**: Python library for Ethereum blockchain interaction
- **Hardhat**: Ethereum development environment and testing framework
- **Solidity**: Smart contract programming language
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
# Stored in Smart Contract with current timestamp
```

---

*This implementation demonstrates Smart Contract integration with FastAPI, following clean architecture principles while meeting all technical exercise requirements.*

