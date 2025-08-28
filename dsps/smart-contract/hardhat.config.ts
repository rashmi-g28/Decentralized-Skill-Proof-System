import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
import * as dotenv from "dotenv";

dotenv.config();

const PRIVATE_KEY = process.env.PRIVATE_KEY as string | undefined;
const SEPOLIA_RPC_URL = process.env.SEPOLIA_RPC_URL as string | undefined;
const POLYGON_MUMBAI_RPC_URL = process.env.POLYGON_MUMBAI_RPC_URL as string | undefined;

const accounts = PRIVATE_KEY ? [PRIVATE_KEY] : [];

const config: HardhatUserConfig = {
	defaultNetwork: "hardhat",
	solidity: {
		version: "0.8.24",
		settings: {
			optimizer: { enabled: true, runs: 200 },
		},
	},
	networks: {
		hardhat: {},
		...(SEPOLIA_RPC_URL && PRIVATE_KEY
			? {
				sepolia: {
					url: SEPOLIA_RPC_URL,
					accounts,
					chainId: 11155111,
				},
			}
			: {}),
		...(POLYGON_MUMBAI_RPC_URL && PRIVATE_KEY
			? {
				polygonMumbai: {
					url: POLYGON_MUMBAI_RPC_URL,
					accounts,
					chainId: 80001,
				},
			}
			: {}),
	},
	paths: {
		sources: "contracts",
		tests: "test",
		cache: "cache",
		artifacts: "artifacts",
	},
};

export default config;