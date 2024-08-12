#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from setuptools import setup, find_packages

setup(
    name="findtheorigin",
    version="0.1.0",
    author="Natanael Wildner Fraga",
    author_email="natanael.wf@gmail.com",
    description="Testing reasoning degradation in LLMs as context windows grow. This test challenges LLMs to identify the origin vertex in a series of interconnected nodes, progressively increasing the context window to measure the impact on reasoning ability. The benchmark includes varying degrees of complexity, adjusting parameters such as the distance between connections and the order of connections.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/natanaelwf/LLMTest_FindTheOrigin",
    packages=find_packages(),
    install_requires=[
        'openai==1.40.1',
        'tiktoken==0.7.0'
    ],
    entry_points={
        'console_scripts': [
            'findtheorigin=findtheorigin.run_test:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

