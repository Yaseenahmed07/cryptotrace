def detect_suspicious_transactions(transactions):
    suspicious = []

    for tx in transactions:
        reasons = []

        if tx["amount"] < 0.01:
            reasons.append("Possible dust transaction")

        if tx["amount"] > 100:
            reasons.append("Unusually large transfer")

        if tx["from"] == tx["to"]:
            reasons.append("Self transfer")

        if reasons:
            suspicious.append({
                "transaction": tx,
                "reasons": reasons
            })

    return suspicious
def detect_peel_chain(graph, min_length=3):
    detected = []

    for start in graph.nodes():
        current = start
        path = [current]

        while graph.out_degree(current) == 1:
            next_wallet = next(graph.successors(current))

            if next_wallet in path:
                break

            path.append(next_wallet)
            current = next_wallet

        if len(path) >= min_length:
            detected.append({
                "pattern": "Possible Peel Chain",
                "wallet_path": path,
                "hops": len(path) - 1
            })

    return detected


def detect_smurfing(graph, minimum_outputs=3):
    detected = []

    for wallet in graph.nodes():
        neighbours = list(graph.successors(wallet))

        if len(neighbours) >= minimum_outputs:
            detected.append({
                "pattern": "Possible Smurfing",
                "source_wallet": wallet,
                "destination_wallets": neighbours,
                "number_of_outputs": len(neighbours)
            })

    return detected
