### Image and Colors

32bit floating point RGB images are more clearly displayed on Discord profile pictures, compared to images with indexed palette.

Icon Colors
-----------
      | hex     | (RGB)[HSV]
Red   | #d50000 | (83.5,0.0,0.0)[0.0,100.0,83.5]
Dark  | #1e201d | (11.8,12.5,11.4)[100.0,9.4,12.5]


### Response Generation Parameters

The huggingface documentation has been updated, I'm no longer able to find the exact page with these parameters.

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

    - repetition_penalty (Default: 1.0). Don't change this
      - Float ~~ (0.0-100.0) ~~. The more a token is used within generation the more it is penalized to not be picked in successive generation passes.
    - max_time (Default: None).
      - Float (0-120.0). The amount of time in seconds that the query should take maximum. Network can cause some overhead so it will be a soft limit.
~~options  ~~
~~  > (these apply only for the Inference API, not to the pre-trained transformers model) ~~
~~  - a dictionary containing the following keys: ~~
~~    - use_cache (Default: true). Boolean. There is a cache layer on the inference API to speedup requests we have already seen. Most models can use those results as is as models are deterministic (meaning the results will be the same anyway). However if you use a non deterministic model, you can set this parameter to prevent the caching mechanism from being used resulting in a real new query. ~~
~~    - wait_for_model (Default: false) Boolean. If the model is not ready, wait for it instead of receiving 503. It limits the number of requests required to get your inference done. It is advised to only set this flag to true after receiving a 503 error as it will limit hanging in your application to known places. ~~