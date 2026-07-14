from database import (
    add_ingredient, get_pantry, remove_ingredient,
    clear_pantry, save_preference, get_preferences,
    save_to_history, get_history
)

def tool_add_ingredients(ingredients: list):
    """Add ingredients to pantry"""
    added = []
    for item in ingredients:
        if add_ingredient(item):
            added.append(item)
    return f"✅ Added to pantry: {', '.join(added)}"

def tool_get_pantry():
    """Get all ingredients in pantry"""
    items = get_pantry()
    if not items:
        return "🛒 Your pantry is empty! Add some ingredients first."
    ingredient_list = [f"• {item[0]}" + (f" ({item[1]})" if item[1] else "") for item in items]
    return "🧺 Your pantry:\n" + "\n".join(ingredient_list)

def tool_remove_ingredient(ingredient: str):
    """Remove an ingredient from pantry"""
    remove_ingredient(ingredient)
    return f"🗑️ Removed {ingredient} from pantry."

def tool_clear_pantry():
    """Clear all ingredients from pantry"""
    clear_pantry()
    return "🧹 Pantry cleared!"

def tool_check_missing_ingredients(recipe_ingredients: list):
    """Check which ingredients are missing for a recipe"""
    pantry = [item[0].lower() for item in get_pantry()]
    missing = []
    available = []
    for ingredient in recipe_ingredients:
        if ingredient.lower() in pantry:
            available.append(ingredient)
        else:
            missing.append(ingredient)
    
    result = ""
    if available:
        result += f"✅ You have: {', '.join(available)}\n"
    if missing:
        result += f"❌ Missing: {', '.join(missing)}"
    return result if result else "All ingredients checked!"

def tool_generate_shopping_list(missing_ingredients: list):
    """Generate a shopping list from missing ingredients"""
    if not missing_ingredients:
        return "🎉 You have everything you need!"
    shopping_list = "\n".join([f"• {item}" for item in missing_ingredients])
    return f"🛒 Shopping List:\n{shopping_list}"

def tool_save_preference(preference_type: str, value: str):
    """Save user dietary preference"""
    save_preference(preference_type, value)
    return f"✅ Saved preference: {preference_type} → {value}"

def tool_get_preferences():
    """Get all saved preferences"""
    prefs = get_preferences()
    if not prefs:
        return "No preferences saved yet."
    pref_list = [f"• {p[0]}: {p[1]}" for p in prefs]
    return "⚙️ Your preferences:\n" + "\n".join(pref_list)

def tool_save_to_history(recipe_name: str, ingredients_used: str):
    """Save a recipe to history"""
    save_to_history(recipe_name, ingredients_used)
    return f"📖 Saved {recipe_name} to history!"

def tool_get_history():
    """Get recipe history"""
    history = get_history()
    if not history:
        return "No recipe history yet."
    history_list = [f"• {h[0]} — {h[2][:10]}" for h in history]
    return "📖 Recent recipes:\n" + "\n".join(history_list)

def tool_clear_history():
    """Clear all recipe history"""
    from database import clear_history
    clear_history()
    return "🧹 Recipe history cleared!"

# Tool definitions for Gemini API
TOOL_DEFINITIONS = [
    {
        "name": "add_ingredients",
        "description": "Add one or more ingredients to the user's pantry",
        "parameters": {
            "type": "object",
            "properties": {
                "ingredients": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of ingredients to add"
                }
            },
            "required": ["ingredients"]
        }
    },
    {
        "name": "get_pantry",
        "description": "Get all ingredients currently in the user's pantry",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "remove_ingredient",
        "description": "Remove an ingredient from the pantry",
        "parameters": {
            "type": "object",
            "properties": {
                "ingredient": {
                    "type": "string",
                    "description": "Ingredient to remove"
                }
            },
            "required": ["ingredient"]
        }
    },
    {
        "name": "clear_pantry",
        "description": "Clear all ingredients from the pantry",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "check_missing_ingredients",
        "description": "Check which ingredients are missing for a specific recipe",
        "parameters": {
            "type": "object",
            "properties": {
                "recipe_ingredients": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of ingredients needed for the recipe"
                }
            },
            "required": ["recipe_ingredients"]
        }
    },
    {
        "name": "generate_shopping_list",
        "description": "Generate a shopping list from missing ingredients",
        "parameters": {
            "type": "object",
            "properties": {
                "missing_ingredients": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of missing ingredients"
                }
            },
            "required": ["missing_ingredients"]
        }
    },
    {
        "name": "save_preference",
        "description": "Save a dietary preference or cuisine preference for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "preference_type": {
                    "type": "string",
                    "description": "Type of preference e.g. dietary, cuisine, skill_level"
                },
                "value": {
                    "type": "string",
                    "description": "Value of the preference e.g. vegan, Italian, beginner"
                }
            },
            "required": ["preference_type", "value"]
        }
    },
    {
        "name": "get_preferences",
        "description": "Get all saved user preferences",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "save_to_history",
        "description": "Save a recipe to the user's history",
        "parameters": {
            "type": "object",
            "properties": {
                "recipe_name": {
                    "type": "string",
                    "description": "Name of the recipe"
                },
                "ingredients_used": {
                    "type": "string",
                    "description": "Comma separated list of ingredients used"
                }
            },
            "required": ["recipe_name", "ingredients_used"]
        }
    },
    {
        "name": "get_history",
        "description": "Get the user's recipe history",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
    ,{
        "name": "clear_history",
        "description": "Clear all recipe history",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]

def execute_tool(tool_name: str, tool_args: dict):
    """Execute a tool by name with given arguments"""
    if tool_name == "add_ingredients":
        return tool_add_ingredients(tool_args.get("ingredients", []))
    elif tool_name == "get_pantry":
        return tool_get_pantry()
    elif tool_name == "remove_ingredient":
        return tool_remove_ingredient(tool_args.get("ingredient", ""))
    elif tool_name == "clear_pantry":
        return tool_clear_pantry()
    elif tool_name == "check_missing_ingredients":
        return tool_check_missing_ingredients(tool_args.get("recipe_ingredients", []))
    elif tool_name == "generate_shopping_list":
        return tool_generate_shopping_list(tool_args.get("missing_ingredients", []))
    elif tool_name == "save_preference":
        return tool_save_preference(tool_args.get("preference_type", ""), tool_args.get("value", ""))
    elif tool_name == "get_preferences":
        return tool_get_preferences()
    elif tool_name == "save_to_history":
        return tool_save_to_history(tool_args.get("recipe_name", ""), tool_args.get("ingredients_used", ""))
    elif tool_name == "get_history":
        return tool_get_history()
    elif tool_name == "clear_history":
        return tool_clear_history()
    else:
        return f"Unknown tool: {tool_name}"