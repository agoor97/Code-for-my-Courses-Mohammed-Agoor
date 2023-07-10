## Import Libraries, and read the key-token
import openai
import os
from dotenv import load_dotenv
import requests
import tempfile

## Load the Key token
_ = load_dotenv()
key_token = os.getenv('OpenAI_KEY_TOKEN')

## Assign that key_token to api_key of OpenAI
openai.api_key = key_token



def sent_analysis(user_prompt: str, emotions: list):

    ## Define System prompt 
    system_prompt = f''' You are an AI assistant, You are an emotionally intelligent assistant
                        Classify the user's text in ONLY ONE OF THE FOLLOWING EMOTIONS {emotions}
                        After that respond with the emotion only.'''

    messages = [ 
        {'role': 'system', 'content': system_prompt}, 
        {'role': 'user', 'content': user_prompt}  ## from the function
            ]
    
    ## The response
    response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',           
                messages=messages,
                temperature=0,  ## I need the model to be deterministic  
                max_tokens=100,   
                    )
    return response['choices'][0]['message']['content']