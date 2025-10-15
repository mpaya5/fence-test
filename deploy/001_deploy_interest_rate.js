module.exports = async ({ getNamedAccounts, deployments, network }) => {
  const { deploy, log } = deployments;
  const { deployer } = await getNamedAccounts();

  log("🚀 Deploying InterestRateContract...");
  log(`📍 Network: ${network.name}`);
  log(`👤 Deployer: ${deployer}`);

  // Deploy the contract
  const interestRateContract = await deploy("InterestRateContract", {
    from: deployer,
    args: [], // No constructor arguments
    log: true,
    waitConfirmations: 1, // Wait for 1 confirmation
  });

  log(`✅ InterestRateContract deployed to: ${interestRateContract.address}`);
  log(`📝 Contract Address: ${interestRateContract.address}`);
  log(`🔑 Deployer Address: ${deployer}`);
  log("");
  log("📋 Add these values to your .env file:");
  log(`CONTRACT_ADDRESS=${interestRateContract.address}`);
  log(`BLOCKCHAIN_RPC_URL=http://hardhat-node:8545`);
  log("");

  return true;
};

module.exports.tags = ["InterestRateContract"];
