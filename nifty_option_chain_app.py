import streamlit as st
from kiteconnect import KiteConnect
import pandas as pd
import os
from dotenv import load_dotenv

st.set_page_config(page_title="NIFTY Option Chain Viewer", layout="wide")
st.title("📈 Live NIFTY Option Chain – Zerodha API")

load_dotenv()
api_key = os.getenv("Z_API_KEY")
access_token = os.getenv("Z_ACCESS_TOKEN")

# Zerodha session
kite = KiteConnect(api_key=api_key)
try:
    kite.set_access_token(access_token)
except Exception as e:
    st.error("❌ Access token invalid or expired. Run the token generator.")
    st.stop()

# Cache instruments list
@st.cache_data(ttl=3600)
def get_instruments():
    df = pd.DataFrame(kite.instruments("NFO"))
    return df

instruments = get_instruments()

# Filter NIFTY options
nifty_options = instruments[
    (instruments['name'] == 'NIFTY') & 
    (instruments['segment'] == 'NFO-OPT')
]

# Select expiry
expiries = sorted(nifty_options['expiry'].unique())
selected_expiry = st.selectbox("🗓️ Select Expiry Date", expiries)

# Filter for selected expiry
filtered = nifty_options[nifty_options['expiry'] == selected_expiry]

# Get required columns
option_df = filtered[['instrument_token', 'tradingsymbol', 'strike', 'instrument_type']].copy()

# Fetch LTPs
ltp_dict = kite.ltp(option_df['instrument_token'].tolist())
option_df['ltp'] = option_df['instrument_token'].map(lambda x: ltp_dict.get(x, {}).get('last_price', None))

# Pivot into Option Chain
chain = option_df.pivot_table(index='strike', columns='instrument_type', values='ltp').reset_index()
chain = chain.sort_values('strike')

# Rename columns
chain = chain.rename(columns={'CE': 'Call LTP', 'PE': 'Put LTP'})

st.dataframe(chain, use_container_width=True)

st.markdown("""
🔹 Data fetched live using Zerodha API  
🔹 This table shows Call/Put LTPs grouped by Strike  
🔹 Use this to identify OTM/ATM/ITM contracts
""")
