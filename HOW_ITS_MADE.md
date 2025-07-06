# How It's Made

## The Stack That Powers InfraLink

### Frontend Web3 Magic
- React + TypeScript - Because we like our code typed and our bugs caught early
- Vite - Lightning-fast builds that don't make you wait for coffee
- Tailwind CSS + shadcn/ui - Beautiful components without the CSS headaches
- Privy - Web3 authentication that actually works (email, SMS, socials, wallets)
- wagmi + viem - Ethereum interactions made simple
- Tanstack Query - Smart data fetching that caches like a boss

### Smart Contracts
- Solidity - The language of money (and IoT devices apparently)
- Device Contract - Handles payments, sessions, and device control
- Info Contract - Manages user profiles and whitelisting
- Multi-chain deployment - Works on Hedera, Flow EVM, Zircuit, Ethereum, and more

### Device Monitor (Python)
- tkinter - Yes, we made desktop GUI cool again
- Web3.py - Ethereum client for Python that speaks fluent blockchain
- Network switching - Dropdown to hop between chains like a pro
- Real-time monitoring - Watches device states and user sessions

### The Hacky Bits

#### Multi-Chain Network Utilities
Built a unified network abstraction layer that handles:
- Different decimal places (HBAR uses 8, ETH uses 18)
- Chain-specific fee calculations 
- Network-aware currency formatting
- RPC endpoint management

```python
# One function to rule them all
def format_native_amount(amount, chain_id, decimals=None):
    # Handles HBAR's 8 decimals vs ETH's 18 automatically
```

#### Smart Contract Address Magic
Instead of hardcoding addresses, we use profile-based configuration:
```python
NETWORK_PROFILES = {
    "Hedera Testnet": {
        "device_contract": "0x...",
        "info_contract": "0x...",
        "rpc_url": "https://testnet.hashio.io/api"
    }
}
```

#### Real-time Device State Sync
The Python monitor polls contract state every 10 seconds and updates the UI:
- Device online/offline status
- Current user sessions
- Whitelist status
- Payment rates (regular vs whitelisted)

#### Payload Script Separation
Split device control logic into separate script for easy customization:
```python
# devicepayload.py - The fun stuff
def on_device_enable():
    play_sound("song.mp3")
    run_command("your_custom_enable_script.sh")
```

### Partner Tech Integration

Authentication handles wallet connections across all chains with email/SMS authentication for Web2 users, embedded wallets for seamless onboarding, and chain switching without the headaches. The blockchain infrastructure provides low fees perfect for IoT micropayments, fast finality for real-time device control, and JSON-RPC compatibility that works with standard Web3 tools across multiple networks.

### The Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web3 App      │    │  Smart Contracts│    │  Device Monitor │
│                 │    │                 │    │                 │
│ • User profiles │◄──►│ • Device control│◄──►│ • Real-time UI  │
│ • QR scanning   │    │ • Payments      │    │ • Chain switch  │
│ • Payments      │    │ • Whitelisting  │    │ • Payload exec  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Why This Stack Rocks

1. Multi-chain from day one - No vendor lock-in
2. Web2 UX meets Web3 power - Authentication makes onboarding painless
3. Real devices, real control - Python monitor actually controls hardware
4. Hackathon to production - Built with scale in mind
5. Developer friendly - Easy to customize and extend

### The Secret Sauce

The real magic happens in the seamless integration between:
- Web3 payments triggering real-world device actions
- Cross-chain compatibility without user friction  
- Professional desktop monitoring for device operators
- Flexible payload system for any IoT use case

Built for hackathons, designed for the real world.
