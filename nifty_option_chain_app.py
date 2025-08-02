import streamlit as st
import pandas as pd
from kiteconnect import KiteConnect
import os
from dotenv import load_dotenv

# Load Zerodha credentials
load_dotenv()
api_key = os.getenv("Z_API_KEY")
access_token = os.getenv("Z_ACCESS_TOKEN")

# Initialize Kite Connect
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

st.set_page_config(page_title="NIFTY Option Chain Viewer", layout="wide")
st.title("🔗 Live NIFTY Option Chain (Zerodha API)")

# Get instrument list (cached for performance)
@st.cache_data(ttl=3600)
def load_instruments():
    return pd.DataFrame(kite.instruments("NSE"))

instruments_df = load_instruments()

# Filter only NIFTY options
nifty_options = instruments_df[
    (instruments_df['name'] == 'NIFTY') & (instruments_df['instrument_type'] == 'CE')
]

# Expiry filter
expiries = sorted(nifty_options['expiry'].unique())
selected_expiry = st.selectbox("📆 Select Expiry Date", expiries)

# Filter all options (CE + PE) for that expiry
filtered = instruments_df[
    (instruments_df['name'] == 'NIFTY') &
    (instruments_df['expiry'] == selected_expiry) &
    (instruments_df['instrument_type'].isin(['CE', 'PE']))
]

# Get LTPs in batch
tokens = filtered['instrument_token'].tolist()
ltps = kite.ltp(tokens)

# Parse LTPs
filtered['ltp'] = filtered['instrument_token'].apply(lambda x: ltps.get(x, {}).get('last_price', None))

# Pivot into option chain format
pivot_df = filtered.pivot_table(
    index='strike',
    columns='instrument_type',
    values='ltp',
    aggfunc='first'
).reset_index().sort_values('strike')

st.dataframe(pivot_df, use_container_width=True)

st.markdown("""
- 💡 Use this as a live NIFTY option chain viewer.
- Data updates every time you refresh or rerun.
""")
