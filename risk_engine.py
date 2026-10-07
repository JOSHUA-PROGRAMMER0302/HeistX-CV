def calculate_risk(
    loitering=False,
    running=False
):

    score = 0

    if loitering:
        score += 60

    if running:
        score += 40

    if score >= 80:
        level = "HIGH"

    elif score >= 40:
        level = "MEDIUM"

    else:
        level = "LOW"

    return score, level