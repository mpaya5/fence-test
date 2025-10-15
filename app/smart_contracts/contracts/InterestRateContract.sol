// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title InterestRateContract
 * @dev Smart contract to store and manage average interest rates
 * @notice This contract stores the latest calculated average interest rate with timestamp
 */
contract InterestRateContract {
    // State variables
    uint256 private currentRate;
    uint256 private lastUpdated;
    address private owner;
    
    // Events
    event InterestRateUpdated(uint256 newRate, uint256 timestamp);
    
    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    
    // Constructor
    constructor() {
        owner = msg.sender;
        currentRate = 0;
        lastUpdated = 0;
    }
    
    /**
     * @dev Update the interest rate with a new calculated average
     * @param newRate The new average interest rate (multiplied by 100 for precision)
     * @param timestamp The timestamp when the rate was calculated
     */
    function updateInterestRate(uint256 newRate, uint256 timestamp) external onlyOwner {
        require(timestamp >= lastUpdated, "Timestamp must be greater than or equal to last update");
        
        currentRate = newRate;
        lastUpdated = timestamp;
        
        emit InterestRateUpdated(newRate, timestamp);
    }
    
    /**
     * @dev Get the current stored interest rate
     * @return rate The current interest rate
     * @return timestamp The timestamp when it was last updated
     */
    function getInterestRate() external view returns (uint256 rate, uint256 timestamp) {
        return (currentRate, lastUpdated);
    }
    
}
