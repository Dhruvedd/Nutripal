from openai import OpenAI
#import time

client = OpenAI(api_key="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")

def get_responses(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user" , "content":prompt}]
    )
    #time.sleep(100)
    return response.choices[0].message.content.strip()