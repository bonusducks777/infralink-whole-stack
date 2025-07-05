# InfraLink Network Configuration Guide

## Adding Hedera Testnet to MetaMask

To use InfraLink on Hedera testnet, you need to add the network to your wallet:

### Manual Configuration
1. Open MetaMask
2. Click the network dropdown (usually shows "Ethereum Mainnet")
3. Click "Add Network" or "Add a network manually"
4. Enter the following details:

```
Network Name: Hedera Testnet
New RPC URL: https://testnet.hashio.io/api
Chain ID: 296
Currency Symbol: HBAR
Block Explorer URL: https://hashscan.io/testnet
```

5. Click "Save"
6. Switch to the Hedera Testnet network

### Getting Test HBAR
1. Visit https://portal.hedera.com/
2. Create a testnet account or log in
3. Navigate to the testnet faucet
4. Request test HBAR for your wallet address

## Supported Networks in InfraLink

### Testnets (Recommended for Development)
- **Hedera Testnet**: Fast, low-cost testing with HBAR
- **Ethereum Sepolia**: Traditional Ethereum testnet with ETH

### Mainnets (Production Use)
- **Ethereum Mainnet**: High security, broad ecosystem
- **Polygon**: Lower fees, fast transactions
- **Optimism**: Layer 2 scaling with ETH
- **Arbitrum**: Layer 2 scaling with ETH
- **Base**: Coinbase's Layer 2 solution

## Configuration Files

### Device Monitor (Python)
Update `devicelocal.py`:
```python
# For Hedera testnet
INFURA_URL = "https://testnet.hashio.io/api"

# For Ethereum sepolia
INFURA_URL = "https://sepolia.infura.io/v3/YOUR_PROJECT_ID"
```

### Web Application
The web app automatically supports all configured networks. Users can switch between them using their wallet's network selector.

## Network-Specific Considerations

### Hedera Testnet
- **Currency**: HBAR (18 decimals)
- **Fees**: Very low transaction costs
- **Speed**: ~3-5 second finality
- **Faucet**: https://portal.hedera.com/
- **Explorer**: https://hashscan.io/testnet

### Ethereum Networks
- **Currency**: ETH (18 decimals) 
- **Fees**: Variable based on network congestion
- **Speed**: ~12-15 seconds per block
- **Faucets**: Various testnet faucets available
- **Explorer**: https://etherscan.io/ (mainnet) or https://sepolia.etherscan.io/ (testnet)

## Deployment Recommendations

### For Testing
1. **Start with Hedera Testnet** - Fast, cheap, and reliable
2. Get test HBAR from the official faucet
3. Deploy both InfraLink Info and Device contracts
4. Test full user flows including payments and whitelist management

### For Production
1. **Evaluate your needs**:
   - High security + broad ecosystem → Ethereum Mainnet
   - Lower fees + faster transactions → Polygon or Layer 2s
   - Enterprise features + sustainability → Hedera Mainnet
2. Ensure sufficient native token balance for deployments
3. Consider gas optimization for your contracts
4. Test thoroughly on testnets first

## Quick Setup Commands

### Add Hedera Testnet (via wallet)
```javascript
// For programmatic addition
await window.ethereum.request({
  method: 'wallet_addEthereumChain',
  params: [{
    chainId: '0x128', // 296 in hex
    chainName: 'Hedera Testnet',
    nativeCurrency: {
      name: 'HBAR',
      symbol: 'HBAR',
      decimals: 18
    },
    rpcUrls: ['https://testnet.hashio.io/api'],
    blockExplorerUrls: ['https://hashscan.io/testnet']
  }]
});
```

### Environment Variables
```bash
# For development
REACT_APP_HEDERA_TESTNET_RPC=https://testnet.hashio.io/api
REACT_APP_INFRALINK_INFO_ADDRESS=0x... # Your deployed Info contract
REACT_APP_DEFAULT_NETWORK=hedera-testnet
```
