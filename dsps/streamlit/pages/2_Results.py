import os
import requests
import streamlit as st

st.set_page_config(page_title="Results - DSPS")
st.header("Results")

api_base = os.getenv("API_BASE_URL", st.session_state.get("API_BASE_URL", "http://localhost:8000"))

col1, col2 = st.columns([2,1])
with col1:
	result_id = st.text_input("Result ID", value="")
with col2:
	load_btn = st.button("Load")

if load_btn and result_id:
	try:
		res = requests.get(f"{api_base}/api/v1/results/{int(result_id)}", timeout=30)
		res.raise_for_status()
		data = res.json()
		st.json(data)
		cert_url = f"{api_base}/api/v1/certificates/{int(result_id)}"
		st.markdown(f"[Download Certificate]({cert_url})")
		if data.get("passed") and not data.get("blockchain_tx_hash"):
			if st.button("Push On-Chain"):
				try:
					push = requests.post(f"{api_base}/api/v1/results/{int(result_id)}/push", timeout=60)
					push.raise_for_status()
					st.success("Pushed on-chain.")
					st.json(push.json())
				except Exception as e:
					st.error(f"Failed to push: {e}")
	except Exception as e:
		st.error(f"Failed to fetch: {e}")