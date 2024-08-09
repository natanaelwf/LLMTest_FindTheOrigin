#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from openai import OpenAI
import os
import requests
import csv
import time
import argparse
from .generate_prompt import generate_prompt
from .generate_prompt_shuffled import generate_prompt_shuffled
from .count_tokens import count_tokens
from .check_response import check_response

endpoint_claude = "https://api.anthropic.com/v1/messages"

n_tokens, model_responses = [],[]

def main():
    # Configuring the argument parser
    parser = argparse.ArgumentParser(description="Run the Find the Origin benchmark tests.")
    parser.add_argument('--provider', type=str, required=True, help='API provider (openai or anthropic)')
    parser.add_argument('--model_name', type=str, required=True, help='Model name (e.g., gpt-3.5-turbo-0125)')
    parser.add_argument('--d_parameter', type=int, required=True, help='Distance parameter')
    parser.add_argument('--max_lines', type=int, required=True, help='Maximum number of lines to insert')
    parser.add_argument('--step_lines', type=int, required=True, help='Step increment for the number of lines of each prompt')
    parser.add_argument('--shuffle', type=bool, required=False, default=False, help='Randomize the positioning of irrelevant vertices.')

    # Parsing the arguments
    args = parser.parse_args()
    d = args.d_parameter
    max_lines = args.max_lines
    step_lines = args.step_lines
    model = args.model_name
    provider = args.provider
    shuffle = args.shuffle

    # List to save the number of tokens
    n_tokens = []

    # Loop to run the tests
    for n in range(1+abs(d), max_lines, step_lines):
        
        print('Running prompt for {} lines of vertices'.format(n))
        
        if shuffle == False:
            prompt = generate_prompt('vertices.txt', 'vertices_reorg.txt', d, n)
        else:
            prompt = generate_prompt_shuffled('vertices.txt', 'vertices_reorg.txt', d, n)
        
        num_tokens = count_tokens(prompt)
        n_tokens.append(num_tokens)

        # OpenAI models:
        if provider == 'openai':
            client_oa = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
            got_response = False
            while got_response == False:
                try:
                    response = client_oa.chat.completions.create(
                        model= model,
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": prompt},
                        ],
                        max_tokens=256,
                        temperature=0.
                    )
                    got_response = True
                except Exception as e:
                    print('Error accessing OpenAI:', e)
                    print('Trying again in 10 seconds')
                    time.sleep(10)

            response = response.choices[0].message.content
            result = check_response(response)    
            model_responses.append(result)       

        elif provider == 'anthropic':
            
        # Anthropic models:
            api_key_claude = os.getenv('CLAUDE_API_KEY')
            headers_claude = {'Content-Type': 'application/json', 'x-api-key': api_key_claude, 'anthropic-version': '2023-06-01'}
            data_claude = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "system": "You are a helpful assistant.",
                "max_tokens": 256,
                "top_p": 1,
                "temperature": 0.
            }

            got_response = False
            while got_response == False:
                try:
                    response = requests.post(endpoint_claude, headers=headers_claude, json=data_claude)
                    if response.status_code == 200:
                        got_response = True
                    else:
                        print('Error accessing Anthropic:', response)
                        print('Trying again in 10 seconds')
                        time.sleep(10)
                except Exception as e:
                    print('Error accessing Anthropic:', e)
                    print('Trying again in 10 seconds')
                    time.sleep(10)

            response_json = response.json()
            dict_data = response_json['content'][0]
            text_content = dict_data['text']
            result = check_response(text_content)
            model_responses.append(result)

    # Saving results
    dataset_dic = {
        'n_tokens': n_tokens,
         model: model_responses,
    }

    str_d = str(d)
    filename = f'results_d{str_d}_model_{model}_max_lines{max_lines}_steps{step_lines}.csv'

    # Writing the CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(dataset_dic.keys())
        for values in zip(*dataset_dic.values()):
            writer.writerow(values)

if __name__ == "__main__":
    main()

