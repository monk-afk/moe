# cogs/chat.py
import discord
import re
import random
from discord.ext import commands
import torch
from utils.pgsql import (
    get_reply_channel,
    get_input_ids,
    set_input_ids,
    check_reply_to
)
import asyncio
from utils.logroll import logging
log = logging.getLogger(__name__)
from utils.model_loader import model_loader

response_triggers = {
    "moe": r".*\b@?[Mm][oø]e\b.*",
    "bot": r".*\bbots?\b.*",
    "molo": r".*\b[Mm][Oo][Ll][Oo]+\b.*",
    "monk": r".*\b@?[Mm][oø][Nn][Kk]+\b.*",
}

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.processing_channel = {}
        self.model, self.tokenizer = model_loader.load_model_and_tokenizer()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:  # ignore direct messages
            return

        if message.content.startswith(self.bot.command_prefix):  # don't process message if it's a command
            return

        guild_id = message.guild.id
        channel_id = message.channel.id

        if channel_id in self.processing_channel:  # process only one message per channel
            return

        reply_channel = get_reply_channel(guild_id)

        if (
            message.author == self.bot.user  # don't reply to self
            # don't reply to bot messages not in the reply channel
            or (message.author.bot and channel_id != reply_channel)
        ):
            return

        if (
            channel_id == reply_channel
            or any(re.match(pattern, message.content.lower()) for pattern in response_triggers.values())
            or check_reply_to(guild_id, message.author.id)
        ):
            self.processing_channel[channel_id] = True  # to avoid queuing message processing in a single channel
            asyncio.create_task(self.processor(message))

    async def processor(self, message):
        channel_id = message.channel.id
        input_tokens = await self.generate_tokens_from_message(message)

        try:
            await self.generate_response(message, input_tokens)

        except Exception as e:
            log.error(f"ERROR processor({message}): {e}")
            pass

        finally:
            del self.processing_channel[channel_id]

    async def generate_tokens_from_message(self, message):
        saved_input_ids = get_input_ids(message.guild.id, message.author.id) # get user chat history

        message_content = ' '.join(message.content.split()[:30]) # limit input 30 words from message

        new_user_input_ids = self.tokenizer.encode(message_content + self.tokenizer.eos_token, return_tensors='pt')

        if saved_input_ids is None:
            saved_input_ids = []

        new_saved_input_ids = saved_input_ids + new_user_input_ids.flatten().tolist()

        eos_count = 0
        token_count = 0
        eos_break_flag = 0
        final_saved_input_ids = []

        for token in reversed(new_saved_input_ids):  # reversed to trim oldest messages from input tokens
            token_count += 1  # limit input to 100, or 12 EOS tokens
            if token == 50256:
                eos_count += 1
            if token_count >= 100:
                eos_break_flag = 1
            if eos_count == 12 or (eos_break_flag == 1 and token == 50256):
                break
            final_saved_input_ids.insert(0, token)

        return final_saved_input_ids

    async def generate_response(self, message, final_saved_input_ids):
        await asyncio.sleep(random.uniform(1.2, 3.4))  # delay typing

        async with message.channel.typing():
            bot_input_ids = torch.tensor(final_saved_input_ids).unsqueeze(0)

            attention_mask = torch.ones_like(bot_input_ids)

            response_tokens = self.model.generate(
                bot_input_ids,
                min_length = 20,
                max_length = 1000,
                pad_token_id = self.tokenizer.eos_token_id,
                attention_mask = attention_mask,
                do_sample = True,
                # adjusting these three causes the most noticeable change to responses
                top_k = 100,               # limits the number of tokens considered
                top_p = 0.89,              # smallest set of tokens whose total probability adds up to
                temperature = 0.92,        # lower temp outputs more predictably, high temp more varied and creative
                no_repeat_ngram_size = 2,  # prevents repeating words too often, 3 is more strict
                repetition_penalty = 1.0
            )

            response = self.tokenizer.decode(response_tokens[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

            final_saved_input_ids += self.tokenizer.encode(response + self.tokenizer.eos_token)

            set_input_ids(message.guild.id, message.author.id, final_saved_input_ids)

            # # Incase there are issues with generating too quickly, this can be a fallback method:
            # estimated_words = len(response_tokens[0])
            # typing_time = min(4, max(1, estimated_words / 4))
            # await asyncio.sleep(typing_time)
        await message.channel.send(response)

async def setup(bot):
    await bot.add_cog(Chat(bot))



######################################################################################
##  MIT License                                                                     ##
##                                                                                  ##
##  Copyright © 2024-2025 monk                                                      ##
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