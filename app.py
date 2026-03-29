import streamlit as st
from datetime import datetime
import random, re, copy

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Family Meal Planner",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Hide default Streamlit branding */
    #MainMenu {visibility:hidden;} footer {visibility:hidden;}

    /* Page background */
    .stApp { background: #f4f6f9; }

    /* Main header */
    .main-header {
        background: linear-gradient(135deg, #2D6A4F 0%, #1B4332 100%);
        color: white; padding: 24px 32px; border-radius: 16px;
        margin-bottom: 20px; text-align: center;
    }
    .main-header h1 { margin:0; font-size:2rem; font-weight:800; }
    .main-header p  { margin:4px 0 0; opacity:0.85; font-size:1rem; }

    /* Week badge */
    .week-badge {
        display:inline-block; background:#52B788; color:white;
        padding:4px 14px; border-radius:20px; font-size:0.85rem;
        font-weight:700; margin-top:8px;
    }

    /* Profile cards */
    .profile-card-wife {
        background: linear-gradient(135deg, #2D6A4F, #40916C);
        color:white; padding:20px; border-radius:14px; height:100%;
    }
    .profile-card-husband {
        background: linear-gradient(135deg, #1A4480, #2B7BB9);
        color:white; padding:20px; border-radius:14px; height:100%;
    }
    .profile-card-wife h3, .profile-card-husband h3 {
        margin:0 0 12px; font-size:1.2rem;
    }
    .profile-stat { font-size:0.85rem; opacity:0.9; margin:3px 0; }
    .profile-goal {
        display:inline-block; background:rgba(255,255,255,0.25);
        padding:3px 10px; border-radius:10px; font-size:0.8rem;
        font-weight:700; margin-top:8px;
    }

    /* Meal table rows */
    .meal-row {
        background:white; border-radius:10px; padding:10px 16px;
        margin-bottom:6px; border-left:4px solid #52B788;
        box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    }
    .meal-row-husband { border-left-color: #2B7BB9; }
    .meal-type { font-weight:700; font-size:0.8rem; color:#888; text-transform:uppercase; }
    .meal-name { font-size:0.95rem; font-weight:600; color:#1B1B1B; margin:2px 0; }
    .meal-items { font-size:0.82rem; color:#555; }
    .meal-cal   { font-size:0.82rem; font-weight:700; color:#2D6A4F; }
    .meal-cal-h { color:#1A4480; }

    /* Day header */
    .day-header-wife {
        background: #D8F3DC; color: #1B4332;
        padding: 8px 16px; border-radius: 8px;
        font-weight:800; font-size:0.95rem; margin: 14px 0 6px;
    }
    .day-header-husband {
        background: #D6E8F6; color: #1A4480;
        padding: 8px 16px; border-radius: 8px;
        font-weight:800; font-size:0.95rem; margin: 14px 0 6px;
    }

    /* Macro summary bar */
    .macro-bar {
        display:flex; gap:12px; flex-wrap:wrap;
        background:white; padding:10px 16px;
        border-radius:10px; margin-bottom:8px;
        box-shadow:0 1px 4px rgba(0,0,0,0.07);
    }
    .macro-chip {
        padding:3px 10px; border-radius:12px;
        font-size:0.8rem; font-weight:700;
    }
    .chip-cal  { background:#FFF3E0; color:#E65100; }
    .chip-prot { background:#E8F5E9; color:#2D6A4F; }
    .chip-carb { background:#E3F2FD; color:#1A4480; }
    .chip-fat  { background:#FFF9C4; color:#F57F17; }

    /* Chat messages */
    .chat-user { background:#2D6A4F; color:white; padding:8px 14px;
                 border-radius:14px 14px 4px 14px; margin:4px 0;
                 font-size:0.9rem; text-align:right; }
    .chat-bot  { background:white; color:#1B1B1B; padding:8px 14px;
                 border-radius:14px 14px 14px 4px; margin:4px 0;
                 font-size:0.9rem; border:1px solid #e0e0e0; }

    /* Section title */
    .section-title {
        font-size:1.1rem; font-weight:800; color:#1B4332;
        border-bottom:2px solid #52B788; padding-bottom:6px; margin-bottom:12px;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PROFILES
# ─────────────────────────────────────────────────────────────────────────────
WIFE = dict(
    name="Wife", emoji="👩", key="wife",
    age=30, weight=59, height=149, target_weight=52,
    goal="Weight Loss  🔥", bmr=1210, tdee=1664,
    cal_range="1,200–1,350 kcal", protein="55–68 g",
    timeline="~19 weeks to reach 52 kg",
    color="#2D6A4F", light_color="#D8F3DC", accent="#52B788",
    header_class="day-header-wife", card_class="profile-card-wife",
    row_class="meal-row", cal_class="meal-cal",
)
HUSBAND = dict(
    name="Husband", emoji="👨", key="husband",
    age=30, weight=69.5, height=176, target_weight=None,
    goal="Lean Muscle  💪", bmr=1650, tdee=2269,
    cal_range="2,300–2,500 kcal", protein="~140 g",
    timeline="12–16 weeks to visible muscle gains",
    color="#1A4480", light_color="#D6E8F6", accent="#2B7BB9",
    header_class="day-header-husband", card_class="profile-card-husband",
    row_class="meal-row meal-row-husband", cal_class="meal-cal meal-cal-h",
)

DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

# ─────────────────────────────────────────────────────────────────────────────
# MEAL DATA POOLS  (from FitPass / Aspire WellConsult prescription)
# ─────────────────────────────────────────────────────────────────────────────

# ── WIFE  (1,200–1,350 kcal/day, weight loss) ────────────────────────────────
WAKE_UP_W = {
    "type":"Wake-Up","name":"Honey Water + Soaked Almonds",
    "items":["Honey Water — 1 glass (34 Cal)","Soaked Almonds — 5 pieces (40 Cal)"],
    "cal":74,"p":1.5,"c":8.9,"f":3.5,
}
BEDTIME_W = {
    "type":"Bedtime","name":"Double Toned Milk",
    "items":["Double Toned Milk — 200 ml (94 Cal)"],
    "cal":94,"p":6.6,"c":10.0,"f":3.0,
}
SNACK_W = {
    "type":"Snack","name":"Guavas (raw)",
    "items":["Guavas, common raw — 1 cup (136 Cal)"],
    "cal":136,"p":5.2,"c":28.6,"f":2.0,
}

BREAKFAST_W = [
    {"name":"Sunny Side Up + Toast","items":["Sunny Side Up — 2 eggs (256 Cal)","Plain Toast — 2 slices (116 Cal)","Chamomile Tea — 1 cup (0 Cal)"],"cal":372,"p":17.2,"c":26.8,"f":23.0},
    {"name":"Scrambled Egg Whites + Toast","items":["Scrambled Egg White Without Oil — 3 whites (63 Cal)","Plain Toast — 2 slices (116 Cal)","Chamomile Tea — 1 cup (0 Cal)"],"cal":179,"p":15.7,"c":26.3,"f":1.3},
    {"name":"Vegetable Besan Cheela","items":["Veg Besan Cheela — 2 cheela (200 Cal)","Tomato Ketchup — 1 tbsp (16 Cal)","Chamomile Tea — 1 cup (0 Cal)"],"cal":216,"p":7.2,"c":22.5,"f":10.6},
    {"name":"Egg White Veg Omelette + Toast","items":["Egg White Veg Omelette — 3 whites (165 Cal)","Plain Toast — 1 slice (58 Cal)","Chamomile Tea — 1 cup (0 Cal)"],"cal":223,"p":13.6,"c":19.9,"f":9.5},
    {"name":"Boiled Eggs + Toast","items":["Boiled Egg — 3 pieces (231 Cal)","Plain Toast — 2 slices (116 Cal)","Chamomile Tea — 1 cup (0 Cal)"],"cal":347,"p":22.7,"c":26.6,"f":16.3},
    {"name":"Open Paneer Sandwich","items":["Veg Open Paneer Sandwich — 2 pieces (348 Cal)","Mint Chutney — 2 tbsp (13 Cal)","Chamomile Tea — 1 cup (0 Cal)"],"cal":361,"p":15.2,"c":54.9,"f":9.1},
    {"name":"Besan Cheela + Mint Chutney","items":["Veg Besan Cheela — 2 cheela (200 Cal)","Mint Chutney — 2 tbsp (13 Cal)","Chamomile Tea — 1 cup (0 Cal)"],"cal":213,"p":7.8,"c":21.1,"f":10.7},
]

LUNCH_W = [
    {"name":"Mix Dal + Rice + Curd","items":["Mix Dal — 200 g (198 Cal)","Boiled White Rice — 150 g (145 Cal)","Curd — 200 g (124 Cal)","Sliced Cucumber — 150 g (22 Cal)"],"cal":490,"p":29.5,"c":80.1,"f":16.3},
    {"name":"Jowar Roti + Shimla Mirch Sabji","items":["Jowar Roti — 2 rotis (182 Cal)","Shimla Mirch Besan Sabji — 200 g (168 Cal)","Curd — 200 g (124 Cal)"],"cal":474,"p":20.1,"c":68.4,"f":20.2},
    {"name":"Rajma + Rice + Curd","items":["Rajma Curry — 200 g (162 Cal)","Boiled White Rice — 150 g (145 Cal)","Curd — 200 g (124 Cal)"],"cal":431,"p":18.1,"c":63.2,"f":12.5},
    {"name":"Jowar Roti + Tofu Bhurji","items":["Jowar Roti — 2 rotis (182 Cal)","Tofu Bhurji — 200 g (206 Cal)","Cucumber & Tomato Salad — 200 g (36 Cal)"],"cal":424,"p":21.4,"c":51.4,"f":16.4},
    {"name":"Dal Parantha + Curd","items":["Dal Parantha — 2 parathas (372 Cal)","Curd — 1 cup (124 Cal)","Cucumber & Tomato Salad — 200 g (36 Cal)"],"cal":532,"p":20.5,"c":72.6,"f":20.6},
    {"name":"Veg Stuffed Jowar Roti + Curd","items":["Veg Stuffed Jowar Roti — 2 rotis (144 Cal)","Curd — 200 g (124 Cal)","Cucumber & Tomato Salad — 200 g (36 Cal)"],"cal":304,"p":11.0,"c":40.0,"f":8.0},
    {"name":"Masoor Dal Khichri + Curd","items":["Masoor Dal Khichri — 200 g (165 Cal)","Curd — 200 g (124 Cal)","Sliced Cucumber — 150 g (22 Cal)"],"cal":311,"p":13.5,"c":46.2,"f":5.5},
]

DINNER_W = [
    {"name":"Paneer Bhurji + Jowar Roti","items":["Paneer Bhurji — 200 g (312 Cal)","Jowar Roti — 1 roti (91 Cal)"],"cal":403,"p":16.6,"c":29.4,"f":25.0},
    {"name":"Tofu Sesame Salad","items":["Tofu Sesame Salad — 250 g (286 Cal)"],"cal":286,"p":25.9,"c":16.3,"f":14.9},
    {"name":"Egg Bhurji + Parantha","items":["Egg Bhurji — 200 g (244 Cal)","Plain Parantha Without Oil — 1 (118 Cal)"],"cal":362,"p":15.0,"c":33.5,"f":16.5},
    {"name":"Quinoa Salad + Soyabean Chaat","items":["Quinoa Salad — 200 g (168 Cal)","Boiled Soyabean Chaat — 100 g (134 Cal)"],"cal":302,"p":24.6,"c":31.2,"f":8.8},
    {"name":"Tofu Bhurji + Jowar Roti","items":["Tofu Bhurji — 200 g (206 Cal)","Jowar Roti — 1 roti (91 Cal)"],"cal":297,"p":16.2,"c":31.5,"f":8.4},
    {"name":"Namkeen Dalia + Steamed Veg","items":["Namkeen Dalia — 200 g (151 Cal)","Steamed Vegetables — 200 g (64 Cal)","Masala Aloo Dry — 150 g (208 Cal)"],"cal":423,"p":14.7,"c":77.5,"f":16.3},
    {"name":"Paneer Bhurji + Roti","items":["Paneer Bhurji — 150 g (234 Cal)","Jowar Roti — 1 roti (91 Cal)"],"cal":325,"p":13.5,"c":24.0,"f":18.0},
]

# ── HUSBAND  (2,300–2,500 kcal/day, lean muscle ~140g protein) ───────────────
WAKE_UP_H = {
    "type":"Wake-Up","name":"Honey Water + Almonds",
    "items":["Honey Water — 1 glass (34 Cal)","Soaked Almonds — 10 pieces (80 Cal)"],
    "cal":114,"p":3.0,"c":10.0,"f":7.0,
}
BEDTIME_H = {
    "type":"Bedtime","name":"Double Toned Milk",
    "items":["Double Toned Milk — 400 ml (188 Cal)"],
    "cal":188,"p":13.2,"c":20.0,"f":6.0,
}
SNACK_H = [
    {"name":"Guavas + Soyabean Chaat + Almonds","items":["Guavas — 1 cup (136 Cal)","Boiled Soyabean Chaat — 150 g (201 Cal)","Soaked Almonds — 10 pieces (80 Cal)"],"cal":417,"p":32.0,"c":46.0,"f":9.0},
    {"name":"Guavas + Paneer + Roti","items":["Guavas — 1 cup (136 Cal)","Paneer — 100 g (265 Cal)","Jowar Roti — 1 roti (91 Cal)"],"cal":492,"p":22.0,"c":38.0,"f":24.0},
    {"name":"Guavas + Quinoa Salad + Boiled Egg","items":["Guavas — 1 cup (136 Cal)","Quinoa Salad — 200 g (168 Cal)","Boiled Egg — 2 pieces (154 Cal)"],"cal":458,"p":24.0,"c":42.0,"f":14.0},
    {"name":"Guavas + Tofu + Roasted Chana","items":["Guavas — 1 cup (136 Cal)","Tofu — 100 g (80 Cal)","Roasted Chana — 30 g (100 Cal)","Almonds — 10 pieces (80 Cal)"],"cal":396,"p":22.0,"c":40.0,"f":12.0},
    {"name":"Fruit Bowl + Soyabean + Almonds","items":["Mixed Fruit Bowl — 1 cup (150 Cal)","Boiled Soyabean — 100 g (134 Cal)","Almonds — 10 pieces (80 Cal)"],"cal":364,"p":22.0,"c":40.0,"f":10.0},
    {"name":"Guavas + Paneer Bhurji","items":["Guavas — 1 cup (136 Cal)","Paneer Bhurji — 150 g (234 Cal)"],"cal":370,"p":16.0,"c":35.0,"f":16.0},
    {"name":"Guavas + Egg Bhurji","items":["Guavas — 1 cup (136 Cal)","Egg Bhurji — 150 g (183 Cal)","Jowar Roti — 1 roti (91 Cal)"],"cal":410,"p":20.0,"c":42.0,"f":14.0},
]

BREAKFAST_H = [
    {"name":"Sunny Side Up (3) + Toast + Milk","items":["Sunny Side Up — 3 eggs (384 Cal)","Plain Toast — 3 slices (174 Cal)","Double Toned Milk — 200 ml (94 Cal)","Chamomile Tea — 1 cup (0 Cal)"],"cal":652,"p":29.0,"c":42.0,"f":33.0},
    {"name":"Scrambled Whole Eggs + Toast + Milk","items":["Scrambled Whole Egg — 3 eggs (270 Cal)","Plain Toast — 3 slices (174 Cal)","Double Toned Milk — 200 ml (94 Cal)","Chamomile Tea — 1 cup (0 Cal)"],"cal":538,"p":29.0,"c":40.0,"f":22.0},
    {"name":"Besan Cheela (3) + Paneer + Toast","items":["Veg Besan Cheela — 3 cheela (300 Cal)","Paneer — 50 g (133 Cal)","Plain Toast — 2 slices (116 Cal)","Chamomile Tea — 1 cup (0 Cal)"],"cal":549,"p":26.0,"c":42.0,"f":22.0},
    {"name":"Boiled Eggs (4) + Toast + Milk","items":["Boiled Egg — 4 pieces (308 Cal)","Plain Toast — 3 slices (174 Cal)","Double Toned Milk — 200 ml (94 Cal)","Chamomile Tea — 1 cup (0 Cal)"],"cal":576,"p":35.0,"c":40.0,"f":22.0},
    {"name":"Paneer Sandwich + Milk","items":["Veg Open Paneer Sandwich — 3 pieces (522 Cal)","Mint Chutney — 2 tbsp (13 Cal)","Double Toned Milk — 200 ml (94 Cal)","Chamomile Tea — 1 cup (0 Cal)"],"cal":629,"p":27.0,"c":76.0,"f":20.0},
    {"name":"Egg White Omelette + Whole Egg + Toast","items":["Egg White Veg Omelette — 4 whites (220 Cal)","Boiled Egg — 1 piece (77 Cal)","Plain Toast — 2 slices (116 Cal)","Double Toned Milk — 200 ml (94 Cal)","Chamomile Tea — 1 cup (0 Cal)"],"cal":507,"p":33.0,"c":35.0,"f":16.0},
    {"name":"Besan Cheela + Boiled Eggs + Milk","items":["Veg Besan Cheela — 3 cheela (300 Cal)","Boiled Egg — 2 pieces (154 Cal)","Double Toned Milk — 200 ml (94 Cal)","Chamomile Tea — 1 cup (0 Cal)"],"cal":548,"p":30.0,"c":38.0,"f":20.0},
]

LUNCH_H = [
    {"name":"Mix Dal + Rice (big) + Curd + Roti","items":["Mix Dal — 200 g (198 Cal)","Boiled White Rice — 200 g (194 Cal)","Jowar Roti — 1 roti (91 Cal)","Curd — 200 g (124 Cal)","Cucumber & Tomato Salad — 200 g (36 Cal)"],"cal":643,"p":36.0,"c":108.0,"f":16.0},
    {"name":"Jowar Roti (3) + Shimla Mirch Sabji + Paneer","items":["Jowar Roti — 3 rotis (273 Cal)","Shimla Mirch Besan Sabji — 200 g (168 Cal)","Paneer Bhurji — 100 g (156 Cal)","Curd — 200 g (124 Cal)"],"cal":721,"p":38.0,"c":76.0,"f":28.0},
    {"name":"Rajma + Rice + Roti + Curd","items":["Rajma Curry — 200 g (162 Cal)","Boiled White Rice — 200 g (194 Cal)","Jowar Roti — 1 roti (91 Cal)","Curd — 200 g (124 Cal)","Salad — 200 g (36 Cal)"],"cal":607,"p":28.0,"c":92.0,"f":12.0},
    {"name":"Jowar Roti (3) + Tofu Bhurji + Dal","items":["Jowar Roti — 3 rotis (273 Cal)","Tofu Bhurji — 250 g (258 Cal)","Mix Dal — 100 g (99 Cal)","Curd — 200 g (124 Cal)"],"cal":754,"p":46.0,"c":72.0,"f":26.0},
    {"name":"Dal Parantha (3) + Curd + Soyabean","items":["Dal Parantha — 3 parathas (558 Cal)","Curd — 200 g (124 Cal)","Boiled Soyabean — 50 g (67 Cal)","Salad — 200 g (36 Cal)"],"cal":785,"p":38.0,"c":98.0,"f":26.0},
    {"name":"Masoor Khichri + Egg Bhurji + Curd","items":["Masoor Dal Khichri — 300 g (248 Cal)","Egg Bhurji — 100 g (122 Cal)","Curd — 200 g (124 Cal)","Salad — 200 g (36 Cal)"],"cal":530,"p":38.0,"c":60.0,"f":14.0},
    {"name":"Veg Stuffed Jowar Roti (3) + Dal + Curd","items":["Veg Stuffed Jowar Roti — 3 rotis (216 Cal)","Mix Dal — 200 g (198 Cal)","Curd — 200 g (124 Cal)","Salad — 200 g (36 Cal)"],"cal":574,"p":30.0,"c":76.0,"f":14.0},
]

DINNER_H = [
    {"name":"Paneer Bhurji (big) + Jowar Roti (2)","items":["Paneer Bhurji — 300 g (468 Cal)","Jowar Roti — 2 rotis (182 Cal)"],"cal":650,"p":33.0,"c":42.0,"f":38.0},
    {"name":"Tofu Sesame Salad + Dal + Roti","items":["Tofu Sesame Salad — 300 g (343 Cal)","Mix Dal — 100 g (99 Cal)","Jowar Roti — 1 roti (91 Cal)"],"cal":533,"p":38.0,"c":40.0,"f":20.0},
    {"name":"Egg Bhurji (big) + Parantha (2)","items":["Egg Bhurji — 300 g (366 Cal)","Plain Parantha Without Oil — 2 (236 Cal)"],"cal":602,"p":30.0,"c":54.0,"f":26.0},
    {"name":"Quinoa Salad + Soyabean + Paneer","items":["Quinoa Salad — 300 g (252 Cal)","Boiled Soyabean Chaat — 150 g (201 Cal)","Paneer — 50 g (133 Cal)"],"cal":586,"p":40.0,"c":44.0,"f":22.0},
    {"name":"Tofu Bhurji (big) + Jowar Roti (2) + Dal","items":["Tofu Bhurji — 300 g (309 Cal)","Jowar Roti — 2 rotis (182 Cal)","Mix Dal — 100 g (99 Cal)"],"cal":590,"p":40.0,"c":54.0,"f":18.0},
    {"name":"Paneer Bhurji + Dal + Roti","items":["Paneer Bhurji — 200 g (312 Cal)","Mix Dal — 150 g (149 Cal)","Jowar Roti — 2 rotis (182 Cal)"],"cal":643,"p":32.0,"c":60.0,"f":26.0},
    {"name":"Egg Curry + Jowar Roti (2)","items":["Egg Curry — 2 eggs (280 Cal)","Jowar Roti — 2 rotis (182 Cal)","Curd — 100 g (62 Cal)"],"cal":524,"p":28.0,"c":44.0,"f":18.0},
]


# ─────────────────────────────────────────────────────────────────────────────
# PLAN GENERATOR
# ─────────────────────────────────────────────────────────────────────────────
def generate_plan(profile_key: str, week_num: int) -> list:
    """Generate a deterministic 7-day plan seeded by week number."""
    seed = week_num * 1000 + (1 if profile_key == "wife" else 2)
    rng  = random.Random(seed)

    plan = []
    for day_idx in range(7):
        d_seed = seed + day_idx * 10
        rng2   = random.Random(d_seed)

        if profile_key == "wife":
            b = rng2.choice(BREAKFAST_W)
            l = rng2.choice(LUNCH_W)
            s = SNACK_W
            d = rng2.choice(DINNER_W)
            meals = [
                {**WAKE_UP_W, "type":"Wake-Up"},
                {**b,         "type":"Breakfast"},
                {**l,         "type":"Lunch"},
                {**s,         "type":"Snack"},
                {**d,         "type":"Dinner"},
                {**BEDTIME_W, "type":"Bedtime"},
            ]
        else:
            b = rng2.choice(BREAKFAST_H)
            l = rng2.choice(LUNCH_H)
            s = rng2.choice(SNACK_H)
            d = rng2.choice(DINNER_H)
            meals = [
                {**WAKE_UP_H, "type":"Wake-Up"},
                {**b,         "type":"Breakfast"},
                {**l,         "type":"Lunch"},
                {**s,         "type":"Snack"},
                {**d,         "type":"Dinner"},
                {**BEDTIME_H, "type":"Bedtime"},
            ]

        total_cal  = sum(m["cal"] for m in meals)
        total_p    = round(sum(m["p"]   for m in meals), 1)
        total_c    = round(sum(m["c"]   for m in meals), 1)
        total_f    = round(sum(m["f"]   for m in meals), 1)

        plan.append({
            "day": DAYS[day_idx],
            "meals": meals,
            "total_cal": total_cal,
            "total_p": total_p,
            "total_c": total_c,
            "total_f": total_f,
        })
    return plan


# ─────────────────────────────────────────────────────────────────────────────
# CHAT HANDLER
# ─────────────────────────────────────────────────────────────────────────────
DAY_MAP   = {d.lower(): i for i, d in enumerate(DAYS)}
MEAL_MAP  = {"wake-up":0,"breakfast":1,"lunch":2,"snack":3,"dinner":4,"bedtime":5}
ALT_POOLS = {
    "wife":    {"breakfast": BREAKFAST_W, "lunch": LUNCH_W, "snack": [SNACK_W], "dinner": DINNER_W},
    "husband": {"breakfast": BREAKFAST_H, "lunch": LUNCH_H, "snack": SNACK_H,   "dinner": DINNER_H},
}

def detect_day(msg: str):
    for name, idx in DAY_MAP.items():
        if name in msg: return idx, DAYS[idx]
    return None, None

def detect_meal(msg: str):
    for name, idx in MEAL_MAP.items():
        if name in msg: return idx, name
    return None, None

def handle_chat(msg: str, profile_key: str) -> str:
    """Return a text response and optionally modify session state plan."""
    msg_l = msg.lower().strip()
    plan_key = f"{profile_key}_plan"
    plan = st.session_state[plan_key]

    # ── Show options for a meal ──
    if any(w in msg_l for w in ["option","alternative","choice","what can","show me"]):
        day_idx, day_name = detect_day(msg_l)
        meal_idx, meal_name = detect_meal(msg_l)
        if meal_name and meal_name in ALT_POOLS[profile_key]:
            pool = ALT_POOLS[profile_key][meal_name]
            opts = "\n".join(f"• {m['name']} ({m['cal']} Cal)" for m in pool)
            return f"Here are all **{meal_name}** options:\n\n{opts}"
        return "Please mention a meal type (breakfast / lunch / snack / dinner) to see options."

    # ── Swap / change a specific meal ──
    if any(w in msg_l for w in ["swap","change","replace","different","switch"]):
        day_idx, day_name = detect_day(msg_l)
        meal_idx, meal_name = detect_meal(msg_l)

        if day_idx is None:
            return "Which day? (e.g. Monday, Tuesday…)"
        if meal_idx is None or meal_name not in ("breakfast","lunch","snack","dinner"):
            return f"Which meal on **{day_name}**? (breakfast / lunch / snack / dinner)"

        pool = ALT_POOLS[profile_key].get(meal_name, [])
        current = plan[day_idx]["meals"][meal_idx]["name"]
        alternatives = [m for m in pool if m["name"] != current]
        if not alternatives:
            return f"No alternative found for {meal_name} on {day_name}."

        new_meal = random.choice(alternatives)
        plan[day_idx]["meals"][meal_idx] = {**new_meal, "type": meal_name.capitalize()}
        # Recalculate totals
        plan[day_idx]["total_cal"] = sum(m["cal"] for m in plan[day_idx]["meals"])
        plan[day_idx]["total_p"]   = round(sum(m["p"] for m in plan[day_idx]["meals"]), 1)
        plan[day_idx]["total_c"]   = round(sum(m["c"] for m in plan[day_idx]["meals"]), 1)
        plan[day_idx]["total_f"]   = round(sum(m["f"] for m in plan[day_idx]["meals"]), 1)
        st.session_state[plan_key] = plan
        return (f"✅ Done! **{day_name} {meal_name.capitalize()}** changed to:\n\n"
                f"**{new_meal['name']}** — {new_meal['cal']} Cal, P:{new_meal['p']}g")

    # ── Make a day lighter / heavier ──
    if any(w in msg_l for w in ["lighter","lower cal","less calories","reduce"]):
        day_idx, day_name = detect_day(msg_l)
        if day_idx is None:
            return "Which day should I make lighter?"
        day = plan[day_idx]
        changes = []
        for slot, meal_name in [(1,"breakfast"),(2,"lunch"),(4,"dinner")]:
            pool = ALT_POOLS[profile_key].get(meal_name,[])
            current = day["meals"][slot]
            lighter = [m for m in pool if m["cal"] < current["cal"] and m["name"] != current["name"]]
            if lighter:
                best = min(lighter, key=lambda x: x["cal"])
                day["meals"][slot] = {**best, "type": meal_name.capitalize()}
                changes.append(f"• {meal_name.capitalize()} → {best['name']} ({best['cal']} Cal)")
        day["total_cal"] = sum(m["cal"] for m in day["meals"])
        day["total_p"]   = round(sum(m["p"] for m in day["meals"]),1)
        day["total_c"]   = round(sum(m["c"] for m in day["meals"]),1)
        day["total_f"]   = round(sum(m["f"] for m in day["meals"]),1)
        st.session_state[plan_key] = plan
        if changes:
            return f"✅ **{day_name}** made lighter ({day['total_cal']} Cal total):\n\n" + "\n".join(changes)
        return f"**{day_name}** is already at a low-calorie configuration."

    if any(w in msg_l for w in ["heavier","more calories","bulk","increase"]):
        day_idx, day_name = detect_day(msg_l)
        if day_idx is None:
            return "Which day should I make heavier?"
        day = plan[day_idx]
        changes = []
        for slot, meal_name in [(1,"breakfast"),(2,"lunch"),(4,"dinner")]:
            pool = ALT_POOLS[profile_key].get(meal_name,[])
            current = day["meals"][slot]
            heavier = [m for m in pool if m["cal"] > current["cal"] and m["name"] != current["name"]]
            if heavier:
                best = max(heavier, key=lambda x: x["cal"])
                day["meals"][slot] = {**best, "type": meal_name.capitalize()}
                changes.append(f"• {meal_name.capitalize()} → {best['name']} ({best['cal']} Cal)")
        day["total_cal"] = sum(m["cal"] for m in day["meals"])
        day["total_p"]   = round(sum(m["p"] for m in day["meals"]),1)
        day["total_c"]   = round(sum(m["c"] for m in day["meals"]),1)
        day["total_f"]   = round(sum(m["f"] for m in day["meals"]),1)
        st.session_state[plan_key] = plan
        if changes:
            return f"✅ **{day_name}** made higher-calorie ({day['total_cal']} Cal total):\n\n" + "\n".join(changes)
        return f"**{day_name}** is already at a high-calorie configuration."

    # ── Reset plan ──
    if any(w in msg_l for w in ["reset","original","start over","regenerate"]):
        week_num = datetime.now().isocalendar()[1]
        st.session_state[plan_key] = generate_plan(profile_key, week_num)
        return "✅ Plan reset to this week's auto-generated version!"

    # ── Calorie summary ──
    if any(w in msg_l for w in ["total","calorie","macro","summary","how many"]):
        lines = [f"**Weekly calorie summary:**"]
        for d in plan:
            lines.append(f"• {d['day']}: {d['total_cal']} Cal  |  P:{d['total_p']}g  C:{d['total_c']}g  F:{d['total_f']}g")
        avg = round(sum(d['total_cal'] for d in plan)/7)
        lines.append(f"\n**Average: {avg} Cal/day**")
        return "\n".join(lines)

    # ── Help ──
    if any(w in msg_l for w in ["help","what can","how to","command"]):
        return (
            "I can help you modify the meal plan! Try:\n\n"
            "• **Swap Monday breakfast** — get a different breakfast on Monday\n"
            "• **Change Thursday lunch** — swap Thursday's lunch\n"
            "• **Make Wednesday lighter** — lower the calories for Wednesday\n"
            "• **Make Friday heavier** — increase calories for Friday\n"
            "• **Show breakfast options** — see all breakfast choices\n"
            "• **Total calories summary** — see weekly macro summary\n"
            "• **Reset plan** — go back to the auto-generated plan\n"
        )

    return (
        "I didn't quite understand that. Type **help** to see what I can do, "
        "or try something like 'swap Monday breakfast' or 'make Wednesday lighter'."
    )


# ─────────────────────────────────────────────────────────────────────────────
# RENDER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────
def render_meal_row(meal: dict, profile: dict):
    items_str = " · ".join(meal["items"])
    st.markdown(f"""
    <div class="{profile['row_class']}">
        <div class="meal-type">{meal['type']}</div>
        <div class="meal-name">{meal['name']}</div>
        <div class="meal-items">{items_str}</div>
        <div class="{profile['cal_class']}">
            {meal['cal']} Cal &nbsp;|&nbsp; P:{meal['p']}g &nbsp;C:{meal['c']}g &nbsp;F:{meal['f']}g
        </div>
    </div>""", unsafe_allow_html=True)


def render_day(day_data: dict, profile: dict):
    st.markdown(f"""
    <div class="{profile['header_class']}">
        📅 {day_data['day']}
        <span style="float:right;font-size:0.85rem;">
            {day_data['total_cal']} Cal &nbsp;|&nbsp;
            P:{day_data['total_p']}g &nbsp;
            C:{day_data['total_c']}g &nbsp;
            F:{day_data['total_f']}g
        </span>
    </div>""", unsafe_allow_html=True)
    for meal in day_data["meals"]:
        render_meal_row(meal, profile)


def render_profile_card(profile: dict):
    bmi = round(profile["weight"] / (profile["height"]/100)**2, 1)
    target_str = f"→ {profile['target_weight']} kg" if profile.get("target_weight") else "Build Lean Mass"
    st.markdown(f"""
    <div class="{profile['card_class']}">
        <h3>{profile['emoji']} {profile['name']}</h3>
        <div class="profile-stat">🎂 Age: {profile['age']} years</div>
        <div class="profile-stat">📏 Height: {profile['height']} cm &nbsp;|&nbsp; BMI: {bmi}</div>
        <div class="profile-stat">⚖️ Weight: {profile['weight']} kg &nbsp;{target_str}</div>
        <div class="profile-stat">🔥 BMR: {profile['bmr']} kcal &nbsp;|&nbsp; TDEE: {profile['tdee']} kcal</div>
        <div class="profile-stat">🍽️ Target: {profile['cal_range']} &nbsp;|&nbsp; Protein: {profile['protein']}</div>
        <div class="profile-stat">⏱️ {profile['timeline']}</div>
        <span class="profile-goal">{profile['goal']}</span>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────────────────────
iso_week = datetime.now().isocalendar()[1]
iso_year = datetime.now().isocalendar()[0]
week_label = f"Week {iso_week}, {iso_year}"

if "wife_plan" not in st.session_state:
    st.session_state.wife_plan = generate_plan("wife", iso_week)
if "husband_plan" not in st.session_state:
    st.session_state.husband_plan = generate_plan("husband", iso_week)
if "wife_chat" not in st.session_state:
    st.session_state.wife_chat = [
        {"role":"assistant","content":"Hi! I'm your meal plan assistant. Type **help** to see what I can do."}
    ]
if "husband_chat" not in st.session_state:
    st.session_state.husband_chat = [
        {"role":"assistant","content":"Hi! I'm your meal plan assistant. Type **help** to see what I can do."}
    ]
if "active_chat" not in st.session_state:
    st.session_state.active_chat = "wife"


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — CHAT
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 💬 Meal Plan Assistant")

    chat_for = st.radio("Modify plan for:", ["Wife", "Husband"],
                        horizontal=True, key="chat_radio")
    profile_key = chat_for.lower()
    chat_key    = f"{profile_key}_chat"

    # Display chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state[chat_key]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Input
    user_input = st.chat_input("e.g. swap Monday breakfast…")
    if user_input:
        st.session_state[chat_key].append({"role":"user","content":user_input})
        response = handle_chat(user_input, profile_key)
        st.session_state[chat_key].append({"role":"assistant","content":response})
        st.rerun()

    st.markdown("---")
    st.markdown("**Quick commands:**")
    quick = [
        "swap Monday breakfast",
        "change Wednesday lunch",
        "make Thursday lighter",
        "show dinner options",
        "total calories summary",
        "reset plan",
    ]
    for q in quick:
        if st.button(q, key=f"q_{q}", use_container_width=True):
            st.session_state[chat_key].append({"role":"user","content":q})
            resp = handle_chat(q, profile_key)
            st.session_state[chat_key].append({"role":"assistant","content":resp})
            st.rerun()

    st.markdown("---")
    st.caption("🔄 Plan auto-rotates every Monday based on the week number.")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="main-header">
    <h1>🥗 Family Meal Planner</h1>
    <p>Aspire WellConsult (OPD) · FitPass Prescription</p>
    <span class="week-badge">📅 {week_label}</span>
</div>""", unsafe_allow_html=True)

# Profile cards
col1, col2 = st.columns(2)
with col1:
    render_profile_card(WIFE)
with col2:
    render_profile_card(HUSBAND)

st.markdown("<br>", unsafe_allow_html=True)

# Tabs
tab_wife, tab_husband = st.tabs(["👩 Wife's Plan  (Weight Loss)", "👨 Husband's Plan  (Lean Muscle)"])

with tab_wife:
    wife_plan = st.session_state.wife_plan
    avg_cal_w = round(sum(d["total_cal"] for d in wife_plan) / 7)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg Daily Calories", f"{avg_cal_w} kcal", delta=f"Target: 1,200–1,350")
    c2.metric("Avg Protein", f"{round(sum(d['total_p'] for d in wife_plan)/7, 1)} g", "Target: 55–68 g")
    c3.metric("Avg Carbs",   f"{round(sum(d['total_c'] for d in wife_plan)/7, 1)} g")
    c4.metric("Avg Fat",     f"{round(sum(d['total_f'] for d in wife_plan)/7, 1)} g")

    st.markdown("<br>", unsafe_allow_html=True)

    # 2 columns layout for the 7 days
    days_col1 = wife_plan[:4]
    days_col2 = wife_plan[4:]
    col_a, col_b = st.columns(2)
    with col_a:
        for day_data in days_col1:
            render_day(day_data, WIFE)
    with col_b:
        for day_data in days_col2:
            render_day(day_data, WIFE)

with tab_husband:
    husband_plan = st.session_state.husband_plan
    avg_cal_h = round(sum(d["total_cal"] for d in husband_plan) / 7)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg Daily Calories", f"{avg_cal_h} kcal", delta=f"Target: 2,300–2,500")
    c2.metric("Avg Protein", f"{round(sum(d['total_p'] for d in husband_plan)/7, 1)} g", "Target: ~140 g")
    c3.metric("Avg Carbs",   f"{round(sum(d['total_c'] for d in husband_plan)/7, 1)} g")
    c4.metric("Avg Fat",     f"{round(sum(d['total_f'] for d in husband_plan)/7, 1)} g")

    st.markdown("<br>", unsafe_allow_html=True)

    days_col1 = husband_plan[:4]
    days_col2 = husband_plan[4:]
    col_a, col_b = st.columns(2)
    with col_a:
        for day_data in days_col1:
            render_day(day_data, HUSBAND)
    with col_b:
        for day_data in days_col2:
            render_day(day_data, HUSBAND)

# Footer
st.markdown("---")
st.caption(
    "🔄 Plan auto-rotates every week  ·  "
    "💬 Use the chat sidebar to modify any meal  ·  "
    "📋 Based on Aspire WellConsult FitPass prescription (Mar 2026)"
)
