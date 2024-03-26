from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
#import time

client = OpenAI(api_key = os.getenv('API_KEY'))

def get_responses(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user" , "content":prompt}]
    )
    #time.sleep(100)
    return response.choices[0].message.content.strip()