# DSPS Streamlit Frontend

## Setup
```bash
cd /workspace/dsps/streamlit
cp .env.example .env
# Edit API_BASE_URL if your backend runs elsewhere
python3 -m pip install --break-system-packages -r requirements.txt
```

## Run
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```
Open http://localhost:8501

## Pages
- Upload: submit `.py` file, see evaluation result
- Results: fetch by result ID, push on-chain, download certificate
- Verify: enter wallet to read on-chain records