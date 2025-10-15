import json
import os
from pathlib import Path

# Load ABI from JSON file
_abi_path = Path(__file__).parent / "interest_rate_contract.json"
with open(_abi_path, 'r') as f:
    ABI = json.load(f)
