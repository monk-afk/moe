# Changelog

#### 0.2.0

[0.2.0] - 2025-03-10
  - Removed PostgreSQL dependency
  - Implement storage using JSON file
  - Fixed trying to fetch_application_emoji from non-existent emoji
  - Refuse sending empty messages
  - Save to file on shutdown
  - Update `install.sh`
    - Creates `run_bot.sh`
  - Cleaned up all the files
  - Add commands:
    - `shutdown` to softly put moe to sleep
    - `chatlogs` to give the user their decoded chat history
    - `dumpbackend` to dump raw memory to logs for debugging
  - Move model and tokenizer into own untils file
  - Tweak response generation parameters slightly
  - Initialize from bot.py instead of init.py
  - Drop user chat history on leave guild event

___
___

#### 0.1.0

[0.1.1] - 2025-03-03
  - Fix typing indicator appearing after message is sent
    - Added a slight random delay before typing
    - Fallback method included in comment
  - Remove leftover import transformers statement
  - Move command prefix check before assigning variables
  - Adjusted token limits:
    - Maximum 30 words from new messages
    - Truncate old messages to 100 tokens or 12 EOS tokens
  - Adjust output generate parameters for better responses
  - Add no_repeat_ngram_size parameter
  - Append model's output to the user's token history

[0.1.0] - 2025-03-01
  - Update to **[Privacy Policy](docs/Privacy_Policy.md)**
  - Remove per-channel and introduce per-user conversation history
  - Command for users to delete their conversation history with the Chatbot
  - Bot owner command to **rebuild database with new schema** (use: `rebuild`)
  - Restructure database table schematic to support per-user context
  - Move log capturing from logroll.py to module files and increase log events
  - DialoGPT Model now loads from `utils/model_loader.py`
  - Adjust default model generate parameters
  - Reduce install steps outlined in install.sh
    - Leave shared memory buffer to default
    - No creating database test user
    - discord.py 2.5.0 is now provided through pip
  - Fix crash when running `reload chat` [#10](https://github.com/monk-afk/moe/issues/10)
  - Fix crash caused by receiving direct messages
  - Fix reply-to-user guild restrictions [#9](https://github.com/monk-afk/moe/issues/9)

___
___

#### 0.0.0

0.0.11 - 2024-11-16
  - Truncate user input exceeding 100 words
  - Limit input tokens by number eos token or input tokens, whichever hits the limit first

0.0.10 - Oct 9, 2024
  - Add command to reload cogs
  - Channel context tokens are actively updated instead of per reply

0.0.9
  - Add Reaction emoji to messages with matching pattern

0.0.8
  - Command prefix is now in the .env file
  - Add reply-to command

0.0.7
  - Tidy reply conditional
  - ~~Add reply referencing~~ rolled back

0.0.6
  - Fix typing indicator bug

0.0.5
  - Properly formatted help message
  - Fix typing indicator bug
  - Fix errors on Guild removal

0.0.4
  - Ignore direct messages
  - bugfix trailing eos token

0.0.3
  - bugfix for context saving

0.0.2
  - Save channel/guild contexts separately
  - Concurrent message processing
  - Purge guild data when bot is removed from guild

0.0.1
  - Initial Public Release