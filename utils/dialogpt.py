# moe/utils/dialogpt.py
# Copyright © 2026 monk <https://github.com/monk-afk>
# SPDX-License-Identifier: MIT
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from utils.logroll import logging

log = logging.getLogger(__name__)

class DialoGPT:
    def __init__(self):
        self.model_name = "microsoft/DialoGPT-medium"
        self.tokenizer = None
        self.model = None
        log.info(f"Initializing GPT model: {self.model_name}")

    def load_tokenizer(self):
        if self.tokenizer is None:
            self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
            log.info(f"OK load_tokenizer: {self.model_name}")
        return self.tokenizer

    def load_model(self):
        if self.model is None:
            self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
            log.info(f"OK load_model: {self.model_name}")
        return self.model

dialogpt = DialoGPT()
