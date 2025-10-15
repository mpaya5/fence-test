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

  return interestRateContract;
};

module.exports.id = "InterestRateContract";
module.exports.tags = ["InterestRateContract"];
