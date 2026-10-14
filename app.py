
import html
import streamlit as st
from analyzer import analyze_email



st.set_page_config(
    page_title="PhishMail | Email Security Analyzer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)



st.markdown(
    """
    <style>
    /* Main page */
    .stApp {
        background-color: #08111F;
        color: #E5EDF5;
    }

    .block-container {
        width: 100%;
        max-width: 1100px;
        box-sizing: border-box;
        padding: 2rem 1.25rem 3rem;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    /* HERO CARD */
    .hero {
        width: 100%;
        box-sizing: border-box;
        background: linear-gradient(135deg, #101F33 0%, #0B1929 100%);
        border: 1px solid #24394D;
        border-radius: 20px;
        padding: 30px 34px;
        margin: 0 0 30px 0;
        overflow: hidden;
    }

    .eyebrow {
        display: block;
        color: #5EEAD4;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2.5px;
        line-height: 1.5;
        margin: 0 0 18px 0;
    }

    .hero-title {
        color: #F1F5F9;
        font-size: clamp(30px, 4vw, 44px);
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: -1.2px;
        margin: 0 0 14px 0;
        overflow-wrap: anywhere;
    }

    .hero-description {
        color: #A9BACB;
        font-size: 15px;
        line-height: 1.8;
        max-width: 680px;
        margin: 0 0 22px 0;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        color: #5EEAD4;
        background: #102D32;
        border: 1px solid #24514F;
        border-radius: 30px;
        padding: 8px 13px;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1px;
        line-height: 1.5;
    }

    /* Section headings */
    .section-heading {
        color: #F1F5F9;
        font-size: 24px;
        font-weight: 750;
        line-height: 1.3;
        margin: 0 0 8px 0;
    }

    .section-description {
        color: #94A9BC;
        font-size: 14px;
        line-height: 1.7;
        margin-bottom: 20px;
    }

    /* Input labels */
    div[data-testid="stTextInput"] label,
    div[data-testid="stTextArea"] label {
        color: #D7E4EF !important;
        font-weight: 700 !important;
        font-size: 12px !important;
        letter-spacing: 1px;
    }

    /* Input fields */
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {
        background-color: #0D1B2A !important;
        color: #E5EDF5 !important;
        border: 1px solid #294057 !important;
        border-radius: 10px !important;
        box-sizing: border-box;
    }

    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus {
        border-color: #5EEAD4 !important;
        box-shadow: 0 0 0 1px #5EEAD4 !important;
    }

    /* Analyze button */
    div[data-testid="stFormSubmitButton"] > button {
        width: 100%;
        min-height: 46px;
        background-color: #5EEAD4 !important;
        color: #08111F !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        transition: background-color 0.2s ease;
    }

    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #99F6E4 !important;
    }

    /* Results metrics */
    div[data-testid="stMetric"] {
        background: #0D1B2A;
        border: 1px solid #20364A;
        border-radius: 14px;
        padding: 16px;
        box-sizing: border-box;
    }

    div[data-testid="stMetricLabel"] {
        color: #9EB1C4 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #F1F5F9 !important;
        overflow-wrap: anywhere;
    }

    /* Risk status cards */
    .risk-high,
    .risk-medium,
    .risk-low {
        border-radius: 10px;
        padding: 14px 16px;
        margin: 16px 0;
        line-height: 1.7;
        overflow-wrap: anywhere;
    }

    .risk-high {
        color: #FCA5A5;
        background: #351A24;
        border: 1px solid #71313C;
    }

    .risk-medium {
        color: #FCD34D;
        background: #302819;
        border: 1px solid #665027;
    }

    .risk-low {
        color: #6EE7B7;
        background: #102C29;
        border: 1px solid #24564C;
    }

    /* Individual findings */
    .finding-card {
        background: #0D1B2A;
        border: 1px solid #20364A;
        border-left: 4px solid #5EEAD4;
        border-radius: 10px;
        padding: 15px 18px;
        margin-bottom: 12px;
        box-sizing: border-box;
        overflow-wrap: anywhere;
    }

    .finding-title {
        color: #F1F5F9;
        font-size: 15px;
        font-weight: 750;
        line-height: 1.5;
        margin-bottom: 8px;
    }

    .finding-detail {
        color: #B3C3D2;
        font-size: 13px;
        line-height: 1.6;
        overflow-wrap: anywhere;
        word-break: break-word;
    }

    .finding-points {
        color: #5EEAD4;
        font-size: 12px;
        font-weight: 750;
        margin-top: 9px;
    }

    /* Footer */
    .footer {
        color: #71869A;
        text-align: center;
        font-size: 12px;
        line-height: 1.8;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #203044;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* Mobile layout */
    @media (max-width: 600px) {
        .block-container {
            padding: 1rem 0.75rem 2rem;
        }

        .hero {
            padding: 24px 20px;
            border-radius: 16px;
        }

        .eyebrow {
            letter-spacing: 2px;
        }

        .hero-title {
            letter-spacing: -0.5px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)



st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">EMAIL SECURITY ANALYZER</div>
        <div class="hero-title">Know What's in Your Inbox.</div>
        <div class="hero-description">
            Inspect email content for suspicious language, risky URL
            patterns, and potential phishing indicators.
        </div>
        <div class="status-pill">
            ●&nbsp; RULE-BASED ANALYSIS ENGINE
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)



st.markdown(
    '<div class="section-heading">Analyze an email</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-description">
        Paste an email below to check for potential phishing indicators.
        Use fictional or sample emails. Never include real passwords,
        OTPs, or other sensitive information.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("email_analysis_form"):
    subject = st.text_input(
        "EMAIL SUBJECT",
        placeholder="Example: Urgent — Verify your account",
    )

    message = st.text_area(
        "EMAIL MESSAGE",
        placeholder=(
            "Paste the email body here...\n\n"
            "Example: Your account requires verification. "
            "Visit http://example.com to continue."
        ),
        height=190,
    )

    submitted = st.form_submit_button("Analyze Email")


if submitted:
    if not subject.strip() and not message.strip():
        st.warning("Please enter an email subject or message first.")

    else:
        try:
            warnings, risk_score, risk_level = analyze_email(
                subject.strip(),
                message.strip(),
            )

            # Validate the returned score.
            risk_score = max(0, min(100, int(risk_score)))

            # Keep the displayed category consistent with the score.
            if risk_score >= 50:
                risk_level = "High"
            elif risk_score >= 20:
                risk_level = "Medium"
            else:
                risk_level = "Low"

            st.divider()

            st.markdown(
                '<div class="section-heading">Analysis results</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="section-description">
                    Review the score and individual indicators identified
                    by the rule-based analyzer.
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Summary metrics
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("RISK SCORE", f"{risk_score}/100")

            with col2:
                st.metric("RISK LEVEL", risk_level)

            with col3:
                st.metric("INDICATORS FOUND", len(warnings))

            # Risk explanation
            risk_classes = {
                "High": "risk-high",
                "Medium": "risk-medium",
                "Low": "risk-low",
            }

            risk_messages = {
                "High": (
                    "HIGH RISK — Warning indicators were detected. "
                    "Avoid interacting with suspicious links or attachments."
                ),
                "Medium": (
                    "MEDIUM RISK — Some warning indicators were detected. "
                    "Verify the sender and links independently."
                ),
                "Low": (
                    "LOW RISK — Few or no indicators matched. "
                    "This does not guarantee that the email is safe."
                ),
            }

            st.markdown(
                f'<div class="{risk_classes[risk_level]}">'
                f'<strong>{risk_messages[risk_level]}</strong>'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Findings
            st.markdown(
                '<div class="section-heading">Detected indicators</div>',
                unsafe_allow_html=True,
            )

            if warnings:
                for index, warning in enumerate(warnings, start=1):
                    warning_type = html.escape(
                        str(warning.get("type", "Warning"))
                    )
                    warning_detail = html.escape(
                        str(warning.get("detail", "No details available"))
                    )

                    try:
                        points = int(warning.get("points", 0))
                    except (TypeError, ValueError):
                        points = 0

                    st.markdown(
                        f"""
                        <div class="finding-card">
                            <div class="finding-title">
                                {index}. {warning_type}
                            </div>
                            <div class="finding-detail">
                                {warning_detail}
                            </div>
                            <div class="finding-points">
                                Rule contribution: +{points} points
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            else:
                st.success(
                    "No indicators matched the current rules. "
                    "A phishing email may still go undetected."
                )

            # Safety recommendations
            st.markdown(
                '<div class="section-heading">Safety recommendations</div>',
                unsafe_allow_html=True,
            )

            recommendations = [
                "Check the sender's full email address, not just their display name.",
                "Never share passwords or OTPs through links in unsolicited emails.",
                "Visit official websites by typing their address yourself.",
                "Be cautious of messages that pressure you to act immediately.",
                "Verify unexpected requests through an official communication channel.",
            ]

            for recommendation in recommendations:
                st.markdown(f"- {recommendation}")

            # Explain the scoring system
            with st.expander("How does the risk score work?"):
                st.write(
                    """
                    PhishMail uses predefined rules rather than a trained
                    machine-learning model. It checks for suspicious phrases
                    and URL patterns such as unencrypted HTTP links, known
                    URL shorteners, and IP addresses used as website hosts.
                    """
                )

                st.write(
                    """
                    Matching rules add points, and the total is capped at 100.
                    Scores of 0–19 are Low, 20–49 are Medium, and 50–100
                    are High.
                    """
                )

                st.info(
                    "The score is illustrative, not a calibrated probability "
                    "of phishing. The analyzer does not verify sender identity, "
                    "visit links, inspect website content, or guarantee detection."
                )

        except Exception as error:
            st.error(
                "The email could not be analyzed. Check that analyzer.py "
                "is in the same folder and that analyze_email() returns "
                "warnings, risk_score, and risk_level."
            )

            with st.expander("Technical details"):
                st.code(str(error))


st.markdown(
    """
    <div class="footer">
        PhishMail · Email Security Analyzer<br>
        A rule-based educational project for phishing awareness.
    </div>
    """,
    unsafe_allow_html=True,
)
