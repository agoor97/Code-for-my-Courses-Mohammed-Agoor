## Import Libraries, and read the key-token
import openai
import os
from dotenv import load_dotenv
import os
from pytube import YouTube

## Load the Key token
_ = load_dotenv()
key_token = os.getenv('OpenAI_KEY_TOKEN')

## Assign that key_token to api_key of OpenAI
openai.api_key = key_token


## Create the folder for downloaded audio files.
os.makedirs('youtube_audio_vids', exist_ok=True)
AUDIO_FOLDER_PATH = os.path.join(os.getcwd(), 'youtube_audio_vids')

def dowanload_rename_audio(link):
    ''' This Function take the link, dowanload the audio of the provided youtube link, and rename it.

    Args:
    *****
        (link: url) --> The youtube video link.

    Returns:
    ******* 
        (audio_path_new: str) --> The path of the audio file after renaming and making it .mp3
    '''

    ## Some validation
    if 'youtube.com' not in link: 
        return 'Check your Link, There is an error in it.'
    
    try:
        ## Downloading only the Audio
        yt_vid = YouTube(url=link)
        audio_file = yt_vid.streams.filter(only_audio=True).first()
        print('Downloading video ...')
        audio_path_old = audio_file.download(output_path=AUDIO_FOLDER_PATH)
        print('Done downloading ...')

        ## Rename the audio file
        basename_old = os.path.basename(audio_path_old)
        name_old, exten_old = os.path.splitext(basename_old)
        name_old = name_old.lower().replace(' ', '-')

        ## From mp4 to mp3 and 
        audio_path_new = f'{name_old}.mp3'
        audio_path_new = os.path.join(os.getcwd(), 'youtube_audio_vids', audio_path_new)
        os.rename(audio_path_old, audio_path_new)
        print('Done Renaming ...')

    except:
        return 'Sorry there is an error in loading the audio file'
    
    return audio_path_new



def summarize_trancribt(link:str, is_english: bool=True):
    ''' This Function take the link, call the above function and translate or transripe the audio file.

    Args:
    *****
        (link: url) --> The youtube video link.
        (is_english: bool) --> check language for transcribtion only if english, and translate if other languages.

    Returns:
    ******* 
        (response: str) --> The Summarization of transcribted audio file.    
    '''

    try:
        ## Call the above function
        audio_path = dowanload_rename_audio(link=link)

        ## Trancribe if the language is_english else translate to english
        if is_english:
            ## Transcrip using whipser
            with open(audio_path, 'rb') as file:
                transcribt = openai.Audio.transcribe('whisper-1', file)
        
        else:
            ## Translate using whipser if not english
            with open(audio_path, 'rb') as file:
                transcribt = openai.Audio.translate('whisper-1', file)

        ## delete the audio file
        os.remove(audio_path)

        ## Use ChatGPT API for summarization
        ## Prompts
        system_prompt = 'You are an AI assistant and work as a life coach.'
        user_prompt = f''' Create a summary of the following text.
                    Text: {transcribt}

                    Add a title to the summary.
                    Your summary should be informative and factual, covering the most important aspects of the topic.
                    Start your summary with an INTRODUCTION PARGRAPH that gives an overview of the topic FOLLOWED by 
                    BULLETS POINTS if possible AND the summary with a CONCLUSION PHARASE.
            
                    '''
        ## Messages
        messgaes = [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                    ]

        ## ChatCompletion API
        response = openai.ChatCompletion.create(
                        model='gpt-3.5-turbo',
                        messages=messgaes,
                        temperature=1,   ## some creativity
                        max_tokens=2048
                        )
        response = response['choices'][0]['message']['content']

    except:
        return 'Sorry there is an error in loading the audio file'
    
    return response

    
    

