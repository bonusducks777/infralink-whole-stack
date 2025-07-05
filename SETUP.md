# InfraLink v2.0 Deployment & Setup Guide

## 📋 Prerequisites

1. **Node.js** (v18 or higher)
2. **Python** (v3.8 or higher)
3. **Web3 Wallet** (MetaMask, WalletConnect compatible)
4. **Blockchain Node Access** (Infura, Alchemy, Hedera testnet, or local node)
5. **Solidity Compiler** (for contract deployment)

## 🌐 Supported Networks

- **Ethereum Mainnet/Testnets** (Sepolia, Goerli)
- **Hedera Testnet** (Chain ID: 296, Currency: HBAR)
- **Local Development** (Ganache, Hardhat)
- **Other EVM-compatible networks**

## 🚀 Quick Start

### 1. Deploy Smart Contracts

#### Deploy InfraLink Info Contract (New in v2.0)
```solidity
// Deploy infralink-info.sol first - this is the central registry
// No constructor parameters needed
// This contract will be permanent and handle all user profiles and device whitelist
```

#### Deploy Test Token (Optional)
```solidity
// Deploy testtoken.sol if you need a test ERC20 token
// Constructor parameters: name, symbol, decimals
// Example: "InfraLink Token", "ILT", 18
```

#### Deploy Device Contract

**IMPORTANT: Fee calculation varies by network! Use the correct values below.**

```solidity
// Deploy devicecontract.sol with these parameters:
// - _token: Address of your ERC20 token (set to zero address 0x0000000000000000000000000000000000000000 for native token)
// - _feePerSecond: Fee in smallest units per second (see network-specific values below)
// - _whitelistFeePerSecond: Fee in smallest units per second for whitelisted users (0 for free access)
// - _deviceName: Human-readable name for your device (e.g., "3D Printer Lab A")
// - _deviceDescription: Description of the device (e.g., "High-resolution 3D printer for prototyping")
```

##### Network-Specific Fee Values for Native Token Usage

**For 0.001 native token per second rate:**

| Network | Chain ID | Currency | Decimals | Fee Value (_feePerSecond) | Example 10min Cost |
|---------|----------|----------|----------|---------------------------|-------------------|
| Ethereum Mainnet | 1 | ETH | 18 | 1000000000000000 | 0.6 ETH |
| Ethereum Sepolia | 11155111 | ETH | 18 | 1000000000000000 | 0.6 ETH |
| Ethereum Goerli | 5 | ETH | 18 | 1000000000000000 | 0.6 ETH |
| Hedera Mainnet | 295 | HBAR | 8 | 100000 | 0.6 HBAR |
| Hedera Testnet | 296 | HBAR | 8 | 100000 | 0.6 HBAR |
| Polygon | 137 | MATIC | 18 | 1000000000000000 | 0.6 MATIC |
| BSC | 56 | BNB | 18 | 1000000000000000 | 0.6 BNB |
| Avalanche | 43114 | AVAX | 18 | 1000000000000000 | 0.6 AVAX |

**Deployment Examples:**

```solidity
// Ethereum networks (18 decimals):
// Constructor(_token, _feePerSecond, _whitelistFeePerSecond, _deviceName, _deviceDescription)
Constructor(
    0x0000000000000000000000000000000000000000,  // Zero address for ETH
    1000000000000000,                            // 0.001 ETH per second
    500000000000000,                             // 0.0005 ETH per second for whitelist
    "Lab Printer A",
    "High-resolution 3D printer"
)

// Hedera networks (8 decimals):
Constructor(
    0x0000000000000000000000000000000000000000,  // Zero address for HBAR
    100000,                                      // 0.001 HBAR per second
    50000,                                       // 0.0005 HBAR per second for whitelist
    "Lab Printer A",
    "High-resolution 3D printer"
)
```

**Important Notes:**
- The contract automatically detects the network and sets the correct currency symbol
- Always use the zero address (0x0000000000000000000000000000000000000000) for native token usage
- Use the `debug_contract.py` script to verify your deployment has correct values

### Hedera Testnet Deployment

```bash
# Hedera Testnet Configuration
Network: Hedera Testnet
Chain ID: 296
Currency: HBAR
RPC URL: https://testnet.hashio.io/api
Block Explorer: https://hashscan.io/testnet

# To deploy on Hedera testnet:
# 1. Add Hedera testnet to your wallet:
#    - Network Name: Hedera Testnet
#    - RPC URL: https://testnet.hashio.io/api
#    - Chain ID: 296
#    - Currency Symbol: HBAR
#    - Block Explorer: https://hashscan.io/testnet
# 2. Get testnet HBAR from: https://portal.hedera.com/
# 3. Deploy contracts using the same process as Ethereum
# 4. Native token payments will use HBAR instead of ETH
```

### 2. Set Up Web Application

```bash
cd infralink-webapp
npm install

# Update the InfraLink Info contract address in these files:
# 1. src/components/UserProfile.tsx - Line 27
# 2. src/components/WhitelistManager.tsx - Line 37
# Replace "0x0000000000000000000000000000000000000000" with your deployed Info contract address

# Example:
# const INFRALINK_INFO_ADDRESS = "0x1234567890123456789012345678901234567890";

npm run dev
```

