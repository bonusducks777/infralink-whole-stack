# InfraLink Multi-Chain Configuration

## Supported Networks and Native Token Specifications

### Ethereum Networks
- **Ethereum Mainnet**
  - Chain ID: `1`
  - Native Token: `ETH`
  - Decimals: `18`
  - Smallest Unit: `wei` (1 ETH = 10^18 wei)
  - RPC: `https://mainnet.infura.io/v3/YOUR_PROJECT_ID`

- **Ethereum Sepolia Testnet**
  - Chain ID: `11155111`
  - Native Token: `ETH`
  - Decimals: `18`
  - Smallest Unit: `wei` (1 ETH = 10^18 wei)
  - RPC: `https://sepolia.infura.io/v3/YOUR_PROJECT_ID`

- **Ethereum Goerli Testnet** (Deprecated but still supported)
  - Chain ID: `5`
  - Native Token: `ETH`
  - Decimals: `18`
  - Smallest Unit: `wei` (1 ETH = 10^18 wei)
  - RPC: `https://goerli.infura.io/v3/YOUR_PROJECT_ID`

### Hedera Networks
- **Hedera Testnet**
  - Chain ID: `296`
  - Native Token: `HBAR`
  - Decimals: `8`
  - Smallest Unit: `tinybar` (1 HBAR = 10^8 tinybars)
  - RPC: `https://testnet.hashio.io/api`
  - Block Explorer: `https://hashscan.io/testnet`

- **Hedera Mainnet**
  - Chain ID: `295`
  - Native Token: `HBAR`
  - Decimals: `8`
  - Smallest Unit: `tinybar` (1 HBAR = 10^8 tinybars)
  - RPC: `https://mainnet.hashio.io/api`
  - Block Explorer: `https://hashscan.io/mainnet`

### Other EVM Networks (Examples)
- **Polygon**
  - Chain ID: `137`
  - Native Token: `MATIC`
  - Decimals: `18`
  - Smallest Unit: `wei` (1 MATIC = 10^18 wei)

- **BSC (Binance Smart Chain)**
  - Chain ID: `56`
  - Native Token: `BNB`
  - Decimals: `18`
  - Smallest Unit: `wei` (1 BNB = 10^18 wei)

- **Avalanche**
  - Chain ID: `43114`
  - Native Token: `AVAX`
  - Decimals: `18`
  - Smallest Unit: `wei` (1 AVAX = 10^18 wei)

## Fee Calculation Examples

### For 0.001 Native Token per Second

| Network | Chain ID | Token | Decimals | Fee in Smallest Unit | Human Readable |
|---------|----------|-------|----------|---------------------|----------------|
| Ethereum | 1, 5, 11155111 | ETH | 18 | 1000000000000000 | 0.001 ETH |
| Hedera | 295, 296 | HBAR | 8 | 100000 | 0.001 HBAR |
| Polygon | 137 | MATIC | 18 | 1000000000000000 | 0.001 MATIC |
| BSC | 56 | BNB | 18 | 1000000000000000 | 0.001 BNB |
| Avalanche | 43114 | AVAX | 18 | 1000000000000000 | 0.001 AVAX |

### Duration Examples (10 minutes = 600 seconds)

| Network | Fee/Second | Total Cost (Smallest Unit) | Total Cost (Human) |
|---------|------------|----------------------------|-------------------|
| Ethereum | 1000000000000000 | 600000000000000000 | 0.6 ETH |
| Hedera | 100000 | 60000000 | 0.6 HBAR |
| Polygon | 1000000000000000 | 600000000000000000 | 0.6 MATIC |

## Contract Deployment Parameters

### Native Token Deployment (Recommended)

```solidity
// For ALL networks using native tokens:
// _token = 0x0000000000000000000000000000000000000000 (zero address)

// Ethereum networks (18 decimals):
// For 0.001 ETH/second: _feePerSecond = 1000000000000000
// For 0.0005 ETH/second: _whitelistFeePerSecond = 500000000000000

// Hedera networks (8 decimals):
// For 0.001 HBAR/second: _feePerSecond = 100000
// For 0.0005 HBAR/second: _whitelistFeePerSecond = 50000

// Other 18-decimal networks (Polygon, BSC, Avalanche):
// For 0.001 TOKEN/second: _feePerSecond = 1000000000000000
// For 0.0005 TOKEN/second: _whitelistFeePerSecond = 500000000000000
```

### ERC20 Token Deployment

```solidity
// For ERC20 tokens, use the token's contract address
// _token = 0x... (your ERC20 token address)

// Fee calculation depends on token's decimals:
// For token with 18 decimals: 0.001 TOKEN = 1000000000000000
// For token with 6 decimals: 0.001 TOKEN = 1000
// For token with 8 decimals: 0.001 TOKEN = 100000
```

## Implementation Notes

### Smart Contract Network Detection
The updated contract automatically detects the network and sets appropriate values:

```solidity
if (block.chainid == 296 || block.chainid == 295) {
    // Hedera networks
    tokenName = "HBAR";
    tokenSymbol = "HBAR";
    tokenDecimals = 8;
} else {
    // Default to Ethereum-style networks
    tokenName = "Ether";
    tokenSymbol = "ETH";
    tokenDecimals = 18;
}
```

### Frontend Network Detection
The web app should detect the network and show appropriate currency symbols and decimal formatting.

### Python Monitor Network Detection
The Python monitor should format amounts based on the contract's reported decimals, not assume 18 decimals.

## Testing Checklist

- [ ] Deploy on Ethereum testnet with 18-decimal fees
- [ ] Deploy on Hedera testnet with 8-decimal fees
- [ ] Verify frontend shows correct currency symbols
- [ ] Verify Python monitor formats amounts correctly
- [ ] Test payments work with correct amounts
- [ ] Verify error messages show correct currency names
