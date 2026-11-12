import re
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

from blockchain import get_transactions
from audit_log import save_audit_log, verify_audit_log
from risk_engine import calculate_risk
from graph_analysis import (
    build_transaction_graph,
    trace_paths,
    trace_wallet,
    get_path_details
)
from detection import detect_peel_chain, detect_smurfing


# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="CryptoTrace AI",
    page_icon="🔎",
    layout="wide"
)


# --------------------------------
# CUSTOM STYLE
# --------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------
# HEADER
# --------------------------------

st.title("🔎 CryptoTrace AI")

st.subheader("Blockchain Forensics & Transaction Analysis")

st.write(
    "Investigate blockchain transactions, "
    "identify suspicious patterns and analyse wallet risk."
)

st.divider()


# --------------------------------
# WALLET INVESTIGATION
# --------------------------------

st.header("Wallet Investigation")

wallet = st.text_input(
    "Enter Ethereum wallet address",
    placeholder="0x..."
)

investigate = st.button("Investigate Wallet")


if investigate:

    # Validate wallet address
    if not re.fullmatch(r"0x[a-fA-F0-9]{40}", wallet):

        st.error("Please enter a valid Ethereum wallet address.")

    else:

        st.success("Wallet address format is valid!")

        with st.spinner("Fetching blockchain transactions..."):

            try:

                # Fetch transactions
                transactions = get_transactions(wallet)

                if not transactions:

                    st.warning(
                        "No transactions found or blockchain API request failed."
                    )

                else:

                    # --------------------------------
                    # BUILD TRANSACTION GRAPH
                    # --------------------------------

                    st.divider()
                    st.header("Investigation Results")

                    graph = build_transaction_graph(transactions)

                    # --------------------------------
                    # MULTI-HOP TRANSACTION TRACING
                    # --------------------------------

                    st.subheader("Multi-Hop Transaction Tracing")

                    paths = trace_paths(
                        graph,
                        wallet,
                        hops=3,
                        max_paths=20
                    )

                    traced_wallets = trace_wallet(
                        graph,
                        wallet,
                        hops=3
                    )

                    path_details = get_path_details(
                        graph,
                        paths
                    )

                    col1, col2 = st.columns(2)

                    col1.metric(
                        "Wallets Traced",
                        len(traced_wallets)
                    )

                    col2.metric(
                        "Transaction Paths Found",
                        len(paths)
                    )

                    if path_details:

                        for index, path in enumerate(
                            path_details,
                            start=1
                        ):

                            st.write(f"Path {index}")
                            st.json(path)

                    else:

                        st.info(
                            "No outgoing transaction paths found within 3 hops."
                        )

                    # --------------------------------
                    # DETECT SUSPICIOUS PATTERNS
                    # --------------------------------

                    st.divider()
                    st.header("Suspicious Activity")

                    peel = detect_peel_chain(graph)

                    smurf = detect_smurfing(graph)

                    st.subheader("Peel Chain Detection")

                    if peel:
                        st.warning("Possible peel-chain pattern detected.")
                        st.json(peel)
                    else:
                        st.success("No peel-chain pattern detected.")

                    st.subheader("Smurfing Detection")

                    if smurf:
                        st.warning("Possible smurfing pattern detected.")
                        st.json(smurf)
                    else:
                        st.success("No smurfing pattern detected.")

                    # --------------------------------
                    # CALCULATE WALLET RISK
                    # --------------------------------

                    st.divider()
                    st.header("Wallet Risk Analysis")

                    risk = calculate_risk(
                        [],
                        peel,
                        smurf
                    )

                    risk_score = risk.get("risk_score", 0)

                    risk_level = risk.get(
                        "risk_level",
                        "Unknown"
                    )

                    reasons = risk.get("reasons", [])

                    col1, col2 = st.columns(2)

                    col1.metric(
                        "Risk Score",
                        risk_score
                    )

                    col2.metric(
                        "Risk Level",
                        risk_level
                    )

                    st.write("### Risk Assessment Reasons")

                    if reasons:

                        for reason in reasons:
                            st.write("•", reason)

                    else:

                        st.info("No risk indicators identified.")

                    # --------------------------------
                    # TRANSACTION FLOW VISUALIZATION
                    # --------------------------------

                    st.divider()

                    st.header("Transaction Flow Visualization")

                    net = Network(
                        height="550px",
                        width="100%",
                        directed=True,
                        bgcolor="#0e1117",
                        font_color="white"
                    )

                    # Add wallet nodes
                    for node in graph.nodes():

                        net.add_node(
                            str(node),
                            label=str(node)[:12] + "...",
                            title=str(node),
                            color="#00b4d8"
                        )

                    # Add transaction connections
                    for source, destination in graph.edges():

                        net.add_edge(
                            str(source),
                            str(destination),
                            color="#aaaaaa",
                            arrows="to"
                        )

                    html = net.generate_html()

                    components.html(
                        html,
                        height=570,
                        scrolling=True
                    )

                    # --------------------------------
                    # FORENSIC AUDIT LOG
                    # --------------------------------

                    st.divider()

                    st.header("Forensic Audit Log")

                    save_audit_log(
                        "Wallet Investigation",
                        {
                            "wallet": wallet,
                            "risk_score": risk_score,
                            "risk_level": risk_level,
                            "transactions": len(transactions)
                        }
                    )

                    if verify_audit_log():

                        st.success(
                            "Audit log verified successfully!"
                        )

                    else:

                        st.error(
                            "Audit log verification failed."
                        )

                    st.success("Investigation completed!")

            except Exception as error:

                st.error(
                    f"Investigation failed: {error}"
                )


# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.caption(
    "CryptoTrace AI | Blockchain Forensics & Transaction Analysis"
)

st.caption(
    "Risk scores indicate suspicious patterns, "
    "not proof of criminal activity."
)
