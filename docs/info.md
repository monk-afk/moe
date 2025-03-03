### Image and Colors

32bit floating point RGB images are more clearly displayed on Discord profile pictures, compared to images with indexed palette.

Icon Colors
-----------
```
      | hex     | (RGB)[HSV]
Red   | #d50000 | (83.5,0.0,0.0)[0.0,100.0,83.5]
Dark  | #1e201d | (11.8,12.5,11.4)[100.0,9.4,12.5]
```

### Response Generation Parameters

[The huggingface response parameters.](https://huggingface.co/docs/transformers/v4.49.0/en/main_classes/text_generation#transformers.GenerationConfig)

  - parameters (a dict containing the following keys)
    - `min_length` (Default: None).
      - Integer to define the minimum length in tokens of the output summary.
    - `max_length` (Default: None).
      - Integer to define the maximum length in tokens of the output summary.
    - `top_k` (Default: None).
      - An integer that limits the number of tokens considered when generating the next word. Example: top_k = 50: The model will only consider the 50 most probable next words.
    - `top_p` (Default: None).
      - Nucleus sampling dynamically adjusts the pool of candidate tokens based on the sum of the probabilities of the next tokens. Example: If top_p is 0.9, the model will consider the smallest set of tokens whose total probability adds up to 0.9 (90%).
    - `temperature` (Default: 1.0).
      - Float (0.0-100.0). adjusts the randomness of the model's predictions by scaling the probabilities of the next tokens. A high temperature makes all tokens more equally likely, while a low temperature makes the most likely tokens even more likely. Lower temperatures make the output more predictable and repetitive, while higher temperatures make it more varied and creative.
    - `no_repeat_ngram_size` (Default: none, Integer)
      - Prevents the model from repeating the same sequence of words (ngrams) within a response. A parameter of 2 will restrict output from repeating any two-word phrases preventing immediate word repetition without being too restrictive. Setting to 3 prevents repeating any three-word phrases to force more variety in sentence structures.
    - `repetition_penalty` (Default: 1.0). Don't change this
      - Float ~~ (0.0-100.0) ~~. The more a token is used within generation the more it is penalized to not be picked in successive generation passes.