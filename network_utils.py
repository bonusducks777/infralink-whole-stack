"""
Network configuration and utilities for InfraLink
Handles multi-chain compatibility and proper fee calculations
"""

# Network configurations
NETWORK_CONFIG = {
    # Ethereum Mainnet
    1: {
        'name': 'Ethereum Mainnet',
        'currency': 'ETH',
        'decimals': 18,
        'rpc_url': 'https://mainnet.infura.io/v3/YOUR_PROJECT_ID',
        'explorer': 'https://etherscan.io'
    },
    # Ethereum Goerli Testnet
    5: {
        'name': 'Ethereum Goerli',
        'currency': 'ETH',
        'decimals': 18,
        'rpc_url': 'https://goerli.infura.io/v3/YOUR_PROJECT_ID',
        'explorer': 'https://goerli.etherscan.io'
    },
    # Ethereum Sepolia Testnet
    11155111: {
        'name': 'Ethereum Sepolia',
        'currency': 'ETH',
        'decimals': 18,
        'rpc_url': 'https://sepolia.infura.io/v3/YOUR_PROJECT_ID',
        'explorer': 'https://sepolia.etherscan.io'
    },
    # Hedera Mainnet
    295: {
        'name': 'Hedera Mainnet',
        'currency': 'HBAR',
        'decimals': 8,
        'rpc_url': 'https://mainnet.hashio.io/api',
        'explorer': 'https://hashscan.io/mainnet'
    },
    # Hedera Testnet
    296: {
        'name': 'Hedera Testnet',
        'currency': 'HBAR',
        'decimals': 8,
        'rpc_url': 'https://testnet.hashio.io/api',
        'explorer': 'https://hashscan.io/testnet'
    },
    # Polygon Mainnet
    137: {
        'name': 'Polygon',
        'currency': 'MATIC',
        'decimals': 18,
        'rpc_url': 'https://polygon-rpc.com/',
        'explorer': 'https://polygonscan.com'
    },
    # BSC Mainnet
    56: {
        'name': 'Binance Smart Chain',
        'currency': 'BNB',
        'decimals': 18,
        'rpc_url': 'https://bsc-dataseed.binance.org/',
        'explorer': 'https://bscscan.com'
    },
    # Avalanche Mainnet
    43114: {
        'name': 'Avalanche',
        'currency': 'AVAX',
        'decimals': 18,
        'rpc_url': 'https://api.avax.network/ext/bc/C/rpc',
        'explorer': 'https://snowtrace.io'
    }
}

def get_network_info(chain_id):
    """Get network information by chain ID"""
    return NETWORK_CONFIG.get(chain_id, {
        'name': f'Unknown Network (Chain ID: {chain_id})',
        'currency': 'UNKNOWN',
        'decimals': 18,  # Default to 18 decimals
        'rpc_url': None,
        'explorer': None
    })

def calculate_fee_for_network(human_fee_per_second, chain_id):
    """
    Calculate the fee in smallest units for a given network
    
    Args:
        human_fee_per_second (float): Fee in human-readable format (e.g., 0.001)
        chain_id (int): Network chain ID
        
    Returns:
        int: Fee in smallest units (wei, tinybars, etc.)
    """
    network = get_network_info(chain_id)
    return int(human_fee_per_second * (10 ** network['decimals']))

def format_native_amount(amount, chain_id, contract_decimals=None):
    """
    Format native token amount for display
    
    Args:
        amount (int): Amount in smallest units
        chain_id (int): Network chain ID
        contract_decimals (int, optional): Decimals from contract (overrides network default)
        
    Returns:
        str: Formatted amount with appropriate precision
    """
    network = get_network_info(chain_id)
    decimals = contract_decimals if contract_decimals is not None else network['decimals']
    
    if amount == 0:
        return "0"
    
    # Convert to decimal with proper precision
    decimal_amount = amount / (10 ** decimals)
    
    # Format with appropriate decimal places
    if decimal_amount >= 1:
        return f"{decimal_amount:.6f}"
    else:
        return f"{decimal_amount:.8f}"

def get_currency_symbol(chain_id, contract_symbol=None):
    """
    Get currency symbol for the network
    
    Args:
        chain_id (int): Network chain ID
        contract_symbol (str, optional): Symbol from contract (overrides network default)
        
    Returns:
        str: Currency symbol
    """
    if contract_symbol:
        return contract_symbol
    
    network = get_network_info(chain_id)
    return network['currency']

