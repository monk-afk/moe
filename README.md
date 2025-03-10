# møe

A Discord chatbot equipped with DialoGTP; a pre-trained language model tailored for casual conversation.

<img decoding="async" loading="lazy" alt="moe banner red and white pixelated letters" src="https://raw.githubusercontent.com/monk-afk/moe/main/images/moe_banner_v3_680x240.png"  width="340"/>

møe's official home is at the SquareOne Discord:

[![](https://dcbadge.limes.pink/api/server/pE4Tu3cf23)](https://discord.gg/pE4Tu3cf23)

___

## Features

- Casual Conversational AI Language Model, Powered by [DialoGPT, courtesy of Huggingface](https://huggingface.co/docs/transformers/main/en/model_doc/dialogpt) - [docs](https://huggingface.co/docs/transformers/v4.49.0/en/main_classes/text_generation#transformers.GenerationConfig)

- Response triggers: "moe", "bot", "monk", "molo"

- Designated Reply-to Channel allows møe to reply freely with guild Members

- Always-reply-to enables møe to always respond to specified Users in any channel

___

## Installation

- Memory Requirements:
  - 6GB RAM
  - 5GB Disk

- [Install Script](install.sh)
  - Requires Linux Bash

- Python3 (3.8 or higher. tested with 3.11)
  - python3-venv (Python Virtual Environment)
  - python3-pip (Python Package Installer):
    - transformers (Provides HuggingFace AI Model)
    - torch (Message tensor encoding)
    - wheel (Replaces pip-deprecated setup.py)
    - py-dotenv (Environment Variables)
    - discord.py (version 2.5.0 or higher)

___

## Commands

The command prefix default is `m1`, as set in the .env file.

> `command`(privilege): deatils of command

- `chatlogs`(send_messages): show your conversation history
- `forgetme`(send_messages): erase møe's memory of your conversation
- `ping`(send_messages): test latency
- `help`(send_messages): list all commands
- `source`(send_messages): get the link to møe's repository
- `squareone`(send_messages): get the invite link to møe's home Discord server

- `forgetuser @mention_member`(manage_messages): erase møe's memory of the mentioned user
- `setreplychannel`(administrator): set or overwrite reply channel to focused channel
- `unsetreplychannel`(administrator): unset reply channel
- `sayhi @mention`(administrator): set reply-to user in any channel
- `saybye @mention`(administrator): remove reply-to user
- `forgetguild`(administrator): erase møe's conversation memory for the entire guild

- `rebuild`(owner): rebuild the database
- `reload [cogs name]`(owner): reload a cogs module
- `shutdown`(owner): send the shutdown signal for graceful termination
- `dumpbackend`(owner): dump the raw memory to debug.txt

___

## Troubleshoot

- ToDo

___

**[Changelog](CHANGELOG.md)**

**[Terms of Service](Terms_of_Service.md)**

**[Privacy Policy](Privacy_Policy.md)**

___

```py
######################################################################################
##  MIT License                                                                     ##
##                                                                                  ##
##  Copyright © 2024-2025 monk (Discord ID: 699370563235479624)                     ##
##                                                                                  ##
##  Permission is hereby granted, free of charge, to any person obtaining a copy    ##
##  of this software and associated documentation files (the "Software"), to deal   ##
##  in the Software without restriction, including without limitation the rights    ##
##  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell       ##
##  copies of the Software, and to permit persons to whom the Software is           ##
##  furnished to do so, subject to the following conditions:                        ##
##                                                                                  ##
##  The above copyright notice and this permission notice shall be included in all  ##
##  copies or substantial portions of the Software.                                 ##
##                                                                                  ##
##  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR      ##
##  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,        ##
##  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE     ##
##  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER          ##
##  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,   ##
##  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE   ##
##  SOFTWARE.                                                                       ##
######################################################################################
```