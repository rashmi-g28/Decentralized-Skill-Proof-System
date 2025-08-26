import { ethers, network } from "hardhat";
import { writeFileSync, mkdirSync } from "fs";
import { join } from "path";

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with:", deployer.address);

  const factory = await ethers.getContractFactory("DSPSkillProof");
  const contract = await factory.deploy(await deployer.getAddress());
  await contract.waitForDeployment();

  const address = await contract.getAddress();
  console.log("DSPSkillProof deployed at:", address);

  // Write deployment info for tooling
  const outDir = join(__dirname, "..", "deployments");
  try { mkdirSync(outDir, { recursive: true }); } catch {}
  const outPath = join(outDir, "local.json");
  const data = {
    network: network.name,
    chainId: (await ethers.provider.getNetwork()).chainId.toString(),
    contract: "DSPSkillProof",
    address,
    deployer: deployer.address,
  };
  writeFileSync(outPath, JSON.stringify(data, null, 2));
  console.log("Wrote deployment:", outPath);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});