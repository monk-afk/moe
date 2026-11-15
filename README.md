# møe

A Discord chatbot powered by DialoGPT, a pre-trained language model tailored for casual conversation.

<img decoding="async" loading="lazy" alt="moe banner red and white pixelated letters" src="https://raw.githubusercontent.com/monk-afk/moe/main/images/moe_banner_v3_680x240.png"  width="340"/>

møe's official home is at the SquareOne Discord:

[![](https://dcbadge.limes.pink/api/server/pE4Tu3cf23)](https://discord.gg/pE4Tu3cf23)

**[Terms of Service](Terms_of_Service.md)**

**[Privacy Policy](Privacy_Policy.md)**

___

## Features

- Casual conversational AI powered by [Microsoft DialoGPT](https://huggingface.co/microsoft/DialoGPT-medium) through Hugging Face Transformers - [generation docs](https://huggingface.co/docs/transformers/v4.49.0/en/main_classes/text_generation#transformers.GenerationConfig)

- Response triggers: "moe", "@møe", "doot", and "bot"

- Maintains a short channel context from eligible messages without generating a response until triggered

- Designated reply channel allows møe to respond freely in a selected channel

- Replying directly to møe's message keeps a separate reply context and sends the response as a Discord reply

- Recent context is limited to 12 messages or 100 model tokens and is encrypted at rest


___

## Installation

- Memory Requirements:
  - 6GB RAM
  - 5GB Disk

- [Install Script](install.sh)
  - Requires Linux Bash

- Python3 (3.9 or higher; tested with 3.11)
  - python3-venv (Python Virtual Environment)
  - python3-pip (Python Package Installer):
    - transformers (Loads and runs DialoGPT)
    - torch (Model inference)
    - cryptography (Encrypted data storage)
    - wheel (Replaces pip-deprecated setup.py)
    - py-dotenv (Environment Variables)
    - discord.py (version 2.5.0 or higher)

### Discord Configuration

Enable the **Server Members Intent** and **Message Content Intent** for the application in the Discord Developer Portal.

___

## Commands

The command prefix default is `m1`, as set in the .env file.

> `command`(privilege): details of command

- `help`(send_messages): list all commands
- `source`(send_messages): get the link to møe's repository
- `squareone`(send_messages): get the invite link to møe's home Discord server
- `ping`(send_messages): test latency
- `time`(send_messages): show server and local time
- `forgetme`(send_messages): erase your reply-specific conversation memory

- `forgetuser @mention_member`(manage_messages): erase reply-specific memory associated with the mentioned user
- `setreplychannel`(administrator): set the current channel as the designated reply channel
- `unsetreplychannel`(administrator): unset reply channel
- `ignore @mention_member`(administrator): prevent møe from processing the mentioned user's messages
- `dontignore @mention_member`(administrator): remove the mentioned user from the ignore list
- `forgetguild`(administrator): erase conversation memory for the guild while preserving its settings
- `resetguild`(administrator): erase conversation memory and settings for the guild

- `rebuild`(owner): erase and rebuild the encrypted data file
- `reload [cog name]`(owner): reload a cog module
- `shutdown`(owner): save data and gracefully stop møe

___

Copyright © 2024-2026 monk <https://github.com/monk-afk>
