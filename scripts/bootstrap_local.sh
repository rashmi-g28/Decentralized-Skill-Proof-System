#!/usr/bin/env bash
set -euo pipefail

# DSPS bootstrap (local)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "[1/4] Backend deps"
cd "$ROOT_DIR/backend"
cp -n .env.example .env || true
pip install --break-system-packages -r requirements.txt

echo "[2/4] Frontend deps"
cd "$ROOT_DIR/frontend"
cp -n .env.example .env || true
npm i

echo "[3/4] Contracts deps & compile"
cd "$ROOT_DIR/smart-contract"
cp -n .env.example .env || true
npm i
npx hardhat compile

echo "[4/4] Done. Start services with scripts/run_backend.sh and scripts/run_frontend.sh"