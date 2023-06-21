import openai
from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.getenv("SECRET_KEY_OPENAI")

openai.api_key = secret_key


def call_gpt(prompt):
    
    collected_message = ""
    
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[ {"role": "user", "content": prompt }],
        temperature=0,
        stream=True 
    )
    
    for chunk in completions:
        if 'content' in chunk.choices[0].delta:
            chunk_message = chunk.choices[0].delta.content
            collected_message += chunk_message
            print(chunk_message, end="")

    #print(collected_message)

    return collected_message

call_gpt("Disserte sobre os animais do norte do planeta")
