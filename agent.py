from groq import Groq
import os
import json
from dotenv import load_dotenv
from database import init_db
from tools import TOOL_DEFINITIONS, execute_tool
import streamlit as st

load_dotenv()

api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", None)
client = Groq(api_key=api_key)
MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """
You are a smart Recipe Suggester Agent. You help users:
1. Manage their pantry (add/remove ingredients)
2. Suggest recipes based on available ingredients
3. Check missing ingredients for recipes
4. Generate shopping lists
5. Remember dietary preferences and cuisine choices
6. Track recipe history

Always:
- Use tools to manage pantry and preferences
- Suggest creative recipes based on what the user has
- Be friendly and encouraging
- When suggesting recipes, mention which ingredients they have and which are missing
- Save recipes to history when user shows interest
- Consider user's saved preferences when suggesting recipes

When user adds ingredients, always confirm by calling add_ingredients tool.
When user asks for recipes, first check pantry using get_pantry tool, then suggest recipes.
"""

def build_groq_tools():
    """Convert tool definitions to Groq format"""
    groq_tools = []
    for tool in TOOL_DEFINITIONS:
        groq_tools.append({
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool.get("parameters", {})
            }
        })
    return groq_tools

def init_agent():
    """Initialize database"""
    init_db()
    return client

def chat(model, history, user_message):
    """Send a message and get response"""

    history.append({
        "role": "user",
        "content": user_message
    })

    tools = build_groq_tools()

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
            tools=tools,
            tool_choice="auto",
            max_tokens=2048
        )

        message = response.choices[0].message
        assistant_message = {
            "role": "assistant",
            "content": message.content or "",
        }
        if message.tool_calls:
            assistant_message["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in message.tool_calls
            ]
        history.append(assistant_message)

        if not message.tool_calls:
            return message.content, history

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            print(f"🔧 Tool: {tool_name} | Args: {tool_args}")
            result = execute_tool(tool_name, tool_args)
            print(f"✅ Result: {result}")

            history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

if __name__ == "__main__":
    print("🍳 Recipe Suggester Agent")
    print("=" * 40)
    print("Type 'quit' to exit")
    print("=" * 40)

    init_agent()
    history = []

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ["quit", "exit", "bye"]:
            print("👋 Goodbye! Happy cooking!")
            break

        if not user_input:
            continue

        try:
            response, history = chat(None, history, user_input)
            print(f"\n🤖 Agent: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")