import openai
import os
from dotenv import load_dotenv, find_dotenv
import argparse
from datetime import datetime

GPT4_MODEL = "gpt-4-turbo"
GPT4o_MODEL = "gpt-4o"
GPT3P5_MODEL = "gpt-3.5-turbo"
EXIT_FLAG = "-exit"
SAVE_FLAG = "-save_current_dialogue"
CLO_FLAG = "c "
LOG_FOLDER = "logs"

RET_continue = 0
RET_exit = 1
RET_restart = 2


class GPTbot:
    def __init__(self, key, temperature=0.5, model=GPT4o_MODEL, name="", save_before_end=True):
        self.key = key
        self.msgs = []
        self.temperature = temperature
        self.client = openai.OpenAI(api_key=key)
        self.model = model
        if not name:
            name = self.__class__.__name__
        self.name = name
        self.parser = self.init_parser()
        self.save_before_end = save_before_end

    @staticmethod
    def init_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument('-e', "--exit", action='store_true')
        parser.add_argument('-sa', "--save_all", action='store_true')
        parser.add_argument('-slg', "--save_last_dialogue", type = int)
        parser.add_argument('-sl', "--save_last_reply", type = int)
        return parser

    def ask(self, question, role="system", model= "", temperature=0):
            if not model:
                model = self.model
            if not temperature:
                temperature = self.temperature
            self.msgs.append({"role" : role, "content" : question})
            response = self.client.chat.completions.create(
                model=model,
                messages=self.msgs,
                temperature=temperature
            )
            reply = response.choices[0].message.content.strip()
            self.msgs.append({"role": "assistant", "content": reply})
            return reply

    def start_demo(self):
        greetings = f"Greetings, this is {self.name}, what can I do for you?"
        self.msgs.append({"role": "assistant", "content": greetings})
        print(greetings)
        while 1:
            input_info = input()
            input_info, preprocess_res = self.input_preprocessing(input_info)
            if preprocess_res == RET_exit:
                return
            elif preprocess_res == RET_restart:
                print("Done")
                continue
            response = self.ask(input_info)
            print(response)

    def reset_parser_vals(self):
        self.parser.save_last_dialogue = None
        self.parser.save_last_reply = None
        self.save_all = None

    def input_preprocessing(self, input):
        if input == EXIT_FLAG:
            print("See you soon")
            return "", RET_exit
        if input.startswith(CLO_FLAG):
            input = input[len(CLO_FLAG):]
            self.reset_parser_vals()
            parse_res = self.parser.parse_args(input.split())
            if parse_res.save_last_dialogue:
                self.save_dialogue_to_file("dialogue", parse_res.save_last_dialogue)
            elif parse_res.save_last_reply:
                self.save_dialogue_to_file("reply", parse_res.save_last_reply)
            elif parse_res.save_all:
                self.save_dialogue_to_file("dialogue")
            elif "exit" in parse_res:
                if self.save_before_end:
                    self.save_dialogue_to_file("dialogue")
                return "", RET_exit
            return input, RET_restart
        else:
            return input, RET_continue

    def save_dialogue_to_file(self, mode, count = 0, prefix = ""):
        fn = LOG_FOLDER + "/"
        fn += prefix if prefix else self.name
        fn += datetime.today().strftime("%m%d_%H%M%S.txt")
        if not os.path.exists(LOG_FOLDER):
            os.mkdir(LOG_FOLDER)
        # print("flag 87")
        with open(fn, "w") as f:
            msg_num = len(self.msgs)
            if count:
                count *= 2
                count = count if msg_num > count else msg_num
            else:
                count = msg_num
            for i in range(count):
                ind = msg_num - count + i
                msg = self.msgs[ind]
                content = msg["content"]
                role = msg["role"]
                # print(content)
                if i % 2 == 0:
                    f.write(f"{role}:\n{content}\n\n")
                elif mode == "dialogue" and i % 2 == 1:
                    f.write(f"{role}:\n{content}\n\n")


if __name__ == "__main__":
    _ = load_dotenv(find_dotenv())
    bot01 = GPTbot(os.environ.get('OPENAI_API_KEY'), model = GPT4o_MODEL)
    bot01.start_demo()
    # parser = bot01.parser
    # parse_res = parser.parse_args("-sl 10".split())
    # print("save_last_reply" in parse_res)