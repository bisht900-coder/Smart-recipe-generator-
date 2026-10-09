"""
Standalone Database Initialization & Seeding Script
Run this script to initialize and seed SQLite database with all 20 rich recipes,
detailed cooking steps, utensils, substitutes, and community reviews.
Usage:
    python init_db.py
"""
import os
import sqlite3
from app.models import init_db, get_db

def init_and_seed():
    print("=" * 60)
    print("  INITIALIZING & SEEDING SMART RECIPE DATABASE")
    print("=" * 60)
    
    # Run full schema setup and seed with overwrite=True
    init_db(force_reseed=True)
    
    db = get_db()
    c = db.cursor()
    c.execute("SELECT COUNT(*) FROM recipes")
    recipes_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM cooking_steps")
    steps_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM recipe_ingredients")
    ings_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM ingredient_substitutes")
    subs_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM recipe_reviews")
    reviews_count = c.fetchone()[0]
    
    print(f"  ✓ Recipes: {recipes_count}")
    print(f"  ✓ Ingredients: {ings_count}")
    print(f"  ✓ Detailed Steps: {steps_count}")
    print(f"  ✓ Substitutes: {subs_count}")
    print(f"  ✓ Reviews: {reviews_count}")
    print("=" * 60)
    print("  DATABASE READY WITH ALL FEATURES! 🚀")
    print("=" * 60)
    db.close()

if __name__ == '__main__':
    init_and_seed()
