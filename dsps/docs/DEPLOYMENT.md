# Deployment Guide

## Contract
1) In `smart-contract/.env`, set `PRIVATE_KEY` and `SEPOLIA_RPC_URL` or `POLYGON_MUMBAI_RPC_URL`.
2) `npm i && npx hardhat compile && npx hardhat run --network sepolia scripts/deploy.ts`
3) Note the deployed address, and copy ABI to backend if desired.

## Backend (Render/Railway)
- Build command: `pip install -r backend/requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port 8000`
- Root directory: `backend`
- Environment:
  - `DATABASE_URL` (e.g. sqlite:///./dsps.db or postgres URL)
  - `BACKEND_CORS_ORIGINS` (include your frontend URL)
  - `WEB3_PROVIDER_URL`, `CONTRACT_ADDRESS`, `CONTRACT_PRIVATE_KEY`
  - `DSPS_AUTO_PUSH=true` (optional)

## Frontend (Vercel)
- Root directory: `frontend`
- Build command: `npm run build`
- Output: `frontend/dist`
- Env: `VITE_API_BASE_URL` set to your backend public URL

## Verify
- Submit a passing Fibonacci solution
- Check `GET /api/v1/results/{id}` shows a tx hash
- Download certificate and confirm the hash is embedded
- On the frontend Verify page, enter the wallet to see on-chain records