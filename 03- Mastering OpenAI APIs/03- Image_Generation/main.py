## Import Libraries
from fastapi import FastAPI, BackgroundTasks
from starlette.responses import FileResponse
import os
from utils import gen_images    ## my custom function


## Intialize an app
app = FastAPI(debug=True)

def delete_images(image_path: str):
    os.remove(image_path)
    return None

@app.post('/images_gen')
async def images_gen(background_tasks: BackgroundTasks, prompt: str):

    ## Call the Function -> returns the image path
    image_path_local = gen_images(user_prompt=prompt)

    ## Get that Response and then delete image itself.
    response = FileResponse(image_path_local, media_type='image/png')

    ## Delete the output image file after the response has been sent
    background_tasks.add_task(delete_images, image_path_local)


    return response