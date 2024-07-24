# møe

A Discord chatbot equipped with DialoGTP; a pre-trained language model tailored for casual conversation.

<img decoding="async" loading="lazy" alt="moe icon of a red and black checkered diamond" src="https://raw.githubusercontent.com/monk-afk/moe/main/docs/images/moe_banner_v3_680x240.png" width="340"/>

[![](https://dcbadge.limes.pink/api/server/CFBC8juT8c)](https://discord.gg/CFBC8juT8c)

This Readme is incomplete and may contain errors.

___

- > Response Triggers
  - Messages containing the keywords "moe" or "bot".
  - Reply references 
- > Channel Specific
  - It can be configured to respond only in designated channels.
- > AI Language Model
  - Utilizes the DialoGPT model from Microsoft to simulate chat.

___

## Installation

- Install script found in docs/install.sh

- PostgreSQL database.
- Python3 (tested with 3.11)
- python3-venv for virtual environment
- python3-pip for additional libraries and modules
  - A list of required modules can be found in docs/requirements.txt

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
  - a dictionary containing the following keys:
    - use_cache (Default: true). Boolean. There is a cache layer on the inference API to speedup requests we have already seen. Most models can use those results as is as models are deterministic (meaning the results will be the same anyway). However if you use a non deterministic model, you can set this parameter to prevent the caching mechanism from being used resulting in a real new query.
    - wait_for_model (Default: false) Boolean. If the model is not ready, wait for it instead of receiving 503. It limits the number of requests required to get your inference done. It is advised to only set this flag to true after receiving a 503 error as it will limit hanging in your application to known places.

___

## Changelog

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