The app will be available at `http://localhost:5173`

### 3. Configure Device Monitor

```bash
# Install Python dependencies
pip install -r requirements.txt

# Edit devicelocal.py and update:
# - INFURA_URL: Your blockchain node URL (Infura, Alchemy, or Hedera testnet)
# - DEVICE_CONTRACT_ADDRESS: Your deployed contract address

# For Hedera testnet, use:
# INFURA_URL = "https://testnet.hashio.io/api"

# Run the monitor
python devicelocal.py
```

## 🔧 Configuration

### Contract Owner Tasks

1. **Register Device with Info Contract**
   ```solidity
   // In infralink-info.sol
   registerDevice(address deviceContract, string deviceName, string deviceDescription)
   ```

2. **Set Fees**
   ```solidity
   setFee(uint256 _regularFee, uint256 _whitelistFee) // Set both fees at once
   setWhitelistFee(uint256 _fee) // Set whitelist fee only (0 for free access)
   ```

3. **Manage Whitelist (Enhanced in v2.0)**
   ```solidity
   // Via device contract (legacy)
   setWhitelist(address user, bool status, string name) // Add/remove user with custom name
   
   // Via InfraLink Info contract (recommended)
   addDeviceWhitelist(address deviceContract, address user, string name, uint256 fee, bool isFree)
   removeDeviceWhitelist(address deviceContract, address user)
   ```

4. **Update Device Information**
   ```solidity
   setDeviceInfo(string name, string description) // Update device details
   ```

5. **Withdraw Fees (Enhanced for Native Tokens)**
   ```solidity
   withdrawFees() // Withdraw collected fees (ETH or ERC20) to owner
   ```

6. **View Information (Enhanced)**
   ```solidity
   getDeviceInfo(address user) // Get comprehensive device and user info (including native token support)
   getWhitelistInfo() // Get all whitelisted users and their names
   ```

### User Profile Management (New in v2.0)

1. **Create/Update Profile**
   ```solidity
   // In infralink-info.sol
   setUserProfile(string name, string bio, string email, string avatar)
   ```

2. **View Profile and Device Access**
   ```solidity
   getUserProfile(address user) // Get user profile information
   getAllUserDevices(address user) // Get all devices user has whitelist access to
   ```

### Device Setup

1. **Generate QR Code**
   - Go to `/device-owner` in the web app
   - Use the QR Generator tab
   - Enter your contract address
   - Generate and print QR code
   - Place on your device

2. **Manage Whitelist**
   - Use the Whitelist Manager tab in Device Owner tools
   - Enter your device contract address
   - Add/remove users with custom names and fees
   - View user profiles when managing access

3. **Configure Monitor**
   - Update `devicelocal.py` with your contract address
   - Run the Python script on your device hardware
   - Monitor will show device status, payment type, and countdown

## 💰 Native Token Support (New in v2.0)

### Using Native Tokens (ETH/HBAR) Instead of ERC20

1. **Deploy Device Contract with Native Token Support**
   ```solidity
   // Set _token to zero address (0x0000000000000000000000000000000000000000)
   // This automatically sets useNativeToken to true in the contract
   // Set fees in wei (1 ETH = 1e18 wei, 1 HBAR = 1e8 tinybars)
   ```

2. **User Experience with Native Tokens**
   - No token approval required
   - Direct ETH/HBAR payment to contract
   - Fees shown in ETH/HBAR instead of token units
   - Automatic balance checking for native currency

3. **Network-Specific Benefits**
   - **Ethereum**: Familiar ETH payments, broad wallet support
   - **Hedera**: Fast transactions, low fees, enterprise-grade security
   - Simpler user experience (no token approval step)
   - Direct native currency collection
   - Lower gas costs for users
   - Broader user accessibility
   - Monitor will show device status and countdown

## 📱 User Flow

1. **Connect Wallet**
   - Users open the web app
   - Connect their Web3 wallet

2. **Find Device**
   - Scan QR code OR enter contract address manually
   - App fetches device information from contract

3. **Activate Device**
   - Choose duration (minutes)
   - Approve ERC20 token spending
   - Pay for device activation
   - Device becomes active for specified duration

4. **Monitor Session**
   - View remaining time
   - Extend session if needed
   - Deactivate early if desired

## 🔐 Security Notes

- **Contract Owner**: Has full control over fees and whitelist
- **Device Access**: Only current session holder can use device
- **Token Approval**: Users must approve token spending before activation
- **Session Management**: Sessions expire automatically or can be ended manually

## 🧪 Testing

### Local Testing Setup

1. **Use Ganache or Hardhat** for local blockchain
2. **Deploy contracts** to local network
3. **Fund test accounts** with test tokens
4. **Test full flow** from QR scan to device activation

### Testnet Deployment

1. **Deploy to Ethereum Testnets** (Sepolia/Goerli)
   - Get testnet ETH from faucets
   - Test with real wallet interactions
   - Verify contracts on Etherscan

