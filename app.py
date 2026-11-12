import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go

from detection import detect_suspicious_transactions
from graph_analysis import build_transaction_graph, trace_wallet
from audit_log import save_audit_log

st.set_page_config(
    page_title="CryptoTrace AI",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 CryptoTrace AI")
st.subheader("Blockchain Forensics & Transaction Intelligence")

# Sample transaction dataset
transactions = [
    {"from": "Wallet_A", "to": "Wallet_B", "amount": 50},
    {"from": "Wallet_B", "to": "Wallet_C", "amount": 45},
    {"from": "Wallet_C", "to": "Wallet_D", "amount": 0.005},
    {"from": "Wallet_D", "to": "Wallet_E", "amount": 120},
    {"from": "Wallet_A", "to": "Wallet_F", "amount": 0.002},
    {"from": "Wallet_F", "to": "Wallet_G", "amount": 20},
    {"from": "Wallet_G", "to": "Wallet_G", "amount": 5}
]

st.sidebar.header("Investigation Panel")

wallet = st.sidebar.selectbox(
    "Select starting wallet",
    ["Wallet_A", "Wallet_B", "Wallet_C"]
)

if st.sidebar.button("Investigate Wallet"):

    graph = build_transaction_graph(transactions)

    traced = trace_wallet(graph, wallet, 3)

    suspicious = detect_suspicious_transactions(transactions)

    risk = min(len(suspicious) * 15, 100)

    save_audit_log(
        "Wallet Investigation",
        {"wallet": wallet, "risk_score": risk}
    )

    st.success("Investigation completed!")

    col1, col2, col3 = st.columns(3)

    col1.metric("Wallets Traced", len(traced))
    col2.metric("Suspicious Transactions", len(suspicious))
    col3.metric("Risk Score", str(risk) + "/100")

    st.subheader("Wallet Trace Results")
    st.write(traced)

    st.subheader("Suspicious Transactions")

    for item in suspicious:
        st.warning(
            str(item["transaction"]) +
            " | Reasons: " + ", ".join(item["reasons"])
        )

    st.subheader("Transaction Network")

    positions = nx.spring_layout(graph, seed=42)

    edge_x = []
    edge_y = []

    for source, target in graph.edges():
        x0, y0 = positions[source]
        x1, y1 = positions[target]

        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(width=2, color="gray"),
        hoverinfo="none"
    )

    node_trace = go.Scatter(
        x=[positions[n][0] for n in graph.nodes()],
        y=[positions[n][1] for n in graph.nodes()],
        mode="markers+text",
        text=list(graph.nodes()),
        textposition="top center",
        marker=dict(
            size=25,
            color="orange"
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace])

    fig.update_layout(
        title="Wallet-to-Wallet Transaction Flow",
        showlegend=False,
        template="plotly_dark"
    )

    st.plotly_chart(fig, width="stretch")

    st.subheader("Risk Score Explanation")

    st.write("Risk score is a demonstration heuristic, not a probability.")

    st.write("Detected suspicious patterns:")

    for item in suspicious:
        st.write(
            "- " + ", ".join(item["reasons"])
        )

    st.subheader("Forensic Audit")

    st.write("Audit entry hash:")

    st.code(
        save_audit_log(
            "Investigation Report",
            {"wallet": wallet, "risk_score": risk}
        )
    )


