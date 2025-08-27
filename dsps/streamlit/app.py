import os
import streamlit as st

st.set_page_config(page_title="DSPS (Streamlit)", page_icon="🧪", layout="centered")

st.title("Decentralized Skill Proof System (Streamlit)")

api_base = os.getenv("API_BASE_URL", "http://localhost:8000")
if "API_BASE_URL" not in st.session_state:
	st.session_state["API_BASE_URL"] = api_base

st.info(
	"Use the pages in the left sidebar to Upload code, check Results, or Verify on-chain records.\n"
	"Make sure your backend is running at: " + st.session_state["API_BASE_URL"],
)

st.write("\n")
st.markdown("- Upload: submit a Python file with `solve(input)`; get score and certificate")
st.markdown("- Results: fetch result by ID, push to chain if needed, download certificate")
st.markdown("- Verify: enter a wallet to read on-chain records")