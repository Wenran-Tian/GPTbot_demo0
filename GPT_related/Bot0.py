import openai
import os
from dotenv import load_dotenv, find_dotenv


_ = load_dotenv(find_dotenv())
openai.api_key = os.environ.get('OPENAI_API_KEY')


def generate_app_ideas(prompt, num_ideas):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=50,
        n=num_ideas,
        stop=None,
        temperature=0.7,
        frequency_penalty=0.2,
        presence_penalty=0.0
    )
    ideas = [choice['text'].strip() for choice in response.choices]
    return ideas


prompt = "Generate 10 unique app ideas that leverage the power of the GPT-4 API"
num_ideas = 10
ideas = generate_app_ideas(prompt, num_ideas)

for i, idea in enumerate(ideas):
    print(f"Idea {i + 1}: {idea}")