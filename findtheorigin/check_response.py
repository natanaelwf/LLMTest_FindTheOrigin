#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re

def check_response(model_response):
    pattern = r"answer[: ]*\"?{}\"?".format('workbench', re.IGNORECASE)
    match = re.search(pattern, model_response, re.IGNORECASE)
    # Returns True if pattern is found, False otherwise
    return bool(match)

