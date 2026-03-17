import streamlit as st
from PIL import Image
from transformers import pipeline

# =============================
# 🎨 PAGE CONFIG
# =============================
st.set_page_config(page_title="AI Calorie App", layout="centered")

# =============================
# 🎨 FULL PRO UI CSS
# =============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap');

html, body, [class*="st-"] {
    font-family: 'Kanit', sans-serif;
}

.main {
    background: #f8fafc;
}

/* NAVBAR */
.navbar {
    position: sticky;
    top: 0;
    background: rgba(255,255,255,0.8);
    backdrop-filter: blur(10px);
    padding: 12px 20px;
    border-bottom: 1px solid #e5e7eb;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 999;
}

.logo {
    font-weight: 700;
    font-size: 18px;
}

.menu span {
    margin-left: 20px;
    color: #64748b;
    cursor: pointer;
}

/* CARD */
.card {
    padding: 22px;
    border-radius: 18px;
    background: #ffffff;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    margin-bottom: 20px;
    transition: all 0.2s ease;
}

.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
}

/* HEADER */
h1 {
    font-size: 36px !important;
    font-weight: 700 !important;
    text-align: center;
    margin-bottom: 25px !important;
    background: linear-gradient(90deg, #4f46e5, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

h3 {
    font-size: 20px;
    font-weight: 600 !important;
}

/* SECTION TITLE */
.section-title h2 {
    margin-bottom: 5px;
}

.section-title p {
    color: #64748b;
    font-size: 14px;
}

/* BUTTON */
.stButton>button {
    border-radius: 10px;
    height: 2.8em;
    background-color: #4f46e5 !important;
    color: white !important;
    font-weight: 500;
    border: none;
    transition: all 0.2s ease;
}

.stButton>button:hover {
    transform: scale(1.02);
    background-color: #4338ca !important;
}

/* RESET BUTTON */
div[data-testid="stVerticalBlock"] > div:nth-child(2) .stButton>button {
    background-color: #ef4444 !important;
}

/* UPLOAD */
.stFileUploader {
    border: 2px dashed #cbd5f5;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    background-color: #f8fafc;
}

.stFileUploader:hover {
    border-color: #6366f1;
}

/* METRIC */
[data-testid="stMetric"] {
    background: #ffffff;
    padding: 12px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
}

/* BADGE */
.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    background: #eef2ff;
    color: #4338ca;
    font-size: 12px;
    margin-top: 10px;
}

/* RESULT */
.big-font {
    font-size: 26px !important;
    font-weight: 600;
    text-align: center;
    padding: 10px;
    background: #eef2ff;
    color: #3730a3;
    border-radius: 12px;
}

/* ANIMATION */
.fade-in {
    animation: fadeIn 0.6s ease-in-out;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* SPACING */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* DARK MODE */
@media (prefers-color-scheme: dark) {
    .main {
        background: #0f172a;
        color: #f1f5f9;
    }

    .card {
        background: #1e293b;
        border: 1px solid #334155;
    }
}
</style>
""", unsafe_allow_html=True)

# =============================
# 🧭 NAVBAR
# =============================
st.markdown("""
<div class="navbar">
    <div class="logo">🍱 AI Calorie</div>
    <div class="menu">
        <span>Dashboard</span>
        <span>Health</span>
        <span>AI Scan</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<h1>AI Calorie App</h1>", unsafe_allow_html=True)

# =============================
# 🧠 SESSION
# =============================
if "total_cal" not in st.session_state:
    st.session_state.total_cal = 0

# =============================
# 📊 FOOD DATA
# =============================
food_data = {
    "pizza": 285, "hamburger": 295, "banana": 105, "apple": 95,
    "cake": 350, "fried_rice": 400, "pad_thai": 450,
    "cola": 140, "unknown": 0
}

# =============================
# 🤖 MODEL
# =============================
@st.cache_resource
def load_model():
    return pipeline("image-classification", model="nateraw/food")

classifier = load_model()

def detect_food(image):
    try:
        result = classifier(image)
        label = result[0]['label'].lower()
        return label
    except:
        return "unknown"

def map_food(label):
    if "cake" in label:
        return "cake"
    elif "pizza" in label:
        return "pizza"
    elif "burger" in label:
        return "hamburger"
    elif "banana" in label:
        return "banana"
    elif "apple" in label:
        return "apple"
    elif "rice" in label:
        return "fried_rice"
    elif "pad thai" in label or "noodle" in label:
        return "pad_thai"
    elif "cola" in label or "coke" in label or "soda" in label:
        return "cola"
    else:
        return "unknown"

# =============================
# 📸 FOOD SCANNER
# =============================
st.markdown('<div class="card fade-in">', unsafe_allow_html=True)

st.markdown("""
<div class="section-title">
    <h2>📸 Food Scanner</h2>
    <p>Upload your meal and let AI estimate calories instantly</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)

    with st.spinner("🤖 AI กำลังวิเคราะห์อาหาร..."):
        label = detect_food(image)

    food = map_food(label)
    cal = food_data.get(food, 0)

    col1, col2 = st.columns(2)
    col1.metric("🍽️ Food", food)
    col2.metric("🔥 Calories", f"{cal} kcal")

    st.markdown(f"<span class='badge'>{food}</span>", unsafe_allow_html=True)

    if st.button("➕ Add to Total"):
        st.session_state.total_cal += cal

st.markdown('</div>', unsafe_allow_html=True)

# =============================
# 📊 TOTAL + PROGRESS
# =============================
st.markdown('<div class="card fade-in">', unsafe_allow_html=True)

st.metric("📊 Total Today", f"{st.session_state.total_cal} kcal")

st.markdown('</div>', unsafe_allow_html=True)

# =============================
# 🧠 HEALTH
# =============================
st.markdown('<div class="card fade-in">', unsafe_allow_html=True)

st.subheader("🧠 Health Calculator")

col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", min_value=1, max_value=100, step=1)

with col2:
    weight = int(st.number_input("Weight (kg)", min_value=30, step=1, value=60))
    height = int(st.number_input("Height (cm)", min_value=100, step=1, value=170))

activity_map = {
    "🪑 นั่งเฉยๆ": 1.2,
    "🚶 เล็กน้อย": 1.375,
    "🏃 ปานกลาง": 1.55
}

activity = st.selectbox("Activity", list(activity_map.keys()))

# =============================
# 🧠 CALCULATE
# =============================
if gender == "Male":
    bmr = 10*weight + 6.25*height - 5*age + 5
else:
    bmr = 10*weight + 6.25*height - 5*age - 161

tdee = bmr * activity_map[activity]
bmi = weight / ((height/100) ** 2)

col1, col2, col3 = st.columns(3)

col1.metric("🧠 BMR", f"{bmr:.0f}")
col2.metric("🔥 TDEE", f"{tdee:.0f}")
col3.metric("📊 BMI", f"{bmi:.1f}")

# 🔥 PROGRESS BAR
progress = min(st.session_state.total_cal / tdee, 1.0)
st.progress(progress)

# BMI STATUS
if bmi < 18.5:
    status = "⚠️ ผอม"
elif bmi < 25:
    status = "✅ ปกติ"
elif bmi < 30:
    status = "⚠️ อ้วน"
else:
    status = "❗ อ้วนมาก"

st.markdown(f"<p class='big-font'>{status}</p>", unsafe_allow_html=True)

# ANALYSIS
eat = st.session_state.total_cal

if bmi < 18.5:
    if eat < tdee:
        st.warning("⚠️ ควรกินเพิ่ม")
    else:
        st.success("✅ เหมาะกับการเพิ่มน้ำหนัก")

elif bmi < 25:
    if eat > tdee + 200:
        st.error("❗ กินเกิน")
    elif eat < tdee - 200:
        st.warning("⚠️ กินน้อยไป")
    else:
        st.success("✅ สมดุลดี")

else:
    if eat > tdee:
        st.error("❗ ควรลดอาหาร")
    else:
        st.success("✅ ดีแล้ว")

# RESET
if st.button("🔄 Reset"):
    st.session_state.total_cal = 0

st.markdown('</div>', unsafe_allow_html=True)