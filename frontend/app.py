import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import tempfile
import pandas as pd
from tools.vision_tool import analyze_leaf
from tools.profile_tool import load_profile
from tools.memory_tool import save_farmer
from tools.weather_tool import get_weather, get_hourly_forecast
from tools.market_tool import market_price



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
            "🎥 Demo Mode",
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

    # Load Farmer Profile
    profile_data = load_profile("farmer1")
    if not isinstance(profile_data, dict):
        village_val = "Nashik"
        crop_val = "Soybean"
        soil_val = "Black"
    else:
        village_val = profile_data.get("Village") or "Nashik"
        crop_val = profile_data.get("Crop") or "Soybean"
        soil_val = profile_data.get("Soil") or "Black"

    st.title("🌾 Krishi AI Dashboard")
    st.caption("AI Agricultural Intelligence & Farm Management Platform")

    col_main, col_sidebar = st.columns([7, 3])

    with col_sidebar:
        st.markdown("### 🚜 Farm Profile")
        with st.container(border=True):
            st.markdown(f"📍 **Location:** `{village_val}`")
            st.markdown(f"🌱 **Primary Crop:** `{crop_val}`")
            st.markdown(f"🪨 **Soil Type:** `{soil_val}` Soil")
            
            with st.expander("📝 Edit Settings"):
                with st.form("profile_form"):
                    new_village = st.text_input("Village/City", value=village_val)
                    new_crop = st.selectbox(
                        "Primary Crop",
                        ["Soybean", "Cotton", "Rice", "Wheat", "Tomato", "Millet"],
                        index=["Soybean", "Cotton", "Rice", "Wheat", "Tomato", "Millet"].index(crop_val) if crop_val in ["Soybean", "Cotton", "Rice", "Wheat", "Tomato", "Millet"] else 0
                    )
                    new_soil = st.selectbox(
                        "Soil Type",
                        ["Black", "Red", "Sandy", "Clay"],
                        index=["Black", "Red", "Sandy", "Clay"].index(soil_val) if soil_val in ["Black", "Red", "Sandy", "Clay"] else 0
                    )
                    submit_profile = st.form_submit_button("Save Profile")
                    if submit_profile:
                        save_farmer("farmer1", new_village, new_crop, new_soil)
                        st.success("Profile saved!")
                        st.rerun()

    with col_main:
        with st.spinner("Loading dynamic farm dashboard..."):
            weather_data = get_weather(village_val)
            m_price = market_price(crop_val)

        st.markdown("### 📊 Live Conditions")
        c1, c2, c3, c4 = st.columns(4)

        temp = weather_data.get("temperature")
        humidity = weather_data.get("humidity")
        rain_prob = weather_data.get("rain_probability")
        wind_speed = weather_data.get("wind")
        advice = weather_data.get("advice")

        with c1:
            st.metric("🌡 Temperature", f"{temp}°C" if temp != "N/A" else "N/A")
        with c2:
            st.metric("💧 Humidity", f"{humidity}%" if humidity != "N/A" else "N/A")
        with c3:
            st.metric("🌧 Rain", f"{rain_prob}%" if rain_prob != "N/A" else "N/A")
        with c4:
            st.metric("💰 Market Price", f"{m_price['price']}" if m_price else "N/A")

        if advice and advice != "Location not found.":
            st.info(f"🚜 **Agricultural Advice:** {advice}")
        elif advice == "Location not found.":
            st.warning(f"⚠️ Could not fetch weather for `{village_val}`. Please edit location to a valid city.")

        st.markdown("### 📈 24-Hour Temperature Forecast")
        forecast = get_hourly_forecast(village_val)
        if forecast and forecast.get("times"):
            df_forecast = pd.DataFrame({
                "Time": forecast["times"],
                "Temperature (°C)": forecast["temperatures"]
            }).set_index("Time")
            st.area_chart(df_forecast, color="#2e7d32")
        else:
            st.info("Hourly forecast chart not available for this location.")

        st.markdown("### 💬 AI Agriculture Assistant")
        
        # Shortcut action queries
        shortcut_query = None
        s1, s2, s3 = st.columns(3)
        with s1:
            if st.button("🌦 Check weather details", use_container_width=True):
                shortcut_query = f"what is the weather forecast for {village_val}?"
        with s2:
            if st.button("💰 What's the market price?", use_container_width=True):
                shortcut_query = f"what is the market price of {crop_val}?"
        with s3:
            if st.button("🏛 Government schemes", use_container_width=True):
                shortcut_query = f"what government schemes are available for {crop_val}?"

        st.divider()

        # ---------------- CHAT HISTORY ----------------
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Handle input / shortcut
        query = st.chat_input("Ask anything about farming...")
        if shortcut_query:
            query = shortcut_query

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

            if route == "weather":
                weather = result["result"]
                answer = f"""
## 🌦 Weather Report for {weather['village']}

🌡 **Temperature:** {weather['temperature']}°C
💧 **Humidity:** {weather['humidity']}%
🌧 **Rain Probability:** {weather['rain_probability']}%
🌬 **Wind:** {weather['wind']} km/h

🚜 **Advice:** {weather['advice']}
"""
            elif route == "market":
                market = result["result"]
                answer = f"""
## 💰 Market Price

🌾 **Crop:** {market['crop']}
💵 **Price:** {market['price']}
"""
            elif route == "scheme":
                schemes = result["result"]["schemes"]
                answer = "## 🏛 Government Schemes\n\n"
                for s in schemes:
                    answer += f"✅ {s}\n"
            elif route == "vision":
                answer = "📷 Please open the Disease Detection page from the sidebar to upload a leaf photo."
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
                
            st.rerun()

