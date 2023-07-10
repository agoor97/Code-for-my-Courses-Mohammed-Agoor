## Import Libraries, and read the key-token
import openai
import os
from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
import numpy as np
from dotenv import load_dotenv

## Load the Key token
_ = load_dotenv()
key_token = os.getenv('OpenAI_KEY_TOKEN')

## Assign that key_token to api_key of OpenAI
openai.api_key = key_token


## Load the Embedding File
df = pd.read_csv('embeddings.csv')

## Convert from string to numpy array
df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)



def text_search(search_text: str, threshold: float=0.3):
    ''' This Function get the simialr words to the given one.
    
    Args:
    *****
        (search_text: str) --> The required word to get similar with it.
        (threshold: float) --> The maximum threshold to get words bigger than it (cosine_similarity)

    Returns:
    *******
        (similar_texts: list) --> List of similar texts to the given one (search_word).
    '''
    ## Searching in real time
    search_vector = get_embedding(text=search_text, engine='text-embedding-ada-002')
    ## Get the simialr using metric (cosing_similarity) for example.
    ## Apply that for each instance
    df['similarity'] = df['embeddings'].apply(lambda vector: cosine_similarity(search_vector, vector))

    ## Sorting
    df.sort_values(by='similarity', ascending=False, inplace=True)

    # ## Use Threshold to filter these.
    similar_texts = df[df['similarity'] > threshold]['text'].tolist()

    return similar_texts