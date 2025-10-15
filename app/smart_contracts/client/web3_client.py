"""
Web3 client for interacting with the Interest Rate Smart Contract.
"""
import json
import os
from typing import Tuple, Optional
from decimal import Decimal
from web3 import Web3
from eth_account import Account
from ..abi import ABI
from app.core.config import settings


class Web3Client:
    """Web3 client for smart contract interactions."""
    
    def __init__(self, rpc_url: str, contract_address: str, private_key: str):
        """
        Initialize Web3 client.
        
        Args:
            rpc_url: Ethereum RPC URL
            contract_address: Smart contract address
            private_key: Private key for transactions
        """
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        if not self.w3.is_connected():
            raise ConnectionError(f"Failed to connect to Ethereum node at {rpc_url}")
            
        self.contract_address = contract_address
        self.account = Account.from_key(private_key)
        
        # Load contract
        self.contract = self.w3.eth.contract(
            address=contract_address,
            abi=ABI
        )
    
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
    
