# DSPS - Decentralized Skill Proof System

DSPS lets users prove their coding skills by submitting solutions to small coding challenges. The backend evaluates code against predefined test cases, stores the result in a database, and (optionally) writes a tamper-proof proof on a blockchain. Successful users can download a PDF certificate containing the blockchain transaction hash.

## Components
- Backend: FastAPI, SQLite, Web3.py, ReportLab
- Frontend: React + Tailwind (Vite)
- Smart contract: Solidity (Hardhat), Ownable admin to add verified records

## High-level flow
1. User uploads a Python file implementing `solve(input)`.
2. Backend runs it in a sandboxed subprocess against JSON testcases.
3. Result is persisted (user, skill, score, pass/fail).
4. If configured, backend pushes a record on-chain (admin key) and stores the tx hash.
5. A PDF certificate is generated and made available for download.
6. Anyone can verify a wallet’s records via the verify endpoint (reads from chain).

## MVP decisions
- SQLite for simplicity; easily swappable with Postgres later.
- Minimal evaluator: single function `solve` and deterministic testcases.
- Admin-controlled chain writes via `onlyOwner` contract; later you can add role-based access.