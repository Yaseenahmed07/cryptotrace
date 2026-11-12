import networkx as nx


def normalize_address(address):
    """Normalize wallet addresses for consistent matching."""
    if not address:
        return ""

    return str(address).strip().lower()


def build_transaction_graph(transactions):
    """Build a directed graph from blockchain transactions."""

    graph = nx.DiGraph()

    for tx in transactions:

        source = normalize_address(tx.get("from"))
        target = normalize_address(tx.get("to"))

        if not source or not target:
            continue

        try:
            amount = float(
                tx.get("amount", tx.get("value", 0)) or 0
            )
        except (ValueError, TypeError):
            amount = 0.0

        graph.add_edge(
            source,
            target,
            amount=amount
        )

    return graph


def trace_paths(graph, wallet, hops=3, max_paths=100):
    """Find outgoing transaction paths up to the specified hops."""

    wallet = normalize_address(wallet)

    if wallet not in graph:
        return []

    paths = []

    def explore(current, path):

        if len(paths) >= max_paths:
            return

        if len(path) > 1:
            paths.append(path.copy())

        if len(path) - 1 >= hops:
            return

        for neighbour in graph.successors(current):

            if neighbour not in path:
                explore(neighbour, path + [neighbour])

    explore(wallet, [wallet])

    return paths


def trace_wallet(graph, wallet, hops=3):
    """Return all unique wallets found in traced paths."""

    paths = trace_paths(graph, wallet, hops)

    wallets = []

    for path in paths:
        for address in path:

            if address not in wallets:
                wallets.append(address)

    return wallets


def get_path_details(graph, paths):
    """Get transaction details for every traced path."""

    results = []

    for path in paths:

        transactions = []

        for i in range(len(path) - 1):

            source = path[i]
            target = path[i + 1]

            details = graph.get_edge_data(source, target) or {}

            transactions.append({
                "from": source,
                "to": target,
                "amount": details.get("amount", 0)
            })

        results.append({
            "path": path,
            "transactions": transactions,
            "hops": len(path) - 1
        })

    return results
