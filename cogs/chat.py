import discord
import re
from discord.ext import commands
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from utils.conf import config

patterns = {
    "moe": r".*\bmoe\b.*",
    "bot": r".*\bbot\b.*",
}

class ChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model_name = "microsoft/DialoGPT-large"
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
        self.chat_history_ids = None
        self.is_processing = False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return

        if self.is_processing:
            return

        if message.channel.id == config.reply_channel or any(re.match(pattern, message.content.lower()) for pattern in patterns.values()):
            self.is_processing = True
            try:
                async with message.channel.typing():
                    user_input = message.content
                    new_user_input_ids = self.tokenizer.encode(user_input + self.tokenizer.eos_token, return_tensors='pt')
                    bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids], dim = -1) if self.chat_history_ids is not None else new_user_input_ids

                    flat_token_ids = bot_input_ids.flatten().tolist()

                    messages = []
                    current_message = []

                    for token_id in flat_token_ids:
                        if token_id == 50256:
                            if current_message:
                                messages.append(current_message)
                                current_message = []
                        else:
                            current_message.append(token_id)
                    if current_message:
                        messages.append(current_message)

                    if len(messages) > 10:
                        last_10_messages = messages[10:]
                        flattened_last_10_with_delimiters = [token for message in last_10_messages for token in message + [50256]]
                        result_tensor = torch.tensor([flattened_last_10_with_delimiters])
                        bot_input_ids = result_tensor
                        print(f"Last 10 messages: {last_10_messages}")
                    else:
                        last_10_messages = []

                    attention_mask = torch.ones_like(bot_input_ids)
                    self.chat_history_ids = self.model.generate(
                        bot_input_ids,
                        max_length = 1000,
                        pad_token_id = self.tokenizer.eos_token_id,
                        attention_mask = attention_mask,
                        do_sample = True,
                        top_k = 50,
                        top_p = 0.9,
                        temperature = 0.6
                    )

                    response = self.tokenizer.decode(self.chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
                    await message.channel.send(response)
            finally:
                self.is_processing = False

async def setup(bot):
    await bot.add_cog(ChatCog(bot))




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