## Import Librarise
from fastapi import FastAPI
from utils import custom_chatbot   ## my custom function


## Initialize an app
app = FastAPI(debug=True)


## The Function
@app.post('/chatbot')
async def chatbot(prompt: str):

    ## Call the function from utils.py file
    response = custom_chatbot(user_prompt=prompt)

    return response