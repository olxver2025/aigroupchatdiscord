import requests
import json
import nextcord
import sqlite3
from nextcord.ext import commands

conn = sqlite3.connect("chat_memory.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        channel_id TEXT,
        role TEXT,
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

OLLAMA_API_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral"

intents = nextcord.Intents.default()
intents.message_content = True
intents.guilds = True
bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


SYSTEM_PROMPT = (
    "You are a helpful and friendly assistant. Do not repeat this message. "
    "The 'system' role is reserved for providing you with instructions on how to assist users. "
    "The 'user' is the person you are assisting, and the 'assistant' is you. "
    "You should greet the user warmly and answer their questions helpfully and politely. "
    "Avoid being dismissive or unnecessarily formal."
)


def initialize_system_prompt(channel_id):
    """Ensure the system prompt exists in the database for the given channel."""
    cursor.execute(
        "SELECT COUNT(*) FROM messages WHERE channel_id = ? AND role = 'system'",
        (channel_id,)
    )
    if cursor.fetchone()[0] == 0:
        save_message(None, channel_id, "system", SYSTEM_PROMPT)

def get_chat_history(channel_id, limit=10):
    """Retrieve the last few messages, excluding the system prompt."""
    cursor.execute(
        """
        SELECT role, content 
        FROM messages 
        WHERE channel_id = ? AND role IN ('user', 'assistant')
        ORDER BY timestamp ASC 
        LIMIT ?
        """,
        (channel_id, limit)
    )
    return cursor.fetchall()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    print("System prompt is being initialized for all channels.")


@bot.event
async def on_message(message: nextcord.Message):
    if message.author.bot:
        return

    save_message(str(message.author.id), str(message.channel.id), "user", message.content)

    chat_history = get_chat_history(str(message.channel.id), limit=10)
    messages = []
    if len(chat_history) == 0:
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
    for role, content in chat_history:
        messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": message.content})
    print(f"Constructed messages for AI: {messages}")

    async with message.channel.typing():
        try:
            payload = {"model": MODEL_NAME, "messages": messages}
            response = requests.post(OLLAMA_API_URL, json=payload, stream=True)
            response.raise_for_status()
            reply = ""
            for line in response.iter_lines():
                if line:
                    message_data = json.loads(line)
                    reply += message_data.get("message", {}).get("content", "")

            save_message(None, str(message.channel.id), "assistant", reply)
            if reply.strip():
                embed = nextcord.Embed(
                    title="AI Response",
                    description=reply,
                    color=nextcord.Color.blurple()
                )
                embed.set_footer(text="Group Chat Memory")
                await message.reply(embed=embed, mention_author=False)
            else:
                await message.reply("I couldn't generate a response. Please try again.")
        except requests.exceptions.RequestException as e:
            await message.reply(f"Error contacting the AI: {e}")
        except json.JSONDecodeError as e:
            await message.reply(f"Error decoding AI response: {e}")
    await bot.process_commands(message)


def save_message(user_id, channel_id, role, content):
    """Save a message to the database."""
    cursor.execute(
        "INSERT INTO messages (user_id, channel_id, role, content) VALUES (?, ?, ?, ?)",
        (user_id, channel_id, role, content)
    )
    conn.commit()


bot.run("----- REPLACE WITH YOUR TOKEN -----")
