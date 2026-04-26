# Zhaba

A Discord bot for managing reaction-role panels per channel.

This project lets server administrators:
- create reaction-role entries in a specific text channel
- generate a reaction-role embed panel for that channel
- set a separate embed color for each channel
- remove entries by role or emoji
- clear messages in the current channel

## Features

- Slash commands only
- Per-channel reaction-role configuration
- Per-channel embed color settings
- SQLite storage
- Automatic reaction-role assignment and removal
- Console-only custom logging
- Minimal modular architecture with `cogs`, repository, services, and validators

## Requirements

- Python 3.11+ recommended
- A Discord bot token

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your_bot_token_here
```

3. Start the bot:

```bash
python bot.py
```

## Commands

The bot currently provides these slash commands:

- `/add_role` - Add a reaction role in the current channel
- `/delete_role` - Delete a reaction role from the current channel
- `/color` - Set the embed color for the current channel's reaction-role panel
- `/roles` - Create the reaction-role panel in the current channel
- `/clear` - Delete messages in the current channel

## How It Works

Each text channel can have its own:
- reaction-role entries
- panel message
- embed color

When a user adds a reaction to the generated panel message, the bot gives the linked role. When the reaction is removed, the bot removes that role.

## Project Structure

```text
.
├── bot.py
├── requirements.txt
├── reaction_roles.db
└── app/
    ├── bot.py
    ├── config.py
    ├── database.py
    ├── logging_config.py
    ├── repository.py
    ├── responses.py
    ├── services.py
    ├── validators.py
    └── cogs/
        ├── admin.py
        └── reactions.py
```

## Data Storage

The bot uses SQLite and stores data in:

- `reaction_roles.db`

The database includes:
- reaction-role mappings
- panel message references
- per-channel embed color settings

## Logging

The project uses its own logger and disables `discord.py` logging noise.

- Application logs are printed to the console
- Logs are not written to a file

## Notes

- The bot syncs slash commands on startup
- A forced command cache reset is performed during startup before syncing commands
- The bot must have permissions to manage roles, read message history, add reactions, and manage messages where relevant

## License

No license file is included in this repository by default.
