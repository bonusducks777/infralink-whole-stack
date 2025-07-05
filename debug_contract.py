#!/usr/bin/env python3
"""
Debug script to check contract deployment values with network awareness
"""
import sys
from web3 import Web3
from network_utils import (
    get_network_info, validate_deployment_fee, 
    format_native_amount, get_currency_symbol,
    print_deployment_guide
)

# Configuration
HEDERA_TESTNET_RPC = "https://testnet.hashio.io/api"
CONTRACT_ADDRESS = "0xaff84326fc701dfb3c5881b2749dba27e9a98978"

# Minimal ABI for debugging
MINIMAL_ABI = [
    {
        "inputs": [],
        "name": "feePerSecond",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "whitelistFeePerSecond",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "useNativeToken",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "tokenSymbol",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "tokenDecimals",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "deviceName",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    }
]

def main():
    print("=== InfraLink Contract Debug ===")
    print(f"Contract Address: {CONTRACT_ADDRESS}")
    print(f"RPC URL: {HEDERA_TESTNET_RPC}")
    print()
    
    # Initialize Web3
    w3 = Web3(Web3.HTTPProvider(HEDERA_TESTNET_RPC))
    
    if not w3.is_connected():
        print("❌ Failed to connect to Hedera testnet")
        sys.exit(1)
    
    print("✅ Connected to network")
    chain_id = w3.eth.chain_id
    network_info = get_network_info(chain_id)
    print(f"Chain ID: {chain_id}")
    print(f"Network: {network_info['name']}")
    print(f"Native Currency: {network_info['currency']}")
    print(f"Expected Decimals: {network_info['decimals']}")
    print()
    
    # Initialize contract
    try:
        contract_address = w3.to_checksum_address(CONTRACT_ADDRESS.lower())
        contract = w3.eth.contract(address=contract_address, abi=MINIMAL_ABI)
        print("✅ Contract initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize contract: {e}")
        sys.exit(1)
    
    print()
    print("=== Contract Values ===")
    
    try:
        # Get basic info
        device_name = contract.functions.deviceName().call()
        print(f"Device Name: {device_name}")
        
        use_native = contract.functions.useNativeToken().call()
        print(f"Use Native Token: {use_native}")
        
        token_symbol = contract.functions.tokenSymbol().call()
        print(f"Token Symbol: {token_symbol}")
        
        token_decimals = contract.functions.tokenDecimals().call()
        print(f"Token Decimals: {token_decimals}")
        
        # Get fee info
        fee_per_second = contract.functions.feePerSecond().call()
        whitelist_fee = contract.functions.whitelistFeePerSecond().call()
        
        print(f"Fee Per Second (raw): {fee_per_second}")
        print(f"Whitelist Fee Per Second (raw): {whitelist_fee}")
        
        # Calculate human-readable fees using network-aware formatting
        fee_human_formatted = format_native_amount(fee_per_second, chain_id, token_decimals)
        whitelist_fee_human_formatted = format_native_amount(whitelist_fee, chain_id, token_decimals)
        
        # Get network-appropriate currency symbol
        currency_symbol = get_currency_symbol(chain_id, token_symbol)
        
        print(f"Fee Per Second (human): {fee_human_formatted} {currency_symbol}")
        print(f"Whitelist Fee Per Second (human): {whitelist_fee_human_formatted} {currency_symbol}")
        
        print()
        print("=== Test Calculation ===")
        
        # Test calculation for 10 minutes (600 seconds)
        duration = 600
        total_cost_raw = fee_per_second * duration
        total_cost_human_formatted = format_native_amount(total_cost_raw, chain_id, token_decimals)
        
        print(f"Duration: {duration} seconds (10 minutes)")
        print(f"Total Cost (raw): {total_cost_raw}")
        print(f"Total Cost (human): {total_cost_human_formatted} {currency_symbol}")
        
        # Expected values based on network
        expected_fee = 0.001
        expected_total = expected_fee * duration
        
        print()
        print("=== Expected vs Actual ===")
        print(f"Expected fee per second: {expected_fee} {currency_symbol}")
        print(f"Actual fee per second: {fee_human_formatted} {currency_symbol}")
        print(f"Expected total cost: {expected_total} {currency_symbol}")
        print(f"Actual total cost: {total_cost_human_formatted} {currency_symbol}")
        
        # Convert human-formatted strings to float for comparison
        try:
            actual_fee_float = float(fee_human_formatted)
            actual_total_float = float(total_cost_human_formatted)
            
            if abs(actual_fee_float - expected_fee) < 0.0001:
                print("✅ Fee per second matches expected value")
            else:
                print("❌ Fee per second does NOT match expected value")
                
            if abs(actual_total_float - expected_total) < 0.0001:
                print("✅ Total cost matches expected value")
            else:
                print("❌ Total cost does NOT match expected value")
        except ValueError:
            print("⚠️  Could not parse formatted amounts for comparison")
            
    except Exception as e:
        print(f"❌ Error reading contract values: {e}")
        sys.exit(1)
    
    print()
    print("=== Network-Specific Deployment Guide ===")
    print_deployment_guide(chain_id)

if __name__ == "__main__":
    main()
