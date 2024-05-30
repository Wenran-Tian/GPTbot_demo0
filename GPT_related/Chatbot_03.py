import os
import PyPDF2
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv



if __name__ == "__main__" :
    # print(load_dotenv(".env"))
    _ = load_dotenv(find_dotenv())
    print(os.environ.get('OPENAI_API_KEY'))
    # client = OpenAI(api_key=)
    model = "gpt-3.5-turbo"
    temperature = 0.3  # random degree
    max_tokens = 500
    topic = ""
    



