#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from .reorganize_file import reorganize_file
from .select_lines import select_lines

def generate_prompt(input_file, output_file, d, n_lines):
    reorganize_file(input_file, output_file, d)
    selected_lines = select_lines(output_file, d, n_lines)
    result_string = ''.join(selected_lines)
    prompt = '''Several words below are interconnected. For example:
"X" is connected to "Y"
"Y" is connected to "Z"
In this scenario, the origin of "Z" is "X". We can visualize these connections as vertices and edges, like this:
"X"-->"Y"-->"Z"

Using this logic, consider the following list of connections, where each word is simply the name of a vertex with no other semantic meaning:

{}
Your task is to find the origin of "admire". Work carefully, step by step. Your final answer must be in this format: FINAL ANSWER: YOUR_ANSWER'''.format(result_string)
    
    return prompt

