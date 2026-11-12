def rank_end_receivers(graph, start_wallet, max_hops=3):
    results = []

    def explore(current, path, depth):
        if depth == max_hops:
            if graph.out_degree(current) == 0:
                results.append({
                    "wallet": current,
                    "path": path.copy(),
                    "hops": depth,
                    "reason": "No outgoing transactions found"
                })
            return

        neighbours = list(graph.successors(current))

        if not neighbours and depth > 0:
            results.append({
                "wallet": current,
                "path": path.copy(),
                "hops": depth,
                "reason": "No outgoing transactions found"
            })
            return

        for neighbour in neighbours:
            if neighbour not in path:
                explore(neighbour, path + [neighbour], depth + 1)

    if start_wallet not in graph:
        return []

    explore(start_wallet, [start_wallet], 0)

    # Remove duplicate receiver entries
    unique = {}

    for item in results:
        unique[item["wallet"]] = item

    return list(unique.values())
