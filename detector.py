def detect_phishing(email_text):
    suspicious_words = [
        "urgent",
        "verify",
        "password",
        "bank",
        "login",
        "click here",
        "account suspended"
    ]

    score = 0

    for word in suspicious_words:
        if word.lower() in email_text.lower():
            score += 15

    if score >= 50:
        return "High Risk", score
    elif score >= 25:
        return "Medium Risk", score
    else:
        return "Low Risk", score

