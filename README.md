# Fence Test - Asset Interest Rate Management API

## Overview

This project implements a FastAPI application for managing financial assets and calculating average interest rates. Following the exercise instructions, I've created **two complete implementations** to demonstrate different approaches and technologies.

## 🚀 **Available Versions**

This repository contains **two complete implementations** of the same requirements:

### 📊 **Database Version** (`feat-database-version` branch)
- **Storage**: PostgreSQL database with SQLAlchemy ORM
- **Migrations**: Alembic for database schema management
- **Architecture**: Repository pattern with clean separation of concerns
- **Best for**: Production applications requiring ACID compliance and complex queries

### 🔗 **Smart Contract Version** (`feat-smartcontract-version` branch)  
- **Storage**: Solidity Smart Contract on Hardhat local blockchain
- **Deployment**: Automated contract deployment with hardhat-deploy
- **Architecture**: Web3 integration with singleton pattern optimization
- **Best for**: Decentralized applications and blockchain integration

## 📋 **API Endpoints**

Both versions implement the exact same API endpoints as specified in `INSTRUCTIONS.md`:

### POST /asset
Receives a list of assets and updates the average interest rate.

**Example**:
```bash
curl -X POST "http://localhost:8000/asset" \
  -H "api_key: your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d '[{"id": "id-1", "interest_rate": 100}, {"id": "id-2", "interest_rate": 10}]'
```

**Response**:
```json
{
  "message": "Average interest rate calculated and saved successfully"
}
```

### GET /interest_rate
Returns the current average interest rate.

**Example**:
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

## 🚀 **Quick Start**

### Option 1: Database Version
```bash
git checkout feat-database-version
cp .env.example .env
docker-compose up --build
```

### Option 2: Smart Contract Version
```bash
git checkout feat-smartcontract-version
cp .env.example .env
docker-compose up --build
```

Both versions will be available at:
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/

## 📊 **Version Comparison**

| Feature | Database Version | Smart Contract Version |
|---------|------------------|------------------------|
| **Storage** | PostgreSQL | Solidity Contract |
| **Persistence** | ACID compliant | Blockchain immutable |
| **Performance** | Fast queries | Slower transactions |
| **Setup** | Medium complexity | Low complexity (automated) |
| **Production Ready** | ✅ Yes | ⚠️ Needs mainnet |

## 🤝 **Choose Your Version**

- **Database Version**: For traditional web applications, production systems
- **Smart Contract Version**: For blockchain integration, DeFi applications

Each branch includes complete documentation, setup instructions, and Docker configuration.

---

*Both implementations demonstrate clean architecture principles while meeting all technical exercise requirements.*