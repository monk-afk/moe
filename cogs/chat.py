# moe/cogs/chat.py
# Copyright © 2026 monk <https://github.com/monk-afk>
# SPDX-License-Identifier: MIT
import discord
import re
import random
from discord.ext import commands
import torch
from utils.nosj import (
    get_reply_channel,
    get_input_tokens,
    set_key,
    get_reply_to
)
import asyncio
from utils.conf import config
from utils.logroll import logging
log = logging.getLogger(__name__)

from utils.dialogpt import dialogpt

response_triggers = {
    "moe": r".*\bm+[oø]+e+\b.*",
    "atmoe": r".*<@1249786267898740757>.*",  # '@mention' is received by numeric ID
    "doot": r".*\bdoot\b.*",
    "bot": r".*\bbots?\b.*",
}

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.processing_channel = {}
        self.model = dialogpt.load_model()
        self.tokenizer = dialogpt.load_tokenizer()
        self.bad_words_ids = self.get_blacklisted()
        self.generation_lock = asyncio.Lock()
        self.blacklist = {
            "love", "lub", "luv", "ily", "kiss", "baby", "kith",
            "babe", "bby", "bb", "bich", "pregnancy", "molester",
            "beotch", "bae", "suicide", "betch", "fokking", "sexual",
            "sex", "fagit", "faggot", "gay", "bf", "boyfriend", "gf",
            "girlfriend", "sexy", "fuck", "shit", "whore", "karmawhore",
            "fap", "fapping", "fappening", "beer", "wuv", "fokken", "gulag",
        }

    def get_blacklisted(self): # will refuse to say words on the blacklist
        bad_words_ids = [self.tokenizer(word, add_prefix_space=True).input_ids for word in self.blacklist]
        return bad_words_ids

    def trim_token_memory(self, tokens):
        if not tokens:
            return []

        eos_token_id = self.tokenizer.eos_token_id
        token_list = list(tokens)
        start_index = max(0, len(token_list) - 100)
        trimmed = token_list[start_index:]

        if start_index > 0 and token_list[start_index - 1] != eos_token_id:
            try:
                first_eos_index = trimmed.index(eos_token_id)
            except ValueError:
                first_eos_index = None

            if first_eos_index is not None and first_eos_index < len(trimmed) - 1:
                trimmed = trimmed[first_eos_index + 1:]

        eos_positions = [
            index
            for index, token in enumerate(trimmed)
            if token == eos_token_id
        ]

        if len(eos_positions) > 12:
            trim_after_index = eos_positions[-13] + 1
            if trim_after_index < len(trimmed):
                trimmed = trimmed[trim_after_index:]

        return list(trimmed)

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

        reply_channel = await get_reply_channel(guild_id)

        if (
            message.author == self.bot.user  # don't reply to self
            # don't reply to bot messages not in the reply channel
            or (message.author.bot and channel_id != reply_channel)
        ):
            return

        if (
            channel_id == reply_channel
            or any(re.match(pattern, message.content.lower()) for pattern in response_triggers.values())
            or await get_reply_to(guild_id, message.author.id)
        ):
            self.processing_channel[channel_id] = True  # to avoid queuing message processing in a single channel
            asyncio.create_task(self.processor(message))

    async def processor(self, message):
        try:
            input_tokens = await self.generate_tokens_from_message(message)
            await self.generate_response(message, input_tokens)

        except Exception as e:
            log.error("ERROR processor: %s", type(e).__name__)
            pass

        finally:
            del self.processing_channel[message.channel.id]

    async def generate_tokens_from_message(self, message):
        saved_input_ids = await get_input_tokens(message.guild.id, message.author.id) # get user chat history

        message_content = ' '.join(message.content.split()[:30]) # limit input 30 words from message
        new_user_input_ids = self.tokenizer.encode(message_content + self.tokenizer.eos_token, return_tensors='pt')

        if saved_input_ids is None:
            saved_input_ids = []

        new_saved_input_ids = saved_input_ids + new_user_input_ids.flatten().tolist()
        return self.trim_token_memory(new_saved_input_ids)

    async def generate_response(self, message, final_saved_input_ids):
        await asyncio.sleep(random.uniform(2.2, 3.8))  # delay typing

        async with message.channel.typing():
            bot_input_ids = torch.tensor(final_saved_input_ids).unsqueeze(0)

            attention_mask = torch.ones_like(bot_input_ids)

            async with self.generation_lock:
                response_tokens = await asyncio.to_thread(
                    self.model.generate,
                    bot_input_ids,
                    min_length = 20,
                    max_length = 1000,
                    pad_token_id = self.tokenizer.eos_token_id,
                    attention_mask = attention_mask,
                    bad_words_ids = self.bad_words_ids,
                    repetition_penalty = 1.0,
                    do_sample = True,
                    # adjusting these causes the most noticeable change to responses
                    top_k = 95,                # limits the number of tokens considered
                    top_p = 0.9,               # smallest set of tokens whose total probability adds up to
                    temperature = 0.7,         # lower temp outputs more predictably, high temp more varied and creative
                    no_repeat_ngram_size = 2   # prevents repeating words too often, 3 is more strict\
                )

            response = self.tokenizer.decode(response_tokens[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

            if not response.strip():
                log.warning(f"Refused empty message")
                return

            final_saved_input_ids += self.tokenizer.encode(response + self.tokenizer.eos_token)
            final_saved_input_ids = self.trim_token_memory(final_saved_input_ids)
            await set_key(message.guild.id, message.author.id, "input_tokens", final_saved_input_ids)
        await message.channel.send(response)

async def setup(bot):
    await bot.add_cog(Chat(bot))
