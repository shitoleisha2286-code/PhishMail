
import re
import ipaddress
from urllib.parse import urlsplit


# Suspicious phrases to check in emails
SUSPICIOUS_PHRASES = [
    "urgent",
    "verify your password",
    "account suspended",
    "click here immediately",
    "confirm your otp",
]

# Common URL-shortening services
URL_SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "is.gd",
}


def analyze_email(subject, message):
    warnings = []
    risk_score = 0

    # Combine the subject and message
    email_text = f"{subject} {message}".lower()

    # Check for suspicious phrases
    for phrase in SUSPICIOUS_PHRASES:
        if phrase in email_text:
            warnings.append({
                "type": "Suspicious phrase",
                "detail": phrase,
                "points": 10,
            })
            risk_score += 10

    # Find URLs in the email text
    urls = re.findall(r'https?://[^\s<>"\']+', email_text)

    for raw_url in urls:
        # Remove punctuation following a URL
        url = raw_url.rstrip(".,!?;:)]}")

        try:
            parsed_url = urlsplit(url)
            hostname = parsed_url.hostname

            if not hostname:
                continue

            hostname = hostname.lower()

        except ValueError:
            continue

        # Check for unencrypted HTTP
        if parsed_url.scheme == "http":
            warnings.append({
                "type": "Unencrypted HTTP link",
                "detail": url,
                "points": 15,
            })
            risk_score += 15

        # Check for known URL shorteners
        if hostname in URL_SHORTENERS:
            warnings.append({
                "type": "URL shortener",
                "detail": hostname,
                "points": 15,
            })
            risk_score += 15

        # Check whether the hostname is an IP address
        try:
            ipaddress.ip_address(hostname)
            is_ip_address = True
        except ValueError:
            is_ip_address = False

        if is_ip_address:
            warnings.append({
                "type": "IP address used as website",
                "detail": hostname,
                "points": 25,
            })
            risk_score += 25

    # Keep the score within 0–100
    risk_score = min(risk_score, 100)

    # Assign a risk category
    if risk_score >= 50:
        risk_level = "High"
    elif risk_score >= 20:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    
    return warnings, risk_score, risk_level
