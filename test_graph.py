from graph_analysis import (
    build_transaction_graph,
    trace_paths,
    get_path_details
)

from receiver_analysis import rank_end_receivers


# =====================================
# SAMPLE BLOCKCHAIN TRANSACTIONS
# =====================================

transactions = [
    {"from": "A", "to": "B", "amount": 100},
    {"from": "B", "to": "C", "amount": 80},
    {"from": "C", "to": "D", "amount": 60},
    {"from": "B", "to": "E", "amount": 20},
    {"from": "A", "to": "F", "amount": 30},
    {"from": "F", "to": "G", "amount": 25},
    {"from": "G", "to": "H", "amount": 15},
    {"from": "A", "to": "I", "amount": 50},
    {"from": "I", "to": "J", "amount": 40},
]


# =====================================
# BUILD TRANSACTION GRAPH
# =====================================

graph = build_transaction_graph(transactions)


# =====================================
# TRACE UP TO 3 HOPS
# =====================================

start_wallet = "A"

print("=================================")
print("       CRYPTOTRACE AI")
print("=================================")

print("Starting wallet:", start_wallet)

paths = trace_paths(
    graph,
    start_wallet,
    hops=3
)

details = get_path_details(graph, paths)

print("\nNumber of paths:", len(details))


# =====================================
# DISPLAY TRANSACTION PATHS
# =====================================

print("\nTHREE-HOP TRACING RESULTS")

for path_data in details:

    print("\nWallet path:",
          " -> ".join(path_data["path"]))

    print("Hops:", path_data["hops"])

    print("Transactions:")

    for tx in path_data["transactions"]:

        print(
            tx["from"],
            "->",
            tx["to"],
            "| Amount:",
            tx["amount"]
        )


# =====================================
# END RECEIVER ANALYSIS
# =====================================

print("\n=================================")
print("       END RECEIVER ANALYSIS")
print("=================================")

receivers = rank_end_receivers(
    graph,
    start_wallet,
    max_hops=3
)

print("Receivers found:", len(receivers))


# =====================================
# DISPLAY RECEIVER DETAILS
# =====================================

if receivers:

    for receiver in receivers:

        print("\nWallet:", receiver["wallet"])

        print(
            "Path:",
            " -> ".join(receiver["path"])
        )

        print("Hops:", receiver["hops"])

        print("Reason:", receiver["reason"])

else:

    print("No end receivers identified.")


print("\n=================================")
print("       ANALYSIS COMPLETED")
print("=================================")
