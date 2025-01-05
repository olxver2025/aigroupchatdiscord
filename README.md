# AI Discord Group Chat
This is a Python-based Discord bot using the `nextcord` library. The bot maintains a memory of conversations within a SQLite database and integrates with an Ollama model to generate responses on your local machine.

## Features

- AI-Powered Responses: The bot uses Ollama to respond to user messages in a friendly and helpful manner.
- Group Chat Memory: Chat history is stored in a SQLite database, allowing the bot to consider recent messages when generating responses.
- Customizable System Prompt: A predefined system prompt ensures the bot remains helpful and consistent.

## Requirements

- Python 3.8 or higher
- `nextcord` library
- `requests` library
- A local SQLite database (`chat_memory.db`)
- Ollama model downloaded and running (Mistral is an example, but you can use any model you please)

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/olxver2025/aigroupchatdiscord.git
   ```

2. Install dependencies:

   ```
   pip install nextcord requests
   ```
3. Download and setup Ollama at https://ollama.ai

4. Configure your bot token by replacing the token in `bot.run()` with your own Discord bot token.

5. Run the bot:

   ```
   python bot.py
   ```

## Usage

- Invite your bot to a Discord server.
- Send messages in a channel where the bot is active, and it will respond using the AI.
- Chat history is saved automatically to provide context for future interactions.

## Database

The bot uses an SQLite database (`chat_memory.db`) to store messages. The database schema includes:

- `id`: Primary key for the message.
- `user_id`: ID of the user who sent the message.
- `channel_id`: ID of the channel where the message was sent.
- `role`: Role of the sender (`user`, `assistant`, or `system`).
- `content`: The content of the message.
- `timestamp`: Timestamp when the message was saved.

## Contributing

Feel free to fork this repository and submit pull requests. Suggestions and contributions are welcome.

## License

This project is licensed under the MIT License.


## Note

Some models may hallucinate or read out the system prompt. I can not do anything about this, but if you feel like you can help please submit a pull request.

## Example
![image](https://github.com/user-attachments/assets/56d05c8a-e21d-4e9f-b346-f3ca9a7477ea)
Here's an image showing the bot working in Discord. The bot recalls me saying 'hello' earlier and brings it up. `(This is using llama3.2:3b)`
