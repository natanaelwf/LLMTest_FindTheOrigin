#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def select_lines(filename, d, n_lines):
    
    if n_lines<=abs(d):
        raise ValueError("n_lines must be greater than abs(d).")
        
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    # Find the index of the row containing "workbench"
    index_workbench = next(i for i, line in enumerate(lines) if "workbench" in line)
    
    # Calculates the initial index based on d
    if d >= 0:
        start = index_workbench - int((n_lines - d)/2)
    else:
        start = index_workbench - int((n_lines - abs(d))/2) - abs(d)
    
    # Ensures that start is not negative
    start = max(0, start)
    
    # Returns n_lines
    return lines[start:start+n_lines]

