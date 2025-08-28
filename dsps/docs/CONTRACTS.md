# Smart Contract (DSPSkillProof)

- Ownable contract that stores `Record{ user, skill, score, timestamp }` per user.
- Admin (owner) calls `addRecord(user, skill, score, timestamp)` to append.
- Anyone can call `getRecords(user)` to read.

## Dev
```bash
cd smart-contract
cp .env.example .env
npm i
npx hardhat compile
```

## Deploy (Sepolia or Mumbai)
```bash
# Fill PRIVATE_KEY and RPC URL(s) in .env
npx hardhat run --network sepolia scripts/deploy.ts
# or
npx hardhat run --network polygonMumbai scripts/deploy.ts
```
Copy the deployed address and update backend `.env`:
```
WEB3_PROVIDER_URL=...
CONTRACT_ADDRESS=0x...
CONTRACT_PRIVATE_KEY=0x...
DSPS_AUTO_PUSH=true
```

Optionally copy the compiled ABI to backend:
```bash
cp artifacts/contracts/DSPSkillProof.sol/DSPSkillProof.json \
  ../../backend/app/services/blockchain/abi/DSPSkillProof.json
```