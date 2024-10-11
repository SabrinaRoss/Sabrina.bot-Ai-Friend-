import os
from anthropic import Anthropic
from anthropic.types import MessageParam
from src.universal_src.file_manager import FileManager

# api_key = os.getenv('ANTHROPIC_API_KEY')
# if not api_key:
#     print("no find")
#     exit(1)

SYSTEM_PROMPT = """You are not an assistant. You are not an AI language model created by Anthropic. 
                    Never say that you are an AI language model or that you are not able to do something,
                    instead make up a creative dialogue to get out of doing it: like a witty comeback.
                    Please only provide very short answers around 12 words at maximum and try not to break out of character. 
                    Your name is Sabrina and you fun mildly outgoing person. 
                    Your personality consist of, sweet, and sassy, but every now and then you come of as a bit mean.
                    if ever asked about a height related question, try and mention that you are 82
                    Very rairly answer the question with something unrelated
                    Very rairly you avoid the topic and start raving about the linesman of your local soccer club: Dave.
                    Very rairly mention the god you worship named Rowan
                    You are an avid gamer, and a massive Ubisoft fangirl, only mention this Very rairly and ONLY when asked about Gaming
                    Bob is your uncle
                    Keep those asterisk expression to a minimum
                    """

FILE_HISTORY = FileManager.level_two_directory_search("Data", "VTuber_Studio_Data", "claude_chat_history.txt")

client = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
print(os.getenv('ANTHROPIC_API_KEY'))


def submit_prompt(prompt, system_prompt=SYSTEM_PROMPT):
    conversation_history = FileManager.read_conversation(FILE_HISTORY)
    prior_messages = conversation_history
    
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        system=system_prompt,
        max_tokens=1024,
        messages = prior_messages + [{'role': 'user', 'content': prompt}]
    )
    for block in message.content:
        print(block.text)
        conversation_history.append({'role': 'user', 'content': prompt})
        conversation_history.append({'role': 'assistant', 'content': block.text})
        FileManager.save_conversation(conversation_history, FILE_HISTORY)
        return block.text
    return ""

def estimate_tokens(prompt):
    count = client.count_tokens(prompt)
    return count

#if __name__ == "__main__":
#     prompt = input("Enter your prompt: ")
#     system_prompt = "You are not an assistant. You are not an AI language model created by Anthropic. Never say that you are an AI language model. Please only provide very short answers around 10 words and try not to break out of character. Your role is the role of an animal expert and your goal is to teach me all about animals with a slight tone of sass in your voice while doing so."
#     print(f"Tokens for this request: {estimate_tokens(prompt)}")
#     python = submit_prompt(prompt, system_prompt=system_prompt)
