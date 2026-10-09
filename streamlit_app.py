"""
Smart Recipe Generator – Standalone Streamlit Cloud Edition
Self-contained single file with zero local folder dependencies.
Can be run locally or pasted directly into GitHub to deploy on Streamlit Cloud!
"""
import streamlit as st
import sqlite3
import difflib
import json
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Smart Recipe Generator",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DATABASE SETUP (SELF-CONTAINED & PERSISTENT) ---
DB_FILE = "recipes_cloud.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@st.cache_resource
def init_standalone_db():
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        food_type TEXT NOT NULL,
        spice_level TEXT,
        preparation_time INTEGER,
        cooking_time INTEGER,
        difficulty_level TEXT,
        image_url TEXT,
        is_leftover_friendly INTEGER DEFAULT 0,
        cuisine TEXT DEFAULT 'North Indian',
        meal_type TEXT DEFAULT 'Lunch/Dinner',
        diet_pref TEXT DEFAULT 'Vegetarian',
        utensils TEXT DEFAULT '',
        rating REAL DEFAULT 4.8,
        review_count INTEGER DEFAULT 15
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS recipe_ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER,
        ingredient_name TEXT NOT NULL,
        quantity TEXT,
        unit TEXT
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS cooking_steps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER,
        step_number INTEGER,
        instruction TEXT,
        heat_level TEXT,
        duration TEXT,
        pro_tip TEXT
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS ingredient_substitutes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ingredient_name TEXT NOT NULL,
        substitute_name TEXT NOT NULL,
        note TEXT
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS recipe_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER,
        user_name TEXT,
        rating INTEGER,
        comment TEXT
    )''')
    conn.commit()

    # Check if recipes seeded
    c.execute("SELECT COUNT(*) FROM recipes")
    if c.fetchone()[0] == 0:
        seed_data(conn)
    conn.close()

def seed_data(conn):
    c = conn.cursor()
    recipes_data = [
        (1, 'Aloo Paratha', 'Vegetarian', 'Medium', 'Medium', 20, 15,
         'https://images.unsplash.com/photo-1626074353765-517a681e40be?auto=format&fit=crop&w=800&q=80',
         'Flaky golden whole wheat flatbread stuffed with spiced potato filling.', 1, 'North Indian', 'Breakfast', 'Vegetarian',
         json.dumps(["Tawa (Flat Griddle)", "Rolling Pin & Board", "Mixing Bowl", "Spatula"]), 4.9, 28),
        (2, 'Aloo Gobi', 'Vegetarian', 'Medium', 'Easy', 25, 10,
         'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=800&q=80',
         'Home-style dry curry made with tender cauliflower florets, golden potatoes, and warm spices.', 0, 'North Indian', 'Lunch/Dinner', 'Vegan',
         json.dumps(["Deep Kadai", "Chef Knife", "Stirring Ladle"]), 4.7, 19),
        (3, 'Paneer Butter Masala', 'Vegetarian', 'Mild', 'Medium', 30, 15,
         'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=800&q=80',
         'Soft cottage cheese cubes simmered in a silky, buttery tomato-cashew gravy.', 0, 'North Indian', 'Lunch/Dinner', 'High Protein',
         json.dumps(["Saucepan / Kadai", "Blender", "Fine Strainer"]), 4.9, 42),
        (4, 'Vegetable Pulao', 'Vegetarian', 'Mild', 'Easy', 25, 10,
         'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=800&q=80',
         'Fragrant basmati rice cooked with fresh seasonal vegetables and whole spices.', 1, 'North Indian', 'Lunch/Dinner', 'Gluten-Free',
         json.dumps(["Pressure Cooker / Pot", "Colander", "Ladle"]), 4.8, 23),
        (5, 'Poha', 'Vegetarian', 'Mild', 'Easy', 15, 5,
         'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&w=800&q=80',
         'Light and fluffy flattened rice sautéed with crunchy peanuts, onions, and fresh lemon.', 1, 'Street Food', 'Breakfast', 'Vegan',
         json.dumps(["Frying Pan", "Colander", "Wooden Spoon"]), 4.8, 31),
        (6, 'Veg Sandwich', 'Vegetarian', 'Mild', 'Easy', 8, 7,
         'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=800&q=80',
         'Crispy toasted sandwich layered with cucumber, tomato, boiled potato, chutney, and cheese.', 1, 'Continental', 'Snacks', 'Quick & Easy',
         json.dumps(["Grill Pan / Tawa", "Butter Knife", "Spatula"]), 4.7, 26),
        (7, 'Masala Omelette', 'Non-Vegetarian', 'Medium', 'Easy', 8, 5,
         'https://images.unsplash.com/photo-1510693206972-df098062cb71?auto=format&fit=crop&w=800&q=80',
         'Fluffy beaten eggs infused with finely diced onions, tomatoes, and green chillies.', 0, 'Continental', 'Breakfast', 'High Protein',
         json.dumps(["Non-Stick Skillet", "Mixing Bowl", "Whisk"]), 4.9, 37),
        (8, 'Chicken Curry', 'Non-Vegetarian', 'Spicy', 'Medium', 35, 15,
         'https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=800&q=80',
         'Tender chicken pieces simmered in an aromatic onion, ginger, garlic, and tomato gravy.', 0, 'North Indian', 'Lunch/Dinner', 'High Protein',
         json.dumps(["Heavy Kadai", "Chef Knife", "Wooden Spatula"]), 4.9, 54),
        (9, 'Egg Fried Rice', 'Non-Vegetarian', 'Mild', 'Easy', 15, 10,
         'https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=800&q=80',
         'Savory wok-tossed day-old rice combined with scrambled eggs, scallions, and soy sauce.', 1, 'Indo-Chinese', 'Lunch/Dinner', 'Quick & Easy',
         json.dumps(["Wok / Large Pan", "Wok Ladle"]), 4.8, 30),
        (10, 'Dal Tadka', 'Vegetarian', 'Medium', 'Easy', 25, 10,
         'https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=800&q=80',
         'Creamy yellow lentils finished with sizzling ghee tempering of cumin, garlic, and dried chillies.', 0, 'North Indian', 'Lunch/Dinner', 'High Protein',
         json.dumps(["Pressure Cooker", "Tadka Pan", "Whisk"]), 4.9, 33),
        (11, 'Chole', 'Vegetarian', 'Spicy', 'Medium', 35, 15,
         'https://images.unsplash.com/photo-1596797038530-2c107229654b?auto=format&fit=crop&w=800&q=80',
         'Punjabi style dark chickpea curry loaded with aromatic spices and tangy gravy.', 0, 'North Indian', 'Lunch/Dinner', 'High Protein',
         json.dumps(["Pressure Cooker", "Deep Kadai", "Masher"]), 4.8, 29),
        (12, 'Chicken Biryani', 'Non-Vegetarian', 'Spicy', 'Hard', 50, 25,
         'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=800&q=80',
         'Royal layered feast of aromatic saffron basmati rice and marinated spicy chicken cooked on dum.', 0, 'North Indian', 'Lunch/Dinner', 'High Protein',
         json.dumps(["Heavy Handi", "Large Rice Strainer", "Tawa for Dum"]), 5.0, 68),
        (13, 'French Fries', 'Vegetarian', 'Mild', 'Easy', 15, 15,
         'https://images.unsplash.com/photo-1576107232684-1279f3908594?auto=format&fit=crop&w=800&q=80',
         'Ultra crispy, golden potato batons seasoned with sea salt and black pepper.', 0, 'Continental', 'Snacks', 'Vegan',
         json.dumps(["Deep Frying Kadai", "Slotted Spoon", "Paper Towel"]), 4.8, 40),
        (14, 'Masala Dosa', 'Vegetarian', 'Medium', 'Hard', 20, 15,
         'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=800&q=80',
         'Crispy fermented crepe folded over a flavorful turmeric potato and mustard seed mash.', 0, 'South Indian', 'Breakfast', 'Gluten-Free',
         json.dumps(["Cast Iron Tawa", "Pouring Ladle", "Flat Spatula"]), 4.9, 45)
    ]
    c.executemany('''
        INSERT INTO recipes (id, name, food_type, spice_level, difficulty_level, cooking_time, preparation_time,
                             image_url, description, is_leftover_friendly, cuisine, meal_type, diet_pref, utensils, rating, review_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', recipes_data)

    ingredients_data = [
        # Aloo Paratha
        (1, 'wheat flour', '2', 'cups'), (1, 'potato', '3', 'boiled'), (1, 'green chilli', '2', 'chopped'), (1, 'ghee', '2', 'tbsp'),
        # Aloo Gobi
        (2, 'cauliflower', '1', 'head'), (2, 'potato', '2', 'cubed'), (2, 'onion', '1', 'chopped'), (2, 'turmeric', '0.5', 'tsp'),
        # Paneer Butter Masala
        (3, 'paneer', '250', 'g'), (3, 'tomato', '4', 'ripe'), (3, 'butter', '3', 'tbsp'), (3, 'garlic', '5', 'cloves'),
        # Vegetable Pulao
        (4, 'rice', '1.5', 'cups'), (4, 'carrot', '1', 'diced'), (4, 'peas', '0.5', 'cup'), (4, 'ghee', '2', 'tbsp'),
        # Poha
        (5, 'flattened rice', '2', 'cups'), (5, 'onion', '1', 'chopped'), (5, 'peanut', '3', 'tbsp'), (5, 'lemon juice', '1', 'tbsp'),
        # Veg Sandwich
        (6, 'bread', '4', 'slices'), (6, 'potato', '1', 'boiled'), (6, 'tomato', '1', 'sliced'), (6, 'butter', '2', 'tbsp'),
        # Masala Omelette
        (7, 'egg', '2', 'eggs'), (7, 'onion', '2', 'tbsp'), (7, 'green chilli', '1', 'minced'), (7, 'oil', '1', 'tbsp'),
        # Chicken Curry
        (8, 'chicken', '500', 'g'), (8, 'onion', '2', 'sliced'), (8, 'tomato', '2', 'pureed'), (8, 'garlic', '5', 'cloves'),
        # Egg Fried Rice
        (9, 'rice', '2', 'cups cooked'), (9, 'egg', '2', 'eggs'), (9, 'soy sauce', '1.5', 'tbsp'), (9, 'garlic', '3', 'cloves'),
        # Dal Tadka
        (10, 'toor dal', '1', 'cup'), (10, 'tomato', '1', 'chopped'), (10, 'garlic', '4', 'cloves'), (10, 'ghee', '2', 'tbsp'),
        # Chole
        (11, 'chana', '1.5', 'cups'), (11, 'onion', '2', 'minced'), (11, 'tomato', '2', 'pureed'), (11, 'garlic', '4', 'cloves'),
        # Chicken Biryani
        (12, 'chicken', '500', 'g'), (12, 'rice', '2', 'cups basmati'), (12, 'onion', '2', 'sliced'), (12, 'ghee', '3', 'tbsp'),
        # French Fries
        (13, 'potato', '3', 'large'), (13, 'oil', '2', 'cups'), (13, 'salt', '1', 'tsp'),
        # Masala Dosa
        (14, 'dosa batter', '2', 'cups'), (14, 'potato', '2', 'boiled'), (14, 'onion', '1', 'sliced'), (14, 'mustard seeds', '1', 'tsp')
    ]
    c.executemany("INSERT INTO recipe_ingredients (recipe_id, ingredient_name, quantity, unit) VALUES (?, ?, ?, ?)", ingredients_data)

    steps_data = [
        # Aloo Paratha
        (1, 1, 'Knead 2 cups wheat flour with 3/4 cup water into soft dough. Rest 15 mins.', 'No Flame', '5 mins', 'Soft dough keeps stuffing inside.'),
        (1, 2, 'Mash 3 boiled potatoes completely with chillies, cumin, and salt.', 'No Flame', '3 mins', 'Cool potatoes prevent moisture leaks.'),
        (1, 3, 'Roll dough circle, place 2 tbsp potato filling in center, seal and roll flat.', 'No Flame', '4 mins', 'Roll gently from center outward.'),
        (1, 4, 'Cook on a medium-hot tawa with ghee on both sides until golden spots appear.', 'Medium Flame', '3 mins', 'Medium heat ensures cooked interior.'),
        
        # Paneer Butter Masala
        (3, 1, 'Boil tomatoes, garlic, and cashews in 1 cup water for 10 mins. Blend into smooth purée.', 'Medium Flame', '10 mins', 'Cashews give velvety texture.'),
        (3, 2, 'Melt 2 tbsp butter in a kadai, pour tomato purée, add chilli powder and turmeric.', 'Medium Flame', '8 mins', 'Stir continuously to prevent sticking.'),
        (3, 3, 'Simmer gravy on low heat until butter separates on top.', 'Low Heat', '8 mins', 'Cover the pan to avoid splatters.'),
        (3, 4, 'Add fresh paneer cubes and cream. Simmer for just 3 minutes and remove from heat.', 'Low Heat', '3 mins', 'Do not overcook paneer or it turns rubbery.'),
        
        # Poha
        (5, 1, 'Rinse 2 cups thick flattened rice under water for 30 seconds. Drain completely.', 'No Flame', '2 mins', 'Do not soak; quick rinse is enough.'),
        (5, 2, 'Roast peanuts in 2 tbsp hot oil until crunchy and set aside.', 'Medium Flame', '3 mins', 'Frying separately keeps peanuts crunchy.'),
        (5, 3, 'Splutter mustard seeds, sauté chopped onions and chillies until translucent.', 'Medium Flame', '3 mins', 'Cook onions soft, not dark brown.'),
        (5, 4, 'Add turmeric, drained poha, and fried peanuts. Toss gently on low heat with lemon juice.', 'Low Heat', '3 mins', 'Toss gently so flakes stay fluffy.')
    ]
    c.executemany("INSERT INTO cooking_steps (recipe_id, step_number, instruction, heat_level, duration, pro_tip) VALUES (?, ?, ?, ?, ?, ?)", steps_data)

    substitutes_data = [
        ('butter', 'oil', 'Use cooking oil in 3:4 ratio'),
        ('cream', 'milk + butter', 'Whisk whole milk with melted butter'),
        ('paneer', 'tofu', 'Firm pressed tofu for dairy-free texture'),
        ('ghee', 'butter', 'Regular unsalted butter works well'),
        ('chicken', 'mushroom', 'King oyster mushrooms provide meaty chew'),
        ('bread', 'tortilla', 'Roti or tortilla can wrap sandwich ingredients'),
        ('potato', 'sweet potato', 'Healthier lower-glycemic root substitute')
    ]
    c.executemany("INSERT INTO ingredient_substitutes (ingredient_name, substitute_name, note) VALUES (?, ?, ?)", substitutes_data)

    reviews_data = [
        (1, 'Priya Sharma', 5, 'Best paratha tip! Rolling from center kept all the filling inside. 10/10.'),
        (1, 'Aman Verma', 5, 'Super crispy and delicious breakfast.'),
        (3, 'David Miller', 5, 'Turned out restaurant-style! Kids loved the creamy gravy.')
    ]
    c.executemany("INSERT INTO recipe_reviews (recipe_id, user_name, rating, comment) VALUES (?, ?, ?, ?)", reviews_data)
    conn.commit()

init_standalone_db()

# --- SYNONYM & SPELLCHECK ENGINE ---
SYNONYMS = {
    'potatoes': 'potato', 'aloo': 'potato', 'tomatoes': 'tomato', 'tamatar': 'tomato',
    'onions': 'onion', 'pyaz': 'onion', 'capsicum': 'bell pepper', 'paneer': 'paneer',
    'chawal': 'rice', 'atta': 'wheat flour', 'besan': 'gram flour', 'dahi': 'yogurt',
    'anda': 'egg', 'eggs': 'egg', 'dosa': 'dosa batter', 'sooji': 'semolina', 'rava': 'semolina'
}

VOCAB = [
    'potato', 'onion', 'tomato', 'green chilli', 'garlic', 'rice', 'wheat flour',
    'bread', 'egg', 'chicken', 'paneer', 'butter', 'ghee', 'flattened rice',
    'semolina', 'toor dal', 'chana', 'spinach', 'cauliflower', 'pea', 'peanut'
]

def clean_ingredient(name):
    if not name: return ""
    norm = name.lower().strip()
    return SYNONYMS.get(norm, norm)

def find_spelling_suggestion(word):
    if not word or len(word) < 3: return None
    w = word.lower().strip()
    if w in VOCAB or w in SYNONYMS: return None
    matches = difflib.get_close_matches(w, VOCAB, n=1, cutoff=0.55)
    return matches[0].title() if matches else None

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1556910103-1c02745aae4d?auto=format&fit=crop&w=400&q=80", use_container_width=True)
    st.title("🍳 Filter Options")
    lang = st.selectbox("🌐 Language", ["English", "हिंदी (Hindi)", "Hinglish"])
    
    st.divider()
    food_type = st.radio("Food Type", ["All", "Vegetarian", "Non-Vegetarian", "Vegan"])
    cuisine = st.selectbox("Cuisine", ["All", "North Indian", "South Indian", "Indo-Chinese", "Street Food", "Continental"])
    meal_type = st.selectbox("Meal Time", ["All", "Breakfast", "Lunch/Dinner", "Snacks"])
    max_time = st.selectbox("Max Cooking Time", ["Any", "15", "30", "45", "60"])
    difficulty = st.selectbox("Difficulty", ["Any", "Easy", "Medium", "Hard"])
    spice_level = st.radio("Spice Level", ["Any", "Mild", "Medium", "Spicy"], horizontal=True)
    leftover_mode = st.checkbox("♻️ Leftover Hero Mode", value=False)

# --- MAIN UI ---
st.title("🍳 What Can I Cook Today?")
st.write("Enter the ingredients you already have at home to discover instant, personalized recipes.")

common_picks = ["potato", "onion", "tomato", "green chilli", "garlic", "rice", "wheat flour", "bread", "egg", "chicken", "paneer"]
c1, c2 = st.columns([3, 1])
with c1:
    selected = st.multiselect("Select ingredients you have:", common_picks, default=["potato", "onion"])
with c2:
    custom = st.text_input("Or type another item:", placeholder="e.g. tamato, dahi")

# Typo spellcheck feedback
if custom:
    sug = find_spelling_suggestion(custom)
    if sug:
        st.warning(f"💡 Did you mean: **{sug}**?")
        if st.button(f"Add '{sug}'"):
            selected.append(sug.lower())
            st.rerun()
    else:
        cleaned = clean_ingredient(custom)
        if cleaned not in selected:
            selected.append(cleaned)

# --- RECIPE MATCHING ALGORITHM ---
if st.button("Find What I Can Cook! 🔍", use_container_width=True) or selected:
    user_ings = set([clean_ingredient(x) for x in selected])
    
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM recipes")
    all_recipes = [dict(r) for r in c.fetchall()]
    
    matched_results = []
    other_suggestions = []

    for r in all_recipes:
        # Filter checks
        if food_type != "All" and r['food_type'] != food_type: continue
        if cuisine != "All" and r['cuisine'] != cuisine: continue
        if meal_type != "All" and meal_type not in r['meal_type']: continue
        if max_time != "Any" and (r['preparation_time'] + r['cooking_time']) > int(max_time): continue
        if difficulty != "Any" and r['difficulty_level'] != difficulty: continue
        if spice_level != "Any" and r['spice_level'] != spice_level: continue
        if leftover_mode and not r['is_leftover_friendly']: continue

        # Fetch recipe ingredients
        c.execute("SELECT ingredient_name FROM recipe_ingredients WHERE recipe_id = ?", (r['id'],))
        r_ings = set([clean_ingredient(row[0]) for row in c.fetchall()])

        matched = user_ings.intersection(r_ings)
        missing = r_ings.difference(user_ings)

        # Status badge (NO PERCENTAGE - Requirement 4)
        if leftover_mode:
            badge = "Leftover Hero"
        elif len(missing) == 0:
            badge = "Pantry Ready"
        elif len(missing) == 1:
            badge = "1 Item Needed"
        else:
            badge = "Few Items Needed"

        item = {**r, 'matched': len(matched), 'missing': len(missing), 'badge': badge}

        if len(user_ings) == 0 or len(matched) > 0:
            matched_results.append(item)
        else:
            other_suggestions.append(item)

    matched_results.sort(key=lambda x: (-x['matched'], x['missing']))

    st.subheader(f"Found {len(matched_results)} Delicious Recipes")

    # Render Cards in 2 columns
    for i in range(0, len(matched_results), 2):
        cols = st.columns(2)
        for j in range(2):
            idx = i + j
            if idx < len(matched_results):
                rec = matched_results[idx]
                with cols[j]:
                    with st.container(border=True):
                        st.image(rec['image_url'], use_container_width=True)
                        st.write(f"**{rec['name']}** • ⭐ {rec['rating']} ({rec['review_count']} reviews)")
                        st.caption(f"📍 {rec['cuisine']} • ⏱️ {rec['cooking_time']} mins • 📊 {rec['difficulty_level']}")
                        st.write(rec['description'])
                        
                        # Expandable recipe details
                        with st.expander("📖 View Recipe, Utensils & Steps"):
                            st.markdown("#### 🥣 Required Ingredients:")
                            c.execute("SELECT ingredient_name, quantity, unit FROM recipe_ingredients WHERE recipe_id = ?", (rec['id'],))
                            for ing in c.fetchall():
                                has = clean_ingredient(ing[0]) in user_ings
                                icon = "✅" if has else "❌"
                                st.write(f"{icon} **{ing[0].title()}**: {ing[1]} {ing[2]}")
                                if not has:
                                    c.execute("SELECT substitute_name, note FROM ingredient_substitutes WHERE ingredient_name = ?", (clean_ingredient(ing[0]),))
                                    sub = c.fetchone()
                                    if sub:
                                        st.caption(f"↳ *Substitute:* Use **{sub[0].title()}** ({sub[1]})")

                            if rec['utensils']:
                                st.markdown("#### 🍳 Utensils Needed:")
                                u_list = json.loads(rec['utensils']) if rec['utensils'].startswith('[') else []
                                st.write(", ".join([f"🔪 {u}" for u in u_list]))

                            st.markdown("#### 📝 Step-by-Step Instructions:")
                            c.execute("SELECT step_number, instruction, heat_level, duration, pro_tip FROM cooking_steps WHERE recipe_id = ? ORDER BY step_number", (rec['id'],))
                            steps = c.fetchall()
                            if steps:
                                for s in steps:
                                    st.write(f"**Step {s[0]}:** [{s[2]} • {s[3]}] {s[1]}")
                                    if s[4]: st.caption(f"💡 *Tip:* {s[4]}")
                            else:
                                st.write("Cook over medium heat until tender and fragrant. Garnish with fresh herbs and serve warm.")
    conn.close()

# Footer
st.divider()
st.info("🌱 **Mission:** Smart Recipe Generator turns pantry items into meals to help prevent household food waste.")
