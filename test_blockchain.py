from blockchain import get_transactions
from audit_log import save_audit_log,verify_audit_log
from risk_engine import calculate_risk
from graph_analysis import build_transaction_graph
from detection import detect_peel_chain, detect_smurfing

wallet = "0x0000000000000000000000000000000000000000"

transactions = get_transactions(wallet)

print("Transactions fetched:", len(transactions))

graph = build_transaction_graph(transactions)

print("Wallets in graph:", graph.number_of_nodes())
print("Transaction connections:", graph.number_of_edges())

peel = detect_peel_chain(graph)
smurf = detect_smurfing(graph)

print("Peel chain results:", peel)
print("Smurfing results:", smurf)
risk=calculate_risk([],peel,smurf)
print("Risk analysis:",risk)
# Save investigation in audit log

save_audit_log(
    "Wallet Investigation",
    {
        "wallet": wallet,
        "risk_score": risk["risk_score"],
        "risk_level": risk["risk_level"],
        "transactions": len(transactions)
    }
)

# Verify audit log

print("Audit log valid:", verify_audit_log())
