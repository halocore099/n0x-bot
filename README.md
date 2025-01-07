# Discord Bot Project

## Overview
A modular Discord bot built using Discord.py, designed to be extensible and easy to customize.

## Setup and Installation

### Prerequisites
- Python 3.8+
- Discord Bot Token

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/discord-bot.git
cd discord-bot
```

### 2. Dependencies
Create a `requirements.txt` file with the following content:

```text
discord.py==2.3.2
youtube-dl
PyNaCl
propcache
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configuration
Create a `config.json` file in the root directory:

```json
{
    "token": "YOUR_DISCORD_BOT_TOKEN_HERE"
}
```

#### Token Security
- **Never commit `config.json` to version control.**
- Add `config.json` to `.gitignore`.

Create a `.gitignore` file:

```text
config.json
__pycache__/
*.pyc
```

## Project Structure
```text
.
├── main.py           # Bot entry point
├── config.json       # Configuration file (gitignored)
├── cogs/             # Command modules
│   └── ...
└── requirements.txt  # Python dependencies
```

## Bot Functionality
The bot uses a cog-based architecture for modular command management.

### Key Features
- Automatic cog loading
- Flexible command structure
- Easy extensibility

## Running the Bot
```bash
python main.py
```

## Adding New Commands
1. Create a new file in the `cogs/` directory.
2. Define commands using Discord.py's cog system.
3. The bot will automatically load new cogs on restart.

## Security Guidelines
- Keep your bot token confidential.
- Use environment variables in production.
- Regularly rotate your Discord bot token.

## Contributing
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push to the branch.
5. Create a Pull Request.

## Current Commands
Commands are dynamically loaded from `cogs/`.

| Command  | Description             | Usage     |
|----------|-------------------------|-----------|
| `!help`  | Shows available commands| `!help`   |

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