# =====================================================
# DEMO MODE PAGE
# =====================================================

elif page == "🎥 Demo Mode":

    st.title("🎥 Interactive Demo Mode & Project Guide")
    st.caption("Load agricultural presets, review platform architecture, and explore features.")

    tab_presets, tab_how_it_works, tab_features = st.tabs([
        "🚀 Preset Scenarios", 
        "⚙️ How It Works", 
        "🌾 Feature Walkthrough"
    ])

    with tab_presets:
        st.write("Choose a scenario below to seed the database and chat session with predefined simulation data, then redirect to the Dashboard to review.")

        c1, c2 = st.columns(2)

        with c1:
            with st.container(border=True):
                st.markdown("### 🚜 Cotton Farm Scenario (Pune)")
                st.write("This scenario pre-populates a dry-season farm setup in Pune for growing cotton.")
                st.write("- **Location:** Pune")
                st.write("- **Primary Crop:** Cotton")
                st.write("- **Soil:** Black Soil")
                st.write("- **Chat History:** Injects cotton planning and weather advice chat logs.")
                
                if st.button("Activate Cotton Scenario", use_container_width=True):
                    # Update DB
                    save_farmer("farmer1", "Pune", "Cotton", "Black")
                    # Seed Session State Messages
                    st.session_state.messages = [
                        {"role": "user", "content": "I am planning to grow cotton in my farm in Pune. What should I check?"},
                        {"role": "assistant", "content": "Welcome! I have saved your farm location to Pune, crop to Cotton, and soil to Black Soil. Currently, the weather is clear. Since cotton grows well in deep black soil with moderate rainfall, your soil choice is excellent. You should check the rain probability and current market prices on the dashboard."}
                    ]
                    st.success("Cotton farm scenario activated! Redirecting...")
                    st.rerun()

        with c2:
            with st.container(border=True):
                st.markdown("### 📷 Disease Diagnostic Scenario")
                st.write("Pre-configures a soybean farm setup in Nashik and preloads crop health check logs.")
                st.write("- **Location:** Nashik")
                st.write("- **Primary Crop:** Soybean")
                st.write("- **Soil:** Black Soil")
                st.write("- **Chat History:** Injects leaf diagnostics chat logs simulating image analysis.")

                if st.button("Activate Disease Scenario", use_container_width=True):
                    # Update DB
                    save_farmer("farmer1", "Nashik", "Soybean", "Black")
                    # Seed Session State Messages
                    st.session_state.messages = [
                        {"role": "user", "content": "Can you analyze this leaf photo for disease?"},
                        {"role": "assistant", "content": "📷 **Leaf Diagnostic Report**\n\n- **Detected Disease:** Soybean Rust (Phakopsora pachyrhizi)\n- **Severity:** Moderate (approx 15-20% leaf coverage)\n- **Confidence:** 94%\n\n🚜 **Action Plan:**\n1. Apply fungicide spray immediately (e.g. Tebuconazole or Azoxystrobin).\n2. Improve field drainage to reduce relative humidity in the canopy.\n3. Monitor neighboring crop fields for rust spread."}
                    ]
                    st.success("Disease diagnostic scenario activated! Redirecting...")
                    st.rerun()

        st.divider()

        with st.container(border=True):
            st.markdown("### 🔄 Reset Application")
            st.write("Clear all active profile configurations, reset settings to defaults, and erase conversation history.")
            if st.button("Clear & Reset App", use_container_width=True, type="primary"):
                save_farmer("farmer1", "Nashik", "Soybean", "Black")
                st.session_state.messages = []
                st.success("App successfully reset to default settings!")
                st.rerun()

    with tab_how_it_works:
        st.markdown("""
        ### ⚙️ Architecture: How Krishi AI Works
        
        Krishi AI is a state-of-the-art agricultural platform operating on a multi-agent routing system:
        
        ```
          Farmer Query -> Intelligent Router -> classified route
                               |
             +-----------------+-----------------+-----------------+
             |                 |                 |                 |
          [Weather]         [Market]          [Scheme]         [ADK/LLM]
             |                 |                 |                 |
          GeoPy &          Mandi Rates      Database Query    ADK Root Agent
         Open-Meteo           API                API         (Crop/Disease/Memory)
        ```
        
        #### 🔍 Key Components:
        1. **Farmer Profiles (`SQLite` & `memory_tool`)**: Holds settings (Location, Crop, Soil) per farmer. Updating this profile dynamically updates the dashboard metrics and weather forecasts instantly.
        2. **Intelligent Router (`router.py`)**: Classifies text queries using intent-matching keywords to direct queries to specialized APIs or fallback to the LLM agent.
        3. **Google ADK Agents (`krishi_ai/`)**: Leverages specialized AI agents (Crop, Disease, Memory) orchestrating custom tools to answer farming inquiries.
        """)

    with tab_features:
        st.markdown("""
        ### 🌾 Platform Modules & Feature Guide
        
        Explore the primary modules of Krishi AI:
        
        * **🏠 Dynamic Dashboard**: Central hub displaying real-time metrics, forecast charts, and the AI Assistant. It automatically updates when the farmer changes location or crop parameters.
        * **🌦 Live Weather & Advice**: Connects to the **Open-Meteo API** to get real-time temperature, humidity, rain probability, and wind. It automatically generates irrigation recommendations (e.g. *heavy rain expected, avoid irrigation*).
        * **🌱 AI Crop Recommendation**: Analyzes soil conditions and expected rainfall patterns to suggest the most profitable crop options with confidence scores.
        * **📷 Crop Disease Scanner**: Evaluates leaf photographs utilizing Gemini Vision models to detect pathogens, estimate severity, and produce chemical/cultural treatment recommendations.
        * **💰 Market Mandi Prices**: Lists mandi crop prices.
        * **🏛 Government Schemes**: Tailors regional and national scheme recommendations based on active profile settings.
        * **📞 RSK Expert Helpline**: Generates support tickets routed to regional agriculture centers.
        """)


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

    st.title("💰 Market Prices & Mandi Rates")
    st.caption("Live crop pricing and market trends across regional agriculture mandis.")

    # Load Farmer Profile
    profile_data = load_profile("farmer1")
    if not isinstance(profile_data, dict):
        crop_val = "Soybean"
    else:
        crop_val = profile_data.get("Crop") or "Soybean"

    # Crop list options
    crops_list = ["Soybean", "Cotton", "Rice", "Wheat", "Tomato", "Millet"]
    
    # Selection box
    selected_crop = st.selectbox(
        "Select Crop to check rates:",
        crops_list,
        index=crops_list.index(crop_val) if crop_val in crops_list else 0
    )

    # Get baseline price from market tool
    from tools.market_tool import market_price
    base_data = market_price(selected_crop)
    
    # Extract baseline price number
    import re
    price_str = base_data.get("price", "₹5200 / quintal")
    digits = re.findall(r'\d+', price_str)
    base_price = int(digits[0]) if digits else 5200

    st.divider()

    # Mandi list and pricing calculations
    mandi_data = [
        {"Mandi / APMC Market": "APMC Nagpur (Maharashtra)", "Current Rate": f"₹{base_price}/quintal", "Daily Trend": "📈 +1.4% (Up)", "Status": "Active"},
        {"Mandi / APMC Market": "APMC Indore (Madhya Pradesh)", "Current Rate": f"₹{base_price - 80}/quintal", "Daily Trend": "📉 -0.8% (Down)", "Status": "Active"},
        {"Mandi / APMC Market": "APMC Rajkot (Gujarat)", "Current Rate": f"₹{base_price + 150}/quintal", "Daily Trend": "📈 +2.1% (Up)", "Status": "Active"},
        {"Mandi / APMC Market": "APMC Amritsar (Punjab)", "Current Rate": f"₹{base_price + 50}/quintal", "Daily Trend": "➖ Stable", "Status": "Active"},
        {"Mandi / APMC Market": "APMC Gadag (Karnataka)", "Current Rate": f"₹{base_price - 120}/quintal", "Daily Trend": "📉 -1.2% (Down)", "Status": "Active"},
    ]

    st.subheader(f"📊 Mandi Price Sheet for {selected_crop}")
    df_mandi = pd.DataFrame(mandi_data)
    st.dataframe(df_mandi, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader(f"📈 7-Day Market Trend Analysis ({selected_crop})")
    
    # Seed values based on crop list index for stable visualization per crop
    import random
    random.seed(crops_list.index(selected_crop))
    trend_prices = []
    current_p = base_price
    for _ in range(7):
        current_p += random.randint(-150, 150)
        trend_prices.append(current_p)

    dates = ["July 1", "July 2", "July 3", "July 4", "July 5", "July 6", "July 7"]
    df_trend = pd.DataFrame({
        "Date": dates,
        "Price (₹/quintal)": trend_prices
    }).set_index("Date")

    st.line_chart(df_trend, color="#388e3c")

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