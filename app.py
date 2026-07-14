import streamlit as st
from agent import init_agent, chat
from database import init_db, get_pantry, get_history, clear_history

st.set_page_config(
    page_title="FridgeToFork",
    page_icon="🍳",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background: #fff8f4; }
    
    .banner {
        background: #e8533a;
        padding: 18px 24px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 16px;
    }
    .banner-left { display: flex; align-items: center; gap: 14px; }
    .logo-circle {
        width: 44px; height: 44px;
        border-radius: 12px;
        background: rgba(255,255,255,0.2);
        display: flex; align-items: center;
        justify-content: center;
        font-size: 22px;
    }
    .banner-title { font-size: 20px; font-weight: 500; color: white; margin: 0; }
    .banner-sub { font-size: 12px; color: rgba(255,255,255,0.8); margin: 2px 0 0 0; }
    .banner-stats { display: flex; gap: 20px; }
    .stat { text-align: center; }
    .stat-num { font-size: 20px; font-weight: 500; color: white; }
    .stat-label { font-size: 10px; color: rgba(255,255,255,0.7); }

    .recipe-card {
        background: white;
        border-radius: 10px;
        padding: 10px 14px;
        margin: 6px 0;
        border: 0.5px solid #f0ddd5;
        border-left: 3px solid #e8533a;
    }
    .rcard-title { font-size: 14px; font-weight: 500; color: #3d2a25; margin-bottom: 4px; }
    .rcard-meta { font-size: 11px; color: #a08070; margin-bottom: 6px; }
    .badge-have { font-size: 10px; padding: 2px 8px; border-radius: 10px; background: #eaf3de; color: #3b6d11; font-weight: 500; margin-right: 4px; }
    .badge-miss { font-size: 10px; padding: 2px 8px; border-radius: 10px; background: #fcebeb; color: #a32d2d; font-weight: 500; margin-right: 4px; }
    .badge-time { font-size: 10px; padding: 2px 8px; border-radius: 10px; background: #faeeda; color: #633806; font-weight: 500; margin-right: 4px; }

    .pantry-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        background: #fde8e3;
        color: #c0402a;
        font-weight: 500;
        margin: 3px;
    }
    .hist-item {
        font-size: 12px;
        color: #a08070;
        padding: 5px 0;
        border-bottom: 0.5px solid #f5ede8;
    }
    .cuisine-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 5px;
        margin-bottom: 4px;
    }
    .cpill {
        padding: 6px 8px;
        border-radius: 8px;
        font-size: 11px;
        border: 0.5px solid #f0ddd5;
        background: #fff8f4;
        color: #8b4c3c;
        text-align: center;
    }

    .stButton > button {
        background: #fff8f4 !important;
        border: 0.5px solid #f0ddd5 !important;
        color: #3d2a25 !important;
        border-radius: 8px !important;
        font-size: 12px !important;
        width: 100% !important;
        text-align: left !important;
        padding: 8px 10px !important;
    }
    .stButton > button:hover {
        background: #fde8e3 !important;
        border-color: #e8533a !important;
        color: #c0402a !important;
    }

    [data-testid="stSidebar"] {
        background: white !important;
        border-right: 0.5px solid #f0ddd5 !important;
    }
    .sb-title {
        font-size: 10px;
        font-weight: 500;
        color: #c0a090;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 10px;
    }

    .stTabs [data-baseweb="tab-list"] { background: white; border-bottom: 0.5px solid #f0ddd5; gap: 0; }
    .stTabs [data-baseweb="tab"] { font-size: 13px !important; color: #a08070 !important; border-radius: 0 !important; }
    .stTabs [aria-selected="true"] { color: #e8533a !important; border-bottom: 2px solid #e8533a !important; background: white !important; }

    .stChatMessage { background: white !important; border: 0.5px solid #f0ddd5 !important; border-radius: 12px !important; }
    div[data-testid="stChatInput"] textarea { background: #fff8f4 !important; border-radius: 20px !important; border: 1px solid #f0ddd5 !important; }

    hr { border-color: #f0ddd5 !important; }
</style>
""", unsafe_allow_html=True)

# Initialize
init_db()

if "model" not in st.session_state:
    st.session_state.model = init_agent()
if "history" not in st.session_state:
    st.session_state.history = []
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Hi! Tell me what's in your fridge and I'll suggest delicious recipes!\n\nYou can:\n- 🧺 Add ingredients to your pantry\n- 🍽️ Get recipe suggestions\n- 🛒 Generate a shopping list\n- ⚙️ Set dietary preferences\n- 🌍 Ask for specific cuisines\n- 📅 Plan your weekly meals"
        }
    ]
if "quick_action" not in st.session_state:
    st.session_state.quick_action = None

# ── Banner ──────────────────────────────────
pantry = get_pantry()
history_items = get_history()

st.markdown(f"""
<div class="banner">
    <div class="banner-left">
        <div class="logo-circle">🍳</div>
        <div>
            <p class="banner-title">FridgeToFork</p>
            <p class="banner-sub">Recipe Suggester Agent</p>
        </div>
    </div>
    <div class="banner-stats">
        <div class="stat">
            <div class="stat-num">{len(pantry)}</div>
            <div class="stat-label">In pantry</div>
        </div>
        <div class="stat">
            <div class="stat-num">{len(history_items)}</div>
            <div class="stat-label">History</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sb-title">🌍 Cuisine</div>', unsafe_allow_html=True)
    cuisine_html = '<div class="cuisine-grid">'
    cuisines = ["Any", "Indian", "Italian", "Mexican", "Chinese", "Mediterranean"]
    for c in cuisines:
        cuisine_html += f'<div class="cpill">{c}</div>'
    cuisine_html += '</div>'
    st.markdown(cuisine_html, unsafe_allow_html=True)

    selected_cuisine = st.selectbox("", cuisines, label_visibility="collapsed")
    if selected_cuisine != "Any":
        if st.button(f"🍽️ Find {selected_cuisine} recipes"):
            st.session_state.quick_action = f"Suggest {selected_cuisine} recipes based on what I have in my pantry"

    st.divider()

    st.markdown('<div class="sb-title">🧺 Your pantry</div>', unsafe_allow_html=True)
    if pantry:
        pantry_html = ""
        for item in pantry:
            pantry_html += f'<span class="pantry-pill">{item[0]}</span>'
        st.markdown(pantry_html, unsafe_allow_html=True)
    else:
        st.caption("Your pantry is empty!")

    st.divider()

    st.markdown('<div class="sb-title">⚡ Quick actions</div>', unsafe_allow_html=True)
    if st.button("🍽️ Suggest recipes"):
        st.session_state.quick_action = "Suggest recipes based on what I have"
    if st.button("🛒 Shopping list"):
        st.session_state.quick_action = "Generate a shopping list for a recipe I can almost make"
    if st.button("📅 Plan my week"):
        st.session_state.quick_action = "Plan my meals for the entire week based on what I have"
    if st.button("🧹 Clear pantry"):
        st.session_state.quick_action = "Clear my pantry"
    if st.button("🔄 Refresh"):
        st.rerun()

    st.divider()

    st.markdown('<div class="sb-title">📖 Recent recipes</div>', unsafe_allow_html=True)
    if history_items:
        for h in history_items:
            st.markdown(f'<div class="hist-item">🕐 {h[0]}</div>', unsafe_allow_html=True)
        if st.button("🗑️ Clear history"):
            clear_history()
            st.success("History cleared!")
            st.rerun()
    else:
        st.caption("No recipes yet!")

    st.divider()

    st.markdown('<div class="sb-title">⚙️ Diet preference</div>', unsafe_allow_html=True)
    diets = ["Vegetarian", "Vegan", "Gluten-free", "Dairy-free", "Keto", "None"]
    selected_diet = st.selectbox("Diet", diets, label_visibility="collapsed")
    if st.button("💾 Save preference"):
        st.session_state.quick_action = f"Save my dietary preference as {selected_diet}"

# ── Main tabs ──────────────────────────────────
tab1, tab2 = st.tabs(["💬 Chat", "📅 Meal Planner"])

with tab1:
    chat_container = st.container(height=480)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if st.session_state.quick_action:
        user_input = st.session_state.quick_action
        st.session_state.quick_action = None
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("🤔 Thinking..."):
            try:
                response, st.session_state.history = chat(
                    st.session_state.model,
                    st.session_state.history,
                    user_input
                )
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")
        st.rerun()

    user_input = st.chat_input("Ask anything... 'I have eggs and bread' or 'Suggest an Indian recipe'")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("🤔 Thinking..."):
            try:
                response, st.session_state.history = chat(
                    st.session_state.model,
                    st.session_state.history,
                    user_input
                )
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")
        st.rerun()

with tab2:
    st.subheader("📅 Weekly Meal Planner")
    st.markdown("*Plan your entire week based on your pantry*")
    col_a, col_b = st.columns(2)
    with col_a:
        people = st.number_input("Number of people", min_value=1, max_value=10, value=2)
    with col_b:
        cuisine_pref = st.selectbox("Cuisine", ["Any", "Indian", "Italian", "Mexican", "Chinese"])
    if st.button("🗓️ Generate weekly meal plan", type="primary"):
        prompt = f"Create a detailed 7-day meal plan for {people} people"
        if cuisine_pref != "Any":
            prompt += f" with {cuisine_pref} cuisine"
        prompt += ". Use ingredients from my pantry where possible. Include breakfast, lunch and dinner for each day. Format it nicely day by day."
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("📅 Creating your meal plan..."):
            try:
                response, st.session_state.history = chat(
                    st.session_state.model,
                    st.session_state.history,
                    prompt
                )
                st.markdown("### Your Weekly Meal Plan")
                st.markdown(response)
            except Exception as e:
                st.error(f"Error: {e}")