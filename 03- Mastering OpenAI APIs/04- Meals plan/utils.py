## Import Libraries, and read the key-token
import openai
import os
from dotenv import load_dotenv
import tempfile
import requests
import re
import time

## Load the Key token
_ = load_dotenv()
key_token = os.getenv('OpenAI_KEY_TOKEN')

## Assign that key_token to api_key of OpenAI
openai.api_key = key_token


## Create the folder for saving images locally
os.makedirs('gen_images', exist_ok=True)

def create_meals(user_ingredients: str, user_kcal: int=2000):
    ''' This Function takes the ingredients and the maxium kcal and create the meals with its titles and reciep.
    Args:
    *****
        (ingredients: str) --> The ingredients the user want of the meals with space between them.
        (kcal: int) --> The maxium kcal in the meals.

    Returns:
    *******
        (reponse: str) --> The meals plan wiht titles and recipes, The last 3 lines are the 3 titles of meals.
    '''

    ## paramas
    user_ingredients = ''.join(user_ingredients)

    ## prompts
    system_prompt = 'You are a smart and a telented cook'
    user_prompt = f'''Create a healthy daily meal plan for breakfast, lunch and dinner based on
                        the following ingredients {user_ingredients} with only 3 meals.
                        Explain each recipe.
                        The total daily intake of kcal should be below {user_kcal}.
                        Assign a suggestive and concise title to each meal.
                        Your answer should end with 'Titles: ' and the title of each recipe.
                        You MUST RETURN THE 3 Titles of meals at THE END '''
    ## messages
    messages = [ 
        {'role': 'system', 'content': system_prompt}, 
        {'role': 'user', 'content': user_prompt}
        ]
    
    ## Using ChatGPT for ChatCompletion
    response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',           
                messages=messages,
                temperature=0.7,  
                max_tokens=1000,  
                    )

    response = response['choices'][0]['message']['content']     ## The resulst of meals creation (the title and the recipe)

    return response



def meals_images(user_ingredients: str, user_kcal: int=2000):
    ''' This Function call the above function and get the resposne of each meal (the title, recieps).
        The last 3 lines are the title of the 3 meals.
    Args:
    *****
        The same arguments of above function, It call it.
    Returns:
        (images_paths: list) --> The list contains the path of generated images (3 paths for 3 meals).
    '''

    ## Call the above function
    response = create_meals(user_ingredients=user_ingredients, user_kcal=user_kcal)

    ## await
    time.sleep(20)

    ## Slicing the Titles of the 3 meals.
    meals_titles = response.splitlines()[-3:]
    ## Remove Numbers if exists
    meals_titles = [re.sub(r'\d+.', '', title).strip() for title in meals_titles]

    images_paths = []  ## for getting the paths of the generated 3 images. (MUST be before looping).
    
    try:
         ## Trying
        for i in range(len(meals_titles)):

            ## Usign Dall-E -> for each image (for each meal.)
            response = openai.Image.create(
                            prompt=meals_titles[i],   ## for each image for each meal.
                            n=1,    
                            size='1024x1024'    
                        )

            imag_url = response['data'][0]['url']  ## Getting URL only

            ## Download to disk with temporary filename
            request_res = requests.get(imag_url)

            ## Check response and save the image to (gen_images) folder
            if request_res.status_code == 200:

                img_temp_name = os.path.basename(tempfile.NamedTemporaryFile(suffix=".png").name)
                # Set the path where you want to save the image
                image_path_local = os.path.join('gen_images', img_temp_name)
                
                ## Write the image to the save path
                with open(image_path_local, "wb") as file:
                    file.write(request_res.content)

                # Append each image path to the list and return it finally.
                images_paths.append(image_path_local)
                print('image saved successfully. ')
            
                time.sleep(20)  ## await
                    
            else:
                return 'There is an error in getting the image link.'
                
        return images_paths

    except:
        return 'Sorry, There is an error generating the image, try again later.'

