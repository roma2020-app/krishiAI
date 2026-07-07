import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import tempfile
from tools.vision_tool import analyze_leaf

from krishi_ai.router import IntelligentRouter
from krishi_ai.call_adk import ask_adk


router = IntelligentRouter()

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="🌾 Krishi AI",
    page_icon="🌾",
    layout="wide"
)

# ----------------------------------------------------
# SESSION
# ----------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

with st.sidebar:

    st.title("🌾 Krishi AI")
    st.caption("AI Agriculture Platform")

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🌦 Weather",
            "🌱 Crop Recommendation",
            "📷 Disease Detection",
            "💰 Market Prices",
            "🏛 Government Schemes",
            "📞 Expert Support",
        ],
    )

    st.markdown("---")
    st.success("🟢 System Online")

# =====================================================
# DASHBOARD
# =====================================================

if page == "🏠 Dashboard":

    st.title("🌾 Krishi AI")
    st.caption("AI Agricultural Intelligence Platform")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("🌡 Temperature", "31°C")

    with c2:
        st.metric("🌧 Rain", "82%")

    with c3:
        st.metric("🌱 Best Crop", "Soybean")

    with c4:
        st.metric("💰 Market", "₹5200/q")

    st.divider()

    # ---------------- CHAT HISTORY ----------------

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ---------------- CHAT INPUT ----------------

    query = st.chat_input("Ask anything about farming...")

    if query:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": query
            }
        )

        with st.chat_message("user"):
            st.markdown(query)

        result = router.route(query)

        route = result["route"]

        # WEATHER
        if route == "weather":

            weather = result["result"]

            answer = f"""
## 🌦 Weather Report

📍 **Location:** {weather['village']}

🌡 **Temperature:** {weather['temperature']}°C

💧 **Humidity:** {weather['humidity']}%

🌧 **Rain Probability:** {weather['rain_probability']}%

🌬 **Wind:** {weather['wind']} km/h

🚜 **Advice**

{weather['advice']}
"""

        # MARKET
        elif route == "market":

            market = result["result"]

            answer = f"""
## 💰 Market Price

🌾 Crop : {market['crop']}

💵 Price : {market['price']}
"""

        # SCHEMES
        elif route == "scheme":

            schemes = result["result"]["schemes"]

            answer = "## 🏛 Government Schemes\n\n"

            for s in schemes:
                answer += f"✅ {s}\n"

        # IMAGE
        elif route == "vision":

            answer = "📷 Please open the Disease Detection page from the sidebar."

        # LLM
        else:

            with st.spinner("🤖 Thinking..."):
                answer = ask_adk(query)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

# =====================================================
# WEATHER PAGE
# =====================================================

elif page == "🌦 Weather":

    st.title("🌦 Live Weather")

    city = st.text_input("Enter City", "Nashik")

    if st.button("Get Weather"):

        weather = router.route(f"weather in {city}")["result"]

        st.metric("🌡 Temperature", f"{weather['temperature']}°C")
        st.metric("💧 Humidity", f"{weather['humidity']}%")
        st.metric("🌧 Rain", f"{weather['rain_probability']}%")
        st.metric("🌬 Wind", f"{weather['wind']} km/h")

        st.success(weather["advice"])

# =====================================================
# CROP RECOMMENDATION
# =====================================================

elif page == "🌱 Crop Recommendation":

    from tools.crop_tool import recommend_crop

    st.title("🌱 AI Crop Recommendation")

    st.write("Enter your farm details.")

    col1, col2 = st.columns(2)

    with col1:

        village = st.text_input(
            "Village",
            placeholder="Enter village"
        )

        soil = st.selectbox(
            "Soil Type",
            [
                "Black",
                "Red",
                "Alluvial",
                "Laterite",
                "Clay",
                "Sandy"
            ]
        )

    with col2:

        rainfall = st.slider(
            "Expected Rainfall (mm)",
            0,
            500,
            120
        )

    if st.button("🌱 Recommend Crop", use_container_width=True):

        with st.spinner("Analyzing farm conditions..."):

            result = recommend_crop(
                village=village,
                soil=soil,
                rainfall=rainfall
            )

        if result["status"] != "Success":

            st.error(result.get("message", "No recommendation found."))

        else:

            st.success("Recommendation Generated")

            # ---------------- Weather ----------------

            weather = result["weather"]

            st.subheader("🌦 Current Weather")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "Temperature",
                f"{weather['temperature']}°C"
            )

            c2.metric(
                "Humidity",
                f"{weather['humidity']}%"
            )

            c3.metric(
                "Rain",
                f"{weather['rain_probability']}%"
            )

            c4.metric(
                "Wind",
                f"{weather['wind']} km/h"
            )

            st.divider()

            # ---------------- Crop Recommendations ----------------

            st.subheader("🌱 Recommended Crops")

            for crop in result["recommendations"]:

                with st.container(border=True):

                    st.markdown(f"## 🌾 {crop['crop']}")

                    st.progress(crop["confidence"] / 100)

                    st.write(
                        f"**Confidence:** {crop['confidence']}%"
                    )

                    st.write(
                        f"**Expected Rainfall:** {crop['expected_rainfall']} mm"
                    )

                    st.write(
                        f"**Groundwater Level:** {crop['groundwater']} ft"
                    )
# =====================================================
# DISEASE PAGE
# =====================================================

elif page == "📷 Disease Detection":

    st.title("📷 Crop Disease Detection")

    st.write("Upload a clear photo of the affected crop leaf.")

    uploaded = st.file_uploader(
        "Choose Leaf Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded:

        st.image(
            uploaded,
            caption="Uploaded Leaf",
            use_container_width=True
        )

        if st.button("🔍 Analyze Leaf"):

            with st.spinner("🧠 Gemini is analyzing the leaf..."):

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".jpg"
                ) as tmp:

                    tmp.write(uploaded.getbuffer())

                    image_path = tmp.name

                result = analyze_leaf(image_path)

            st.success("✅ Analysis Complete")

            st.markdown(result)

            st.divider()

            if st.button("📞 Send to Rythu Seva Kendra"):

                st.success(
                    "Ticket successfully created and forwarded to the nearest RSK."
                )
# =====================================================
# MARKET PAGE
# =====================================================

elif page == "💰 Market Prices":

    st.title("💰 Market Prices")

    st.info("Coming in next step.")

# =====================================================
# SCHEMES PAGE
# =====================================================

elif page == "🏛 Government Schemes":

    st.title("🏛 Government Schemes")

    st.info("Coming in next step.")

# =====================================================
# EXPERT PAGE
# =====================================================

elif page == "📞 Expert Support":

    st.title("📞 Expert Support")

    name = st.text_input("Farmer Name")

    problem = st.text_area("Describe your issue")

    if st.button("Submit"):

        st.success("Your request has been submitted to the expert.")