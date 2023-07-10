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


## Create a folder
os.makedirs('gen_images', exist_ok=True)


def gen_images(user_prompt= str):

    ## system_prompt for gpt-3.5-turbo
    system_prompt = ''''You are an AI assistant, Your task is to regenerate the following text to be a prompt for an image generation model.
                            Instructions:
                                1. Analyze the text and refine it to ensure clarity, specificity, and accuracy.
                                2. Create a prompt in ENGLISH Langauge that best represent the text meaning.
                                3. If the text is not in English, TRANSLATE it into English.
                                4. Retrun the Result in a list containing only the final prompt in ENGLISH. 
                        '''
    
    ## messages
    messages = [ 
        {'role': 'system', 'content': system_prompt}, 
        {'role': 'user', 'content': user_prompt}
            ]
    
    ## Using ChatGPT to refine the user prompt
    response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',           
                messages=messages,
                temperature=0.7,  
                max_tokens=1000,  
                    )

    refined_prompt = response['choices'][0]['message']['content']  ## That what will Dall-E work on.


    ## Using Dall-E
    response = openai.Image.create(
                    prompt=refined_prompt,   ## The refined_prompt aftre translating and preparing.
                    n=1,    
                    size='1024x1024'    
                )

    imag_url = response['data'][0]['url']  ## Getting URL only

    ## Download to disk with temporary filename
    request_res = requests.get(imag_url)

    ## Check response and save the image to (gen_images) folder
    if request_res.status_code == 200:

        img_temp_name = os.path.basename(tempfile.NamedTemporaryFile(suffix=".png").name)
        ## Set the path where you want to save the image
        image_path_local = os.path.join('gen_images', img_temp_name)
        
        ## Write the image to the save path
        with open(image_path_local, "wb") as file:
            file.write(request_res.content)
            
    else:
        return 'There is an error in getting the image link.'

    return image_path_local








