import { ethers } from "hardhat";

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with:", deployer.address);

  const factory = await ethers.getContractFactory("DSPSkillProof");
  const contract = await factory.deploy(await deployer.getAddress());
  await contract.waitForDeployment();

  const address = await contract.getAddress();
  console.log("DSPSkillProof deployed at:", address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});