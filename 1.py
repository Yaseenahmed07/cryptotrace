import streamlit as st

st.set_page_config(
    page_title="CryptoTrace AI",
    page_icon="🔍",
    layout="wide"
)

st.title("CryptoTrace AI")
st.subheader("Blockchain Forensics Engine")

st.sidebar.header("Investigation Panel")

wallet = st.sidebar.text_input("Enter Wallet Address")

if st.sidebar.button("Investigate Wallet"):
    if wallet:
        st.success("Investigation started!")
        st.write("Wallet Address:", wallet)
    else:
        st.warning("Enter a wallet address")

st.info("Welcome to CryptoTrace AI")

col1, col2, col3 = st.columns(3)

col1.metric("Wallets Traced", "0")
col2.metric("Suspicious Transactions", "0")
col3.metric("Risk Level", "Pending")

st.write("Transaction Analysis")



