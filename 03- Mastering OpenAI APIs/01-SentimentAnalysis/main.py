## Import the Libraries 
from fastapi import FastAPI
from utils import sent_analysis   ## my custom function



## Initialize an app 
app = FastAPI(debug=True)

## The classes you want to work on it
# list_emotions = ['POSITIVE', 'NEUTRAL', 'NEGATIVE']
list_emotions = ['True', 'False']


@app.post('/emotions')
async def get_emotions(prompt: str):

    ## Call the custom Function
    result = sent_analysis(user_prompt=prompt, emotions=list_emotions)

    return result