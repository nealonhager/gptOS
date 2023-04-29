import os
import openai
import json
import pyttsx3

from message import Message, Prompt, Response
from dotenv import load_dotenv

load_dotenv()
engine = pyttsx3.init()
openai.api_key = os.getenv("OPENAI_API_KEY")


def main():
    resp = Response(
        openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[Prompt("what is the color of the sky?").to_dict()],
        )["choices"][0]["message"]["content"]
    )

    print(resp.to_json())
    engine.setProperty("rate", 150)
    engine.save_to_file(resp.content, "./test.mp3")
    engine.say(resp.content)
    engine.runAndWait()
    engine.stop()


if __name__ == "__main__":
    main()
