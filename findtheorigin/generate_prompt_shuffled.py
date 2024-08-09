#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from .reorganize_file import reorganize_file
from .select_lines import select_lines
import random

def generate_prompt_shuffled(input_file, output_file, d, n_lines):
    
    # Getting the lines sorted according to d 
    reorganize_file(input_file, output_file, d)
    selected_lines = select_lines(output_file, d, n_lines)
    result_string = ''.join(selected_lines)
    
    lines = [line for line in result_string.split('\n') if line.strip()]

    # Shuffling all lines except target vertices
    fixed_lines = [
        '"workbench" is connected to "dad"',
        '"dad" is connected to "admire"'
    ]
    fixed_indices = [lines.index(line) for line in fixed_lines]
    lines_to_randomize = [line for i, line in enumerate(lines) if i not in fixed_indices]
    random.shuffle(lines_to_randomize)
    new_lines = []
    randomized_index = 0
    for i in range(len(lines)):
        if i in fixed_indices:
            new_lines.append(lines[i])
        else:
            new_lines.append(lines_to_randomize[randomized_index])
            randomized_index += 1
            
    new_result_string = '\n'.join(new_lines)    
    
    prompt = '''Several words below are interconnected. For example:
"X" is connected to "Y"
"Y" is connected to "Z"
In this scenario, the origin of "Z" is "X". We can visualize these connections as vertices and edges, like this:
"X"-->"Y"-->"Z"

Using this logic, consider the following list of connections, where each word is simply the name of a vertex with no other semantic meaning:

{}

Your task is to find the origin of "admire". Work carefully, step by step. Your final answer must be in this format: FINAL ANSWER: YOUR_ANSWER'''.format(new_result_string)
    
    return prompt

