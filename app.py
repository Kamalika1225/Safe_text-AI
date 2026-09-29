import streamlit as st
import pickle
import re
from datetime import datetime

# =========================================================
# LOAD MODEL
# =========================================================

with open("model/scam_detector.pkl", "rb") as file:
    model = pickle.load(file)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SafeText AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(0, 119, 255, 0.15), transparent 28%),
        radial-gradient(circle at 90% 20%, rgba(120, 70, 255, 0.12), transparent 25%),
        radial-gradient(circle at 50% 100%, rgba(0, 200, 170, 0.08), transparent 30%),
        #070b14;
    color: #f4f7fb;
}

/* Remove Streamlit top spacing */
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Header */
.brand {
    display: flex;
    align-items: center;
    gap: 14px;
}

.brand-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 25px;
    background: linear-gradient(135deg, #1479ff, #744cff);
    box-shadow: 0 0 30px rgba(54, 111, 255, 0.35);
}

.brand-name {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -1px;
}

.brand-name span {
    background: linear-gradient(90deg, #45a7ff, #a77bff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.status {
    margin-left: auto;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(27, 201, 145, 0.08);
    border: 1px solid rgba(27, 201, 145, 0.25);
    padding: 8px 14px;
    border-radius: 30px;
    color: #55e3b2;
    font-size: 13px;
    font-weight: 600;
}

.status-dot {
    width: 8px;
    height: 8px;
    background: #32e6a3;
    border-radius: 50%;
    box-shadow: 0 0 12px #32e6a3;
}

/* Hero */
.hero {
    text-align: center;
    padding: 65px 20px 45px;
}

.hero-badge {
    display: inline-block;
    padding: 7px 15px;
    border-radius: 30px;
    border: 1px solid rgba(103, 161, 255, 0.25);
    background: rgba(80, 130, 255, 0.08);
    color: #7eb6ff;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.hero h1 {
    font-size: 58px;
    line-height: 1.05;
    margin: 18px 0 15px;
    font-weight: 800;
    letter-spacing: -2px;
}

.gradient-text {
    background: linear-gradient(90deg, #4da6ff, #8b6cff, #c36cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    max-width: 680px;
    margin: auto;
    color: #8e9aae;
    font-size: 17px;
    line-height: 1.7;
}

/* Input card */
.input-card {
    background: rgba(16, 23, 37, 0.72);
    border: 1px solid rgba(120, 145, 180, 0.15);
    border-radius: 24px;
    padding: 28px;
    box-shadow:
        0 25px 80px rgba(0, 0, 0, 0.35),
        inset 0 1px rgba(255,255,255,0.04);
    backdrop-filter: blur(20px);
}

.card-title {
    font-size: 14px;
    color: #a9b5c8;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

/* Text area */
.stTextArea textarea {
    background: rgba(5, 10, 20, 0.85) !important;
    color: #edf3ff !important;
    border: 1px solid rgba(120, 145, 180, 0.18) !important;
    border-radius: 16px !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
}

.stTextArea textarea:focus {
    border: 1px solid #4b91ff !important;
    box-shadow: 0 0 0 1px #4b91ff, 0 0 25px rgba(75,145,255,0.15) !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    height: 52px;
    border-radius: 14px;
    border: 0;
    background: linear-gradient(90deg, #1479ff, #7654ff);
    color: white;
    font-size: 15px;
    font-weight: 700;
    box-shadow: 0 10px 30px rgba(59, 105, 255, 0.25);
    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 35px rgba(59, 105, 255, 0.4);
}

/* Stats */
.stat-card {
    background: rgba(16, 23, 37, 0.72);
    border: 1px solid rgba(120, 145, 180, 0.14);
    border-radius: 18px;
    padding: 22px;
    min-height: 125px;
}

.stat-label {
    color: #7f8da3;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 700;
}

.stat-value {
    font-size: 29px;
    font-weight: 800;
    margin-top: 9px;
}

.stat-sub {
    color: #6f7d91;
    font-size: 12px;
    margin-top: 5px;
}

/* Result */
.result-card {
    margin-top: 25px;
    padding: 30px;
    border-radius: 24px;
    background: rgba(16, 23, 37, 0.82);
    border: 1px solid rgba(120, 145, 180, 0.15);
}

.scam-result {
    border: 1px solid rgba(255, 76, 91, 0.35);
    box-shadow: 0 0 40px rgba(255, 50, 70, 0.08);
}

.safe-result {
    border: 1px solid rgba(48, 218, 157, 0.3);
    box-shadow: 0 0 40px rgba(48, 218, 157, 0.07);
}

.result-title {
    font-size: 25px;
    font-weight: 800;
}

.result-desc {
    color: #8b98ab;
    margin-top: 6px;
}

/* Warning cards */
.warning {
    background: rgba(255, 77, 91, 0.06);
    border: 1px solid rgba(255, 77, 91, 0.16);
    border-radius: 14px;
    padding: 15px;
    margin-top: 10px;
    color: #d9e0eb;
}

.safe-box {
    background: rgba(42, 218, 157, 0.06);
    border: 1px solid rgba(42, 218, 157, 0.16);
    border-radius: 14px;
    padding: 18px;
    color: #d9e0eb;
}

/* Risk meter */
.meter {
    height: 10px;
    background: #1b2433;
    border-radius: 20px;
    overflow: hidden;
    margin: 12px 0 20px;
}

.meter-fill {
    height: 100%;
    border-radius: 20px;
}

/* Feature cards */
.feature {
    background: rgba(16, 23, 37, 0.6);
    border: 1px solid rgba(120,145,180,0.12);
    border-radius: 18px;
    padding: 22px;
    height: 150px;
}

.feature-icon {
    font-size: 25px;
}

.feature-title {
    font-weight: 700;
    margin-top: 10px;
}

.feature-text {
    color: #78869a;
    font-size: 13px;
    margin-top: 5px;
    line-height: 1.5;
}

/* Hide Streamlit default */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="brand">
    <div class="brand-icon">🛡️</div>
    <div class="brand-name">Safe<span>Text AI</span></div>
    <div class="status">
        <div class="status-dot"></div>
        AI ENGINE ONLINE
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

<div class="hero-badge">
NLP • MACHINE LEARNING • MESSAGE SECURITY
</div>

<h1>
Think Before You <span class="gradient-text">Click.</span>
</h1>

<p>
An intelligent NLP-powered message analyzer that helps identify
potentially suspicious messages before you interact with them.
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# INPUT SECTION
# =========================================================

st.markdown("""
<div class="input-card">

<div class="card-title">
📩 Message Security Scanner
</div>

</div>
""", unsafe_allow_html=True)

message = st.text_area(
    "Message",
    height=150,
    placeholder="Paste an SMS, WhatsApp message, email or notification here...",
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    analyze = st.button(
        "⚡ ANALYZE MESSAGE",
        use_container_width=True
    )


# =========================================================
# ANALYSIS
# =========================================================

if analyze:

    if message.strip() == "":
        st.warning("Please enter a message to analyze.")

    else:

        prediction = model.predict([message])[0]

        # Model probability
        try:
            probabilities = model.predict_proba([message])[0]
            classes = model.classes_

            probability_dict = dict(zip(classes, probabilities))

            scam_probability = probability_dict.get("scam", 0)
            safe_probability = probability_dict.get("safe", 0)

        except:
            scam_probability = 0.5
            safe_probability = 0.5


        # =================================================
        # WARNING KEYWORDS
        # =================================================

        text_lower = message.lower()

        warning_signs = []

        urgent_words = [
            "urgent",
            "immediately",
            "now",
            "today",
            "hurry",
            "blocked",
            "suspended"
        ]

        money_words = [
            "won",
            "prize",
            "reward",
            "cash",
            "lottery",
            "money",
            "free"
        ]

        sensitive_words = [
            "otp",
            "password",
            "bank details",
            "account details",
            "verify",
            "verification",
            "kyc"
        ]

        link_words = [
            "click",
            "link",
            "http",
            "www"
        ]

        if any(word in text_lower for word in urgent_words):
            warning_signs.append(
                "⚠️ Urgent or threatening language detected"
            )

        if any(word in text_lower for word in money_words):
            warning_signs.append(
                "💰 Prize, reward or money-related content detected"
            )

        if any(word in text_lower for word in sensitive_words):
            warning_signs.append(
                "🔐 Sensitive information or verification requested"
            )

        if any(word in text_lower for word in link_words):
            warning_signs.append(
                "🔗 Link or click request detected"
            )


        # =================================================
        # RESULT
        # =================================================

        if prediction == "scam":

            risk_score = int(
                min(
                    99,
                    max(
                        55,
                        scam_probability * 100 + len(warning_signs) * 4
                    )
                )
            )

            st.markdown(
                f"""
                <div class="result-card scam-result">

                <div class="result-title">
                🚨 Potential Scam Detected
                </div>

                <div class="result-desc">
                The message contains patterns associated with suspicious messages.
                </div>

                <br>

                <b>Threat Indicator — {risk_score}%</b>

                <div class="meter">
                    <div class="meter-fill"
                    style="width:{risk_score}%;
                    background:linear-gradient(90deg,#ff5364,#ff8b5c);">
                    </div>
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            # Stats
            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(
                    f"""
                    <div class="stat-card">
                    <div class="stat-label">Classification</div>
                    <div class="stat-value">SCAM</div>
                    <div class="stat-sub">NLP prediction</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c2:
                st.markdown(
                    f"""
                    <div class="stat-card">
                    <div class="stat-label">Risk Level</div>
                    <div class="stat-value">HIGH</div>
                    <div class="stat-sub">Exercise caution</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c3:
                st.markdown(
                    f"""
                    <div class="stat-card">
                    <div class="stat-label">Warning Signals</div>
                    <div class="stat-value">{len(warning_signs)}</div>
                    <div class="stat-sub">Patterns detected</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            st.markdown("### 🔎 Why was this flagged?")

            if warning_signs:

                for warning in warning_signs:

                    st.markdown(
                        f"""
                        <div class="warning">
                        {warning}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.markdown(
                    """
                    <div class="warning">
                    ⚠️ The ML model identified suspicious language patterns.
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            st.markdown("### 🛡️ Recommended Action")

            st.markdown(
                """
                <div class="safe-box">

                <b>Don't interact with the message.</b><br><br>

                • Don't click unknown links<br>
                • Never share OTP or passwords<br>
                • Don't provide banking details<br>
                • Verify the sender through an official source

                </div>
                """,
                unsafe_allow_html=True
            )


        else:

            risk_score = int(
                max(
                    1,
                    min(
                        35,
                        scam_probability * 100
                    )
                )
            )

            st.markdown(
                f"""
                <div class="result-card safe-result">

                <div class="result-title">
                ✅ Message Appears Safe
                </div>

                <div class="result-desc">
                No major suspicious pattern was detected by the current model.
                </div>

                <br>

                <b>Threat Indicator — {risk_score}%</b>

                <div class="meter">
                    <div class="meter-fill"
                    style="width:{risk_score}%;
                    background:linear-gradient(90deg,#27d99b,#58e6c1);">
                    </div>
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(
                    """
                    <div class="stat-card">
                    <div class="stat-label">Classification</div>
                    <div class="stat-value">SAFE</div>
                    <div class="stat-sub">NLP prediction</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c2:
                st.markdown(
                    """
                    <div class="stat-card">
                    <div class="stat-label">Risk Level</div>
                    <div class="stat-value">LOW</div>
                    <div class="stat-sub">No major signals</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c3:
                st.markdown(
                    """
                    <div class="stat-card">
                    <div class="stat-label">Warning Signals</div>
                    <div class="stat-value">0</div>
                    <div class="stat-sub">Detected in message</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("### 🛡️ Safety Note")

            st.markdown(
                """
                <div class="safe-box">

                The message appears safe based on the trained model.
                However, no automated detector can guarantee that a message
                is completely safe.

                Always verify unexpected requests independently.

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# QUICK EXAMPLES
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("### ⚡ Try a quick example")

e1, e2, e3 = st.columns(3)

with e1:
    st.markdown(
        """
        <div class="feature">
        <div class="feature-icon">🚨</div>
        <div class="feature-title">Bank Alert</div>
        <div class="feature-text">
        Test an urgent account verification message.
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with e2:
    st.markdown(
        """
        <div class="feature">
        <div class="feature-icon">🎁</div>
        <div class="feature-title">Prize Message</div>
        <div class="feature-text">
        Test a suspicious reward or lottery message.
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with e3:
    st.markdown(
        """
        <div class="feature">
        <div class="feature-icon">📦</div>
        <div class="feature-title">Delivery Update</div>
        <div class="feature-text">
        Test a normal package delivery notification.
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# HOW IT WORKS
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

with st.expander("🧠 How SafeText AI works"):

    st.markdown("""
    **01 — Text Input**

    The user provides an SMS, email, WhatsApp message or notification.

    **02 — NLP Processing**

    The text is transformed into numerical features using **TF-IDF**.

    **03 — Machine Learning**

    A trained **Logistic Regression** classifier analyzes the features.

    **04 — Classification**

    The model predicts whether the message is **Safe** or **Scam**.

    **05 — Risk Explanation**

    Additional keyword analysis identifies warning signals such as
    urgency, verification requests, money-related content and links.
    """)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<br><br>

<div style="
text-align:center;
color:#566276;
font-size:12px;
padding:25px;
border-top:1px solid rgba(120,145,180,0.08);
">

🛡️ <b>SafeText AI</b> &nbsp;•&nbsp;
NLP-Powered Message Security

<br><br>

Built with Python • Scikit-learn • TF-IDF • Logistic Regression • Streamlit

</div>
""", unsafe_allow_html=True)