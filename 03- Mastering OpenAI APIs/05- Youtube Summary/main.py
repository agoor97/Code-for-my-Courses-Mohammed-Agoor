## Import Libraries
from fastapi import FastAPI
from utils import summarize_trancribt  ## my custom function




## Initialize an app
app = FastAPI(debug=True)


@app.post('/summarize_youtube')
async def summarize_youtube(link: str, is_english: bool=True):

    ## Call the function from utils.py
    response = summarize_trancribt(link=link, is_english=is_english)

    return response




