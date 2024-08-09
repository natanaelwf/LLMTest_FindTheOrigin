#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tiktoken

def count_tokens(prompt, model_name='gpt-3.5-turbo'):
    
    # Encode the prompt to get the tokens
    enc = tiktoken.encoding_for_model(model_name)
    tokens = enc.encode(prompt)

    return len(tokens)

