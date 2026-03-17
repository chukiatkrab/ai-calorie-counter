import streamlit as st
from PIL import Image

# ✅ NEW: AI MODEL
from transformers import pipeline

# =============================
# 🎨 PAGE CONFIG
# =============================
st.set_page_config(page_title="AI Calorie App", layout="centered")

# =============================
# 🎨 CUSTOM CSS
# =============================
st.markdown("""
<style>
.main {
    background: linear-gradient(to bottom, #f8fafc, #eef2ff);
}
.card {
    padding: 20px;
    border-radius: 20px;
    background: white;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}
.big-font {
    font-size: 22px;
    font-weight: bold;
}
.center {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='center'>🍱 AI Calorie App</h1>", unsafe_allow_html=True)

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
# 🤖 LOAD MODEL (สำคัญมาก)
# =============================
@st.cache_resource
def load_model():
    return pipeline("image-classification", model="nateraw/food")

classifier = load_model()

# =============================
# 🤖 DETECT FOOD (AI จริง)
# =============================
def detect_food(image):
    try:
        result = classifier(image)
        label = result[0]['label'].lower()
        return label
    except:
        return "unknown"

# =============================
# 🧠 MAP LABEL → FOOD
# =============================
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
# 📸 UPLOAD CARD
# =============================
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("📸 Upload Food")

uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)

    label = detect_food(image)
    food = map_food(label)
    cal = food_data.get(food, 0)

    col1, col2 = st.columns(2)
    col1.metric("🍽️ Food", food)
    col2.metric("🔥 Calories", f"{cal} kcal")

    if st.button("➕ Add to Total"):
        st.session_state.total_cal += cal

st.markdown('</div>', unsafe_allow_html=True)

# =============================
# 📊 TOTAL CARD
# =============================
st.markdown('<div class="card center">', unsafe_allow_html=True)

st.metric("📊 Total Today", f"{st.session_state.total_cal} kcal")

if st.button("🔄 Reset"):
    st.session_state.total_cal = 0

st.markdown('</div>', unsafe_allow_html=True)

# =============================
# 🧠 HEALTH CARD
# =============================
st.markdown('<div class="card">', unsafe_allow_html=True)

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

# =============================
# 📈 RESULT
# =============================
col1, col2, col3 = st.columns(3)

col1.metric("🧠 BMR", f"{bmr:.0f}")
col2.metric("🔥 TDEE", f"{tdee:.0f}")
col3.metric("📊 BMI", f"{bmi:.1f}")

if bmi < 18.5:
    status = "⚠️ ผอม"
elif bmi < 25:
    status = "✅ ปกติ"
elif bmi < 30:
    status = "⚠️ อ้วน"
else:
    status = "❗ อ้วนมาก"

st.markdown(f"<p class='big-font'>{status}</p>", unsafe_allow_html=True)

# =============================
# ⚖️ ANALYSIS
# =============================
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

st.markdown('</div>', unsafe_allow_html=True)