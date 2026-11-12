def calculate_risk(suspicious, peel_chains, smurfing):
    score = 0
    reasons = []

    if suspicious:
        score += min(len(suspicious) * 10, 30)
        reasons.append(
            "Suspicious transaction patterns detected"
        )

    if peel_chains:
        score += 30
        reasons.append(
            "Possible peel-chain activity detected"
        )

    if smurfing:
        score += 25
        reasons.append(
            "Possible multiple-output splitting detected"
        )

    score = min(score, 100)

    if score >= 70:
        level = "High"
    elif score >= 40:
        level = "Medium"
    else:
        level = "Low"

    return {
        "risk_score": score,
        "risk_level": level,
        "reasons": reasons
    }
