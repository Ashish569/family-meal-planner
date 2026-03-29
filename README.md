# 🥗 Family Meal Planner — Aspire WellConsult

A free, automatically-rotating weekly meal plan website for both wife (weight loss)
and husband (lean muscle), built with Streamlit.

---

## ✨ Features

| Feature | Details |
|---|---|
| 👩 Wife's Plan | 1,200–1,350 kcal/day · Weight loss (59 → 52 kg) |
| 👨 Husband's Plan | 2,300–2,500 kcal/day · Lean muscle (69.5 kg, ~140g protein) |
| 🔄 Auto-rotation | Plan changes every Monday automatically |
| 💬 Chat to modify | Swap meals, change days, make lighter/heavier |
| 📊 Macro tracking | Daily calories, protein, carbs, fat |
| 🆓 Free hosting | Streamlit Community Cloud |

---

## 🚀 Deploy in 5 Steps (FREE)

### Step 1 — Create a GitHub account
Go to [github.com](https://github.com) and sign up (free).

### Step 2 — Create a new repository
1. Click **New repository**
2. Name it: `family-meal-planner`
3. Set to **Public**
4. Click **Create repository**

### Step 3 — Upload these files
Upload all files from this folder into your new GitHub repo:
```
app.py
requirements.txt
.streamlit/config.toml
.github/workflows/weekly_update.yml
```

### Step 4 — Deploy on Streamlit Community Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **New app**
4. Select your `family-meal-planner` repo
5. Main file: `app.py`
6. Click **Deploy!**

✅ Your website will be live at:
`https://your-username-family-meal-planner-app-XXXX.streamlit.app`

### Step 5 — Enable weekly auto-refresh (optional)
The app auto-rotates based on the week number — no action needed.
The GitHub Actions workflow runs every Monday at 6 AM IST as a safety trigger.

---

## 💬 Chat Commands

| Say this | What happens |
|---|---|
| `swap Monday breakfast` | Gets a different Monday breakfast |
| `change Wednesday lunch` | Swaps Wednesday's lunch |
| `make Thursday lighter` | Reduces Thursday's calories |
| `make Friday heavier` | Increases Friday's calories |
| `show dinner options` | Lists all dinner alternatives |
| `total calories summary` | Shows weekly macro breakdown |
| `reset plan` | Restores the auto-generated plan |

---

## 📋 Nutritional Profiles

### Wife
- Age: 30 · Height: 149 cm · Weight: 59 kg → Target: 52 kg
- BMR: 1,210 kcal · TDEE: 1,664 kcal
- Daily target: ~1,200–1,350 kcal (~400 kcal deficit)
- Timeline: ~19 weeks to reach 52 kg

### Husband
- Age: 30 · Height: 176 cm · Weight: 69.5 kg
- Goal: Lean muscle (body recomposition)
- BMR: 1,650 kcal · TDEE: 2,269 kcal
- Daily target: ~2,300–2,500 kcal (+250 surplus)
- Protein: ~140 g/day (2 g/kg)

---

## 🍽️ Meal Sources
All meals sourced from the Aspire WellConsult (OPD) FitPass prescription (March 2026).
Same Indian vegetarian + egg foods for both — just different portions.
