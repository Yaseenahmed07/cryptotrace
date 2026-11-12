import streamlit as st

st.set_page_config(
    page_title="CryptoTrace AI",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 CryptoTrace AI")
st.subheader("Blockchain Forensics & Transaction Analysis")

st.write(
    "Investigate blockchain transactions, "
    "identify suspicious patterns and analyse wallet risk."
)

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a section",
    ["Dashboard", "Wallet Investigation", "About"]
)

if page == "Dashboard":
    st.header("Investigation Dashboard")
    col1, col2, col3 = st.columns(3)

    col1.metric("Transactions Analysed", "0")
    col2.metric("Wallets Identified", "0")
    col3.metric("Suspicious Patterns", "0")

    st.info("Welcome! Start by entering a wallet address.")

elif page == "Wallet Investigation":
    st.header("Wallet Investigation")

    wallet = st.text_input("Enter Ethereum wallet address")

    if st.button("Investigate Wallet"):
        if wallet.startswith("0x") and len(wallet) == 42:
            st.success("Wallet address format is valid!")
            st.write("Next, we will connect this wallet to our analysis engine.")
        else:
            st.error("Please enter a valid Ethereum wallet address.")

elif page == "About":
    st.header("About CryptoTrace AI")
    st.write(
        "CryptoTrace AI is a blockchain forensics project "
        "designed to trace transactions and detect suspicious activity."
    )
