## Import Libraries, and read the key-token
import openai
import os
from dotenv import load_dotenv
import time

## Load the Key token
_ = load_dotenv()
key_token = os.getenv('OpenAI_KEY_TOKEN')

## Assign that key_token to api_key of OpenAI
openai.api_key = key_token


## Looping to make it much more easier
all_messages = list()

## Create system prompt
system_prompt = 'Answer as concisely as possible.'
all_messages.append({'role': 'system', 'content': system_prompt})

## ------------------------------ Call the API -------------------------------- ##
def custom_chatbot(user_prompt):

    ## Looping while true
    while True:
        
        ## If the user wants to exit the chatbot -> break
        if user_prompt.lower() in ['quit', 'exit', 'ex', 'out', 'escape']:
            time.sleep(2)  ## wait 2 seconds

            ## If the user exit the chatbot, Clear it.
            all_messages.clear()
            return 'Thanks for using my ChatBot'
        
        ## If the user doesn't write any thing -> Continue
        elif user_prompt.lower() == '': 
            continue

        ## Answer
        else:
            ## append the question of user to message as a user roke
            all_messages.append({'role': 'user', 'content': user_prompt})
            
            ## Call the API
            each_response = openai.ChatCompletion.create(
                            model='gpt-3.5-turbo',           
                            messages=all_messages,
                            temperature=0.7,  
                            max_tokens=1000,   
                                )
            each_response = each_response['choices'][0]['message']['content']
            
            ## We must append this respond to the messages
            all_messages.append({'role': 'assistant', 'content': each_response})
            
            return each_response  ## return the response of the api
            