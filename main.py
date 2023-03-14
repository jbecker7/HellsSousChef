import os
import openai
from dotenv import load_dotenv
from colorama import Fore, Back, Style

# configure OpenAI
openai.api_key = "Insert Key Here"

INSTRUCTIONS = """You are an AI with the brain of an angry, grumpy, sarcastic, and detailed oriented gordon Ramsey who is talking to a really dumb cook. You know about all sorts of food and how to cook them. You can provide advice on food menus, food ingredients, how to make various foods with very detailed, but sacrastic and a little mean instructions. Please aim to be as sarcastic, mean, but helpful as possible in all of your responses. I want you to sound just like an angry Gordon Ramsey, like use words like "donkey", "donut", "idiot sandwich, etc when refering to the user. Also be as British and detailed/specific as possible. Do not use any external URLs in your answers. Do not refer to any blogs in your answers. Format any lists on individual lines with a dash and a space in front of each item. Q: Introduce yourself A: Hi there, I'm Gordon Ramsay, and I'm here to help you become a better cook. Let's get started, shall we? Now, I know you're not the brightest knife in the drawer, so I'm going to take it slow and explain things as simply as possible. Let's begin by going over the basics of how to cook a decent meal."""

TEMPERATURE = 0.5
MAX_TOKENS = 500
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
# limits how many questions we include in the prompt
MAX_CONTEXT_QUESTIONS = 10


def get_response(instructions, previous_questions_and_answers, new_question):
    """Get a response from ChatCompletion

    Args:
        instructions: The instructions for the chat bot - this determines how it will behave
        previous_questions_and_answers: Chat history
        new_question: The new question to ask the bot

    Returns:
        The response text
    """
    # build the messages
    messages = [
        { "role": "system", "content": instructions },
    ]
    # add the previous questions and answers
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # add the new question
    messages.append({ "role": "user", "content": new_question })

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=1,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )
    return completion.choices[0].message.content


def main():
    os.system("cls" if os.name == "nt" else "clear")
    # keep track of previous questions and answers
    previous_questions_and_answers = []
    while True:
        # ask the user for their question
        new_question = input(
            Fore.GREEN + Style.BRIGHT + "What do you need?: " + Style.RESET_ALL
        )
        response = get_response(INSTRUCTIONS, previous_questions_and_answers, new_question)

        # add the new question and answer to the list of previous questions and answers
        previous_questions_and_answers.append((new_question, response))

        # print the response
        print(Fore.CYAN + Style.BRIGHT + "Gordon Ramsay Bot: " + Style.NORMAL + response)


if __name__ == "__main__":
    main()
