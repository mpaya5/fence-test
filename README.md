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

## 📋 **Requirements Met**

Both versions implement the exact same API endpoints as specified in `INSTRUCTIONS.md`:

### POST /asset
Receives a list of assets and updates the average interest rate in the chosen storage backend.

**Example Request**:
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
Returns the interest rate value currently stored in the chosen backend.

**Example Request**:
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

## 🎯 **How to Choose Your Version**

### Choose **Database Version** if you want:
- ✅ **Production-ready** database solution
- ✅ **ACID compliance** and data integrity
- ✅ **Complex queries** and reporting capabilities
- ✅ **Familiar technology stack** (PostgreSQL + SQLAlchemy)
- ✅ **Easy debugging** and data inspection

### Choose **Smart Contract Version** if you want:
- ✅ **Blockchain integration** and Web3 capabilities
- ✅ **Decentralized data storage** 
- ✅ **Smart Contract development** experience
- ✅ **Hardhat ecosystem** familiarity
- ✅ **Modern Web3 tooling** and best practices

## 🚀 **Quick Start**

### Option 1: Database Version
```bash
git checkout feat-database-version
docker-compose up --build
```

### Option 2: Smart Contract Version
```bash
git checkout feat-smartcontract-version
docker-compose up --build
```

Both versions will be available at:
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/

## 🏗️ **Architecture Highlights**

### Database Version Features:
- **Clean Architecture** with Repository pattern
- **Alembic migrations** for schema management
- **Connection pooling** and production optimizations
- **Comprehensive error handling** and logging
- **Docker containerization** with PostgreSQL

### Smart Contract Version Features:
- **Solidity Smart Contract** with owner access control
- **Hardhat development environment** with automated deployment
- **Web3.py integration** with singleton pattern optimization
- **Zero-configuration setup** - works out of the box
- **Gas optimization** and transaction monitoring

## 🔧 **Technical Trade-offs**

### Database Version:
- **Pros**: ACID compliance, complex queries, familiar stack
- **Cons**: Centralized, requires database maintenance
- **Best for**: Traditional web applications, financial systems

### Smart Contract Version:
- **Pros**: Decentralized, immutable, transparent
- **Cons**: Gas costs, blockchain dependency, slower transactions
- **Best for**: DeFi applications, trustless systems

## 📊 **Implementation Comparison**

| Feature | Database Version | Smart Contract Version |
|---------|------------------|------------------------|
| **Storage** | PostgreSQL | Solidity Contract |
| **Persistence** | ACID compliant | Blockchain immutable |
| **Performance** | Fast queries | Slower transactions |
| **Setup Complexity** | Medium | Low (automated) |
| **Production Ready** | ✅ Yes | ⚠️ Needs mainnet |
| **Cost** | Infrastructure | Gas fees |
| **Debugging** | Easy (SQL) | Complex (blockchain) |

## 🧪 **Testing Both Versions**

Each branch includes:
- **Unit Tests**: Business logic and storage testing
- **Integration Tests**: API endpoint testing
- **Docker Setup**: Complete containerized environment
- **Documentation**: Comprehensive README with setup instructions

## 📝 **Development Notes**

Both implementations follow the same core principles:
- **Clean Architecture** with clear separation of concerns
- **Dependency Injection** for testability
- **Comprehensive Error Handling** with proper HTTP status codes
- **API Key Authentication** for security
- **Docker Containerization** for easy deployment

The main difference is in the storage layer:
- **Database**: Uses SQLAlchemy with Repository pattern
- **Smart Contract**: Uses Web3.py with direct contract interaction

## 🤝 **Contributing**

1. **Choose your preferred version** from the available branches
2. **Follow the README** in your chosen branch for specific setup
3. **Both versions** are complete and production-ready within their scope
4. **Architecture decisions** are documented in each branch's README

---

*Both implementations demonstrate clean architecture principles while meeting all technical exercise requirements. Choose the version that best fits your use case and technology preferences.*