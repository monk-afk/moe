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
                    bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1) if self.chat_history_ids is not None else new_user_input_ids

                    attention_mask = torch.ones_like(bot_input_ids)
                    self.chat_history_ids = self.model.generate(
                        bot_input_ids,
                        max_length=1000,
                        pad_token_id=self.tokenizer.eos_token_id,
                        attention_mask=attention_mask,
                        do_sample=True,
                        top_k=50,
                        top_p=0.9,
                        temperature=0.7
                    )

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

                    last_5_messages = messages[5:]
                    flattened_last_5_with_delimiters = [token for message in last_5_messages for token in message + [50256]]
                    result_tensor = torch.tensor([flattened_last_5_with_delimiters])
                    response = self.tokenizer.decode(self.chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
                    await message.channel.send(response)
            finally:
                self.is_processing = False

async def setup(bot):
    await bot.add_cog(ChatCog(bot))