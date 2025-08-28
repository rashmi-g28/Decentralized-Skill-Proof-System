import os
import requests
import streamlit as st

st.set_page_config(page_title="Verify - DSPS")
st.header("Verify On-Chain")

api_base = os.getenv("API_BASE_URL", st.session_state.get("API_BASE_URL", "http://localhost:8000"))

wallet = st.text_input("Wallet address", value="")
if st.button("Verify") and wallet:
	try:
		res = requests.get(f"{api_base}/api/v1/verify/{wallet}", timeout=30)
		res.raise_for_status()
		data = res.json()
		records = data.get("records", [])
		if not records:
			st.info("No on-chain records found.")
		else:
			st.write(f"Found {len(records)} record(s):")
			for r in records:
				st.write(f"- Skill: {r['skill']}, Score: {r['score']}%, Timestamp: {r['timestamp']}")
	except Exception as e:
		st.error(f"Failed to fetch: {e}")