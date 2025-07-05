// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title InfraLinkInfo
 * @dev Central registry for user profiles and device whitelist information
 * This contract serves as a permanent index for user information and device access
 */
contract InfraLinkInfo {
    address public owner;
    
    struct UserProfile {
        string name;
        string bio;
        string email;
        string avatar;
        bool exists;
        uint256 createdAt;
        uint256 updatedAt;
    }
    
    struct DeviceWhitelistEntry {
        address deviceContract;
        string deviceName;
        string whitelistName;
        uint256 feePerSecond;
        bool isFree;
        bool isActive;
        uint256 addedAt;
        address addedBy;
    }
    
    struct DeviceInfo {
        string name;
        string description;
        address owner;
        bool isRegistered;
        uint256 registeredAt;
    }
    
    // User profiles mapping
    mapping(address => UserProfile) public userProfiles;
    
    // Device whitelist entries for each user
    mapping(address => DeviceWhitelistEntry[]) public userWhitelists;
    
    // Device information registry
    mapping(address => DeviceInfo) public deviceRegistry;
    
    // Admin permissions for whitelist management
    mapping(address => mapping(address => bool)) public deviceAdmins; // device => admin => hasPermission
    
    // Arrays for enumeration
    address[] public registeredUsers;
    address[] public registeredDevices;
    
    // Events
    event UserProfileUpdated(address indexed user, string name, string bio);
    event UserProfileDeleted(address indexed user);
    event DeviceRegistered(address indexed deviceContract, string name, address indexed owner);
    event DeviceUnregistered(address indexed deviceContract);
    event WhitelistAdded(address indexed user, address indexed deviceContract, string whitelistName, uint256 feePerSecond, bool isFree);
    event WhitelistRemoved(address indexed user, address indexed deviceContract, address indexed removedBy);
    event WhitelistUpdated(address indexed user, address indexed deviceContract, string whitelistName, uint256 feePerSecond, bool isFree);
    event AdminAdded(address indexed deviceContract, address indexed admin, address indexed addedBy);
    event AdminRemoved(address indexed deviceContract, address indexed admin, address indexed removedBy);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not contract owner");
        _;
    }
    
    modifier onlyDeviceOwnerOrAdmin(address deviceContract) {
        require(
            deviceRegistry[deviceContract].owner == msg.sender || 
            deviceAdmins[deviceContract][msg.sender], 
            "Not device owner or admin"
        );
        _;
    }
    
    constructor() {
        owner = msg.sender;
    }
    
    // === USER PROFILE MANAGEMENT ===
    
    function updateUserProfile(
        string memory _name,
        string memory _bio,
        string memory _email,
        string memory _avatar
    ) external {
        UserProfile storage profile = userProfiles[msg.sender];
        
        if (!profile.exists) {
            profile.exists = true;
            profile.createdAt = block.timestamp;
            registeredUsers.push(msg.sender);
        }
        
        profile.name = _name;
        profile.bio = _bio;
        profile.email = _email;
        profile.avatar = _avatar;
        profile.updatedAt = block.timestamp;
        
        emit UserProfileUpdated(msg.sender, _name, _bio);
    }
    
    function deleteUserProfile() external {
        require(userProfiles[msg.sender].exists, "Profile does not exist");
        
        // Remove from registeredUsers array
        for (uint i = 0; i < registeredUsers.length; i++) {
            if (registeredUsers[i] == msg.sender) {
                registeredUsers[i] = registeredUsers[registeredUsers.length - 1];
                registeredUsers.pop();
                break;
            }
        }
        
        delete userProfiles[msg.sender];
        // Note: This doesn't clear whitelist entries for the user
        
        emit UserProfileDeleted(msg.sender);
    }
    
    function getUserProfile(address user) external view returns (
        string memory name,
        string memory bio,
        string memory email,
        string memory avatar,
        bool exists,
        uint256 createdAt,
        uint256 updatedAt
    ) {
        UserProfile memory profile = userProfiles[user];
        return (
            profile.name,
            profile.bio,
            profile.email,
            profile.avatar,
            profile.exists,
            profile.createdAt,
            profile.updatedAt
        );
    }
    
    // === DEVICE REGISTRY MANAGEMENT ===
    
    function registerDevice(
        address deviceContract,
        string memory _name,
        string memory _description
    ) external {
        require(!deviceRegistry[deviceContract].isRegistered, "Device already registered");
        
        deviceRegistry[deviceContract] = DeviceInfo({
            name: _name,
            description: _description,
            owner: msg.sender,
            isRegistered: true,
            registeredAt: block.timestamp
        });
        
        registeredDevices.push(deviceContract);
        
        emit DeviceRegistered(deviceContract, _name, msg.sender);
    }
    
    function updateDeviceInfo(
        address deviceContract,
        string memory _name,
        string memory _description
    ) external onlyDeviceOwnerOrAdmin(deviceContract) {
        require(deviceRegistry[deviceContract].isRegistered, "Device not registered");
        
        deviceRegistry[deviceContract].name = _name;
        deviceRegistry[deviceContract].description = _description;
        
        emit DeviceRegistered(deviceContract, _name, deviceRegistry[deviceContract].owner);
    }
    
    function unregisterDevice(address deviceContract) external {
        require(
            deviceRegistry[deviceContract].owner == msg.sender || 
            msg.sender == owner, 
            "Not device owner or contract owner"
        );
        require(deviceRegistry[deviceContract].isRegistered, "Device not registered");
        
        // Remove from registeredDevices array
        for (uint i = 0; i < registeredDevices.length; i++) {
            if (registeredDevices[i] == deviceContract) {
                registeredDevices[i] = registeredDevices[registeredDevices.length - 1];
                registeredDevices.pop();
                break;
            }
        }
        
        delete deviceRegistry[deviceContract];
        
        emit DeviceUnregistered(deviceContract);
    }
    
    // === WHITELIST MANAGEMENT ===
    
    function addUserToWhitelist(
        address user,
        address deviceContract,
        string memory whitelistName,
        uint256 feePerSecond,
        bool isFree
    ) external onlyDeviceOwnerOrAdmin(deviceContract) {
        require(deviceRegistry[deviceContract].isRegistered, "Device not registered");
        
        // Check if user is already whitelisted for this device
        DeviceWhitelistEntry[] storage userEntries = userWhitelists[user];
        for (uint i = 0; i < userEntries.length; i++) {
            if (userEntries[i].deviceContract == deviceContract && userEntries[i].isActive) {
                revert("User already whitelisted for this device");
            }
        }
        
        userWhitelists[user].push(DeviceWhitelistEntry({
            deviceContract: deviceContract,
            deviceName: deviceRegistry[deviceContract].name,
            whitelistName: whitelistName,
            feePerSecond: feePerSecond,
            isFree: isFree,
            isActive: true,
            addedAt: block.timestamp,
            addedBy: msg.sender
        }));
        
        emit WhitelistAdded(user, deviceContract, whitelistName, feePerSecond, isFree);
    }
    
    function removeUserFromWhitelist(
        address user,
        address deviceContract
    ) external onlyDeviceOwnerOrAdmin(deviceContract) {
        DeviceWhitelistEntry[] storage userEntries = userWhitelists[user];
        
        for (uint i = 0; i < userEntries.length; i++) {
            if (userEntries[i].deviceContract == deviceContract && userEntries[i].isActive) {
                userEntries[i].isActive = false;
                emit WhitelistRemoved(user, deviceContract, msg.sender);
                return;
            }
        }
        
        revert("User not found in whitelist");
    }
    
    function updateWhitelistEntry(
        address user,
        address deviceContract,
        string memory whitelistName,
        uint256 feePerSecond,
        bool isFree
    ) external onlyDeviceOwnerOrAdmin(deviceContract) {
        DeviceWhitelistEntry[] storage userEntries = userWhitelists[user];
        
        for (uint i = 0; i < userEntries.length; i++) {
            if (userEntries[i].deviceContract == deviceContract && userEntries[i].isActive) {
                userEntries[i].whitelistName = whitelistName;
                userEntries[i].feePerSecond = feePerSecond;
                userEntries[i].isFree = isFree;
                userEntries[i].deviceName = deviceRegistry[deviceContract].name;
                
                emit WhitelistUpdated(user, deviceContract, whitelistName, feePerSecond, isFree);
                return;
            }
        }
        
        revert("User not found in whitelist");
    }
    
    // === ADMIN MANAGEMENT ===
    
    function addDeviceAdmin(address deviceContract, address admin) external {
        require(
            deviceRegistry[deviceContract].owner == msg.sender || 
            msg.sender == owner, 
            "Not device owner or contract owner"
        );
        require(deviceRegistry[deviceContract].isRegistered, "Device not registered");
        
        deviceAdmins[deviceContract][admin] = true;
        
        emit AdminAdded(deviceContract, admin, msg.sender);
    }
    
    function removeDeviceAdmin(address deviceContract, address admin) external {
        require(
            deviceRegistry[deviceContract].owner == msg.sender || 
            msg.sender == owner, 
            "Not device owner or contract owner"
        );
        
        deviceAdmins[deviceContract][admin] = false;
        
        emit AdminRemoved(deviceContract, admin, msg.sender);
    }
    
    // === VIEW FUNCTIONS ===
    
    function getUserWhitelists(address user) external view returns (
        address[] memory deviceContracts,
        string[] memory deviceNames,
        string[] memory whitelistNames,
        uint256[] memory feePerSeconds,
        bool[] memory isFreeAccess,
        uint256[] memory addedAts
    ) {
        DeviceWhitelistEntry[] memory entries = userWhitelists[user];
        uint256 activeCount = 0;
        
        // Count active entries
        for (uint i = 0; i < entries.length; i++) {
            if (entries[i].isActive) {
                activeCount++;
            }
        }
        
        // Create arrays for active entries
        deviceContracts = new address[](activeCount);
        deviceNames = new string[](activeCount);
        whitelistNames = new string[](activeCount);
        feePerSeconds = new uint256[](activeCount);
        isFreeAccess = new bool[](activeCount);
        addedAts = new uint256[](activeCount);
        
        uint256 index = 0;
        for (uint i = 0; i < entries.length; i++) {
            if (entries[i].isActive) {
                deviceContracts[index] = entries[i].deviceContract;
                deviceNames[index] = entries[i].deviceName;
                whitelistNames[index] = entries[i].whitelistName;
                feePerSeconds[index] = entries[i].feePerSecond;
                isFreeAccess[index] = entries[i].isFree;
                addedAts[index] = entries[i].addedAt;
                index++;
            }
        }
        
        return (deviceContracts, deviceNames, whitelistNames, feePerSeconds, isFreeAccess, addedAts);
    }
    
    function isUserWhitelisted(address user, address deviceContract) external view returns (bool) {
        DeviceWhitelistEntry[] memory entries = userWhitelists[user];
        
        for (uint i = 0; i < entries.length; i++) {
            if (entries[i].deviceContract == deviceContract && entries[i].isActive) {
                return true;
            }
        }
        
        return false;
    }
    
    function getWhitelistInfo(address user, address deviceContract) external view returns (
        string memory whitelistName,
        uint256 feePerSecond,
        bool isFree,
        uint256 addedAt,
        address addedBy
    ) {
        DeviceWhitelistEntry[] memory entries = userWhitelists[user];
        
        for (uint i = 0; i < entries.length; i++) {
            if (entries[i].deviceContract == deviceContract && entries[i].isActive) {
                return (
                    entries[i].whitelistName,
                    entries[i].feePerSecond,
                    entries[i].isFree,
                    entries[i].addedAt,
                    entries[i].addedBy
                );
            }
        }
        
        revert("User not whitelisted for this device");
    }
    
    function getAllRegisteredUsers() external view returns (address[] memory) {
        return registeredUsers;
    }
    
    function getAllRegisteredDevices() external view returns (address[] memory) {
        return registeredDevices;
    }
    
    function getRegisteredUsersCount() external view returns (uint256) {
        return registeredUsers.length;
    }
    
    function getRegisteredDevicesCount() external view returns (uint256) {
        return registeredDevices.length;
    }
    
    // === CONTRACT OWNER FUNCTIONS ===
    
    function transferOwnership(address newOwner) external onlyOwner {
        owner = newOwner;
    }
    
    // Emergency functions for contract owner
    function emergencyRemoveWhitelist(address user, address deviceContract) external onlyOwner {
        DeviceWhitelistEntry[] storage userEntries = userWhitelists[user];
        
        for (uint i = 0; i < userEntries.length; i++) {
            if (userEntries[i].deviceContract == deviceContract && userEntries[i].isActive) {
                userEntries[i].isActive = false;
                emit WhitelistRemoved(user, deviceContract, msg.sender);
                return;
            }
        }
    }
}