2. **Deploy to Hedera Testnet** (Recommended for fast, low-cost testing)
   - Get testnet HBAR from https://portal.hedera.com/
   - Add Hedera testnet to MetaMask (see configuration above)
   - Deploy contracts using same process as Ethereum
   - Verify contracts on https://hashscan.io/testnet
   - Test native HBAR payments

## 📊 Monitoring & Analytics

### Device Monitor Features
- **Real-time session status** with device name and description
- **Token information display** showing payment token details
- **User whitelist status** showing if current user is whitelisted
- **Fee rate display** showing regular and whitelist rates
- **Whitelist viewer** showing all whitelisted users with their names
- **Progress tracking** with accurate countdown timer
- **Connection status** and error handling
- **Automatic updates** with configurable intervals

### Contract Events
- `DeviceActivated`: When device is activated (includes whitelist status and amount paid)
- `DeviceDeactivated`: When device is deactivated (includes whitelist status)
- `FeeChanged`: When fees are updated (both regular and whitelist fees)
- `WhitelistUpdated`: When whitelist is modified (includes user name)
- `DeviceInfoUpdated`: When device information is updated

## 🛠️ Troubleshooting

### Common Issues

1. **"Device is busy"**
   - Another user has an active session
   - Wait for session to expire or subscribe to notifications

2. **"Insufficient allowance"**
   - Approve token spending first
   - Check token balance and allowance amount

3. **"Insufficient balance"**
   - User doesn't have enough tokens
   - Show current balance vs required payment

4. **"Not whitelisted" or fee confusion**
   - User sees different fee rates based on whitelist status
   - Clear display of regular vs whitelist fees
   - Whitelist status clearly shown in UI

5. **"Connection failed"**
   - Check RPC URL in Python script
   - For Hedera: Use https://testnet.hashio.io/api
   - For Ethereum: Use Infura/Alchemy URL
   - Verify contract address is correct
   - Ensure network connectivity and correct chain ID

6. **Python script errors**
   - Install dependencies: `pip install web3`
   - Check contract ABI matches deployed contract
   - Verify network connection and RPC endpoint
   - For Hedera: Ensure using correct RPC URL and chain ID

7. **Network-specific issues**
   - **Ethereum**: Check gas prices and network congestion
   - **Hedera**: Verify HBAR balance and account permissions
   - **All networks**: Confirm wallet is connected to correct network

8. **Insufficient ETH/HBAR sent error on Hedera**
   - **CRITICAL**: If you get "Insufficient ETH sent" on Hedera, the contract was deployed with the old version
   - The contract is using 18 decimals (ETH) instead of 8 decimals (HBAR)
   - **Solution**: Redeploy the contract with the updated `devicecontract.sol` that properly detects Hedera networks
   - Updated contract will show "HBAR" symbol and use 8 decimals for proper fee calculation
   - Run `python debug_contract.py` to verify contract values

9. **Fee calculation issues**
   - **Ethereum**: 1 ETH = 1e18 wei (18 decimals)
   - **Hedera**: 1 HBAR = 1e8 tinybars (8 decimals)
   - For 0.001 HBAR/second fee on Hedera: deploy with `_feePerSecond = 100000`
   - For 0.001 ETH/second fee on Ethereum: deploy with `_feePerSecond = 1000000000000000`
   - Use the debug script to verify deployed values

7. **Whitelist issues**
   - Only contract owner can modify whitelist
   - Whitelist names are optional but recommended
   - Free access requires whitelist fee to be set to 0

8. **Currency and fee confusion**
   - **Problem**: Wrong fee calculation for different networks
   - **Solution**: Use network-specific fee values from NETWORK_CONFIG.md
   - **Ethereum**: Fees in ETH (wei units: 1 ETH = 10^18 wei)
   - **Hedera**: Fees in HBAR (tinybar units: 1 HBAR = 10^8 tinybars)
   - **Other EVM**: Usually 18 decimals (10^18 smallest units)
   - **Debug**: Run `python debug_contract.py` to verify contract values

9. **Contract deployed with wrong fee values**
   - **Problem**: Payments fail due to incorrect fee denomination
   - **Symptoms**: "Insufficient ETH/HBAR sent" errors even with correct amounts
   - **Solution**: Redeploy contract with correct network-specific values
   - **Prevention**: Use the fee table in SETUP.md for deployment parameters

### Debug Tips

- Use `python debug_contract.py` to check contract deployment values
- Check browser console for errors
- Verify contract addresses are correct
- Ensure sufficient token balance
- Check network connectivity
- Monitor contract events on block explorer
- Verify decimals match the network (8 for Hedera, 18 for Ethereum)

## 🔄 Maintenance

### Regular Tasks

1. **Monitor device uptime**
2. **Check fee collection**
3. **Update whitelist as needed**
4. **Backup contract data**
5. **Monitor for software updates**

### Upgrades

- Contract upgrades require redeployment
- Update QR codes if contract address changes
- Notify users of any changes
- Test thoroughly before production use

## 📞 Support

For issues or questions:
1. Check this guide first
2. Review contract code and comments
3. Test on local/testnet environment
4. Check network status and connectivity
