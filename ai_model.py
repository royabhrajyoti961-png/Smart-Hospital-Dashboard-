def predict_risk(hr, oxygen):
    score = 0

    if oxygen < 90:
        score += 2
    elif oxygen < 95:
        score += 1

    if hr > 120 or hr < 50:
        score += 2
    elif hr > 100:
        score += 1

    if score >= 3:
        return "High Risk"
    elif score == 2:
        return "Medium Risk"
    else:
        return "Low Risk"
