import streamlit as st
from kiteconnect import KiteConnect
import os

ENV_FILE_PATH = ".env"

st.set_page_config(page_title="Zerodha Access Token Updater", layout="centered")
st.title("🔐 Update Zerodha Access Token")

# Input fields
api_key = st.text_input("📎 Kite API Key", value=os.getenv("Z_API_KEY", ""))
api_secret = st.text_input("🔑 Kite API Secret", type="password", value=os.getenv("Z_API_SECRET", ""))
request_token = st.text_input("📥 Paste your `request_token` from login URL")

if st.button("⚙️ Generate and Save Access Token"):
    if not (api_key and api_secret and request_token):
        st.warning("Please fill all fields before proceeding.")
        st.stop()

    try:
        kite = KiteConnect(api_key=api_key)
        session_data = kite.generate_session(request_token, api_secret=api_secret)
        access_token = session_data["access_token"]

        st.success("✅ Access Token generated successfully!")
        st.code(access_token, language="bash")

        # Update .env file
        updated_lines = []
        env_keys = {"Z_API_KEY": api_key, "Z_API_SECRET": api_secret, "Z_ACCESS_TOKEN": access_token}

        # Load existing .env or create new
        if os.path.exists(ENV_FILE_PATH):
            with open(ENV_FILE_PATH, "r") as f:
                lines = f.readlines()
            for line in lines:
                key = line.strip().split("=")[0]
                if key in env_keys:
                    updated_lines.append(f"{key}={env_keys[key]}\n")
                    env_keys.pop(key)
                else:
                    updated_lines.append(line)
        else:
            updated_lines = []

        # Add remaining keys
        for k, v in env_keys.items():
            updated_lines.append(f"{k}={v}\n")

        # Save .env
        with open(ENV_FILE_PATH, "w") as f:
            f.writelines(updated_lines)

        st.success("💾 `.env` file updated successfully!")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.info("""
🔹 First, use `login_zerodha.py` or browser to get `request_token`.  
🔹 This tool will then generate the daily `access_token` and update `.env`.  
🔹 Use this daily before launching your algo app.
""")
