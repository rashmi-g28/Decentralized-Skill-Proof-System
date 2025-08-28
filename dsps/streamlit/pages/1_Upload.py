import io
import os
import requests
import streamlit as st

st.set_page_config(page_title="Upload - DSPS")
st.header("Upload Code")

api_base = os.getenv("API_BASE_URL", st.session_state.get("API_BASE_URL", "http://localhost:8000"))

with st.form("upload_form", clear_on_submit=False):
	user_name = st.text_input("Your name", value="")
	wallet = st.text_input("Wallet address (optional)", value="")
	skill = st.selectbox("Skill", options=["fibonacci", "palindrome"], index=0)
	file = st.file_uploader("Python file (.py)", type=["py"]) 
	submitted = st.form_submit_button("Submit")

	if submitted:
		if not file:
			st.error("Please choose a .py file")
			st.stop()
		try:
			files = {"file": (file.name, file.getvalue(), "text/x-python")}
			data = {"user_name": user_name, "wallet_address": wallet, "skill": skill}
			resp = requests.post(f"{api_base}/api/v1/submit", files=files, data=data, timeout=60)
			resp.raise_for_status()
			res = resp.json()
			st.success(f"Score: {res['score']}%, Passed: {res['passed_overall']}")
			st.json(res)
		except requests.HTTPError as e:
			st.error(f"Upload failed: {e.response.text}")
		except Exception as e:
			st.error(f"Error: {e}")