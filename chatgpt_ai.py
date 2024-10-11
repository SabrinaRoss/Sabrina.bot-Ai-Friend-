import os
import openai

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

CONTEXT = [
    {"role": "system", "content": "You are a big mucsle gym bro"}
]

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    CONTEXT.append({"role": "user", "content": user_input})

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages = CONTEXT
    )

    gpt_response = response['choices'][0]['message']['content']
    print(gpt_response)

    CONTEXT.append({"role": "assistant", "content": gpt_response})