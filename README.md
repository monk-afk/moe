# møe

A Discord chatbot equipped with DialoGTP; a pre-trained language model tailored for casual conversation.

<img decoding="async" loading="lazy" alt="moe banner red and white pixelated letters" src="https://raw.githubusercontent.com/monk-afk/moe/main/docs/images/moe_banner_v3_680x240.png"  width="340"/>

møe's official home is at the SquareOne Discord:

[![](https://dcbadge.limes.pink/api/server/pE4Tu3cf23)](https://discord.gg/pE4Tu3cf23)

[Invite moe to your server!](https://discord.com/oauth2/authorize?client_id=1249786267898740757)

___

- Casual Conversational AI Language Model
  - Powered by [DialoGPT, courtesy of Huggingface](https://huggingface.co/docs/transformers/main/en/model_doc/dialogpt)!

- Response Triggers
  - Messages containing the keywords "moe" or "bot".

- Specific Reply-to Channel
  - Configure to respond in designated channels

- Specific Reply-to User(s)
  - Will follow and reply to specified users

___


## Usage Examples

- When møe joins a guild, set a reply channel for him to chat freely:
  - In the designated channel, type: `m1 setreplychannel`
  - To unset a reply channel, type: `m1 unsetreplychannel`

- If a member needs extra attention, set a reply-to and møe will respond to their messages:
  - In any channel, type: `m1 sayhi @user`
  - To stop the replies, type: `m1 saybye @user`

- møe will remember the context of a conversation per-channel for up to ten messages:
  - To erase his memory in a channel, type: `m1 forgetchannel`
  - To erase his memory of all channels, type: `m1 forgetguild`

- Thats pretty much it. He's just a chat bot.
  - For all commands, type: `m1 help`

___

## Installation

- [Install steps](docs/install.sh)
- Requires discord.py version 2.5.0 or higher
- PostgreSQL database.
- Python3 (tested with 3.11)
- python3-venv for virtual environment
- python3-pip for additional libraries and modules
  - [Required modules](docs/requirements.txt)

___

### Response Generation Parameters

inputs
  - text (required)
    - The last input from the user in the conversation.
  - generated_responses
    - A list of strings corresponding to the earlier replies from the model.
  - past_user_inputs
    - A list of strings corresponding to the earlier replies from the user. Should be of the same length of generated_responses.
  - parameters (a dict containing the following keys)
    - min_length (Default: None).
      - Integer to define the minimum length in tokens of the output summary.
    - max_length (Default: None).
      - Integer to define the maximum length in tokens of the output summary.
    - top_k (Default: None).
      - An integer that limits the number of tokens considered when generating the next word. Example: top_k = 50: The model will only consider the 50 most probable next words.
    - top_p (Default: None).
      - Nucleus sampling dynamically adjusts the pool of candidate tokens based on the sum of the probabilities of the next tokens. Example: If top_p is 0.9, the model will consider the smallest set of tokens whose total probability adds up to 0.9 (90%).
    - temperature (Default: 1.0).
      - Float (0.0-100.0). adjusts the randomness of the model's predictions by scaling the probabilities of the next tokens. A high temperature makes all tokens more equally likely, while a low temperature makes the most likely tokens even more likely. Lower temperatures make the output more predictable and repetitive, while higher temperatures make it more varied and creative.
    - repetition_penalty (Default: None).
      - Float (0.0-100.0). The more a token is used within generation the more it is penalized to not be picked in successive generation passes.
    - max_time (Default: None).
      - Float (0-120.0). The amount of time in seconds that the query should take maximum. Network can cause some overhead so it will be a soft limit.
options 
  > (these apply only for the Inference API, not to the pre-trained transformers model)
  - a dictionary containing the following keys:
    - use_cache (Default: true). Boolean. There is a cache layer on the inference API to speedup requests we have already seen. Most models can use those results as is as models are deterministic (meaning the results will be the same anyway). However if you use a non deterministic model, you can set this parameter to prevent the caching mechanism from being used resulting in a real new query.
    - wait_for_model (Default: false) Boolean. If the model is not ready, wait for it instead of receiving 503. It limits the number of requests required to get your inference done. It is advised to only set this flag to true after receiving a 503 error as it will limit hanging in your application to known places.

___

## Changelog

- 0.0.9
  - Add Reaction emoji to messages with matching pattern
- 0.0.8
  - Command prefix is now in the .env file
  - Add reply-to command
- 0.0.7
  - Tidy reply conditional
  - ~~Add reply referencing [#7](https://github.com/monk-afk/moe/issues/7)~~
- 0.0.6
  - Fix typing indicator bug [#3](https://github.com/monk-afk/moe/issues/3)
- 0.0.5
  - Properly formatted help message
  - ~~Fix typing indicator bug [#3](https://github.com/monk-afk/moe/issues/3)~~
  - Fix errors on Guild removal [#5](https://github.com/monk-afk/moe/issues/5)
- 0.0.4
  - Ignore direct messages
  - bugfix trailing eos token
- 0.0.3
  - bugfix for context saving [#2](https://github.com/monk-afk/moe/issues/2)
- 0.0.2
  - Save channel/guild contexts separately
  - Concurrent message processing [#1](https://github.com/monk-afk/moe/issues/1)
  - Purge guild data when bot is removed from guild
- 0.0.1
  - Initial Public Release

___

```py
####################################################################################
# MIT License                                                                      #
#                                                                                  #
# Copyright (c) 2024 monk                                                          #
#                                                                                  #
# Permission is hereby granted, free of charge, to any person obtaining a copy     #
# of this software and associated documentation files (the "Software"), to deal    #
# in the Software without restriction, including without limitation the rights     #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell        #
# copies of the Software, and to permit persons to whom the Software is            #
# furnished to do so, subject to the following conditions:                         #
#                                                                                  #
# The above copyright notice and this permission notice shall be included in all   #
# copies or substantial portions of the Software.                                  #
#                                                                                  #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR       #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,         #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE      #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER           #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,    #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE    #
# SOFTWARE.                                                                        #
####################################################################################
```