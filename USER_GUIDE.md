# InfraLink v2.0 - User Guide

## New Features in v2.0

### 🔗 InfraLink Info Contract
A central registry that manages user profiles and device whitelist information.

**For Users:**
- Create and manage your user profile (name, bio, email, avatar)
- View all devices you have whitelist access to
- See your fee rates and access levels across all devices
- Check your whitelist status and permissions

**For Device Owners:**
- Manage whitelist entries through the Info contract
- Add/remove users with custom names and fee rates
- View user profiles when managing whitelist
- Centralized management of device access permissions

### 💳 Native Token Support
Devices can now accept both ERC20 tokens and native tokens (ETH/HBAR).

**Features:**
- Device contracts can be configured to use native tokens instead of ERC20 tokens
- **Ethereum**: Uses ETH as native token
- **Hedera**: Uses HBAR as native token  
- No token approval required for native token payments
- Automatic handling of payment types in both web and Python interfaces
- Clear indication of payment type in all UIs

### 🌐 Multi-Chain Support
InfraLink now supports multiple blockchain networks.

**Supported Networks:**
- **Hedera Testnet** (Chain ID: 296, Currency: HBAR)
- **Ethereum Mainnet/Testnets** (Sepolia)
- **Polygon**, **Optimism**, **Arbitrum**, **Base**

**Benefits:**
- **Hedera**: Fast transactions, low fees, enterprise-grade security
- **Ethereum**: Broad ecosystem and wallet support
- Choose the network that best fits your use case

### 🌐 Enhanced Error Handling
Better error messages and chain detection for improved user experience.

**Improvements:**
- Contract validation before connection attempts
- Clear error messages for wrong network connections
- Automatic detection of non-contract addresses
- Helpful prompts to check network settings

## Using the New Features

### User Profile Management

1. **Navigate to Profile:**
   - Click the "Profile" button in the main navigation
   - Connect your wallet if not already connected

2. **Create/Edit Profile:**
   - Click "Edit Profile" to create or update your information
   - Add your name, bio, email, and avatar URL
   - Save your changes to the blockchain

3. **View Device Access:**
   - See all devices you have whitelist access to
   - Check your specific fee rates and access levels
   - View device information and contract addresses

### Device Owner Tools

1. **Manage Whitelist:**
   - Go to Device Owner Tools → Whitelist Manager tab
   - Enter your device contract address
   - Add users with custom names and fee rates
   - Remove users as needed
   - View user profiles when managing whitelist

2. **QR Code Generation:**
   - Use the QR Generator tab to create device QR codes
   - Configure for both ERC20 and native token devices
   - Print and place QR codes on your devices

### Multi-Chain Configuration

1. **For Device Owners:**
   - Choose your preferred blockchain network
   - **Hedera**: Fast, low-cost transactions with HBAR
   - **Ethereum**: Broad ecosystem support with ETH
   - Deploy your device contract with `useNativeToken = true` for native tokens
   - Set fees in appropriate units:
     - Ethereum: wei (1 ETH = 1e18 wei)
     - Hedera: tinybars (1 HBAR = 1e8 tinybars)

2. **For Users:**
   - Add the network to your wallet if not already configured
   - **Hedera Testnet**: Network settings provided above
   - Native token devices show currency-specific info:
     - "Native Token (ETH)" on Ethereum
     - "Native Token (HBAR)" on Hedera
   - No token approval required - payments are direct native transfers
   - Ensure sufficient balance (ETH/HBAR) for device usage

## Contract Addresses

**InfraLink Info Contract:**
- Mainnet: `0x0000000000000000000000000000000000000000` (To be deployed)
- Testnet: `0x0000000000000000000000000000000000000000` (To be deployed)

**Important:** Update the contract addresses in the application configuration files after deployment.

## Integration Steps

### Web Application
1. Update `INFRALINK_INFO_ADDRESS` in UserProfile.tsx and WhitelistManager.tsx
2. Deploy the updated application
3. Users can now manage profiles and view device access

### Python Device Monitor
1. The monitor automatically detects native token vs ERC20 configuration
2. Displays payment type clearly in the interface
3. Shows appropriate fee information based on configuration

### Device Contracts
1. Deploy with `useNativeToken` parameter set appropriately
2. Configure fees in correct units (wei for ETH, token units for ERC20)
3. Register device with InfraLink Info contract for enhanced features

## Best Practices

### For Device Owners
- Always test your device configuration before production use
- Set reasonable fees to encourage usage
- Use descriptive names for whitelist entries
- Register your device with the Info contract for better user experience

### For Users
- Keep your profile information current
- Check your whitelist status before attempting device access
- Ensure sufficient balance before using devices:
  - **Ethereum**: ETH for native token devices, ERC20 tokens for token devices
  - **Hedera**: HBAR for native token devices, HTS tokens for token devices
- Verify you're connected to the correct network
- Add Hedera testnet to your wallet if using Hedera-based devices

### For Developers
- Always validate contract addresses before connection
- Handle both native token and ERC20 payment flows
- Implement proper error handling for network issues
- Test on testnets before mainnet deployment

## Troubleshooting

### Common Issues

**"Contract not found" errors:**
- Check that you're connected to the correct network
- Verify the contract address is correct
- Ensure the contract is deployed and verified

**Payment failures:**
- For ERC20 tokens: Check token approval and balance
- For native tokens: Check ETH/HBAR balance
- Verify you're using the correct payment method for the network
- **Network-specific issues**:
  - **Ethereum**: May have high gas fees during network congestion
  - **Hedera**: Check HBAR balance and ensure account is properly funded

**Network connection issues:**
- Verify you're connected to the correct blockchain network
- **Hedera users**: Ensure Hedera testnet is added to your wallet
- Check RPC endpoints are responding
- Try switching between networks and back

**Profile/whitelist not loading:**
- Ensure InfraLink Info contract is properly deployed
- Check that the contract address is configured correctly
- Verify network connection and contract state

### Getting Help

1. Check the error messages - they now provide more specific guidance
2. Verify your network connection and contract addresses
3. Ensure you have sufficient funds for transactions
4. Test with small amounts first on testnets

## Future Enhancements

- Mobile app integration
- Advanced analytics and usage tracking
- Subscription-based access models
- Multi-chain support
- Enhanced device discovery features

---

**InfraLink v2.0** - Enhanced decentralized hardware access with user profiles, native token support, and improved error handling.
