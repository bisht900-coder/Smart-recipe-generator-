# 🍳 Smart Recipe Generator – Your AI-Powered Cooking Assistant

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask Version](https://img.shields.io/badge/flask-2.3%2B-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Database](https://img.shields.io/badge/database-SQLite3-lightgrey.svg)](https://www.sqlite.org/)
[![UI](https://img.shields.io/badge/UI-Responsive%20HTML5%2FCSS3-orange.svg)](#)

> Discover delicious recipes using ingredients you already have at home, minimize food waste, find instant smart ingredient substitutes, and cook effortlessly!

---

## 📖 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [API Endpoints](#-api-endpoints)
- [Recipe Matching Algorithm](#-recipe-matching-algorithm)
- [Sample Recipes Included](#-sample-recipes-included)
- [UI & Screenshots](#-ui--screenshots)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

**Smart Recipe Generator** is a modern full-stack web application that solves the universal daily question: *"What should I cook with what's in my fridge?"* 

Instead of browsing through hundreds of recipes only to find out you're missing key ingredients, **Smart Recipe Generator** inverts the process. Input the ingredients sitting on your counter or in your refrigerator, apply dietary and time filters, and let the smart matching algorithm calculate match percentages, recommend suitable dishes, and provide culinary substitutes for missing items. 

Whether you're looking to cook a gourmet dinner, make a quick 15-minute lunch, or find creative ways to repurpose leftovers, Smart Recipe Generator is your ultimate kitchen companion.

---

## ✨ Features

- 🔍 **Smart Ingredient-Based Search:** Enter any combination of ingredients (comma-separated or tagged) to find recipes you can make right now.
- 📊 **Match Percentage Scoring:** Precise algorithm calculates the exact percentage of ingredients you possess for every dish.
- 🌶️ **Multi-Criteria Filtering:** Filter search results by:
  - **Food Type:** Vegetarian, Non-Vegetarian, Vegan
  - **Spice Level:** Mild, Medium, Spicy
  - **Difficulty:** Easy, Medium, Hard
  - **Max Cooking Time:** 15m, 30m, 45m, 60m+
- 🔄 **Ingredient Substitute Suggestions:** Never abandon a recipe because of one missing ingredient. The system suggests culinary-approved substitutes (e.g., Greek yogurt for heavy cream, cashew paste for paneer).
- ♻️ **Leftover Mode:** Dedicated mode tailored for utilizing pantry remnants, day-old rice, and leftover veggies to reduce household food waste.
- 🧠 **AI-Inspired Normalization & Synonym Mapping:** Automatically handles culinary variations, plurals, and regional names (e.g., *capsicum* ↔ *bell pepper*, *eggplant* ↔ *brinjal*, *cilantro* ↔ *coriander leaves*).
- ⭐ **Featured Recipe Suggestions:** Rotating recommendations on the homepage to spark cooking inspiration.
- 📝 **Step-by-Step Cooking Instructions:** Clear, chronological recipe walkthroughs with ingredient quantities, preparation time, and cooking time.
- 📱 **Fully Responsive Design:** Seamless user experience across mobile phones, tablets, and desktop workstations.

---

## 🛠️ Tech Stack

| Layer | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla ES6+) | Lightweight, dependency-free responsive interface with modern UI components |
| **Backend** | Python 3.8+, Flask 2.3+ | Fast, modular WSGI application with Blueprints and RESTful API architecture |
| **Database** | SQLite3 | Embedded relational database with automatic table creation and data seeding |
| **Data Processing** | NumPy, Pandas | Optimized array operations, ingredient ranking, and tabular querying |

---

## 📁 Project Structure

```
smart-recipe-generator/
├── run.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── database/
│   └── recipes.db                  # SQLite database (auto-generated on first run)
├── app/
│   ├── __init__.py                 # Flask app factory & blueprint registration
│   ├── config.py                   # Application configurations
│   ├── models.py                   # SQLite schema & database connection helpers
│   ├── seed_data.py                # Initial database seed script (20 recipes & substitutes)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── api.py                  # RESTful API endpoints
│   │   └── views.py                # Frontend page routing
│   ├── services/
│   │   ├── __init__.py
│   │   ├── matching.py             # Match score calculation & ranking logic
│   │   ├── normalizer.py           # Ingredient synonym mapping & string cleaning
│   │   └── substitutes.py          # Ingredient substitution engine
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css           # Modern styles, responsive layout & animations
│   │   └── js/
│   │       └── app.js              # Client-side dynamic interaction & API integration
│   └── templates/
│       ├── base.html               # Shared HTML layout with navigation & footer
│       ├── index.html              # Main dashboard with search, filters & cards
│       └── recipe_detail.html      # Detailed recipe view with steps & ingredient checklist
```

---

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.8** or higher installed on your operating system
- **pip** (Python package installer)
- Git (optional, for cloning)

### Step-by-Step Guide

1. **Clone or download the project repository:**
   ```bash
   git clone https://github.com/your-username/smart-recipe-generator.git
   cd smart-recipe-generator
   ```

2. **Create a virtual environment:**
   - **Windows:**
     ```powershell
     python -m venv venv
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     ```

3. **Activate the virtual environment:**
   - **Windows (Command Prompt):**
     ```cmd
     venv\Scripts\activate
     ```
   - **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install project dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Flask application:**
   ```bash
   python run.py
   ```

6. **Open in your web browser:**
   Navigate to `http://localhost:5000` or `http://127.0.0.1:5000`.

> [!NOTE]
> The SQLite database file (`database/recipes.db`) is automatically initialized and seeded with **20 comprehensive recipes**, ingredient mappings, cooking steps, and culinary substitutes on first launch.

---

## 🔌 API Endpoints

The backend provides a clean RESTful API under the `/api` route prefix.

### 1. Get All Recipes (with optional filters)
- **Method:** `GET`
- **Path:** `/api/recipes`
- **Query Parameters:**
  - `food_type` *(optional, string)*: `Vegetarian`, `Non-Vegetarian`, `Vegan`
  - `spice_level` *(optional, string)*: `Mild`, `Medium`, `Spicy`
  - `difficulty_level` *(optional, string)*: `Easy`, `Medium`, `Hard`
- **Example Request:**
  ```http
  GET /api/recipes?food_type=Vegetarian&spice_level=Medium
  ```
- **Example Response (`200 OK`):**
  ```json
  [
    {
      "id": 1,
      "name": "Paneer Butter Masala",
      "food_type": "Vegetarian",
      "spice_level": "Medium",
      "difficulty_level": "Medium",
      "preparation_time": 15,
      "cooking_time": 25,
      "image_url": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7",
      "description": "Rich and creamy cottage cheese curry cooked in a spiced tomato-butter gravy."
    }
  ]
  ```

---

### 2. Get Recipe Details by ID
- **Method:** `GET`
- **Path:** `/api/recipes/<recipe_id>`
- **Description:** Returns complete recipe data, including required ingredients with units and ordered preparation steps.
- **Example Request:**
  ```http
  GET /api/recipes/1
  ```
- **Example Response (`200 OK`):**
  ```json
  {
    "id": 1,
    "name": "Paneer Butter Masala",
    "food_type": "Vegetarian",
    "spice_level": "Medium",
    "difficulty_level": "Medium",
    "preparation_time": 15,
    "cooking_time": 25,
    "is_leftover_friendly": 0,
    "description": "Rich and creamy cottage cheese curry cooked in a spiced tomato-butter gravy.",
    "ingredients": [
      { "ingredient_name": "paneer", "quantity": "250", "unit": "g", "is_optional": 0 },
      { "ingredient_name": "butter", "quantity": "2", "unit": "tbsp", "is_optional": 0 },
      { "ingredient_name": "tomato", "quantity": "4", "unit": "medium", "is_optional": 0 },
      { "ingredient_name": "cream", "quantity": "3", "unit": "tbsp", "is_optional": 1 }
    ],
    "steps": [
      { "step_number": 1, "instruction": "Blanch tomatoes and blend into a smooth puree." },
      { "step_number": 2, "instruction": "Melt butter in a pan, add aromatic spices and saute the puree." },
      { "step_number": 3, "instruction": "Gently add paneer cubes, stir in cream, and simmer on low heat." }
    ]
  }
  ```

---

### 3. Smart Recipe Recommendations
- **Method:** `POST`
- **Path:** `/api/recommendations`
- **Headers:** `Content-Type: application/json`
- **Description:** Calculates match percentage against user-provided ingredients, filters by dietary preferences, and highlights missing items and substitute recommendations.
- **Example Request Body:**
  ```json
  {
    "ingredients": ["paneer", "tomato", "butter", "garlic", "onion"],
    "preferences": {
      "food_type": "Vegetarian",
      "spice_level": "Medium",
      "max_cooking_time": 45
    }
  }
  ```
- **Example Response (`200 OK`):**
  ```json
  {
    "count": 1,
    "message": "Recipes recommended successfully",
    "results": [
      {
        "recipe": {
          "id": 1,
          "name": "Paneer Butter Masala",
          "food_type": "Vegetarian",
          "spice_level": "Medium",
          "difficulty_level": "Medium",
          "preparation_time": 15,
          "cooking_time": 25,
          "is_leftover_friendly": 0
        },
        "match_score": 83.33,
        "matched_ingredients": ["butter", "garlic", "onion", "paneer", "tomato"],
        "missing_ingredients": ["cream"],
        "substitutes": {
          "cream": [
            {
              "substitute_name": "Greek yogurt",
              "note": "Whisk thoroughly and add on low heat to prevent curdling."
            },
            {
              "substitute_name": "Cashew paste",
              "note": "Blend soaked cashews with warm water for a rich, velvety texture."
            }
          ]
        },
        "total_time": 40,
        "smart_message": "You can prepare this with 83% of available ingredients."
      }
    ]
  }
  ```

---

### 4. Get Ingredient Substitutes
- **Method:** `GET`
- **Path:** `/api/substitutes/<ingredient>`
- **Description:** Queries the substitution directory for alternatives to any missing ingredient.
- **Example Request:**
  ```http
  GET /api/substitutes/cream
  ```
- **Example Response (`200 OK`):**
  ```json
  {
    "ingredient": "cream",
    "substitutes": [
      {
        "substitute_name": "Greek yogurt",
        "note": "Whisk thoroughly and add on low heat to prevent curdling."
      },
      {
        "substitute_name": "Cashew paste",
        "note": "Blend soaked cashews with warm water for a rich, velvety texture."
      },
      {
        "substitute_name": "Coconut milk",
        "note": "Ideal 1:1 substitute for vegan or dairy-free curries."
      }
    ]
  }
  ```

---

### 5. Leftover-Friendly Suggestions
- **Method:** `POST`
- **Path:** `/api/leftover-suggestions`
- **Headers:** `Content-Type: application/json`
- **Description:** Specifically searches for dishes flagged with `is_leftover_friendly = 1` (e.g., stir-fries, khichdi, fried rice) that make optimal use of existing cooked pantry items.
- **Example Request Body:**
  ```json
  {
    "ingredients": ["cooked rice", "egg", "scallion", "soy sauce"],
    "preferences": {
      "food_type": "Non-Vegetarian",
      "max_cooking_time": 25
    }
  }
  ```
- **Example Response (`200 OK`):**
  ```json
  [
    {
      "recipe": {
        "id": 5,
        "name": "Egg Fried Rice",
        "food_type": "Non-Vegetarian",
        "spice_level": "Mild",
        "preparation_time": 5,
        "cooking_time": 10,
        "is_leftover_friendly": 1
      },
      "match_score": 100.0,
      "matched_ingredients": ["cooked rice", "egg", "scallion", "soy sauce"],
      "missing_ingredients": [],
      "substitutes": {},
      "total_time": 15,
      "smart_message": "You have all the ingredients! Let's get cooking!"
    }
  ]
  ```

---

### 6. Get Featured Recipes
- **Method:** `GET`
- **Path:** `/api/featured-recipes`
- **Description:** Returns a randomized selection of featured recipes to display on the landing page showcase.
- **Example Response (`200 OK`):**
  ```json
  [
    {
      "id": 4,
      "name": "Chana Masala",
      "food_type": "Vegetarian",
      "spice_level": "Medium",
      "difficulty_level": "Easy",
      "preparation_time": 10,
      "cooking_time": 20,
      "image_url": "https://images.unsplash.com/photo-1546833999-b9f581a1996d"
    },
    {
      "id": 14,
      "name": "Butter Chicken",
      "food_type": "Non-Vegetarian",
      "spice_level": "Medium",
      "difficulty_level": "Medium",
      "preparation_time": 20,
      "cooking_time": 30,
      "image_url": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398"
    }
  ]
  ```

---

## 🧠 Recipe Matching Algorithm

The recommendation engine powers the heart of the application with a multi-phase matching and scoring pipeline:

```
[User Input Ingredients] 
          │
          ▼
 [Ingredient Normalizer] ──► (Lowercase, trim whitespace, map culinary synonyms)
          │
          ▼
   [Filter Recipes]     ──► (Exclude mismatched food_type, spice_level, max_time)
          │
          ▼
  [Calculate Score]     ──► Match Score = (Matched Ingredients / Total Recipe Ingredients) * 100
          │
          ▼
 [Substitute Lookup]    ──► Retrieve culinary substitutes for missing ingredients
          │
          ▼
  [Rank & Sort Order]   ──► 1. Match Score (DESC)
                            2. Missing Ingredient Count (ASC)
                            3. Total Cooking Time (ASC)
```

### 1. Mathematical Formula
$$\text{Match Score} = \left( \frac{\text{Count of Matched Ingredients}}{\text{Total Ingredients in Recipe}} \right) \times 100$$

### 2. Multi-Tiered Ranking Criteria
Matches are prioritized systematically:
1. **Primary Sort:** `match_score DESC` — Recipes with the highest percentage of ingredients already in your pantry appear first.
2. **Secondary Sort:** `len(missing_ingredients) ASC` — If two recipes have identical match scores, the recipe requiring fewer missing items is given priority.
3. **Tertiary Sort:** `total_time ASC` — Recipes that take less total time (`preparation_time` + `cooking_time`) rank higher to save time in the kitchen.

### 3. Normalization & Synonym Mapping
Ingredients often have multiple regional or colloquial names. The normalizer maps variations to canonical terms before calculating sets:
- `capsicum` $\rightarrow$ `bell pepper`
- `coriander leaves` / `cilantro leaves` $\rightarrow$ `cilantro`
- `eggplant` / `aubergine` $\rightarrow$ `brinjal`
- `garbanzo beans` $\rightarrow$ `chana`
- `cottage cheese` $\rightarrow$ `paneer`
- `lady finger` / `bhindi` $\rightarrow$ `okra`
- `clarified butter` $\rightarrow$ `ghee`
- `scallions` / `spring onion` $\rightarrow$ `scallion`

### 4. Smart Dynamic Feedback
Users receive encouraging, context-aware messages alongside their match score:
- **100% Match:** *"You have all the ingredients! Let's get cooking!"*
- **$\ge$ 80% Match:** *"You can prepare this with X% of available ingredients."*
- **1 Missing Item:** *"You only need one more ingredient!"*
- **Under 20 Minutes:** *"Great choice for a quick X-minute meal!"*

---

## 🍲 Sample Recipes Included

The application comes pre-populated with **20 diverse, authentic recipes**:

| # | Recipe Name | Food Type | Spice Level | Difficulty | Time (Prep + Cook) | Leftover Friendly |
| :-: | :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | **Paneer Butter Masala** | Vegetarian | Medium | Medium | 15 + 25 min | No |
| 2 | **Palak Paneer** | Vegetarian | Mild | Easy | 15 + 20 min | No |
| 3 | **Dal Tadka** | Vegetarian | Medium | Easy | 10 + 20 min | Yes ♻️ |
| 4 | **Chana Masala** | Vegetarian | Spicy | Medium | 15 + 30 min | Yes ♻️ |
| 5 | **Aloo Gobi** | Vegetarian | Medium | Easy | 10 + 20 min | No |
| 6 | **Vegetable Biryani** | Vegetarian | Spicy | Hard | 25 + 35 min | Yes ♻️ |
| 7 | **Bhindi Masala** | Vegetarian | Medium | Easy | 10 + 15 min | No |
| 8 | **Baingan Bharta** | Vegetarian | Spicy | Medium | 15 + 25 min | No |
| 9 | **Masala Khichdi** | Vegetarian | Mild | Easy | 10 + 20 min | Yes ♻️ |
| 10 | **Vegetable Fried Rice** | Vegetarian | Mild | Easy | 10 + 15 min | Yes ♻️ |
| 11 | **Classic Tomato Basil Pasta** | Vegetarian | Mild | Easy | 10 + 15 min | Yes ♻️ |
| 12 | **Vegetable Hakka Noodles** | Vegetarian | Medium | Easy | 15 + 10 min | Yes ♻️ |
| 13 | **Rajma Masala** | Vegetarian | Medium | Medium | 15 + 35 min | Yes ♻️ |
| 14 | **Butter Chicken** | Non-Vegetarian | Medium | Medium | 20 + 30 min | No |
| 15 | **Chicken Tikka Masala** | Non-Vegetarian | Spicy | Medium | 25 + 30 min | No |
| 16 | **Egg Fried Rice** | Non-Vegetarian | Mild | Easy | 5 + 10 min | Yes ♻️ |
| 17 | **Egg Curry (Anda Masala)** | Non-Vegetarian | Medium | Easy | 10 + 20 min | Yes ♻️ |
| 18 | **Garlic Butter Herb Chicken** | Non-Vegetarian | Mild | Easy | 10 + 20 min | No |
| 19 | **Moong Dal Khichdi** | Vegan | Mild | Easy | 10 + 20 min | Yes ♻️ |
| 20 | **Vegetable Tofu Stir-Fry** | Vegan | Mild | Easy | 10 + 15 min | Yes ♻️ |

---

## 📸 UI & Screenshots

You can preview and interact with the full web experience by starting the Flask server and visiting `http://localhost:5000` in any browser:

- **Interactive Search Dashboard:** Tag-based ingredient entry with auto-suggestions, clear buttons, and dynamic filter pills.
- **Recipe Cards:** Featuring high-resolution recipe photos, preparation time, difficulty badges, and match percentage meters.
- **Missing Ingredient & Substitute Drawer:** One-click modal displaying exact substitutes and cooking tips for unavailable ingredients.
- **Detailed Recipe Pages:** Step-by-step cooking steps with interactive checkboxes to track your preparation in real-time.

---

## 🔮 Future Enhancements

- 🤖 **Generative AI Integration:** Connect with OpenAI / Gemini API to dynamically invent unique recipes on the fly for rare ingredient combinations.
- 👤 **User Profiles & Bookmarks:** Save favorite recipes, record personal notes, and keep cooking history.
- 📅 **Weekly Meal Planner:** Drag-and-drop recipe schedule with automated nutritional tracking.
- 📊 **Macro & Calorie Calculator:** Detailed breakdowns for calories, proteins, carbohydrates, and fats per serving.
- 🛒 **Automated Shopping List:** Export missing ingredients directly to a clean checklist or popular grocery delivery carts.
- 🎙️ **Hands-Free Voice Input:** Use Web Speech API to add ingredients while your hands are busy prepping food.

---

## 🤝 Contributing

Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**!

1. **Fork the Project**
2. **Create your Feature Branch:**
   ```bash
   git checkout -b feature/NewFeature
   ```
3. **Commit your Changes:**
   ```bash
   git commit -m "Add NewFeature: ingredient voice recognition"
   ```
4. **Push to the Branch:**
   ```bash
   git push origin feature/NewFeature
   ```
5. **Open a Pull Request**

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

<p align="center">
  Made with ❤️ for home cooks, food lovers, and zero-waste kitchens everywhere.
</p>
