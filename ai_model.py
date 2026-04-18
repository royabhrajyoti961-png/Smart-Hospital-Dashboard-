def predict_risk(hr, oxygen):
    if oxygen < 90 or hr > 120:
        return "High Risk"
    elif oxygen < 95:
        return "Medium Risk"
    else:
        return "Low Risk"
