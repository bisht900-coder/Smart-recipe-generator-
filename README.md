# 🍳 Smart Recipe Generator – AI Cooking Assistant

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Database](https://img.shields.io/badge/database-SQLite3-lightgrey.svg)](https://www.sqlite.org/)
[![Responsive](https://img.shields.io/badge/UI-Responsive%20%26%20Accessible-brightgreen.svg)](#)

> Turn whatever is in your fridge into delicious meals! Enter the ingredients you already have at home, discover instant recipes, get smart substitute suggestions, and reduce household food waste.

---

## 🌟 Key Features

1. 🔍 **Fuzzy Search & Spelling Suggestion**  
   - Typo-tolerant ingredient search using fuzzy matching (e.g., typing *"tamato"* suggests *"Did you mean: Tomato?"*).
   - Indian synonym mapping (*aloo* ↔ *potato*, *pyaz* ↔ *onion*, *atta* ↔ *wheat flour*, *capsicum* ↔ *bell pepper*).

2. 📸 **Curated HD Recipe Photography**  
   - Dish-specific photography with lazy loading and responsive scaling.
   - Built-in offline SVG fallback placeholder if connection drops.

3. 🎯 **Qualitative Pantry Matching (No Numbers / Percentages)**  
   - Recipes sorted by relevance with clear, qualitative status badges:
     - 🟢 **Pantry Ready:** You have all required ingredients!
     - 🟡 **1 Item Needed:** Missing just one item.
     - 🟠 **Few Items Needed:** Cookable with minor additions.
     - ♻️ **Leftover Hero:** Specially curated to repurpose kitchen leftovers.

4. 🍲 **"You May Also Like" Recommendations**  
   - Related recipe suggestions based on overlapping ingredients so you can discover alternative meal ideas.

5. 🍳 **Kitchen Utensils List**  
   - Every recipe shows the equipment needed (e.g., 🔪 Chef Knife, 🍳 Heavy Kadai, 🥘 Tawa, 🫕 Pressure Cooker).

6. ⏱️ **Chef Pro Tips & Step Flame Levels**  
   - Clear numbered steps with explicit heat levels (*Low Heat*, *Medium Flame*, *High Heat*, *Dum / No Flame*), step duration, and chef tips for foolproof cooking.

7. 🔄 **Smart Ingredient Substitutes**  
   - Missing an ingredient? Real-time culinary alternatives appear directly on the recipe card (e.g., yogurt for cream, tofu for paneer, oil for butter).

8. ⭐ **Community Reviews & Star Rating System**  
   - 1-to-5 star rating picker, user feedback, review counts, and dynamic average calculation.

9. 🌐 **Multi-Language Support**  
   - Instant language switching between **English**, **हिंदी (Hindi)**, and **Hinglish**.

10. 🎨 **Modern & Accessible Design**  
    - Ambient culinary gradient background with GPU-accelerated micro-animations.
    - Honors `prefers-reduced-motion` and optimized for smooth performance on low-end devices.

---

## 🚀 Live Demo & Deployment

This project supports **two ways to run**:

### Option A: 1-Click Streamlit Cloud (Fastest & Free)

Deploy directly to the web with zero server setup:

1. Fork or push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and log in with GitHub.
3. Click **New app** and select:
   - **Repository:** `Luckysisodia14/smart-recipe-generator`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
4. Click **Deploy!** 🚀

### Option B: Local Flask Web Application

```bash
# 1. Clone the repository
git clone https://github.com/Luckysisodia14/smart-recipe-generator.git
cd smart-recipe-generator

# 2. Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database
python init_db.py

# 5. Run the server
python run.py
