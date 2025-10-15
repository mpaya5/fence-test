"""
Web3 client for interacting with the Interest Rate Smart Contract.
"""
import json
import os
from typing import Tuple, Optional
from decimal import Decimal
from web3 import Web3
from eth_account import Account
from app.core.config import settings
from app.core.logger import logger


class Web3Client:
    """Web3 client for smart contract interactions."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls, rpc_url: str = None, private_key: str = None):
        """Singleton pattern to ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super(Web3Client, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, rpc_url: str = None, private_key: str = None):
        """
        Initialize Web3 client (only once due to singleton pattern).
        
        Args:
            rpc_url: Ethereum RPC URL (uses settings if not provided)
            private_key: Private key for transactions (uses settings if not provided)
        """
        # Only initialize once
        if self._initialized:
            return
            
        # Use settings if parameters not provided
        rpc_url = rpc_url or settings.BLOCKCHAIN_RPC_URL
        private_key = private_key or settings.HARDHAT_PRIVATE_KEY
        
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        if not self.w3.is_connected():
            raise ConnectionError(f"Failed to connect to Ethereum node at {rpc_url}")
            
        # Read contract info from Hardhat deployments (only once)
        self.contract_address, self.abi = self._load_contract_info()
        self.account = Account.from_key(private_key)
        
        # Load contract
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=self.abi
        )
        
        logger.info(f"🔗 Connected to contract at: {self.contract_address}")
        self._initialized = True
    
    def _load_contract_info(self) -> tuple[str, list]:
        """Load contract address and ABI from Hardhat deployments."""
        try:
            # Try localhost first (for local development)
            deployment_path = "/app/deployments/localhost/InterestRateContract.json"
            
            if not os.path.exists(deployment_path):
                # Fallback to any network
                deployments_dir = "/app/deployments"
                if os.path.exists(deployments_dir):
                    for network_dir in os.listdir(deployments_dir):
                        network_path = os.path.join(deployments_dir, network_dir)
                        if os.path.isdir(network_path):
                            contract_path = os.path.join(network_path, "InterestRateContract.json")
                            if os.path.exists(contract_path):
                                deployment_path = contract_path
                                break
            
            if not os.path.exists(deployment_path):
                raise FileNotFoundError(f"Contract deployment not found at {deployment_path}")
            
            with open(deployment_path, 'r') as f:
                contract_data = json.load(f)
            
            address = contract_data['address']
            abi = contract_data['abi']
            
            logger.info(f"📄 Loaded contract info from: {deployment_path}")
            logger.info(f"📍 Contract address: {address}")
            
            return address, abi
            
        except Exception as e:
            logger.error(f"❌ Failed to load contract info: {str(e)}")
            raise Exception(f"Could not load contract deployment info: {str(e)}")
    
    def update_interest_rate(self, rate: Decimal, timestamp: int, wait_for_confirmation: bool = True) -> tuple[str, dict]:
        """
        Update interest rate in smart contract.
        
        Args:
            rate: Interest rate as Decimal (will be converted to uint256 with 2 decimals precision)
            timestamp: Unix timestamp
            wait_for_confirmation: Whether to wait for transaction confirmation
            
        Returns:
            Tuple of (transaction_hash, transaction_receipt)
        """
        # Convert Decimal to uint256 with 2 decimal precision
        # e.g., 55.25 -> 5525 (multiply by 100)
        rate_uint = int(rate * Decimal('100'))
        
        # Build transaction
        transaction = self.contract.functions.updateInterestRate(
            rate_uint, timestamp
        ).build_transaction({
            'from': self.account.address,
            'gas': settings.GAS_LIMIT,
            'gasPrice': self.w3.eth.gas_price,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
        })
        
        # Sign and send transaction
        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        receipt = None
        if wait_for_confirmation:
            # Wait for transaction receipt with timeout
            try:
                receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)  # 2 minutes timeout
            except Exception as e:
                raise Exception(f"Transaction confirmation timeout: {str(e)}")
        
        return tx_hash.hex(), receipt
    
    def get_interest_rate(self) -> Optional[Tuple[Decimal, int]]:
        """
        Get current interest rate from smart contract.
        
        Returns:
            Tuple of (rate as Decimal, timestamp) or None if no data
        """
        try:
            rate_uint, timestamp = self.contract.functions.getInterestRate().call()
            
            # Convert uint256 back to Decimal (divide by 100)
            rate = Decimal(rate_uint) / Decimal('100')
            
            # Check if we have valid data (not default values)
            if rate == 0 and timestamp == 0:
                return None
                
            return rate, timestamp
            
        except Exception:
            return None
    
