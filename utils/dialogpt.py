# utils/dialogpt.py
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from utils.logroll import logging

log = logging.getLogger(__name__)

class DialoGPT:
    def __init__(self):
        self.model_name = "microsoft/DialoGPT-large"
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