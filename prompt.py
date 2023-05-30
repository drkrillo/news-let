import os
import time
import openai
import tiktoken

import preprocessing 

from dotenv import load_dotenv
load_dotenv()

MAX_TOKENS = 4096
openai.api_key  = os.getenv('OPENAI_API_KEY')

url = "https://arxiv.org/pdf/2305.14948"


def get_completion(prompt, model="gpt-3.5-turbo"): 
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, 
    )
    return response.choices[0].message["content"]

def summarize(chunks):
    chunks_summaries = ''
    for i in range(len(chunks)):
        prompt = f"""
        Your task is to generate a short summary from a fragment of \
        scientific paper from an e-library to help a junior \
        researcher selecting scientific papers for further study. 

        Summarize the fragment of scientific paper below, delimited by triple \
        backticks, in at most 300 words, and focusing on  \
        general aspects, implications and key points. 

        Review: ```{chunks[i]}```
        """
        response = get_completion(prompt)
        chunks_summaries += response + "\n"
        time.sleep(5)

    time.sleep(20)

    prompt = f"""
    Your task is to generate a consistent document from \
    summaries made from different fragments of the same  \
    scientific paper. 

    Generate a concise document based on the fragments below, \
    delimited by triple backticks, in at most 300 words,  \
    and focusing on technical aspects.

    ```{chunks_summaries}```
    """
    response = get_completion(prompt)
    
    return response