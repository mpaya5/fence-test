require("@nomicfoundation/hardhat-toolbox");
require("hardhat-deploy");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.24",
  networks: {
    hardhat: {
      chainId: 31337,
      accounts: {
        mnemonic: "test test test test test test test test test test test junk",
        count: 10,
        initialIndex: 0,
        path: "m/44'/60'/0'/0",
        accountsBalance: "10000000000000000000000" // 10000 ETH
      }
    },
    localhost: {
      url: "http://hardhat-node:8545", // Point to the Hardhat node service in Docker Compose
      chainId: 31337,
      accounts: {
        mnemonic: "test test test test test test test test test test test junk"
      }
    }
  },
  paths: {
    sources: "./contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts"
  },
  namedAccounts: {
    deployer: 0, // First account will be used as deployer
  },
};
