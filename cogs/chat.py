# cogs/chat.py
import discord
import re
from discord.ext import commands
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from utils.pgsql import (
    get_reply_channel,
    get_channel_input_ids,
    set_channel_input_ids,
    check_reply_to,
)
import asyncio

patterns = {
    "moe": r".*\b@?[Mm][oø]e\b.*",
    "bot": r".*\bbots?\b.*",
    "molo": r".*\b[Mm][Oo][Ll][Oo]+\b.*",
    "monk": r".*\b@?[Mm][oø][Nn][Kk]+\b.*",
}

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.processing_channel = {}
        self.model_name = "microsoft/DialoGPT-large"
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)

    @commands.Cog.listener()
    async def on_message(self, message):
        guild_id = message.guild.id
        reply_channel = get_reply_channel(guild_id)
        channel_id = message.channel.id

        if (
            message.author == self.bot.user
            or (message.author.bot and channel_id != reply_channel)
        ):
            return

        if message.content.startswith(self.bot.command_prefix):
            return

        if message.guild is None:
            return

        if channel_id in self.processing_channel:
            return

        if (
            channel_id == reply_channel
            or any(re.match(pattern, message.content.lower()) for pattern in patterns.values())
            or check_reply_to(message.author.id)
        ):
            self.processing_channel[channel_id] = True
            asyncio.create_task(self.processor(message, reply_channel))

    async def processor(self, message, reply_channel):
        channel_id = message.channel.id
        input_tokens = await self.generate_tokens_from_message(message)

        try:
            typing_task = asyncio.create_task(self.send_typing(message.channel))
            await self.generate_response(message, input_tokens)

        finally:
            typing_task.cancel()
            del self.processing_channel[channel_id]

    async def generate_tokens_from_message(self, message):
        channel_id = message.channel.id
        guild_id = message.guild.id
        saved_input_ids = get_channel_input_ids(channel_id)

        message_content = ' '.join(message.content.split()[:100])

        new_user_input_ids = self.tokenizer.encode(message_content + self.tokenizer.eos_token, return_tensors='pt')

        if saved_input_ids is None:
            saved_input_ids = []

        new_saved_input_ids = saved_input_ids + new_user_input_ids.flatten().tolist()

        eos_count = 0
        token_count = 0
        eos_break_flag = 0
        final_saved_input_ids = []
        for token in reversed(new_saved_input_ids):
            token_count += 1
            if token == 50256:
                eos_count += 1
            if token_count >= 500:
                eos_break_flag = 1
            if eos_count == 10 or (eos_break_flag == 1 and token == 50256):
                break
            final_saved_input_ids.insert(0, token)

        return final_saved_input_ids

    async def generate_response(self, message, final_saved_input_ids):
        channel_id = message.channel.id
        guild_id = message.guild.id

        set_channel_input_ids(channel_id, guild_id, final_saved_input_ids)

        bot_input_ids = torch.tensor(final_saved_input_ids).unsqueeze(0)

        attention_mask = torch.ones_like(bot_input_ids)

        chat_history_ids = self.model.generate(
            bot_input_ids,
            min_length = 10,
            max_length = 1000,
            pad_token_id = self.tokenizer.eos_token_id,
            attention_mask = attention_mask,
            do_sample = True,
            top_k = 50,
            top_p = 0.7,
            temperature = 0.9,
            repetition_penalty = 1.0
        )

        response = self.tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

        await asyncio.sleep(5)
        await message.channel.send(response)

    async def send_typing(self, channel):
        try:
            while True:
                await channel.typing()
                await asyncio.sleep(5)
        except asyncio.CancelledError:
            pass

async def setup(bot):
    await bot.add_cog(Chat(bot))



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
