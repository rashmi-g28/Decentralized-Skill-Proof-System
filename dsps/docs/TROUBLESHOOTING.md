# Troubleshooting

## Python 3.13 build errors
- Pydantic core: use pydantic>=2.9
- SQLAlchemy symbol error: upgrade to 2.0.43+

## Permission denied writing files
- Ensure backend has write access to `app/static/*`

## On-chain push fails
- Confirm env: `WEB3_PROVIDER_URL`, `CONTRACT_ADDRESS`, `CONTRACT_PRIVATE_KEY`
- Ensure the PRIVATE_KEY address is the contract owner that deployed the contract
- Check gas settings and balance on your testnet

## CORS errors
- Add your frontend origin to `BACKEND_CORS_ORIGINS`

## Frontend build errors about ESM/CJS
- Use `.cjs` for `postcss.config` and `tailwind.config` when `"type": "module"` in package.json