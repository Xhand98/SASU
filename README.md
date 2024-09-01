# SASU - Discord Bot

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
<a href="https://github.com/psf/black/blob/main/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>

## Table of Contents

- [SASU - Discord Bot](#sasu---discord-bot)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Features](#features)
  - [Installation](#installation)
    - [DB Setup](#dbsetup)
  - [Usage](#usage)
    - [Example Commands](#example-commands)
  - [Commands](#commands)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)

## About

This is a Python-based Discord bot designed to let users manage some aspects of steam from their discord server/discord dm's. The bot is built using the `pycord` library and includes various features to enhance your Discord server experience.

## Features

- [List some key features of the bot]
  - Example: Custom slash commands for user interaction
  - Example: Integration with Steam API for game-related data
  - Example: Database management for persistent user data

## Installation

To install and run the bot, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/Xhand98/SASU .git
   cd your-repo-name
   ```
2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:

   - Create a `.env` file in the project root and add the following variables:
     ```plaintext
     DISCORD_TOKEN=your-discord-bot-token
     STEAM_API_KEY=your-steam-api-key
     ```
5. Run the bot:

   ```bash
   python main.py
   ```

## DbSetup

To setup the database to make the bot work, follow this steps:

1. Run the dbsetup file:
   ``` command line
   python ./db/dbsetup.py
   ```

2. And that's it, go use your favorite database query tool and check it out!

## Usage

Once the bot is running, invite it to your Discord server using the OAuth2 URL generated on the [Discord Developer Portal](https://discord.com/developers/applications).

### Example Commands

- `/setup`: Gets the bot ready for the user to use without .
- `/gethours [steamid]`: Shows the total hours of an user in steam (across all their games).

## Commands

Here’s a list of available commands:

- **/steamprofile [steamid]**: Fetches and displays the Steam profile of a user based on their SteamID.
- **/gameinfo [game]**: Provides detailed information about a specific game from Steam.
- **/topgames**: Lists the top games currently trending on Steam.

*(Add more commands as needed.)*

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions, feedback, or suggestions, feel free to contact me at [hendrickherrera9@gmail.com](mailto:hendrickherrera9@gmail.com).

---

Thank you for using this bot! I hope it enhances your Discord experience.
