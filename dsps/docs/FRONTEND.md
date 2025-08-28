# Frontend (React + Tailwind)

## Prereqs
- Node 18+ (Node 22 tested)

## Dev server
```bash
cd frontend
cp .env.example .env
# Set VITE_API_BASE_URL to your backend
npm i
npm run dev
```
Open http://localhost:5173

## Build
```bash
npm run build
npm run preview
```

## Pages
- `Upload`: submit `.py` file, see evaluation details
- `Results`: fetch result by ID, push on-chain, download certificate
- `Verify`: enter wallet to fetch on-chain records

## Deploy
- Vercel: import, set `VITE_API_BASE_URL` env to your backend URL
- Netlify: similarly set env and build with `npm run build`