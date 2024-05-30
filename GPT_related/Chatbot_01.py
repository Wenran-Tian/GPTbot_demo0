import openai
import gradio
import os
from dotenv import load_dotenv, find_dotenv


messages = []

_ = load_dotenv(find_dotenv())
client = openai.OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY')
)


def CustomGPTBot(message):
    messages.append({"role" : "system", "content" : message})
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",      # gpt-3.5-turbo
        messages = messages,
        temperature = 0.3,
    )
    reply = response.choices[0].message.content.strip()
    messages.append({"role": "assistant", "content": reply})
    return reply


demo = gradio.Interface(fn=CustomGPTBot, inputs="text", outputs="text", title="Your Title")
demo.launch()

#demo.launch(share = True)