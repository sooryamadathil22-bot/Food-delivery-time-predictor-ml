import streamlit as st
import pandas as pd
from pathlib import Path
import random
import base64

try:
    import joblib
except ImportError:
    joblib = None

# ---------- Page Configuration ----------
st.set_page_config(
    page_title="Food Delivery Time Prediction",
    page_icon="🛵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- Theme State ----------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ---------- Theme Toggle Buttons ----------
# ---------- Custom Theme Toggle ----------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

st.markdown(
    """
    <style>
    .theme-toggle {
        position: relative;
        display: flex;
        align-items: center;
        width: 164px;
        height: 62px;
        padding: 4px;
        border-radius: 40px;
        background: #e9e9e9;
        border: 2px solid #c9c9c9;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.15);
    }

    .theme-toggle.dark {
        background: #303030;
        border-color: #484848;
    }

    .theme-toggle button {
        position: absolute;
        top: 3px;
        width: 56px;
        height: 56px;
        border: none;
        border-radius: 50%;
        background: transparent;
        color: #777;
        font-size: 30px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 2;
    }

    .theme-toggle button.active {
        background: linear-gradient(145deg, #ffca73, #e68b00);
        color: white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    .theme-toggle.dark button.active {
        background: linear-gradient(145deg, #777, #444);
        color: white;
    }

    .theme-toggle .sun {
        left: 3px;
    }

    .theme-toggle .moon {
        right: 3px;
    }

    .theme-toggle.dark button:not(.active) {
        color: #777;
    }
    
    /* Custom theme switch styling */
div[data-testid="stHorizontalBlock"]:has(
    button[key="light_theme"]
) {
    gap: 0 !important;
}

button[key="light_theme"],
button[key="dark_theme"] {
    min-height: 56px !important;
    width: 56px !important;
    border-radius: 50% !important;
    font-size: 1.5rem !important;
}
    </style>
    """,
    unsafe_allow_html=True,
)

_, _, toggle_col = st.columns([5, 2, 0.8])

with toggle_col:
    sun_col, moon_col = st.columns(2, gap="small")

    with sun_col:
        if st.button(
            "☀️",
            key="light_theme",
            help="Switch to Light Mode",
            use_container_width=True,
            type="primary" if not st.session_state.dark_mode else "secondary",
        ):
            st.session_state.dark_mode = False
            st.rerun()

    with moon_col:
        if st.button(
            "🌙",
            key="dark_theme",
            help="Switch to Dark Mode",
            use_container_width=True,
            type="primary" if st.session_state.dark_mode else "secondary",
        ):
            st.session_state.dark_mode = True
            st.rerun()

# ---------- Theme Colors ----------
if st.session_state.dark_mode:
    BG = "#0E1726"
    BG_GRADIENT = "linear-gradient(115deg, #0E1726 0%, #152238 52%, #101B2E 100%)"
    TEXT = "#EAF2FF"
    MUTED = "#A7BAD5"
    BORDER = "#30445F"
    PANEL = "#17263B"
    INPUT_BG = "#1B2B42"
    PRIMARY = "#398BFF"
    PRIMARY_HOVER = "#2674DF"
    RESULT_BG = "linear-gradient(110deg, #172C48, #1B2B42)"
else:
    BG = "#F7FBFF"
    BG_GRADIENT = "linear-gradient(115deg, #f7fbff 0%, #ffffff 52%, #f8fbff 100%)"
    TEXT = "#10294D"
    MUTED = "#526F98"
    BORDER = "#D7E8FC"
    PANEL = "rgba(255,255,255,0.75)"
    INPUT_BG = "rgba(255,255,255,0.9)"
    PRIMARY = "#1971E5"
    PRIMARY_HOVER = "#105FC8"
    # Light theme
    RESULT_BG = "linear-gradient(110deg, #E0EFFF, #F2F8FF)"
# ---------- Dynamic Styling ----------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], [data-testid="stAppViewContainer"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background: {BG_GRADIENT};
        color: {TEXT};
    }}

    [data-testid="stAppViewContainer"] {{
        background: {BG_GRADIENT};
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    #MainMenu, footer {{
        visibility: hidden;
    }}

    .block-container {{
        max-width: 1600px;
        padding: 1.3rem 3.1rem 2.5rem;
    }}

    /* Hero section */
    .hero {{
        display: flex;
        align-items: center;
        gap: 2rem;
        padding: 0.5rem 0 1.1rem;
        border-bottom: 1px solid {BORDER};
        margin-bottom: 1.25rem;
    }}

    .hero-copy {{
        flex: 1.05;
        min-width: 0;
    }}

    .hero-art {{
        flex: 1.35;
        min-width: 0;
        text-align: center;
    }}

    .hero h1 {{
        color: {TEXT};
        font-size: clamp(2.2rem, 3.8vw, 3.8rem);
        line-height: 1.1;
        letter-spacing: -1.8px;
        font-weight: 800;
        margin: 0 0 1rem;
    }}

    .hero p {{
        color: {MUTED};
        font-size: 1.12rem;
        line-height: 1.55;
        margin: 0 0 1.5rem;
    }}

    .hero .meta {{
        color: {MUTED};
        font-size: 0.98rem;
    }}

    .hero img {{
        width: 100%;
        max-height: 315px;
        object-fit: contain;
    }}

    /* Section heading */
    .section-title {{
        color: {TEXT};
        font-size: 1.55rem;
        font-weight: 800;
        margin: 0 0 0.7rem;
    }}

    /* Form cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-color: {BORDER} !important;
        border-radius: 12px !important;
        background: {PANEL};
    }}

    /* Labels and text */
    label,
    .stSelectbox label,
    .stNumberInput label,
    [data-testid="stWidgetLabel"] p {{
        color: {TEXT} !important;
        font-weight: 600 !important;
    }}

    /* Dropdowns */
    div[data-baseweb="select"] > div {{
        border-color: {BORDER} !important;
        border-radius: 8px !important;
        min-height: 42px;
        background: {INPUT_BG} !important;
    }}

    div[data-baseweb="select"] span,
    div[data-baseweb="select"] input {{
        color: {TEXT} !important;
    }}

    /* Number inputs */
    div[data-testid="stNumberInput"] input {{
        border-color: {BORDER} !important;
        border-radius: 8px !important;
        min-height: 42px;
        background: {INPUT_BG} !important;
        color: {TEXT} !important;
    }}

    /* Buttons */
    div.stButton > button {{
        background: {PRIMARY};
        color: #FFFFFF !important;
        border: 0;
        border-radius: 9px;
        min-height: 46px;
        font-size: 0.98rem;
        font-weight: 700;
        width: 100%;
        transition: background 0.2s ease;
    }}

    div.stButton > button:hover {{
        background: {PRIMARY_HOVER};
        color: #FFFFFF !important;
        border: 0;
    }}

    /* Prediction result */
    .result-panel {{
        margin-top: 1.25rem;
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 1.2rem 1.3rem;
        background: {RESULT_BG};
    }}

    .result-number {{
        font-size: 2.4rem;
        font-weight: 800;
        color: {PRIMARY};
        margin: 0;
    }}

    .result-caption {{
        color: {MUTED};
        margin-top: 0.15rem;
    }}

    /* Responsive layout */
    @media (max-width: 850px) {{
        .block-container {{
            padding: 1rem 1rem 2rem;
        }}

        .hero {{
            flex-direction: column;
            align-items: stretch;
            gap: 0.5rem;
        }}

        .hero-art img {{
            max-height: 230px;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Hero Section ----------
hero_file = Path(__file__).with_name("delivery_hero.png")

if hero_file.exists():
    encoded = base64.b64encode(hero_file.read_bytes()).decode()
    hero_image = (
        f'<img src="data:image/png;base64,{encoded}" '
        f'alt="Food delivery rider illustration">'
    )
else:
    hero_image = '<div style="font-size:8rem;text-align:center">🛵</div>'

st.markdown(
    f"""
    <div class="hero">
      <div class="hero-copy">
        <h1>Food Delivery<br>Time Prediction</h1>
        <p>
          Predict the estimated food delivery time using<br>
          a trained XGBoost Machine Learning model.
        </p>
        <div class="meta">
          XGBoost Regression   ·   Predictive Analytics
        </div>
      </div>
      <div class="hero-art">{hero_image}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Delivery Details ----------
st.markdown(
    '<div class="section-title">Enter Delivery Details</div>',
    unsafe_allow_html=True,
)

left, middle, right = st.columns(3, gap="small")

with left:
    with st.container(border=True):
        age = st.number_input(
            "Delivery Person Age",
            min_value=18, max_value=70, value=28, step=1
        )

        rating = st.number_input(
            "Delivery Person Rating",
            min_value=1.0, max_value=5.0,
            value=4.5, step=0.1, format="%.1f"
        )

        distance = st.number_input(
            "Delivery Distance (km)",
            min_value=0.1, max_value=100.0,
            value=5.0, step=0.5, format="%.1f"
        )

        hour = st.selectbox(
            "Order Hour",
            [f"{h:02d}:00" for h in range(24)],
            index=12
        )

with middle:
    with st.container(border=True):
        traffic = st.selectbox(
            "Road Traffic Density",
            ["Low", "Medium", "High", "Jam"],
            index=1
        )

        vehicle_condition = st.selectbox(
            "Vehicle Condition",
            ["0", "1", "2", "3"],
            index=1
        )

        order_type = st.selectbox(
            "Type of Order",
            ["Meal", "Drinks", "Snack", "Buffet"],
            index=0
        )

        vehicle_type = st.selectbox(
            "Type of Vehicle",
            ["motorcycle", "scooter", "electric_scooter", "bicycle"],
            index=0
        )

with right:
    with st.container(border=True):
        deliveries = st.selectbox(
            "Number of Deliveries",
            [1, 2, 3, 4],
            index=0
        )

        festival = st.selectbox(
            "Festival",
            ["No", "Yes"],
            index=0
        )

        city_type = st.selectbox(
            "City Type",
            ["Urban", "Metropolitan", "Semi-Urban"],
            index=0
        )

        weather = st.selectbox(
            "Weather Conditions",
            ["Sunny", "Cloudy", "Windy", "Fog", "Rainy", "Stormy"],
            index=0
        )

predict_clicked = st.button(
    "Predict Delivery Time",
    use_container_width=True
)

# ---------- Personalized Delivery Messages ----------
delivery_messages = {
    "Meal": [
        "🍽️ Your delicious meal is on its way! Expect it in",
        "🥘 Your meal is being prepared for delivery! Arriving in",
        "😋 Your hunger will be satisfied in"
    ],
    "Drinks": [
        "🥤 Your refreshing drinks are on their way! Arriving in",
        "🧋 Your favorite drinks will reach you in",
        "🍹 Get ready to refresh yourself! Your drinks arrive in"
    ],
    "Snack": [
        "🍟 Your tasty snack is on its way! Arriving in",
        "🍿 Snack time is almost here! Your order arrives in",
        "🥪 Your cravings will be satisfied in"
    ],
    "Buffet": [
        "🍱 Your delicious buffet is on its way! Arriving in",
        "🍛 Get ready for a feast! Your buffet arrives in",
        "🥗 Your buffet experience begins in"
    ]
}
# ---------- Prediction ----------
if predict_clicked:
    model_path = Path(__file__).with_name("model.pkl")
    model = None

    if joblib is not None and model_path.exists():
        try:
            model = joblib.load(model_path)
        except Exception as exc:
            st.error(f"Could not load model.pkl: {exc}")

    if model is not None:
        features = pd.DataFrame([{
            "Delivery_person_Age": age,
            "Delivery_person_Ratings": rating,
            "Distance_km": distance,
            "Order_Hour": int(hour.split(":")[0]),
            "Road_traffic_density": traffic,
            "Vehicle_condition": int(vehicle_condition),
            "Type_of_order": order_type,
            "Type_of_vehicle": vehicle_type,
            "multiple_deliveries": deliveries,
            "Festival": festival,
            "City": city_type,
            "Weather_conditions": weather,
        }])

        try:
            prediction = float(model.predict(features)[0])


            import random

            message = random.choice(delivery_messages[order_type])

            st.markdown(
                f"""
                <div class="result-panel">
                    <div class="section-title">🎉 Prediction Result</div>
                    <p class="result-number">
                        {message} {prediction:.1f} minutes!
                    </p>
                    <div class="result-caption">
                        Estimated delivery time based on your selected details.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        except Exception as exc:
            st.error(
                "The model expects a different feature format. "
                "Check the feature names, column order and preprocessing "
                "used during training."
            )
            st.code(str(exc))

    else:
        # Demo estimate only; not a trained ML prediction.
        traffic_add = {
            "Low": 0, "Medium": 5, "High": 10, "Jam": 16
        }[traffic]

        weather_add = {
            "Sunny": 0, "Cloudy": 2, "Windy": 3,
            "Fog": 5, "Rainy": 7, "Stormy": 10
        }[weather]

        vehicle_add = {
            "motorcycle": 0, "scooter": 2,
            "electric_scooter": 2, "bicycle": 7
        }[vehicle_type]

        hour_num = int(hour.split(":")[0])
        rush_add = (
            6 if hour_num in [8, 9, 17, 18, 19, 20] else 0
        )

        estimate = max(
            5,
            8 + distance * 3.2
            + traffic_add
            + weather_add
            + vehicle_add
            + (deliveries - 1) * 4
            + (5 - rating) * 2
            + rush_add
            + (5 if festival == "Yes" else 0)
        )

        message = random.choice(delivery_messages[order_type])

        st.markdown(
            f"""
            <div class="result-panel">
                <div class="section-title"> Prediction Result</div>
                <p class="result-number">
                    {message} {estimate:.1f} minutes!
                </p>
                
            </div>
            """,
            unsafe_allow_html=True
        )