def rank_end_receivers(graph, start_wallet, max_hops=3):
    """
    Identify possible terminal receivers reachable
    from a starting wallet within the hop limit.
    """

    receivers = []
    visited_receivers = set()

    # Check whether starting wallet exists
    if start_wallet not in graph:
        return receivers

    def explore(current_wallet, path):

        current_hops = len(path) - 1

        # Find outgoing transactions
        neighbours = list(graph.successors(current_wallet))

        # Check terminal wallet BEFORE hop limit
        if current_wallet != start_wallet and len(neighbours) == 0:

            if current_wallet not in visited_receivers:

                visited_receivers.add(current_wallet)

                receivers.append({
                    "wallet": current_wallet,
                    "path": path.copy(),
                    "hops": current_hops,
                    "reason": (
                        "No outgoing transactions found "
                        "within the supplied transaction dataset."
                    )
                })

            return

        # Stop tracing at maximum hop limit
        if current_hops >= max_hops:
            return

        # Explore connected wallets
        for neighbour in neighbours:

            # Prevent cycles
            if neighbour not in path:

                explore(
                    neighbour,
                    path + [neighbour]
                )

    # Start investigation
    explore(start_wallet, [start_wallet])

    # Sort by number of hops
    receivers.sort(key=lambda receiver: receiver["hops"])

    return receivers
