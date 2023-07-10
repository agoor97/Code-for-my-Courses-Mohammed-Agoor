## Import Libraries
from fastapi import FastAPI
from utils import text_search  ## my custom function



## Initialize an app
app = FastAPI(debug=True)


@app.post('/semantic_search')
async def semantic_search(search_text: str, threshold: float=0.3):

    ## Call the function from utils.py
    results = text_search(search_text=search_text, threshold=threshold)

    return results