def validate_deployment_fee(human_fee, chain_id):
    """
    Validate and convert human-readable fee to contract deployment format
    
    Args:
        human_fee (float): Fee in human format (e.g., 0.001)
        chain_id (int): Target network chain ID
        
    Returns:
        dict: Deployment information
    """
    network = get_network_info(chain_id)
    fee_in_smallest = calculate_fee_for_network(human_fee, chain_id)
    
    return {
        'network_name': network['name'],
        'currency': network['currency'],
        'decimals': network['decimals'],
        'human_fee': f"{human_fee} {network['currency']}/second",
        'contract_fee': fee_in_smallest,
        'example_10min_cost': fee_in_smallest * 600,
        'example_10min_human': f"{human_fee * 600} {network['currency']}"
    }

# Pre-calculated fee examples for common rates
COMMON_FEES = {
    # 0.001 token per second
    'low': {
        1: 1000000000000000,      # Ethereum: 0.001 ETH
        5: 1000000000000000,      # Goerli: 0.001 ETH
        11155111: 1000000000000000, # Sepolia: 0.001 ETH
        295: 100000,              # Hedera Mainnet: 0.001 HBAR
        296: 100000,              # Hedera Testnet: 0.001 HBAR
        137: 1000000000000000,    # Polygon: 0.001 MATIC
        56: 1000000000000000,     # BSC: 0.001 BNB
        43114: 1000000000000000,  # Avalanche: 0.001 AVAX
    },
    # 0.01 token per second
    'medium': {
        1: 10000000000000000,     # Ethereum: 0.01 ETH
        5: 10000000000000000,     # Goerli: 0.01 ETH
        11155111: 10000000000000000, # Sepolia: 0.01 ETH
        295: 1000000,             # Hedera Mainnet: 0.01 HBAR
        296: 1000000,             # Hedera Testnet: 0.01 HBAR
        137: 10000000000000000,   # Polygon: 0.01 MATIC
        56: 10000000000000000,    # BSC: 0.01 BNB
        43114: 10000000000000000, # Avalanche: 0.01 AVAX
    },
    # 0.1 token per second
    'high': {
        1: 100000000000000000,    # Ethereum: 0.1 ETH
        5: 100000000000000000,    # Goerli: 0.1 ETH
        11155111: 100000000000000000, # Sepolia: 0.1 ETH
        295: 10000000,            # Hedera Mainnet: 0.1 HBAR
        296: 10000000,            # Hedera Testnet: 0.1 HBAR
        137: 100000000000000000,  # Polygon: 0.1 MATIC
        56: 100000000000000000,   # BSC: 0.1 BNB
        43114: 100000000000000000, # Avalanche: 0.1 AVAX
    }
}

def get_suggested_fee(chain_id, rate_level='low'):
    """
    Get suggested fee for a network
    
    Args:
        chain_id (int): Network chain ID
        rate_level (str): 'low', 'medium', or 'high'
        
    Returns:
        int: Suggested fee in smallest units
    """
    if rate_level not in COMMON_FEES:
        rate_level = 'low'
    
    return COMMON_FEES[rate_level].get(chain_id, COMMON_FEES[rate_level][1])  # Default to Ethereum rate

def print_deployment_guide(target_chain_id):
    """Print deployment guide for a specific network"""
    network = get_network_info(target_chain_id)
    
    print(f"\n=== Deployment Guide for {network['name']} ===")
    print(f"Chain ID: {target_chain_id}")
    print(f"Native Token: {network['currency']}")
    print(f"Decimals: {network['decimals']}")
    print(f"RPC URL: {network['rpc_url']}")
    print()
    
    print("Constructor Parameters for Native Token Usage:")
    print("_token = 0x0000000000000000000000000000000000000000  // Zero address for native token")
    print()
    
    for rate_name, rate_value in [('low', 0.001), ('medium', 0.01), ('high', 0.1)]:
        fee = get_suggested_fee(target_chain_id, rate_name)
        print(f"For {rate_value} {network['currency']}/second ({rate_name} rate):")
        print(f"  _feePerSecond = {fee}")
        print(f"  10 minutes cost: {fee * 600} ({rate_value * 600} {network['currency']})")
        print()

if __name__ == "__main__":
    # Example usage and testing
    print("=== InfraLink Network Configuration ===")
    
    # Test network detection
    test_chains = [1, 296, 137, 56]
    for chain_id in test_chains:
        info = get_network_info(chain_id)
        print(f"Chain {chain_id}: {info['name']} ({info['currency']}, {info['decimals']} decimals)")
    
    print("\n=== Fee Calculation Examples ===")
    
    # Test fee calculations
    human_fee = 0.001
    for chain_id in test_chains:
        contract_fee = calculate_fee_for_network(human_fee, chain_id)
        network = get_network_info(chain_id)
        print(f"{network['name']}: {human_fee} {network['currency']}/sec = {contract_fee} smallest units")
    
    print("\n=== Deployment Guides ===")
    
    # Print deployment guides for main networks
    for chain_id in [1, 296]:  # Ethereum Mainnet and Hedera Testnet
        print_deployment_guide(chain_id)
