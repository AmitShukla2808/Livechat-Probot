import os 
from groq import Groq
import pandas as pd
import time
import json

Groq_API_key = "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"

client = Groq(api_key=Groq_API_key)

def get_model_response(prompt, role='user'):
    chat_response = client.chat.completions.create(
        messages=[
            {
                "role": role,
                "content": prompt, 
            }
        ],
        model="llama3-70b-8192",
    )

    return chat_response.choices[0].message.content