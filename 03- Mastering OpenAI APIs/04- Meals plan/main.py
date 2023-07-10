## Import the Libraries
from fastapi import FastAPI, BackgroundTasks
from starlette.responses import Response
import os, io
import base64
import zipfile
from utils import create_meals, meals_images   ## my custom functions


## The image path folder 
GEN_IMAGES_FOLDER = os.path.join(os.getcwd(), 'gen_images')


## Intialize an app
app = FastAPI(debug=True)


def delete_images(image_path):
    os.remove(image_path)
    return None


@app.post('/meals_plan')
async def meals_plan(ingredients: str, kcal: int=2000):
    ''' This Function takes the ingredients and the maxium kcal and create the meals with its titles and reciep.

    Args:
    *****
        (ingredients: str) --> The ingredients the user want of the meals ** with space between them **.
        (kcal: int) --> The maxium kcal in the meals.

    Returns:
    *******
        (reponse: str) --> The meals plan wiht titles and recipes, The last 3 lines are the 3 titles of meals.
    '''

    ## Call the (create_meals) function
    response = create_meals(user_ingredients=ingredients, user_kcal=kcal)

    return response


@app.post('/generate_images')
async def generate_images(background_tasks: BackgroundTasks, ingredients: str, kcal: int=2000):

    ''' This Function takes the ingredients and the maxium kcal and create the meals with its titles and reciep.

    Args:
    *****
        (ingredients: str) --> The ingredients the user want of the meals ** with space between them **.
        (kcal: int) --> The maxium kcal in the meals.

    Returns:
    *******
        (zipped_images: zipfile) --> The Zipped Folder of the generated images (downloadable).
    '''

    ## Call the (meals_images) function
    images_paths = meals_images(user_ingredients=ingredients, user_kcal=kcal)

    s = io.BytesIO()
    zf = zipfile.ZipFile(s, "w")

    ## Looping fo zipping
    for fpath in images_paths:
        ## Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        ## Add file, at correct path
        zf.write(fpath, fname)

    ## Must close zip for all contents to be written
    zf.close()

    ## Grab ZIP file from in-memory, make response with correct MIME-type
    zipped_images = Response(s.getvalue(), media_type="application/x-zip-compressed", 
                    headers={'Content-Disposition': f'attachment;filename=images.zip'}
                    )
    ## Delete the images in the folder
    for img_path in images_paths:
        background_tasks.add_task(delete_images, img_path)

    return zipped_images

    